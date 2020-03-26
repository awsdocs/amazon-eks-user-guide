# Updating an Existing Worker Node Group<a name="update-stack"></a>

This topic helps you to update an existing AWS CloudFormation self\-managed worker node stack with a new AMI\. You can use this procedure to update your worker nodes to a new version of Kubernetes following a cluster update, or you can update to the latest Amazon EKS\-optimized AMI for an existing Kubernetes version\.

**Important**  
This topic covers worker node updates for self\-managed node groups\. If you are using [Managed Node Groups](managed-node-groups.md), see [Updating a Managed Node Group](update-managed-node-group.md)\.

The latest default Amazon EKS worker node AWS CloudFormation template is configured to launch an instance with the new AMI into your cluster before removing an old one, one at a time\. This configuration ensures that you always have your Auto Scaling group's desired count of active instances in your cluster during the rolling update\.

**Note**  
This method is not supported for worker node groups that were created with `eksctl`\. If you created your cluster or worker node group with `eksctl`, see [Migrating to a New Worker Node Group](migrate-stack.md)\.

**To update an existing worker node group**

1. Determine your cluster's DNS provider\.

   ```
   kubectl get deployments -l k8s-app=kube-dns -n kube-system
   ```

   Output \(this cluster is using `kube-dns` for DNS resolution, but your cluster may return `coredns` instead\):

   ```
   NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   kube-dns   1         1         1            1           31m
   ```

1. If your current deployment is running fewer than two replicas, scale out the deployment to two replicas\. Substitute `coredns` for `kube-dns` if your previous command output returned that instead\.

   ```
   kubectl scale deployments/kube-dns --replicas=2 -n kube-system
   ```

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment down to zero replicas to avoid conflicting scaling actions\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=0 -n kube-system
   ```

1. <a name="existing-woker-settings-step"></a>Determine the instance type and desired instance count of your current worker node group\. You will enter these values later when you update the AWS CloudFormation template for the group\.

   1. Open the Amazon EC2 console at [https://console\.aws\.amazon\.com/ec2/](https://console.aws.amazon.com/ec2/)\.

   1. Choose **Launch Configurations** in the left navigation, and note the instance type for your existing worker node launch configuration\.

   1. Choose **Auto Scaling Groups** in the left navigation and note the **Desired** instance count for your existing worker node Auto Scaling group\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Select your worker node group stack, and then choose **Update**\.

1. Select **Replace current template** and select **Amazon S3 URL**\.

1. For **Amazon S3 URL**, paste the following URL into the text area to ensure that you are using the latest version of the worker node AWS CloudFormation template, and then choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-03-23/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify stack details** page, fill out the following parameters, and choose **Next**:
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired instance count that you recorded in [Step 4](#existing-woker-settings-step), or enter a new desired number of nodes to scale to when your stack is updated\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your worker node Auto Scaling group can scale out\. **This value must be at least one node greater than your desired capacity so that you can perform a rolling update of your worker nodes without reducing your node count during the update\.**
   + **NodeInstanceType** – Choose the instance type your recorded in [Step 4](#existing-woker-settings-step), or choose a different instance type for your worker nodes\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.5/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all Regions\.
   + **NodeImageIdSSMParam** – The Amazon EC2 Systems Manager parameter of the AMI ID that you want to update to\. The following value uses the latest Amazon EKS\-optimized AMI for Kubernetes version 1\.15\.

     ```
     /aws/service/eks/optimized-ami/1.15/amazon-linux-2/recommended/image_id
     ```

     You can change the *1\.15* value to any [supported Kubernetes version](platform-versions.md)\. If you want to use the Amazon EKS\-optimized AMI with GPU support, then change `amazon-linux-2` to `amazon-linux-2-gpu`\.
**Note**  
Using the Amazon EC2 Systems Manager parameter enables you to update your worker nodes in the future without having to lookup and specify an AMI ID\. If your AWS CloudFormation stack is using this value, any stack update will always launch the latest recommended Amazon EKS\-optimized AMI for your specified Kubernetes version, even if you don't change any values in the template\.
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

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment back to one replica\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=1 -n kube-system
   ```

1. \(Optional\) Verify that you are using the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.