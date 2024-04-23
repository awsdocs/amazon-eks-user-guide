# Troubleshooting issues in Amazon EKS Connector<a name="troubleshooting-connector"></a>

This topic covers some of the common errors that you might encounter while using the Amazon EKS Connector, including instructions on how to resolve them and workarounds\.

## Basic troubleshooting<a name="tsc-steps"></a>

This section describes steps to diagnose the issue if it's unclear\.

### Check Amazon EKS Connector status<a name="tsc-check"></a>

Check the Amazon EKS Connector status\.

```
kubectl get pods -n eks-connector
```

### Inspect Amazon EKS Connector logs<a name="tsc-logs"></a>

The Amazon EKS Connector Pod consists of three containers\. To retrieve full logs for all of these containers so that you can inspect them, run the following commands:
+ `connector-init`

  ```
  kubectl logs eks-connector-0 --container connector-init -n eks-connector
  kubectl logs eks-connector-1 --container connector-init -n eks-connector
  ```
+ `connector-proxy`

  ```
  kubectl logs eks-connector-0 --container connector-proxy -n eks-connector
  kubectl logs eks-connector-1 --container connector-proxy -n eks-connector
  ```
+ `connector-agent`

  ```
  kubectl exec eks-connector-0 --container connector-agent -n eks-connector -- cat /var/log/amazon/ssm/amazon-ssm-agent.log
  kubectl exec eks-connector-1 --container connector-agent -n eks-connector -- cat /var/log/amazon/ssm/amazon-ssm-agent.log
  ```

### Get the effective cluster name<a name="tsc-name"></a>

Amazon EKS clusters are uniquely identified by `clusterName` within a single AWS account and AWS Region\. If you have multiple connected clusters in Amazon EKS, you can confirm which Amazon EKS cluster that the current Kubernetes cluster is registered to\. To do this, enter the following to find out the `clusterName` of the current cluster\. 

```
kubectl exec eks-connector-0 --container connector-agent -n eks-connector \
  -- cat /var/log/amazon/ssm/amazon-ssm-agent.log | grep -m1 -oE "eks_c:[a-zA-Z0-9_-]+" | sed -E "s/^.*eks_c:([a-zA-Z0-9_-]+)_[a-zA-Z0-9]+.*$/\1/"
kubectl exec eks-connector-1 --container connector-agent -n eks-connector \
  -- cat /var/log/amazon/ssm/amazon-ssm-agent.log | grep -m1 -oE "eks_c:[a-zA-Z0-9_-]+" | sed -E "s/^.*eks_c:([a-zA-Z0-9_-]+)_[a-zA-Z0-9]+.*$/\1/"
```

### Miscellaneous commands<a name="tsc-misc"></a>

The following commands are useful to retrieve information that you need to troubleshoot issues\.
+ Use the following command to gather images that's used by Pods in Amazon EKS Connector\.

  ```
  kubectl get pods -n eks-connector -o jsonpath="{.items[*].spec.containers[*].image}" | tr -s '[[:space:]]' '\n'
  ```
+ Use the following command to determine the node names that Amazon EKS Connector is running on\.

  ```
  kubectl get pods -n eks-connector -o jsonpath="{.items[*].spec.nodeName}" | tr -s '[[:space:]]' '\n'
  ```
+ Run the following command to get your Kubernetes client and server versions\.

  ```
  kubectl version
  ```
+ Run the following command to get information about your nodes\.

  ```
  kubectl get nodes -o wide --show-labels
  ```

## Helm issue: 403 Forbidden<a name="w735aac58c33b9"></a>

If you received the following error when running helm install commands:

```
Error: INSTALLATION FAILED: unexpected status from HEAD request to https://public.ecr.aws/v2/eks-connector/eks-connector-chart/manifests/0.0.6: 403 Forbidden
```

You can run the following line to fix it:

```
docker logout public.ecr.aws
```

## Console error: the cluster is stuck in the Pending state<a name="symp-pending"></a>

