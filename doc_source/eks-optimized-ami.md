# Create nodes with optimized Amazon Linux AMIs<a name="eks-optimized-ami"></a>

The Amazon EKS optimized Amazon Linux AMI is built on top of Amazon Linux 2 \(AL2\) and Amazon Linux 2023 \(AL2023\)\. It's configured to serve as the base image for Amazon EKS nodes\. The AMI is configured to work with Amazon EKS and it includes the following components:
+ `kubelet`
+ AWS IAM Authenticator
+ Docker \(Amazon EKS version `1.23` and earlier\)
+ `containerd`

**Note**  
You can track security or privacy events for AL2 at the [Amazon Linux security center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
Before deploying an accelerated or Arm AMI, review the information in [Amazon EKS optimized accelerated Amazon Linux AMIs](#gpu-ami) and [Amazon EKS optimized Arm Amazon Linux AMIs](#arm-ami)\.
For Kubernetes version `1.23`, you can use an optional bootstrap flag to test migration from Docker to `containerd`\. For more information, see [Test Amazon Linux 2 migration from Docker to `containerd`](dockershim-deprecation.md#containerd-bootstrap)\.
Starting with Kubernetes version `1.25`, you will no longer be able to use Amazon EC2 `P2` instances with the Amazon EKS optimized accelerated Amazon Linux AMIs out of the box\. These AMIs for Kubernetes versions `1.25` or later will support `NVIDIA 525` series or later drivers, which are incompatible with the `P2` instances\. However, `NVIDIA 525` series or later drivers are compatible with the `P3`, `P4`, and `P5` instances, so you can use those instances with the AMIs for Kubernetes version `1.25` or later\. Before your Amazon EKS clusters are upgraded to version `1.25`, migrate any `P2` instances to `P3`, `P4`, and `P5` instances\. You should also proactively upgrade your applications to work with the `NVIDIA 525` series or later\. We plan to back port the newer `NVIDIA 525` series or later drivers to Kubernetes versions `1.23` and `1.24` in late January 2024\.
Any newly created managed node groups in clusters on version `1.30` or newer will automatically default to using AL2023 as the node operating system\. Previously, new node groups would default to AL2\. You can continue to use AL2 by choosing it as the AMI type when creating a new node group\.
Support for AL2 will end on June 30th, 2025\. For more information, see [Amazon Linux 2 FAQs](https://aws.amazon.com/amazon-linux-2/faqs/)\.

## Amazon EKS optimized accelerated Amazon Linux AMIs<a name="gpu-ami"></a>

**Note**  
Amazon EKS accelerated AMIs based on AL2023 will be available at a later date\. If you have accelerated workloads, you should continue to use the AL2 accelerated AMI or Bottlerocket\.

The Amazon EKS optimized accelerated Amazon Linux AMI is built on top of the standard Amazon EKS optimized Amazon Linux AMI\. It's configured to serve as an optional image for Amazon EKS nodes to support GPU, [Inferentia](https://aws.amazon.com/machine-learning/inferentia/), and [Trainium](https://aws.amazon.com/machine-learning/trainium/) based workloads\.

In addition to the standard Amazon EKS optimized AMI configuration, the accelerated AMI includes the following:
+ NVIDIA drivers
+ `nvidia-container-runtime`
+ AWS Neuron driver

For a list of the latest components included in the accelerated AMI, see the `amazon-eks-ami` [Releases](https://github.com/awslabs/amazon-eks-ami/releases) on GitHub\.

**Note**  
The Amazon EKS optimized accelerated AMI only supports GPU and Inferentia based instance types\. Make sure to specify these instance types in your node AWS CloudFormation template\. By using the Amazon EKS optimized accelerated AMI, you agree to [NVIDIA's Cloud End User License Agreement \(EULA\)](https://s3.amazonaws.com/EULA/NVidiaEULAforAWS.pdf)\.
The Amazon EKS optimized accelerated AMI was previously referred to as the *Amazon EKS optimized AMI with GPU support*\. 
Previous versions of the Amazon EKS optimized accelerated AMI installed the `nvidia-docker` repository\. The repository is no longer included in Amazon EKS AMI version `v20200529` and later\. 

**To enable AWS Neuron \(ML accelerator\) based workloads**  
For details on training and inference workloads using Neuron in Amazon EKS, see the following references:
+ [Containers \- Kubernetes \- Getting Started](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/containers/kubernetes-getting-started.html) in the *AWS Neuron Documentation*
+ [Training](https://github.com/aws-neuron/aws-neuron-eks-samples/blob/master/README.md#training) in AWS Neuron EKS Samples on GitHub
+ [Deploy ML inference workloads with AWSInferentia on Amazon EKS](inferentia-support.md)

**To enable GPU based workloads**

The following procedure describes how to run a workload on a GPU based instance with the Amazon EKS optimized accelerated AMI\.

1. After your GPU nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster\. Replace `vX.X.X` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/deployments/static/nvidia-device-plugin.yml
   ```

1. You can verify that your nodes have allocatable GPUs with the following command\.

   ```
   kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
   ```

**To deploy a Pod to test that your GPU nodes are configured properly**

1. Create a file named `nvidia-smi.yaml` with the following contents\. Replace `tag` with your desired tag for [https://hub.docker.com/r/nvidia/cuda/tags](https://hub.docker.com/r/nvidia/cuda/tags)\. This manifest launches an [https://developer.nvidia.com/cuda-zone](https://developer.nvidia.com/cuda-zone) container that runs `nvidia-smi` on a node\.

   ```
   apiVersion: v1
   kind: Pod
   metadata:
     name: nvidia-smi
   spec:
     restartPolicy: OnFailure
     containers:
     - name: nvidia-smi
       image: nvidia/cuda:tag
       args:
       - "nvidia-smi"
       resources:
         limits:
           nvidia.com/gpu: 1
   ```

1. Apply the manifest with the following command\.

   ```
   kubectl apply -f nvidia-smi.yaml
   ```

1. After the Pod has finished running, view its logs with the following command\.

   ```
   kubectl logs nvidia-smi
   ```

   An example output is as follows\.

   ```
   Mon Aug  6 20:23:31 20XX
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI XXX.XX                 Driver Version: XXX.XX                    |
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

## Amazon EKS optimized Arm Amazon Linux AMIs<a name="arm-ami"></a>

Arm instances deliver significant cost savings for scale\-out and Arm\-based applications such as web servers, containerized microservices, caching fleets, and distributed data stores\. When adding Arm nodes to your cluster, review the following considerations\.

**Considerations**
+ If your cluster was deployed before August 17, 2020, you must do a one\-time upgrade of critical cluster add\-on manifests\. This is so that Kubernetes can pull the correct image for each hardware architecture in use in your cluster\. For more information about updating cluster add\-ons, see [Update the Kubernetes version for your Amazon EKS cluster](update-cluster.md#update-existing-cluster)\. If you deployed your cluster on or after August 17, 2020, then your CoreDNS, `kube-proxy`, and Amazon VPC CNI plugin for Kubernetes add\-ons are already multi\-architecture capable\. 
+ Applications deployed to Arm nodes must be compiled for Arm\.
+ If you have DaemonSets that are deployed in an existing cluster, or you want to deploy them to a new cluster that you also want to deploy Arm nodes in, then verify that your DaemonSet can run on all hardware architectures in your cluster\. 
+ You can run Arm node groups and x86 node groups in the same cluster\. If you do, consider deploying multi\-architecture container images to a container repository such as Amazon Elastic Container Registry and then adding node selectors to your manifests so that Kubernetes knows what hardware architecture a Pod can be deployed to\. For more information, see [Pushing a multi\-architecture image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-multi-architecture-image.html) in the *Amazon ECR User Guide* and the [Introducing multi\-architecture container images for Amazon ECR](https://aws.amazon.com/blogs/containers/introducing-multi-architecture-container-images-for-amazon-ecr/) blog post\.

## More information<a name="linux-more-information"></a>

For more information about using Amazon EKS optimized Amazon Linux AMIs, see the following sections:
+ To use Amazon Linux with managed node groups, see [Simplify node lifecycle with managed node groups](managed-node-groups.md)\.
+ To launch self\-managed Amazon Linux nodes, see [Retrieve recommended Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For version information, see [Retrieve Amazon Linux AMI version information](eks-linux-ami-versions.md)\.
+ To retrieve the latest IDs of the Amazon EKS optimized Amazon Linux AMIs, see [Retrieve recommended Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For open\-source scripts that are used to build the Amazon EKS optimized AMI, see [Build a custom Amazon Linux AMI with a script](eks-ami-build-scripts.md)\.