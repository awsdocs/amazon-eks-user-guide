# Vertical Pod Autoscaler<a name="vertical-pod-autoscaler"></a>

The Kubernetes [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) automatically adjusts the CPU and memory reservations for your Pods to help "right size" your applications\. This adjustment can improve cluster resource utilization and free up CPU and memory for other Pods\. This topic helps you to deploy the Vertical Pod Autoscaler to your cluster and verify that it is working\.

**Prerequisites**
+ You have an existing Amazon EKS cluster\. If you don't, see [Getting started with Amazon EKS](getting-started.md)\.
+ You have the Kubernetes Metrics Server installed\. For more information, see [Installing the Kubernetes Metrics Server](metrics-server.md)\.
+ You are using a `kubectl` client that is [configured to communicate with your Amazon EKS cluster](getting-started-console.md#eks-configure-kubectl)\.
+ OpenSSL `1.1.1` or later installed on your device\.

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

1. If your nodes don't have internet access to the `registry.k8s.io` container registry, then you need to pull the following images and push them to your own private repository\. For more information about how to pull the images and push them to your own private repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

   ```
   registry.k8s.io/autoscaling/vpa-admission-controller:0.10.0
   registry.k8s.io/autoscaling/vpa-recommender:0.10.0
   registry.k8s.io/autoscaling/vpa-updater:0.10.0
   ```

   If you're pushing the images to a private Amazon ECR repository, then replace `registry.k8s.io` in the manifests with your registry\. Replace `111122223333` with your account ID\. Replace `region-code` with the AWS Region that your cluster is in\. The following commands assume that you named your repository the same as the repository name in the manifest\. If you named your repository something different, then you'll need to change it too\.

   ```
   sed -i.bak -e 's/registry.k8s.io/111122223333.dkr.ecr.region-code.amazonaws.com/' ./deploy/admission-controller-deployment.yaml
   sed -i.bak -e 's/registry.k8s.io/111122223333.dkr.ecr.region-code.amazonaws.com/' ./deploy/recommender-deployment.yaml
   sed -i.bak -e 's/registry.k8s.io/111122223333.dkr.ecr.region-code.amazonaws.com/' ./deploy/updater-deployment.yaml
   ```

1. Deploy the Vertical Pod Autoscaler to your cluster with the following command\.

   ```
   ./hack/vpa-up.sh
   ```

1. Verify that the Vertical Pod Autoscaler Pods have been created successfully\.

   ```
   kubectl get pods -n kube-system
   ```

   An example output is as follows\.

   ```
   NAME                                        READY   STATUS    RESTARTS   AGE
   [...]
   metrics-server-8459fc497-kfj8w              1/1     Running   0          83m
   vpa-admission-controller-68c748777d-ppspd   1/1     Running   0          7s
   vpa-recommender-6fc8c67d85-gljpl            1/1     Running   0          8s
   vpa-updater-786b96955c-bgp9d                1/1     Running   0          8s
   ```

## Test your Vertical Pod Autoscaler installation<a name="vpa-sample-app"></a>

In this section, you deploy a sample application to verify that the Vertical Pod Autoscaler is working\.

**To test your Vertical Pod Autoscaler installation**

1. Deploy the `hamster.yaml` Vertical Pod Autoscaler example with the following command\.

   ```
   kubectl apply -f examples/hamster.yaml
   ```

1. Get the Pods from the `hamster` example application\.

   ```
   kubectl get pods -l app=hamster
   ```

   An example output is as follows\.

   ```
   hamster-c7d89d6db-rglf5   1/1     Running   0          48s
   hamster-c7d89d6db-znvz5   1/1     Running   0          48s
   ```

1. Describe one of the Pods to view its `cpu` and `memory` reservation\. Replace `c7d89d6db-rglf5` with one of the IDs returned in your output from the previous step\.

   ```
   kubectl describe pod hamster-c7d89d6db-rglf5
   ```

   An example output is as follows\.

   ```
   [...]
   Containers:
     hamster:
       Container ID:  docker://e76c2413fc720ac395c33b64588c82094fc8e5d590e373d5f818f3978f577e24
       Image:         registry.k8s.io/ubuntu-slim:0.1
       Image ID:      docker-pullable://registry.k8s.io/ubuntu-slim@sha256:b6f8c3885f5880a4f1a7cf717c07242eb4858fdd5a84b5ffe35b1cf680ea17b1
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
   [...]
   ```

   You can see that the original Pod reserves 100 millicpu of CPU and 50 mebibytes of memory\. For this example application, 100 millicpu is less than the Pod needs to run, so it is CPU\-constrained\. It also reserves much less memory than it needs\. The Vertical Pod Autoscaler `vpa-recommender` deployment analyzes the `hamster` Pods to see if the CPU and memory requirements are appropriate\. If adjustments are needed, the `vpa-updater` relaunches the Pods with updated values\.

1. Wait for the `vpa-updater` to launch a new `hamster` Pod\. This should take a minute or two\. You can monitor the Pods with the following command\.
**Note**  
If you are not sure that a new Pod has launched, compare the Pod names with your previous list\. When the new Pod launches, you will see a new Pod name\.

   ```
   kubectl get --watch Pods -l app=hamster
   ```

1. When a new `hamster` Pod is started, describe it and view the updated CPU and memory reservations\.

   ```
   kubectl describe pod hamster-c7d89d6db-jxgfv
   ```

   An example output is as follows\.

   ```
   [...]
   Containers:
     hamster:
       Container ID:  docker://2c3e7b6fb7ce0d8c86444334df654af6fb3fc88aad4c5d710eac3b1e7c58f7db
       Image:         registry.k8s.io/ubuntu-slim:0.1
       Image ID:      docker-pullable://registry.k8s.io/ubuntu-slim@sha256:b6f8c3885f5880a4f1a7cf717c07242eb4858fdd5a84b5ffe35b1cf680ea17b1
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
   [...]
   ```

   In the previous output, you can see that the `cpu` reservation increased to 587 millicpu, which is over five times the original value\. The `memory` increased to 262,144 Kilobytes, which is around 250 mebibytes, or five times the original value\. This Pod was under\-resourced, and the Vertical Pod Autoscaler corrected the estimate with a much more appropriate value\.

1. Describe the `hamster-vpa` resource to view the new recommendation\.

   ```
   kubectl describe vpa/hamster-vpa
   ```

   An example output is as follows\.

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