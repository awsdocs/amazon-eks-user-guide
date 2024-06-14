# Enable Auto Scaling group metrics collection<a name="enable-asg-metrics"></a>

This topic describes how you can enable Auto Scaling group metrics collection using [AWS Lambda](https://aws.amazon.com/lambda) and [AWS CloudTrail](https://aws.amazon.com/cloudtrail)\. Amazon EKS doesn't automatically enable group metrics collection for Auto Scaling groups created for managed nodes\.

You can use [Auto Scaling group metrics](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-cloudwatch-monitoring.html) to track changes in an Auto Scaling group and to set alarms on threshold values\. Auto Scaling group metrics are available in the Auto Scaling console or the [Amazon CloudWatch](https://aws.amazon.com/cloudwatch) console\. Once enabled, the Auto Scaling group sends sampled data to Amazon CloudWatch every minute\. There is no charge for enabling these metrics\.

By enabling Auto Scaling group metrics collection, you'll be able to monitor the scaling of managed node groups\. Auto Scaling group metrics report the minimum, maximum, and desired size of an Auto Scaling group\. You can create an alarm if the number of nodes in a node group falls below the minimum size, which would indicate an unhealthy node group\. Tracking node group size is also useful in adjusting the maximum count so that your data plane doesn't run out of capacity\.

When you create a managed node group, AWS CloudTrail sends a `CreateNodegroup` event to [Amazon EventBridge](https://aws.amazon.com/eventbridge)\. By creating an Amazon EventBridge rule that matches the `CreateNodegroup` event, you trigger a Lambda function to enable group metrics collection for the Auto Scaling group associated with the managed node group\.

![\[Diagram showing the managed node group, CloudTrail, and EventBridge component\]](http://docs.aws.amazon.com/eks/latest/userguide/images/enable-asg-metrics.png)

**To enable Auto Scaling group metrics collection**

1. Create an IAM role for Lambda\.

   ```
   LAMBDA_ROLE=$(aws iam create-role \
     --role-name lambda-asg-enable-metrics \
     --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' \
     --output text \
     --query 'Role.Arn')
   echo $LAMBDA_ROLE
   ```

1. Create a policy that allows describing Amazon EKS node groups and enabling Auto Scaling group metrics collection\.

   ```
   cat > /tmp/lambda-policy.json <<EOF
   {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
               "eks:DescribeNodegroup",
               "autoscaling:EnableMetricsCollection"
               ],
           "Resource": [
               "*"
           ]
         }
       ]
   }
   EOF
   LAMBDA_POLICY_ARN=$(aws iam create-policy \
     --policy-name lambda-asg-enable-metrics-policy \
     --policy-document file:///tmp/lambda-policy.json \
     --output text \
     --query 'Policy.Arn')
   echo $LAMBDA_POLICY_ARN
   ```

1. Attach the policy to the IAM role for Lambda\.

   ```
   aws iam attach-role-policy \
     --policy-arn $LAMBDA_POLICY_ARN \
     --role-name lambda-asg-enable-metrics
   ```

1. Add the `AWSLambdaBasicExecutionRole` managed policy, which has the permissions that the function needs to write logs to CloudWatch Logs\.

   ```
   aws iam attach-role-policy \
     --role-name lambda-asg-enable-metrics \
     --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```

1. Create the Lambda code\.

   ```
   cat > /tmp/lambda-handler.py <<EOF
   import json
   import boto3
   import time
   import logging
   
   eks = boto3.client('eks')
   autoscaling = boto3.client('autoscaling')
   
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   
   def lambda_handler(event, context):
       ASG_METRICS_COLLLECTION_TAG_NAME = "ASG_METRICS_COLLLECTION_ENABLED"
       initial_retry_delay = 10
       attempts = 0 
       
       #print(event)
       
       if not event["detail"]["eventName"] == "CreateNodegroup":
           print("invalid event.")
           return -1
           
       clusterName = event["detail"]["requestParameters"]["name"]
       nodegroupName = event["detail"]["requestParameters"]["nodegroupName"]
       try:
           metricsCollectionEnabled = event["detail"]["requestParameters"]["tags"][ASG_METRICS_COLLLECTION_TAG_NAME]
       except KeyError:
           print(ASG_METRICS_COLLLECTION_TAG_NAME, "tag not found.")
           return
       
       # Check if metrics collection is enabled in tags
       if metricsCollectionEnabled.lower() != "true":
           print("Metrics collection is not enabled in nodegroup tags.")
           return
       
       # Get the name of the associated autoscaling group
       print("Getting the autoscaling group name for nodegroup=", nodegroupName, ", cluster=", clusterName )
       for i in range(0,10):
           try:
               autoScalingGroup = eks.describe_nodegroup(clusterName=clusterName,nodegroupName=nodegroupName)["nodegroup"]["resources"]["autoScalingGroups"][0]["name"]
           except:
               attempts += 1
               print("Failed to obtain the associated autoscaling group for nodegroup", nodegroupName, "Retrying in", initial_retry_delay*attempts, "seconds.")
               time.sleep(initial_retry_delay*attempts)
           else:
               break
       
       print("Enabling metrics collection on autoscaling group ", autoScalingGroup)
       
       # Enable metrics collection in the autoscaling group
       try:
           enableMetricsCollection = autoscaling.enable_metrics_collection(AutoScalingGroupName=autoScalingGroup,Granularity="1Minute")
       except:
           print("Unable to enable metrics collection on nodegroup=",nodegroup)
       print("Enabled metrics collection on nodegroup", nodegroupName)
   EOF
   ```

1. Create a deployment package\.

   ```
   cd /tmp 
   zip function.zip lambda-handler.py
   ```

1. Create a Lambda function\.

   ```
   LAMBDA_ARN=$(aws lambda create-function --function-name asg-enable-metrics-collection \
     --zip-file fileb://function.zip --handler lambda-handler.lambda_handler \
     --runtime python3.9 \
     --timeout 600 \
     --role $LAMBDA_ROLE \
     --output text \
     --query 'FunctionArn')
   echo $LAMBDA_ARN
   ```

1. Create an EventBridge rule\.

   ```
   RULE_ARN=$(aws events put-rule --name CreateNodegroupRuleToLambda \
     --event-pattern "{\"source\":[\"aws.eks\"],\"detail-type\":[\"AWS API Call via CloudTrail\"],\"detail\":{\"eventName\":[\"CreateNodegroup\"],\"eventSource\":[\"eks.amazonaws.com\"]}}" \
     --output text \
     --query 'RuleArn')
   echo $RULE_ARN
   ```

1. Add the Lambda function as a target\.

   ```
   aws events put-targets --rule CreateNodegroupRuleToLambda \
    --targets "Id"="1","Arn"="$LAMBDA_ARN"
   ```

1. Add a policy that allows EventBridge to invoke the Lambda function\.

   ```
   aws lambda add-permission \
     --function-name asg-enable-metrics-collection \
     --statement-id CreateNodegroupRuleToLambda \
     --action 'lambda:InvokeFunction' \
     --principal events.amazonaws.com \
     --source-arn $RULE_ARN
   ```

The Lambda function enables Auto Scaling group metrics collection for any managed node groups that you tag with `ASG_METRICS_COLLLECTION_ENABLED` set to `TRUE`\. To confirm that **Auto Scaling group metrics collection** is enabled, navigate to the associated Auto Scaling group in the Amazon EC2 console\. In the **Monitoring** tab, you should see that the **Enable** check box is activated\.