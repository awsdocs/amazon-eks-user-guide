# View resource usage with the KubernetesMetrics Server<a name="metrics-server"></a>

The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster, and it isn't deployed by default in Amazon EKS clusters\. For more information, see [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server) on GitHub\. The Metrics Server is commonly used by other Kubernetes add ons, such as the [Scale pod deployments with Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) or the [Kubernetes Dashboard](eks-managing.md)\. For more information, see [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/) in the Kubernetes documentation\. This topic explains how to deploy the Kubernetes Metrics Server on your Amazon EKS cluster\.

**Important**  
The metrics are meant for point\-in\-time analysis and aren't an accurate source for historical analysis\. They can't be used as a monitoring solution or for other non\-auto scaling purposes\. For information about monitoring tools, see [Observability in Amazon EKS](eks-observe.md)\.

**Deploy the Metrics Server**

1. Deploy the Metrics Server with the following command:

   ```
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   ```

   If you are using Fargate, you will need to change this file\. In the default configuration, the metrics server uses port 10250\. This port is reserved on Fargate\. Replace references to port 10250 in components\.yaml with another port, such as 10251\. 

1. Verify that the `metrics-server` deployment is running the desired number of Pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   An example output is as follows\.

   ```
   NAME             READY   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1/1     1            1           6m
   ```

1. Test the metrics server is working by displaying resource \(CPU/memory\) usage of nodes\. 

   ```
   kubectl top nodes
   ```

1. If you receive the error message `Error from server (Forbidden)`, you need to update your Kubernetes RBAC configuration\. Your Kubernetes RBAC identity needs sufficent permissions to read cluster metrics\. Review the[ minimum required Kubernetes API permissions for reading metrics](https://github.com/kubernetes-sigs/metrics-server/blob/e285375a49e3bf77ddd78c08a05aaa44f2249ebd/manifests/base/rbac.yaml#L5C9-L5C41) on GitHub\. Learn how to[ grant AWS IAM Identities, such as Roles, access to Kubernetes APIs](grant-k8s-access.md#authentication-modes)\. 