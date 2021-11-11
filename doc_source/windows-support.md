# Windows support<a name="windows-support"></a>

Before deploying Windows nodes, be aware of the following considerations\.

**Considerations**
+ Amazon EC2 instance types C3, C4, D2, I2, M4 \(excluding m4\.16xlarge\), and R3 instances are not supported for Windows workloads\.
+ Host networking mode is not supported for Windows workloads\. 
+ Amazon EKS clusters must contain one or more Linux or Fargate nodes to run core system pods that only run on Linux, such as CoreDNS\.
+ The `kubelet` and `kube-proxy` event logs are redirected to the `EKS` Windows Event Log and are set to a 200 MB limit\.
+ You can't use [Security groups for pods](security-groups-for-pods.md) with pods running on Windows nodes\.
+ You can't use [custom networking](cni-custom-network.md) with Windows nodes\.
+ You can't use [IP prefixes](cni-increase-ip-addresses.md) with Windows nodes\.
+ Windows nodes support one elastic network interface per node\. The number of pods that you can run per Windows node is equal to the number of IP addresses available per elastic network interface for the node's instance type, minus one\. For more information, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Windows Instances*\.
+ In an Amazon EKS cluster, a single service with a load balancer can support up to 64 backend pods\. Each pod has its own unique IP address\. This is a limitation of the Windows operating system on the Amazon EC2 nodes\.
+ You can't deploy Windows managed or Fargate nodes\. You can only create self\-managed Windows nodes\. For more information, see [Launching self\-managed Windows nodes](launch-windows-workers.md)\.
+ You can't retrieve logs from the `vpc-resource-controller` Pod\. You previously could when you deployed the controller to the data plane\.
+ There is a cool down period before an IPv4 address is assigned to a new Pod\. This prevents traffic from flowing to an older Pod with the same IPv4 address due to stale `kube-proxy` rules\.
+ The source for the controller is managed on GitHub\. To contribute to, or file issues against the controller, vist the [project](https://github.com/aws/amazon-vpc-resource-controller-k8s) on GitHub\. <a name="windows-support-prerequisites"></a>

**Prerequisites**
+ An existing cluster\. The cluster must be running one of the Kubernetes versions and platform versions listed in the following table\. Any Kubernetes and platform versions later than those listed are also supported\.    
<a name="windows-support-platform-versions"></a>[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/windows-support.html)

  Your cluster must have at least one \(we recommend at least two\) Linux node or Fargate pod to run CoreDNS\.
+ An existing [Amazon EKS cluster IAM role](service_IAM_role.md)\.

## Enabling Windows support<a name="enable-windows-support"></a>

**To enable Windows support for your cluster**

1. If you've never enabled Windows support on your cluster, skip to the next step\. If you enabled Windows support on a cluster that is earlier than a Kubernetes or platform version listed in the [Prerequisites](#windows-support-platform-versions), then you must first [remove the `vpc-resource-controller` and `vpc-admission-webhook` from your data plane](#remove-windows-support-data-plane)\. They're deprecated and no longer needed\.

1. If you don't have Amazon Linux nodes in your cluster and use security groups for pods, skip to the next step\. Otherwise, confirm that the `AmazonEKSVPCResourceController` managed policy is attached to your [cluster role](service_IAM_role.md)\. Replace *eksClusterRole* with your cluster role name\.

   ```
   aws iam list-attached-role-policies --role-name eksClusterRole
   ```

   Output

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

1. Attach the **[AmazonEKSVPCResourceController](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController$jsonEditor)** managed policy to your [Amazon EKS cluster IAM role](service_IAM_role.md)\. Replace *eksClusterRole* with your cluster role name and *111122223333* with your account ID\.

   ```
   aws iam attach-role-policy \
     --role-name eksClusterRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
   ```

1. Create a file named *vpc\-resource\-controller\-configmap\.yaml* with the following contents\.

   ```
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: amazon-vpc-cni
     namespace: kube-system
   data:
     enable-windows-ipam: "true"
   ```

1. Apply the ConfigMap to your cluster\.

   ```
   kubectl apply -f vpc-resource-controller-configmap.yaml
   ```

## Remove Windows support from your data plane<a name="remove-windows-support-data-plane"></a>

If you enabled Windows support on a cluster that is earlier than a Kubernetes or platform version listed in the [Prerequisites](#windows-support-platform-versions), then you must first remove the `vpc-resource-controller` and `vpc-admission-webhook` from your data plane\. They're deprecated and no longer needed because the functionality that they provided is now enabled on the control plane\.

1. Uninstall the `vpc-resource-controller` with the following command\. Use this command regardless of which tool you originally installed it with\. Replace *us\-west\-2* \(only the instance of that text after `/manifests/`\) with the Region that your cluster is in\.

   ```
   kubectl delete -f https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/us-west-2/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Uninstall the `vpc-admission-webhook` using the instructions for the tool that you installed it with\.

------
#### [ eksctl ]

   Run the following commands\.

   ```
   kubectl delete deployment -n kube-system vpc-admission-webhook
   kubectl delete service -n kube-system vpc-admission-webhook
   kubectl delete mutatingwebhookconfigurations.admissionregistration.k8s.io vpc-admission-webhook-cfg
   ```

------
#### [ kubectl on macOS or Windows ]

   Run the following command\. Replace *us\-west\-2* \(only the instance of that text after `/manifests/`\) with the Region that your cluster is in\.

   ```
   kubectl delete -f https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/us-west-2/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml
   ```

------

1. [Enable Windows support](#enable-windows-support) for your cluster on the control plane\.

## Disabling Windows support<a name="windows-support-disabling"></a>

**To disable Windows support on your cluster**

1. If your cluster contains Amazon Linux nodes and you use [security groups for pods](security-groups-for-pods.md) with them, then skip this step\.

   Remove the `AmazonVPCResourceController` managed IAM policy from your [cluster role](service_IAM_role.md)\. Replace *eksClusterRole* with the name of your cluster role and *111122223333* with your account ID\.

   ```
   aws iam detach-role-policy \
       --role-name eksClusterRole \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
   ```

1. Disable Windows IPAM in the `amazon-vpc-cni` ConfigMap\.

   ```
   kubectl patch configmap/amazon-vpc-cni \-n kube-system \--type merge \-p '{"data":{"enable-windows-ipam":"false"}}'
   ```

## Deploying Pods<a name="windows-support-pod-deployment"></a>

When you deploy Pods to your cluster, you need to specify the operating system that they use if you're running a mixture of node types\. 

For Linux pods, use the following node selector text in your manifests\.

```
nodeSelector:
        kubernetes.io/os: linux
        kubernetes.io/arch: amd64
```

For Windows pods, use the following node selector text in your manifests\.

```
nodeSelector:
        kubernetes.io/os: windows
        kubernetes.io/arch: amd64
```

You can deploy a [sample application](sample-deployment.md) to see the node selectors in use\.