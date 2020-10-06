# Migrating to a new node group<a name="migrate-stack"></a>

This topic helps you to create a new node group, gracefully migrate your existing applications to the new group, and then remove the old node group from your cluster\. You can migrate to a new node group using [`eksctl`](#migrate-node-group-eksctl) or the [AWS Management Console](#migrate-node-group-console)\.<a name="migrate-node-group-eksctl"></a>

**To migrate your applications to a new node group with `eksctl`**

This procedure requires `eksctl` version `0.29.1` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters and node groups that were created with `eksctl`\.

1. Retrieve the name of your existing node groups, substituting <default> with your cluster name\.

   ```
   eksctl get nodegroups --cluster=<default>
   ```

   Output:

   ```
   CLUSTER      NODEGROUP          CREATED               MIN SIZE      MAX SIZE     DESIRED CAPACITY     INSTANCE TYPE     IMAGE ID
   default      standard-nodes   2019-05-01T22:26:58Z  1             4            3                    t3.medium         ami-05a71d034119ffc12
   ```

1. Launch a new node group with `eksctl` with the following command, substituting the <example> values with your own values\.
**Note**  
For more available flags and their descriptions, see [https://eksctl\.io/](https://eksctl.io/)\.

   ```
   eksctl create nodegroup \
   --cluster <default> \
   --version <1.17> \
   --name <standard-nodes-new> \
   --node-type <t3.medium> \
   --nodes <3> \
   --nodes-min <1> \
   --nodes-max <4> \
   --node-ami auto
   ```

1. When the previous command completes, verify that all of your nodes have reached the `Ready` state with the following command:

   ```
   kubectl get nodes
   ```

1. Delete the original node group with the following command, substituting the <example> values with your cluster and nodegroup names:

   ```
   eksctl delete nodegroup --cluster <default> --name <standard-nodes>
   ```<a name="migrate-node-group-console"></a>

**To migrate your applications to a new node group with the AWS Management Console**

1. Launch a new node group by following the steps outlined in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. <a name="node-instance-role-step"></a>Record the **NodeInstanceRole** for the node group that was created\. You need this to add the new Amazon EKS nodes to your cluster\.
**Note**  
If you have attached any additional IAM policies to your old node group IAM role, such as adding permissions for the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), you should attach those same policies to your new node group IAM role to maintain that functionality on the new group\.

1. Update the security groups for both node groups so that they can communicate with each other\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md)\.

   1. Record the security group IDs for both node groups\. This is shown as the **NodeSecurityGroup** value in the AWS CloudFormation stack outputs\. 

      You can use the following AWS CLI commands to get the security group IDs from the stack names\. In these commands, `oldNodes` is the AWS CloudFormation stack name for your older node stack, and `newNodes` is the name of the stack that you are migrating to\.

      ```
      oldNodes="<old_node_CFN_stack_name>"
      newNodes="<new_node_CFN_stack_name>"
      
      oldSecGroup=$(aws cloudformation describe-stack-resources --stack-name $oldNodes \
      --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].PhysicalResourceId' \
      --output text)
      newSecGroup=$(aws cloudformation describe-stack-resources --stack-name $newNodes \
      --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].PhysicalResourceId' \
      --output text)
      ```

   1. Add ingress rules to each node security group so that they accept traffic from each other\.

      The following AWS CLI commands add ingress rules to each security group that allow all traffic on all protocols from the other security group\. This configuration allows pods in each node group to communicate with each other while you are migrating your workload to the new group\.

      ```
      aws ec2 authorize-security-group-ingress --group-id $oldSecGroup \
      --source-group $newSecGroup --protocol -1
      aws ec2 authorize-security-group-ingress --group-id $newSecGroup \
      --source-group $oldSecGroup --protocol -1
      ```

