# Amazon EKS service quotas<a name="service-quotas"></a>

The following table provides the default quotas \(also referred to as limits\) for Amazon EKS for an AWS account that can be changed\. To request a quota increase, open the [AWS Support Center](https://console.aws.amazon.com/support/home#/) page, sign in if necessary, and choose **Create case**\. Choose **Service limit increase**\. Complete and submit the form\.


| Resource | Default quota | 
| --- | --- | 
| Maximum number of Amazon EKS clusters \(per Region, per account\) | 100 | 
| Maximum number of managed node groups per cluster | 30 | 
| Maximum number of nodes per managed node group | 100 | 
| Maximum number Fargate profiles per cluster | 10 | 
| Maximum number selectors per Fargate profile | 5 | 
| Maximum number of label pairs per Fargate profile selector | 5 | 
| Maximum number of concurrent Fargate pods \(per Region, per account\)\. The Fargate pods that you run count against the Tasks using the Fargate launch type or the FARGATE capacity provider, per Region, per account quota listed in [Amazon ECS service quotas](https://docs.aws.amazon.com/AmazonECS/latest/userguide/service-quotas.html)\. As a result, all of your running Amazon ECS tasks using the Fargate launch type and Amazon EKS Fargate pods count against this quota\. | 100 | 

The following table provides quotas for Amazon EKS that cannot be changed\.


| Resource | Default quota | 
| --- | --- | 
| Maximum number of control plane security groups per cluster \(these are specified when you create the cluster\) | 4 | 
| Maximum number of public endpoint access CIDR ranges per cluster | 40 | 
| Maximum number Fargate pod launches per second \(per Region, per account\) | 1, with temporary burst up to 10 | 

You can also view your Amazon EKS quotas using Service Quotas, an AWS service that enables you to view and manage your quotas from a central location\. For more information, see [What is service quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) in the *Service Quotas User Guide*\. Service Quotas makes it easy to look up the value of all of the Amazon EKS service quotas using the AWS Management Console or AWS CLI\. Choose the tool that you'd like to use to view your service quotas\.

## AWS Management Console<a name="sq-console"></a>

**To view Amazon EKS service quotas using the AWS Management Console**

1. Open the Service Quotas console at [https://console\.aws\.amazon\.com/servicequotas/](https://console.aws.amazon.com/servicequotas/)\.

1. In the navigation pane, choose **AWS services**\.

1. From the **AWS services** list, search for and select **Amazon Elastic Kubernetes Service \(Amazon EKS\)**\.

   In the **Service quotas** list, you can see the service quota name, applied value \(if it is available\), AWS default quota, and whether the quota value is adjustable\.

1. To view additional information about a service quota, such as the description, choose the quota name\.

1. \(Optional\) To request a quota increase, select the quota that you want to increase, select **Request quota increase**, enter or select the required information, and select **Request**\.

To work more with service quotas using the AWS Management Console see the [Service Quotas User Guide](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)\. To request a quota increase, see [Requesting a Quota Increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*\.

The following Amazon EKS quotas are not shown in the Service Quotas console\.


| Resource | Default quota | 
| --- | --- | 
| [Maximum number of concurrent Fargate pods \(per Region, per account\)](https://console.aws.amazon.com/servicequotas/home?#!/services/ecs/quotas/L-46458851)\. The Fargate pods that you run count against the Tasks using the Fargate launch type, per Region, per account quota listed in [Amazon ECS service quotas](https://docs.aws.amazon.com/AmazonECS/latest/userguide/service-quotas.html)\. As a result, all of your running Amazon ECS tasks using the Fargate launch type and Amazon EKS Fargate pods count against this quota\. | 100 \(can be increased\) | 
| Maximum number Fargate pod launches per second \(per Region, per account\) | 1, with temporary burst up to 10 \(cannot be increased\) | 

To request a quota increase for the `Maximum number of concurrent Fargate pods (per Region, per account)` quota, select the quota in the previous table to open the AWS Management Console\. Select **Request quota increase**, enter or select the required information, and then select **Request**\.

**Note**  
This quota is an Amazon ECS quota\.

## AWS CLI<a name="sq-cli"></a>

**To view Amazon EKS service quotas using the AWS CLI**  
Run the following command\.

```
aws service-quotas list-aws-default-service-quotas \
    -query 'Quotas[*].{Adjustable:Adjustable,Name:QuotaName,Value:Value,Code:QuotaCode}' \
    -service-code eks \
    -output table
```

To work more with service quotas using the AWS CLI, see the [Service Quotas AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\. To request a quota increase, see the [https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html) command in the [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\.

The following Amazon EKS quotas are not returned by the previous command\.


| Resource | Default quota | 
| --- | --- | 
| [Maximum number of concurrent Fargate pods \(per Region, per account\)](https://console.aws.amazon.com/servicequotas/home?#!/services/ecs/quotas/L-46458851)\. The Fargate pods that you run count against the Tasks using the Fargate launch type, per Region, per account quota listed in [Amazon ECS service quotas](https://docs.aws.amazon.com/AmazonECS/latest/userguide/service-quotas.html)\. As a result, all of your running Amazon ECS tasks using the Fargate launch type and Amazon EKS Fargate pods count against this quota\. | 100 \(can be increased\) | 
| Maximum number Fargate pod launches per second \(per Region, per account\) | 1, with temporary burst up to 10 \(cannot be increased\) | 

To request a quota increase for the `Maximum number of concurrent Fargate pods (per Region, per account)` quota, enter the following command\.

**Note**  
This quota is an Amazon ECS quota\.

```
aws service-quotas request-service-quota-increase \
    --service-code ecs \
    --quota-code L-46458851 \
    --desired-value your-desired-value
```