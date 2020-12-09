# View workloads<a name="view-workloads"></a>

Workloads define applications running on a Kubernetes cluster\. Every workload controls pods\. Pods are the fundamental unit of computing within a Kubernetes cluster and represent one or more containers that run together\.

You can use the Amazon EKS console to view information about the Kubernetes workloads and pods running on your cluster\.

**Prerequisites**

The IAM user or IAM role that you sign into the AWS Management Console with must meet the following requirements\.
+ Has the `eks:AccessKubernetesApi` and other necessary IAM permissions to view workloads attached to it\. For an example IAM policy, see [View nodes and workloads for all clusters in the AWS Management Console](security_iam_id-based-policy-examples.md#policy_example3) \.
+ Is mapped to Kubernetes user or group in the `aws-auth` `configmap`\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\.
+ The Kubernetes user or group that the IAM user or role is mapped to in the configmap must be bound to a Kubernetes `role` or `clusterrole` that has permissions to view the resources in the namespaces that you want to view\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can download the following example manifests that create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`:
  + **View Kubernetes resources in all namespaces** – The group name in the file is `eks-console-dashboard-full-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the Region that your cluster is in\.
    + [All Regions other than Beijing and Ningxia China](https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml)
    + [Beijing and Ningxia China Regions](https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/docs/eks-console-full-access.yaml)
  + **View Kubernetes resources in a specific namespace** – The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\. The group name in the file is `eks-console-dashboard-restricted-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the Region that your cluster is in\.
    + [All Regions other than Beijing and Ningxia China](https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml)
    + [Beijing and Ningxia China Regions](https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/docs/eks-console-restricted-access.yaml)

**To view workloads using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **Clusters** list, select the cluster that you want to view workloads for\.

1. On the **Workloads** tab, you see a list of **Names** of all the Kubernetes workloads that are currently deployed to your cluster, the **Pod count**, and **Status** for each workload\. 
**Important**  
If you can't see any workloads, or you see a **Your current user or role does not have access to Kubernetes objects on this EKS cluster**, you may need to select a different namespace from the **All Namespaces** drop\-down list\. If you're still having problems, see the prerequisites for this topic\. If you don't resolve the issue, you can still view and manage your Amazon EKS cluster on the **Configuration** tab, but you won't be able to see information about your workloads\.

   You can deploy the following types of workloads on a cluster\.
   + **Deployment** – Ensures that a specific number of pods run and includes logic to deploy changes\.
   + **ReplicaSet** – Ensures that a specific number of pods run\. Can be controlled by deployments\.
   + **StatefulSet** – Manages the deployment of stateful applications\.
   + **DaemonSet** – Ensures that a copy of a pod runs on all \(or some\) nodes in the cluster\.
   + **Job** – Creates one or more pods and ensures that a specified number of them run to completion\.

   For more information, see [Workloads](https://kubernetes.io/docs/concepts/workloads/) in the Kubernetes documentation\.

   By default, all Amazon EKS clusters have the following workloads:
   + **coredns** –A `Deployment` that deploys two replicas of the `coredns` pods\. The pods provide name resolution for all pods in the cluster\. Two pods are deployed by default for high availability, regardless of the number of nodes deployed in your cluster\. For more information, see [Installing or upgrading CoreDNS](coredns.md)\. The pods can be deployed to any node type\. However, they can be deployed to Fargate nodes only if your cluster includes a Fargate profile with a namespace that matches the namespace for the workload\.
   + **aws\-node** – A `DaemonSet` that deploys one pod to each Amazon EC2 node in your cluster\. The pod runs the Amazon Virtual Private Cloud \(Amazon VPC\) CNI controller, which provides VPC networking functionality to the pods and nodes in your cluster\. For more information, see [Pod networking \(CNI\)](pod-networking.md)\. This workload isn't deployed to Fargate nodes because Fargate already contains the Amazon VPC CNI controller\.
   + **kube\-proxy** – A `DaemonSet` that deploys one pod to each Amazon EC2 node in your cluster\. The pods maintain network rules on nodes that enable networking communication to your pods\. For more information, see [https://kubernetes.io/docs/concepts/overview/components/#kube-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy) in the Kubernetes documentation\. This workload isn't deployed to Fargate nodes\. 

**View workload details**  
Selecting the link in the **Name** column for one of the **Workloads** shows you the following information:
   + The **Status**, **Namespace**, and **Selectors** \(if any\) assigned to the workload\.
   + The list of **Pods** managed by the workload, their **Status** and **Created** date and time\.
   + The Kubernetes **Labels** and **Annotations** assigned to the workload\. These could have been assigned by you, by Kubernetes, or by the Amazon EKS API when the workload was created\.

   Some of the detailed information that you see when inspecting a workload might be different depending on the type of workload\. To learn more about the unique properties of each workload type, see [Workloads](https://kubernetes.io/docs/concepts/workloads/) in the Kubernetes documentation\.

**View pod details**  
Pods are the fundamental unit of computing within a Kubernetes cluster and represent one or more containers that run together\. Each workload controls one of more pods running on the cluster\. Pods are designed as relatively ephemeral and immutable objects\. Over time it's normal to have pods start and stop while your cluster is running\. Pods starting or stopping reflect changes in your workloads as well as changes in the scale of your cluster\. For more information, see [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) in the Kubernetes documentation\.

   When viewing a workload, select a link in the **Name** column for one of the **Pods** to see the following information about the pod:
   + The Kubernetes **Namespace** that the pod is in and the pod's **Status**\.
   + The node on which the pod is running\. The node might be an Amazon EC2 instance or a Fargate pod\. For more information about viewing nodes, see [View nodes](view-nodes.md)\.
   + The **Containers** in the pod\. Selecting the name of a container provides the **Image**, **Ports**, **Mounts**, and **Arguments** provided when the pod was started\. Pods can define two types of containers\. The first is *application* containers, which are containers that run as long as the pod is running\. The second is *init* containers, which are containers that serve as processes that run during pod startup\. You can see both types of containers on the pod detail page\.
   + The Kubernetes **Labels** and **Annotations** assigned to the pod\.