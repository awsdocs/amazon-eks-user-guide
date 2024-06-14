--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Enabling Windows support for your Amazon EKS cluster<a name="windows-support"></a>

Before deploying Windows nodes, be aware of the following considerations\.
+ You can use host networking on Windows nodes using `HostProcess` Pods\. For more information, see [Create a Windows HostProcessPod](https://kubernetes.io/docs/tasks/configure-pod-container/create-hostprocess-pod/) in the Kubernetes documentation\.
+ Amazon EKS clusters must contain one or more Linux or Fargate nodes to run core system Pods that only run on Linux, such as CoreDNS\.
+ The `kubelet` and `kube-proxy` event logs are redirected to the `EKS` Windows Event Log and are set to a 200 MB limit\.
+ You can’t use `IPv6` with Windows nodes\.
+  Windows nodes support one elastic network interface per node\. By default, the number of Pods that you can run per Windows node is equal to the number of IP addresses available per elastic network interface for the node’s instance type, minus one\. For more information, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-WindowsGuide\-using\-eni\-html\-AvailableIpPerENI\}\[IP addresses per network interface per instance type\] in the *Amazon EC2 User Guide for Windows Instances*\.
+ In an Amazon EKS cluster, a single service with a load balancer can support up to 1024 back\-end Pods\. Each Pod has its own unique IP address\. The previous limit of 64 Pods is no longer the case, after [a Windows Server update](https://github.com/microsoft/Windows-Containers/issues/93) starting with [OS Build 17763\.2746](https://support.microsoft.com/en-us/topic/march-22-2022-kb5011551-os-build-17763-2746-preview-690a59cd-059e-40f4-87e8-e9139cc65de4)\.
+ Windows containers aren’t supported for Amazon EKS Pods on Fargate\.
+ You can’t retrieve logs from the `vpc-resource-controller` Pod\. You previously could when you deployed the controller to the data plane\.
+ There is a cool down period before an `IPv4` address is assigned to a new Pod\. This prevents traffic from flowing to an older Pod with the same `IPv4` address due to stale `kube-proxy` rules\.
+ The source for the controller is managed on GitHub\. To contribute to, or file issues against the controller, visit the [project](https://github.com/aws/amazon-vpc-resource-controller-k8s) on GitHub\.

\+<a name="windows-support-platform-versions"></a>
+ Your cluster must have at least one \(we recommend at least two\) Linux node or Fargate Pod to run CoreDNS\. If you enable legacy Windows support, you must use a Linux node \(you can’t use a Fargate Pod\) to run CoreDNS\.

## Enabling Windows support<a name="enable-windows-support"></a>

If you’ve never enabled Windows support on your cluster, skip to the next step\.

\+

```
aws iam list-attached-role-policies --role-name eksClusterRole
```

\+

An example output is as follows\.

\+

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

\+

If the policy is attached, as it is in the previous output, skip the next step\.

\+

```
aws iam attach-role-policy \
  --role-name eksClusterRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
```

1. Create a file named ` vpc-resource-controller-configmap.yaml ` with the following contents\.

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

1. Verify that your `aws-auth`ConfigMap contains a mapping for the instance role of the Windows node to include the `eks:kube-proxy-windows` RBAC permission group\. You can verify by running the following command\.

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
         rolearn: arn:aws:iam::`111122223333`:role/`eksNodeRole`username: system:node:{{EC2PrivateDNSName}}
   [...]
   ```

## Removing legacy Windows support from your data plane<a name="remove-windows-support-data-plane"></a>

1. Uninstall the `vpc-resource-controller` with the following command\. Use this command regardless of which tool you originally installed it with\. Replace ` region-code ` \(only the instance of that text after `/manifests/`\) with the AWS Region that your cluster is in\.

   ```
   kubectl delete -f https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Uninstall the `vpc-admission-webhook` using the instructions for the tool that you installed it with\.  
eksctl  
   + Run the following commands\.

     ```
     kubectl delete deployment -n kube-system vpc-admission-webhook
     kubectl delete service -n kube-system vpc-admission-webhook
     kubectl delete mutatingwebhookconfigurations.admissionregistration.k8s.io vpc-admission-webhook-cfg
     ```  
kubectl on macOS or Windows   
   + Run the following command\. Replace ` region-code ` \(only the instance of that text after `/manifests/`\) with the AWS Region that your cluster is in\.

     ```
     kubectl delete -f https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml
     ```

## Disabling Windows support<a name="windows-support-disabling"></a>

\+

\+

```
aws iam detach-role-policy \
    --role-name eksClusterRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
```

1. Disable Windows IPAM in the `amazon-vpc-cni` ConfigMap\.

   ```
   kubectl patch configmap/amazon-vpc-cni \
                       -n kube-system \
                       --type merge \
                       -p '{"data":{"enable-windows-ipam":"false"}}'
   ```

## Deploying Pods<a name="windows-support-pod-deployment"></a>

When you deploy Pods to your cluster, you need to specify the operating system that they use if you’re running a mixture of node types\.

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

## Enabling legacy Windows support<a name="legacy-windows-support"></a>

You can use `eksctl`, a Windows client, or a macOS or Linux client to enable legacy Windows support for your cluster\.

eksctl  
\.Prerequisite This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command\.

```
eksctl version
```

For more information about installing or upgrading `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

1. Enable Windows support for your Amazon EKS cluster with the following `eksctl` command\. Replace ` my-cluster ` with the name of your cluster\. This command deploys the VPC resource controller and VPC admission controller webhook that are required on Amazon EKS clusters to run Windows workloads\.

   ```
   eksctl utils install-vpc-controllers --cluster my-cluster --approve
   ```  
 Windows   
In the following steps, replace ` region-code ` with the AWS Region that your cluster resides in\.

1. Deploy the VPC resource controller to your cluster\.

   ```
   kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Deploy the VPC admission controller webhook to your cluster\.

   1. Download the required scripts and deployment files\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml;
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/Setup-VPCAdmissionWebhook.ps1;
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.ps1;
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-patch-ca-bundle.ps1;
      ```

   1. Install [OpenSSL](https://wiki.openssl.org/index.php/Binaries) and [jq](https://stedolan.github.io/jq/download/)\.

   1. Set up and deploy the VPC admission webhook\.

      ```
      ./Setup-VPCAdmissionWebhook.ps1 -DeploymentTemplate ".\vpc-admission-webhook-deployment.yaml"
      ```

1. Determine if your cluster has the required cluster role binding\.

   ```
   kubectl get clusterrolebinding eks:kube-proxy-windows
   ```

   If output similar to the following example output is returned, then the cluster has the necessary role binding\.

   ```
   NAME                      AGE
   eks:kube-proxy-windows    10d
   ```

   If the output includes `Error from server (NotFound)`, then the cluster does not have the necessary cluster role binding\. Add the binding by creating a file named ` eks-kube-proxy-windows-crb.yaml ` with the following content\.

   ```
   kind: ClusterRoleBinding
   apiVersion: rbac.authorization.k8s.io/v1beta1
   metadata:
     name: eks:kube-proxy-windows
     labels:
       k8s-app: kube-proxy
       eks.amazonaws.com/component: kube-proxy
   subjects:
     - kind: Group
       name: "eks:kube-proxy-windows"
   roleRef:
     kind: ClusterRole
     name: system:node-proxier
     apiGroup: rbac.authorization.k8s.io
   ```

   Apply the configuration to the cluster\.

   ```
   kubectl apply -f eks-kube-proxy-windows-crb.yaml
   ```  
macOS and Linux   
This procedure requires that the `openssl` library and `jq` JSON processor are installed on your client system\.

In the following steps, replace ` region-code ` with the AWS Region that your cluster resides in\.

1. Deploy the VPC resource controller to your cluster\.

   ```
   kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Create the VPC admission controller webhook manifest for your cluster\.

   1. Download the required scripts and deployment files\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.sh
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-patch-ca-bundle.sh
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml
      ```

   1. Add permissions to the shell scripts so that they can be run\.

      ```
      chmod +x webhook-create-signed-cert.sh webhook-patch-ca-bundle.sh
      ```

   1. Create a secret for secure communication\.

      ```
      ./webhook-create-signed-cert.sh
      ```

   1. Verify the secret\.

      ```
      kubectl get secret -n kube-system vpc-admission-webhook-certs
      ```

   1. Configure the webhook and create a deployment file\.

      ```
      cat ./vpc-admission-webhook-deployment.yaml | ./webhook-patch-ca-bundle.sh > vpc-admission-webhook.yaml
      ```

1. Deploy the VPC admission webhook\.

   ```
   kubectl apply -f vpc-admission-webhook.yaml
   ```

1. Determine if your cluster has the required cluster role binding\.

   ```
   kubectl get clusterrolebinding eks:kube-proxy-windows
   ```

   If output similar to the following example output is returned, then the cluster has the necessary role binding\.

   ```
   NAME                     ROLE                              AGE
   eks:kube-proxy-windows   ClusterRole/system:node-proxier   19h
   ```

   If the output includes `Error from server (NotFound)`, then the cluster does not have the necessary cluster role binding\. Add the binding by creating a file named ` eks-kube-proxy-windows-crb.yaml ` with the following content\.

   ```
   kind: ClusterRoleBinding
   apiVersion: rbac.authorization.k8s.io/v1beta1
   metadata:
     name: eks:kube-proxy-windows
     labels:
       k8s-app: kube-proxy
       eks.amazonaws.com/component: kube-proxy
   subjects:
     - kind: Group
       name: "eks:kube-proxy-windows"
   roleRef:
     kind: ClusterRole
     name: system:node-proxier
     apiGroup: rbac.authorization.k8s.io
   ```

   Apply the configuration to the cluster\.

   ```
   kubectl apply -f eks-kube-proxy-windows-crb.yaml
   ```

### Renewing the VPC admission webhook certificate<a name="windows-certificate"></a>

The certificate used by the VPC admission webhook expires one year after issue\. To avoid down time, it’s important that you renew the certificate before it expires\. You can check the expiration date of your current certificate with the following command\.

```
kubectl get secret \
    -n kube-system \
    vpc-admission-webhook-certs -o json | \
    jq -r '.data."cert.pem"' | \
    base64 -decode | \
    openssl x509 \
    -noout \
    -enddate | \
    cut -d= -f2
```

An example output is as follows\.

```
May 28 14:23:00 2022 GMT
```

You can renew the certificate using `eksctl` or a Windows or Linux/macOS computer\. Follow the instructions for the tool you originally used to install the VPC admission webhook\. For example, if you originally installed the VPC admission webhook using `eksctl`, then you should renew the certificate using the instructions on the `eksctl` tab\.

eksctl  

1. Reinstall the certificate\. Replace ` my-cluster ` with the name of your cluster\.

   ```
   eksctl utils install-vpc-controllers -cluster my-cluster -approve
   ```

1. Verify that you receive the following output\.

   ```
   2021/05/28 05:24:59 [INFO] generate received request
   2021/05/28 05:24:59 [INFO] received CSR
   2021/05/28 05:24:59 [INFO] generating key: rsa-2048
   2021/05/28 05:24:59 [INFO] encoded CSR
   ```

1. Restart the webhook deployment\.

   ```
   kubectl rollout restart deployment -n kube-system vpc-admission-webhook
   ```

1. If the certificate that you renewed was expired, and you have Windows Pods stuck in the `Container creating` state, then you must delete and redeploy those Pods\.

 Windows   

1. Get the script to generate new certificate\.

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.ps1;
   ```

1. Prepare parameter for the script\.

   ```
   ./webhook-create-signed-cert.ps1 -ServiceName vpc-admission-webhook-svc -SecretName vpc-admission-webhook-certs -Namespace kube-system
   ```

1. Restart the webhook deployment\.

   ```
   kubectl rollout restart deployment -n kube-system vpc-admission-webhook-deployment
   ```

1. If the certificate that you renewed was expired, and you have Windows Pods stuck in the `Container creating` state, then you must delete and redeploy those Pods\.

 Linux and macOS  
\* \.Prerequisite You must have OpenSSL and `jq` installed on your computer\.  

1. Get the script to generate new certificate\.

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.sh
   ```

1. Change the permissions\.

   ```
   chmod +x webhook-create-signed-cert.sh
   ```

1. Run the script\.

   ```
   ./webhook-create-signed-cert.sh
   ```

1. Restart the webhook\.

   ```
   kubectl rollout restart deployment -n kube-system vpc-admission-webhook-deployment
   ```

1. If the certificate that you renewed was expired, and you have Windows Pods stuck in the `Container creating` state, then you must delete and redeploy those Pods\.

## Supporting higher Pod density on Windows nodes<a name="windows-support-pod-density"></a>

In Amazon EKS, each Pod is allocated an `IPv4` address from your VPC\. Due to this, the number of Pods that you can deploy to a node is constrained by the available IP addresses, even if there are sufficient resources to run more Pods on the node\. Since only one elastic network interface is supported by a Windows node, by default, the maximum number of available IP addresses on a Windows node is equal to:

```
Number of privateaddresses for each interface on the node - 1
```

One IP address is used as the primary IP address of the network interface, so it can’t be allocated to Pods\.

You can enable higher Pod density on Windows nodes by enabling IP prefix delegation\. This feature enables you to assign a `/28`IPv4 prefix to the primary network interface, instead of assigning secondary `IPv4` addresses\. Assigning an IP prefix increases the maximum available `IPv4` addresses on the node to:

```
(Number of privateaddresses assigned to the interface attached to the node - 1) * 16
```