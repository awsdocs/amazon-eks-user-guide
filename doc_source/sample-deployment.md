# Deploy a sample Linux application<a name="sample-deployment"></a>

In this topic, you create a Kubernetes manifest and deploy it to your cluster\.

**Prerequisites**
+ You must have an existing Kubernetes cluster to deploy a sample application\. If you don't have an existing cluster, you can deploy an Amazon EKS cluster using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ You must have `kubectl` installed on your computer\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ `kubectl` must be configured to communicate with your cluster\. For more information, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\.

**To deploy a sample application**

1. Create a Kubernetes namespace for the sample app\.

   ```
   kubectl create namespace my-namespace
   ```

1. Create a Kubernetes service and deployment\. 

   1. Save the following contents to a file named `sample-service.yaml` on your computer\. If you're deploying to [AWS Fargate](fargate.md) pods, then make sure that the value for `namespace` matches the namespace that you defined in your [AWS Fargate profile](fargate-profile.md)\. This sample deployment will pull a container image from a public repository, deploy three instances of it to your cluster, and create a Kubernetes service with its own IP address that can be accessed from within the cluster only\. To access the service from outside the cluster, you need to deploy a [load balancer](load-balancing-and-ingress.md) or [ALB Ingress Controller\.](alb-ingress.md)

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: my-service
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        selector:
          app: my-app
        ports:
          - protocol: TCP
            port: 80
            targetPort: 80
      ---
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: my-app
        template:
          metadata:
            labels:
              app: my-app
          spec:
            containers:
            - name: nginx
              image: nginx:1.14.2
              ports:
              - containerPort: 80
      ```

      To learn more about Kubernetes [services](https://kubernetes.io/docs/concepts/services-networking/service/) and [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), see the Kubernetes documentation\. The containers in the sample manifest do not use network storage, but they may be able to\. For more information, see [Storage](storage.md)\. Though not implemented in this example, we recommend that you create Kubernetes service accounts for your pods, and associate them to AWS IAM accounts\. Specifying service accounts enables your pods to have the minimum permissions that they require to interact with other services\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md)

   1. Deploy the application\.

      ```
      kubectl apply -f sample-service.yaml
      ```

1. View all resources that exist in the `my-namespace` namespace\.

   ```
   kubectl get all -n my-namespace
   ```

   Output

   ```
   NAME                                 READY   STATUS    RESTARTS   AGE
   pod/my-deployment-776d8f8fd8-78w66   1/1     Running   0          27m
   pod/my-deployment-776d8f8fd8-dkjfr   1/1     Running   0          27m
   pod/my-deployment-776d8f8fd8-wmqj6   1/1     Running   0          27m
   
   NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
   service/my-service   ClusterIP   10.100.190.12   <none>        80/TCP    32m
   
   NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/my-deployment   3/3     3            3           27m
   
   NAME                                       DESIRED   CURRENT   READY   AGE
   replicaset.apps/my-deployment-776d8f8fd8   3         3         3       27m
   ```

   In the output, you see the service and deployment that are specified in the sample manifest deployed in the previous step\. You also see three pods, which are due to specifying `3` for `replicas` in the sample manifest\. For more information about pods, see [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) in the Kubernetes documentation\. Kubernetes automatically created the `replicaset` resource, even though it wasn't specified in the sample manifest\. For more information about ReplicaSets, see [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) in the Kubernetes documentation\.
**Note**  
Kubernetes will maintain the number of replicas specified in the manifest\. If this were a production deployment and you wanted Kubernetes to horizontally scale the number of replicas or vertically scale the compute resources for the pods, you'd need to use the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) and the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md)\.

1. View the details of the deployed service\.

   ```
   kubectl -n my-namespace describe service my-service
   ```

   Abbreviated output

   ```
   Name:              my-service
   Namespace:         my-namespace
   Labels:            app=my-app
   Annotations:       kubectl.kubernetes.io/last-applied-configuration:
                        {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"app":"my-app"},"name":"my-service","namespace":"my-namespace"}...
   Selector:          app=my-app
   Type:              ClusterIP
   IP:                10.100.190.12
   Port:              <unset>  80/TCP
   TargetPort:        80/TCP
   ...
   ```

   In the output, the value for `IP:` is a unique IP address that can be reached from any pod within the cluster\.

1. View the details of one of the pods that was deployed\.

   ```
   kubectl -n my-namespace describe pod my-deployment-776d8f8fd8-78w66
   ```

   Abbreviated output

   ```
   Name:         my-deployment-776d8f8fd8-78w66
   Namespace:    my-namespace
   Priority:     0
   Node:         ip-192-168-9-36.us-west-2.compute.internal/192.168.9.36
   ...
   IP:           192.168.16.57
   IPs:
     IP:           192.168.16.57
   Controlled By:  ReplicaSet/my-deployment-776d8f8fd8
   ...
   Conditions:
     Type              Status
     Initialized       True
     Ready             True
     ContainersReady   True
     PodScheduled      True
   ...
   Events:
     Type    Reason     Age    From                                                 Message
     ----    ------     ----   ----                                                 -------
     Normal  Scheduled  3m20s  default-scheduler                                    Successfully assigned my-namespace/my-deployment-776d8f8fd8-78w66 to ip-192-168-9-36.us-west-2.compute.internal
   ...
   ```

   In the output, the value for `IP:` is a unique IP that is assigned to the pod from the CIDR block assigned to the subnet that the worker node is in, by default\. If you'd prefer that pods be assigned IP addresses from different CIDR blocks than the subnet that the worker node is in, you can change the default behavior\. For more information, see [CNI custom networking](cni-custom-network.md)\. You can also see that the Kubernetes scheduler scheduled the pod on the worker node with the IP address `192.168.9.36`\.

1. Execute a shell on one of the pods by replacing the *value* below with a value returned for one of your pods in step 3\.

   ```
   kubectl exec -it my-deployment-776d8f8fd8-78w66 -n my-namespace -- /bin/bash
   ```

1. View the DNS resolver configuration file\.

   ```
   cat /etc/resolv.conf
   ```

   Output

   ```
   nameserver 10.100.0.10
   search my-namespace.svc.cluster.local svc.cluster.local cluster.local us-west-2.compute.internal
   options ndots:5
   ```

   In the previous output, the value for `nameserver` is the cluster's nameserver and is automatically assigned as the name server for any pod deployed to the cluster\.

1. Disconnect from the pod by typing `exit`\.

1. Remove the sample service, deployment, pods, and namespace\.

   ```
   kubectl delete namespace my-namespace
   ```