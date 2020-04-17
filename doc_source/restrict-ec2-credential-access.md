# Restricting access to Amazon EC2 instance profile credentials<a name="restrict-ec2-credential-access"></a>

By default, all containers that are running on a worker node have all permissions assigned to the [Amazon EKS worker node IAM role](worker_node_IAM_role.md) that is attached to the worker node\. The Amazon EC2 [instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) provides the credentials to any process running on an instance\. For more information, see [Retrieving Security Credentials from Instance Metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#instance-metadata-security-credentials)\. 

When you implement IAM roles for service accounts for a pod, the containers in the pod have all permissions assigned to the service account and the worker node IAM role\. If you implement IAM roles for service accounts for all pods in a cluster, you may want to prevent the containers in the pods from using the permissions assigned to the worker node IAM role\. Keep in mind however, that there may be certain key permissions on the worker node IAM role that pods need to function\. It’s important to properly scope your service account IAM roles so that your pods have all of the necessary permissions\. For example, the worker node IAM role is assigned permissions to pull container images from Amazon ECR\. If a pod isn't assigned those permissions, then the pod can't pull container images from Amazon ECR\.

To prevent all containers in all pods on a worker node from using the permissions assigned to the worker node IAM role \(while still allowing the permissions that are assigned to the service account\), run the following `iptables` commands on your worker nodes \(as `root`\) or include them in your instance bootstrap user data script\.

**Important**  
These commands completely block **all** containers running on a worker node from querying the instance metadata service for any metadata, not just the credentials for the worker node IAM role\. Do not run these commands on worker nodes that run pods that you haven't implemented IAM roles for service accounts for or none of the containers on the node will have any of the permissions assigned to the worker node IAM role\.

```
yum install -y iptables-services
iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP
iptables-save | tee /etc/sysconfig/iptables 
systemctl enable --now iptables
```