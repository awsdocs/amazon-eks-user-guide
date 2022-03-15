# AWS Fargate profile<a name="fargate-profile"></a>

Before you can schedule pods on Fargate in your cluster, you must define at least one Fargate profile that specifies which pods use Fargate when launched\.

The Fargate profile allows an administrator to declare which pods run on Fargate\. This declaration is done through the profile’s selectors\. Each profile can have up to five selectors that contain a namespace and optional labels\. You must define a namespace for every selector\. The label field consists of multiple optional key\-value pairs\. Pods that match a selector \(by matching a namespace for the selector and all of the labels specified in the selector\) are scheduled on Fargate\. If a namespace selector is defined without any labels, Amazon EKS attempts to schedule all pods that run in that namespace onto Fargate using the profile\. If a to\-be\-scheduled pod matches any of the selectors in the Fargate profile, then that pod is scheduled on Fargate\.

If a pod matches multiple Fargate profiles, Amazon EKS picks one of the matches at random\. In this case, you can specify which profile a pod should use by adding the following Kubernetes label to the pod specification: `eks.amazonaws.com/fargate-profile: fargate_profile_name`\. However, the pod must still match a selector in that profile in order to be scheduled onto Fargate\. Kubernetes affinity/anti\-affinity rules aren't taken into consideration and are unnecessary with Amazon EKS Fargate pods\.

When you create a Fargate profile, you must specify a pod execution role for the Amazon EKS components that run on the Fargate infrastructure using the profile\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization so that the `kubelet` that's running on the Fargate infrastructure can register with your Amazon EKS cluster and appear in your cluster as a node\. The pod execution role also provides IAM permissions to the Fargate infrastructure to allow read access to Amazon ECR image repositories\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.

Fargate profiles are immutable\. However, you can create a new updated profile to replace an existing profile and then delete the original after the updated profile has finished creating\.

**Note**  
Any pods that are running using a Fargate profile will be stopped and put into pending when the profile is deleted\.

If any Fargate profiles in a cluster are in the `DELETING` status, you must wait for that Fargate profile to finish deleting before you can create any other profiles in that cluster\.

Amazon EKS and Fargate try to spread pods across each of the subnets defined in the Fargate profile, but you may end up with an uneven spread\. If you must have an even spread \(such as when deploying two replicas without any downtime\), then you need to use two Fargate profiles\. Each profile should have only one subnet\.

## Fargate profile components<a name="fargate-profile-components"></a>

The following components are contained in a Fargate profile\.
+ **Pod execution role** – When your cluster creates pods on AWS Fargate, the `kubelet` that's running on the Fargate infrastructure must make calls to AWS APIs on your behalf\. This is, for example, to pull container images from Amazon ECR\. The Amazon EKS pod execution role provides the IAM permissions to do this\.

  When you create a Fargate profile, you must specify a pod execution role to use with your pods\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization\. This is so that the `kubelet` that's running on the Fargate infrastructure can register with your Amazon EKS cluster and appear in your cluster as a node\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.
+ **Subnets** – The IDs of subnets to launch pods into that use this profile\. At this time, pods that are running on Fargate aren't assigned public IP addresses\. Therefore, only private subnets \(with no direct route to an Internet Gateway\) are accepted for this parameter\.
+ **Selectors** – The selectors to match for pods to use this Fargate profile\. Each selector must have an associated namespace\. Optionally, you can also specify labels for a namespace\. You may specify up to five selectors in a Fargate profile\. A pod only must match one selector to run using the Fargate profile\.
+ **Namespace** – You must specify a namespace for a selector\. The selector only matches pods that are created in this namespace, but you can create multiple selectors to target multiple namespaces\.
+ **Labels** – You can optionally specify Kubernetes labels to match for the selector\. The selector only matches pods that have all of the labels that are specified in the selector\. 

## Creating a Fargate profile<a name="create-fargate-profile"></a>

