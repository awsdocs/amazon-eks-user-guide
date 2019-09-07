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
#### [ Kubernetes version 1\.14\.6 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-02ed30745089113eb | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0d5628765ec5d0c5a | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-02ce33febfee0b888 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0c23d82cc7e2b0f53 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0981d2926d2260939 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0515f3ce5064036dc | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0cba72a7e9b560b06 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0503f4de442edeef2 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-09a0ec306d79ed058 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0698f87b093bbcdda | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-04cef31a7c7bf1169 | 
| EU \(London\) \(eu\-west\-2\) | ami\-04f1bbad31585405d | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0ebcd2fd2eb614793 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-04e7d365014dee49c | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-07ca0892ebe2c442e | 

------
#### [ Kubernetes version 1\.13\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-080eaa48408e4cce8 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0b2f191b2ddb13526 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0842679a8337cad05 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0a63a7853310f3111 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0e80f1d31941f6010 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0a443fa8decd2df67 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-019966f3e72baba33 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07f34d09a8d7fe5a4 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-03563e56d0af30647 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0e262bd06b1cbc1d6 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-05cded29b25d50f91 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0163f3b1681613866 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0bc7f58961988d81e | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0b219ca1c6aa2f7fb | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-0dd405f6294e0414d | 

------
#### [ Kubernetes version 1\.12\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-043355c6f9c7b980c | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0585963de7ab8b964 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-04f40a6dd1cd12b3c | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0f6b904acd6b3add8 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-008ab31273984feb4 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0364b5f7211f80363 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-08704c644f2f284bb | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-044d6be5df6aa258e | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-002dcfad1b6044f1d | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0a697401e7cfa02bd | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-049574de1981b69dc | 
| EU \(London\) \(eu\-west\-2\) | ami\-009594e276ffd81b0 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-06cb6ffbba9a766eb | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0051b31561a86c5fb | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-0d4ec4bd32daaae1c | 

------
#### [ Kubernetes version 1\.11\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-06352290702ae9aa4 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-06dbf81822c5d802d | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-01ccb69d4e42d3098 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0bf87f2c6a31cf83c | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-067c840a5dce7fe27 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0dc2541c99f0623e1 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-013299f00c1c965d4 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07e5bc491d2ec43e1 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-04b5a2ebc54d30b11 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0147c8fcfea398609 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-01f0f9e4092c0f784 | 
| EU \(London\) \(eu\-west\-2\) | ami\-024af210119b7a9f8 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-00d28dcaaa9b1010a | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0a2aefc5b3775e1da | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-03ba561b225de5fc7 | 

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