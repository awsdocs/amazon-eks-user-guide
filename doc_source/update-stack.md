# Updating an Existing Worker Node Group<a name="update-stack"></a>

This topic helps you to update an existing AWS CloudFormation worker node stack with a new AMI\. You can use this procedure to update your worker nodes to a new version of Kubernetes following a cluster update, or you can update to the latest Amazon EKS\-optimized AMI for an existing Kubernetes version\.

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

1. Select your worker node group stack, and then choose **Actions**, **Update stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area to ensure that you are using the latest version of the worker node AWS CloudFormation template, and then choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify Details** page, fill out the following parameters, and choose **Next**:
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired instance count that you recorded in [Step 4](#existing-woker-settings-step), or enter a new desired number of nodes to scale to when your stack is updated\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your worker node Auto Scaling group can scale out\. **This value must be at least one node greater than your desired capacity so that you can perform a rolling update of your worker nodes without reducing your node count during the update\.**
   + **NodeInstanceType** – Choose the instance type your recorded in [Step 4](#existing-woker-settings-step), or choose a different instance type for your worker nodes\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.4/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all regions\.
   + **NodeImageId** – Enter the current Amazon EKS worker node AMI ID for your Region\. The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.
**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.13\.7 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-stack.html)

------
#### [ Kubernetes version 1\.12\.7 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-stack.html)

------
#### [ Kubernetes version 1\.11\.9 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-stack.html)

------
#### [ Kubernetes version 1\.10\.13 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-stack.html)

------
**Note**  
The Amazon EKS worker node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Update**\.
**Note**  
Wait for the update to complete before performing the next steps\.

1. If your cluster's DNS provider is `kube-dns`, scale in the `kube-dns` deployment to one replica\.

   ```
   kubectl scale deployments/kube-dns --replicas=1 -n kube-system
   ```

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment back to one replica\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=1 -n kube-system
   ```

1. \(Optional\) Verify that you are using the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.