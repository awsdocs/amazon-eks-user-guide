--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Installing the Kubernetes Metrics Server<a name="metrics-server"></a>

**Important**  

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