# Fargate pod configuration<a name="fargate-pod-configuration"></a>

This section describes some of the unique pod configuration details for running Kubernetes pods on AWS Fargate\.

## Pod CPU and memory<a name="fargate-cpu-and-memory"></a>

With Kubernetes, you can define requests, a minimum vCPU amount, and memory resources that are allocated to each container in a pod\. Pods are scheduled by Kubernetes to ensure that at least the requested resources for each pod are available on the compute resource\. For more information, see [Managing compute resources for containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) in the Kubernetes documentation\.

**Note**  
Since Amazon EKS Fargate runs only one pod per node, the scenario of evicting pods in case of fewer resources doesn't occur\. All Amazon EKS Fargate pods run with guaranteed priority, so the requested CPU and memory must be equal to the limit for all of the containers\. For more information, see [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) in the Kubernetes documentation\.

When pods are scheduled on Fargate, the vCPU and memory reservations within the pod specification determine how much CPU and memory to provision for the pod\.
+ The maximum request out of any Init containers is used to determine the Init request vCPU and memory requirements\.
+ Requests for all long\-running containers are added up to determine the long\-running request vCPU and memory requirements\.
+ The larger of the above two values is chosen for the vCPU and memory request to use for your pod\.
+ Fargate adds 256 MB to each pod's memory reservation for the required Kubernetes components \(`kubelet`, `kube-proxy`, and `containerd`\)\.

Fargate rounds up to the compute configuration shown below that most closely matches the sum of vCPU and memory requests in order to ensure pods always have the resources that they need to run\.

If you do not specify a vCPU and memory combination, then the smallest available combination is used \(\.25 vCPU and 0\.5 GB memory\)\.

The following table shows the vCPU and memory combinations that are available for pods running on Fargate\. 


|  vCPU value  |  Memory value  | 
| --- | --- | 
|  \.25 vCPU  |  0\.5 GB, 1 GB, 2 GB  | 
|  \.5 vCPU  |  1 GB, 2 GB, 3 GB, 4 GB  | 
|  1 vCPU  |  2 GB, 3 GB, 4 GB, 5 GB, 6 GB, 7 GB, 8 GB  | 
|  2 vCPU  |  Between 4 GB and 16 GB in 1\-GB increments  | 
|  4 vCPU  |  Between 8 GB and 30 GB in 1\-GB increments  | 

The additional memory reserved for the Kubernetes components can cause a Fargate task with more vCPUs than requested to be provisioned\. For example, a request for 1 vCPU and 8 GB memory will have 256 MB added to its memory request, and will provision a Fargate task with 2 vCPUs and 9 GB memory, since no task with 1 vCPU and 9 GB memory is available\.

There is no correlation between the size of the pod running on Fargate and the node size reported by Kubernetes with `kubectl get nodes`\. The reported node size is often larger than the pod's capacity\. You can verify pod capacity with the following command\. Replace `<pod-name>` \(including `<>`\) with the name of your pod\.

```
kubectl describe pod <pod-name>
```

The output is as follows\.

```
...
annotations:
    CapacityProvisioned: 0.25vCPU 0.5GB
...
```

The `CapacityProvisioned` annotation represents the enforced pod capacity and it determines the cost of your pod running on Fargate\. For pricing information for the compute configurations, see [AWS Fargate Pricing](http://aws.amazon.com/fargate/pricing/)\.

## Fargate storage<a name="fargate-storage"></a>

When provisioned, each pod running on Fargate receives 20 GB of container image layer storage\. Pod storage is ephemeral\. After a pod stops, the storage is deleted\. New pods launched onto Fargate on or after May 28, 2020, have encryption of the ephemeral storage volume enabled by default\. The ephemeral pod storage is encrypted with an AES\-256 encryption algorithm using AWS Fargate managed keys\.

**Note**  
The usable storage for Amazon EKS pods that run on Fargate is less than 20 GB because some space is used by the `kubelet` and other Kubernetes modules that are loaded inside the pod\.