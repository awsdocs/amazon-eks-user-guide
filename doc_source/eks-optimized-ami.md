# Amazon EKS optimized Amazon Linux AMIs<a name="eks-optimized-ami"></a>

The Amazon EKS optimized Amazon Linux AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS nodes\. The AMI is configured to work with Amazon EKS and it includes the following components:
+ `kubelet`
+ AWS IAM Authenticator
+ Docker \(Amazon EKS version `1.23` and earlier\)
+ `containerd`

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux security center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
Before deploying an accelerated or Arm AMI, review the information in [Amazon EKS optimized accelerated Amazon Linux AMIs](#gpu-ami) and [Amazon EKS optimized Arm Amazon Linux AMIs](#arm-ami)\.
For Kubernetes version `1.23`, you can use an optional bootstrap flag to test migration from Docker to `containerd`\. For more information, see [Testing migration from Docker to `containerd`](#containerd-bootstrap)\.
Starting with Kubernetes version `1.25`, you will no longer be able to use Amazon EC2 `P2` instances with the Amazon EKS optimized accelerated Amazon Linux AMIs out of the box\. These AMIs for Kubernetes versions `1.25` or later will support `NVIDIA 525` series or later drivers, which are incompatible with the `P2` instances\. However, `NVIDIA 525` series or later drivers are compatible with the `P3`, `P4`, and `P5` instances, so you can use those instances with the AMIs for Kubernetes version `1.25` or later\. Before your Amazon EKS clusters are upgraded to version `1.25`, migrate any `P2` instances to `P3`, `P4`, and `P5` instances\. You should also proactively upgrade your applications to work with the `NVIDIA 525` series or later\.

## Testing migration from Docker to `containerd`<a name="containerd-bootstrap"></a>

Amazon EKS ended support for Docker starting with the Kubernetes version `1.24` launch\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.

For Kubernetes version `1.23`, you can use an optional bootstrap flag to enable the `containerd` runtime for Amazon EKS optimized Amazon Linux 2 AMIs\. This feature gives you a clear path to migrate to `containerd` when updating to version `1.24` or later\. Amazon EKS ended support for Docker starting with the Kubernetes version `1.24` launch\. The `containerd` runtime is widely adopted in the Kubernetes community and is a graduated project with the CNCF\. You can test it by adding a node group to a new or existing cluster\.

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

## Amazon EKS optimized accelerated Amazon Linux AMIs<a name="gpu-ami"></a>

The Amazon EKS optimized accelerated Amazon Linux AMI is built on top of the standard Amazon EKS optimized Amazon Linux AMI\. It's configured to serve as an optional image for Amazon EKS nodes to support GPU and [Inferentia](http://aws.amazon.com/machine-learning/inferentia/) based workloads\.

In addition to the standard Amazon EKS optimized AMI configuration, the accelerated AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-container-runtime` \(as the default runtime\)
+ AWS Neuron container runtime

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
+ You can run Arm node groups and x86 node groups in the same cluster\. If you do, consider deploying multi\-architecture container images to a container repository such as Amazon Elastic Container Registry and then adding node selectors to your manifests so that Kubernetes knows what hardware architecture a Pod can be deployed to\. For more information, see [Pushing a multi\-architecture image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-multi-architecture-image.html) in the *Amazon ECR User Guide* and the [Introducing multi\-architecture container images for Amazon ECR](http://aws.amazon.com/blogs/containers/introducing-multi-architecture-container-images-for-amazon-ecr/) blog post\.

## More information<a name="linux-more-information"></a>

For more information about using Amazon EKS optimized Amazon Linux AMIs, see the following sections:
+ To use Amazon Linux with managed node groups, see [Managed node groups](managed-node-groups.md)\.
+ To launch self\-managed Amazon Linux nodes, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For version information, see [Amazon EKS optimized Amazon Linux AMI versions](eks-linux-ami-versions.md)\.
+ To retrieve the latest IDs of the Amazon EKS optimized Amazon Linux AMIs, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
+ For open\-source scripts that are used to build the Amazon EKS optimized AMI, see [Amazon EKS optimized Amazon Linux AMI build script](eks-ami-build-scripts.md)\.