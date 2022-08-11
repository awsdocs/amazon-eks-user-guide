# Autoscaling<a name="autoscaling"></a>

Autoscaling is a function that automatically scales your resources up or down to meet changing demands\. This is a major Kubernetes function that would otherwise require extensive human resources to perform manually\.

Amazon EKS supports two autoscaling products\. The Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) and the [Karpenter](https://karpenter.sh/) open source autoscaling project\. The cluster autoscaler uses AWS scaling groups, while Karpenter works directly with the Amazon EC2 fleet\.

## Cluster Autoscaler<a name="cluster-autoscaler"></a>

The Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) automatically adjusts the number of nodes in your cluster when pods fail or are rescheduled onto other nodes\. The Cluster Autoscaler is typically installed as a [Deployment](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/cloudprovider/aws/examples) in your cluster\. It uses [leader election](https://en.wikipedia.org/wiki/Leader_election) to ensure high availability, but scaling is done by only one replica at a time\.

Before you deploy the Cluster Autoscaler, make sure that you're familiar with how Kubernetes concepts interface with AWS features\. The following terms are used throughout this topic:
+ **Kubernetes Cluster Autoscaler ** – A core component of the Kubernetes control plane that makes scheduling and scaling decisions\. For more information, see [Kubernetes Control Plane FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) on GitHub\.
+ **AWS Cloud provider implementation** – An extension of the Kubernetes Cluster Autoscaler that implements the decisions of the Kubernetes Cluster Autoscaler by communicating with AWS products and services such as Amazon EC2\. For more information, see [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md) on GitHub\.
+ **Node groups** – A Kubernetes abstraction for a group of nodes within a cluster\. Node groups aren't a true Kubernetes resource, but they're found as an abstraction in the Cluster Autoscaler, Cluster API, and other components\. Nodes that are found within a single node group might share several common properties such as labels and taints\. However, they can still consist of more than one Availability Zone or instance type\.
+ **Amazon EC2 Auto Scaling groups** – A feature of AWS that's used by the Cluster Autoscaler\. Auto Scaling groups are suitable for a large number of use cases\. Amazon EC2 Auto Scaling groups are configured to launch instances that automatically join their Kubernetes cluster\. They also apply labels and taints to their corresponding node resource in the Kubernetes API\.

For reference, [Managed node groups](managed-node-groups.md) are managed using Amazon EC2 Auto Scaling groups, and are compatible with the Cluster Autoscaler\.

This topic describes how you can deploy the Cluster Autoscaler to your Amazon EKS cluster and configure it to modify your Amazon EC2 Auto Scaling groups\.

### Prerequisites<a name="ca-prerequisites"></a>

Before deploying the Cluster Autoscaler, you must meet the following prerequisites:
+ An existing Amazon EKS cluster – If you don’t have a cluster, see [Creating an Amazon EKS cluster](create-cluster.md)\.
+ An existing IAM OIDC provider for your cluster\. To determine whether you have one or need to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Node groups with Auto Scaling groups tags\. The Cluster Autoscaler requires the following tags on your Auto Scaling groups so that they can be auto\-discovered\.
  + If you used `eksctl` to create your node groups, these tags are automatically applied\.
  + If you didn't use `eksctl`, you must manually tag your Auto Scaling groups with the following tags\. For more information, see [Tagging your Amazon EC2 resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) in the Amazon EC2 User Guide for Linux Instances\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html)

### Create an IAM policy and role<a name="ca-create-policy"></a>

Create an IAM policy that grants the permissions that the Cluster Autoscaler requires to use an IAM role\. Replace all of the `example values` with your own values throughout the procedures\.

1. Create an IAM policy\.

   1. Save the following contents to a file that's named `cluster-autoscaler-policy.json`\. If your existing node groups were created with `eksctl` and you used the `--asg-access` option, then this policy already exists and you can skip to step 2\. 

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "VisualEditor0",
                  "Effect": "Allow",
                  "Action": [
                      "autoscaling:SetDesiredCapacity",
                      "autoscaling:TerminateInstanceInAutoScalingGroup"
                  ],
                  "Resource": "*",
                  "Condition": {
                      "StringEquals": {
                          "aws:ResourceTag/k8s.io/cluster-autoscaler/my-cluster": "owned"
                      }
                  }
              },
              {
                  "Sid": "VisualEditor1",
                  "Effect": "Allow",
                  "Action": [
                      "autoscaling:DescribeAutoScalingInstances",
                      "autoscaling:DescribeAutoScalingGroups",
                      "ec2:DescribeLaunchTemplateVersions",
                      "autoscaling:DescribeTags",
                      "autoscaling:DescribeLaunchConfigurations"
                  ],
                  "Resource": "*"
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

      Take note of the Amazon Resource Name \(ARN\) that's returned in the output\. You need to use it in a later step\.

1. You can create an IAM role and attach an IAM policy to it using `eksctl` or the AWS Management Console\. Select the desired tab for the following instructions\.

------
#### [ eksctl ]

   1. Run the following command if you created your Amazon EKS cluster with `eksctl`\. If you created your node groups using the `--asg-access` option, then replace `AmazonEKSClusterAutoscalerPolicy` with the name of the IAM policy that `eksctl` created for you\. The policy name is similar to `eksctl-my-cluster-nodegroup-ng-xxxxxxxx-PolicyAutoScaling`\.

      ```
      eksctl create iamserviceaccount \
        --cluster=my-cluster \
        --namespace=kube-system \
        --name=cluster-autoscaler \
        --attach-policy-arn=arn:aws:iam::111122223333:policy/AmazonEKSClusterAutoscalerPolicy \
        --override-existing-serviceaccounts \
        --approve
      ```

   1. We recommend that, if you created your node groups using the `--asg-access` option, you detach the IAM policy that `eksctl` created and attached to the [Amazon EKS node IAM role](create-node-role.md) that `eksctl` created for your node groups\. You detach the policy from the node IAM role for Cluster Autoscaler to function properly\. Detaching the policy doesn't give other pods on your nodes the permissions in the policy\. For more information, see [Removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#remove-policies-console) in the Amazon EC2 User Guide for Linux Instances\.

------
#### [ AWS Management Console ]

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the left navigation pane, choose **Roles**\. Then choose **Create role**\.

   1. In the **Trusted entity type** section, choose **Web identity**\.

   1. In the **Web identity** section:

      1. For **Identity provider**, choose the **OpenID Connect provider URL** for your cluster \(as shown in the cluster **Overview** tab in Amazon EKS\)\.

      1. For **Audience**, choose `sts.amazonaws.com`\.

   1. Choose **Next**\.

   1. In the **Filter policies** box, enter **AmazonEKSClusterAutoscalerPolicy**\. Then select the check box to the left of the policy name returned in the search\.

   1. Choose **Next**\.

   1. For **Role name**, enter a unique name for your role, such as **AmazonEKSClusterAutoscalerRole**\.

   1. For **Description**, enter descriptive text such as **Amazon EKS \- Cluster autoscaler role**\.

   1. Choose **Create role**\.

   1. After the role is created, choose the role in the console to open it for editing\.

   1. Choose the **Trust relationships** tab, and then choose **Edit trust policy**\.

   1. Find the line that looks similar to the following:

      ```
      "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
      ```

      Change the line to look like the following line\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with your cluster's OIDC provider ID\. Replace `region-code` with the AWS Region that your cluster is in\.

      ```
      "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:cluster-autoscaler"
      ```

   1. Choose **Update policy** to finish\.

------

### Deploy the Cluster Autoscaler<a name="ca-deploy"></a>

Complete the following steps to deploy the Cluster Autoscaler\. We recommend that you review [Deployment considerations](#ca-deployment-considerations) and optimize the Cluster Autoscaler deployment before you deploy it to a production cluster\.

**To deploy the Cluster Autoscaler**

1. Download the Cluster Autoscaler YAML file\.

   ```
   curl -o cluster-autoscaler-autodiscover.yaml https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
   ```

1. Modify the YAML file and replace *<YOUR CLUSTER NAME>* with your cluster name\. Also consider replacing the `cpu` and `memory` values as determined by your environment\.

1. Apply the YAML file to your cluster\.

   ```
   kubectl apply -f cluster-autoscaler-autodiscover.yaml
   ```

1. Annotate the `cluster-autoscaler` service account with the ARN of the IAM role that you created previously\. Replace the `example values` with your own values\. 

   ```
   kubectl annotate serviceaccount cluster-autoscaler \
     -n kube-system \
     eks.amazonaws.com/role-arn=arn:aws:iam::ACCOUNT_ID:role/AmazonEKSClusterAutoscalerRole
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

   Edit the `cluster-autoscaler` container command to add the following options\. `--balance-similar-node-groups` ensures that there is enough available compute across all availability zones\. `--skip-nodes-with-system-pods=false` ensures that there are no problems with scaling to zero\.
   + `--balance-similar-node-groups`
   + `--skip-nodes-with-system-pods=false`

   ```
       spec:
         containers:
         - command
           - ./cluster-autoscaler
           - --v=4
           - --stderrthreshold=info
           - --cloud-provider=aws
           - --skip-nodes-with-local-storage=false
           - --expander=least-waste
           - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
           - --balance-similar-node-groups
           - --skip-nodes-with-system-pods=false
   ```

   Save and close the file to apply the changes\.

1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page from GitHub in a web browser and find the latest Cluster Autoscaler version that matches the Kubernetes major and minor version of your cluster\. For example, if the Kubernetes version of your cluster is `1.23`, find the latest Cluster Autoscaler release that begins with `1.23`\. Record the semantic version number \(`1.23.n`\) for that release to use in the next step\.

1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. Replace `1.23.n` with your own value\.

   ```
   kubectl set image deployment cluster-autoscaler \
     -n kube-system \
     cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.23.n
   ```

### View your Cluster Autoscaler logs<a name="ca-view-logs"></a>

After you have deployed the Cluster Autoscaler, you can view the logs and verify that it's monitoring your cluster load\.

View your Cluster Autoscaler logs with the following command\.

```
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
```

The example output is as follows\.

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

### Deployment considerations<a name="ca-deployment-considerations"></a>

Review the following considerations to optimize your Cluster Autoscaler deployment\.

#### Scaling considerations<a name="ca-considerations-scaling"></a>

The Cluster Autoscaler can be configured to include any additional features of your nodes\. These features can include Amazon EBS volumes attached to nodes, Amazon EC2 instance types of nodes, or GPU accelerators\. 

**Scope node groups across more than one Availability Zone**  
We recommend that you configure multiple node groups, scope each group to a single Availability Zone, and enable the `--balance-similar-node-groups` feature\. If you only create one node group, scope that node group to span over more than one Availability Zone\.

When setting `--balance-similar-node-groups` to true, make sure that the node groups you want the Cluster Autoscaler to balance have matching labels \(except for automatically added zone labels\)\. You can pass a `--balancing-ignore-label` flag to nodes with different labels to balance them regardless, but this should only be done as needed\.

**Optimize your node groups**  
The Cluster Autoscaler makes assumptions about how you're using node groups\. This includes which instance types that you use within a group\. To align with these assumptions, configure your node group based on these considerations and recommendations: 
+ Each node in a node group must have identical scheduling properties\. This includes labels, taints, and resources\.
  + For `MixedInstancePolicies`, the instance types must have compatible CPU, memory, and GPU specifications\.
  + The first instance type that's specified in the policy simulates scheduling\.
  + If your policy has additional instance types with more resources, resources might be wasted after scale out\.
  + If your policy has additional instance types with fewer resources than the original instance types, pods might fail to schedule on the instances\.
+ Configure a smaller number of node groups with a larger number of nodes because the opposite configuration can negatively affect scalability\.
+ Use Amazon EC2 features whenever both systems provide support them \(for example, use Regions and `MixedInstancePolicy`\.\)

If possible, we recommend that you use [Managed node groups](managed-node-groups.md)\. Managed node groups come with powerful management features\. These include features for Cluster Autoscaler such as automatic Amazon EC2 Auto Scaling group discovery and graceful node termination\.

**Use EBS volumes as persistent storage**  
Persistent storage is critical for building stateful applications, such as databases and distributed caches\. With Amazon EBS volumes, you can build stateful applications on Kubernetes\. However, you're limited to only building them within a single Availability Zone\. For more information, see [How do I use persistent storage in Amazon EKS?](http://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/)\. For a better solution, consider building stateful applications that are sharded across more than one Availability Zone using a separate Amazon EBS volume for each Availability Zone\. Doing so means that your application can be highly available\. Moreover, the Cluster Autoscaler can balance the scaling of the Amazon EC2 Auto Scaling groups\. To do this, make sure that the following conditions are met:
+ Node group balancing is enabled by setting `balance-similar-node-groups=true`\.
+ Your node groups are configured with identical settings \(outside of being in more than one Availability Zone and using different Amazon EBS volumes\)\.

**Co\-scheduling**  
Machine learning distributed training jobs benefit significantly from the minimized latency of same\-zone node configurations\. These workloads deploy multiple pods to a specific zone\.You can achieve this by setting pod affinity for all co\-scheduled pods or node affinity using `topologyKey: topology.kubernetes.io/zone`\. Using this configuration, the Cluster Autoscaler scales out a specific zone to match demands\. Allocate multiple Amazon EC2 Auto Scaling groups, with one for each Availability Zone, to enable failover for the entire co\-scheduled workload\. Make sure that the following conditions are met:
+ Node group balancing is enabled by setting `balance-similar-node-groups=true`\.
+ [Node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity), [pod preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/), or both, are used when clusters include both Regional and Zonal node groups\.
  + Use [Node Affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) to force or encourage regional pods and avoid zonal node groups\.
  + Don't schedule zonal pods onto Regional node groups\. Doing so can result in imbalanced capacity for your Regional pods\.
  + Configure [pod preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) if your zonal workloads can tolerate disruption and relocation\. Doing so enforces preemption and rescheduling on a less contested zone for your Regionally scaled pods\.

**Accelerators and GPUs**  
Some clusters use specialized hardware accelerators such as a dedicated GPU\. When scaling out, the accelerator can take several minutes to advertise the resource to the cluster\. During this time, the Cluster Autoscaler simulates that this node has the accelerator\. However, until the accelerator becomes ready and updates the available resources of the node, pending pods can't be scheduled on the node\. This can result in [repeated unnecessary scale out](https://github.com/kubernetes/kubernetes/issues/54959)\.

Nodes with accelerators and high CPU or memory utilization aren't considered for scale down even if the accelerator is unused\. However, this can be result in unncessary costs\. To avoid these costs, the Cluster Autoscaler can apply special rules to consider nodes for scale down if they have unoccupied accelerators\.

To ensure the correct behavior for these cases, configure the `kubelet` on your accelerator nodes to label the node before it joins the cluster\. The Cluster Autoscaler uses this label selector to invoke the accelerator optimized behavior\. Make sure that the following conditions are met: 
+ The `kubelet` for GPU nodes is configured with `--node-labels k8s.amazonaws.com/accelerator=$ACCELERATOR_TYPE`\.
+ Nodes with accelerators adhere to the identical scheduling properties rule\.

**Scaling from zero**  
Cluster Autoscaler can scale node groups to and from zero\. This might result in a significant cost savings\. The Cluster Autoscaler detects the CPU, memory, and GPU resources of an Auto Scaling group by inspecting the `InstanceType` that is specified in its `LaunchConfiguration` or `LaunchTemplate`\. Some pods require additional resources such as `WindowsENI` or `PrivateIPv4Address`\. Or they might require specific `NodeSelectors` or `Taints`\. These latter two can't be discovered from the `LaunchConfiguration`\. However, the Cluster Autoscaler can account for these factors by discovering them from the following tags on the Auto Scaling group\. 

```
Key: k8s.io/cluster-autoscaler/node-template/resources/$RESOURCE_NAME
Value: 5
Key: k8s.io/cluster-autoscaler/node-template/label/$LABEL_KEY
Value: $LABEL_VALUE
Key: k8s.io/cluster-autoscaler/node-template/taint/$TAINT_KEY
Value: NoSchedule
```

**Note**  
When scaling to zero, your capacity is returned to Amazon EC2 and might become unavailable in the future\.
You can use [describeNodegroup](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeNodegroup.html) to diagnose issues with managed node groups when scaling to and from zero\.

**Additional configuration parameters**  
There are many configuration options that can be used to tune the behavior and performance of the Cluster Autoscaler\. For a complete list of parameters, see [What are the parameters to CA?](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-the-parameters-to-ca) on GitHub\.

#### Performance considerations<a name="considerations-performance"></a>

There are a few key items that you can change to tune the performance and scalability of the Cluster Autoscaler\. The primary ones are any resources that are provided to the process, the scan interval of the algorithm, and the number of node groups in the cluster\. However, there are also several other factors that are involved in the true runtime complexity of this algorithm\. These include the scheduling plug\-in complexity and the number of pods\. These are considered to be unconfigurable parameters because they're integral to the workload of the cluster and can't easily be tuned\.

*Scalability* refers to how well the Cluster Autoscaler performs as the number of pods and nodes in your Kubernetes cluster increases\. If its scalability quotas are reached, the performance and functionality of the Cluster Autoscaler degrades\. Additionally, when it exceeds its scalability quotas, the Cluster Autoscaler can no longer add or remove nodes in your cluster\.

*Performance* refers to how quickly the Cluster Autoscaler can make and implement scaling decisions\. A perfectly performing Cluster Autoscaler instantly make decisions and invoke scaling actions in response to specific conditions, such as a pod becoming unschedulable\.

Be familiar with the runtime complexity of the autoscaling algorithm\. Doing so makes it easier to tune the Cluster Autoscaler to operate well in large clusters \(with more than [1,000 nodes](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/scalability_tests.md)\)\.

The Cluster Autoscaler loads the state of the entire cluster into memory\. This includes the pods, nodes, and node groups\. On each scan interval, the algorithm identifies unschedulable pods and simulates scheduling for each node group\. Know that tuning these factors in different ways comes with different tradeoffs\.

**Vertical autoscaling**  
You can scale the Cluster Autoscaler to larger clusters by increasing the resource requests for its deployment\. This is one of the simpler methods to do this\. Increase both the memory and CPU for the large clusters\. Know that how much you should increase the memory and CPU depends greatly on the specific cluster size\. The autoscaling algorithm stores all pods and nodes in memory\. This can result in a memory footprint larger than a gigabyte in some cases\. You usually need to increase resources manually\. If you find that you often need to manually increase resources, consider using the [Addon Resizer](https://github.com/kubernetes/autoscaler/tree/master/addon-resizer) or [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) to automate the process\.

**Reducing the number of node groups**  
You can lower the number of node groups to improve the performance of the Cluster Autoscaler in large clusters\. If you structured your node groups on an individual team or application basis, this might be challenging\. Even though this is fully supported by the Kubernetes API, this is considered to be a Cluster Autoscaler anti\-pattern with repercussions for scalability\. There are many advantages to using multiple node groups that, for example, use both Spot or GPU instances\. In many cases, there are alternative designs that achieve the same effect while using a small number of groups\. Make sure that the following conditions are met: 
+ Isolate pods by using namespaces rather than node groups\.
  + You might not be able to do this in low\-trust multi\-tenant clusters\.
  + Set pod `ResourceRequests` and `ResourceLimits` properly to avoid resource contention\.
  + Use larger instance types for more optimal bin packing and reduced system pod overhead\.
+ Avoid using `NodeTaints` or `NodeSelectors` to schedule pods\. Only use them on a limited basis\.
+ Define Regional resources as a single Amazon EC2 Auto Scaling group with more than one Availability Zone\.

**Reducing the scan interval**  
Using a low scan interval, such as the default setting of ten seconds, ensures that the Cluster Autoscaler responds as quickly as possible when pods become unschedulable\. However, each scan results in many API calls to the Kubernetes API and Amazon EC2 Auto Scaling group or the Amazon EKS managed node group APIs\. These API calls can result in rate limiting or even service unavailability for your Kubernetes control plane\.

The default scan interval is ten seconds, but on AWS, launching a node takes significantly longer to launch a new instance\. This means that it’s possible to increase the interval without significantly increasing overall scale up time\. For example, if it takes two minutes to launch a node, don't change the interval to one minute because this might result in a trade\-off of 6x reduced API calls for 38% slower scale ups\.

**Sharing across node groups**  
You can configure the Cluster Autoscaler to operate on a specific set of node groups\. By using this functionality, you can deploy multiple instances of the Cluster Autoscaler\. Configure each instance to operate on a different set of node groups\. By doing this, you can use arbitrarily large numbers of node groups, trading cost for scalability\. However, we only recommend that you do this as last resort for improving the performance of Cluster Autoscaler\.

This configuration has its drawbacks\. It can result in unnecessary scale out of multiple node groups\. The extra nodes scale back in after the `scale-down-delay`\.

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

#### Cost efficiency and availability<a name="considerations-cost-efficiency"></a>

The primary options for tuning the cost efficiency of the Cluster Autoscaler are related to provisioning Amazon EC2 instances\. Additionally, cost efficiency must be balanced with availability\. This section describes strategies such as using Spot instances to reduce costs and overprovisioning to reduce latency when creating new nodes\.
+ **Availability** – Pods can be scheduled quickly and without disruption\. This is true even for when newly created pods need to be scheduled and for when a scaled down node terminates any remaining pods scheduled to it\.
+ **Cost** – Determined by the decision behind scale\-out and scale\-in events\. Resources are wasted if an existing node is underutilized or if a new node is added that is too large for incoming pods\. Depending on the specific use case, there can be costs that are associated with prematurely terminating pods due to an aggressive scale down decision\.

**Spot instances**  
You can use Spot Instances in your node groups to save up to 90% off the on\-demand price\. This has the trade\-off of Spot Instances possibly being interrupted at any time when Amazon EC2 needs the capacity back\. `Insufficient Capacity Errors` occur whenever your Amazon EC2 Auto Scaling group can't scale up due to a lack of available capacity\. Selecting many different instance families has two main benefits\. First, it can increase your chance of achieving your desired scale by tapping into many Spot capacity pools\. Second, it also can decrease the impact of Spot Instance interruptions on cluster availability\. Mixed Instance Policies with Spot Instances are a great way to increase diversity without increasing the number of node groups\. However, know that, if you need guaranteed resources, use On\-Demand Instances instead of Spot Instances\.

Spot instances might be terminated when demand for instances rises\. For more information, see the [Spot Instance Interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html) section of the Amazon EC2 User Guide for Linux Instances\. The [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler) project automatically alerts the Kubernetes control plane when a node is going down\. The project uses the Kubernetes API to cordon the node to ensure that no new work is scheduled there, then drains it and removes any existing work\.

It’s critical that all instance types have similar resource capacity when configuring [Mixed instance policies](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_MixedInstancesPolicy.html)\. The scheduling simulator of the autoscaler uses the first instance type in the Mixed Instance Policy\. If subsequent instance types are larger, resources might be wasted after a scale up\. If the instances are smaller, your pods may fail to schedule on the new instances due to insufficient capacity\. For example, `M4`, `M5`, `M5a,` and `M5n` instances all have similar amounts of CPU and memory and are great candidates for a Mixed Instance Policy\. The Amazon EC2 Instance Selector tool can help you identify similar instance types or additional critical criteria, such as size\. For more information, see [Amazon EC2 Instance Selector](https://github.com/aws/amazon-ec2-instance-selector) on GitHub\.

We recommend that you isolate your On\-Demand and Spot instances capacity into separate Amazon EC2 Auto Scaling groups\. We recommend this over using a [base capacity strategy](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-purchase-options.html#asg-instances-distribution) because the scheduling properties of On\-Demand and Spot instances are different\. Spot Instances can be interrupted at any time\. When Amazon EC2 needs the capacity back, preemptive nodes are often tainted, thus requiring an explicit pod toleration to the preemption behavior\. This results in different scheduling properties for the nodes, so they should be separated into multiple Amazon EC2 Auto Scaling groups\.

The Cluster Autoscaler involves the concept of [Expanders](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders)\. They collectively provide different strategies for selecting which node group to scale\. The strategy `--expander=least-waste` is a good general purpose default, and if you're going to use multiple node groups for Spot Instance diversification, as described previously, it could help further cost\-optimize the node groups by scaling the group that would be best utilized after the scaling activity\.

**Prioritizing a node group or Auto Scaling group**  
You might also configure priority\-based autoscaling by using the `Priority` expander\. `--expander=priority` enables your cluster to prioritize a node group or Auto Scaling group, and if it is unable to scale for any reason, it will choose the next node group in the prioritized list\. This is useful in situations where, for example, you want to use `P3` instance types because their GPU provides optimal performance for your workload, but as a second option you can also use `P2` instance types\. For example:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-priority-expander
  namespace: kube-system
data:
  priorities: |-
    10:
      - .*p2-node-group.*
    50:
      - .*p3-node-group.*
```

Cluster Autoscaler attempts to scale up the Amazon EC2 Auto Scaling group matching the name `p3-node-group`\. If this operation doesn't succeed within `--max-node-provision-time`, it then attempts to scale an Amazon EC2 Auto Scaling group matching the name `p2-node-group`\. This value defaults to 15 minutes and can be reduced for more responsive node group selection\. However, if the value is too low, unnecessary scaleout might occur\.

**Overprovisioning**  
The Cluster Autoscaler helps to minimize costs by ensuring that nodes are only added to the cluster when they're needed and are removed when they're unused\. This significantly impacts deployment latency because many pods must wait for a node to scale up before they can be scheduled\. Nodes can take multiple minutes to become available, which can increase pod scheduling latency by an order of magnitude\.

This can be mitigated using [overprovisioning](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-can-i-configure-overprovisioning-with-cluster-autoscaler), which trades cost for scheduling latency\. Overprovisioning is implemented using temporary pods with negative priority\. These pods occupy space in the cluster\. When newly created pods are unschedulable and have a higher priority, the temporary pods are preempted to make room\. Then, the temporary pods become unschedulable, causing the Cluster Autoscaler to scale out new overprovisioned nodes\.

There are other benefits to overprovisioning\. Without overprovisioning, pods in a highly utilized cluster make less optimal scheduling decisions using the `preferredDuringSchedulingIgnoredDuringExecution` rule\. A common use case for this is to separate pods for a highly available application across Availability Zones using `AntiAffinity`\. Overprovisioning can significantly increase the chance that a node of the desired zone is available\.

It's important to choose an appropriate amount of overprovisioned capacity\. One way that you can make sure that you choose an appropriate amount is by taking your average scaleup frequency and dividing it by the duration of time it takes to scale up a new node\. For example, if, on average, you require a new node every 30 seconds and Amazon EC2 takes 30 seconds to provision a new node, a single node of overprovisioning ensures that there’s always an extra node available\. Doing this can reduce scheduling latency by 30 seconds at the cost of a single additional Amazon EC2 instance\. To make better zonal scheduling decisions, you can also overprovision the number of nodes to be the same as the number of Availability Zones in your Amazon EC2 Auto Scaling group\. Doing this ensures that the scheduler can select the best zone for incoming pods\.

**Prevent scale down eviction**  
Some workloads are expensive to evict\. Big data analysis, machine learning tasks, and test runners can take a long time to complete and must be restarted if they're interrupted\. The Cluster Autoscaler helps to scale down any node under the `scale-down-utilization-threshold`\. This interrupts any remaining pods on the node\. However, you can prevent this from happening by ensuring that pods that are expensive to evict are protected by a label recognized by the Cluster Autoscaler\. To do this, ensure that pods that are expensive to evict have the label `cluster-autoscaler.kubernetes.io/safe-to-evict=false`\. 

## Karpenter<a name="karpenter"></a>

Amazon EKS supports the Karpenter open\-source autoscaling project\. See the [Karpenter](https://karpenter.sh/docs/) documentation to deploy it\.

### About Karpenter<a name="karp-overview"></a>

Karpenter is a flexible, high\-performance Kubernetes cluster autoscaler that helps improve application availability and cluster efficiency\. Karpenter launches right\-sized compute resources, \(for example, Amazon EC2 instances\), in response to changing application load in under a minute\. Through integrating Kubernetes with AWS, Karpenter can provision just\-in\-time compute resources that precisely meet the requirements of your workload\. Karpenter automatically provisions new compute resources based on the specific requirements of cluster workloads\. These include compute, storage, acceleration, and scheduling requirements\. Amazon EKS supports clusters using Karpenter, although Karpenter works with any conformant Kubernetes cluster\.

### How Karpenter works<a name="karp-works"></a>

Karpenter works in tandem with the Kubernetes scheduler by observing incoming pods over the lifetime of the cluster\. It launches or terminates nodes to maximize application availability and cluster utilization\. When there is enough capacity in the cluster, the Kubernetes scheduler will place incoming pods as usual\. When pods are launched that cannot be scheduled using the existing capacity of the cluster, Karpenter bypasses the Kubernetes scheduler and works directly with your provider’s compute service, \(for example, Amazon EC2\), to launch the minimal compute resources needed to fit those pods and binds the pods to the nodes provisioned\. As pods are removed or rescheduled to other nodes, Karpenter looks for opportunities to terminate under\-utilized nodes\. Running fewer, larger nodes in your cluster reduces overhead from daemonsets and Kubernetes system components and provides more opportunities for efficient bin\-packing\.

### Prerequisites<a name="karpenter-prerequisites"></a>

Before deploying Karpenter, you must meet the following prerequisites:
+ An existing Amazon EKS cluster – If you don’t have a cluster, see [Creating an Amazon EKS cluster](create-cluster.md)\.
+ An existing IAM OIDC provider for your cluster\. To determine whether you have one or need to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ A user or role with permission to create a cluster\.
+ AWS CLI
+ [Installing or updating `kubectl`](install-kubectl.md)
+ [Using Helm with Amazon EKS](helm.md)

You can deploy Karpenter using `eksctl` if you prefer\. See [Installing or updating `eksctl`](eksctl.md)\.