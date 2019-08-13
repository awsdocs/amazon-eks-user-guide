# Amazon EKS\-Optimized AMI with GPU Support<a name="gpu-ami"></a>

The Amazon EKS\-optimized AMI with GPU support is built on top of the standard Amazon EKS\-optimized AMI, and is configured to serve as an optional image for Amazon EKS worker nodes to support GPU workloads\.

In addition to the standard Amazon EKS\-optimized AMI configuration, the GPU AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-docker2` package
+ The `nvidia-container-runtime` \(as the default runtime\)

The AMI IDs for the latest Amazon EKS\-optimized AMI with GPU support are shown in the following table\. 

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.13\.7 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0ccac9d9b57864000 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0017d945a10387606 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-08335952e837d087b | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | N/A\* | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-005b754faac73f0cc | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-04cf69bbd6c0fae0b | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0730e699ed0118737 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07be5e97a529cd146 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0a2f4c3aeb596aa7e | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0fbbd205f797ecccd | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0f9571a3e65dc4e20 | 
| EU \(London\) \(eu\-west\-2\) | ami\-032348bd69c5dd665 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-053962359d6859fec | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0641def7f02a4cac5 | 

------
#### [ Kubernetes version 1\.12\.7 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-067d88fb64d3d7990 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-06e46a15650294dfa | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-084e8e620163aa50e | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | N/A\* | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-09ad3a49fb13389a0 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0cd09d7293f31df8a | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-006549812c03748cb | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-01be8fddd9b16320c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0a1bf783357dd8492 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0ae5976723472b6d4 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-042f9abf2f96a0097 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0b87e9246afd42760 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0d9405868a6e9ee11 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0122b7e2a6736e3c5 | 

------
#### [ Kubernetes version 1\.11\.9 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0b87186dda80931ee | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-07207754196c1a8fc | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-052da6a4e0ae156ad | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | N/A\* | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-04645af6384529c5d | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0a8f4e1f9bf09a81f | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-01db6bb089f6adfcf | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0e001196bd450aa0c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0c7132a332aa55aa6 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-05cb4f6e8be8b83f1 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-02f337476a5c33f1b | 
| EU \(London\) \(eu\-west\-2\) | ami\-0aa2208dbb9bb7cc5 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0f6ea479cb4e7a4d2 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-078c260b9a737fc35 | 

------

\* GPU instance types are not available in the Asia Pacific \(Hong Kong\) \(`ap-east-1`\) region, so Amazon EKS does not publish the Amazon EKS\-optimized AMI with GPU support in that region\.

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You can't use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your worker nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

After your GPU worker nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

```
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
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