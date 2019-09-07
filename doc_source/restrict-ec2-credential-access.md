# Restricting Access to Amazon EC2 Instance Profile Credentials<a name="restrict-ec2-credential-access"></a>

By default, containers that are running on your worker nodes are not prevented from accessing the credentials that are supplied to the worker node's instance profile through the Amazon EC2 instance metadata server\. This section helps you to block pod access to Amazon EC2 instance profile credentials\.

To prevent containers in pods from accessing the credential information supplied to the worker node instance profile \(while still allowing the permissions that are provided by the service account\) by running the following `iptables` commands on your worker nodes \(as `root`\) or include them in your instance bootstrap user data script\.

**Important**  
These commands block ALL containers from using the instance profile credentials\. 

```
yum install -y iptables-services
iptables --insert FORWARD 1 --in-interface eni+ --destination 169.254.169.254/32 --jump DROP
iptables-save | tee /etc/sysconfig/iptables 
systemctl enable --now iptables
```