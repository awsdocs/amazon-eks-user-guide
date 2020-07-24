# Restricting access to Amazon EC2 instance profile credentials<a name="restrict-ec2-credential-access"></a>

By default, all containers that are running on a node have all permissions assigned to the [Amazon EKS node IAM role](worker_node_IAM_role.md) that is attached to the node\. The Amazon EC2 [instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) provides the credentials to any process running on an instance\. For more information, see [Retrieving Security Credentials from Instance Metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#instance-metadata-security-credentials)\. 

When you implement IAM roles for service accounts for a pod, the containers in the pod have all permissions assigned to the service account and the node IAM role\. If you implement IAM roles for service accounts for all pods in a cluster, you may want to prevent the containers in the pods from using the permissions assigned to the node IAM role\. Keep in mind however, that there may be certain key permissions on the node IAM role that pods need to function\. It’s important to properly scope your service account IAM roles so that your pods have all of the necessary permissions\. For example, the node IAM role is assigned permissions to pull container images from Amazon ECR\. If a pod isn't assigned those permissions, then the pod can't pull container images from Amazon ECR\.

To prevent all containers in all pods on a node from using the permissions assigned to the node IAM role \(while still allowing the permissions that are assigned to the service account\), run the following `iptables` commands on your nodes \(as `root`\) or include them in your instance bootstrap user data script\.

**Important**  
These commands completely block **all** containers running on a node from querying the instance metadata service for any metadata, not just the credentials for the node IAM role\. Do not run these commands on nodes that run pods that you haven't implemented IAM roles for service accounts for or none of the containers on the node will have any of the permissions assigned to the node IAM role\.
If you implement network policy, using a tool such as [Calico](calico.md), this rule may be overridden\. When implementing network policy, ensure that it doesn't override this rule, or that your policy includes this rule\.

```
yum install -y iptables-services
iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP
iptables-save | tee /etc/sysconfig/iptables 
systemctl enable --now iptables
```