1. Edit the `aws-auth` configmap to map the new node instance role in RBAC\.

   ```
   kubectl edit configmap -n kube-system aws-auth
   ```

   Add a new `mapRoles` entry for the new node group\. 

   ```
   apiVersion: v1
   data:
     mapRoles: |
   <    - rolearn: <ARN of instance role (not instance profile)>
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes>
       - rolearn: arn:aws:iam::111122223333:role/nodes-1-16-NodeInstanceRole-U11V27W93CX5
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
   ```

   Replace the `<ARN of instance role (not instance profile)>` snippet with the **NodeInstanceRole** value that you recorded in a [previous step](#node-instance-role-step), then save and close the file to apply the updated configmap\.

1. Watch the status of your nodes and wait for your new nodes to join your cluster and reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment down to 0 replicas to avoid conflicting scaling actions\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=0 -n kube-system
   ```

1. Use the following command to taint each of the nodes that you want to remove with `NoSchedule` so that new pods are not scheduled or rescheduled on the nodes you are replacing:

   ```
   kubectl taint nodes <node_name> key=value:NoSchedule
   ```

   If you are upgrading your nodes to a new Kubernetes version, you can identify and taint all of the nodes of a particular Kubernetes version \(in this case, 1\.15\) with the following code snippet\.

   ```
   K8S_VERSION=<1.15>
   nodes=$(kubectl get nodes -o jsonpath="{.items[?(@.status.nodeInfo.kubeletVersion==\"v$K8S_VERSION\")].metadata.name}")
   for node in ${nodes[@]}
   do
       echo "Tainting $node"
       kubectl taint nodes $node key=value:NoSchedule
   done
   ```

1. <a name="migrate-determine-dns-step"></a>Determine your cluster's DNS provider\.

   ```
   kubectl get deployments -l k8s-app=kube-dns -n kube-system
   ```

   Output \(this cluster is using `kube-dns` for DNS resolution, but your cluster may return `coredns` instead\):

   ```
   NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   <kube-dns>   1         1         1            1           31m
   ```

1. If your current deployment is running fewer than two replicas, scale out the deployment to two replicas\. Substitute `coredns` for `kube-dns` if your previous command output returned that instead\.

   ```
   kubectl scale deployments/<kube-dns> --replicas=2 -n kube-system
   ```

1. Drain each of the nodes that you want to remove from your cluster with the following command:

   ```
   kubectl drain <node_name> --ignore-daemonsets --delete-local-data
   ```

   If you are upgrading your nodes to a new Kubernetes version, you can identify and drain all of the nodes of a particular Kubernetes version \(in this case, 1\.15\) with the following code snippet\.

   ```
   K8S_VERSION=<1.15>
   nodes=$(kubectl get nodes -o jsonpath="{.items[?(@.status.nodeInfo.kubeletVersion==\"v$K8S_VERSION\")].metadata.name}")
   for node in ${nodes[@]}
   do
       echo "Draining $node"
       kubectl drain $node --ignore-daemonsets --delete-local-data
   done
   ```

1. After your old nodes have finished draining, revoke the security group ingress rules you authorized earlier, and then delete the AWS CloudFormation stack to terminate the instances\.
**Note**  
If you have attached any additional IAM policies to your old node group IAM role, such as adding permissions for the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)\), you must detach those additional policies from the role before you can delete your AWS CloudFormation stack\.

   1. Revoke the ingress rules that you created for your node security groups earlier\. In these commands, `oldNodes` is the AWS CloudFormation stack name for your older node stack, and `newNodes` is the name of the stack that you are migrating to\.

      ```
      oldNodes="<old_node_CFN_stack_name>"
      newNodes="<new_node_CFN_stack_name>"
      
      oldSecGroup=$(aws cloudformation describe-stack-resources --stack-name $oldNodes \
      --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].PhysicalResourceId' \
      --output text)
      newSecGroup=$(aws cloudformation describe-stack-resources --stack-name $newNodes \
      --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].PhysicalResourceId' \
      --output text)
      aws ec2 revoke-security-group-ingress --group-id $oldSecGroup \
      --source-group $newSecGroup --protocol -1
      aws ec2 revoke-security-group-ingress --group-id $newSecGroup \
      --source-group $oldSecGroup --protocol -1
      ```

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select your old node stack\.

   1. Choose **Actions**, then **Delete stack**\.

1. Edit the `aws-auth` configmap to remove the old node instance role from RBAC\.

   ```
   kubectl edit configmap -n kube-system aws-auth
   ```

   Delete the `mapRoles` entry for the old node group\. 

   ```
   apiVersion: v1
   data:
     mapRoles: |
       - rolearn: arn:aws:iam::111122223333:role/nodes-1-16-NodeInstanceRole-W70725MZQFF8
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
   <    - rolearn: arn:aws:iam::111122223333:role/nodes-1-15-NodeInstanceRole-U11V27W93CX5
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes>
   ```

   Save and close the file to apply the updated configmap\.

1. \(Optional\) If you are using the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), scale the deployment back to one replica\.
**Note**  
You must also tag your new Auto Scaling group appropriately \(for example, `k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<YOUR CLUSTER NAME>`\) and update your Cluster Autoscaler deployment's command to point to the newly tagged Auto Scaling group\. For more information, see [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/tree/cluster-autoscaler-release-1.3/cluster-autoscaler/cloudprovider/aws)\.

   ```
   kubectl scale deployments/cluster-autoscaler --replicas=1 -n kube-system
   ```

1. \(Optional\) Verify that you are using the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.

1. If your cluster is using `kube-dns` for DNS resolution \(see [previous step](#migrate-determine-dns-step)\), scale in the `kube-dns` deployment to one replica\.

   ```
   kubectl scale deployments/kube-dns --replicas=1 -n kube-system
   ```