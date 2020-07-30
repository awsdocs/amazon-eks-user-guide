# Amazon EKS service quotas<a name="service-quotas"></a>

The following tables provide the default quotas \(also referred to as limits\) for Amazon EKS and AWS Fargate for an AWS account\.

## Amazon EKS service quotas<a name="service-quotas-eks"></a>

The following are Amazon EKS service quotas\.

Most of these service quotas, but not all, are listed under the Amazon Elastic Kubernetes Service \(Amazon EKS\) namespace in the Service Quotas console\. To request a quota increase, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-increase.html) in the *Service Quotas User Guide*\.


|  Service quota  |  Description  |  Default quota value  |  Adjustable  | 
| --- | --- | --- | --- | 
|  Clusters  |  The maximum number of EKS clusters in this account in the current Region\.  |  100  |  Yes  | 
|  Control plane security groups per cluster  |  The maximum number of control plane security groups per cluster \(these are specified when you create the cluster\)\.  |  4  |  No  | 
|  Managed node groups per cluster  |  The maximum number of managed node groups per cluster\.  |  30  |  Yes  | 
|  Nodes per managed node group  |  The maximum number of nodes per managed node group\.  |  100  |  Yes  | 
|  Public endpoint access CIDR ranges per cluster  |  The maximum number of public endpoint access CIDR ranges per cluster \(these are specified when you create or update the cluster\)\.  |  40  |  No  | 
|  Fargate profiles per cluster  | The maximum number Fargate profiles per cluster\. | 10 |  Yes  | 
| Selectors per Fargate profile | The maximum number selectors per Fargate profile | 5 |  Yes  | 
|  Label pairs per Fargate profile selector  | The maximum number of label pairs per Fargate profile selector | 5 |  Yes  | 

## AWS Fargate service quotas<a name="service-quotas-fargate"></a>

The following are Amazon EKS on AWS Fargate service quotas\.

These service quotas are listed under the AWS Fargate namespace in the Service Quotas console\. To request a quota increase, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-increase.html) in the *Service Quotas User Guide*\.


|  Service quota  |  Description  |  Default quota value  |  Adjustable  | 
| --- | --- | --- | --- | 
|  Fargate On\-Demand resource count  |  The maximum number of Amazon ECS tasks or Amazon EKS pods running concurrently on Fargate in this account in the current Region\.  |  100  | Yes | 

## Managing your Amazon EKS and AWS Fargate service quotas in the AWS Management Console<a name="service-quotas-manage"></a>

Amazon EKS has integrated with Service Quotas, an AWS service that enables you to view and manage your quotas from a central location\. For more information, see [What Is Service Quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) in the *Service Quotas User Guide*\.

Service Quotas makes it easy to look up the value of your Amazon EKS service quotas\.

### AWS Management Console<a name="sq-console"></a>

**To view Amazon EKS and Fargate service quotas using the AWS Management Console**

1. Open the Service Quotas console at [https://console\.aws\.amazon\.com/servicequotas/](https://console.aws.amazon.com/servicequotas/)\.

1. In the navigation pane, choose **AWS services**\.

1. From the **AWS services** list, search for and select **Amazon Elastic Kubernetes Service \(Amazon EKS\)** or **AWS Fargate**\.

   In the **Service quotas** list, you can see the service quota name, applied value \(if it is available\), AWS default quota, and whether the quota value is adjustable\.

1. To view additional information about a service quota, such as the description, choose the quota name\.

1. \(Optional\) To request a quota increase, select the quota that you want to increase, select **Request quota increase**, enter or select the required information, and select **Request**\.

To work more with service quotas using the AWS Management Console see the [Service Quotas User Guide](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)\. To request a quota increase, see [Requesting a Quota Increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*\.

### AWS CLI<a name="sq-cli"></a>

**To view Amazon EKS and Fargate service quotas using the AWS CLI**  
Run the following command to view your Amazon EKS quotas\.

```
aws service-quotas list-aws-default-service-quotas \
    --query 'Quotas[*].{Adjustable:Adjustable,Name:QuotaName,Value:Value,Code:QuotaCode}' \
    --service-code eks \
    --output table
```

Run the following command to view your Fargate quotas\.

```
aws service-quotas list-aws-default-service-quotas \
    --query 'Quotas[*].{Adjustable:Adjustable,Name:QuotaName,Value:Value,Code:QuotaCode}' \
    --service-code fargate \
    --output table
```

**Note**  
The quota returned is the maximum number of Amazon ECS tasks or Amazon EKS pods running concurrently on Fargate in this account in the current Region\.

To work more with service quotas using the AWS CLI, see the [Service Quotas AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\. To request a quota increase, see the [https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html) command in the [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\.