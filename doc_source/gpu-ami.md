# Amazon EKS\-Optimized AMI with GPU Support<a name="gpu-ami"></a>

The Amazon EKS\-optimized AMI with GPU support is built on top of the standard Amazon EKS\-optimized AMI, and is configured to serve as an optional image for Amazon EKS worker nodes to support GPU workloads\.

In addition to the standard Amazon EKS\-optimized AMI configuration, the GPU AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-docker2` package
+ The `nvidia-container-runtime` \(as the default runtime\)

The AMI IDs for the latest Amazon EKS\-optimized AMI with GPU support are shown in the following table\. 

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. Because this AMI includes third\-party software that requires an end user license agreement \(EULA\), you must subscribe to the AMI in the AWS Marketplace and accept the EULA before you can use the AMI in your worker node groups\. To subscribe to the AMI, visit [the AWS Marketplace](https://aws.amazon.com/marketplace/pp/B07GRHFXGM)\.


**Kubernetes version 1\.11**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-014f4e495a19d3e4f | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-08a0bb74d1c9a5e2f | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-04a758678ae5ebad5 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-050db3f5f9dbd4439 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-69b03e17 | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-08754f7ac73185331 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-03c499c67bc65c089 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-081210a2fd7f3c487 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-047637529a86c7237 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-24b43a5a | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-12-10/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows them to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

After your GPU worker nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a daemon set on your cluster with the following command\.

```
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.11/nvidia-device-plugin.yml
```

You can verify that your nodes have allocatable GPUs with the following command:

```
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```

## Example GPU Manifest<a name="example-gpu-manifest"></a>

This section provides an example pod manifest for you to test that your GPU workers are configured properly\.

**Example Get `nvidia-smi` output**  

**Example**  
This example pod manifest launches a Cuda container that runs `nvidia-smi` on a worker node\. Create a file called `nvidia-smi.yaml`, copy and paste the following manifest into it, and save the file\.  

```
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-smi
spec:
  restartPolicy: OnFailure
  containers:
  - name: nvidia-smi
    image: nvidia/cuda:9.2-devel
    args:
    - "nvidia-smi"
    resources:
      limits:
        nvidia.com/gpu: 1
```
Apply the manifest with the following command:  

```
kubectl apply -f nvidia-smi.yaml
```
After the pod has finished running, view its logs with the following command:  

```
kubectl logs nvidia-smi
```
Output:  

```
Mon Aug  6 20:23:31 2018
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 396.26                 Driver Version: 396.26                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla V100-SXM2...  On   | 00000000:00:1C.0 Off |                    0 |
| N/A   46C    P0    47W / 300W |      0MiB / 16160MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```