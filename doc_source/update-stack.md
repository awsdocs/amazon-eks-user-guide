# Updating an existing self\-managed node group<a name="update-stack"></a>

This topic describes how you can update an existing AWS CloudFormation self\-managed node stack with a new AMI\. You can use this procedure to update your nodes to a new version of Kubernetes following a cluster update\. Otherwise, you can update to the latest Amazon EKS optimized AMI for an existing Kubernetes version\.

**Important**  
This topic covers node updates for self\-managed nodes\. For information about using [Managed node groups](managed-node-groups.md), see [Updating a managed node group](update-managed-node-group.md)\.

The latest default Amazon EKS node AWS CloudFormation template is configured to launch an instance with the new AMI into your cluster before removing an old one, one at a time\. This configuration ensures that you always have your Auto Scaling group's desired count of active instances in your cluster during the rolling update\.

**Note**  
This method isn't supported for node groups that were created with `eksctl`\. If you created your cluster or node group with `eksctl`, see [Migrating to a new node group](migrate-stack.md)\.

**To update an existing node group**

1. Determine the DNS provider for your cluster\.

   ```
   kubectl get deployments -l k8s-app=kube-dns -n kube-system
   ```

   An example output is as follows\. This cluster is using CoreDNS for DNS resolution, but your cluster might return `kube-dns` instead\. Your output might look different depending on the version of `kubectl` that you're using\.

   ```
   NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   coredns   1         1         1            1           31m
   ```

1. If your current deployment is running fewer than two replicas, scale out the deployment to two replicas\. Replace *`coredns`* with **`kube-dns`** if your previous command output returned that instead\.

   ```
   kubectl scale deployments/coredns --replicas=2 -n kube-system
   ```

1. \(Optional\) If you're using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment down to zero \(0\) replicas to avoid conflicting scaling actions\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=0 -n kube-system
   ```

1. <a name="existing-worker-settings-step"></a>Determine the instance type and desired instance count of your current node group\. You enter these values later when you update the AWS CloudFormation template for the group\.

   1. Open the Amazon EC2 console at [https://console\.aws\.amazon\.com/ec2/](https://console.aws.amazon.com/ec2/)\.

   1. In the left navigation pane, choose **Launch Configurations**, and note the instance type for your existing node launch configuration\.

   1. In the left navigation pane, choose **Auto Scaling Groups**, and note the **Desired** instance count for your existing node Auto Scaling group\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Select your node group stack, and then choose **Update**\.

1. Select **Replace current template** and select **Amazon S3 URL**\.

1. For **Amazon S3 URL**, paste the following URL into the text area to ensure that you're using the latest version of the node AWS CloudFormation template\. Then, choose **Next**:

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2022-12-23/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify stack details** page, fill out the following parameters, and choose **Next**:
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired instance count that you recorded in a [previous step](#existing-worker-settings-step)\. Or, enter your new desired number of nodes to scale to when your stack is updated\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your node Auto Scaling group can scale out\. This value must be at least one node more than your desired capacity\. This is so that you can perform a rolling update of your nodes without reducing your node count during the update\.
   + **NodeInstanceType** – Choose the instance type your recorded in a [previous step](#existing-worker-settings-step)\. Alternatively, choose a different instance type for your nodes\. Before choosing a different instance type, review [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. Each Amazon EC2 instance type supports a maximum number of elastic network interfaces \(network interface\) and each network interface supports a maximum number of IP addresses\. Because each worker node and Pod ,is assigned its own IP address, it's important to choose an instance type that will support the maximum number of Pods that you want to run on each Amazon EC2 node\. For a list of the number of network interfaces and IP addresses supported by instance types, see [ IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI)\. For example, the `m5.large` instance type supports a maximum of 30 IP addresses for the worker node and Pods\.
**Note**  
The supported instance types for the latest version of the [https://github.com/aws/amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s) are shown in [vpc\_ip\_resource\_limit\.go](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/pkg/vpc/vpc_ip_resource_limit.go) on GitHub\. You might need to update your Amazon VPC CNI plugin for Kubernetes version to use the latest supported instance types\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.
**Important**  
Some instance types might not be available in all AWS Regions\.
   + **NodeImageIdSSMParam** – The Amazon EC2 Systems Manager parameter of the AMI ID that you want to update to\. The following value uses the latest Amazon EKS optimized AMI for Kubernetes version `1.29`\.

     ```
     /aws/service/eks/optimized-ami/1.29/amazon-linux-2/recommended/image_id
     ```

     You can replace `1.29` with a [supported Kubernetes version](platform-versions.md) that's the same\. Or, it should be up to one version earlier than the Kubernetes version running on your control plane\. We recommend that you keep your nodes at the same version as your control plane\. You can also replace `amazon-linux-2` with a different AMI type\. For more information, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
**Note**  
Using the Amazon EC2 Systems Manager parameter enables you to update your nodes in the future without having to look up and specify an AMI ID\. If your AWS CloudFormation stack is using this value, any stack update always launches the latest recommended Amazon EKS optimized AMI for your specified Kubernetes version\. This is even the case even if you don't change any values in the template\.
   + **NodeImageId** – To use your own custom AMI, enter the ID for the AMI to use\.
**Important**  
This value overrides any value specified for **NodeImageIdSSMParam**\. If you want to use the **NodeImageIdSSMParam** value, ensure that the value for **NodeImageId** is blank\.
   + **DisableIMDSv1** – By default, each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2\. However, you can disable IMDSv1\. Select **true** if you don't want any nodes or any Pods scheduled in the node group to use IMDSv1\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. If you've implemented IAM roles for service accounts, assign necessary permissions directly to all Pods that require access to AWS services\. This way, no Pods in your cluster require access to IMDS for other reasons, such as retrieving the current AWS Region\. Then, you can also disable access to IMDSv2 for Pods that don't use host networking\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\. 

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Update stack**\.
**Note**  
The update of each node in the cluster takes several minutes\. Wait for the update of all nodes to complete before performing the next steps\.

1. If your cluster's DNS provider is `kube-dns`, scale in the `kube-dns` deployment to one replica\.

   ```
   kubectl scale deployments/kube-dns --replicas=1 -n kube-system
   ```

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment back to your desired amount of replicas\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=1 -n kube-system
   ```

1. \(Optional\) Verify that you're using the latest version of the [https://github.com/aws/amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s)\. You might need to update your Amazon VPC CNI plugin for Kubernetes version to use the latest supported instance types\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.