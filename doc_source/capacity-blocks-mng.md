# Create a managed node group with Amazon EC2 Capacity Blocks for ML<a name="capacity-blocks-mng"></a>

Capacity Blocks for machine learning \(ML\) allow you to reserve GPU instances on a future date to support your short duration ML workloads\. For more information, see [Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html) in the *Amazon EC2 User Guide for Linux Instances*\.

## Considerations<a name="capacity-blocks-mng-considerations"></a>

**Important**  
Capacity Blocks are only available for certain Amazon EC2 instance types and AWS Regions\. For compatibility information, see [Work with Capacity Blocks Prerequisites](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/capacity-blocks-using.html#capacity-blocks-prerequisites) in the *Amazon EC2 User Guide for Linux Instances*\.
For more information, see [Use Capacity Blocks for machine learning workloads](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-template-capacity-blocks.html) in the *Amazon EC2 Auto Scaling User Guide*\.
Managed node groups with Capacity Blocks can only be created with custom launch templates\.
When upgrading managed node groups with Capacity Blocks, make sure that the desired size of the node group is set to `0`\.

## Create a managed node group with Amazon EC2 Capacity Blocks<a name="capacity-blocks-mng-procedure"></a>

You can use Capacity Blocks with Amazon EKS managed node groups for provisioning and scaling GPU\-accelerated worker nodes\. The AWS CloudFormation template examples that follow don’t cover every aspect needed in a production clusters\. Typically, you’d also want a bootstrapping script to join the node to the cluster and specify the Amazon EKS accelerated AMI\. For more information, see [Creating a managed node group](create-managed-node-group.md)\.

1. Create a launch template that's appropriate for your workloads and works with Amazon EKS managed node groups\. For more information, see [Customizing managed nodes with launch templates](launch-templates.md)\.

   In addition to the requirements in the above procedures, make sure that the `LaunchTemplateData` includes the following:
   + `InstanceMarketOptions` with `MarketType` set to `"capacity-block"` 
   + `CapacityReservationSpecification: CapacityReservationTarget` with `CapacityReservationId` set to the Capacity Block \(for example: `cr-02168da1478b509e0` \)
   + `InstanceType` set to an instance type that supports Capacity Blocks \(for example: `p5.48xlarge`\)

   The following is an excerpt of a CloudFormation template that creates a launch template targeting a Capacity Block\. To create a custom AMI managed node group, you can also add `ImageId` and `UserData` parameters\.

   ```
   NodeLaunchTemplate:
     Type: "AWS::EC2::LaunchTemplate"
     Properties:
       LaunchTemplateData:
         InstanceMarketOptions:
           MarketType: "capacity-block"
         CapacityReservationSpecification:
           CapacityReservationTarget:
             CapacityReservationId: "cr-02168da1478b509e0"
         InstanceType: p5.48xlarge
   ```

1. Use the launch template to create a managed node group\.

   The following is an example create node group command for Capacity Blocks\. Replace `example-values` with ones applicable to your cluster\.

   When creating the Capacity Block managed node group, do the following:
   + Set the `capacity-type` to `"CAPACITY_BLOCK"`\. If the capacity type isn’t set to `"CAPACITY_BLOCK"` or any of the other above required launch template values are missing, then the create request will be rejected\.
   + When specifying `subnets` in the create request, make sure to only specify the subnet in the same Availability Zone as the capacity reservation\.
   + If you specify a non\-zero `desiredSize` in the create request, Amazon EKS will honor that when creating the Auto Scaling group \(ASG\)\. However, if the create request is made before the capacity reservation is active, then the ASG won’t be able to launch Amazon EC2 instances until it becomes active\. As a result, ASG scaling activities will have launch errors\. Whenever the reservation becomes active, then the launch of instances will succeed and the ASG will be scaled up to the `desiredSize` mentioned at create time\.

   ```
   aws eks create-nodegroup \
       --cluster-name my-cluster \
       --nodegroup-name my-mng \
       --node-role node-role-arn \
       --region region-code \
       --subnets subnet-id \
       --scaling-config minSize=node-group-min-size,maxSize=node-group-max-size,desiredSize=node-group-desired-size \
       --capacity-type "CAPACITY_BLOCK" \
       --launch-template id="lt-id",version=1
   ```

1. Make sure that the nodes join after scale up\. Amazon EKS clusters using managed node groups with Capacity Blocks don't perform any validations that instances launched actually join and register with the cluster\.

1. If you set `desiredSize` to `0` at create time, then you have different options to scale up the node group when the capacity reservation becomes active:
   + Create a scheduled scaling policy for the ASG that aligns to the Capacity Block reservation start time\. For more information, see [Scheduled scaling for Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html) in the *Amazon EC2 Auto Scaling User Guide*\.
   + Use the Amazon EKS console or `eks update-nodegroup-config` to update the scaling config and set the desired size of the node group\.
   + Use the Kubernetes Cluster Autoscaler\. For more information, see [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)\.

1. The node group is now ready for workloads and Pods to be scheduled\.

1. In order for your Pods to be gracefully drained before reservation ends, Amazon EKS uses a scheduled scaling policy to scale down the node group size to `0` \. This scheduled scaling will be set with name titled `Amazon EKS Node Group Capacity Scaledown Before Reservation End` \. We recommend not editing or deleting this action\.

   Amazon EC2 starts shutting down the instances 30 minutes before reservation end time\. As a result, Amazon EKS will setup a scheduled scale down on the node group 40 minutes prior to their reservation end in order to safely and gracefully evict Pods\.