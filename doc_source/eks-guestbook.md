# Launch a guest book application<a name="eks-guestbook"></a>

In this topic, you create a sample guest book application to test your Amazon EKS cluster\.

**Note**  
For more information about setting up the guest book example, see [https://github\.com/kubernetes/examples/blob/master/guestbook\-go/README\.md](https://github.com/kubernetes/examples/blob/master/guestbook-go/README.md) in the Kubernetes documentation\.

**To create your guest book application**

1. Create the Redis master replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-master-controller.json
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   replicationcontroller "redis-master" created
   ```

1. Create the Redis master service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-master-service.json
   ```

   Output:

   ```
   service "redis-master" created
   ```

1. Create the Redis slave replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-slave-controller.json
   ```

   Output:

   ```
   replicationcontroller "redis-slave" created
   ```

1. Create the Redis slave service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-slave-service.json
   ```

   Output:

   ```
   service "redis-slave" created
   ```

1. Create the guestbook replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/guestbook-controller.json
   ```

   Output:

   ```
   replicationcontroller "guestbook" created
   ```

1. Create the guestbook service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/guestbook-service.json
   ```

   Output:

   ```
   service "guestbook" created
   ```

1. Query the services in your cluster and wait until the **External IP** column for the `guestbook` service is populated\.
**Note**  
It might take several minutes before the IP address is available\.

   ```
   kubectl get services -o wide
   ```

1. After your external IP address is available, point a web browser to that address at port 3000 to view your guest book\. For example, *http://a7a95c2b9e69711e7b1a3022fdcfdf2e\-1985673473\.region\.elb\.amazonaws\.com:3000*
**Note**  
It might take several minutes for DNS to propagate and for your guest book to show up\.  
![\[Guest book\]](http://docs.aws.amazon.com/eks/latest/userguide/images/guestbook.png)
**Important**  
If you are unable to connect to the external IP address with your browser, be sure that your corporate firewall is not blocking non\-standards ports, like 3000\. You can try switching to a guest network to verify\.

**To clean up your guest book application**

When you are finished experimenting with your guest book application, you should clean up the resources that you created for it\.
+ The following command deletes all of the services and replication controllers for the guest book application:

  ```
  kubectl delete rc/redis-master rc/redis-slave rc/guestbook svc/redis-master svc/redis-slave svc/guestbook
  ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

  If you are done with your Amazon EKS cluster, you should delete it and its resources so that you do not incur additional charges\. For more information, see [Deleting a cluster](delete-cluster.md)\.