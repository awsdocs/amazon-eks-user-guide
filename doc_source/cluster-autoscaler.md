# Cluster Autoscaler<a name="cluster-autoscaler"></a>

The Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) automatically adjusts the number of nodes in your cluster when pods fail or are rescheduled onto other nodes\. That is, the AWS Cloud Provider implementation within the Kubernetes Cluster Autoscaler controls the `.DesiredReplicas` field of Amazon EC2 Auto Scaling groups\. The Cluster Autoscaler is typically installed as a [Deployment](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/cloudprovider/aws/examples) in your cluster\. It uses [leader election](https://en.wikipedia.org/wiki/Leader_election) to ensure high availability, but scaling is one done by a single replica at a time\.

Before you deploy the Cluster Autoscaler, it's important to understand how Kubernetes concepts relate to AWS features\. The following terms are used throughout this topic:
+ **Kubernetes Cluster Autoscaler – **A core component of the Kubernetes control plane that makes scheduling and scaling decisions\. For more information, see [Kubernetes Control Plane FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) on GitHub\.
+ **AWS Cloud provider implementation – **An extension of the Kubernetes Cluster Autoscaler that implements the decisions of the Kubernetes Cluster Autoscaler by communicating with the AWS platform \(for example Amazon EC2\)\. For more information, see [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md) on GitHub\.
+ **Node groups** – A Kubernetes abstraction for a group of nodes within a cluster\. Node groups aren't a true Kubernetes resource, but they do exist as an abstraction in the Cluster Autoscaler, Cluster API, and other components\. Nodes that exist within a single node group might share several properties like labels and taints\. However, they can still consist of multiple Availability Zones or instance types\.
+ **Amazon EC2 Auto Scaling groups** – A feature of AWS that is used by the Cluster Autoscaler\. Auto Scaling groups are suitable for a large number of use cases\. Amazon EC2 Auto Scaling groups are configured to launch instances that automatically join their Kubernetes cluster\. They also apply labels and taints to their corresponding node resource in the Kubernetes API\.

For reference, [Managed node groups](managed-node-groups.md) are implemented using Amazon EC2 Auto Scaling groups, and are compatible with the Cluster Autoscaler\.

This topic shows how you can deploy the Cluster Autoscaler to your Amazon EKS cluster and configure it to modify your Amazon EC2 Auto Scaling groups\.

## Prerequisites<a name="ca-prerequisites"></a>

Before deploying the Cluster Autoscaler, you must meet the following prerequisites\.
+ Have an existing Kubernetes cluster – If you don’t have a cluster, see [Creating an Amazon EKS cluster](create-cluster.md)\.
+ An existing IAM OIDC provider for your cluster\. To determine whether you have one, or to create one if you don't, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Node groups with Auto Scaling groups tags – The Cluster Autoscaler requires the following tags on your Auto Scaling groups so that they can be auto\-discovered\. If you used `eksctl` to create your node groups, these tags are automatically applied\. If you didn't use `eksctl` to create your node groups, then you must manually tag your Auto Scaling groups with the following tags\. For more information, see [Tagging your Amazon EC2 resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) in the Amazon EC2 User Guide for Linux Instances\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cluster-autoscaler.html)

## Create an IAM policy and role<a name="ca-create-policy"></a>

Create an IAM policy that grants the permissions that the Cluster Autoscaler requires to an IAM role\. Replace the `<example-values>` \(including `<>`\) with your own values throughout the procedures\.

1. Create an IAM policy\.

   1. Save the following contents to a file named `cluster-autoscaler-policy.json`\. If your existing node groups were created with `eksctl` and you used the `--asg-access` option, then this policy already exists and you can skip to step 2\. 

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

   1. Create the policy with the following command\. You can change the value for `policy-name`\.

      ```
      aws iam create-policy \
          --policy-name AmazonEKSClusterAutoscalerPolicy \
          --policy-document file://cluster-autoscaler-policy.json
      ```

      Note the ARN returned in the output for use in a later step\.

