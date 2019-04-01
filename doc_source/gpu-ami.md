# Amazon EKS\-Optimized AMI with GPU Support<a name="gpu-ami"></a>

The Amazon EKS\-optimized AMI with GPU support is built on top of the standard Amazon EKS\-optimized AMI, and is configured to serve as an optional image for Amazon EKS worker nodes to support GPU workloads\.

In addition to the standard Amazon EKS\-optimized AMI configuration, the GPU AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-docker2` package
+ The `nvidia-container-runtime` \(as the default runtime\)

The AMI IDs for the latest Amazon EKS\-optimized AMI with GPU support are shown in the following table\. 

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.


**Kubernetes version 1\.12\.7**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0bebf2322fd52a42e | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0cb7959f92429410a | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0118b61dc2312dee2 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0c57db5b204001099 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-09354b076296f5946 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0fbc930681258db86 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0d832fced2cfe0f7b | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0f8fa088b406ebba2 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-08e41cc84f4b3f27f | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0c43b885e33fdc29e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0d3ecaf4f3318c714 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0655b4dbbe2d46703 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-07079cd9ff1b312da | 


**Kubernetes version 1\.11\.9**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-08377056d89909b2a | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-06ec2ea207616c078 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0e6993a35aae3407b | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0bf09c13f4204ce9d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0a1714bb5be631b59 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0b4d0f56587640d5a | 
| EU \(London\) \(eu\-west\-2\) | ami\-00e98f9e6fd2319e5 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0039e2556e6290828 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-07fc636e8f6d3e18b | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-002057772097fcef9 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-04fe7f4c75aac7196 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-08d5da0b12751a31f | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-04024dd8e0b9e36ff | 


**Kubernetes version 1\.10\.13**  

| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0901518d7557125c8 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-00f74c3728d4ca27d | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0a788defb66cdfffb | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0a8536a894bd4ea06 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-05baf7a6c293fe2ed | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0f6f3929a9d7a418e | 
| EU \(London\) \(eu\-west\-2\) | ami\-0a12396b818bc2383 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-086d5edcaacd0ccfd | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-073f06a1edd22ae2e | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0baff950f5217e54e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-033bd2c2a3431923e | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-09defa93988984fa1 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-00d9364d705e902c9 | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows them to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

After your GPU worker nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a daemon set on your cluster with the following command\.

```
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.12/nvidia-device-plugin.yml
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