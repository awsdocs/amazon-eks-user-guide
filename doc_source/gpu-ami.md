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
| US West \(Oregon\) \(us\-west\-2\) | ami\-06045aa686f46dd58 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0558da965e2fc68b0 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0c3afad2ea917168e | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0939712219b80b525 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-18bf3666 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-014969e8d07b2fc9f | 
| EU \(London\) \(eu\-west\-2\) | ami\-0bb14a7e038ad534c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0a3db0dbd972b38f2 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0880d3b662781d6d6 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0c3db49d90afa0f1e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-00b37b9a91efc5fff | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0c903ead334faa6a3 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-02d7e0f064bd7d8e0 | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-02e0b615d7749e016 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-00cce60e4c241de4c | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0bbfeb020c5ec10ee | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0c1746c6d5d61b4d3 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-63aa231d | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-08d23ed2de9320c90 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0f136e808b9365a1c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0b6c4fac3cdcc191d | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-061f5b653b1a98557 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0a8159b97b9a7e078 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-03ba4c3cea82ce746 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-02aa3e8ad27163456 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0679fa5d74309eb79 | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
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