1. You can create an IAM role and attach an IAM policy to it using `eksctl` or the AWS Management Console\. Select the tab with the name of the tool that you'd like to create the role with\.

------
#### [ eksctl ]

   1. Run the following command if you created your cluster with `eksctl`\. If you created your node groups using the `--asg-access` option, then replace `<AmazonEKSClusterAutoscalerPolicy>` with the name of the IAM policy that `eksctl` created for you\. The policy name is similar to `eksctl-<cluster-name>-nodegroup-ng-<xxxxxxxx>-PolicyAutoScaling`\.

      ```
      eksctl create iamserviceaccount \
        --cluster=<my-cluster> \
        --namespace=kube-system \
        --name=cluster-autoscaler \
        --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/<AmazonEKSClusterAutoscalerPolicy> \
        --override-existing-serviceaccounts \
        --approve
      ```

   1. If you created your node groups using the `--asg-access` option, we recommend that you detach the IAM policy that `eksctl` created and attached to the [Amazon EKS node IAM role](create-node-role.md) that `eksctl` created for your node groups\. Detaching the policy from the node IAM role enables the Cluster Autoscaler to function properly, but doesn't give other pods on your nodes the permissions in the policy\. For more information, see [Removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#remove-policies-console) in the Amazon EC2 User Guide for Linux Instances\.

------
#### [ AWS Management Console ]

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the navigation panel, choose **Roles**, **Create Role**\.

   1. In the **Select type of trusted entity** section, choose **Web identity**\.

   1. In the **Choose a web identity provider** section:

      1. For **Identity provider**, choose the URL for your cluster\.

      1. For **Audience**, choose `sts.amazonaws.com`\.

   1. Choose **Next: Permissions**\.

   1. In the **Attach Policy** section, select the `AmazonEKSClusterAutoscalerPolicy` policy that you created in step 1 to use for your service account\.

   1. Choose **Next: Tags**\.

   1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

   1. For **Role Name**, enter a name for your role, such as `AmazonEKSClusterAutoscalerRole`, and then choose **Create Role**\.

   1. After the role is created, choose the role in the console to open it for editing\.

   1. Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\.

   1. Find the line that looks similar to the following:

      ```
      "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
      ```

      Change the line to look like the following line\. Replace `<EXAMPLED539D4633E53DE1B716D3041E>` \(including `<>`\)with your cluster's OIDC provider ID and replace <region\-code> with the Region code that your cluster is in\.

      ```
      "oidc.eks.<region-code>.amazonaws.com/id/<EXAMPLED539D4633E53DE1B716D3041E>:sub": "system:serviceaccount:kube-system:cluster-autoscaler"
      ```

   1. Choose **Update Trust Policy** to finish\.

------

## Deploy the Cluster Autoscaler<a name="ca-deploy"></a>

