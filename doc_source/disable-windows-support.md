# Disable Windows support<a name="disable-windows-support"></a>

**To disable Windows support on your cluster**

1. If your cluster contains Amazon Linux nodes and you use [security groups for Pods](security-groups-for-pods.md) with them, then skip this step\.

   Remove the `AmazonVPCResourceController` managed IAM policy from your [cluster role](cluster-iam-role.md)\. Replace `eksClusterRole` with the name of your cluster role and `111122223333` with your account ID\.

   ```
   aws iam detach-role-policy \
       --role-name eksClusterRole \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
   ```

1. Disable Windows IPAM in the `amazon-vpc-cni` ConfigMap\.

   ```
   kubectl patch configmap/amazon-vpc-cni \
                       -n kube-system \
                       --type merge \
                       -p '{"data":{"enable-windows-ipam":"false"}}'
   ```