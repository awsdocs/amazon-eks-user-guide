# Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)<a name="dashboard-tutorial"></a>

This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your Amazon EKS cluster, complete with CPU and memory metrics\. It also helps you to create an Amazon EKS administrator service account that you can use to securely connect to the dashboard to view and control your cluster\.

![\[Kubernetes dashboard\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubernetes-dashboard.png)

## Prerequisites<a name="dashboard-prereqs"></a>

This tutorial assumes the following:
+ You have created an Amazon EKS cluster by following the steps in [Getting Started with Amazon EKS](getting-started.md)\.
+ The security groups for your control plane elastic network interfaces and worker nodes follow the recommended settings in [Cluster Security Group Considerations](sec-group-reqs.md)\.
+ You are using a kubectl client that is [configured to communicate with your Amazon EKS cluster](getting-started-console.md#eks-configure-kubectl)\.

## Step 1: Deploy the Kubernetes Metrics Server<a name="dashboard-metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. The Kubernetes dashboard uses the metrics server to gather metrics for your cluster, such as CPU and memory usage over time\. Choose the tab below that corresponds to your desired deployment method\.

------
#### [ curl and jq ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using `curl` and `jq`**

If you have a macOS or Linux system with `curl`, `tar`, `gzip`, and the `jq` JSON parser installed, you can download, extract, and install the latest release with the following commands\. Otherwise, use the next procedure to download the latest version using a web browser\.

1. Open a terminal window and navigate to a directory where you would like to download the latest `metrics-server` release\. 

1. Copy and paste the commands below into your terminal window and type **Enter** to execute them\. These commands download the latest release, extract it, and apply the version 1\.8\+ manifests to your cluster\.

   ```
   DOWNLOAD_URL=$(curl --silent "https://api.github.com/repos/kubernetes-incubator/metrics-server/releases/latest" | jq -r .tarball_url)
   DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
   curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
   mkdir metrics-server-$DOWNLOAD_VERSION
   tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
   kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------
#### [ Web browser ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using a web browser**

1. Download and extract the latest version of the metrics server code from GitHub\.

   1. Navigate to the latest release page of the `metrics-server` project on GitHub \([https://github\.com/kubernetes\-incubator/metrics\-server/releases/latest](https://github.com/kubernetes-incubator/metrics-server/releases/latest)\), then choose a source code archive for the latest release to download it\.
**Note**  
If you are downloading to a remote server, you can use the following `curl` command, substituting the red text with the latest version number\.  

      ```
      curl --remote-name --location https://github.com/kubernetes-incubator/metrics-server/archive/v0.3.4.tar.gz
      ```

   1. Navigate to your downloads location and extract the source code archive\. For example, if you downloaded the `.tar.gz` archive on a macOS or Linux system, use the following command to extract \(substituting your release version\)\. 

      ```
      tar -xzf v0.3.4.tar.gz
      ```

1. Apply all of the YAML manifests in the `metrics-server-0.3.4/deploy/1.8+` directory \(substituting your release version\)\.

   ```
   kubectl apply -f metrics-server-0.3.4/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------

## Step 2: Deploy the Dashboard<a name="deploy-dashboard"></a>

Use the following command to deploy the Kubernetes dashboard\.

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta4/aio/deploy/recommended.yaml
```

Output:

```
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
```

## Step 3: Create an `eks-admin` Service Account and Cluster Role Binding<a name="eks-admin-service-account"></a>

By default, the Kubernetes dashboard user has limited permissions\. In this section, you create an `eks-admin` service account and cluster role binding that you can use to securely connect to the dashboard with admin\-level permissions\. For more information, see [Managing Service Accounts](https://kubernetes.io/docs/admin/service-accounts-admin/) in the Kubernetes documentation\.

**To create the `eks-admin` service account and cluster role binding**
**Important**  
The example service account created with this procedure has full `cluster-admin` \(superuser\) privileges on the cluster\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/admin/authorization/rbac/) in the Kubernetes documentation\.

1. Create a file called `eks-admin-service-account.yaml` with the text below\. This manifest defines a service account and cluster role binding called `eks-admin`\.

   ```
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: eks-admin
     namespace: kube-system
   ---
   apiVersion: rbac.authorization.k8s.io/v1beta1
   kind: ClusterRoleBinding
   metadata:
     name: eks-admin
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: ClusterRole
     name: cluster-admin
   subjects:
   - kind: ServiceAccount
     name: eks-admin
     namespace: kube-system
   ```

1. Apply the service account and cluster role binding to your cluster\.

   ```
   kubectl apply -f eks-admin-service-account.yaml
   ```

   Output:

   ```
   serviceaccount "eks-admin" created
   clusterrolebinding.rbac.authorization.k8s.io "eks-admin" created
   ```

## Step 4: Connect to the Dashboard<a name="view-dashboard"></a>

Now that the Kubernetes dashboard is deployed to your cluster, and you have an administrator service account that you can use to view and control your cluster, you can connect to the dashboard with that service account\.

**To connect to the Kubernetes dashboard**

1. Retrieve an authentication token for the `eks-admin` service account\. Copy the *<authentication\_token>* value from the output\. You use this token to connect to the dashboard\.

   ```
   kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')
   ```

   Output:

   ```
   Name:         eks-admin-token-b5zv4
   Namespace:    kube-system
   Labels:       <none>
   Annotations:  kubernetes.io/service-account.name=eks-admin
                 kubernetes.io/service-account.uid=bcfe66ac-39be-11e8-97e8-026dce96b6e8
   
   Type:  kubernetes.io/service-account-token
   
   Data
   ====
   ca.crt:     1025 bytes
   namespace:  11 bytes
   token:      <authentication_token>
   ```

1. Start the kubectl proxy\.

   ```
   kubectl proxy
   ```

1. To access the dashboard endpoint, open the following link with a web browser: [http://localhost:8001/api/v1/namespaces/kubernetes\-dashboard/services/https:kubernetes\-dashboard:/proxy/\#\!/login](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login)

1. Choose **Token**, paste the *<authentication\_token>* output from the previous command into the **Token** field, and choose **SIGN IN**\.  
![\[Kubernetes token auth\]](http://docs.aws.amazon.com/eks/latest/userguide/images/dashboard-token-auth.png)
**Note**  
It may take a few minutes before CPU and memory metrics appear in the dashboard\.

## Step 5: Next Steps<a name="dashboard-next-steps"></a>

After you have connected to your Kubernetes cluster dashboard, you can view and control your cluster using your `eks-admin` service account\. For more information about using the dashboard, see the [project documentation on GitHub](https://github.com/kubernetes/dashboard)\.