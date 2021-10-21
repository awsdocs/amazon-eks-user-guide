# Amazon EKS security best practices<a name="best-practices-security"></a>

This topic provides security best practices for your cluster\.

## Restricting access to the IMDS and Amazon EC2 instance profile credentials<a name="restrict-ec2-credential-access"></a>

By default, the Amazon EC2 [instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) \(IMDS\) provides the credentials assigned to the [node IAM role](create-node-role.md) to the instance, and any container running on the instance\. When you use [IAM roles for service accounts](iam-roles-for-service-accounts.md), it updates the credential chain of the pod to use the IAM roles for service accounts token\. The pod, however, can still inherit the rights of the instance profile assigned to the node\. We recommended that you block pod access to IMDS to minimize the permissions available to your containers if:
+ You’ve implemented IAM roles for service accounts and have assigned necessary permissions directly to all pods that require access to AWS services\.
+ No pods in your cluster require access to IMDS for other reasons, such as retrieving the current Region\. 

For more information, see [Retrieving Security Credentials from Instance Metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#instance-metadata-security-credentials)\. You can prevent access to IMDS from your instance and containers using one of the following options\.

**Important**  
If you use the AWS Load Balancer Controller in your cluster, you may need to change your load balancer configuration\. For more information, see [To deploy the AWS Load Balancer Controller to an Amazon EKS cluster](aws-load-balancer-controller.md#deploy-lb-controller)\.
+ **Block access to IMDSv1 from the node and all containers and block access to IMDSv2 for all containers that don't use host networking** – Your instance and pods that have `hostNetwork: true` in their pod spec use host networking\. To implement this option, complete the steps in the row and column that apply to your situation\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/best-practices-security.html)
+ **Block access to IMDSv1 and IMDSv2 for all containers that don't use host networking** – Your instance and pods that have `hostNetwork: true` in their pod spec use host networking, but for legacy reasons still require access to IMDSv1\. Run the following `iptables` commands on each of your Amazon Linux nodes \(as root\) or include them in your instance bootstrap user data script\.

  ```
  sudo yum install -y iptables-services
  sudo iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP
  sudo iptables-save | tee /etc/sysconfig/iptables 
  sudo systemctl enable --now iptables
  ```
**Important**  
The previous rule applies only to network interfaces within the node that have a name that starts with `eni`, which is all network interfaces that the CNI plugin creates for pods that don't use host networking\. Traffic to the IMDS is not dropped for the node, or for pods that use host networking, such as `kube-proxy` and the CNI plugin\. 
If you implement network policy, using a tool such as [Calico](calico.md), the previous rule may be overridden\. When implementing network policy, ensure that it doesn't override this rule, or that your policy includes this rule\.
If you've applied security groups to pods and therefore, have branch network interfaces, in addition to the previous command, also run the following command\.  

    ```
    iptables -t mangle -A POSTROUTING -o vlan+ --destination 169.254.169.254/32 --jump DROP
    ```
For more information about branch network interfaces, see [Security groups for pods](security-groups-for-pods.md)\.