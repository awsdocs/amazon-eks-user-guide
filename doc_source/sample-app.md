# Deploy a sample application to test the AWS Distro for OpenTelemetry Collector<a name="sample-app"></a>

The sample application will generate and send OTLP data to any of the services that you have configured through the AWS Distro for OpenTelemetry [\(ADOT\) Collector deployment](deploy-collector.md)\. This step is optional if you already have an application running inside your cluster that can produce data\. Consult your application’s documentation to ensure that data is sent to the correct endpoints\. The sample application set up includes applying two YAML files:
+ A [traffic generator file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/traffic-generator.yaml) `traffic-generator.yaml`
+ A [sample app file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/sample-app.yaml) `sample-app.yaml`

The sample application and traffic generator were largely taken from an example in the [ADOT Collector repository](https://github.com/aws-observability/aws-otel-collector/blob/main/examples/docker/docker-compose.yaml)\. A `docker-compose.yaml `file was translated to Kubernetes resources using the [Kompose tool](https://kompose.io/)\.

`traffic-generator.yaml `makes http calls to the Kubernetes service `sample-app:4567`\. This allows our traffic generator to interact with our sample application on port 4567\. `sample-app` resolves to the IP address of the `sample-app` pod\. Ensure that the `kind` value reflects your deployment mode\.

`traffic-generator.yaml`

```
apiVersion: v1
metadata:
  labels:
    io.kompose.service: traffic-generator
  name: traffic-generator
spec:
  ports:
    - name: "80"
      port: 80
      targetPort: 80
  selector:
    io.kompose.service: traffic-generator
status:
  loadBalancer: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    io.kompose.service: traffic-generator
  name: traffic-generator
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: traffic-generator
  strategy: {}
  template:
    metadata:
      labels:
        io.kompose.service: traffic-generator
    spec:
      containers:
        - args:
            - /bin/bash
            - -c
            - sleep 10; while :; do curl sample-app:4567/outgoing-http-call > /dev/null 1>&1; sleep 2; curl sample-app:4567/aws-sdk-call > /dev/null 2>&1; sleep 5; done
          image: ellerbrock/alpine-bash-curl-ssl:latest
          name: traffic-generator
          ports:
            - containerPort: 80
          resources: {}
      restartPolicy: Always
status: {}
```

`sample-app.yaml`
+ The Service resource configures port:4567 to allow HTTP requests for our traffic generator\.
+ The Deployment resource configures some environment variables:
  + AWS\_REGION should be your AWS Region\.
  + The LISTEN\_ADDRESS is configured to 0\.0\.0\.0:4567 for HTTP requests from our traffic generator\.
  + The OTEL\_EXPORTER\_OTLP\_ENDPOINT has a value of http://my\-collector\-collector:4317\. my\-collector\-collector is the name of the Kubernetes service that allows our sample application to interact with our ADOT Collector on port 4317\. In the ADOT Collector configuration, the ADOT Collector receives metrics/traces from an endpoint: 0\.0\.0\.0:4317\. 

```
apiVersion: v1
kind: Service
metadata:
  labels:
    io.kompose.service: sample-app
  name: sample-app
spec:
  ports:
    - name: "4567"
      port: 4567
      targetPort: 4567
  selector:
    io.kompose.service: sample-app
status:
  loadBalancer: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    io.kompose.service: sample-app
  name: sample-app
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: sample-app
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        io.kompose.service: sample-app
    spec:
      containers:
        - env:
            - name: AWS_REGION
              value: <AWS_REGION>
            - name: LISTEN_ADDRESS
              value: 0.0.0.0:4567
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http://my-collector-collector:4317
            - name: OTEL_RESOURCE_ATTRIBUTES
              value: service.namespace=AOCDockerDemo,service.name=AOCDockerDemoService
          image: public.ecr.aws/aws-otel-test/aws-otel-java-test-spark:v0.11.0
          name: sample-app
          ports:
            - containerPort: 4567
          resources: {}
      restartPolicy: Always
status: {}
```

## Deploy the traffic generator and sample application<a name="adot-sample"></a>

To apply the traffic generator and sample application, use the following commands for each YAML:

```
kubectl apply -f traffic-generator.yaml
```

```
kubectl apply -f sample-app.yaml
```