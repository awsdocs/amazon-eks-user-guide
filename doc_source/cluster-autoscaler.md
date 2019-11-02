# Cluster Autoscaler<a name="cluster-autoscaler"></a>

The Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) automatically adjusts the number of nodes in your cluster when pods fail to launch due to lack of resources or when nodes in the cluster are underutilized and their pods can be rescheduled onto other nodes in the cluster\.

This topic shows you how to deploy the Cluster Autoscaler to your Amazon EKS cluster and how to configure it to modify your Amazon EC2 Auto Scaling groups\. The Cluster Autoscaler modifies your worker node groups so that they scale out when you need more resources and scale in when you have underutilized resources\.

## Create an Amazon EKS Cluster<a name="ca-create-cluster"></a>

Create an Amazon EKS cluster with no node groups with the following `eksctl` command\. For more information, see [Creating an Amazon EKS Cluster](create-cluster.md)\. Note the Availability Zones that the cluster is created in\. You will use these Availability Zones when you create your node groups\. Substitute the red variable text with your own values\.

```
eksctl create cluster --name my-cluster --version 1.14 --without-nodegroup
```

Output:

```
[ℹ]  using region us-west-2
[ℹ]  setting availability zones to [us-west-2a us-west-2c us-west-2b]
[ℹ]  subnets for us-west-2a - public:192.168.0.0/19 private:192.168.96.0/19
[ℹ]  subnets for us-west-2c - public:192.168.32.0/19 private:192.168.128.0/19
[ℹ]  subnets for us-west-2b - public:192.168.64.0/19 private:192.168.160.0/19
[ℹ]  using Kubernetes version 1.14
[ℹ]  creating EKS cluster "my-cluster" in "us-west-2" region
[ℹ]  will create a CloudFormation stack for cluster itself and 0 nodegroup stack(s)
[ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=us-west-2 --name=my-cluster'
[ℹ]  CloudWatch logging will not be enabled for cluster "my-cluster" in "us-west-2"
[ℹ]  you can enable it with 'eksctl utils update-cluster-logging --region=us-west-2 --name=my-cluster'
[ℹ]  1 task: { create cluster control plane "my-cluster" }
[ℹ]  building cluster stack "eksctl-my-cluster-cluster"
[ℹ]  deploying stack "eksctl-my-cluster-cluster"
[✔]  all EKS cluster resource for "my-cluster" had been created
[✔]  saved kubeconfig as "/Users/ericn/.kube/config"
[ℹ]  kubectl command should work with "/Users/ericn/.kube/config", try 'kubectl get nodes'
[✔]  EKS cluster "my-cluster" in "us-west-2" region is ready
```

This cluster was created in the following Availability Zones: *us\-west\-2a us\-west\-2c us\-west\-2b*\.

## Create Node Groups for your Cluster<a name="ca-create-ngs"></a>

Create single\-zone node groups for each Availability Zone that your cluster was created in\. For more information, see [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)\.

The Cluster Autoscaler does not support Auto Scaling groups that span multiple Availability Zones\. Instead, use an Auto Scaling group for each Availability Zone\. You can later enable the `--balance-similar-node-groups` feature to keep your cluster's node count relatively even across Availability Zones\. If you do use a single Auto Scaling Group that spans multiple Availability Zones you will find that AWS unexpectedly terminates nodes without them being drained because of the [rebalancing feature of AWS EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html#arch-AutoScalingMultiAZ).

For each Availability Zone in your cluster, use the following `eksctl` command to create a node group\. Substitute the red variable text with your own values\. This command creates an Auto Scaling group with a minimum count of one and a maximum count of ten\.

```
eksctl create nodegroup --cluster my-cluster --node-zones us-west-2a --name us-west-2a --asg-access --nodes-min 1 --nodes-max 10
```

### Node Group IAM Policy<a name="ca-ng-iam-policy"></a>

The Cluster Autoscaler requires the following IAM permissions to make calls to AWS APIs on your behalf\.

If you used the previous `eksctl` command to create your node groups, these permissions are automatically provided and attached to your worker node IAM roles\. If you did not use `eksctl`, you must create an IAM policy with the following document and attach it to your worker node IAM roles\. For more information, see [Modifying a Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_modify.html) in the *IAM User Guide*\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeTags",
                "autoscaling:SetDesiredCapacity",
                "autoscaling:TerminateInstanceInAutoScalingGroup",
                "ec2:DescribeLaunchTemplateVersions"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

