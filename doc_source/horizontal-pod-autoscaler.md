# Horizontal Pod Autoscaler<a name="horizontal-pod-autoscaler"></a>

The Kubernetes [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) automatically scales the number of pods in a deployment, replication controller, or replica set based on that resource's CPU utilization\. This can help your applications scale out to meet increased demand or scale in when resources are not needed, thus freeing up your worker nodes for other applications\. When you set a target CPU utilization percentage, the Horizontal Pod Autoscaler scales your application in or out to try to meet that target\.

The Horizontal Pod Autoscaler is a standard API resource in Kubernetes that simply requires that a metrics source \(such as the Kubernetes metrics server\) is installed on your Amazon EKS cluster to work\. You do not need to deploy or install the Horizontal Pod Autoscaler on your cluster to begin scaling your applications\. For more information, see [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) in the Kubernetes documentation\.

Use this topic to prepare the Horizontal Pod Autoscaler for your Amazon EKS cluster and to verify that it is working with a sample application\.

**Note**  
This topic is based on the [Horizontal Pod Autoscaler Walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) in the Kubernetes documentation\.

## Install the Metrics Server<a name="hpa-install-metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster\. The metrics server is not deployed by default in Amazon EKS clusters, but it provides metrics that are required by the Horizontal Pod Autoscaler\. This topic explains how to deploy the Kubernetes metrics server on your Amazon EKS cluster\.

If you have already deployed the metrics server to your cluster, you can move on to the next section\. You can check for the metrics server with the following command\.

```
kubectl -n kube-system get deployment/metrics-server
```

If this command returns a `NotFound` error, then you must deploy the metrics server to your Amazon EKS cluster\. Choose the tab below that corresponds to your preferred installation method\.

------
#### [ curl and jq ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using `curl` and `jq`**

If you have a macOS or Linux system with `curl`, `tar`, `gzip`, and the `jq` JSON parser installed, you can download, extract, and install the latest release with the following commands\. Otherwise, use the next procedure to download the latest version using a web browser\.

1. Open a terminal window and navigate to a directory where you would like to download the latest `metrics-server` release\. 

1. Copy and paste the commands below into your terminal window and type **Enter** to execute them\. These commands download the latest release, extract it, and apply the version 1\.8\+ manifests to your cluster\.

   ```
   DOWNLOAD_URL=$(curl -Ls "https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest" | jq -r .tarball_url)
   DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
   curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
   mkdir metrics-server-$DOWNLOAD_VERSION
   tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
   kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------
#### [ Web browser ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using a web browser**

1. Download and extract the latest version of the metrics server code from GitHub\.

   1. Navigate to the latest release page of the `metrics-server` project on GitHub \([https://github\.com/kubernetes\-sigs/metrics\-server/releases/latest](https://github.com/kubernetes-sigs/metrics-server/releases/latest)\), then choose a source code archive for the latest release to download it\.
**Note**  
If you are downloading to a remote server, you can use the following `wget` command, substituting the *alternate\-colored* text with the latest version number\.  

      ```
      wget -O v0.3.6.tar.gz https://codeload.github.com/kubernetes-sigs/metrics-server/tar.gz/v0.3.6
      ```

   1. Navigate to your downloads location and extract the source code archive\. For example, if you downloaded the `.tar.gz` archive, use the following command to extract \(substituting your release version\)\. 

      ```
      tar -xzf v0.3.6.tar.gz
      ```

1. Apply all of the YAML manifests in the `metrics-server-0.3.6/deploy/1.8+` directory \(substituting your release version\)\.

   ```
   kubectl apply -f metrics-server-0.3.6/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------

## Run a Horizontal Pod Autoscaler Test Application<a name="hpa-sample-app"></a>

In this section, you deploy a sample application to verify that the Horizontal Pod Autoscaler is working\.

**Note**  
This example is based on the [Horizontal Pod Autoscaler Walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) in the Kubernetes documentation\.

**To test your Horizontal Pod Autoscaler installation**

1. Create a simple Apache web server application with the following command\.

   ```
   kubectl run httpd --image=httpd --requests=cpu=100m --limits=cpu=200m --expose --port=80
   ```

   This Apache web server pod is given 100 millicpu and 200 megabytes of memory, and it is serving on port 80\.

1. Create a Horizontal Pod Autoscaler resource for the `httpd` deployment\.

   ```
   kubectl autoscale deployment httpd --cpu-percent=50 --min=1 --max=10
   ```

   This command creates an autoscaler that targets 50 percent CPU utilization for the deployment, with a minimum of one pod and a maximum of ten pods\. When the average CPU load is below 50 percent, the autoscaler tries to reduce the number of pods in the deployment, to a minimum of one\. When the load is greater than 50 percent, the autoscaler tries to increase the number of pods in the deployment, up to a maximum of ten\. For more information, see [How does the Horizontal Pod Autoscaler work?](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#how-does-the-horizontal-pod-autoscaler-work) in the Kubernetes documentation\.

1. Describe the autoscaler with the following command to view its details\.

   ```
   kubectl describe hpa/httpd
   ```

   Output:

   ```
   Name:                                                  httpd
   Namespace:                                             default
   Labels:                                                <none>
   Annotations:                                           <none>
   CreationTimestamp:                                     Fri, 27 Sep 2019 13:32:15 -0700
   Reference:                                             Deployment/httpd
   Metrics:                                               ( current / target )
     resource cpu on pods  (as a percentage of request):  1% (1m) / 50%
   Min replicas:                                          1
   Max replicas:                                          10
   Deployment pods:                                       1 current / 1 desired
   Conditions:
     Type            Status  Reason              Message
     ----            ------  ------              -------
     AbleToScale     True    ReadyForNewScale    recommended size matches current size
     ScalingActive   True    ValidMetricFound    the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
     ScalingLimited  False   DesiredWithinRange  the desired count is within the acceptable range
   Events:           <none>
   ```

   As you can see, the current CPU load is only one percent, but the pod count is already at its lowest boundary \(one\), so it cannot scale in\.

1. Create a load for the web server\. The following command uses the Apache Bench program to send hundreds of thousands of requests to the `httpd` server\. This should significantly increase the load and cause the autoscaler to scale out the deployment\.

   ```
   kubectl run apache-bench -i --tty --rm --image=httpd -- ab -n 500000 -c 1000 http://httpd.default.svc.cluster.local/
   ```

1. Watch the `httpd` deployment scale out while the load is generated\. To watch the deployment and the autoscaler, periodically run the following command\.

   ```
   kubectl get horizontalpodautoscaler.autoscaling/httpd
   ```

   Output:

   ```
   NAME    REFERENCE          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
   httpd   Deployment/httpd   76%/50%   1         10        10         4m50s
   ```

   When the load finishes, the deployment should scale back down to 1\. 

1. When you are done experimenting with your sample application, delete the `httpd` resources\.

   ```
   kubectl delete deployment.apps/httpd service/httpd horizontalpodautoscaler.autoscaling/httpd
   ```