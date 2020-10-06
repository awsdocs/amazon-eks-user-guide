# AWS Fargate profile<a name="fargate-profile"></a>

Before you can schedule pods on Fargate in your cluster, you must define at least one Fargate profile that specifies which pods should use Fargate when they are launched\.

The Fargate profile allows an administrator to declare which pods run on Fargate\. This declaration is done through the profile’s selectors\. Each profile can have up to five selectors that contain a namespace and optional labels\. You must define a namespace for every selector\. The label field consists of multiple optional key\-value pairs\. Pods that match a selector \(by matching a namespace for the selector and all of the labels specified in the selector\) are scheduled on Fargate\. If a namespace selector is defined without any labels, Amazon EKS will attempt to schedule all pods that run in that namespace onto Fargate using the profile\. If a to\-be\-scheduled pod matches any of the selectors in the Fargate profile, then that pod is scheduled on Fargate\.

If a pod matches multiple Fargate profiles, Amazon EKS picks one of the matches at random\. In this case, you can specify which profile a pod should use by adding the following Kubernetes label to the pod specification: `eks.amazonaws.com/fargate-profile: <profile_name>`\. However, the pod must still match a selector in that profile in order to be scheduled onto Fargate\.

When you create a Fargate profile, you must specify a pod execution role for the pods that run on Fargate using the profile\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization so that the `kubelet` that is running on the Fargate infrastructure can register with your Amazon EKS cluster and appear in your cluster as a node\. The pod execution role also provides IAM permissions to the Fargate infrastructure to allow read access to Amazon ECR image repositories\. For more information, see [Pod execution role](pod-execution-role.md)\.

Fargate profiles are immutable\. However, you can create a new updated profile to replace an existing profile and then delete the original after the updated profile has finished creating\.

**Note**  
Any pods that are running using a Fargate profile will be stopped and put into pending when the profile is deleted\.

If any Fargate profiles in a cluster are in the `DELETING` status, you must wait for that Fargate profile to finish deleting before you can create any other profiles in that cluster\.

## Fargate profile components<a name="fargate-profile-components"></a>

The following components are contained in a Fargate profile\.

```
{
    "fargateProfileName": "",
    "clusterName": "",
    "podExecutionRoleArn": "",
    "subnets": [
        ""
    ],
    "selectors": [
        {
            "namespace": "",
            "labels": {
                "KeyName": ""
            }
        }
    ],
    "clientRequestToken": "",
    "tags": {
        "KeyName": ""
    }
}
```

**Pod execution role**  
When your cluster creates pods on AWS Fargate, the pod needs to make calls to AWS APIs on your behalf, for example, to pull container images from Amazon ECR\. The Amazon EKS pod execution role provides the IAM permissions to do this\.  
When you create a Fargate profile, you must specify a pod execution role to use with your pods\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization, so that the `kubelet` that is running on the Fargate infrastructure can register with your Amazon EKS cluster and appear in your cluster as a node\. For more information, see [Pod execution role](pod-execution-role.md)\.

**Subnets**  
The IDs of subnets to launch pods into that use this profile\. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets \(with no direct route to an Internet Gateway\) are accepted for this parameter\.

**Selectors**  
The selectors to match for pods to use this Fargate profile\. Each selector must have an associated namespace\. Optionally, you can also specify labels for a namespace\. You may specify up to five selectors in a Fargate profile\. A pod only needs to match one selector to run using the Fargate profile\.    
**Namespace**  
You must specify a namespace for a selector\. The selector only matches pods that are created in this namespace, but you can create multiple selectors to target multiple namespaces\.  
**Labels**  
You can optionally specify Kubernetes labels to match for the selector\. The selector only matches pods that have all of the labels that are specified in the selector\. 

## Creating a Fargate profile<a name="create-fargate-profile"></a>

This topic helps you to create a Fargate profile\. Your cluster must support Fargate \(beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.5`\)\. You also must have created a pod execution role to use for your Fargate profile\. For more information, see [Pod execution role](pod-execution-role.md)\. Pods running on Fargate are only supported on private subnets \(with [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) access to AWS services, but not a direct route to an Internet Gateway\), so your cluster's VPC must have private subnets available\. You can create a profile with [`eksctl`](#create-fargate-profile-eksctl2) or the [AWS Management Console](#create-fargate-profile-console2)\.<a name="create-fargate-profile-eksctl2"></a>

**To create a Fargate profile for a cluster with `eksctl`**

This procedure requires `eksctl` version `0.29.1` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
+ Create your Fargate profile with the following `eksctl` command, replacing the <variable text> with your own values\. You must specify a namespace, but the labels option is not required\.

  ```
  eksctl create fargateprofile --cluster <cluster_name> --name <fargate_profile_name> --namespace <kubernetes_namespace> --labels <key=value>
  ```<a name="create-fargate-profile-console2"></a>

**To create a Fargate profile for a cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, enter the following information and choose **Next**\.

   1. For **Name**, enter a unique name for your Fargate profile\.

   1. For **Pod execution role**, choose the pod execution role to use with your Fargate profile\. Only IAM roles with the `eks-fargate-pods.amazonaws.com` service principal are shown\. If you do not see any roles listed here, you must create one\. For more information, see [Pod execution role](pod-execution-role.md)\.

   1. For **Subnets**, choose the subnets to use for your pods\. By default, all subnets in your cluster's VPC are selected\. Only private subnets are supported for pods running on Fargate; you must deselect any public subnets\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags do not propagate to other resources associated with the profile, such as its pods\.

1. On the **Configure pods selection** page, enter the following information and choose **Next**\.

   1. For **Namespace**, enter a namespace to match for pods, such as `kube-system` or `default`\.

   1. \(Optional\) Add Kubernetes labels to the selector that pods in the specified namespace must have to match the selector\. For example, you could add the label `infrastructure: fargate` to the selector so that only pods in the specified namespace that also have the `infrastructure: fargate` Kubernetes label match the selector\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

## Deleting a Fargate profile<a name="delete-fargate-profile"></a>

This topic helps you to delete a Fargate profile\. 

When you delete a Fargate profile, any pods that were scheduled onto Fargate with the profile are deleted\. If those pods match another Fargate profile, then they are scheduled on Fargate with that profile\. If they no longer match any Fargate profiles, then they are not scheduled onto Fargate and may remain as pending\.

Only one Fargate profile in a cluster can be in the `DELETING` status at a time\. You must wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster\.

**To delete a Fargate profile from a cluster**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that you want to delete the Fargate profile from\.

1. Choose the Fargate profile to delete and then **Delete**\.

1. On the **Delete <cluster\_name>** page, type the name of the cluster and choose **Confirm** to delete\.