# Fargate Pod configuration<a name="fargate-pod-configuration"></a>

**Important**  
AWS Fargate with Amazon EKS isn't available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

This section describes some of the unique Pod configuration details for running Kubernetes Pods on AWS Fargate\.

## Pod CPU and memory<a name="fargate-cpu-and-memory"></a>

With Kubernetes, you can define requests, a minimum vCPU amount, and memory resources that are allocated to each container in a Pod\. Pods are scheduled by Kubernetes to ensure that at least the requested resources for each Pod are available on the compute resource\. For more information, see [Managing compute resources for containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) in the Kubernetes documentation\.

**Note**  
Since Amazon EKS Fargate runs only one Pod per node, the scenario of evicting Pods in case of fewer resources doesn't occur\. All Amazon EKS Fargate Pods run with guaranteed priority, so the requested CPU and memory must be equal to the limit for all of the containers\. For more information, see [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) in the Kubernetes documentation\.

When Pods are scheduled on Fargate, the vCPU and memory reservations within the Pod specification determine how much CPU and memory to provision for the Pod\.
+ The maximum request out of any Init containers is used to determine the Init request vCPU and memory requirements\.
+ Requests for all long\-running containers are added up to determine the long\-running request vCPU and memory requirements\.
+ The larger of the previous two values is chosen for the vCPU and memory request to use for your Pod\.
+ Fargate adds 256 MB to each Pod's memory reservation for the required Kubernetes components \(`kubelet`, `kube-proxy`, and `containerd`\)\.

Fargate rounds up to the following compute configuration that most closely matches the sum of vCPU and memory requests in order to ensure Pods always have the resources that they need to run\.

If you don't specify a vCPU and memory combination, then the smallest available combination is used \(\.25 vCPU and 0\.5 GB memory\)\.

The following table shows the vCPU and memory combinations that are available for Pods running on Fargate\. 


|  vCPU value  |  Memory value  | 
| --- | --- | 
|  \.25 vCPU  |  0\.5 GB, 1 GB, 2 GB  | 
|  \.5 vCPU  |  1 GB, 2 GB, 3 GB, 4 GB  | 
|  1 vCPU  |  2 GB, 3 GB, 4 GB, 5 GB, 6 GB, 7 GB, 8 GB  | 
|  2 vCPU  |  Between 4 GB and 16 GB in 1\-GB increments  | 
|  4 vCPU  |  Between 8 GB and 30 GB in 1\-GB increments  | 
|  8 vCPU  |  Between 16 GB and 60 GB in 4\-GB increments  | 
|  16 vCPU  |  Between 32 GB and 120 GB in 8\-GB increments  | 

The additional memory reserved for the Kubernetes components can cause a Fargate task with more vCPUs than requested to be provisioned\. For example, a request for 1 vCPU and 8 GB memory will have 256 MB added to its memory request, and will provision a Fargate task with 2 vCPUs and 9 GB memory, since no task with 1 vCPU and 9 GB memory is available\.

There is no correlation between the size of the Pod running on Fargate and the node size reported by Kubernetes with `kubectl get nodes`\. The reported node size is often larger than the Pod's capacity\. You can verify Pod capacity with the following command\. Replace `default` with your Pod's namespace and `pod-name` with the name of your Pod\.

```
kubectl describe pod --namespace default pod-name 
```

An example output is as follows\.

```
[...]
annotations:
    CapacityProvisioned: 0.25vCPU 0.5GB
[...]
```

The `CapacityProvisioned` annotation represents the enforced Pod capacity and it determines the cost of your Pod running on Fargate\. For pricing information for the compute configurations, see [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)\.

## Fargate storage<a name="fargate-storage"></a>

A Pod running on Fargate automatically mounts an Amazon EFS file system\. You can't use dynamic persistent volume provisioning with Fargate nodes, but you can use static provisioning\. For more information, see [Amazon EFS CSI Driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/README.md) on GitHub\.

When provisioned, each Pod running on Fargate receives a default 20 GiB of ephemeral storage\. This type of storage is deleted after a Pod stops\. New Pods launched onto Fargate have encryption of the ephemeral storage volume enabled by default\. The ephemeral Pod storage is encrypted with an AES\-256 encryption algorithm using AWS Fargate managed keys\.

**Note**  
The default usable storage for Amazon EKS Pods that run on Fargate is less than 20 GiB\. This is because some space is used by the `kubelet` and other Kubernetes modules that are loaded inside the Pod\.

You can increase the total amount of ephemeral storage up to a maximum of 175 GiB\. To configure the size with Kubernetes, specify the requests of `ephemeral-storage` resource to each container in a Pod\. When Kubernetes schedules Pods, it ensures that the sum of the resource requests for each Pod is less than the capacity of the Fargate task\. For more information, see [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) in the Kubernetes documentation\.

Amazon EKS Fargate provisions more ephemeral storage than requested for the purposes of system use\. For example, a request of 100 GiB will provision a Fargate task with 115 GiB ephemeral storage\. 