Complete the following steps to deploy the Cluster Autoscaler\. We recommend you review [Deployment considerations](#ca-deployment-considerations) and optimize the Cluster Autoscaler deployment before you deploy it to a production cluster\.

**To deploy the Cluster Autoscaler**

1. Deploy the Cluster Autoscaler\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
   ```

1. Annotate the `cluster-autoscaler` service account with the ARN of the IAM role that you created previously\. Replace the *<example values>* with your own values\. 

   ```
   kubectl annotate serviceaccount cluster-autoscaler \
     -n kube-system \
     eks.amazonaws.com/role-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:role/<AmazonEKSClusterAutoscalerRole>
   ```

1. Patch the deployment to add the `cluster-autoscaler.kubernetes.io/safe-to-evict` annotation to the Cluster Autoscaler pods with the following command\.

   ```
   kubectl patch deployment cluster-autoscaler \
     -n kube-system \
     -p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict": "false"}}}}}'
   ```

1. Edit the Cluster Autoscaler deployment with the following command\.

   ```
   kubectl -n kube-system edit deployment.apps/cluster-autoscaler
   ```

   Edit the `cluster-autoscaler` container command to replace `<YOUR CLUSTER NAME>` \(including *`<>`*\) with your cluster's name, and add the following options\.
   + `--balance-similar-node-groups`
   + `--skip-nodes-with-system-pods=false`

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

1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page from GitHub in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.19, find the latest Cluster Autoscaler release that begins with 1\.19\. Record the semantic version number \(`1.19.n`\) for that release to use in the next step\.

1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. Replace *`1.19.n`* with your own value\.

   ```
   kubectl set image deployment cluster-autoscaler \
     -n kube-system \
     cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v<1.19.n>
   ```

## View your Cluster Autoscaler logs<a name="ca-view-logs"></a>

After you have deployed the Cluster Autoscaler, you can view the logs and verify that it is monitoring your cluster load\.

View your Cluster Autoscaler logs with the following command\.

```
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
```

Output:

```
I0926 23:15:55.165842       1 static_autoscaler.go:138] Starting main loop
I0926 23:15:55.166279       1 utils.go:595] No pod using affinity / antiaffinity found in cluster, disabling affinity predicate for this loop
I0926 23:15:55.166293       1 static_autoscaler.go:294] Filtering out schedulables
I0926 23:15:55.166330       1 static_autoscaler.go:311] No schedulable pods
I0926 23:15:55.166338       1 static_autoscaler.go:319] No unschedulable pods
I0926 23:15:55.166345       1 static_autoscaler.go:366] Calculating unneeded nodes
I0926 23:15:55.166357       1 utils.go:552] Skipping ip-192-168-3-111.<region-code>.compute.internal - node group min size reached
I0926 23:15:55.166365       1 utils.go:552] Skipping ip-192-168-71-83.<region-code>.compute.internal - node group min size reached
I0926 23:15:55.166373       1 utils.go:552] Skipping ip-192-168-60-191.<region-code>.compute.internal - node group min size reached
I0926 23:15:55.166435       1 static_autoscaler.go:393] Scale down status: unneededOnly=false lastScaleUpTime=2019-09-26 21:42:40.908059094 ...
I0926 23:15:55.166458       1 static_autoscaler.go:403] Starting scale down
I0926 23:15:55.166488       1 scale_down.go:706] No candidates for scale down
```

## Deployment considerations<a name="ca-deployment-considerations"></a>

Review the following considerations to optimize your Cluster Autoscaler deployment\.

### Scaling considerations<a name="ca-considerations-scaling"></a>

The Cluster Autoscaler can be configured to consider additional features of your nodes\. These features may include Amazon EBS volumes attached to nodes, Amazon EC2 instance types of nodes, and GPU accelerators\. 

**Availability Zones**  
We recommend that you configure multiple node groups, scope each group to a single Availability Zone, and enable the `--balance-similar-node-groups` feature\. Otherwise, if you only create one node group, you can scope that node group to span over multiple Availability Zones\.

**Node group composition**  
The Cluster Autoscaler makes assumptions about how you are using node groups, such as which instance types you use within a group\. To align with these assumptions, it's important to configure your node group based on these considerations: 
+ Each node in a node group has identical scheduling properties, such as labels, taints, and resources\.
  + For `MixedInstancePolicies`, the instance types must be of the same shape for CPU, memory, and GPU\.
  + The first instance type specified in the policy simulates scheduling\.
  + If your policy has additional instance types with more resources, resources may be wasted after scale out\.
  + If your policy has additional instance types with fewer resources than the original instance types, pods may fail to schedule on the instances\.
+ We recommend that you configure a smaller number of node groups with a larger number of nodes, rather than the opposite\. This is because the opposite configuration negatively affects scalability\.
+ We recommend that you use Amazon EC2 features whenever both systems provide support\. \(For example, use Regions and `MixedInstancePolicy`\.\)

If possible, we recommend that you use [Managed node groups](managed-node-groups.md)\. Managed node groups come with powerful management features, including features for Cluster Autoscaler like automatic Amazon EC2 Auto Scaling group discovery and graceful node termination\.

**EBS volumes**  
Persistent storage is critical for building stateful applications, such as databases and distributed caches\. With Amazon EBS volumes, you can build stateful applications on Kubernetes, but you are limited to doing this within a specific zone\. For more information, see [How do I use persistent storage in Amazon EKS?](https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/)\. Stateful applications can be highly available if sharded \(split\) across multiple Availability Zones using a separate Amazon EBS volume for each Availability Zone\. As such, the Cluster Autoscaler can balance the scaling of the Amazon EC2 Auto Scaling groups\. To do this, make sure that the following conditions are met\. 
+ Node group balancing is enabled by setting `balance-similar-node-groups=true`\.
+ Node groups are configured with identical settings except for different Availability Zones and Amazon EBS volumes\.

**Co\-scheduling**  
Machine learning distributed training jobs benefit significantly from the minimized latency of same\-zone node configurations\. These workloads deploy multiple pods to a specific zone\. This can be achieved by setting pod affinity for all co\-scheduled pods or node affinity using `topologyKey: failure-domain.beta.kubernetes.io/zone`\. Based on this configuration, the Cluster Autoscaler scales out a specific zone to match demands\. You might want to allocate multiple Amazon EC2 Auto Scaling groups, with one for each Availability Zone to enable failover for the entire co\-scheduled workload\. Make sure that the following conditions are met\.
+ Node group balancing is enabled by setting `balance-similar-node-groups=false.`
+ [Node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity), [pod preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/), or both are used when clusters include both Regional and Zonal node groups\.
  + Use [Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) to force or encourage regional pods and avoid zonal node groups\.
  + If zonal pods schedule onto regional node groups, this results in imbalanced capacity for your regional pods\.
  + If your zonal workloads can tolerate disruption and relocation, configure [pod preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) to enable regionally scaled pods to force preemption and rescheduling on a less contested zone\.

**Accelerators and GPUs**  
Some clusters take advantage of specialized hardware accelerators such as a dedicated GPU\. When scaling out, the accelerator device plugin can take several minutes to advertise the resource to the cluster\. During this time, the Cluster Autoscaler simulates that this node has the accelerator\. However, until the accelerator becomes ready and updates the node’s available resources, pending pods can't be scheduled on the node\. This can result in [repeated unnecessary scale out](https://github.com/kubernetes/kubernetes/issues/54959)\.

Nodes with accelerators and high CPU or memory utilization aren't considered for scale down even if the accelerator is unused\. However, this can be expensive\. To avoid these costs, the Cluster Autoscaler can apply special rules to consider nodes for scale down if they have unoccupied accelerators\.

To ensure the correct behavior for these cases, you can configure the `kubelet` on your accelerator nodes to label the node before it joins the cluster\. The Cluster Autoscaler uses this label selector to invoke the accelerator optimized behavior\. Make sure that the following conditions are met\. 
+ The `kubelet `for GPU nodes is configured with `--node-labels k8s.amazonaws.com/accelerator=$ACCELERATOR_TYPE`\.
+ Nodes with accelerators adhere to the identical scheduling properties rule\.

**Scaling from zero**  
Cluster Autoscaler can scale node groups to and from zero, which can yield significant cost savings\. It detects the CPU, memory, and GPU resources of an Auto Scaling group by inspecting the `InstanceType` that is specified in its `LaunchConfiguration` or `LaunchTemplate`\. Some pods require additional resources such as `WindowsENI` or `PrivateIPv4Address` or specific `NodeSelectors` or `Taints`, which can't be discovered from the `LaunchConfiguration`\. The Cluster Autoscaler can account for these factors by discovering them from the following tags on the Auto Scaling group\. 

```
Key: k8s.io/cluster-autoscaler/node-template/resources/$RESOURCE_NAME
Value: 5
Key: k8s.io/cluster-autoscaler/node-template/label/$LABEL_KEY
Value: $LABEL_VALUE
Key: k8s.io/cluster-autoscaler/node-template/taint/$TAINT_KEY
Value: NoSchedule
```

**Note**  
When scaling to zero, your capacity is returned to Amazon EC2 and may be unavailable in the future\.

**Additional configuration parameters**  
There are many configuration options that can be used to tune the behavior and performance of the Cluster Autoscaler\. For a complete list of parameters, see [What are the parameters to CA?](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-the-parameters-to-ca) on GitHub\.

### Performance considerations<a name="considerations-performance"></a>

The primary items that you can change to tune the performance and scalability of the Cluster Autoscaler are the resources provided to the process, the scan interval of the algorithm, and the number of node groups in the cluster\. There are other factors involved in the true runtime complexity of this algorithm, such as scheduling plug\-in complexity and the number of pods\. These are considered to be unconfigurable parameters, because they are natural to the cluster’s workload and can't easily be tuned\.

*Scalability* refers to how well the Cluster Autoscaler performs as the number of pods and nodes in your Kubernetes cluster increases\. If scalability limits are reached, the Cluster Autoscaler’s performance and functionality degrades\. Additionally, when it exceeds its scalability limits, the Cluster Autoscaler can no longer add or remove nodes in your cluster\.

*Performance* refers to how quickly the Cluster Autoscaler can make and implement scaling decisions\. A perfectly performing Cluster Autoscaler instantly make decisions and invoke scaling actions in response to stimuli, such as a pod becoming unschedulable\.

Familiarizing yourself with the autoscaling algorithm’s runtime complexity makes tuning the Cluster Autoscaler to continue operating smoothly in large clusters \(with more than [1,000 nodes](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/scalability_tests.md)\) easier\.

The Cluster Autoscaler loads the entire cluster’s state into memory, including pods, nodes, and node groups\. On each scan interval, the algorithm identifies unschedulable pods and simulates scheduling for each node group\. Tuning these factors come with different tradeoffs, which should be carefully considered\.

**Vertical autoscaling**  
The simplest way to scale the Cluster Autoscaler to larger clusters is to increase the resource requests for its deployment\. Both memory and CPU should be increased for large clusters, though this varies significantly with cluster size\. The autoscaling algorithm stores all pods and nodes in memory\. This can result in a memory footprint larger than a gigabyte in some cases\. Increasing resources is typically done manually\. If you find that constant resource tuning is creating an operational burden, consider using the [Addon Resizer](https://github.com/kubernetes/autoscaler/tree/master/addon-resizer) or [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)\.

**Reducing the number of node groups**  
Minimizing the number of node groups is one way to ensure that the Cluster Autoscaler performs well on large clusters\. This may be challenging if you structure your node groups on an individual team or application basis\. Even though this is fully supported by the Kubernetes API, this is considered to be a Cluster Autoscaler anti\-pattern with repercussions for scalability\. There are many reasons to use multiple node groups, such as Spot or GPU instances\. In many cases, there are alternative designs that achieve the same effect while using a small number of groups\. Make sure that the following conditions are met\. 
+ Pod isolation is done using namespaces rather than node groups\.
  + This may not be possible in low\-trust multi\-tenant clusters\.
  + Pod `ResourceRequests` and `ResourceLimits` are properly set to avoid resource contention\.
  + Larger instance types result in more optimal bin packing and reduced system pod overhead\.
+ `NodeTaints` or `NodeSelectors` are used to schedule pods as the exception, not as the rule\.
+ Regional resources are defined as a single Amazon EC2 Auto Scaling group with multiple Availability Zones\.

**Reducing the scan interval**  
A low scan interval, such as ten seconds, ensures that the Cluster Autoscaler responds as quickly as possible when pods become unschedulable\. However, each scan results in many API calls to the Kubernetes API and Amazon EC2 Auto Scaling group or the Amazon EKS managed node group APIs\. These API calls can result in rate limiting or even service unavailability for your Kubernetes control plane\.

The default scan interval is ten seconds, but on AWS, launching a node takes significantly longer to launch a new instance\. This means that it’s possible to increase the interval without significantly increasing overall scale up time\. For example, if it takes two minutes to launch a node, changing the interval to one minute results in a trade\-off of 6x reduced API calls for 38% slower scale ups\.

**Sharding across node groups**  
The Cluster Autoscaler can be configured to operate on a specific set of node groups\. Using this functionality, it’s possible to deploy multiple instances of the Cluster Autoscaler, each configured to operate on a different set of node groups\. When you use this strategy, you can use arbitrarily large numbers of node groups, trading cost for scalability\. However, we only recommend using this strategy as a last resort for improving performance\.

The Cluster Autoscaler wasn't originally designed for this configuration, so there are some side effects\. Because the shards don't communicate, it’s possible for multiple autoscalers to attempt to schedule an unschedulable pod\. This can result in unnecessary scale out of multiple node groups\. The extra nodes scale back in after the `scale-down-delay`\.

```
metadata:
  name: cluster-autoscaler
  namespace: cluster-autoscaler-1

