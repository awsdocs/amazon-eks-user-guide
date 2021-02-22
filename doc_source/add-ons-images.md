# Amazon EKS add\-on container image addresses<a name="add-ons-images"></a>

When you deploy Amazon EKS add\-ons such as the [AWS Load Balancer Controller](aws-load-balancer-controller.md), the [VPC CNI plug\-in](pod-networking.md), [kube\-proxy](update-cluster.md#update-existing-cluster), [CoreDNS](coredns.md), or [storage drivers](storage.md), you pull an image from an Amazon ECR repository\. The image name and tag are listed in the topics for each add\-on\.

The following table contains a list of Regions and the addresses you can use to pull images from\. 


| Region | Address | 
| --- | --- | 
| us\-gov\-west\-1 |  013241004608\.dkr\.ecr\.us\-gov\-west\-1\.amazonaws\.com/ | 
| us\-gov\-east\-1 | 151742754352\.dkr\.ecr\.us\-gov\-east\-1\.amazonaws\.com/ | 
| me\-south\-1 | 558608220178\.dkr\.ecr\.me\-south\-1\.amazonaws\.com/ | 
| eu\-south\-1 | 590381155156\.dkr\.ecr\.eu\-south\-1\.amazonaws\.com/ | 
| ap\-east\-1 | 800184023465\.dkr\.ecr\.ap\-east\-1\.amazonaws\.com/ | 
| af\-south\-1 | 877085696533\.dkr\.ecr\.af\-south\-1\.amazonaws\.com/ | 
| cn\-north\-1 | 918309763551\.dkr\.ecr\.cn\-north\-1\.amazonaws\.com\.cn/ | 
| cn\-northwest\-1 | 961992271922\.dkr\.ecr\.cn\-northwest\-1\.amazonaws\.com\.cn/ | 

For all Regions not listed in the previous table, you can use the following address and replace *us\-west\-2* with your Region code\.

```
602401143452.dkr.ecr.us-west-2.amazonaws.com/
```