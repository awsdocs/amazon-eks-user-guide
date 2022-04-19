# Troubleshooting issues in Amazon EKS Connector<a name="troubleshooting-connector"></a>

This topic covers some of the common errors that you might encounter while using the Amazon EKS Connector, including instructions on how to resolve them, workarounds, and frequently asked questions\.

## Common issues<a name="tsc-symptoms"></a>

This section describes how you can troubleshoot some functional issues that you might encounter while using Amazon EKS Connector\. It provides solutions and workarounds for these issues\.

### Console error: the cluster is stuck in the Pending state<a name="symp-pending"></a>

If, after you registered the cluster, the cluster gets stuck in the `Pending` state on the Amazon EKS console, it might be because Amazon EKS Connector didn't successfully connect the cluster to AWS yet\. For a registered cluster, the `Pending` state means that the connection wasn't already successfully established\. To resolve this issue, make sure that you have applied the manifest to the target Kubernetes cluster\. If you did apply it to the cluster but the cluster is still in the Pending state, then most likely Amazon EKS Connector might be unhealthy in your cluster\. To troubleshoot this issue, see the section that's named [Amazon EKS connector pods are crash looping ](#symp-loop)in this topic\. 

### Console error: User “system:serviceaccount:eks\-connector:eks\-connector” can't impersonate resource “users” in API group “” at cluster scope<a name="symp-imp"></a>

