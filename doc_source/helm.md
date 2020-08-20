# Using Helm with Amazon EKS<a name="helm"></a>

The Helm package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster\. For more information, see the [Helm documentation](https://docs.helm.sh/)\. This topic helps you install and run the Helm binaries so that you can install and manage charts using the Helm CLI on your local system\.

**Important**  
Before you can install Helm charts on your Amazon EKS cluster, you must configure  `kubectl`  to work for Amazon EKS\. If you have not already done this, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) before proceeding\. If the following command succeeds for your cluster, you're properly configured\.  

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

1. To pick up the new binary in your `PATH`, Close your current terminal window and open a new one\.

1. Confirm that Helm is running with the following command\.

   ```
   helm help
   ```

1. At this point, you can run any Helm commands \(such as `helm install chart_name`\) to install, modify, delete, or query Helm charts in your cluster\. If you're new to Helm and don't have a specific chart to install, you can:
   + Experiment by installing an example chart\. See [Install an example chart](https://helm.sh/docs/intro/quickstart#install-an-example-chart) in the Helm [Quickstart guide](https://helm.sh/docs/intro/quickstart/)\.
   + Install an Amazon EKS chart from the [eks\-charts](https://github.com/aws/eks-charts) GitHub repo or from [Helm Hub](https://hub.helm.sh/charts?q=eks)\.