...

--nodes=1:10:k8s-worker-asg-1
--nodes=1:10:k8s-worker-asg-2

---

metadata:
  name: cluster-autoscaler
  namespace: cluster-autoscaler-2

...

--nodes=1:10:k8s-worker-asg-3
--nodes=1:10:k8s-worker-asg-4
```

Make sure that the following conditions are true\.
+ Each shard is configured to point to a unique set of Amazon EC2 Auto Scaling groups\.
+ Each shard is deployed to a separate namespace to avoid leader election conflicts\.

### Cost efficiency and availability<a name="considerations-cost-efficiency"></a>

The primary options for tuning the cost efficiency of the Cluster Autoscaler are related to provisioning Amazon EC2 instances\. Additionally, cost efficiency must be balanced with availability\. This section describes strategies like using Spot instances to reduce costs and overprovisioning to reduce latency when creating new nodes\.
+ **Availability** – Pods can be scheduled quickly and without disruption\. This is true even for when newly created pods need to be scheduled and for when a scaled down node terminates any remaining pods scheduled to it\.
+ **Cost** – Determined by the decision behind scale\-out and scale\-in events\. Resources are wasted if an existing node is underutilized or if a new node is added that is too large for incoming pods\. Depending on the specific use case, there can be costs associated with prematurely terminating pods due to an aggressive scale down decision\.

**Spot instances**  
You can use Spot Instances in your node groups and save up to 90% off the on\-demand price\. This has the trade\-off of Spot Instances possibly being interrupted at any time when Amazon EC2 needs the capacity back\. `Insufficient Capacity Errors` occur whenever your Amazon EC2 Auto Scaling group can't scale up due to a lack of available capacity\. Selecting many different instance families has two main benefits\. First, it can increase your chance of achieving your desired scale by tapping into many Spot capacity pools\. Second, it also can decrease the impact of Spot Instance interruptions on cluster availability\. Mixed Instance Policies with Spot Instances are a great way to increase diversity without increasing the number of node groups\. However, know that, if you need guaranteed resources, use On\-Demand Instances instead of Spot Instances\.

Spot instances may be terminated when demand for instances rises\. For more information, see the [Spot Instance Interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html) section of the Amazon EC2 User Guide for Linux Instances\. The [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler) project automatically alerts the Kubernetes control plane when a node is going down\. The project uses the Kubernetes API to cordon the node to ensure that no new work is scheduled there, then drains it and removes any existing work\.

It’s critical that all instance types have similar resource capacity when configuring [Mixed instance policies](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_MixedInstancesPolicy.html)\. The autoscaler’s scheduling simulator uses the first instance type in the Mixed Instance Policy\. If subsequent instance types are larger, resources may be wasted after a scale up\. If smaller, your pods may fail to schedule on the new instances due to insufficient capacity\. For example, `M4`, `M5`, `M5a,` and `M5n` instances all have similar amounts of CPU and memory and are great candidates for a Mixed Instance Policy\. The Amazon EC2 Instance Selector tool can help you identify similar instance types\. For more information, see [Amazon EC2 Instance Selector]((https://github.com/aws/amazon-ec2-instance-selector) on GitHub\.

We recommend that you isolate your On\-Demand and Spot instances capacity into separate Amazon EC2 Auto Scaling groups\. We recommend this over using a [base capacity strategy](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-purchase-options.html#asg-instances-distribution) because the scheduling properties of On\-Demand and Spot instances are different\. Spot Instances can be interrupted at any time\. When Amazon EC2 needs the capacity back, preemptive nodes are often tainted, thus requiring an explicit pod toleration to the preemption behavior\. This results in different scheduling properties for the nodes, so they should be separated into multiple Amazon EC2 Auto Scaling groups\.

The Cluster Autoscaler involves the concept of [Expanders](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders)\. They collectively provide different strategies for selecting which node group to scale\. The strategy `--expander=least-waste` is a good general purpose default, and if you're going to use multiple node groups for Spot Instance diversification, as described previously, it could help further cost\-optimize the node groups by scaling the group that would be best utilized after the scaling activity\.

**Prioritizing a node group or Auto Scaling group**  
You may also configure priority\-based autoscaling by using the `Priority` expander\. `--expander=priority` enables your cluster to prioritize a node group or Auto Scaling group, and if it is unable to scale for any reason, it will choose the next node group in the prioritized list\. This is useful in situations where, for example, you want to use `P3` instance types because their GPU provides optimal performance for your workload, but as a second option you can also use `P2` instance types\. For example:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-priority-expander
  namespace: kube-system
data:
  priority: |-
    10:
      - .*p2-node-group.*
    50:
      - .*p3-node-group.*
```

