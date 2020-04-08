# Installing the Kubernetes Metrics Server<a name="metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. The metrics server is commonly used by other Kubernetes add ons, such as the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) or the [Kubernetes Dashboard](dashboard-tutorial.md)\. For more information, see [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/) in the Kubernetes documentation\. This topic explains how to deploy the Kubernetes metrics server on your Amazon EKS cluster\.

**To deploy the metrics server**

1. Deploy the metrics server with the following command:

   ```
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
   ```

1. Verify that the metrics\-server deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output

   ```
   NAME             READY   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1/1     1            1           6m
   ```