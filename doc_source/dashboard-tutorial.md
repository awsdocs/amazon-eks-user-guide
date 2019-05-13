# Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)<a name="dashboard-tutorial"></a>

This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your Amazon EKS cluster, complete with CPU and memory metrics\. It also helps you to create an Amazon EKS administrator service account that you can use to securely connect to the dashboard to view and control your cluster\.

![\[Kubernetes dashboard\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubernetes-dashboard.png)

## Prerequisites<a name="dashboard-prereqs"></a>

This tutorial assumes the following:
+ You have created an Amazon EKS cluster by following the steps in [Getting Started with Amazon EKS](getting-started.md)\.
+ The security groups for your control plane elastic network interfaces and worker nodes follow the recommended settings in [Cluster Security Group Considerations](sec-group-reqs.md)\.
+ You are using a kubectl client that is [configured to communicate with your Amazon EKS cluster](getting-started-console.md#eks-configure-kubectl)\.

## Step 1: Deploy the Dashboard<a name="deploy-dashboard"></a>

Use the following steps to deploy the Kubernetes dashboard, `heapster`, and the `influxdb` backend for CPU and memory metrics to your cluster\.

**To deploy the Kubernetes dashboard**

1. Deploy the Kubernetes dashboard to your cluster:

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
   ```

   Output:

   ```
   secret "kubernetes-dashboard-certs" created
   serviceaccount "kubernetes-dashboard" created
   role "kubernetes-dashboard-minimal" created
   rolebinding "kubernetes-dashboard-minimal" created
   deployment "kubernetes-dashboard" created
   service "kubernetes-dashboard" created
   ```

1. Deploy `heapster` to enable container cluster monitoring and performance analysis on your cluster:

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/heapster.yaml
   ```
**Note**  
Although `heapster` is deprecated, it is currently the only supported metrics provider for the Kubernetes dashboard\. For more information, see [https://github\.com/kubernetes/dashboard/issues/2986](https://github.com/kubernetes/dashboard/issues/2986)\.

   Output:

   ```
   serviceaccount "heapster" created
   deployment "heapster" created
   service "heapster" created
   ```

1. Deploy the `influxdb` backend for `heapster` to your cluster:

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/influxdb.yaml
   ```

   Output:

   ```
   deployment "monitoring-influxdb" created
   service "monitoring-influxdb" created
   ```

1. Create the `heapster` cluster role binding for the dashboard: 

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/rbac/heapster-rbac.yaml
   ```

   Output:

   ```
   clusterrolebinding "heapster" created
   ```

## Step 2: Create an `eks-admin` Service Account and Cluster Role Binding<a name="eks-admin-service-account"></a>

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

1. Apply the service account and cluster role binding to your cluster:

   ```
   kubectl apply -f eks-admin-service-account.yaml
   ```

   Output:

   ```
   serviceaccount "eks-admin" created
   clusterrolebinding.rbac.authorization.k8s.io "eks-admin" created
   ```

## Step 3: Connect to the Dashboard<a name="view-dashboard"></a>

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

1. Open the following link with a web browser to access the dashboard endpoint: [http://localhost:8001/api/v1/namespaces/kube\-system/services/https:kubernetes\-dashboard:/proxy/\#\!/login](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login)

1. Choose **Token**, paste the *<authentication\_token>* output from the previous command into the **Token** field, and choose **SIGN IN**\.  
![\[Kubernetes token auth\]](http://docs.aws.amazon.com/eks/latest/userguide/images/dashboard-token-auth.png)
**Note**  
It may take a few minutes before CPU and memory metrics appear in the dashboard\.

## Step 4: Next Steps<a name="dashboard-next-steps"></a>

After you have connected to your Kubernetes cluster dashboard, you can view and control your cluster using your `eks-admin` service account\. For more information about using the dashboard, see the [project documentation on GitHub](https://github.com/kubernetes/dashboard)\.