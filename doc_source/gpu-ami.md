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
#### [ Kubernetes version 1\.13\.8 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0af8403c143fd4a07 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0484012ada3522476 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0d24da600cc96ae6b | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-080eb165234752969 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-010dbb7183ab64b39 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-069303796840f8155 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-04f71dc710ff5baf4 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0213fc532b1c2e05f | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-01fc0a4c67f82532b | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-07b7cbb235789cc31 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-00bfeece5b673b69f | 
| EU \(London\) \(eu\-west\-2\) | ami\-0babebc79dbf6016c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-03136b5b83c5b61ba | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-057821acea15c1a98 | 

------
#### [ Kubernetes version 1\.12\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0b42bfc7af8bb3abc | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0eb0119f55d589a03 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0c9156d7fcd3c2948 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0a5e7de0e5d22a988 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0c1bc87ff613a979b | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0e2f87975f5aa9908 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-08101c357b41e9f9a | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0420c66a82472f4b2 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-04a085528a6af6499 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-09c45f4e40a56254b | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-04668c090ff8c1f50 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0b925567bd252e74c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0f975ac243bcd0da0 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-093da2874a5426ce3 | 

------
#### [ Kubernetes version 1\.11\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0f9e62727a55f68d3 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0c3d92683a7946ac3 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-058b22acd515ec20b | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0baf9ac8446e87fb5 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0c709282458d1114c | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-023f507ec007de487 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0ccbbe6530310b01d | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0341435cf966cb837 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0987b07bd338f97db | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-060f13bd7397f782d | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0d84963dfda5af073 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0189e53a00d37a0b6 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0baea83f5f5d2abfe | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0d5b7823e58094232 | 

------

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