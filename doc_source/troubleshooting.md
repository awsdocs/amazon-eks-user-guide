# Amazon EKS Troubleshooting<a name="troubleshooting"></a>

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them\.

## Insufficient Capacity<a name="ICE"></a>

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified does not have sufficient capacity to support a cluster\.

`Cannot create cluster 'example-cluster' because us-east-1d, the targeted availability zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these availability zones: us-east-1a, us-east-1b, us-east-1c`

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message\.

## `aws-iam-authenticator` Not Found<a name="no-auth-provider"></a>

If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.

## Worker Nodes Fail to Join Cluster<a name="worker-node-fail"></a>

There are two common reasons that prevent worker nodes from joining the cluster:
+ The `aws-auth-cm.yaml` file does not have the correct IAM role ARN for your worker nodes\. Ensure that the worker node IAM role ARN \(not the instance profile ARN\) is specified in your `aws-auth-cm.yaml` file\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.
+ The **ClusterName** in your worker node AWS CloudFormation template does not exactly match the name of the cluster you want your worker nodes to join\. Passing an incorrect value to this field results in an incorrect configuration of the worker node's `/var/lib/kubelet/kubeconfig` file, and the nodes will not join the cluster\.

## `hostname doesn't match`<a name="python-version"></a>

Your system's Python version must be Python 3, or Python 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.