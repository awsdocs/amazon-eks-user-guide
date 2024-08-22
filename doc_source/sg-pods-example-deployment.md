# Use a security group policy for an Amazon EKS Pod<a name="sg-pods-example-deployment"></a>

To use security groups for Pods, you must have an existing security group\. The following steps show you how to use the security group policy for a Pod\. Unless otherwise noted, complete all steps from the same terminal because variables are used in the following steps that don't persist across terminals\.

If you have a Pod with Amazon EC2 instances, you must configure the plugin before you use this procedure\. For more information, see [Configure the Amazon VPC CNI plugin for Kubernetes for security groups for Amazon EKS Pods](security-groups-pods-deployment.md)\.

1. Create a Kubernetes namespace to deploy resources to\. You can replace *my\-namespace* with the name of a namespace that you want to use\.

   ```
   kubectl create namespace my-namespace
   ```

1. Deploy an Amazon EKS `SecurityGroupPolicy` to your cluster\.

   1. Copy the following contents to your device\. You can replace *podSelector* with **serviceAccountSelector** if you'd rather select Pods based on service account labels\. You must specify one selector or the other\. An empty `podSelector` \(example: `podSelector: {}`\) selects all Pods in the namespace\. You can change *my\-role* to the name of your role\. An empty `serviceAccountSelector` selects all service accounts in the namespace\. You can replace *my\-security\-group\-policy* with a name for your `SecurityGroupPolicy` and *my\-namespace* with the namespace that you want to create the `SecurityGroupPolicy` in\. 

      You must replace *my\_pod\_security\_group\_id* with the ID of an existing security group\. If you don't have an existing security group, then you must create one\. For more information, see [Amazon EC2 security groups for Linux instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) in the [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)\. You can specify 1\-5 security group IDs\. If you specify more than one ID, then the combination of all the rules in all the security groups are effective for the selected Pods\.

      ```
      cat >my-security-group-policy.yaml <<EOF
      apiVersion: vpcresources.k8s.aws/v1beta1
      kind: SecurityGroupPolicy
      metadata:
        name: my-security-group-policy
        namespace: my-namespace
      spec:
        podSelector: 
          matchLabels:
            role: my-role
        securityGroups:
          groupIds:
            - my_pod_security_group_id
      EOF
      ```
**Important**  
The security group or groups that you specify for your Pods must meet the following criteria:  
They must exist\. If they don't exist, then, when you deploy a Pod that matches the selector, your Pod remains stuck in the creation process\. If you describe the Pod, you'll see an error message similar to the following one: `An error occurred (InvalidSecurityGroupID.NotFound) when calling the CreateNetworkInterface operation: The securityGroup ID 'sg-05b1d815d1EXAMPLE' does not exist`\.
They must allow inbound communication from the security group applied to your nodes \(for `kubelet`\) over any ports that you've configured probes for\.
They must allow outbound communication over `TCP` and `UDP` ports 53 to a security group assigned to the Pods \(or nodes that the Pods run on\) running CoreDNS\. The security group for your CoreDNS Pods must allow inbound `TCP` and `UDP` port 53 traffic from the security group that you specify\.
They must have necessary inbound and outbound rules to communicate with other Pods that they need to communicate with\.
They must have rules that allow the Pods to communicate with the Kubernetes control plane if you're using the security group with Fargate\. The easiest way to do this is to specify the cluster security group as one of the security groups\.
Security group policies only apply to newly scheduled Pods\. They do not affect running Pods\.

   1. Deploy the policy\.

      ```
      kubectl apply -f my-security-group-policy.yaml
      ```

1. Deploy a sample application with a label that matches the `my-role` value for `podSelector` that you specified in a previous step\.

   1. Copy the following contents to your device\. Replace the *example values* with your own and then run the modified command\. If you replace *my\-role*, make sure that it's the same as the value you specified for the selector in a previous step\.

      ```
      cat >sample-application.yaml <<EOF
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        replicas: 4
        selector:
          matchLabels:
            app: my-app
        template:
          metadata:
            labels:
              app: my-app
              role: my-role
          spec:
            terminationGracePeriodSeconds: 120
            containers:
            - name: nginx
              image: public.ecr.aws/nginx/nginx:1.23
              ports:
              - containerPort: 80
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: my-app
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        selector:
          app: my-app
        ports:
          - protocol: TCP
            port: 80
            targetPort: 80
      EOF
      ```

   1. Deploy the application with the following command\. When you deploy the application, the Amazon VPC CNI plugin for Kubernetes matches the `role` label and the security groups that you specified in the previous step are applied to the Pod\.

      ```
      kubectl apply -f sample-application.yaml
      ```