If the cluster gets stuck in the `Pending` state on the Amazon EKS console after you're registered it, it might be because the Amazon EKS Connector didn't successfully connect the cluster to AWS yet\. For a registered cluster, the `Pending` state means that the connection isn't successfully established\. To resolve this issue, make sure that you have applied the manifest to the target Kubernetes cluster\. If you applied it to the cluster, but the cluster is still in the `Pending` state, then the `eks-connector` statefulset might be unhealthy\. To troubleshoot this issue, see [Amazon EKS connector Pods are crash looping ](#symp-loop)in this topic\.

## Console error: `User “system:serviceaccount:eks-connector:eks-connector” can't impersonate resource “users” in API group “”` at cluster scope<a name="symp-imp"></a>

The Amazon EKS Connector uses Kubernetes [user impersonation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#user-impersonation) to act on behalf of [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) from the AWS Management Console\. Each principal that accesses the Kubernetes API from the AWS `eks-connector` service account must be granted permission to impersonate the corresponding Kubernetes user with an IAM ARN as its Kubernetes user name\. In the following examples, the IAM ARN is mapped to a Kubernetes user\.
+ IAM user `john` from AWS account `111122223333` is mapped to a Kubernetes user\. [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) recommend that you grant permissions to roles instead of users\.

  ```
  arn:aws:iam::111122223333:user/john
  ```
+ IAM role `admin` from AWS account `111122223333` is mapped to a Kubernetes user:

  ```
  arn:aws:iam::111122223333:role/admin
  ```

  The result is an IAM role ARN, instead of the AWS STS session ARN\.

For instructions on how to configure the `ClusterRole` and `ClusterRoleBinding` to grant the `eks-connector` service account privilege to impersonate the mapped user, see [Granting access to an IAM principal to view Kubernetes resources on a cluster](connector-grant-access.md)\. Make sure that in the template, `%IAM_ARN%` is replaced with the IAM ARN of the AWS Management Console IAM principal\. 

## Console error: `[...] is forbidden: User [...] cannot list resource “[...] in API group”` at the cluster scope<a name="symp-rbac"></a>

Consider the following problem\. The Amazon EKS Connector has successfully impersonated the requesting AWS Management Console IAM principal in the target Kubernetes cluster\. However, the impersonated principal doesn't have RBAC permission for Kubernetes API operations\. 

To resolve this issue, there are two methods to give permissions to additional users\. If you previously installed eks\-connector via helm chart, you can easily grant users access by running the following command\. Replace the `userARN1` and `userARN2` with a list of the ARNs of the IAM roles to give access to view the Kubernetes resources:

```
helm upgrade eks-connector oci://public.ecr.aws/eks-connector/eks-connector-chart \
    --reuse-values \
    --set 'authentication.allowedUserARNs={userARN1,userARN2}'
```

 Or, as the cluster administrator, grant the appropriate level of RBAC privileges to individual Kubernetes users\. For more information and examples, see [Granting access to an IAM principal to view Kubernetes resources on a cluster](connector-grant-access.md)\. 

## Console error: **Amazon EKS can't communicate with your Kubernetes cluster API server\. The cluster must be in an ACTIVE state for successful connection\. Try again in few minutes\.**<a name="symp-con"></a>

If the Amazon EKS service can't communicate with the Amazon EKS connector in the target cluster, it might be because of one of the following reasons:
+ The Amazon EKS Connector in the target cluster is unhealthy\.
+ Poor connectivity or an interrupted connection between the target cluster and the AWS Region\.

To resolve this problem, check the [Amazon EKS Connector logs](#tsc-logs)\. If you don't see an error for the Amazon EKS Connector, retry the connection after a few minutes\. If you regularly experience high latency or intermittent connectivity for the target cluster, consider re\-registering the cluster to an AWS Region that's located closer to you\.

## Amazon EKS connector Pods are crash looping<a name="symp-loop"></a>

There are many reasons that can cause an Amazon EKS connector Pod to enter the `CrashLoopBackOff` status\. This issue likely involves the `connector-init` container\. Check the status of the Amazon EKS connector Pod\.

```
kubectl get pods -n eks-connector
```

An example output is as follows\.

```
NAME              READY   STATUS                  RESTARTS   AGE
eks-connector-0   0/2     Init:CrashLoopBackOff   1          7s
```

If your output is similar to the previous output, see [Inspect Amazon EKS Connector logs](#tsc-logs) to troubleshoot the issue\.

## `Failed to initiate eks-connector: InvalidActivation`<a name="symp-regis"></a>

When you start the Amazon EKS Connector for the first time, it registers an `activationId` and `activationCode` with Amazon Web Services\. The registration might fail, which can cause the `connector-init` container to crash with an error similar to the following error\.

```
F1116 20:30:47.261469       1 init.go:43] failed to initiate eks-connector: InvalidActivation:
```

To troubleshoot this issue, consider the following causes and recommended fixes:
+ Registration might have failed because the `activationId` and `activationCode` aren't in your manifest file\. If this is the case, make sure that they are the correct values that were returned from the `RegisterCluster` API operation, and that the `activationCode` is in the manifest file\. The `activationCode` is added to Kubernetes secrets, so it must be `base64` encoded\. For more information, see [Step 1: Registering the cluster](connecting-cluster.md#connector-connecting)\.
+ Registration might have failed because your activation expired\. This is because, for security reasons, you must activate the Amazon EKS Connector within three days after registering the cluster\. To resolve this issue, make sure that the Amazon EKS Connector manifest is applied to the target Kubernetes cluster before the expiry date and time\. To confirm your activation expiry date, call the `DescribeCluster` API operation\.

  ```
  aws eks describe-cluster --name my-cluster
  ```

   In the following example response, the expiry date and time is recorded as `2021-11-12T22:28:51.101000-08:00`\. 

  ```
  {
      "cluster": {
          "name": "my-cluster",
          "arn": "arn:aws:eks:region:111122223333:cluster/my-cluster",
          "createdAt": "2021-11-09T22:28:51.449000-08:00",
          "status": "FAILED",
          "tags": {
          },
          "connectorConfig": {
              "activationId": "00000000-0000-0000-0000-000000000000",
              "activationExpiry": "2021-11-12T22:28:51.101000-08:00",
              "provider": "OTHER",
              "roleArn": "arn:aws:iam::111122223333:role/my-connector-role"
          }
      }
  }
  ```

  If the `activationExpiry` passed, deregister the cluster and register it again\. Do this generates a new activation\.

## Cluster node is missing outbound connectivity<a name="symp-out"></a>

To work properly, the Amazon EKS Connector requires outbound connectivity to several AWS endpoints\. You can't connect a private cluster without outbound connectivity to a target AWS Region\. To resolve this issue, you must add the necessary outbound connectivity\. For information about connector requirements, see [Amazon EKS Connector considerations](eks-connector.md#connect-cluster-reqts)\. 

## Amazon EKS connector Pods are in `ImagePullBackOff` state<a name="symp-img"></a>

If you run the `get pods` command and Pods are in the `ImagePullBackOff` state, they can't work properly\. If the Amazon EKS Connector Pods are in the `ImagePullBackOff` state, they can't work properly\. Check the status of your Amazon EKS Connector Pods\.

```
kubectl get pods -n eks-connector
```

An example output is as follows\.

```
NAME              READY   STATUS                  RESTARTS   AGE
eks-connector-0   0/2     Init:ImagePullBackOff   0          4s
```

The default Amazon EKS Connector manifest file references images from the [Amazon ECR Public Gallery](https://gallery.ecr.aws/)\. It's possible that the target Kubernetes cluster can't pull images from the Amazon ECR Public Gallery\. Either resolve the Amazon ECR Public Gallery image pull issue, or consider mirroring the images in the private container registry of your choice\.