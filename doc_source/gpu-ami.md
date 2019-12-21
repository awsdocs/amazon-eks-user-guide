# Amazon EKS\-Optimized AMI with GPU Support<a name="gpu-ami"></a>

The Amazon EKS\-optimized AMI with GPU support is built on top of the standard Amazon EKS\-optimized AMI, and is configured to serve as an optional image for Amazon EKS worker nodes to support GPU workloads\.

In addition to the standard Amazon EKS\-optimized AMI configuration, the GPU AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-docker2` package
+ The `nvidia-container-runtime` \(as the default runtime\)

The AMI IDs for the latest Amazon EKS\-optimized AMI with GPU support are shown in the following table\. You can also retrieve the IDs with an Amazon EC2 Systems Manager parameter using different tools\. For more information, see [Retrieving Amazon EKS\-Optimized AMI IDs](retrieve-ami-id.md)\.  

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports GPU instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.14\.7 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://us-east-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://us-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://ap-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://ap-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://ap-northeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://ap-northeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://ap-southeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://ap-southeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://ca-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| EU \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://eu-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| EU \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://eu-west-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| EU \(London\) \(eu\-west\-2\) | [View AMI ID](https://eu-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| EU \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://eu-west-3.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| EU \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://eu-north-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://me-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://sa-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 

------
#### [ Kubernetes version 1\.13\.11 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://us-east-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://us-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://ap-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://ap-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://ap-northeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://ap-northeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://ap-southeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://ap-southeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://ca-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| EU \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://eu-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| EU \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://eu-west-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| EU \(London\) \(eu\-west\-2\) | [View AMI ID](https://eu-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| EU \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://eu-west-3.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| EU \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://eu-north-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://me-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://sa-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.13%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 

------
#### [ Kubernetes version 1\.12\.10 ]


| Region | Amazon EKS\-optimized AMI with GPU support | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://us-east-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://us-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://ap-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://ap-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://ap-northeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://ap-northeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://ap-southeast-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://ap-southeast-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://ca-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| EU \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://eu-central-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| EU \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://eu-west-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| EU \(London\) \(eu\-west\-2\) | [View AMI ID](https://eu-west-2.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| EU \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://eu-west-3.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| EU \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://eu-north-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://me-south-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://sa-east-1.console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.12%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 

------

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You can't use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your worker nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)\.

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