1. View the Pods deployed with the sample application\. For the remainder of this topic, this terminal is referred to as `TerminalA`\.

   ```
   kubectl get pods -n my-namespace -o wide
   ```

   An example output is as follows\.

   ```
   NAME                             READY   STATUS    RESTARTS   AGE     IP               NODE                                            NOMINATED NODE   READINESS GATES
   my-deployment-5df6f7687b-4fbjm   1/1     Running   0          7m51s   192.168.53.48    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-j9fl4   1/1     Running   0          7m51s   192.168.70.145   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-rjxcz   1/1     Running   0          7m51s   192.168.73.207   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-zmb42   1/1     Running   0          7m51s   192.168.63.27    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   ```
**Note**  
If any Pods are stuck in the `Waiting` state, then run `kubectl describe pod my-deployment-xxxxxxxxxx-xxxxx -n my-namespace`\. If you see `Insufficient permissions: Unable to create Elastic Network Interface.`, confirm that you added the IAM policy to the IAM cluster role in a previous step\.
If any Pods are stuck in the `Pending` state, confirm that your node instance type is listed in [https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go) and that the product of the maximum number of branch network interfaces supported by the instance type multiplied times the number of nodes in your node group hasn't already been met\. For example, an `m5.large` instance supports nine branch network interfaces\. If your node group has five nodes, then a maximum of 45 branch network interfaces can be created for the node group\. The 46th Pod that you attempt to deploy will sit in `Pending` state until another Pod that has associated security groups is deleted\.

   If you run `kubectl describe pod my-deployment-xxxxxxxxxx-xxxxx -n my-namespace` and see a message similar to the following message, then it can be safely ignored\. This message might appear when the Amazon VPC CNI plugin for Kubernetes tries to set up host networking and fails while the network interface is being created\. The plugin logs this event until the network interface is created\.

   ```
   Failed to create Pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container "e24268322e55c8185721f52df6493684f6c2c3bf4fd59c9c121fd4cdc894579f" network for Pod "my-deployment-5df6f7687b-4fbjm": networkPlugin
   cni failed to set up Pod "my-deployment-5df6f7687b-4fbjm-c89wx_my-namespace" network: add cmd: failed to assign an IP address to container
   ```

   You can't exceed the maximum number of Pods that can be run on the instance type\. For a list of the maximum number of Pods that you can run on each instance type, see [eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/main/templates/shared/runtime/eni-max-pods.txt) on GitHub\. When you delete a Pod that has associated security groups, or delete the node that the Pod is running on, the VPC resource controller deletes the branch network interface\. If you delete a cluster with Pods using Pods for security groups, then the controller doesn't delete the branch network interfaces, so you'll need to delete them yourself\. For information about how to delete network interfaces, see [Delete a network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#delete_eni) in the Amazon EC2 User Guide\.

1. In a separate terminal, shell into one of the Pods\. For the remainder of this topic, this terminal is referred to as `TerminalB`\. Replace **5df6f7687b*\-*4fbjm** with the ID of one of the Pods returned in your output from the previous step\.

   ```
   kubectl exec -it -n my-namespace my-deployment-5df6f7687b-4fbjm -- /bin/bash
   ```

1. From the shell in `TerminalB`, confirm that the sample application works\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   [...]
   ```

   You received the output because all Pods running the application are associated with the security group that you created\. That group contains a rule that allows all traffic between all Pods that the security group is associated to\. DNS traffic is allowed outbound from that security group to the cluster security group, which is associated with your nodes\. The nodes are running the CoreDNS Pods, which your Pods did a name lookup to\.

1. From `TerminalA`, remove the security group rules that allow DNS communication to the cluster security group from your security group\. If you didn't add the DNS rules to the cluster security group in a previous step, then replace `$my_cluster_security_group_id` with the ID of the security group that you created the rules in\.

   ```
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_tcp_rule_id
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_udp_rule_id
   ```

1. From `TerminalB`, attempt to access the application again\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   curl: (6) Could not resolve host: my-app
   ```

   The attempt fails because the Pod is no longer able to access the CoreDNS Pods, which have the cluster security group associated to them\. The cluster security group no longer has the security group rules that allow DNS communication from the security group associated to your Pod\.

   If you attempt to access the application using the IP addresses returned for one of the Pods in a previous step, you still receive a response because all ports are allowed between Pods that have the security group associated to them and a name lookup isn't required\.

1. Once you've finished experimenting, you can remove the sample security group policy, application, and security group that you created\. Run the following commands from `TerminalA`\.

   ```
   kubectl delete namespace my-namespace
   aws ec2 revoke-security-group-ingress --group-id $my_pod_security_group_id --security-group-rule-ids $my_inbound_self_rule_id
   wait
   sleep 45s 
   aws ec2 delete-security-group --group-id $my_pod_security_group_id
   ```