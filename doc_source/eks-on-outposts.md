# Amazon EKS on AWS Outposts<a name="eks-on-outposts"></a>

You can create and run Amazon EKS nodes on AWS Outposts\. AWS Outposts enables native AWS services, infrastructure, and operating models in on\-premises facilities for low latency, local data processing, and data residency needs\. In AWS Outposts environments, you can use the same AWS APIs, tools, and infrastructure that you use in the AWS Cloud\. For more information about AWS Outposts, see the [AWS Outposts User Guide](https://docs.aws.amazon.com/outposts/latest/userguide/)\.

You can use Amazon EKS to run Kubernetes applications on\-premises with AWS Outposts\. Amazon EKS on AWS Outposts supports extended clusters, with the Kubernetes control plane running in the parent AWS Region, and worker nodes running on AWS Outposts\. The Kubernetes control plane is fully managed by AWS, and you can use the same Amazon EKS APIs, tools, and console to create and run Amazon EKS worker nodes on AWS Outposts\.

![\[Outposts Configuration\]](http://docs.aws.amazon.com/eks/latest/userguide/images/outpost_env.png)

## Prerequisites<a name="eks-outposts-prereq"></a>

 The following are the prerequisites for using Amazon EKS nodes on AWS Outposts:
+ You must have installed and configured an Outpost in your on\-premises data center\. For more information, see [Create an Outpost and order Outpost capacity](https://docs.aws.amazon.com/outposts/latest/userguide/order-outpost-capacity.html) in the AWS Outposts User Guide\.
+ You must have a reliable network connection between your Outpost and its parent AWS Region\. We recommend that you provide highly available, low\-latency connectivity between your Outpost and its parent AWS Region\. For more information, see [Outpost connectivity to the local network](https://docs.aws.amazon.com/outposts/latest/userguide/local-network-connectivity.html) in the AWS Outposts User Guide\. 
+ The AWS Region for the Outpost must support Amazon EKS\. For a list of supported AWS Regions, see [Amazon EKS service endpoints](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the *AWS General Reference*\.

## Outpost considerations<a name="eks-outposts-considerations"></a>

### Architecture<a name="eks-outposts-considerations-architecture"></a>
+ AWS Outposts are available in a variety of form factors including 1U and 2U Outposts servers and 42U Outposts racks\. Amazon EKS is supported on the 42U Outposts racks only\.
+ A single subnet cannot span multiple logical Outposts, and inter\-Outposts traffic must use customer\-owned IP addresses and traverse the local network\. Because of this, it is recommended to run a single Amazon EKS cluster per logical Outpost\.
+ Traffic from Amazon EKS worker nodes running on AWS Outposts to the control plane in an AWS Region stays within your VPC and traverses the service link connection\. You can use private or public connectivity for your service link connection\. For more information about the service link, see [Outposts Connectivity to AWS Regions](https://docs.aws.amazon.com/outposts/latest/userguide/how-outposts-works.html#region-connectivity) in the AWS Outposts User Guide\.
+ If network connectivity between your Outpost and its parent AWS Region is lost, your Amazon EKS worker nodes will continue to run\. However, you cannot create new nodes or perform mutating management actions on existing deployments until connectivity is restored\. The recommended course of action during network disconnects is to attempt to reconnect your AWS Outposts to the parent AWS Region following the [network connectivity checklist](https://docs.aws.amazon.com/outposts/latest/userguide/network-troubleshoot.html)\. In case of instance failures during periods of network disconnect, the instances will not be replaced automatically\. The Amazon EKS Kubernetes control plane runs in the parent AWS Region, and missing kubelet heartbeats can lead to the following:
  + Pods on the AWS Outposts being marked as unhealthy
  + the Node status times out
  + the Pods will be marked for eviction

  For more information, see [Node Controller](https://kubernetes.io/docs/concepts/architecture/nodes/#node-controller) in the Kubernetes documentation\.

### Operational<a name="eks-outposts-considerations-operation"></a>
+  When you create your Amazon EKS cluster, you must use subnets that run in the AWS Region because these are used for the creation of the Amazon EKS Kubernetes control plane\. During cluster creation, do not use subnets that run on your AWS Outposts\. 
+  You can run self\-managed nodes on AWS Outposts only, managed nodes and Fargate are not supported\. When you create a self\-managed node group, you must pass the subnets that exist on your AWS Outposts\. 
+  The Amazon EKS worker nodes’ VPC must be associated with an LGW route table for Services running on the worker nodes to be accessible over the local network\. If you are using customer\-owned IPs, then the subnet in which the worker nodes run must have a route to the LGW\. 
+  IPv6 cannot be used for service link or local network traffic on AWS Outposts\. You shouldn't create your Amazon EKS cluster with the IPv6 IP family if you plan to run Amazon EKS worker nodes on AWS Outposts\. 
+  The Kubernetes components for Amazon EKS worker nodes are pulled from Amazon Elastic Container Registry \(Amazon ECR\) in the parent AWS Region\. When bootstrapping new Amazon EC2 instances to your Amazon EKS cluster, expect an increase in traffic over your service link connection\. 
+  You can use Amazon ECR in the parent AWS Region to host your application container images\. The size of your application container images will affect the service link bandwidth usage and the startup time when deploying new Pods that are not already cached\. If you need to reduce your application deployment time, consider hosting a local container registry or cache for your application container images\. If you have “isolated” subnets that do not have a path to the internet, you must set up [ VPC Endpoints ](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html) for Amazon S3 and Amazon ECR to create Amazon EKS worker nodes on AWS Outposts\. 
+ When creating your Amazon EKS worker nodes, you must use the `gp2` volume type\.

### Application<a name="eks-outposts-considerations-application"></a>
+  With AWS Outposts, you can run some AWS services locally, and you can connect to a broad range of services available in the parent AWS Region\. The locally available AWS services will have lower latency response times compared to those running in the parent AWS Region\. The AWS services that you use in the AWS Region will not be available during periods of network disconnect to the parent AWS Region\. For information on the AWS services available locally, see the [AWS Outposts User Guide ](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html) \. 
+  You can connect to your applications running on Amazon EKS on AWS Outposts over your local network using the normal methods for Kubernetes [ Services ](https://kubernetes.io/docs/concepts/services-networking/service/) and [ Ingress ](https://kubernetes.io/docs/concepts/services-networking/ingress/) \. Application Load Balancer \(ALB\) is available for Kubernetes Ingress on Outposts racks\. Network Load Balancer \(Network Load Balancer\) is not available on AWS Outposts\. A common practice to conserve capacity on AWS Outposts is to use a single ALB deployment with [ path\-based routing ](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#rule-condition-types) for each Kubernetes Service\. For more information, see the [ Application Load Balancer documentation ](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#outposts) \. 
+  Amazon EBS volumes do not span physical or logical AWS Outposts, similar to the multi\-Availability Zone behavior in AWS Regions\. For example, if a Node running on physical Outpost A moves to physical Outpost B, the EBS volume will not move with it\. If you are running stateful workloads on Amazon EKS with Pods backed by EBS volumes, consider implementing dual writes at the application layer or using an alternative storage mechanism if your application and its data must remain available during single\-rack failures\. 

## <a name="eks-outposts-limit"></a>

## Deploy an Amazon EKS cluster with worker nodes on AWS Outposts<a name="eks-outposts-deploy"></a>

This section describes how to create an Amazon EKS cluster and deploy Amazon EKS worker nodes on AWS Outposts using `eksctl` and the AWS CLI\. You must have permissions to create and manage subnets on AWS Outposts\. Click here to learn more about shareable Outpost resources[https://docs.aws.amazon.com/outposts/latest/userguide/sharing-outposts.html#sharing-resources](https://docs.aws.amazon.com/outposts/latest/userguide/sharing-outposts.html#sharing-resources)\.

1. Create a public Amazon EKS cluster using a YAML file:

   ```
   eksctl create cluster -f cluster-config.yaml
   ```

   An example YAML file is shown below:

   ```
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-outposts-cluster
     version: 1.21
     region: us-west-2
     
   cloudWatch:
     clusterLogging:
       enableTypes: [ "api", "audit", "authenticator", "controllerManager", "scheduler" ]
   
   iam:
     withOIDC: true
   
   addons:
     - name: vpc-cni
     - name: coredns
     - name: kube-proxy
   ```

   To create a fully private cluster, add the following to your config YAML file:

   ```
   privateCluster:
     enabled: true
   ```

   Your output should looks similar to this:

   ```
   eksctl version 0.80.0
   using region us-west-2
   subnets for us-west-2a - public:192.168.0.0/19 private:192.168.96.0/19
   subnets for us-west-2b - public:192.168.32.0/19 private:192.168.128.0/19
   subnets for us-west-2c - public:192.168.64.0/19 private:192.168.160.0/19
   using Kubernetes version 1.21
   creating EKS cluster "my-outpost-cluster" in "us-west-2" region with
   if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks —region=us-west-2 —cluster=my-outpost-cluster’
   Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "my-outpost-cluster" in "us-west-2"
   CloudWatch logging will not be enabled for cluster "my-outpost-cluster" in "us-west-2"
   you can enable it with 'eksctl utils update-cluster-logging —enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} —region=us-west-2 —cluster=my-outpost-cluster’
   2 sequential tasks: { create cluster control plane "my-outpost-cluster", wait for control plane to become ready
   }
   building cluster stack "eksctl-my-outpost-cluster-cluster"
   deploying stack "eksctl-my-outpost-cluster-cluster"
   waiting for CloudFormation stack "eksctl-my-outpost-cluster-cluster"
   waiting for CloudFormation stack "eksctl-my-outpost-cluster-cluster"...
   
   waiting for the control plane availability...
   saved kubeconfig as "../.kube/config"
   no tasks
   all EKS cluster resources for "my-outpost-cluster" have been created
   kubectl command should work with "../.kube/config", try 'kubectl get nodes'
   EKS cluster "my-outpost-cluster" in "us-west-2" region is ready
   ```

   You can confirm your cluster has been created in the Amazon EKS AWS Management Console or the command:

   ```
   eksctl get cluster —name my-outposts-cluster
   ```

1. Identify the VPC created with your new cluster\. This VPC will host the subnet that contains your worker nodes\. You can find your `vpc-id` with the command:

   ```
   eksctl get cluster --name my-outposts-cluster
   ```

1. Identify the subnet and CIDR for your Outpost\. The CIDR shouldn't conflict with other IP addresses in use on your local network\. This can be done by using a [subnet calculator](https://www.site24x7.com/tools/ipv4-subnetcalculator.html) and determining the appropriate settings for your environment\. Once you have calculated the CIDR, you can use this value in the next step\. Your `availability-zone` is visible in the AWS Management Console\.

1. Create a subnet on AWS Outposts using AWS CLI to host your worker nodes\. Use the `vpc-id` that you retrieved in the previous step in the following command:

   ```
   aws ec2 create-subnet \ 
       --region us-west-2 \ 
       --availability-zone us-west-2 \ 
       --outpost-arn your-outpost-arn\ 
       --vpc-id your-vpc-id \ 
       --cidr-block your-cidr-block
   ```

   Note the subnet id that appears in the message after creation\.

   Your output should look similar to this:

   ```
   {
   "Subnet": {
   "AvailabilityZone": "us-west-2b",
   "AvailabilityZoneId": "usw2-az1",
   "AvailableIpAddressCount": 11,
   "CidrBlock": "192.168.192.0/28",
   "DefaultForAz": false,
   "MapPublicIpOnLaunch": false,
   "State": "available",
   "SubnetId": "subnet-042e2c531a5713a5b",
   "VpcId": "vpc-08edbe538f4045578",
   "OwnerId": "[user-arn]",
   "AssignIpv6AddressOnCreation": false,
   "Ipv6CidrBlockAssociationSet": [],
   "SubnetArn": "arn:aws:ec2:us-west-2:[user-arn]:subnet/subnet-042e2c531a5713a5b",
   "OutpostArn": "arn:aws:outposts:us-west-2:[user-arn]:outpost/op-039eded540aa85d85",
   "EnableDns64": false,
   "Ipv6Native": false,
   "PrivateDnsNameOptionsOnLaunch": {
   "HostnameType": "ip-name",
   "EnableResourceNameDnsARecord": false,
   "EnableResourceNameDnsAAAARecord": false
   }
   }
   }
   ```

   You can verify the subnet creation in the AWS Management Console under your cluster details\.

1. Create worker nodes by using a YAML file\. Replace the `vpc-id` with the value created in step 1 and `subnet-id` created in step 2\. The `security-group-id` was created in step 1 and can be retrieved with the command:

   ```
   eksctl get cluster --name my-outposts-cluster
   ```

   The nodes can be created with a YAML file by using the command:

   ```
   eksctl create nodegroup -f worker-nodes-config.yaml
   ```

   The following is an example YAML file to include in this step\. For `instanceType`, select the instance size that is:
   + slotted on your Outpost
   + available for your workload

   ```
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-outposts-cluster
     region: us-west-2
   
   nodeGroups:
     - name: outpost-worker-nodes
       instanceType: m5.large
       desiredCapacity: 1
       minSize: 1
       maxSize: 1
       volumeSize: 50
       volumeType: gp2
       volumeEncrypted: true
       subnets:
         - subnet-042e2c531a5713a5b
       privateNetworking: true
   ```

   To create private worker nodes, add this to the end of the YAML file:

   ```
   subnets:
         - outpost-subnet
       volumeType: gp2
       privateNetworking: true
   ```

   Your output should look similar to this:

   ```
   all nodegroups have up-to-date cloudformation templates
   eksctl version 0.80.0
   using region us-west-2
   will use version 1.21 for new nodegroup(s) based on control plane version
   nodegroup "outpost-worker-nodes" will use "ami-085e8e02353a59de5" [AmazonLinux2/1.21]1 nodegroup (outpost-worker-nodes) was included (based on the include/exclude rules)
   will create a CloudFormation stack for each of 1 nodegroups in cluster "my-outpost-cluster"
   2 sequential tasks: { fix cluster compatibility, 1 task: { 1 task: { create nodegroup "outpost-worker-nodes" } }
   }
   checking cluster stack for missing resources
   cluster stack has all required resources
   building nodegroup stack "eksctl-my-outpost-cluster-nodegroup-outpost-worker-nodes"
   deploying stack "eksctl-my-outpost-cluster-nodegroup-outpost-worker-nodes"
   waiting for CloudFormation stack "eksctl-my-outpost-cluster-nodegroup-outpost-worker-nodes"
   waiting for CloudFormation stack "eksctl-my-outpost-cluster-nodegroup-outpost-worker-nodes"...
   no tasks
   adding identity "arn:aws:iam::601017151385:role/eksctl-my-outpost-cluster-nodegro-NodeInstanceRole-LHYFK4K4DV85" to auth ConfigMap
   nodegroup "outpost-worker-nodes" has 0 node(s)
   waiting for at least 1 node(s) to become ready in "outpost-worker-nodes"
   nodegroup "outpost-worker-nodes" has 2 node(s)
   node "ip-192-168-192-5.us-west-2.compute.internal" is not ready
   node "ip-192-168-192-9.us-west-2.compute.internal" is ready
   created 1 nodegroup(s) in cluster "my-outpost-cluster"
   created 0 managed nodegroup(s) in cluster "my-outpost-cluster"
   checking security group configuration for all nodegroups
   ```

1. \(Optional\) To expose worker nodes over your local network, see [How local gateways work](https://docs.aws.amazon.com/outposts/latest/userguide/how-racks-work.html#local-gateway)\.

Now that you have a configured Amazon EKS cluster with worker nodes running on AWS Outposts, you can install add\-ons and deploying applications to your cluster\. See the following for more information on how to extend your cluster's functionality:
+ The IAM entity \(user or role\) that created the cluster is the only IAM user that can make calls to the API server using `kubectl`\. To grant access to other useres or roles, see [Apply the `aws-auth``ConfigMap` to your cluster](add-user-role.md#aws-auth-configmap)\.
+ [Deploy a sample application](sample-deployment.md) to your cluster\.
+ Learn about important [Cluster management](eks-managing.md) tools\.
+ [Deploy a containerized application on AWS Outposts](http://aws.amazon.com/blogs/containers/deploying-containerized-application-on-aws-outposts-with-amazon-eks/)\.
+ [Build a modern application on AWS Outposts with Terraform examples](http://aws.amazon.com/blogs/compute/building-modern-applications-with-amazon-eks-on-amazon-outposts/)\.