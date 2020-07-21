# Tutorial: Deploy the Kubernetes Dashboard \(web UI\)<a name="dashboard-tutorial"></a>

This tutorial guides you through deploying the [Kubernetes Dashboard](https://github.com/kubernetes/dashboard) to your Amazon EKS cluster, complete with CPU and memory metrics\. It also helps you to create an Amazon EKS administrator service account that you can use to securely connect to the dashboard to view and control your cluster\.

![\[Kubernetes Dashboard\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubernetes-dashboard.png)

## Prerequisites<a name="dashboard-prereqs"></a>

This tutorial assumes the following:
+ You have created an Amazon EKS cluster by following the steps in [Getting started with Amazon EKS](getting-started.md)\.
+ The security groups for your control plane elastic network interfaces and nodes follow the recommended settings in [Amazon EKS security group considerations](sec-group-reqs.md)\.
+ You are using a kubectl client that is [configured to communicate with your Amazon EKS cluster](getting-started-console.md#eks-configure-kubectl)\.

## Step 1: Deploy the Kubernetes Metrics Server<a name="dashboard-metrics-server"></a>

The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. The Kubernetes Dashboard uses the metrics server to gather metrics for your cluster, such as CPU and memory usage over time\.

**To deploy the Metrics Server**

1. Deploy the Metrics Server with the following command:

   ```
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output

   ```
   NAME             READY   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1/1     1            1           6m
   ```

## Step 2: Deploy the dashboard<a name="deploy-dashboard"></a>

Use the following command to deploy the Kubernetes Dashboard\.

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
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

## Step 3: Create an `eks-admin` service account and cluster role binding<a name="eks-admin-service-account"></a>

By default, the Kubernetes Dashboard user has limited permissions\. In this section, you create an `eks-admin` service account and cluster role binding that you can use to securely connect to the dashboard with admin\-level permissions\. For more information, see [Managing Service Accounts](https://kubernetes.io/docs/admin/service-accounts-admin/) in the Kubernetes documentation\.

**To create the `eks-admin` service account and cluster role binding**
**Important**  
The example service account created with this procedure has full `cluster-admin` \(superuser\) privileges on the cluster\. For more information, see [Using RBAC authorization](https://kubernetes.io/docs/admin/authorization/rbac/) in the Kubernetes documentation\.

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

## Step 4: Connect to the dashboard<a name="view-dashboard"></a>

Now that the Kubernetes Dashboard is deployed to your cluster, and you have an administrator service account that you can use to view and control your cluster, you can connect to the dashboard with that service account\.

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

1. To access the dashboard endpoint, open the following link with a web browser: [http://localhost:8001/api/v1/namespaces/kubernetes\-dashboard/services/https:kubernetes\-dashboard:/proxy/\#\!/login](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login)\.

1. Choose **Token**, paste the *<authentication\_token>* output from the previous command into the **Token** field, and choose **SIGN IN**\.  
![\[Kubernetes token auth\]](http://docs.aws.amazon.com/eks/latest/userguide/images/dashboard-token-auth.png)
**Note**  
It may take a few minutes before CPU and memory metrics appear in the dashboard\.

## Step 5: Next steps<a name="dashboard-next-steps"></a>

After you have connected to your Kubernetes Dashboard, you can view and control your cluster using your `eks-admin` service account\. For more information about using the dashboard, see the [project documentation on GitHub](https://github.com/kubernetes/dashboard)\.