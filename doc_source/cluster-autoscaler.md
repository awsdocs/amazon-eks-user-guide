// current page: intro to Cluster Autoscaler
# Cluster Autoscaler<a name="cluster-autoscaler"></a>

The Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) automatically adjusts the number of nodes in your cluster.  It watches for pods that fail to schedule and for nodes that are underutilized. More specifically, the AWS Cloud Provider implementation within Cluster Autoscaler controls the `.DesiredReplicas` field of EC2 Auto Scaling Groups.

**Node Groups** are an abstract Kubernetes concept for a group of nodes within a cluster.  It is not a true Kubernetes resource, but exists as an abstraction in the Cluster Autoscaler, Cluster API, and other components. Nodes within a Node Group share properties like labels and taints, but may consist of multiple Availability Zones or Instance Types.

**EC2 Auto Scaling Groups** can be used as an implementation of Node Groups on EC2. EC2 Auto Scaling Groups are configured to launch instances that automatically join their Kubernetes Clusters and apply labels and taints to their corresponding Node resource in the Kubernetes API.

For reference, [EKS Managed Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html) are implemented using EC2 Auto Scaling Groups, and are compatible with the Cluster Autoscaler. 

This topic shows you how to deploy the Cluster Autoscaler to your Amazon EKS cluster and how to configure it to modify your Amazon EC2 Auto Scaling groups\. The Cluster Autoscaler modifies your node groups so that they scale out when you need more resources and scale in when you have underutilized resources\.

