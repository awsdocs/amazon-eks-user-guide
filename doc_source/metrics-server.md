# Installing the Kubernetes Metrics Server<a name="metrics-server"></a>

The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. For more information, see [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server) on GitHub\. The Metrics Server is commonly used by other Kubernetes add ons, such as the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) or the [Kubernetes Dashboard](dashboard-tutorial.md)\. For more information, see [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/) in the Kubernetes documentation\. This topic explains how to deploy the Kubernetes Metrics Server on your Amazon EKS cluster\.

**Deploy the Metrics Server**

1. Deploy the Metrics Server with the following command:

   ```
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   ```

1. Modify the manifest\.

   1. View the manifest file or files that you downloaded and note the name of the image\. Download the image locally with the following command\.

      ```
      docker pull image:<tag>
      ```

   1. Tag the image to be pushed to an Amazon Elastic Container Registry repository in China with the following command\.

      ```
      docker tag image:<tag> <aws_account_id>.dkr.ecr.<cn-north-1>.amazonaws.com.cn/image:<tag>
      ```

   1. Push the image to a China Amazon ECR repository with the following command\.

      ```
      docker push image:<tag> <aws_account_id>.dkr.ecr.<cn-north-1>.amazonaws.com.cn/image:<tag>
      ```

   1. Update the Kubernetes manifest file or files to reference the Amazon ECR image URL in your Region\.

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output

   ```
   NAME             READY   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1/1     1            1           6m
   ```