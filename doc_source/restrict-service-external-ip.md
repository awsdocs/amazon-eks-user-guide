# Restricting external IP addresses that can be assigned to services<a name="restrict-service-external-ip"></a>

Kubernetes services can be reached from inside of a cluster through:
+ A cluster IP address that is assigned automatically by Kubernetes
+ Any IP address that you specify for the `externalIPs` property in a service spec\. External IP addresses are not managed by Kubernetes and are the responsibility of the cluster administrator\. External IP addresses specified with `externalIPs` are different than the external IP address assigned to a service of type `LoadBalancer` by a cloud provider\.

To learn more about Kubernetes services, see [Service](https://kubernetes.io/docs/concepts/services-networking/service/) in the Kubernetes documentation\. You can restrict the IP addresses that can be specified for `externalIPs` in a service spec\.

**To restrict the IP addresses that can be specified for `externalIPs` in a service spec**

1. Deploy cert\-manager to manage webhook certificates\. For more information, see the [cert\-manager](https://cert-manager.io/docs/) documentation\.

   ```
   kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager.yaml
   ```

1. Verify that the cert\-manager pods are running\.

   ```
   kubectl get pods -n cert-manager
   ```

   Output

   ```
   NAME                                       READY   STATUS    RESTARTS   AGE
   cert-manager-58c8844bb8-nlx7q              1/1     Running   0          15s
   cert-manager-cainjector-745768f6ff-696h5   1/1     Running   0          15s
   cert-manager-webhook-67cc76975b-4v4nk      1/1     Running   0          14s
   ```

1. Review your existing services to ensure that none of them have external IP addresses assigned to them that aren't contained within the CIDR block you want to limit addresses to\.

   ```
   kubectl get services --all-namespaces
   ```

   Output

   ```
   NAMESPACE                      NAME                                    TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)         AGE
   cert-manager                   cert-manager                            ClusterIP      10.100.102.137   <none>          9402/TCP        20m
   cert-manager                   cert-manager-webhook                    ClusterIP      10.100.6.136     <none>          443/TCP         20m
   default                        kubernetes                              ClusterIP      10.100.0.1       <none>          443/TCP         2d1h
   externalip-validation-system   externalip-validation-webhook-service   ClusterIP      10.100.234.179   <none>          443/TCP         16s
   kube-system                    kube-dns                                ClusterIP      10.100.0.10      <none>          53/UDP,53/TCP   2d1h
   my-namespace                   my-service                              ClusterIP      10.100.128.10    192.168.1.1     80/TCP          149m
   ```

   If any of the values are IP addresses that are not within the block you want to restrict access to, you'll need to change the addresses to be within the block, and redeploy the services\. For example, the `my-service` service in the previous output has an external IP address assigned to it that isn't within the CIDR block example in step 5\. 

1. Download the external IP webhook manifest\. You can also view the [source code for the webhook](https://github.com/kubernetes-sigs/externalip-webhook) on GitHub\.

   ```
   curl -o externalip-webhook.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/docs/externalip-webhook.yaml
   ```

1. Open the downloaded file in your editor and remove the `#` at the start of the following lines\.

   ```
   #args:
   #- --allowed-external-ip-cidrs=10.0.0.0/8
   ```

   Replace `10.0.0.0/8` with your own CIDR block\. You can specify as many blocks as you like\. If specifying mutiple blocks, add a comma between blocks\.

1. If your cluster is in the `us-gov-west-1`, `us-gov-east-1`, `me-south-1`, `eu-south-1`, `ap-east-1`, `af-south-1`, `cn-north-1`, or `cn-northwest-1` Region, you need to modify the following line to an address listed for the Region in [Amazon EKS add\-on container image addresses](add-ons-images.md)\. If your cluster is in any other Region, you can change *us\-west\-2* to the Region code that your cluster is deployed in\.

   ```
   image: 602401143452.dkr.ecr.us-west-2.amazonaws.com/externalip-webhook:v1.0.0
   ```

1. Apply the manifest to your cluster\.

   ```
   kubectl apply -f externalip-webhook.yaml
   ```

   An attempt to deploy a service to your cluster with an IP address specified for `externalIPs` that is not contained in the blocks that you specified in step 5 will fail\.