### Auto Scaling Group Tags<a name="ca-ng-asg-tags"></a>

The Cluster Autoscaler requires the following tags on your node group Auto Scaling groups so that they can be auto\-discovered\.

If you used the previous `eksctl` command to create your node groups, these tags are automatically applied\. If not, you must manually tag your Auto Scaling groups with the following tags\. For more information, see [Tagging Your Amazon EC2 Resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) in the *Amazon EC2 User Guide for Linux Instances*\.


| Key | Value | 
| --- | --- | 
|  `k8s.io/cluster-autoscaler/<cluster-name>`  |  `owned`  | 
|  `k8s.io/cluster-autoscaler/enabled`  |  `true`  | 

## Deploy the Cluster Autoscaler<a name="ca-deploy"></a>

**To deploy the Cluster Autoscaler**

1. Deploy the Cluster Autoscaler to your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
   ```

1. Add the `cluster-autoscaler.kubernetes.io/safe-to-evict` annotation to the deployment with the following command\.

   ```
   kubectl -n kube-system annotate deployment.apps/cluster-autoscaler cluster-autoscaler.kubernetes.io/safe-to-evict="false"
   ```

1. Edit the Cluster Autoscaler deployment with the following command\.

   ```
   kubectl -n kube-system edit deployment.apps/cluster-autoscaler
   ```

   Edit the `cluster-autoscaler` container command to replace `<YOUR CLUSTER NAME>` with your cluster's name, and add the following options\.
   + *\-\-balance\-similar\-node\-groups*
   + *\-\-skip\-nodes\-with\-system\-pods=false*

   ```
       spec:
         containers:
         - command:
           - ./cluster-autoscaler
           - --v=4
           - --stderrthreshold=info
           - --cloud-provider=aws
           - --skip-nodes-with-local-storage=false
           - --expander=least-waste
           - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<YOUR CLUSTER NAME>
           - --balance-similar-node-groups
           - --skip-nodes-with-system-pods=false
   ```

   Save and close the file to apply the changes\.

1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.14, find the Cluster Autoscaler release that begins with 1\.14\. Record the semantic version number \(1\.14\.*n*\) for that release to use in the next step\.

1. Set the Cluster Autoscaler image tag to the version you recorded in the previous step with the following command\. Replace the red variable text with your own value\.

   ```
   kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=k8s.gcr.io/cluster-autoscaler:v1.14.5
   ```

## View your Cluster Autoscaler Logs<a name="ca-view-logs"></a>

After you have deployed the Cluster Autoscaler, you can view the logs and verify that it is monitoring your cluster load\.

View your Cluster Autoscaler logs with the following command\.

```
kubectl -n kube-system logs deployment.apps/cluster-autoscaler
```

Output:

```
I0926 23:15:55.165842       1 static_autoscaler.go:138] Starting main loop
I0926 23:15:55.166279       1 utils.go:595] No pod using affinity / antiaffinity found in cluster, disabling affinity predicate for this loop
I0926 23:15:55.166293       1 static_autoscaler.go:294] Filtering out schedulables
I0926 23:15:55.166330       1 static_autoscaler.go:311] No schedulable pods
I0926 23:15:55.166338       1 static_autoscaler.go:319] No unschedulable pods
I0926 23:15:55.166345       1 static_autoscaler.go:366] Calculating unneeded nodes
I0926 23:15:55.166357       1 utils.go:552] Skipping ip-192-168-3-111.us-west-2.compute.internal - node group min size reached
I0926 23:15:55.166365       1 utils.go:552] Skipping ip-192-168-71-83.us-west-2.compute.internal - node group min size reached
I0926 23:15:55.166373       1 utils.go:552] Skipping ip-192-168-60-191.us-west-2.compute.internal - node group min size reached
I0926 23:15:55.166435       1 static_autoscaler.go:393] Scale down status: unneededOnly=false lastScaleUpTime=2019-09-26 21:42:40.908059094 ...
I0926 23:15:55.166458       1 static_autoscaler.go:403] Starting scale down
I0926 23:15:55.166488       1 scale_down.go:706] No candidates for scale down
```