# Deploy Windows nodes on EKS clusters<a name="windows-support"></a>

Before deploying Windows nodes, be aware of the following considerations\.

**Considerations**
+ You can use host networking on Windows nodes using `HostProcess` Pods\. For more information, see [Create a Windows `HostProcess`Pod](https://kubernetes.io/docs/tasks/configure-pod-container/create-hostprocess-pod/) in the Kubernetes documentation\.
+ Amazon EKS clusters must contain one or more Linux or Fargate nodes to run core system Pods that only run on Linux, such as CoreDNS\.
+ The `kubelet` and `kube-proxy` event logs are redirected to the `EKS` Windows Event Log and are set to a 200 MB limit\.
+ You can't use [Security groups for Pods](security-groups-for-pods.md) with Pods running on Windows nodes\.
+ You can't use [custom networking](cni-custom-network.md) with Windows nodes\.
+ You can't use `IPv6` with Windows nodes\.
+ Windows nodes support one elastic network interface per node\. By default, the number of Pods that you can run per Windows node is equal to the number of IP addresses available per elastic network interface for the node's instance type, minus one\. For more information, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide*\.
+ In an Amazon EKS cluster, a single service with a load balancer can support up to 1024 back\-end Pods\. Each Pod has its own unique IP address\. The previous limit of 64 Pods is no longer the case, after [a Windows Server update](https://github.com/microsoft/Windows-Containers/issues/93) starting with [OS Build 17763\.2746](https://support.microsoft.com/en-us/topic/march-22-2022-kb5011551-os-build-17763-2746-preview-690a59cd-059e-40f4-87e8-e9139cc65de4)\.
+ Windows containers aren't supported for Amazon EKS Pods on Fargate\.
+ You can't retrieve logs from the `vpc-resource-controller` Pod\. You previously could when you deployed the controller to the data plane\.
+ There is a cool down period before an `IPv4` address is assigned to a new Pod\. This prevents traffic from flowing to an older Pod with the same `IPv4` address due to stale `kube-proxy` rules\.
+ The source for the controller is managed on GitHub\. To contribute to, or file issues against the controller, visit the [project](https://github.com/aws/amazon-vpc-resource-controller-k8s) on GitHub\.
+ When specifying a custom AMI ID for Windows managed node groups, add `eks:kube-proxy-windows` to your AWS IAM Authenticator configuration map\. For more information, see [Limits and conditions when specifying an AMI ID](launch-templates.md#mng-ami-id-conditions)\.
+ If preserving your available IPv4 addresses is crucial for your subnet, refer to [ EKS Best Practices Guide \- Windows Networking IP Address Management](https://aws.github.io/aws-eks-best-practices/windows/docs/networking/#ip-address-management) for guidance\. <a name="windows-support-prerequisites"></a>

**Prerequisites**
+ An existing cluster\. The cluster must be running one of the Kubernetes versions and platform versions listed in the following table\. Any Kubernetes and platform versions later than those listed are also supported\.    
<a name="windows-support-platform-versions"></a>[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/windows-support.html)
+ Your cluster must have at least one \(we recommend at least two\) Linux node or Fargate Pod to run CoreDNS\. If you enable legacy Windows support, you must use a Linux node \(you can't use a Fargate Pod\) to run CoreDNS\.
+ An existing [Amazon EKS cluster IAM role](cluster_IAM_role.md)\.

## Enable Windows support<a name="enable-windows-support"></a>

**To enable Windows support for your cluster**

1. If you don't have Amazon Linux nodes in your cluster and use security groups for Pods, skip to the next step\. Otherwise, confirm that the `AmazonEKSVPCResourceController` managed policy is attached to your [cluster role](cluster_IAM_role.md)\. Replace `eksClusterRole` with your cluster role name\.

   ```
   aws iam list-attached-role-policies --role-name eksClusterRole
   ```

   An example output is as follows\.

   ```
   {
       "AttachedPolicies": [
           {
               "PolicyName": "AmazonEKSClusterPolicy",
               "PolicyArn": "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
           },
           {
               "PolicyName": "AmazonEKSVPCResourceController",
               "PolicyArn": "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
           }
       ]
   }
   ```

   If the policy is attached, as it is in the previous output, skip the next step\.

1. Attach the **[AmazonEKSVPCResourceController](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSVPCResourceController.html)** managed policy to your [Amazon EKS cluster IAM role](cluster_IAM_role.md)\. Replace `eksClusterRole` with your cluster role name\.

   ```
   aws iam attach-role-policy \
     --role-name eksClusterRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
   ```

1. Create a file named `vpc-resource-controller-configmap.yaml` with the following contents\.

   ```
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: amazon-vpc-cni
     namespace: kube-system
   data:
     enable-windows-ipam: "true"
   ```

1. Apply the `ConfigMap` to your cluster\.

   ```
   kubectl apply -f vpc-resource-controller-configmap.yaml
   ```

1. Verify that your `aws-auth` `ConfigMap` contains a mapping for the instance role of the Windows node to include the `eks:kube-proxy-windows` RBAC permission group\. You can verify by running the following command\. 

   ```
   kubectl get configmap aws-auth -n kube-system -o yaml
   ```

   An example output is as follows\.

   ```
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: aws-auth
     namespace: kube-system
   data:
     mapRoles: |
       - groups:
         - system:bootstrappers
         - system:nodes
         - eks:kube-proxy-windows # This group is required for Windows DNS resolution to work
         rolearn: arn:aws:iam::111122223333:role/eksNodeRole
         username: system:node:{{EC2PrivateDNSName}}
   [...]
   ```

   You should see `eks:kube-proxy-windows` listed under groups\. If the group isn't specified, you need to update your `ConfigMap` or create it to include the required group\. For more information about the `aws-auth` `ConfigMap`, see [Apply the `aws-auth`   `ConfigMap` to your cluster](auth-configmap.md#aws-auth-configmap)\.

## Deploy Windows Pods<a name="windows-support-pod-deployment"></a>

When you deploy Pods to your cluster, you need to specify the operating system that they use if you're running a mixture of node types\. 

For Linux Pods, use the following node selector text in your manifests\.

```
nodeSelector:
        kubernetes.io/os: linux
        kubernetes.io/arch: amd64
```

For Windows Pods, use the following node selector text in your manifests\.

```
nodeSelector:
        kubernetes.io/os: windows
        kubernetes.io/arch: amd64
```

You can deploy a [sample application](sample-deployment.md) to see the node selectors in use\.

## Support higher Pod density on Windows nodes<a name="windows-support-pod-density"></a>

In Amazon EKS, each Pod is allocated an `IPv4` address from your VPC\. Due to this, the number of Pods that you can deploy to a node is constrained by the available IP addresses, even if there are sufficient resources to run more Pods on the node\. Since only one elastic network interface is supported by a Windows node, by default, the maximum number of available IP addresses on a Windows node is equal to:

```
Number of private IPv4 addresses for each interface on the node - 1
```

One IP address is used as the primary IP address of the network interface, so it can't be allocated to Pods\.

You can enable higher Pod density on Windows nodes by enabling IP prefix delegation\. This feature enables you to assign a `/28` `IPv4` prefix to the primary network interface, instead of assigning secondary `IPv4` addresses\. Assigning an IP prefix increases the maximum available `IPv4` addresses on the node to:

```
(Number of private IPv4 addresses assigned to the interface attached to the node - 1) * 16
```

With this significantly larger number of available IP addresses, available IP addresses shouldn't limit your ability to scale the number of Pods on your nodes\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.