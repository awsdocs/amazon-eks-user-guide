# Fargate Pod Configuration<a name="fargate-pod-configuration"></a>

This section describes some of the unique pod configuration details for running Kubernetes pods on AWS Fargate\.

## Pod CPU and Memory<a name="fargate-cpu-and-memory"></a>

Kubernetes allows you to define requests, a minimum amount of vCPU and memory resources that are allocated to each container in a pod\. Pods are scheduled by Kubernetes to ensure that at least the requested resources for each pod are available on the compute resource\. For more information, see [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) in the Kubernetes documentation\.

When pods are scheduled on Fargate, the vCPU and memory reservations within the pod specification determine how much CPU and memory to provision for the pod\.
+ The maximum request out of any Init containers is used to determine the Init request vCPU and memory requirements\.
+ Requests for all long\-running containers are added up to determine the long\-running request vCPU and memory requirements\.
+ The larger of the above two values is chosen for the vCPU and memory request to use for your pod\.
+ Fargate adds 256 MB to each pod's memory reservation for the required Kubernetes components \(`kubelet`, `kube-proxy`, and `containerd`\)\.

Fargate rounds up to the compute configuration shown below that most closely matches the sum of vCPU and memory requests in order to ensure pods always have the resources that they need to run\.

If you do not specify a vCPU and memory combination, then the smallest available combination is used \(\.25 vCPU and 0\.5 GB memory\)\.

The table below shows the vCPU and memory combinations that are available for pods running on Fargate\. 


|  vCPU value  |  Memory value  | 
| --- | --- | 
|  \.25 vCPU  |  0\.5 GB, 1 GB, 2 GB  | 
|  \.5 vCPU  |  1 GB, 2 GB, 3 GB, 4 GB  | 
|  1 vCPU  |  2 GB, 3 GB, 4 GB, 5 GB, 6 GB, 7 GB, 8 GB  | 
|  2 vCPU  |  Between 4 GB and 16 GB in 1\-GB increments  | 
|  4 vCPU  |  Between 8 GB and 30 GB in 1\-GB increments  | 

For pricing information on these compute configurations, see [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)\.

## Fargate Storage<a name="fargate-storage"></a>

When provisioned, each pod running on Fargate receives the following storage\. Pod storage is ephemeral\. After a pod stops, the storage is deleted\.
+ 10 GB of container image layer storage\.
+ An additional 4 GB for volume mounts\.