Amazon EKS Connector uses Kubernetes [user impersonation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#user-impersonation) to act on behalf of users from the AWS Management Console\. For each IAM identity that accesses the Kubernetes API from the AWS eks\-connector service account, they must be granted permission to impersonate the corresponding Kubernetes user with an IAM ARN as their user name\. In the following examples, the IAM ARN is mapped to a Kubernetes user\.
+ IAM user `john` from AWS account `111122223333` is mapped to a Kubernetes user\.

  ```
  arn:aws:iam::111122223333:user/john
  ```
+ IAM role `admin` from AWS account `111122223333` is mapped to a Kubernetes user:

  ```
  arn:aws:iam::111122223333:role/admin
  ```

  The result is an IAM role ARN, instead of the STS session ARN\.

For instructions on how to configure the `ClusterRole` and `ClusterRoleBinding` to grant `eks-connector` service account privilege to impersonate the mapped user, see [Granting access to a user to view a cluster](connector-grant-access.md)\. Make sure that, in the template, %IAM\_ARN% is replaced with IAM ARN of the AWS Management Console user\. 

### Console error: \.\.\. is forbidden: User \.\.\. cannot list resource “\.\.\. in API group” at the cluster scope<a name="symp-rbac"></a>

Consider the following problem\. The Amazon EKS Connector has successfully impersonated the requesting AWS Management Console user in the target Kubernetes cluster\. However, the impersonated user doesn't have RBAC permission on Kubernetes API operations\. 

To resolve this issues, as the cluster administrator, you must grant the appropriate level of RBAC privileges to individual Kubernetes users\. For more information and examples, see [Granting access to a user to view a cluster](connector-grant-access.md)\. 

### Console error: Amazon EKS can't communicate with your Kubernetes cluster API server\. The cluster must be in an ACTIVE state for successful connection\. Try again in few minutes\.<a name="symp-con"></a>

If the Amazon EKS service can't communicate with Amazon EKS connector in the target cluster, it might be because of one of the following reasons:
+ Amazon EKS Connector in the target cluster is unhealthy\.
+ Poor connectivity or an interrupted connection between the target cluster and the AWS Region\.

To resolve this, check the [Inspect logs of Amazon EKS Connector](#tsc-logs)\. If you don't see an error for the Amazon EKS connector, retry the connection after a few minutes\. If you regularly experience high latency or intermittent connectivity for the target cluster, consider re\-registering the cluster to an AWS Region that's located closer to you\.

### Amazon EKS connector pods are crash looping<a name="symp-loop"></a>

There are many reasons that can cause an EKS connector pod to enter the CrashLoopBackOff status\. This issue likely involves the connector\-init container\. In the following example, it was the connector\-init container that entered the CrashLoopBackOff status\.

```
kubectl get pods -n eks-connector
NAME              READY   STATUS                  RESTARTS   AGE
eks-connector-0   0/2     Init:CrashLoopBackOff   1          7s
```

To troubleshoot this issue, [Inspect logs of Amazon EKS Connector](#tsc-logs)\.

### failed to initiate eks\-connector: InvalidActivation<a name="symp-regis"></a>

When you start Amazon EKS Connector for the first time, it registers an `activationId` and `activationCode` with Amazon Web Services\. The registration might fail, which can cause the `connector-init` container to crash\.

```
F1116 20:30:47.261469       1 init.go:43] failed to initiate eks-connector: InvalidActivation:
```

To troubleshoot this issue, consider the following causes and recommended fixes:
+ Registration might have failed because the activationId and activationCode aren't in your manifest file\. If this is the case, make sure that they are the correct values that were returned from the RegisterCluster API operation, and that the activationCode is in the manifest file\. The activationCode is added to Kubernetes secrets, so it must be base64 encoded\. For more information, see [Step 1: Registering the cluster](connecting-cluster.md#connector-connecting)\.
+ Registration might have failed because your activation expired\. This is because, for security reasons, you must activate the EKS connector within 3 days after registering the cluster\. To resolve this issue, make sure that the EKS connector manifest is applied to the target Kubernetes cluster before the expiry date and time\. To confirm your activation expiry date, call the DescribeCluster API operation\. In the following example response, the expiry date and time is recorded as 2021\-11\-12T22:28:51\.101000\-08:00\. 

  ```
  aws eks describe-cluster --name my-cluster
  {
      "cluster": {
          "name": "my-cluster",
          "arn": "arn:aws:eks:us-east-1:123456789012:cluster/my-cluster",
          "createdAt": "2021-11-09T22:28:51.449000-08:00",
          "status": "FAILED",
          "tags": {
          },
          "connectorConfig": {
              "activationId": "00000000-0000-0000-0000-000000000000",
              "activationExpiry": "2021-11-12T22:28:51.101000-08:00",
              "provider": "OTHER",
              "roleArn": "arn:aws:iam::123456789012:role/my-connector-role"
          }
      }
  }
  ```

  If the `activationExpiry` passed, deregister the cluster and register it again\. Do this generates a new activation\.

### Cluster worker node is missing outbound connectivity<a name="symp-out"></a>

To work properly, EKS connector requires outbound connectivity to several AWS endpoints\. You can't connect a private cluster without outbound connectivity to a target AWS Region\. To resolve this issue, you must add the necessary outbound connectivity\. For information about connector requirements, see [Amazon EKS Connector considerations](eks-connector.md#connect-cluster-reqts)\. 



### Amazon EKS connector pods are in ImagePullBackOff state<a name="symp-img"></a>

If you run the getpods command and pods are in the ImagePullBackOff state, they can't work properly\. If EKS Connector pod is in `ImagePullBackOff` state, they can’t work properly\. See the example below:

```
 kubectl get pods -n eks-connector
 NAME              READY   STATUS                  RESTARTS   AGE
 eks-connector-0   0/2     Init:ImagePullBackOff   0          4s
```

The default Amazon EKS Connector manifest file references images from [Amazon ECR Public Registry](https://gallery.ecr.aws/)\. It is possible that the target Kubernetes cluster cannot pull images from Amazon ECR Public\. Either resolve the Amazon ECR Public image pull issue, or consider mirroring the images in the private container registry of your choice\.

## Frequently asked questions<a name="tsc-faq"></a>

**Q: How does the underlying technology behind Amazon EKS Connector work?**  
A: The Amazon EKS Connector is based on the System Manager \(SSM\) Agent\. The EKS Connector runs as a StatefulSet on your Kubernetes cluster\. It establishes a connection and proxies the communication between the API server of your cluster and Amazon Web Services\. It does this to display cluster data in the Amazon EKS console until you disconnect the cluster from AWS\. SSM agent is an open source project\. For more information about this project, see the [GitHub project page](https://github.com/aws/amazon-ssm-agent)\.

**Q: I have an on\-premises Kubernetes cluster that I want to connect\. Do I need to open firewall ports to connect it?**  
A: No, you don't need to open any firewall ports\. The Kubernetes cluster only requires outbound connection to AWS Regions\. AWS services never access resources in your on\-premises network\. The Amazon EKS Connector runs on your cluster and initiates the connection to AWS\. When the cluster registration completes, AWS only issues commands to the Amazon EKS Connector after you start an action from the Amazon EKS console that requires information from the Kubernetes API server on your cluster\.

**Q: What data is sent from my cluster to AWS by the Amazon EKS Connector?**  
A: The Amazon EKS Connector sends technical information that's necessary for your cluster to be registered on AWS\. It also sends cluster and workload metadata for the Amazon EKS console features that customers request\. Amazon EKS Connector only gathers or sends this data if you start an action from the Amazon EKS console or the Amazon EKS API that necessitates the data to be sent to AWS\. Other than the Kubernetes version number, AWS doesn't store any data by default\. It stores them only if you authorize it\.

**Q: Can I connect a cluster outside of an AWS Region?**  
A: Yes, you can connect a cluster from any location to Amazon EKS\. Moreover, your EKS service can be located in any AWS public commercial AWS Region\. This works with a valid network connection from your cluster to the target AWS Region\. We recommend that you pick an AWS Region, which is the closest to your cluster location for UI performance optimization\. For example, if you have a cluster running in Tokyo, connect your cluster to the AWS Region in Tokyo \(that is, the `ap-northeast-1` AWS Region\) for low latency\. You can connect a cluster from any location to the Amazon EKS in any of the public commercial AWS Regions, except the China or GovCloud AWS Regions\.

## Basic troubleshooting<a name="tsc-steps"></a>

This section describes steps to diagnose the issue if it’s unclear\.

### Check Amazon EKS Connector status<a name="tsc-check"></a>

Check the Amazon EKS Connector status by using the following commands\.

```
kubectl get pods -n eks-connector
```

There are two `eks-connector-x` pods in the Running state\.

### Inspect logs of Amazon EKS Connector<a name="tsc-logs"></a>

The Amazon EKS Connector Pod consists of three containers\. You can inspect the logs of all three of them\.
+ `connector-init`
+ `connector-proxy`
+ `connector-agent`

To retrieve full logs for all of these containers so that you can inspect them, run the following commands\.
+ 

  ```
  # Retrieve log for connector-init container
  kubectl logs eks-connector-0 --container connector-init -n eks-connector
  kubectl logs eks-connector-1 --container connector-init -n eks-connector
  ```
+ 

  ```
  # Retrieve log for connector-proxy container
  kubectl logs eks-connector-0 --container connector-proxy -n eks-connector
  kubectl logs eks-connector-1 --container connector-proxy -n eks-connector
  ```
+ 

  ```
  # Retrieve log for connector-agent container
  kubectl exec eks-connector-0 --container connector-agent -n eks-connector -- cat /var/log/amazon/ssm/amazon-ssm-agent.log
  kubectl exec eks-connector-1 --container connector-agent -n eks-connector -- cat /var/log/amazon/ssm/amazon-ssm-agent.log
  ```

### Get the effective cluster name<a name="tsc-name"></a>

Amazon EKS clusters are uniquely identified by `clusterName` within a single AWS account and AWS Region\. If you have multiple connected clusters in Amazon EKS, you can confirm which Amazon EKS cluster that the current Kubernetes cluster is registered\. To do this, enter the following to find out the `clusterName` of the current cluster\. 

```
kubectl exec eks-connector-0 --container connector-agent -n eks-connector \
  -- cat /var/log/amazon/ssm/amazon-ssm-agent.log \
  | grep -m1 -oE "eks_c:[a-zA-Z0-9_-]+" \
  | sed -E "s/^.*eks_c:([a-zA-Z0-9_-]+)_[a-zA-Z0-9]+.*$/\1/"
kubectl exec eks-connector-1 --container connector-agent -n eks-connector \
  -- cat /var/log/amazon/ssm/amazon-ssm-agent.log \
  | grep -m1 -oE "eks_c:[a-zA-Z0-9_-]+" \
  | sed -E "s/^.*eks_c:([a-zA-Z0-9_-]+)_[a-zA-Z0-9]+.*$/\1/"
```

### Miscellaneous commands<a name="tsc-misc"></a>

The following commands are useful to retrieve information that you need to troubleshoot issues\.
+ Use the following command to gather images that's used by pods in Amazon EKS Connector\.

  ```
  kubectl get pods -n eks-connector -o jsonpath="{.items[*].spec.containers[*].image}" \
    | tr -s '[[:space:]]' '\n'
  ```
+ Use the following command to gather worker node names that Amazon EKS Connector is running on\.

  ```
  kubectl get pods -n eks-connector -o jsonpath="{.items[*].spec.nodeName}" \
    | tr -s '[[:space:]]' '\n'
  ```
+ Run the following command to get your Kubernetes client and server versions\.

  ```
  kubectl version
  ```
+ Run the following command to get information about your worker nodes\.

  ```
  kubectl get nodes -o wide --show-labels
  ```