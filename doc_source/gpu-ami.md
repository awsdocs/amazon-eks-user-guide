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
| US East \(Ohio\) \(us\-east\-2\) | ami\-01f82bb66c17faf20 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-02af865c0f3b337f2 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-08e5329e1dbf22c6a | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-094beaac92afd72eb | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0f409159b757b0292 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-066623eb3f5a82878 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0d660fb17b06078d9 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0d11124f8f06f8a4f | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-085b174e2e2b41f33 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-093009474b04965b3 | 
| EU \(London\) \(eu\-west\-2\) | ami\-08a5d542db43e17ab | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-05cbcb1bc3dbe7a3d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0f66f596ae68c0353 | 

------
#### [ Kubernetes version 1\.12\.7 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-09279e76127f808b2 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0ae641b4b7ed88d72 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-08142df4834399a6b | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-000721b659ba73311 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0b11aeca80a60fbb5 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-08ace4be4e6e52c62 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-054db05dce73fc060 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0045324a51592dbeb | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0bd21d3112638aa26 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0ae2f64856228879f | 
| EU \(London\) \(eu\-west\-2\) | ami\-06cc142c64830e356 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-02461867f991941f2 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-04870dc2b156b47fb | 

------
#### [ Kubernetes version 1\.11\.9 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-05ad04ed51d006bc9 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-06fb2eb20652dafea | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0d6743e4d45d710f4 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0d888cb5eaaba12d4 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-05ab4ae12fa19bfb5 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0bfd390f3bd942923 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0726645aa38e7fe38 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0d2ed580683a2ef3c | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-096075e3334201678 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0fb8e730ee4b17f98 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0c420fc6a2ab8a140 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-009bd30954d1cdf61 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-07fa78fe686748c79 | 

------
#### [ Kubernetes version 1\.10\.13 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0a0d326e98757aa1b | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0e261247a4b523354 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-067089d967e068569 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-014cc26f091950263 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-02fe5649049614901 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-011a0f131a7148431 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0654c7681c0b39e0c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0d120c3ce6fba36d8 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0be7b531dd58c5df1 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0b01f474bfc6c1260 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0513d2fbf2aa77b8c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0032d4bbdc242c41c | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0b9102084fa8d4e01 | 

------

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You can't use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your worker nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

After your GPU worker nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a daemon set on your cluster with the following command\.

**Note**  
If your cluster is running a different Kubernetes version than 1\.13, be sure to substitute your cluster's version in the following URL\.

```
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.13/nvidia-device-plugin.yml
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