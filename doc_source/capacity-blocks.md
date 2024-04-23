# Capacity Blocks for ML<a name="capacity-blocks"></a>

**Important**  
Capacity Blocks are only available for certain Amazon EC2 instance types and AWS Regions\. For compatibility information, see [Use Capacity Blocks for machine learning workloads](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-template-capacity-blocks.html) in the *Amazon EC2 Auto Scaling User Guide*\.
Capacity Blocks currently cannot be used with Amazon EKS managed node groups or Karpenter\.

Capacity Blocks for machine learning \(ML\) allow you to reserve GPU instances on a future date to support your short duration ML workloads\. Instances that run inside a Capacity Block are automatically placed close together inside [Amazon EC2 UltraClusters](https://aws.amazon.com/ec2/ultraclusters/), so there is no need to use a cluster placement group\. For more information, see [Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html) in the *Amazon EC2 User Guide for Linux Instances*\.

You can use Capacity Blocks with Amazon EKS for provisioning and scaling your self\-managed nodes\. The following steps give a general example overview\.

1. Create a launch template in the AWS Management Console\. For more information, see [Use Capacity Blocks for machine learning workloads](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-template-capacity-blocks.html) in the *Amazon EC2 Auto Scaling User Guide*\.

   Make sure to include configuration of instance type and Amazon Machine Image \(AMI\)\.

1. Link the Capacity Block to a launch template using the capacity reservation ID\.

   The following is an example AWS CloudFormation template to create a launch template targeting a Capacity Block:

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
           IamInstanceProfile:
             Arn: iam-instance-profile-arn
           ImageId: image-id
           InstanceType: p5.48xlarge
           KeyName: key-name
           SecurityGroupIds:
           - sg-05b1d815d1EXAMPLE
           UserData: user-data
   ```

   You must pass the subnet in the Availability Zone in which the reservation is made because Capacity Blocks are zonal\.

1. If you are creating the self managed node group prior to the capacity reservation becoming active, then set the desired capacity to `0`\. When creating the node group, make sure that you are only specifying the respective subnet for the Availability Zone in which the capacity is reserved\.

   The following is a sample CloudFormation template that can be used\. This example gets the `LaunchTemplateId` and `Version` of the `AWS::Amazon EC2::LaunchTemplate` resource shown in the previous example\. It also gets the values for `DesiredCapacity`, `MaxSize`, `MinSize`, and `VPCZoneIdentifier` that are declared elsewhere in the same template\.

   ```
     NodeGroup:
       Type: "AWS::AutoScaling::AutoScalingGroup"
       Properties:
         DesiredCapacity: !Ref NodeAutoScalingGroupDesiredCapacity
         LaunchTemplate:
           LaunchTemplateId: !Ref NodeLaunchTemplate
           Version: !GetAtt NodeLaunchTemplate.LatestVersionNumber
         MaxSize: !Ref NodeAutoScalingGroupMaxSize
         MinSize: !Ref NodeAutoScalingGroupMinSize
         VPCZoneIdentifier: !Ref Subnets
         Tags:
           - Key: Name
             PropagateAtLaunch: true
             Value: !Sub ${ClusterName}-${NodeGroupName}-Node
           - Key: !Sub kubernetes.io/cluster/${ClusterName}
             PropagateAtLaunch: true
             Value: owned
   ```

1. Once the node group is created successfully, make sure to record the `NodeInstanceRole` for the node group that was created\. You need this in order to make sure that when node group is scaled, the new nodes join the cluster and Kubernetes is able to recognize the nodes\. For more information, see the AWS Management Console instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\.

1. We recommend that you create a scheduled scaling policy for the Auto Scaling group that aligns to the Capacity Block reservation times\. For more information, see [Scheduled scaling for Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html) in the *Amazon EC2 Auto Scaling User Guide*\.

   You can use all of the instances you reserved until 30 minutes before the end time of the Capacity Block\. Instances that are still running at that time will start terminating\. To allow sufficient time to gracefully drain the node\(s\), we suggest that you schedule scaling to scale to zero more than 30 minutes before the Capacity Block reservation end time\.

   If you want to instead scale up manually whenever the capacity reservation becomes `Active`, then you need to update the Auto Scaling group's desired capacity at the start time of the Capacity Block reservation\. Then you would need to also scale down manually more than 30 minutes before the Capacity Block reservation end time\.

1. The node group is now ready for workloads and Pods to be scheduled\.

1. In order for your Pods to be gracefully drained, we recommend that you set up AWS Node Termination Handler\. This handler will be able to watch for "ASG Scale\-in" lifecycle events from Amazon EC2 Auto Scaling using EventBridge and allow the Kubernetes control plane to take required action before the instance becomes unavailable\. Otherwise, your Pods and Kubernetes objects will get stuck in a pending state\. For more information, see [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler) on GitHub\.

   If you don't setup a Node Termination Handler, we recommend that you start draining your Pods manually before hitting the 30 minute window so that they have enough time to be gracefully drained\.