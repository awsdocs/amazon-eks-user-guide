# Grant IAM users access to Kubernetes with EKS access entries<a name="access-entries"></a>

**Prerequisites**
+ Familiarity with cluster access options for your Amazon EKS cluster\. For more information, see [Grant IAM users and roles access to Kubernetes APIs](grant-k8s-access.md)\.
+ An existing Amazon EKS cluster\. To deploy one, see [Get started with Amazon EKS](getting-started.md)\. To use *access entries* and change the authentication mode of a cluster, the cluster must have a platform version that is the same or later than the version listed in the following table, or a Kubernetes version that is later than the versions listed in the table\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)

  You can check your current Kubernetes and platform version by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **aws eks describe\-cluster \-\-name *my\-cluster* \-\-query 'cluster\.\{"Kubernetes Version": version, "Platform Version": platformVersion\}'**\.
**Important**  
After Amazon EKS updates your cluster to the platform version listed in the table, Amazon EKS creates an access entry with administrator permissions to the cluster for the IAM principal that originally created the cluster\. If you don't want that IAM principal to have administrator permissions to the cluster, remove the access entry that Amazon EKS created\.  
For clusters with platform versions that are earlier than those listed in the previous table, the cluster creator is always a cluster administrator\. It's not possible to remove cluster administrator permissions from the IAM user or role that created the cluster\.
+ An IAM principal with the following permissions for your cluster: `CreateAccessEntry`, `ListAccessEntries`, `DescribeAccessEntry`, `DeleteAccessEntry`, and `UpdateAccessEntry`\. For more information about Amazon EKS permissions, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.
+ An existing IAM principal to create an access entry for, or an existing access entry to update or delete\.