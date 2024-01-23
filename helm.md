# Using Helm with Amazon EKS<a name="helm"></a>

The Helm package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster\. For more information, see the [Helm documentation](https://docs.helm.sh/)\. This topic helps you install and run the Helm binaries so that you can install and manage charts using the Helm CLI on your local system\.

**Important**  
Before you can install Helm charts on your Amazon EKS cluster, you must configure  `kubectl`  to work for Amazon EKS\. If you have not already done this, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md) before proceeding\. If the following command succeeds for your cluster, you're properly configured\.  

```
kubectl get svc
```

**To install the Helm binaries on your local system**

1. Run the appropriate command for your client operating system\.
   + If you're using macOS with [Homebrew](https://brew.sh/), install the binaries with the following command\.

     ```
     brew install helm
     ```
   + If you're using Windows with [Chocolatey](https://chocolatey.org/), install the binaries with the following command\.

     ```
     choco install kubernetes-helm
     ```
   + If you're using Linux, install the binaries with the following commands\.

     ```
     curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
     chmod 700 get_helm.sh
     ./get_helm.sh
     ```
**Note**  
If you get a message that `openssl` must first be installed, you can install it with the following command\.   

     ```
     sudo yum install openssl
     ```

1. To pick up the new binary in your `PATH`, Close your current terminal window and open a new one\.

1. See the version of Helm that you installed\.

   ```
   helm version | cut -d + -f 1
   ```

   An example output is as follows\.

   ```
   v3.9.0
   ```

1. At this point, you can run any Helm commands \(such as `helm install chart-name`\) to install, modify, delete, or query Helm charts in your cluster\. If you're new to Helm and don't have a specific chart to install, you can:
   + Experiment by installing an example chart\. See [Install an example chart](https://helm.sh/docs/intro/quickstart#install-an-example-chart) in the Helm [Quickstart guide](https://helm.sh/docs/intro/quickstart/)\.
   + Create an example chart and push it to Amazon ECR\. For more information, see [Pushing a Helm chart](https://docs.aws.amazon.com/AmazonECR/latest/userguide/push-oci-artifact.html) in the *Amazon Elastic Container Registry User Guide*\.
   + Install an Amazon EKS chart from the [eks\-charts](https://github.com/aws/eks-charts#eks-charts) GitHub repo or from [ ArtifactHub](https://artifacthub.io/packages/search?page=1&repo=aws)\.