This topic helps you to create a Fargate profile\. AWS Fargate with Amazon EKS is available in all Amazon EKS Regions except China \(Beijing\), China \(Ningxia\), AWS GovCloud \(US\-East\), and AWS GovCloud \(US\-West\)\.\. You also must have created a pod execution role to use for your Fargate profile\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\. Pods that are running on Fargate are only supported on private subnets \(with [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) access to AWS services, but not a direct route to an Internet Gateway\), so your cluster's VPC must have private subnets available\. You can create a profile with `eksctl` or the AWS Management Console\. Select the tab with the name of the tool that you want to create your Fargate profile with\.

This procedure requires `eksctl` version `0.87.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

------
#### [ eksctl ]

**To create a Fargate profile with `eksctl`**  
Create your Fargate profile with the following `eksctl` command, replacing every `example-value` with your own values\. You're required to specify a namespace\. However, the `--labels` option is not required\.

```
eksctl create fargateprofile \
    --cluster my-cluster \
    --name fargate_profile_name \
    --namespace kubernetes_namespace \
    --labels key=value
```

------
#### [ AWS Management Console ]<a name="create-fargate-profile-console"></a>

**To create a Fargate profile for a cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Choose the **Configuration** tab\.

1. Choose the **Compute** tab\.

1. Under **Fargate Profiles**, choose **Add Fargate Profile**\.

1. On the **Configure Fargate Profile** page, do the following:

   1. For **Name**, enter a unique name for your Fargate profile, such as ***my\-profile***\.

   1. For **Pod execution role**, choose the pod execution role to use with your Fargate profile\. Only the IAM roles with the `eks-fargate-pods.amazonaws.com` service principal are shown\. If you don't see any roles listed, you must create one\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.

   1. Choose the **Subnets** dropdown and deselect any subnet with `Public` in its name\. Only private subnets are supported for pods that are running on Fargate\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags don't propagate to other resources associated with the profile, such as pods\.

   1. Choose **Next**\.

1. On the **Configure pod selection** page, do the following:

   1. For **Namespace**, enter a namespace to match for pods, such as **kube\-system** or **default**\.

   1. \(Optional\) Add Kubernetes labels to the selector\. Specifically add them to the one that the pods in the specified namespace need to match\. For example, you could add the label `infrastructure: fargate` to the selector so that only pods in the specified namespace that also have the `infrastructure: fargate` Kubernetes label match the selector\.

   1. Choose **Next**\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

------

## Deleting a Fargate profile<a name="delete-fargate-profile"></a>

This topic helps you to delete a Fargate profile\. 

When you delete a Fargate profile, any pods that were scheduled onto Fargate with the profile are deleted\. If those pods match another Fargate profile, then they are scheduled on Fargate with that profile\. If they no longer match any Fargate profiles, then they aren't scheduled onto Fargate and may remain as pending\.

Only one Fargate profile in a cluster can be in the `DELETING` status at a time\. Wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster\. 

You can delete a profile with `eksctl`, the AWS Management Console, or the AWS CLI\. Select the tab with the name of the tool that you want to use to delete your profile\.

------
#### [ eksctl ]

**To delete a Fargate profile with `eksctl`**

Use the following command to delete a profile from a cluster\. Replace every `example-value` with your own values\.

```
eksctl delete fargateprofile  --name my-profile --cluster my-cluster
```

------
#### [ AWS Management Console ]

**To delete a Fargate profile from a cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose Amazon EKS **Clusters**\. In the list of clusters, choose the cluster that you want to delete the Fargate profile from\.

1. Choose the **Configuration** tab, and then choose the **Compute** tab\.

1. Choose the Fargate profile to delete, and then choose **Delete**\.

1. On the **Delete Fargate Profile** page, type the name of the profile and then choose **Delete**\.

------
#### [ AWS CLI ]

**To delete a Fargate profile with AWS CLI**

Use the following command to delete a profile from a cluster\. Replace every `example-value` with your own values\.

```
aws eks delete-fargate-profile --fargate-profile-name my-profile --cluster-name my-cluster
```

------