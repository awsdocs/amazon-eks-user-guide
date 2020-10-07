# Updating an existing self\-managed node group<a name="update-stack"></a>

This topic helps you to update an existing AWS CloudFormation self\-managed node stack with a new AMI\. You can use this procedure to update your nodes to a new version of Kubernetes following a cluster update, or you can update to the latest Amazon EKS optimized AMI for an existing Kubernetes version\.

**Important**  
This topic covers node updates for self\-managed nodes\. If you are using [Managed node groups](managed-node-groups.md), see [Updating a managed node group](update-managed-node-group.md)\.

The latest default Amazon EKS node AWS CloudFormation template is configured to launch an instance with the new AMI into your cluster before removing an old one, one at a time\. This configuration ensures that you always have your Auto Scaling group's desired count of active instances in your cluster during the rolling update\.

**Note**  
This method is not supported for node groups that were created with `eksctl`\. If you created your cluster or node group with `eksctl`, see [Migrating to a new node group](migrate-stack.md)\.

**To update an existing node group**

1. Determine your cluster's DNS provider\.

   ```
   kubectl get deployments -l k8s-app=kube-dns -n kube-system
   ```

   Output \(this cluster is using `kube-dns` for DNS resolution, but your cluster may return `coredns` instead\):

   ```
   NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   <kube-dns>   1         1         1            1           31m
   ```

1. If your current deployment is running fewer than two replicas, scale out the deployment to two replicas\. Substitute `coredns` for `kube-dns` if your previous command output returned that instead\.

   ```
   kubectl scale deployments/<kube-dns> --replicas=2 -n kube-system
   ```

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment down to zero replicas to avoid conflicting scaling actions\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=0 -n kube-system
   ```

1. <a name="existing-worker-settings-step"></a>Determine the instance type and desired instance count of your current node group\. You will enter these values later when you update the AWS CloudFormation template for the group\.

   1. Open the Amazon EC2 console at [https://console\.aws\.amazon\.com/ec2/](https://console.aws.amazon.com/ec2/)\.

   1. Choose **Launch Configurations** in the left navigation, and note the instance type for your existing node launch configuration\.

   1. Choose **Auto Scaling Groups** in the left navigation and note the **Desired** instance count for your existing node Auto Scaling group\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Select your node group stack, and then choose **Update**\.

1. Select **Replace current template** and select **Amazon S3 URL**\.

1. For **Amazon S3 URL**, paste the following URL into the text area to ensure that you are using the latest version of the node AWS CloudFormation template, and then choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-08-12/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify stack details** page, fill out the following parameters, and choose **Next**:
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired instance count that you recorded in a [previous step](#existing-worker-settings-step), or enter a new desired number of nodes to scale to when your stack is updated\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your node Auto Scaling group can scale out\. **This value must be at least one node greater than your desired capacity so that you can perform a rolling update of your nodes without reducing your node count during the update\.**
   + **NodeInstanceType** – Choose the instance type your recorded in a [previous step](#existing-worker-settings-step), or choose a different instance type for your nodes\. Each Amazon EC2 instance type supports a maximum number of elastic network interfaces \(ENIs\) and each ENI supports a maximum number of IP addresses\. Since each worker node and pod is assigned its own IP address it's important to choose an instance type that will support the maximum number of pods that you want to run on each worker node\. For a list of the number of ENIs and IP addresses supported by instance types, see [ IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI)\. For example, the `m5.large` instance type supports a maximum of 30 IP addresses for the worker node and pods\. Some instance types might not be available in all Regions\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.7/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all Regions\.
   + **NodeImageIdSSMParam** – The Amazon EC2 Systems Manager parameter of the AMI ID that you want to update to\. The following value uses the latest Amazon EKS optimized AMI for Kubernetes version 1\.17\.

     ```
     /aws/service/eks/optimized-ami/<1.17>/<amazon-linux-2>/recommended/image_id
     ```

     You can replace 1\.17 with any [supported Kubernetes version](platform-versions.md)\. If you want to use the Amazon EKS optimized accelerated AMI, then replace `<amazon-linux-2>` with `<amazon-linux-2-gpu>`\.
**Note**  
Using the Amazon EC2 Systems Manager parameter enables you to update your nodes in the future without having to lookup and specify an AMI ID\. If your AWS CloudFormation stack is using this value, any stack update will always launch the latest recommended Amazon EKS optimized AMI for your specified Kubernetes version, even if you don't change any values in the template\.
   + **NodeImageId** – To use your own custom AMI, enter the ID for the AMI to use\.
**Important**  
This value overrides any value specified for **NodeImageIdSSMParam**\. If you want to use the **NodeImageIdSSMParam** value, ensure that the value for **NodeImageId** is blank\.

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
   kubectl scale deployments/cluster-autoscaler --replicas=<1> -n kube-system
   ```

1. \(Optional\) Verify that you are using the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.