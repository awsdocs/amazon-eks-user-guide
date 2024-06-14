--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Updating an existing self\-managed node group<a name="update-stack"></a>

This topic describes how you can update an existing AWS CloudFormation self\-managed node stack with a new AMI\. You can use this procedure to update your nodes to a new version of Kubernetes following a cluster update\. Otherwise, you can update to the latest Amazon EKS optimized AMI for an existing Kubernetes version\.

**Important**  

The latest default Amazon EKS node AWS CloudFormation template is configured to launch an instance with the new AMI into your cluster before removing an old one, one at a time\. This configuration ensures that you always have your Auto Scaling group’s desired count of active instances in your cluster during the rolling update\.

**Note**  

1. Determine the DNS provider for your cluster\.

   ```
   kubectl get deployments -l k8s-app=kube-dns -n kube-system
   ```

   An example output is as follows\. This cluster is using CoreDNS for DNS resolution, but your cluster might return `kube-dns` instead\. Your output might look different depending on the version of `kubectl` that you’re using\.

   ```
   NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   coredns   1         1         1            1           31m
   ```

1. If your current deployment is running fewer than two replicas, scale out the deployment to two replicas\. Replace * `coredns` with ` kube-dns if your previous command output returned that instead.` 

   ```
   kubectl scale deployments/coredns --replicas=2 -n kube-system
   ``` *  \(Optional\) If you’re using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment down to zero \(0\) replicas to avoid conflicting scaling actions\. 

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=0 -n kube-system
   ```    Determine the instance type and desired instance count of your current node group\. You enter these values later when you update the AWS CloudFormation template for the group\.   Open the Amazon EC2 console at [https://console\.aws\.amazon\.com/ec2/](https://console.aws.amazon.com/ec2/)\.   In the left navigation pane, choose **Launch Configurations**, and note the instance type for your existing node launch configuration\.   In the left navigation pane, choose **Auto Scaling Groups**, and note the **Desired** instance count for your existing node Auto Scaling group\.     Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.   Select your node group stack, and then choose **Update**\.   Select **Replace current template** and select **Amazon S3 URL**\.   For **Amazon S3 URL**, paste the following URL into the text area to ensure that you’re using the latest version of the node AWS CloudFormation template\. Then, choose **Next**: 

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2022-12-23/amazon-eks-nodegroup.yaml
   ```   On the **Specify stack details** page, fill out the following parameters, and choose **Next**:    **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your node Auto Scaling group can scale out\. This value must be at least one node more than your desired capacity\. This is so that you can perform a rolling update of your nodes without reducing your node count during the update\.  Some instance types might not be available in all AWS Regions\.     **NodeImageIdSSMParam** – The Amazon EC2 Systems Manager parameter of the AMI ID that you want to update to\. The following value uses the latest Amazon EKS optimized AMI for Kubernetes version `1.29`\. 

     ```
     /aws/service/eks/optimized-ami/1.29/amazon-linux-2/recommended/image_id
     ```  Using the Amazon EC2 Systems Manager parameter enables you to update your nodes in the future without having to look up and specify an AMI ID\. If your AWS CloudFormation stack is using this value, any stack update always launches the latest recommended Amazon EKS optimized AMI for your specified Kubernetes version\. This is even the case even if you don’t change any values in the template\.     **NodeImageId** – To use your own custom AMI, enter the ID for the AMI to use\.  This value overrides any value specified for **NodeImageIdSSMParam**\. If you want to use the **NodeImageIdSSMParam** value, ensure that the value for **NodeImageId** is blank\.     **DisableIMDSv1** – By default, each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2\. However, you can disable IMDSv1\. Select **true** if you don’t want any nodes or any Pods scheduled in the node group to use IMDSv1\. For more information about IMDS, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/configuring\-instance\-metadata\-service\.html\[Configuring the instance metadata service\]\. If you’ve implemented IAM roles for service accounts, assign necessary permissions directly to all Pods that require access to AWS services\. This way, no Pods in your cluster require access to IMDS for other reasons, such as retrieving the current AWS Region\. Then, you can also disable access to IMDSv2 for Pods that don’t use host networking\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.     \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.   On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Update stack**\.  The update of each node in the cluster takes several minutes\. Wait for the update of all nodes to complete before performing the next steps\.    If your cluster’s DNS provider is `kube-dns`, scale in the `kube-dns` deployment to one replica\. 

   ```
   kubectl scale deployments/kube-dns --replicas=1 -n kube-system
   ```   \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment back to your desired amount of replicas\. 

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=1 -n kube-system
   ```  