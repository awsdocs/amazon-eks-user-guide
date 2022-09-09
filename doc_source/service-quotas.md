# Amazon EKS service quotas<a name="service-quotas"></a>

Amazon EKS has integrated with Service Quotas, an AWS service that you can use to view and manage your quotas from a central location\. For more information, see [What Is Service Quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) in the *Service Quotas User Guide*\. With Service Quotas integration, you can quickly look up the value of your Amazon EKS and AWS Fargate service quotas using the AWS Management Console and AWS CLI\.

------
#### [ AWS Management Console ]<a name="service-quotas-console"></a>

**To view Amazon EKS and Fargate service quotas using the AWS Management Console**

1. Open the Service Quotas console at [https://console\.aws\.amazon\.com/servicequotas/](https://console.aws.amazon.com/servicequotas/)\.

1. In the left navigation pane, choose **AWS services**\.

1. From the **AWS services** list, search for and select **Amazon Elastic Kubernetes Service \(Amazon EKS\)** or **AWS Fargate**\.

   In the **Service quotas** list, you can see the service quota name, applied value \(if it's available\), AWS default quota, and whether the quota value is adjustable\.

1. To view additional information about a service quota, such as the description, choose the quota name\.

1. \(Optional\) To request a quota increase, select the quota that you want to increase, select **Request quota increase**, enter or select the required information, and select **Request**\.

To work more with service quotas using the AWS Management Console, see the [Service Quotas User Guide](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)\. To request a quota increase, see [Requesting a Quota Increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*\.

------
#### [ AWS CLI ]
<a name="service-quotas-cli"></a>
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
The quota returned is the number of Amazon ECS tasks or Amazon EKS pods that can run concurrently on Fargate in this account in the current AWS Region\.

To work more with service quotas using the AWS CLI, see the [Service Quotas AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\. To request a quota increase, see the [https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html) command in the [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html#cli-aws-service-quotas)\.

------

## Service quotas<a name="sq-text"></a>

[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/service-quotas.html)

**Note**  
The default values are the initial quotas set by AWS\. These default values are separate from the actual applied quota values and maximum possible service quotas\. For more information, see [Terminology in Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html#intro_getting-started) in the *Service Quotas User Guide*\.

These service quotas are listed under **Amazon Elastic Kubernetes Service \(Amazon EKS\)** in the Service Quotas console\. To request a quota increase for values that are shown as adjustable, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-increase.html) in the *Service Quotas User Guide*\.

## AWS Fargate service quotas<a name="service-quotas-eks-fargate"></a>

This section describes AWS Fargate service quotas for Amazon EKS\. You can configure alarms that alert you when your usage approaches a service quota\. For more information, see [Creating a CloudWatch alarm to monitor Fargate resource usage metrics](monitoring-fargate-usage.md#service-quota-alarm)\.

AWS Fargate is transitioning from pod based quotas to vCPU based quotas\. The following are the important dates related to the new vCPU based quotas\.
+ September 8, 2022 – You can now opt in to using the new vCPU based quotas ahead of automatic migration\. By opting in, your account is controlled by vCPU based quotas rather than the previous pod based quotas\. Pod based quotas remain the default for accounts that don't opt in\.
**Note**  
To use the vCPU based quotas with Amazon EKS before October 3, 2022, you must opt in\.  
To opt in, use the AWS Support Center Console to create a **Service limit increase** case\. Choose **Fargate** for **Limit type** and **Fargate account vCPU limit opt\-in** for **Limit**\. For more information, see [Creating a support case](https://docs.aws.amazon.com/awssupport/latest/user/case-management.html#creating-a-support-case) in the *AWS Support User Guide*\.
+ October 3, 2022 through October 21, 2022 – All new and existing accounts are switched to the vCPU based quotas in a phased manner\.
**Note**  
To continue using the pod based quotas, you must opt out\.  
To opt out, use the AWS Support Center Console to create a **Service limit increase** case\. Choose **Fargate** for **Limit type** and **Fargate account opt\-out of vCPU limit** for **Limit**\. For more information, see [Creating a support case](https://docs.aws.amazon.com/awssupport/latest/user/case-management.html#creating-a-support-case) in the *AWS Support User Guide*\.
+ October 31, 2022 – The last day that you can remain opted out of the vCPU based quotas\.
+ November 1, 2022 through November 15, 2022 – The opt\-out option ends and all accounts are migrated to the vCPU based quotas\. The pod based quotas are no longer available\.

The following table lists the new vCPU based quota followed by the existing pod based quota\. These service quotas are among those listed under the **AWS Fargate** service in the Service Quotas console\. The following table only describes the quotas that also applicable to Amazon EKS\.

You can confirm which quota type is active by looking at the Service Quotas console\. If the vCPU quota is in effect, the Fargate On\-Demand Pod count based quotas show `0` for the **Applied quota value**\. Any other value indicates that the pod count quota is in effect\.

New AWS accounts might have lower initial quotas that can increase over time\. Fargate constantly monitors the account usage within each AWS Region, and then automatically increases the quotas based on the usage\. You can also request a quota increase for values that are shown as adjustable\. For more information, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-increase.html) in the *Service Quotas User Guide*\.


| Name | Default | Adjustable | Description | 
| --- | --- | --- | --- | 
|  Fargate On\-Demand vCPU resource count  | 6 | [Yes](https://console.aws.amazon.com/servicequotas/home/services/fargate/quotas) |  The number of Fargate vCPUs that can run concurrently as Fargate On\-Demand in this account in the current Region\.  | 
| Fargate On\-Demand resource count | 2 |  [Yes](https://console.aws.amazon.com/servicequotas/home/services/fargate/quotas/L-790AF391)  | The number of Amazon ECS tasks and Amazon EKS pods that can run concurrently on Fargate in this account in the current Region\. | 

**Note**  
The default values are the initial quotas set by AWS\. These default values are separate from the actual applied quota values and maximum possible service quotas\. For more information, see [Terminology in Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html#intro_getting-started) in the *Service Quotas User Guide*\.

**Note**  
Fargate additionally enforces Amazon ECS tasks and Amazon EKS pods launch rate quotas\. For more information, see [Fargate throttling limits](https://docs.aws.amazon.com/AmazonECS/latest/userguide/throttling.html) in the *Amazon Elastic Container Service User Guide for AWS Fargate*\.