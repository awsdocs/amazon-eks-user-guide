# Vertical Pod Autoscaler<a name="vertical-pod-autoscaler"></a>

The Kubernetes [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) automatically adjusts the CPU and memory reservations for your pods to help "right size" your applications\. This adjustment can improve cluster resource utilization and free up CPU and memory for other pods\. This topic helps you to deploy the Vertical Pod Autoscaler to your cluster and verify that it is working\.

## Install the Metrics Server<a name="vpa-install-metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster\. It is not deployed by default in Amazon EKS clusters, but it provides metrics that are required by the Vertical Pod Autoscaler\. This topic explains how to deploy the Kubernetes metrics server on your Amazon EKS cluster\.

**Note**  
You can also use Prometheus to provide metrics for the Vertical Pod Autoscaler\. For more information, see [Control Plane Metrics with Prometheus](prometheus.md)\.

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
   DOWNLOAD_URL=$(curl --silent "https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest" | jq -r .tarball_url)
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
If you are downloading to a remote server, you can use the following `curl` command, substituting the red text with the latest version number\.  

      ```
      curl -o v0.3.6.tar.gz https://github.com/kubernetes-sigs/metrics-server/archive/v0.3.6.tar.gz
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

## Deploy the Vertical Pod Autoscaler<a name="vpa-deploy"></a>

In this section, you deploy the Vertical Pod Autoscaler to your cluster\.

**To deploy the Vertical Pod Autoscaler**

1. Open a terminal window and navigate to a directory where you would like to download the Vertical Pod Autoscaler source code\. 

1. Clone the [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler) GitHub repository\.

   ```
   git clone https://github.com/kubernetes/autoscaler.git
   ```

1. Change to the `vertical-pod-autoscaler` directory\.

   ```
   cd autoscaler/vertical-pod-autoscaler/
   ```

1. \(Optional\) If you have already deployed another version of the Vertical Pod Autoscaler, remove it with the following command\.

   ```
   ./hack/vpa-down.sh
   ```

1. Deploy the Vertical Pod Autoscaler to your cluster with the following command\.

   ```
   ./hack/vpa-up.sh
   ```

1. Verify that the Vertical Pod Autoscaler pods have been created successfully\.

   ```
   kubectl get pods -n kube-system
   ```

   Output:

   ```
   NAME                                        READY   STATUS    RESTARTS   AGE
   aws-node-949vx                              1/1     Running   0          122m
   aws-node-b4nj8                              1/1     Running   0          122m
   coredns-6c75b69b98-r9x68                    1/1     Running   0          133m
   coredns-6c75b69b98-rt9bp                    1/1     Running   0          133m
   kube-proxy-bkm6b                            1/1     Running   0          122m
   kube-proxy-hpqm2                            1/1     Running   0          122m
   metrics-server-8459fc497-kfj8w              1/1     Running   0          83m
   vpa-admission-controller-68c748777d-ppspd   1/1     Running   0          7s
   vpa-recommender-6fc8c67d85-gljpl            1/1     Running   0          8s
   vpa-updater-786b96955c-bgp9d                1/1     Running   0          8s
   ```

## Test your Vertical Pod Autoscaler Installation<a name="vpa-sample-app"></a>

In this section, you deploy a sample application to verify that the Vertical Pod Autoscaler is working\.

**To test your Vertical Pod Autoscaler installation**

1. Deploy the `hamster.yaml` Vertical Pod Autoscaler example with the following command\.

   ```
   kubectl apply -f examples/hamster.yaml
   ```

1. Get the pods from the `hamster` example application\.

   ```
   kubectl get pods -l app=hamster
   ```

   Output:

   ```
   hamster-c7d89d6db-rglf5   1/1     Running   0          48s
   hamster-c7d89d6db-znvz5   1/1     Running   0          48s
   ```

1. Describe one of the pods to view its CPU and memory reservation\.

   ```
   kubectl describe pod hamster-c7d89d6db-rglf5
   ```

   Output:

   ```
   Name:           hamster-c7d89d6db-rglf5
   Namespace:      default
   Priority:       0
   Node:           ip-192-168-9-44.us-west-2.compute.internal/192.168.9.44
   Start Time:     Fri, 27 Sep 2019 10:35:15 -0700
   Labels:         app=hamster
                   pod-template-hash=c7d89d6db
   Annotations:    kubernetes.io/psp: eks.privileged
                   vpaUpdates: Pod resources updated by hamster-vpa: container 0:
   Status:         Running
   IP:             192.168.23.42
   IPs:            <none>
   Controlled By:  ReplicaSet/hamster-c7d89d6db
   Containers:
     hamster:
       Container ID:  docker://e76c2413fc720ac395c33b64588c82094fc8e5d590e373d5f818f3978f577e24
       Image:         k8s.gcr.io/ubuntu-slim:0.1
       Image ID:      docker-pullable://k8s.gcr.io/ubuntu-slim@sha256:b6f8c3885f5880a4f1a7cf717c07242eb4858fdd5a84b5ffe35b1cf680ea17b1
       Port:          <none>
       Host Port:     <none>
       Command:
         /bin/sh
       Args:
         -c
         while true; do timeout 0.5s yes >/dev/null; sleep 0.5s; done
       State:          Running
         Started:      Fri, 27 Sep 2019 10:35:16 -0700
       Ready:          True
       Restart Count:  0
       Requests:
         cpu:        100m
         memory:     50Mi
   ...
   ```

   You can see that the original pod reserves 100 millicpu of CPU and 50 Mebibytes of memory\. For this example application, 100 millicpu is less than the pod needs to run, so it is CPU\-constrained\. It also reserves much less memory than it needs\. The Vertical Pod Autoscaler `vpa-recommender` deployment analyzes the `hamster` pods to see if the CPU and memory requirements are appropriate\. If adjustments are needed, the `vpa-updater` relaunches the pods with updated values\.

1. Wait for the `vpa-updater` to launch a new `hamster` pod\. This should take a minute or two\. You can monitor the pods with the following command\.
**Note**  
If you are not sure that a new pod has launched, compare the pod names with your previous list\. When the new pod launches, you will see a new pod name\.

   ```
   kubectl get --watch pods -l app=hamster
   ```

1. When a new `hamster` pod is started, describe it and view the updated CPU and memory reservations\.

   ```
   kubectl describe pod hamster-c7d89d6db-jxgfv
   ```

   Output:

   ```
   Name:           hamster-c7d89d6db-jxgfv
   Namespace:      default
   Priority:       0
   Node:           ip-192-168-9-44.us-west-2.compute.internal/192.168.9.44
   Start Time:     Fri, 27 Sep 2019 10:37:08 -0700
   Labels:         app=hamster
                   pod-template-hash=c7d89d6db
   Annotations:    kubernetes.io/psp: eks.privileged
                   vpaUpdates: Pod resources updated by hamster-vpa: container 0: cpu request, memory request
   Status:         Running
   IP:             192.168.3.140
   IPs:            <none>
   Controlled By:  ReplicaSet/hamster-c7d89d6db
   Containers:
     hamster:
       Container ID:  docker://2c3e7b6fb7ce0d8c86444334df654af6fb3fc88aad4c5d710eac3b1e7c58f7db
       Image:         k8s.gcr.io/ubuntu-slim:0.1
       Image ID:      docker-pullable://k8s.gcr.io/ubuntu-slim@sha256:b6f8c3885f5880a4f1a7cf717c07242eb4858fdd5a84b5ffe35b1cf680ea17b1
       Port:          <none>
       Host Port:     <none>
       Command:
         /bin/sh
       Args:
         -c
         while true; do timeout 0.5s yes >/dev/null; sleep 0.5s; done
       State:          Running
         Started:      Fri, 27 Sep 2019 10:37:08 -0700
       Ready:          True
       Restart Count:  0
       Requests:
         cpu:        587m
         memory:     262144k
   ...
   ```

   Here you can see that the CPU reservation has increased to 587 millicpu, which is over five times the original value\. The memory has increased to 262,144 Kilobytes, which is around 250 Mebibytes, or five times the original value\. This pod was under\-resourced, and the Vertical Pod Autoscaler corrected our estimate with a much more appropriate value\.

1. Describe the `hamster-vpa` resource to view the new recommendation\.

   ```
   kubectl describe vpa/hamster-vpa
   ```

   Output:

   ```
   Name:         hamster-vpa
   Namespace:    default
   Labels:       <none>
   Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                   {"apiVersion":"autoscaling.k8s.io/v1beta2","kind":"VerticalPodAutoscaler","metadata":{"annotations":{},"name":"hamster-vpa","namespace":"d...
   API Version:  autoscaling.k8s.io/v1beta2
   Kind:         VerticalPodAutoscaler
   Metadata:
     Creation Timestamp:  2019-09-27T18:22:51Z
     Generation:          23
     Resource Version:    14411
     Self Link:           /apis/autoscaling.k8s.io/v1beta2/namespaces/default/verticalpodautoscalers/hamster-vpa
     UID:                 d0d85fb9-e153-11e9-ae53-0205785d75b0
   Spec:
     Target Ref:
       API Version:  apps/v1
       Kind:         Deployment
       Name:         hamster
   Status:
     Conditions:
       Last Transition Time:  2019-09-27T18:23:28Z
       Status:                True
       Type:                  RecommendationProvided
     Recommendation:
       Container Recommendations:
         Container Name:  hamster
         Lower Bound:
           Cpu:     550m
           Memory:  262144k
         Target:
           Cpu:     587m
           Memory:  262144k
         Uncapped Target:
           Cpu:     587m
           Memory:  262144k
         Upper Bound:
           Cpu:     21147m
           Memory:  387863636
   Events:          <none>
   ```

1. When you finish experimenting with the example application, you can delete it with the following command\.

   ```
   kubectl delete -f examples/hamster.yaml
   ```