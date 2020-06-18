# Windows support<a name="windows-support"></a>

This topic describes how to add Windows support to Amazon EKS clusters\.

## Considerations<a name="considerations"></a>

Before deploying Windows worker nodes, be aware of the following considerations\.
+ Windows workloads are supported with Amazon EKS clusters running Kubernetes version 1\.14 or later\.
+ Amazon EC2 instance types C3, C4, D2, I2, M4 \(excluding m4\.16xlarge\), and R3 instances are not supported for Windows workloads\.
+ Host networking mode is not supported for Windows workloads\. 
+ Amazon EKS clusters must contain one or more Linux worker nodes to run core system pods that only run on Linux, such as `coredns` and the VPC resource controller\.
+ The `kubelet` and `kube-proxy` event logs are redirected to the `EKS` Windows Event Log and are set to a 200 MB limit\.
+ Windows worker nodes support one elastic network interface per node\. The number of pods that you can run per Windows worker node is equal to the number of IP addresses available per elastic network interface for the node's instance type, minus one\. For more information, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.
+ Group Managed Service Accounts \(GMSA\) for Windows pods and containers is a Kubernetes 1\.14 alpha feature that is not supported by Amazon EKS\. You can follow the instructions in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-gmsa/) to enable and test this alpha feature on your clusters\.

## Enabling Windows support<a name="enable-windows-support"></a>

The following steps help you to enable Windows support for your Amazon EKS cluster\. Choose the tab below to use  standard tools on your client operating system\.

------
#### [ eksctl ]

**To enable Windows support for your cluster with `eksctl`**

This procedure only works for clusters that were created with `eksctl` and assumes that your `eksctl` version is `0.21.0` or later\. You can check your version with the following command\.

```
eksctl version
```

 For more information about installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. Enable Windows support for your Amazon EKS cluster with the following `eksctl` command\. This command deploys the VPC resource controller and VPC admission controller webhook that are required on Amazon EKS clusters to run Windows workloads\.

   ```
   eksctl utils install-vpc-controllers --cluster cluster_name --approve
   ```

1. After you have enabled Windows support, you can launch a Windows node group into your cluster\. For more information, see [Launching Amazon EKS Windows worker nodes](launch-windows-workers.md)\.

After you add Windows support to your cluster, you must specify node selectors on your applications so that the pods land on a node with the appropriate operating system\. For Linux pods, use the following node selector text in your manifests\.

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

------
#### [ Windows ]

**To enable Windows support for your cluster with a Windows client**

In the following steps, replace the *region\-code* with the Region that your cluster resides in\.

1. Deploy the VPC resource controller to your cluster\.

   ```
   kubectl apply -f https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Deploy the VPC admission controller webhook to your cluster\.

   1. Download the required scripts and deployment files\.

      ```
      curl -o vpc-admission-webhook-deployment.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml;
      curl -o Setup-VPCAdmissionWebhook.ps1 https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/Setup-VPCAdmissionWebhook.ps1;
      curl -o webhook-create-signed-cert.ps1 https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.ps1;
      curl -o webhook-patch-ca-bundle.ps1 https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/webhook-patch-ca-bundle.ps1;
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

   If the output includes `Error from server (NotFound)`, then the cluster does not have the necessary cluster role binding\. Add the binding by creating a file named `eks-kube-proxy-windows-crb.yaml` with the following content\.

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

1. After you have enabled Windows support, you can launch a Windows node group into your cluster\. For more information, see [Launching Amazon EKS Windows worker nodes](launch-windows-workers.md)\.

After you add Windows support to your cluster, you must specify node selectors on your applications so that the pods land on a node with the appropriate operating system\. For Linux pods, use the following node selector text in your manifests\.

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

------
#### [ macOS and Linux ]

**To enable Windows support for your cluster with a macOS or Linux client**

This procedure requires that the `openssl` library and `jq` JSON processor are installed on your client system\. 

In the following steps, replace *region\-code* with the Region that your cluster resides in\.

1. Deploy the VPC resource controller to your cluster\.

   ```
   kubectl apply -f https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-resource-controller/latest/vpc-resource-controller.yaml
   ```

1. Create the VPC admission controller webhook manifest for your cluster\.

   1. Download the required scripts and deployment files\.

      ```
      curl -o webhook-create-signed-cert.sh https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/webhook-create-signed-cert.sh
      curl -o webhook-patch-ca-bundle.sh https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/webhook-patch-ca-bundle.sh
      curl -o vpc-admission-webhook-deployment.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/manifests/region-code/vpc-admission-webhook/latest/vpc-admission-webhook-deployment.yaml
      ```

   1. Add permissions to the shell scripts so that they can be executed\.

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
   NAME                      AGE
   eks:kube-proxy-windows    10d
   ```

   If the output includes `Error from server (NotFound)`, then the cluster does not have the necessary cluster role binding\. Add the binding by creating a file named `eks-kube-proxy-windows-crb.yaml` with the following content\.

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

1. After you have enabled Windows support, you can launch a Windows node group into your cluster\. For more information, see [Launching Amazon EKS Windows worker nodes](launch-windows-workers.md)\.

After you add Windows support to your cluster, you must specify node selectors on your applications so that the pods land on a node with the appropriate operating system\. For Linux pods, use the following node selector text in your manifests\.

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

------

## Deploy a Windows sample application<a name="windows-sample-application"></a>

**To deploy a Windows sample application**

1. Create a file named `windows-server-iis.yaml` with the following content\.

   ```
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: windows-server-iis
   spec:
     selector:
       matchLabels:
         app: windows-server-iis
         tier: backend
         track: stable
     replicas: 1
     template:
       metadata:
         labels:
           app: windows-server-iis
           tier: backend
           track: stable
       spec:
         containers:
         - name: windows-server-iis
           image: mcr.microsoft.com/windows/servercore:1809
           ports:
           - name: http
             containerPort: 80
           imagePullPolicy: IfNotPresent
           command:
           - powershell.exe
           - -command
           - "Add-WindowsFeature Web-Server; Invoke-WebRequest -UseBasicParsing -Uri 'https://dotnetbinaries.blob.core.windows.net/servicemonitor/2.0.1.6/ServiceMonitor.exe' -OutFile 'C:\\ServiceMonitor.exe'; echo '<html><body><br/><br/><marquee><H1>Hello EKS!!!<H1><marquee></body><html>' > C:\\inetpub\\wwwroot\\default.html; C:\\ServiceMonitor.exe 'w3svc'; "
         nodeSelector:
           kubernetes.io/os: windows
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: windows-server-iis-service
     namespace: default
   spec:
     ports:
     - port: 80
       protocol: TCP
       targetPort: 80
     selector:
       app: windows-server-iis
       tier: backend
       track: stable
     sessionAffinity: None
     type: LoadBalancer
   ```

1. Deploy the application to the cluster\.

   ```
   kubectl apply -f windows-server-iis.yaml
   ```

1. Get the status of the pod\. 

   ```
   kubectl get pods -o wide --watch
   ```

   Wait for the pod to transition to the `Running` state\.

1. Query the services in your cluster and wait until the **External IP** column for the `windows-server-iis-service` service is populated\.
**Note**  
It might take several minutes for the IP address to become available\.

   ```
   kubectl get services -o wide
   ```

1. After your external IP address is available, point a web browser to that address to view the IIS home page\.
**Note**  
It might take several minutes for DNS to propagate and for your sample application to load in your web browser\.