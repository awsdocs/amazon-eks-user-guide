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
| US West \(Oregon\) \(us\-west\-2\) | ami\-0805ff53a28e7b904 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-000412c12949aa8dd | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-018bc34828bcbf65e | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0b82a79b011122da0 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-d6159ca8 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0fab91784768ff07a | 
| EU \(London\) \(eu\-west\-2\) | ami\-02ab85779351ea872 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-08b97dd0252bd9e51 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0ed8c50e848425cb3 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-042e93c5dc384f6b8 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0f8881c15c47755a9 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0c1b23fe04eafb5a0 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0fe2e260f573c02a8 | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-003a551d4d2e5c75d | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0c67dfb2298cf554a | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0fb4bb0f84f4a0049 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0290406a183d6587d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-d3169fad | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-086252e9df9c3a21e | 
| EU \(London\) \(eu\-west\-2\) | ami\-06389f3a72966a326 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0dce0fff5c4af413e | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0bb5892624403ca87 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-02ef4162c5ee1e443 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-09865c928b7d38fcd | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-09496affecfe51b86 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0dae5c0d203e32e9f | 

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