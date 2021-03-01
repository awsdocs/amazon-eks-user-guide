# Resilience in Amazon EKS<a name="disaster-recovery-resiliency"></a>

The AWS global infrastructure is built around AWS Regions and Availability Zones\. AWS Regions provide multiple physically separated and isolated Availability Zones, which are connected with low\-latency, high\-throughput, and highly redundant networking\. With Availability Zones, you can design and operate applications and databases that automatically fail over between Availability Zones without interruption\. Availability Zones are more highly available, fault tolerant, and scalable than traditional single or multiple data center infrastructures\. 

Amazon EKS runs and scales the Kubernetes control plane across multiple AWS Availability Zones to ensure high availability\. Amazon EKS automatically scales control plane instances based on load, detects and replaces unhealthy control plane instances, and it provides automated version updates and patching for them\.

This control plane consists of at least two API server instances and three `etcd` instances that run across three Availability Zones within a Region\. Amazon EKS:
+ Actively monitors the load on control plane instances and automatically scales them to ensure high performance\.
+ Automatically detects and replaces unhealthy control plane instances, restarting them across the Availability Zones within the Region as needed\.
+ Leverages the architecture of AWS Regions in order to maintain high availability\. Because of this, Amazon EKS is able to offer an [SLA for API server endpoint availability](http://aws.amazon.com/eks/sla)\.

For more information about AWS Regions and Availability Zones, see [AWS global infrastructure](http://aws.amazon.com/about-aws/global-infrastructure/)\.