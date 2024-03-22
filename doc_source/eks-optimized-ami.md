# Amazon EKS optimized Amazon Linux AMIs<a name="eks-optimized-ami"></a>

The Amazon EKS optimized Amazon Linux AMI is built on top of Amazon Linux 2 \(AL2\) and Amazon Linux 2023 \(AL2023\)\. It's configured to serve as the base image for Amazon EKS nodes\. The AMI is configured to work with Amazon EKS and it includes the following components:
+ `kubelet`
+ AWS IAM Authenticator
+ Docker \(Amazon EKS version `1.23` and earlier\)
+ `containerd`

**Note**  
You can track security or privacy events for AL2 at the [Amazon Linux security center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
Before deploying an accelerated or Arm AMI, review the information in [Amazon EKS optimized accelerated Amazon Linux AMIs](#gpu-ami) and [Amazon EKS optimized Arm Amazon Linux AMIs](#arm-ami)\.
For Kubernetes version `1.23`, you can use an optional bootstrap flag to test migration from Docker to `containerd`\. For more information, see [Test migration from Docker to `containerd`](#containerd-bootstrap)\.
Starting with Kubernetes version `1.25`, you will no longer be able to use Amazon EC2 `P2` instances with the Amazon EKS optimized accelerated Amazon Linux AMIs out of the box\. These AMIs for Kubernetes versions `1.25` or later will support `NVIDIA 525` series or later drivers, which are incompatible with the `P2` instances\. However, `NVIDIA 525` series or later drivers are compatible with the `P3`, `P4`, and `P5` instances, so you can use those instances with the AMIs for Kubernetes version `1.25` or later\. Before your Amazon EKS clusters are upgraded to version `1.25`, migrate any `P2` instances to `P3`, `P4`, and `P5` instances\. You should also proactively upgrade your applications to work with the `NVIDIA 525` series or later\. We plan to back port the newer `NVIDIA 525` series or later drivers to Kubernetes versions `1.23` and `1.24` in late January 2024\.
Starting with Amazon EKS version `1.30` or newer, any newly created managed node groups will automatically default to using AL2023 as the node operating system\. Previously, new node groups would default to AL2\. You can continue to use AL2 by choosing it as the AMI type when creating a new node group\.
Support for AL2 will end on June 30th, 2025\. For more information, see [Amazon Linux 2 FAQs](https://aws.amazon.com/amazon-linux-2/faqs/)\.

## Upgrade from AL2 to AL2023<a name="al2023"></a>

The Amazon EKS optimized AMI is available in two families based on AL2 and AL2023\. AL2023 is a new Linux\-based operating system designed to provide a secure, stable, and high\-performance environment for your cloud applications\. It's the next generation of Amazon Linux from Amazon Web Services and is available across all supported Amazon EKS versions, including versions `1.23` and `1.24` in extended support\. Amazon EKS accelerated AMIs based on AL2023 will be available at a later date\. If you have accelerated workloads, you should continue to use the AL2 accelerated AMI or Bottlerocket\.

AL2023 offers several improvements over AL2\. For a full comparison, see [Comparing AL2 and Amazon Linux 2023](https://docs.aws.amazon.com/linux/al2023/ug/compare-with-al2.html) in the *Amazon Linux 2023 User Guide*\. Several packages have been added, upgraded, and removed from AL2\. It's highly recommended to test your applications with AL2023 before upgrading\. For a list of all package changes in AL2023, see [Package changes in Amazon Linux 2023](https://docs.aws.amazon.com/linux/al2023/release-notes/compare-packages.html) in the *Amazon Linux 2023 Release Notes*\.

In addition to these changes, you should be aware of the following:
+ AL2023 introduces a new node initialization process `nodeadm` that uses a YAML configuration schema\. If you're using self\-managed node groups or an AMI with a launch template, you'll now need to provide additional cluster metadata explicitly when creating a new node group\. An [example](https://awslabs.github.io/amazon-eks-ami/nodeadm/) of the minimum required parameters is as follows, where `apiServerEndpoint`, `certificateAuthority`, and service `cidr` are now required:

  ```
  ---
  apiVersion: node.eks.aws/v1alpha1
  kind: NodeConfig
  spec:
    cluster:
      name: my-cluster
      apiServerEndpoint: https://example.com
      certificateAuthority: Y2VydGlmaWNhdGVBdXRob3JpdHk=
      cidr: 10.100.0.0/16
  ```

  In AL2, the metadata from these parameters was discovered from the Amazon EKS `DescribeCluster` API call\. With AL2023, this behavior has changed since the additional API call risks throttling during large node scale ups\. This change doesn't affect you if you're using managed node groups without a launch template or if you're using Karpenter\. For more information on `certificateAuthority` and service `cidr`, see `[DescribeCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeCluster.html)` in the *Amazon EKS API Reference*\.
+ Docker isn't supported in AL2023 for all supported Amazon EKS versions\. Support for Docker has ended and been removed with Amazon EKS version `1.24` or greater in AL2\. For more information on deprecation, see [ Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.
+ Amazon VPC CNI version `1.16.2` or greater is required for AL2023\.
+ AL2023 requires `IMDSv2` by default\. `IMDSv2` has several benefits that help improve security posture\. It uses a session\-oriented authentication method that requires the creation of a secret token in a simple HTTP PUT request to start the session\. A session's token can be valid for anywhere between 1 second and 6 hours\. For more information on how to transition from `IMDSv1` to `IMDSv2`, see [Transition to using Instance Metadata Service Version 2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-transition-to-version-2.html) and [Get the full benefits of IMDSv2 and disable IMDSv1 across your AWS infrastructure](https://aws.amazon.com/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/)\. If you would like to use `IMDSv1`, you can still do so by manually overriding the settings using instance metadata option launch properties\.
**Note**  
For `IMDSv2`, the default hop count for managed node groups is set to 1\. This means that containers won't have access to the node's credentials using IMDS\. If you require container access to the node's credentials, you can still do so by manually overriding the `HttpPutResponseHopLimit` in a [custom Amazon EC2 launch template](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-metadataoptions.html), increasing it to 2\. Alternatively, you can use [ Amazon EKS Pod Identity](pod-identities.md) to provide credentials instead of `IMDSv2`\.
+ AL2023 features the next generation of unified control group hierarchy \(`cgroupv2`\)\. `cgroupv2` is used to implement a container runtime, and by `systemd`\. While AL2023 still includes code that can make the system run using `cgroupv1`, this isn't a recommended or supported configuration\. This configuration will be completely removed in a future major release of Amazon Linux\.

For previously existing managed node groups, you can either perform an in\-place upgrade or a blue/green upgrade depending on how you're using a launch template:
+ If you're using a custom AMI with a managed node group, you can perform an in\-place upgrade by swapping the AMI ID in the launch template\. You should ensure that your applications and any user data transfer over to AL2023 first before performing this upgrade strategy\.
+ If you're using managed node groups with either the standard launch template or with a custom launch template that doesn't specify the AMI ID, you're required to upgrade using a blue/green strategy\. A blue/green upgrade is typically more complex and involves creating an entirely new node group where you would specify AL2023 as the AMI type\. The new node group will need to then be carefully configured to ensure that all custom data from the AL2 node group is compatible with the new OS\. Once the new node group has been tested and validated with your applications, Pods can be migrated from the old node group to the new node group\. Once the migration is completed, you can delete the old node group\.

If you're using Karpenter and want to use AL2023, you'll need to modify the `EC2NodeClass` `amiFamily` field with AL2023\. By default, Drift is enabled in Karpenter\. This means that once the `amiFamily` field has been changed, Karpenter will automatically update your worker nodes to the latest AMI when available\.

## Amazon EKS optimized accelerated Amazon Linux AMIs<a name="gpu-ami"></a>

**Note**  
Amazon EKS accelerated AMIs based on AL2023 will be available at a later date\. If you have accelerated workloads, you should continue to use the AL2 accelerated AMI or Bottlerocket\.

The Amazon EKS optimized accelerated Amazon Linux AMI is built on top of the standard Amazon EKS optimized Amazon Linux AMI\. It's configured to serve as an optional image for Amazon EKS nodes to support GPU, [Inferentia](https://aws.amazon.com/machine-learning/inferentia/), and [Trainium](https://aws.amazon.com/machine-learning/trainium/) based workloads\.

In addition to the standard Amazon EKS optimized AMI configuration, the accelerated AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-container-runtime` \(as the default runtime\)
+ AWS Neuron container runtime

For a list of the latest components included in the accelerated AMI, see the `amazon-eks-ami` [Releases](https://github.com/awslabs/amazon-eks-ami/releases) on GitHub\.

**Note**  
The Amazon EKS optimized accelerated AMI only supports GPU and Inferentia based instance types\. Make sure to specify these instance types in your node AWS CloudFormation template\. By using the Amazon EKS optimized accelerated AMI, you agree to [NVIDIA's user license agreement \(EULA\)](https://www.nvidia.com/en-us/drivers/nvidia-license/)\. 
The Amazon EKS optimized accelerated AMI was previously referred to as the *Amazon EKS optimized AMI with GPU support*\. 
Previous versions of the Amazon EKS optimized accelerated AMI installed the `nvidia-docker` repository\. The repository is no longer included in Amazon EKS AMI version `v20200529` and later\. 

**To enable GPU based workloads**

The following procedure describes how to run a workload on a GPU based instance with the Amazon EKS optimized accelerated AMI\. For other options, see the following references:
+ For more information about using Inferentia based workloads, see [Machine learning inference using AWS Inferentia](inferentia-support.md)\.
+ For more information about using Neuron, see [Containers \- Kubernetes \- Getting Started](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/containers/kubernetes-getting-started.html) in the *AWS Neuron Documentation*\.

1. After your GPU nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster\. Replace `vX.X.X` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/nvidia-device-plugin.yml
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

## Test migration from Docker to `containerd`<a name="containerd-bootstrap"></a>

Amazon EKS ended support for Docker starting with the Kubernetes version `1.24` launch\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.

For Kubernetes version `1.23`, you can use an optional bootstrap flag to enable the `containerd` runtime for Amazon EKS optimized AL2 AMIs\. This feature gives you a clear path to migrate to `containerd` when updating to version `1.24` or later\. Amazon EKS ended support for Docker starting with the Kubernetes version `1.24` launch\. The `containerd` runtime is widely adopted in the Kubernetes community and is a graduated project with the CNCF\. You can test it by adding a node group to a new or existing cluster\.

You can enable the boostrap flag by creating one of the following types of node groups\.

**Self\-managed**  
Create the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Specify an Amazon EKS optimized AMI and the following text for the `BootstrapArguments` parameter\.  

```
--container-runtime containerd
```

**Managed**  
If you use `eksctl`, create a file named `my-nodegroup.yaml` with the following contents\. Replace every `example value` with your own values\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. To retrieve an optimized AMI ID for `ami-1234567890abcdef0`, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.  

```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: my-cluster
  region: region-code
  version: 1.23
managedNodeGroups:
  - name: my-nodegroup
    ami: ami-1234567890abcdef0
    overrideBootstrapCommand: |
      #!/bin/bash
      /etc/eks/bootstrap.sh my-cluster --container-runtime containerd
```
If you launch many nodes simultaneously, you may also want to specify values for the `--apiserver-endpoint`, `--b64-cluster-ca`, and `--dns-cluster-ip` bootstrap arguments to avoid errors\. For more information, see [Specifying an AMI](launch-templates.md#launch-template-custom-ami)\.
Run the following command to create the node group\.  

```
eksctl create nodegroup -f my-nodegroup.yaml
```
If you prefer to use a different tool to create your managed node group, you must deploy the node group using a launch template\. In your launch template, specify an [Amazon EKS optimized AMI ID](retrieve-ami-id.md), then [deploy the node group using a launch template](launch-templates.md) and provide the following user data\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.  

```
/etc/eks/bootstrap.sh my-cluster --container-runtime containerd
```

## More information<a name="linux-more-information"></a>

For more information about using Amazon EKS optimized Amazon Linux AMIs, see the following sections:
+ To use Amazon Linux with managed node groups, see [Managed node groups](managed-node-groups.md)\.
+ To launch self\-managed Amazon Linux nodes, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For version information, see [Amazon EKS optimized Amazon Linux AMI versions](eks-linux-ami-versions.md)\.
+ To retrieve the latest IDs of the Amazon EKS optimized Amazon Linux AMIs, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For open\-source scripts that are used to build the Amazon EKS optimized AMI, see [Amazon EKS optimized Amazon Linux AMI build script](eks-ami-build-scripts.md)\.