# Using Helm with Amazon EKS<a name="helm"></a>

The `helm` package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster\. For more information, see the [Helm documentation](https://docs.helm.sh/)\. This topic helps you install and run the `helm` and `tiller` binaries locally so that you can install and manage charts using the `helm` CLI on your local system\.

Although you can run the server\-side `tiller` component in your cluster \(and many public Helm installation articles offer only this option\), running `tiller` locally in its own namespace as described in this topic reduces the risk of exploit for your cluster in the following ways:
+ When you run the `tiller` server on your cluster, it gets its own Kubernetes Identity and associated permission set, often with full Kubernetes administrator permissions\. This opens up the possibility for a privilege escalation, where an unprivileged Kubernetes user who has network access to the `tiller` server can gain additional Kubernetes permissions by way of installing a chart\.
+ When you run the `tiller` server on your local machine, users don't inherit the `tiller` server permissions on the cluster \(likely full\-admin\), but instead `tiller` inherits the Kubernetes permissions of the end\-user\.
+ Running `tiller` in its own namespace allows you to control access to the Kubernetes secrets that the `tiller` server stores by controlling access to that namespace\.

**Important**  
Before you can install Helm charts on your Amazon EKS cluster, you must configure kubectl to work for Amazon EKS\. If you have not already done this, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) before proceeding\. If the following command succeeds for your cluster, you're properly configured\.  

```
kubectl get svc
```

**To install the `helm` and `tiller` binaries on your local system**

1. 
   + If you're using macOS with [Homebrew](https://brew.sh/), install the binaries with the following command\.

     ```
     brew install kubernetes-helm
     ```
   + If you're using Windows with [Chocolatey](https://chocolatey.org/), install the binaries with the following command\.

     ```
     choco install kubernetes-helm
     ```
   + Otherwise, see [Installing the Helm Client](https://docs.helm.sh/using_helm/#installing-the-helm-client) in the Helm documentation\.
**Important**  
Don't proceed to install the `tiller` server\-side component with the Helm documentation \(stop before you reach [Installing Tiller](https://docs.helm.sh/using_helm/#installing-tiller)\)\. This topic explains how to run `tiller` locally in its own namespace, which reduces the risk of exploit for your cluster\.

1. To pick up the new binaries in your `PATH`, Close your current terminal window and open a new one\.

**To run `helm` and `tiller` locally**

1. Create a namespace called `tiller` with the following command\.

   ```
   kubectl create namespace tiller
   ```
**Note**  
By default, `tiller` stores its secrets in the `kube-system` namespace\. Creating a namespace for `tiller` and specifying that namespace when you run it gives you more specific access controls to who is authorized to view the Helm chart secrets that `tiller` stores in your cluster\.

1. Open a new terminal window for the `tiller` server\. For the following steps, you need a terminal window for the `tiller` server and another window for the `helm` client\.
**Important**  
You should ensure that you are the only active user for the system that you use for the `tiller` server \(such as a local laptop or desktop where you are the only user that is logged in\)\. Otherwise, any user on your system could make requests to the `tiller` server with your Kubernetes permissions\. For Linux and macOS systems, you can see the current users with the following command:  

   ```
   users
   ```
Output:  

   ```
   ericn
   ```
In the above example, there is only a single user named *ericn* on the system, so it is safe to proceed\. If there are more than one user logged in to your system, you should use a different system, or consider launching an Amazon EC2 instance for this procedure so that you can ensure that you are the only active user\.

1. In the `tiller` server terminal, set the `TILLER_NAMESPACE` environment variable to `tiller` and then start the `tiller` server\.

   1. Set the `TILLER_NAMESPACE` environment variable to `tiller`\.
      + **macOS and Linux**:

        ```
        export TILLER_NAMESPACE=tiller
        ```
      + **Windows \(PowerShell\)**:

        ```
        $env:TILLER_NAMESPACE = 'tiller'
        ```

   1. Start the `tiller` server\.
      + **macOS and Linux**:

        ```
        tiller -listen=localhost:44134 -storage=secret -logtostderr
        ```
      + **Windows \(PowerShell\)**:

        ```
        tiller -listen=localhost:44134 -storage=secret
        ```
**Note**  
By default, `tiller` stores release information in ConfigMaps; however, the latest Helm documentation recommends that you use the `-storage=secret` flag to store this information with Kubernetes secrets instead\. For more information, see [Tiller's Release Information](https://helm.sh/docs/using_helm/#tiller-s-release-information) in [Securing your Helm Installation](https://helm.sh/docs/using_helm/#securing-your-helm-installation)\. The `-listen=localhost:44134` flag ensures that the `tiller` server only accepts requests from your local machine \(this prevents unauthorized network users from accessing your local `tiller` process\)\.

1. In the `helm` client terminal window, set the `HELM_HOST` environment variable to `:44134`\.
   + **macOS and Linux**:

     ```
     export HELM_HOST=:44134
     ```
   + **Windows \(PowerShell\)**:

     ```
     $env:HELM_HOST = ':44134'
     ```

1. In the `helm` client terminal window, initialize the `helm` client\.

   ```
   helm init --client-only
   ```

1. In the `helm` client terminal window, verify that `helm` is communicating with the `tiller` server properly\.

   ```
   helm repo update
   ```

   Output:

   ```
   Hang tight while we grab the latest from your chart repositories...
   ...Skip local chart repository
   ...Successfully got an update from the "stable" chart repository
   Update Complete. ⎈ Happy Helming!⎈
   ```

1. At this point, you can run any `helm` commands in your `helm` client terminal window \(such as `helm install chart_name`\) to install, modify, delete, or query Helm charts in your cluster\. As you run `helm` commands, you can follow the `tiller` logs for those commands in its server terminal window\. For more information, see [Helm Commands](https://docs.helm.sh/helm/) and [Charts](https://helm.sh/docs/topics/charts/) in the Helm documentation\.

   If you're just experimenting with `helm` and you don't have a specific chart to install, you can see [Install an Example Chart](https://docs.helm.sh/using_helm/#install-an-example-chart) in the Helm [Quickstart Guide](https://docs.helm.sh/using_helm/)\.

1. When you're finished, close your `helm` client and `tiller` server terminal windows\. Repeat this procedure when you want to use `helm` with your cluster\.