Cluster Autoscaler will try to scale up the Amazon EC2 Auto Scaling group matching the name `p2-node-group`\. If this operation doesn't succeed within `--max-node-provision-time`, it will attempt to scale an Amazon EC2 Auto Scaling group matching the name `p3-node-group`\. This value defaults to 15 minutes and can be reduced for more responsive node group selection, though if the value is too low, it can cause unnecessary scale outs\.

**Overprovisioning**  
The Cluster Autoscaler minimizes costs by ensuring that nodes are only added to the cluster when needed and are removed when unused\. This significantly impacts deployment latency because many pods will be forced to wait for a node scale up before they can be scheduled\. Nodes can take multiple minutes to become available, which can increase pod scheduling latency by an order of magnitude\.

This can be mitigated using [overprovisioning](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-can-i-configure-overprovisioning-with-cluster-autoscaler), which trades cost for scheduling latency\. Overprovisioning is implemented using temporary pods with negative priority\. These pods occupy space in the cluster\. When newly created pods are unschedulable and have a higher priority, the temporary pods are preempted to make room\. Then, the temporary pods become unschedulable, causing the Cluster Autoscaler to scale out new overprovisioned nodes\.

There are other benefits to overprovisioning\. Without overprovisioning, pods in a highly utilized cluster make less optimal scheduling decisions using the `preferredDuringSchedulingIgnoredDuringExecution` rule\. A common use case for this is to separate pods for a highly available application across Availability Zones using `AntiAffinity`\. Overprovisioning can significantly increase the chance that a node of the desired zone is available\.

Choosing the right amount of overprovisioned capacity is important\. One way to make this decision is to determine your average scale up frequency and divide this number by the amount of time it takes to scale up a new node\. For example, if on average you require a new node every 30 seconds and Amazon EC2 takes 30 seconds to provision a new node, a single node of overprovisioning ensures that there’s always an extra node available\. This can reduce scheduling latency by 30 seconds at the cost of a single additional Amazon EC2 instance\. To improve zonal scheduling decisions, you can overprovision the number of nodes to be equal to the number of Availability Zones in your Amazon EC2 Auto Scaling group\. Doing this ensures that the scheduler can select the best zone for incoming pods\.

**Prevent scale down eviction**  
Some workloads are expensive to evict\. Big data analysis, machine learning tasks, and test runners can take a long time to complete and must be restarted if they are interrupted\. The Cluster Autoscaler functions to scale down any node under the `scale-down-utilization-threshold`\. This interrupts any remaining pods on the node\. However, you can prevent this by ensuring that pods that are expensive to evict are protected by a label recognized by the Cluster Autoscaler\. To do this, ensure that pods that are expensive to evict have the label `cluster-autoscaler.kubernetes.io/safe-to-evict=false`\. 