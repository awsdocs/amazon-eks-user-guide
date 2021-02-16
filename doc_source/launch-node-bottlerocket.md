# Launching self\-managed Bottlerocket nodes<a name="launch-node-bottlerocket"></a>

This topic helps you to launch an Auto Scaling group of [Bottlerocket](http://aws.amazon.com/bottlerocket/) nodes that register with your Amazon EKS cluster\. Bottlerocket is a Linux\-based open\-source operating system that is purpose\-built by AWS for running containers on virtual machines or bare metal hosts\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. For more information about Bottlerocket, see the [documentation](https://github.com/bottlerocket-os/bottlerocket/blob/develop/README.md) on GitHub\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

**Important**  
Considerations  
You can deploy to Amazon EC2 instances with x86 or Arm processors, but not to instances that have GPUs or Inferentia chips\.
You can't deploy to the following regions: China \(Beijing\) \(`cn-north-1`\), China \(Ningxia\) \(`cn-northwest-1`\), AWS GovCloud \(US\-East\) \(`us-gov-east-1`\), or AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)\.
There is no AWS CloudFormation template to deploy nodes with\.

**Important**  
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [Launching self\-managed Amazon Linux nodes](launch-workers.md) and [Launching self\-managed Windows nodes](launch-windows-workers.md)\.

**To launch Bottlerocket nodes using `eksctl`**

This procedure requires `eksctl` version `0.38.0` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. This procedure assumes that you have an existing cluster named `my-cluster` in the `us-west-2` Region\. For a different existing cluster, change the values\. If you don't have an existing cluster then you must first [create a cluster](create-cluster.md)\.

   Create a file named *windows\-cluster\.yaml* with the following contents\. Replace the *`example values`* with your own values\. If you change *`1.19`*, then it can only be changed to `1.15` or later\. If you want to deploy on Arm instances, then replace `m5.large` with an Arm instance type\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\. If you want to deploy using a custom AMI, then see [Building Bottlerocket](https://github.com/bottlerocket-os/bottlerocket/blob/develop/BUILDING.md) on GitHub and [Custom AMI support](https://eksctl.io/usage/custom-ami-support/) in the `eksctl` documentation\. If you want to deploy a managed node group then you must deploy a custom AMI using a launch template\. For more information, see [Launch template support](launch-templates.md)\.

   For more information about using a [config file](https://eksctl.io/usage/managing-nodegroups/#creating-a-nodegroup-from-a-config-file) with `eksctl`, the [config file schema](https://eksctl.io/usage/schema/), and [config file samples](https://github.com/weaveworks/eksctl/tree/master/examples), see the `eksctl` documentation\.

   ```
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-cluster
     region: us-west-2
     version: '1.19'
   
   nodeGroups:
     - name: ng-bottlerocket
       instanceType: m5.large
       desiredCapacity: 3
       amiFamily: Bottlerocket
       iam:
          attachPolicyARNs:
             - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
             - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
             - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
             - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
       ssh:
           allow: true
           publicKeyName: YOUR_EC2_KEYPAIR_NAME
   ```

1. Deploy your nodes with the following command\.

   ```
   eksctl create nodegroup --config-file=windows-cluster.yaml
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   Output:

   You'll see several lines of output as the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Create a Kubernetes [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) on a Bottlerocket node using the [Amazon EBS CSI Plugin](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)\. The default Amazon EBS driver relies on file system tools that are not included with Bottlerocket\. For more information about creating a storage class using the driver, see [Amazon EBS CSI driver](ebs-csi.md)\.

1. \(Optional\) By default `kube-proxy` will set the `nf_conntrack_max` kernel parameter to a default value that may differ from what Bottlerocket originally sets at boot\. If you prefer to keep Bottlerocket's [default setting](https://github.com/bottlerocket-os/bottlerocket/blob/develop/packages/release/release-sysctl.conf), then edit the kube\-proxy configuration with the following command\.

   ```
   kubectl edit -n kube-system daemonset kube-proxy
   ```

   Add \-\-conntrack\-max\-per\-core and \-\-conntrack\-min to the kube\-proxy arguments as shown in the following example\. A setting of `0` implies no change\.

   ```
   containers:
         - command:
           - kube-proxy
           - --v=2
           - --config=/var/lib/kube-proxy-config/config
           - --conntrack-max-per-core=0
           - --conntrack-min=0
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your Bottlerocket nodes\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. \(Optional\) If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.