The Cluster Autoscaler is typically installed as a [Deployment](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/cloudprovider/aws/examples) in your cluster. It uses [leader election](https://en.wikipedia.org/wiki/Leader_election) to ensure high availability, but work is done by a single replica at a time. 


## Create an Amazon EKS cluster<a name="ca-create-cluster"></a>

This section helps you to create a cluster and node group or groups\. If you already have a cluster, you can skip ahead to [Cluster Autoscaler node group considerations](#ca-ng-considerations)\.

Effective autoscaling starts with correctly configuring a set of Node Groups for your cluster. Selecting the right set of Node Groups is key to maximizing availability and reducing cost across your workloads. AWS implements Node Groups using EC2 Auto Scaling Groups, which are flexible to a large number of use cases. 

If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](#cluster-autoscaler), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\. Otherwise, you can create a single node group that spans multiple Availability Zones\.

Complete the steps in one of the following cluster creation procedures\.

**\[ To create a cluster with a single managed group that spans multiple Availability Zones \]**
+ Create an Amazon EKS cluster with a single managed node group with the following `eksctl` command\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\. Substitute the *variable text* with your own values\.

  ```
  eksctl create cluster --name my-cluster --version 1.17 --managed --asg-access
  ```

  Portions of the output showing the Availability Zones:

  ```
  ...
  [ℹ]  using region region-code
  [ℹ]  setting availability zones to [region-codea region-codeb region-codec]
  [ℹ]  subnets for region-codea - public:192.168.0.0/19 private:192.168.96.0/19
  [ℹ]  subnets for region-codeb - public:192.168.32.0/19 private:192.168.128.0/19
  [ℹ]  subnets for region-codec - public:192.168.64.0/19 private:192.168.160.0/19
  ...
  [ℹ]  nodegroup "ng-6bcca56a" has 2 node(s)
  [ℹ]  node "ip-192-168-28-68.region-code.compute.internal" is ready
  [ℹ]  node "ip-192-168-61-153.region-code.compute.internal" is ready
  [ℹ]  waiting for at least 2 node(s) to become ready in "ng-6bcca56a"
  [ℹ]  nodegroup "ng-6bcca56a" has 2 node(s)
  [ℹ]  node "ip-192-168-28-68.region-code.compute.internal" is ready
  [ℹ]  node "ip-192-168-61-153.region-code.compute.internal" is ready
  ...
  [✔]  EKS cluster "my-cluster" in "region-code" region-code is ready
  ```

**\[ To create a cluster with a dedicated managed node group for each Availability Zone \]**

1. Create an Amazon EKS cluster with no node groups with the following `eksctl` command\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\. Note the Availability Zones that the cluster is created in\. You will use these Availability Zones when you create your node groups\. Substitute the red variable text with your own values\.

   ```
   eksctl create cluster --name my-cluster --version 1.17 --without-nodegroup
   ```

   Portions of the output showing the Availability Zones:

   ```
   ...
   [ℹ]  using region region-code
   [ℹ]  setting availability zones to [region-codea region-codec region-codeb]
   [ℹ]  subnets for region-codea - public:192.168.0.0/19 private:192.168.96.0/19
   [ℹ]  subnets for region-codec - public:192.168.32.0/19 private:192.168.128.0/19
   [ℹ]  subnets for region-codeb - public:192.168.64.0/19 private:192.168.160.0/19
   ...
   [✔]  EKS cluster "my-cluster" in "region-code" region is ready
   ```

   This cluster was created in the following Availability Zones: *region\-code*a, *region\-code*c, and *region\-code*b\.

1. For each Availability Zone in your cluster, use the following `eksctl` command to create a node group\. Substitute the *variable text* with your own values\. This command creates an Auto Scaling group with a minimum count of one and a maximum count of ten\.

   ```
   eksctl create nodegroup --cluster my-cluster --node-zones region-codea --name region-codea --asg-access --nodes-min 1 --nodes 5 --nodes-max 10 --managed
   ```

## Cluster Autoscaler node group considerations<a name="ca-ng-considerations"></a>

### Node Group Composition

The Cluster Autoscaler makes assumptions about how you are using node groups, such as the EC2 instance types within the group. 

It's important to configure your node group based on these considerations:

* Each Node in a Node Group has identical scheduling properties, such as Labels, Taints, and Resources.
    * For MixedInstancePolicies, the Instance Types must be of the same shape for CPU, Memory, and GPU
    * The first Instance Type specified in the policy will be used to simulate scheduling.
    * If your policy has additional Instance Types with more resources, resources may be wasted after scale out.
    * If your policy has additional Instance Types with less resources, pods may fail to schedule on the instances.
* Node Groups with many nodes are preferred over many Node Groups with fewer nodes. This will have the biggest impact on scalability.
* Wherever possible, prefer EC2 features when both systems provide support (e.g. Regions, MixedInstancePolicy)

*Note: If possible, we recommend using [EKS Managed Node Groups](https://docs.aws.amazon.com/eks/latest/usergueifjcclndvnjijektdlgidebfjfnfglhnetdfblhvkdk
ide/managed-node-groups.html). Managed Node Groups come with powerful management features, including features for Cluster Autoscaler like automatic EC2 Auto Scaling Group discovery and graceful node termination.*

### Node group IAM policy<a name="ca-ng-iam-policy"></a>

The Cluster Autoscaler requires the following IAM permissions to make calls to AWS APIs on your behalf\.

If you used the previous `eksctl` commands to create your node groups, these permissions are automatically provided and attached to your node IAM roles\. If you did not use `eksctl`, you must create an IAM policy with the following document and attach it to your node IAM roles\. For more information, see [Modifying a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_modify.html) in the *IAM User Guide*\.

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

### Auto Scaling group tags<a name="ca-ng-asg-tags"></a>

The Cluster Autoscaler requires the following tags on your node group Auto Scaling groups so that they can be auto\-discovered\.

If you used the previous `eksctl` commands to create your node groups, these tags are automatically applied\. If not, you must manually tag your Auto Scaling groups with the following tags\. For more information, see [Tagging your Amazon EC2 resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) in the *Amazon EC2 User Guide for Linux Instances*\.


| Key | Value | 
| --- | --- | 
|  `k8s.io/cluster-autoscaler/<cluster-name>`  |  `owned`  | 
|  `k8s.io/cluster-autoscaler/enabled`  |  `true`  | 

## Deploy the Cluster Autoscaler<a name="ca-deploy"></a>

**Note**
* The Cluster Autoscaler’s version must match the Cluster’s Version. Cross version compatibility  is [not tested or supported](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/README.md#releases).

* [Auto Discovery](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/cloudprovider/aws#auto-discovery-setup) must be enabled, unless you have specific advanced use cases that prevent use of this mode.

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

1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.17 find the latest Cluster Autoscaler release that begins with 1\.17\. Record the semantic version number \(1\.17\.*`n`*\) for that release to use in the next step\.

1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. Replace *1\.15\.n* with your own value\. You can replace `us` with `asia` or `eu`\.

   ```
   kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.15.n
   ```
**Note**  
Depending on the version that you need, you may need to change the previous address to `gcr.io/google-containers/cluster-autoscaler:v1.n.n` \. The image address is listed on the [releases](https://github.com/kubernetes/autoscaler/releases) page\.

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
I0926 23:15:55.166357       1 utils.go:552] Skipping ip-192-168-3-111.region-code.compute.internal - node group min size reached
I0926 23:15:55.166365       1 utils.go:552] Skipping ip-192-168-71-83.region-code.compute.internal - node group min size reached
I0926 23:15:55.166373       1 utils.go:552] Skipping ip-192-168-60-191.region-code.compute.internal - node group min size reached
I0926 23:15:55.166435       1 static_autoscaler.go:393] Scale down status: unneededOnly=false lastScaleUpTime=2019-09-26 21:42:40.908059094 ...
I0926 23:15:55.166458       1 static_autoscaler.go:403] Starting scale down
I0926 23:15:55.166488       1 scale_down.go:706] No candidates for scale down
```

//new page: configuring Cluster Autoscaler

## Cluster Autoscaler and Specalized Use Cases

### EBS Volumes

Persistent storage is critical for building stateful applications, such as database or distributed caches. [EBS Volumes](https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/) enable this use case on Kubernetes, but are limited to a specific zone. These applications can be highly available if sharded across multiple AZs using a separate EBS Volume for each AZ. The Cluster Autoscaler can then balance the scaling of the EC2 Autoscaling Groups.

Ensure that:

* Node group balancing is enabled by setting `balance-similar-node-groups=true`.
* Node Groups are configured with identical settings except for different availability zones and EBS Volumes.

### Co-Scheduling

Machine learning distributed training jobs benefit significantly from the minimized latency of same-zone node configurations. These workloads deploy multiple pods to a specific zone. This can be achieved by setting Pod Affinity for all co-scheduled pods or Node Affinity using `topologyKey: failure-domain.beta.kubernetes.io/zone`. The Cluster Autoscaler will then scale out a specific zone to match demands. You may wish to allocate multiple EC2 Auto Scaling Groups, one per availability zone to enable failover for the entire co-scheduled workload.

Ensure that:

* Node group balancing is enabled by setting `balance-similar-node-groups=false`
* [Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) and/or [Pod Preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) is used when clusters include both Regional and Zonal Node Groups.
    * Use [Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) to force or encourage regional pods to avoid zonal Node Groups, and vice versa.
    * If zonal pods schedule onto regional node groups, this will result in imbalanced capacity for your regional pods.
    * If your zonal workloads can tolerate disruption and relocation, configure [Pod Preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) to enable regionally scaled pods to force preemption and rescheduling on a less contested zone.

### Accelerators, GPUs

Some clusters take advantage of specialized hardware accelerators such as GPU. When scaling out, the accelerator device plugin can take several minutes to advertise the resource to the cluster. The Cluster Autoscaler has simulated that this node will have the accelerator, but until the accelerator becomes ready and updates the node’s available resources, pending pods can not be scheduled on the node. This can result in [repeated unnecessary scale out](https://github.com/kubernetes/kubernetes/issues/54959).

Additionally, nodes with accelerators and high CPU or Memory utilization will not be considered for scale down, even if the accelerator is unused. This behavior can be expensive due to the relative cost of accelerators. Instead, the Cluster Autoscaler can apply special rules to consider nodes for scale down if they have unoccupied accelerators.

To ensure the correct behavior for these cases, you can configure the kubelet on your accelerator nodes to label the node before it joins the cluster. The Cluster Autoscaler will use this label selector to trigger the accelerator optimized behavior.

Ensure that:

* The Kubelet for GPU nodes is configured with `--node-labels k8s.amazonaws.com/accelerator=$ACCELERATOR_TYPE`
* Nodes with Accelerators adhere to the identical scheduling properties rule noted above.

### Scaling from 0

Cluster Autoscaler is capable of scaling Node Groups to and from zero, which can yield significant cost savings. It detects the CPU, memory, and GPU resources of an Auto Scaling Group by inspecting the InstanceType specified in its LaunchConfiguration or LaunchTemplate. Some pods require additional resources like `WindowsENI` or `PrivateIPv4Address` or specific NodeSelectors or Taints which cannot be discovered from the LaunchConfiguration. The Cluster Autoscaler can account for these factors by discovering them from tags on the EC2 Auto Scaling Group. For example:

```
Key: k8s.io/cluster-autoscaler/node-template/resources/$RESOURCE_NAME
Value: 5
Key: k8s.io/cluster-autoscaler/node-template/label/$LABEL_KEY
Value: $LABEL_VALUE
Key: k8s.io/cluster-autoscaler/node-template/taint/$TAINT_KEY
Value: NoSchedule
```

*Note: Keep in mind, when scaling to zero your capacity is returned to EC2 and may be unavailable in the future.*

## Configuration Parameters

There are many configuration options that can be used to tune the behavior and performance of the Cluster Autoscaler. A complete list of parameters is available on [Github](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-the-parameters-to-ca).

## Cluster Autoscaler Performance Optimization

The primary knobs for tuning the performance and scalability of the Cluster Autoscaler are the resources provided to the process, the scan interval of the algorithm, and the number of Node Groups in the cluster. There are other factors involved in the true runtime complexity of this algorithm, such as scheduling plugin complexity and number of pods. These are considered to be unconfigurable parameters as they are natural to the cluster’s workload and cannot easily be tuned.

**Scalability** refers to how well the Cluster Autoscaler performs as your Kubernetes Cluster increases in number of pods and nodes. As scalability limits are reached, the Cluster Autoscaler’s performance and functionality degrades. As the Cluster Autoscaler exceeds its scalability limits, it may no longer add or remove nodes in your cluster.

**Performance** refers to how quickly the Cluster Autoscaler is able to make and execute scaling decisions. A perfectly performing Cluster Autoscaler would instantly make a decision and trigger a scaling action in response to stimuli, such as a pod becoming unschedulable.

Understanding the autoscaling algorithm’s runtime complexity will help you tune the Cluster Autoscaler to continue operating smoothly in large clusters with greater than [1,000 nodes](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/scalability_tests.md).

The Cluster Autoscaler loads the entire cluster’s state into memory, including Pods, Nodes, and Node Groups. On each scan interval, the algorithm identifies unschedulable pods and simulates scheduling for each Node Group. Tuning these factors come with different tradeoffs which should be carefully considered for your use case.

### Vertically Autoscaling the Cluster Autoscaler

The simplest way to scale the Cluster Autoscaler to larger clusters is to increase the resource requests for its deployment. Both memory and CPU should be increased for large clusters, though this varies significantly with cluster size. The autoscaling algorithm stores all pods and nodes in memory, which can result in a memory footprint larger than a gigabyte in some cases. Increasing resources is typically done manually. If you find that constant resource tuning is creating an operational burden, consider using the [Addon Resizer](https://github.com/kubernetes/autoscaler/tree/master/addon-resizer) or [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler).

### Reducing the number of Node Groups

Minimizing the number of node groups is one way to ensure that the Cluster Autoscaler will continue to perform well on large clusters. This may be challenging for some organizations who structure their node groups per team or per application. While this is fully supported by the Kubernetes API, this is considered to be a Cluster Autoscaler anti-pattern with repercussions for scalability. There are many reasons to use multiple node groups (e.g. Spot or GPUs), but in many cases there are alternative designs that achieve the same effect while using a small number of groups.

Ensure that:

* Pod isolation is done using Namespaces rather than Node Groups.
    * This may not be possible in low-trust multi-tenant clusters.
    * Pod ResourceRequests and ResourceLimits are properly set to avoid resource contention.
    * Larger instance types will result in more optimal bin packing and reduced system pod overhead.
* NodeTaints or NodeSelectors are used to schedule pods as the exception, not as the rule.
* Regional resources are defined as a single EC2 Auto Scaling Group with multiple Availability Zones.

### Reducing the Scan Interval

A low scan interval (e.g. 10 seconds) will ensure that the Cluster Autoscaler responds as quickly as possible when pods become unschedulable. However, each scan results in many API calls to the Kubernetes API and EC2 Auto Scaling Group or EKS Managed Node Group APIs. These API calls can result in rate limiting or even service unavailability for your Kubernetes Control Plane.

The default scan interval is 10 seconds, but on AWS, launching a node takes significantly longer to launch a new instance. This means that it’s possible to increase the interval without significantly increasing overall scale up time. For example, if it takes 2 minutes to launch a node, changing the interval to 1 minute will result a tradeoff of 6x reduced API calls for 38% slower scale ups.

### Sharding Across Node Groups

The Cluster Autoscaler can be configured to operate on a specific set of Node Groups. Using this functionality, it’s possible to deploy multiple instances of the Cluster Autoscaler, each configured to operate on a different set of Node Groups. This strategy enables you use arbitrarily large numbers of Node Groups, trading cost for scalability. We only recommend using this as a last resort for improving performance.

The Cluster Autoscaler was not originally designed for this configuration, so there are some side effects. Since the shards do not communicate, it’s possible for multiple autoscalers to attempt to schedule an unschedulable pod. This can result in unnecessary scale out of multiple Node Groups. These extra nodes will scale back in after the `scale-down-delay`.

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

Ensure that:

* Each shard is configured to point to a unique set of EC2 Auto Scaling Groups
* Each shard is deployed to a separate namespace to avoid leader election conflicts

## Cluster Autoscaler Cost Efficency and Availability

The primary knobs for tuning the cost efficency of the Cluster Autoscaler are related to provisioning EC2 instances. Additionally, cost efficency must be balanced with availibity.  This section describes strategies such as using spot instances to reduce costs, and overprovisioning to reduce latency when creating new nodes. 

**Availability** means that pods can be scheduled quickly and without disruption. This includes when newly created pods need to be scheduled and when a scaled down node terminates any remaining pods scheduled to it.

**Cost** is determined by the decision behind scale out and scale in events. Resources are wasted if an existing node is underutilized or a new node is added that is too large for incoming pods. Depending on the use case, there can be costs associated with prematurely terminating pods due to an aggressive scale down decision.

### Spot Instances

You can use Spot Instances in your node groups and save up to 90% off the on-demand price, with the trade-off the Spot Instances can be interrupted at any time when EC2 needs the capacity back. Insufficient Capacity Errors will occur when your EC2 Auto Scaling group cannot scale up due to lack of available capacity. Maximizing diversity by selecting many instance families can increase your chance of achieving your desired scale by tapping into many Spot capacity pools, and decrease the impact of Spot Instance interruptions on your cluster availability. Mixed Instance Policies with Spot Instances are a great way to increase diversity without increasing the number of node groups. Keep in mind, if you need guaranteed resources, use On-Demand Instances instead of Spot Instances.

It’s critical that all Instance Types have similar resource capacity when configuring [Mixed Instance Policies](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_MixedInstancesPolicy.html). The autoscaler’s scheduling simulator uses the first InstanceType in the MixedInstancePolicy. If subsequent Instance Types are larger, resources may be wasted after a scale up. If smaller, your pods may fail to schedule on the new instances due to insufficient capacity. For example, M4, M5, M5a, and M5n instances all have similar amounts of CPU and Memory and are great candidates for a MixedInstancePolicy. The [EC2 Instance Selector](https://github.com/aws/amazon-ec2-instance-selector) tool can help you identify similar instance types.

![](./spot_mix_instance_policy.jpg)

It's recommended to isolate On-Demand and Spot capacity into separate EC2 Auto Scaling groups. This is preferred over using a [base capacity strategy](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-purchase-options.html#asg-instances-distribution) because the scheduling properties are fundamentally different. Since Spot Instances be interrupted at any time (when EC2 needs the capacity back), users will often taint their preemptable nodes, requiring an explicit pod toleration to the preemption behavior. These taints result in different scheduling properties for the nodes, so they should be separated into multiple EC2 Auto Scaling Groups.

The Cluster Autoscaler has a concept of [Expanders](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders), which provide different strategies for selecting which Node Group to scale. The strategy `--expander=least-waste` is a good general purpose default, and if you're going to use multiple node groups for Spot Instance diversification (as described in the image above), it could help further cost-optimize the node groups by scaling the group which would be best utilized after the scaling activity.

### Prioritizing a node group / ASG

You may also configure priority based autoscaling by using the Priority expander. `--expander=priority` enables your cluster to prioritize a node group / ASG, and if it is unable to scale for any reason, it will choose the next node group in the prioritized list. This is useful in situations where, for example, you want to use P3 instance types because their GPU provides optimal performance for your workload, but as a second option you can also use P2 instance types.

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

Cluster Autoscaler will try to scale up the EC2 Auto Scaling group matching the name *p2-node-group*. If this operation does not succeed within `--max-node-provision-time`, it will attempt to scale an EC2 Auto Scaling group matching the name *p3-node-group*.
This value defaults to 15 minutes and can be reduced for more responsive node group selection, though if the value is too low, it can cause unnecessary scale outs.

### Overprovisioning

The Cluster Autoscaler minimizes costs by ensuring that nodes are only added to the cluster when needed and are removed when unused. This significantly impacts deployment latency because many pods will be forced to wait for a node scale up before they can be scheduled. Nodes can take multiple minutes to become available, which can increase pod scheduling latency by an order of magnitude.

This can be mitigated using [overprovisioning](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-can-i-configure-overprovisioning-with-cluster-autoscaler), which trades cost for scheduling latency. Overprovisioning is implemented using temporary pods with negative priority, which occupy space in the cluster. When newly created pods are unschedulable and have higher priority, the temporary pods will be preempted to make room. The temporary pods then become unschedulable, triggering the Cluster Autoscaler to scale out new overprovisioned nodes.

There are other less obvious benefits to overprovisioning. Without overprovisioning, one of the side effects of a highly utilized cluster is that pods will make less optimal scheduling decisions using the `preferredDuringSchedulingIgnoredDuringExecution` rule of Pod or Node Affinity. A common use case for this is to separate pods for a highly available application across availability zones using AntiAffinity. Overprovisioning can significantly increase the chance that a node of the correct zone is available.

The amount of overprovisioned capacity is a careful business decision for your organization. At its core, it’s a tradeoff between performance and cost. One way to make this decision is to determine your average scale up frequency and divide it by the amount of time it takes to scale up a new node. For example, if on average you require a new node every 30 seconds and EC2 takes 30 seconds to provision a new node, a single node of overprovisioning will ensure that there’s always an extra node available, reducing scheduling latency by 30 seconds at the cost of a single additional EC2 Instance. To improve zonal scheduling decisions, overprovision a number of nodes equal to the number of availability zones in your EC2 Auto Scaling Group to ensure that the scheduler can select the best zone for incoming pods.

### Prevent Scale Down Eviction

Some workloads are expensive to evict. Big data analysis, machine learning tasks, and test runners will eventually complete, but must be restarted if interrupted. The Cluster Autoscaler will attempt to scale down any node under the scale-down-utilization-threshold, which will interrupt any remaining pods on the node. This can be prevented by ensuring that pods that are expensive to evict are protected by a label recognized by the Cluster Autoscaler.

Ensure that:

* Expensive to evict pods have the label `cluster-autoscaler.kubernetes.io/safe-to-evict=false`

## Additional Resources

This page contains a list of Cluster Autoscaler presentations and demos. If you'd like to add a presentation or demo here, please send a pull request.

| Presentation/Demo | Presenters |
| ------------ | ------- |
| [Autoscaling and Cost Optimization on Kubernetes: From 0 to 100](https://sched.co/Zemi) | Guy Templeton, Skyscanner & Jiaxin Shan, Amazon |

References:

* https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md
* https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md
* https://github.com/aws/amazon-ec2-instance-selector
* https://github.com/aws/aws-node-termination-handler