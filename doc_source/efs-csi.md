# Amazon EFS CSI driver<a name="efs-csi"></a>

The [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) provides a CSI interface that allows Kubernetes clusters running on AWS to manage the lifecycle of Amazon EFS file systems\.

This topic shows you how to deploy the Amazon EFS CSI Driver to your Amazon EKS cluster and verify that it works\.

**Note**  
Alpha features of the Amazon EFS CSI Driver aren't supported on Amazon EKS clusters\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) project on GitHub\.

**Considerations**
+ The Amazon EFS CSI Driver isn't compatible with Windows\-based container images\.
+ You can't use dynamic persistent volume provisioning with Fargate nodes, but you can use static provisioning\.
+ Dynamic provisioning requires 1\.2 or later of the driver, which requires a 1\.17 or later cluster\. You can statically provision persistent volumes using 1\.1 of the driver on any [supported Amazon EKS cluster version](kubernetes-versions.md)\.
+ Version 1\.3\.2 or later of this driver supports the Arm64 architecture, including Amazon EC2 Graviton\-based instances\.

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version 2\.6\.3 or later or 1\.23\.11 or later of the AWS CLI installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ The `kubectl` command line tool installed on your computer or AWS CloudShell\. The version must be the same, or up to one minor version earlier or later than your cluster version\. For example, if your cluster is version 1\.21, then your `kubectl` version can be version 1\.22 or 1\.20\. To install or upgrade `kubectl`, see [Installing `kubectl`](install-kubectl.md)\.

**Note**  
A pod running on AWS Fargate automatically mounts an Amazon EFS file system, without needing the manual driver installation steps described on this page\.

## Create an IAM policy and role<a name="efs-create-iam-resources"></a>

Create an IAM policy and assign it to an IAM role\. The policy will allow the Amazon EFS driver to interact with your file system\.

**To deploy the Amazon EFS CSI driver to an Amazon EKS cluster**

1. Create an IAM policy that allows the CSI driver's service account to make calls to AWS APIs on your behalf\.

   1. Download the IAM policy document from GitHub\. You can also view the [policy document](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/iam-policy-example.json)\.

      ```
      curl -o iam-policy-example.json https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/docs/iam-policy-example.json
      ```

   1. Create the policy\. You can change `AmazonEKS_EFS_CSI_Driver_Policy` to a different name, but if you do, make sure to change it in later steps too\.

      ```
      aws iam create-policy \
          --policy-name AmazonEKS_EFS_CSI_Driver_Policy \
          --policy-document file://iam-policy-example.json
      ```

1. Create an IAM role and attach the IAM policy to it\. Annotate the Kubernetes service account with the IAM role ARN and the IAM role with the Kubernetes service account name\. You can create the role using `eksctl` or the AWS CLI\.

------
#### [ eksctl ]

   Run the following command to create the IAM role and Kubernetes service account\. It also attaches the policy to the role, annotates the Kubernetes service account with the IAM role ARN, and adds the Kubernetes service account name to the trust policy for the IAM role\. Replace `my-cluster` with your cluster name and `111122223333` with your account ID\. Replace *region\-code* with the AWS Region that your cluster is in\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-East\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   eksctl create iamserviceaccount \
       --cluster my-cluster \
       --namespace kube-system \
       --name efs-csi-controller-sa \
       --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_EFS_CSI_Driver_Policy \
       --approve \
       --region region-code
   ```

------
#### [ AWS CLI ]

   1. Determine your cluster's OIDC provider URL\. Replace `my-cluster` with your cluster name\. If the output from the command is `None`, review the **Prerequisites**\.

      ```
      aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
      ```

      The example output is as follows\.

      ```
      https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
      ```

   1. Create the IAM role, granting the Kubernetes service account the `AssumeRoleWithWebIdentity` action\.

      1. Copy the following contents to a file named `trust-policy.json`\. Replace `111122223333` with your account ID\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` and `region-code` with the values returned in the previous step\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-East\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

         ```
         {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Principal": {
                 "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
               },
               "Action": "sts:AssumeRoleWithWebIdentity",
               "Condition": {
                 "StringEquals": {
                   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:efs-csi-controller-sa"
                 }
               }
             }
           ]
         }
         ```

      1. Create the role\. You can change `AmazonEKS_EFS_CSI_DriverRole` to a different name, but if you do, make sure to change it in later steps too\.

         ```
         aws iam create-role \
           --role-name AmazonEKS_EFS_CSI_DriverRole \
           --assume-role-policy-document file://"trust-policy.json"
         ```

   1. Attach the IAM policy to the role\. Replace `111122223333` with your account ID\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-East\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:` before running the following command\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_EFS_CSI_Driver_Policy \
        --role-name AmazonEKS_EFS_CSI_DriverRole
      ```

   1. Create a Kubernetes service account that's annotated with the ARN of the IAM role that you created\.

      1. Save the following contents to a file named `efs-service-account.yaml`\. Replace `111122223333` with your account ID\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-East\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

         ```
         ---
         apiVersion: v1
         kind: ServiceAccount
         metadata:
           labels:
             app.kubernetes.io/name: aws-efs-csi-driver
           name: efs-csi-controller-sa
           namespace: kube-system
           annotations:
             eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/AmazonEKS_EFS_CSI_DriverRole
         ```

      1. Create the Kubernetes service account on your cluster\. The Kubernetes service account named `efs-csi-controller-sa` is annotated with the IAM role that you created named `AmazonEKS_EFS_CSI_DriverRole`\.

         ```
         kubectl apply -f efs-service-account.yaml
         ```

------

## Install the Amazon EFS driver<a name="efs-install-driver"></a>

Install the Amazon EFS CSI driver using Helm or a manifest\.

**Important**  
The following steps require a 1\.17 or later cluster\. If you're installing the driver on a cluster that's earlier than version 1\.17, you need to install version 1\.1 of the driver\. For more information, see [Amazon EFS CSI driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) on GitHub\.
Encryption of data in transit using TLS is enabled by default\. Using [encryption in transit](http://aws.amazon.com/blogs/aws/new-encryption-of-data-in-transit-for-amazon-efs/), data is encrypted during its transition over the network to the Amazon EFS service\. To disable it and mount volumes using NFSv4, set the `volumeAttributes` field `encryptInTransit` to `"false"` in your persistent volume manifest\. For an example manifest, see [Encryption in Transit example](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/encryption_in_transit/specs/pv.yaml) on GitHub\.

------
#### [ Helm ]

This procedure requires Helm V3 or later\. To install or upgrade Helm, see [Using Helm with Amazon EKS](helm.md)\.

**To install the driver using Helm**

1. Add the Helm repo\.

   ```
   helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver/
   ```

1. Update the repo\.

   ```
   helm repo update
   ```

1. Install a release of the driver using the Helm chart\. Replace the repository address with the cluster's [container image address](add-ons-images.md)\.

   ```
   helm upgrade -i aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver \
       --namespace kube-system \
       --set image.repository=602401143452.dkr.ecr.region-code.amazonaws.com/eks/aws-efs-csi-driver \
       --set controller.serviceAccount.create=false \
       --set controller.serviceAccount.name=efs-csi-controller-sa
   ```

------
#### [ Manifest \(private registry\) ]

If you want to download the image with a manifest, we recommend first trying these steps to pull secured images from the private Amazon ECR registry\.

**To install the driver using images stored in the private Amazon ECR registry**

1. Download the manifest\.

   ```
   kubectl kustomize \
       "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/ecr?ref=release-1.3" > private-ecr-driver.yaml
   ```
**Note**  
If you encounter an issue that you aren't able to resolve by adding IAM permissions, try the "Manifest \(public registry\)" steps instead\.

1. In the following command, replace `region-code` with the AWS Region that your cluster is in and then run the modified command to replace `us-west-2` in the file with your AWS Region\.

   ```
   sed -i.bak -e 's|us-west-2|region-code|' private-ecr-driver.yaml
   ```

1. Replace `account` in the following command with the account from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in and then run the modified command to replace `602401143452` in the file\.

   ```
   sed -i.bak -e 's|602401143452|account|' private-ecr-driver.yaml
   ```

1. Edit the `private-ecr-driver.yaml` file and remove the following lines that create a Kubernetes service account\. These lines aren't needed because the service account was created in a previous step\.

   ```
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     labels:
       app.kubernetes.io/name: aws-efs-csi-driver
     name: efs-csi-controller-sa
     namespace: kube-system
   ---
   ```

1. Apply the manifest\.

   ```
   kubectl apply -f private-ecr-driver.yaml
   ```

------
#### [ Manifest \(public registry\) ]

For some situations, you may not be able to add the necessary IAM permissions to pull from the private Amazon ECR registry\. One example of this scenario is if your IAM user or role isn't allowed to authenticate with someone else's account\. When this is true, you can use the public Amazon ECR registry\.

**To install the driver using images stored in the public Amazon ECR registry**

1. Download the manifest\.

   ```
   kubectl kustomize \
       "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.3" > public-ecr-driver.yaml
   ```

1. Edit the file and remove the following lines that create a Kubernetes service account\. This isn't necessary because the service account was created in a previous step\. 

   ```
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     labels:
       app.kubernetes.io/name: aws-efs-csi-driver
     name: efs-csi-controller-sa
     namespace: kube-system
   ---
   ```

1. Apply the manifest\.

   ```
   kubectl apply -f public-ecr-driver.yaml
   ```

------

## Create an Amazon EFS file system<a name="efs-create-filesystem"></a>

The Amazon EFS CSI driver supports [Amazon EFS access points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html), which are application\-specific entry points into an Amazon EFS file system that make it easier to share a file system between multiple pods\. Access points can enforce a user identity for all file system requests that are made through the access point, and enforce a root directory for each pod\. For more information, see [Amazon EFS access points](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/access_points/README.md) on GitHub\.

**Important**  
You must complete the following steps in the same terminal because variables are set and used across the steps\.

**To create an Amazon EFS file system for your Amazon EKS cluster**

1. Retrieve the VPC ID that your cluster is in and store it in a variable for use in a later step\. Replace `my-cluster` with your cluster name\.

   ```
   vpc_id=$(aws eks describe-cluster \
       --name my-cluster \
       --query "cluster.resourcesVpcConfig.vpcId" \
       --output text)
   ```

1. Retrieve the CIDR range for your cluster's VPC and store it in a variable for use in a later step\.

   ```
   cidr_range=$(aws ec2 describe-vpcs \
       --vpc-ids $vpc_id \
       --query "Vpcs[].CidrBlock" \
       --output text)
   ```

1. Create a security group with an inbound rule that allows inbound NFS traffic for your Amazon EFS mount points\.

   1. Create a security group\. Replace the *`example values`* with your own\.

      ```
      security_group_id=$(aws ec2 create-security-group \
          --group-name MyEfsSecurityGroup \
          --description "My EFS security group" \
          --vpc-id $vpc_id \
          --output text)
      ```

   1. Create an inbound rule that allows inbound NFS traffic from the CIDR for your cluster's VPC\.

      ```
      aws ec2 authorize-security-group-ingress \
          --group-id $security_group_id \
          --protocol tcp \
          --port 2049 \
          --cidr $cidr_range
      ```
**Important**  
To further restrict access to your file system, you can use the CIDR for your subnet instead of the VPC\.

1. Create an Amazon EFS file system for your Amazon EKS cluster\.

   1. Create a file system\. Replace *region\-code* with the AWS Region that your cluster is in\.

      ```
      file_system_id=$(aws efs create-file-system \
          --region region-code \
          --performance-mode generalPurpose \
          --query 'FileSystemId' \
          --output text)
      ```

   1. Create mount targets\.

      1. Determine the IP address of your cluster nodes\.

         ```
         kubectl get nodes
         ```

         The example output is as follows\.

         ```
         NAME                                         STATUS   ROLES    AGE   VERSION
         ip-192-168-56-0.region-code.compute.internal   Ready    <none>   19m   v1.19.6-eks-49a6c0
         ```

      1. Determine the IDs of the subnets in your VPC and which Availability Zone the subnet is in\.

         ```
         aws ec2 describe-subnets \
             --filters "Name=vpc-id,Values=$vpc_id" \
             --query 'Subnets[*].{SubnetId: SubnetId,AvailabilityZone: AvailabilityZone,CidrBlock: CidrBlock}' \
             --output table
         ```

         The example output is as follows\.

         ```
         |                           DescribeSubnets                          |
         +------------------+--------------------+----------------------------+
         | AvailabilityZone |     CidrBlock      |         SubnetId           |
         +------------------+--------------------+----------------------------+
         |  region-codec    |  192.168.128.0/19  |  subnet-EXAMPLE6e421a0e97  |
         |  region-codeb    |  192.168.96.0/19   |  subnet-EXAMPLEd0503db0ec  |
         |  region-codec    |  192.168.32.0/19   |  subnet-EXAMPLEe2ba886490  |
         |  region-codeb    |  192.168.0.0/19    |  subnet-EXAMPLE123c7c5182  |
         |  region-codea    |  192.168.160.0/19  |  subnet-EXAMPLE0416ce588p  |
         +------------------+--------------------+----------------------------+
         ```

      1. Add mount targets for the subnets that your nodes are in\. From the output in the previous two steps, the cluster has one node with an IP address of `192.168.56.0`\. That IP address is within the `CidrBlock` of the subnet with the ID `subnet-EXAMPLEe2ba886490`\. As a result, the following command creates a mount target for the subnet the node is in\. If there were more nodes in the cluster, you'd run the command once for a subnet in each AZ that you had a node in, replacing `subnet-EXAMPLEe2ba886490` with the appropriate subnet ID\.

         ```
         aws efs create-mount-target \
             --file-system-id $file_system_id \
             --subnet-id subnet-EXAMPLEe2ba886490 \
             --security-groups $security_group_id
         ```

## Deploy a sample application<a name="efs-sample-app"></a>

You can deploy a sample app that dynamically creates a persistent volume, or you can manually create a persistent volume\. You can replace the examples given in this section with a different application\.

------
#### [ Dynamic ]

**Important**  
You can't use dynamic provisioning with Fargate nodes\.

**Prerequisite**  
You must use version 1\.2x or later of the Amazon EFS CSI driver, which requires a 1\.17 or later cluster\. To update your cluster, see [Updating a cluster](update-cluster.md)\.

**To deploy a sample application that uses a persistent volume that the controller creates**

This procedure uses the [Dynamic Provisioning](https://github.com/kubernetes-sigs/aws-efs-csi-driver/tree/master/examples/kubernetes/dynamic_provisioning) example from the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub repository\. It dynamically creates a persistent volume through [Amazon EFS access points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html) and a Persistent Volume Claim \(PVC\) that's consumed by a pod\.

1. Create a storage class for EFS\. For all parameters and configuration options, see [Amazon EFS CSI Driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) on GitHub\.

   1. Retrieve your Amazon EFS file system ID\. You can find this in the Amazon EFS console, or use the following AWS CLI command\.

      ```
      aws efs describe-file-systems --query "FileSystems[*].FileSystemId" --output text
      ```

      The example output is as follows\.

      ```
      fs-582a03f3
      ```

   1. Download a `StorageClass` manifest for Amazon EFS\.

      ```
      curl -o storageclass.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/storageclass.yaml
      ```

   1. Edit the file\. Find the following line, and replace the value for `fileSystemId` with your file system ID\.

      ```
      fileSystemId: fs-582a03f3
      ```

   1. Deploy the storage class\.

      ```
      kubectl apply -f storageclass.yaml
      ```

1. Test automatic provisioning by deploying a Pod that makes use of the `PersistentVolumeClaim`: 

   1. Download a manifest that deploys a pod and a PersistentVolumeClaim\.

      ```
      curl -o pod.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/pod.yaml
      ```

   1. Deploy the pod with a sample app and the PersistentVolumeClaim used by the pod\.

      ```
      kubectl apply -f pod.yaml
      ```

1. Determine the names of the pods running the controller\.

   ```
   kubectl get pods -n kube-system | grep efs-csi-controller
   ```

   The example output is as follows\.

   ```
   efs-csi-controller-74ccf9f566-q5989   3/3     Running   0          40m
   efs-csi-controller-74ccf9f566-wswg9   3/3     Running   0          40m
   ```

1. After few seconds, you can observe the controller picking up the change \(edited for readability\)\. Replace *74ccf9f566\-q5989* with a value from one of the pods in your output from the previous command\.

   ```
   kubectl logs efs-csi-controller-74ccf9f566-q5989 \
       -n kube-system \
       -c csi-provisioner \
       --tail 10
   ```

   The example output is as follows\.

   ```
   ...
   1 controller.go:737] successfully created PV pvc-5983ffec-96cf-40c1-9cd6-e5686ca84eca for PVC efs-claim and csi volume name fs-95bcec92::fsap-02a88145b865d3a87
   ```

   If you don't see the previous output, run the previous command using one of the other controller pods\.

1. Confirm that a persistent volume was created with a status of `Bound` to a `PersistentVolumeClaim`:

   ```
   kubectl get pv
   ```

   The example output is as follows\.

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   pvc-5983ffec-96cf-40c1-9cd6-e5686ca84eca   20Gi       RWX            Delete           Bound    default/efs-claim   efs-sc                  7m57s
   ```

1. View details about the `PersistentVolumeClaim` that was created\.

   ```
   kubectl get pvc
   ```

   The example output is as follows\.

   ```
   NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
   efs-claim   Bound    pvc-5983ffec-96cf-40c1-9cd6-e5686ca84eca   20Gi       RWX            efs-sc         9m7s
   ```

1. View the sample app pod's status until the `STATUS` becomes `Running`\.

   ```
   kubectl get pods -o wide
   ```

   The example output is as follows\.

   ```
   NAME          READY   STATUS    RESTARTS   AGE   IP               NODE                                           NOMINATED NODE   READINESS GATES
   efs-example   1/1     Running   0          10m   192.168.78.156   ip-192-168-73-191.region-code.compute.internal   <none>           <none>
   ```
**Note**  
If a pod doesn't have an IP address listed, make sure that you added a mount target for the subnet that your node is in \(as described at the end of [Create an Amazon EFS file system](#efs-create-filesystem)\)\. Otherwise the pod won't leave `ContainerCreating` status\. When an IP address is listed, it may take a few minutes for a pod to reach the `Running` status\.

1. Confirm that the data is written to the volume\.

   ```
   kubectl exec efs-app -- bash -c "cat data/out"
   ```

   The example output is as follows\.

   ```
   ...
   Tue Mar 23 14:29:16 UTC 2021
   Tue Mar 23 14:29:21 UTC 2021
   Tue Mar 23 14:29:26 UTC 2021
   Tue Mar 23 14:29:31 UTC 2021
   ...
   ```

1. \(Optional\) Terminate the Amazon EKS node that your pod is running on and wait for the pod to be re\-scheduled\. Alternately, you can delete the pod and redeploy it\. Complete the previous step again, confirming that the output includes the previous output\.

------
#### [ Static ]

**To deploy a sample application that uses a persistent volume that you create**

This procedure uses the [Multiple Pods Read Write Many](https://github.com/kubernetes-sigs/aws-efs-csi-driver/tree/master/examples/kubernetes/multiple_pods) example from the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub repository to consume a statically provisioned Amazon EFS persistent volume and access it from multiple pods with the `ReadWriteMany` access mode\.

1. Clone the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub repository to your local system\.

   ```
   git clone https://github.com/kubernetes-sigs/aws-efs-csi-driver.git
   ```

1. Navigate to the `multiple_pods` example directory\.

   ```
   cd aws-efs-csi-driver/examples/kubernetes/multiple_pods/
   ```

1. Retrieve your Amazon EFS file system ID\. You can find this in the Amazon EFS console, or use the following AWS CLI command\.

   ```
   aws efs describe-file-systems --query "FileSystems[*].FileSystemId" --output text
   ```

   The example output is as follows\.

   ```
   fs-582a03f3
   ```

1. Edit the `specs/pv.yaml` file and replace the `volumeHandle` value with your Amazon EFS file system ID\.

   ```
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: efs-pv
   spec:
     capacity:
       storage: 5Gi
     volumeMode: Filesystem
     accessModes:
       - ReadWriteMany
     persistentVolumeReclaimPolicy: Retain
     storageClassName: efs-sc
     csi:
       driver: efs.csi.aws.com
       volumeHandle: fs-582a03f3
   ```
**Note**  
Because Amazon EFS is an elastic file system, it doesn't enforce any file system capacity limits\. The actual storage capacity value in persistent volumes and persistent volume claims isn't used when creating the file system\. However, because storage capacity is a required field in Kubernetes, you must specify a valid value, such as, `5Gi` in this example\. This value doesn't limit the size of your Amazon EFS file system\.

1. Deploy the `efs-sc` storage class, `efs-claim` persistent volume claim, and `efs-pv` persistent volume from the `specs` directory\.

   ```
   kubectl apply -f specs/pv.yaml
   kubectl apply -f specs/claim.yaml
   kubectl apply -f specs/storageclass.yaml
   ```

1. List the persistent volumes in the default namespace\. Look for a persistent volume with the `default/efs-claim` claim\.

   ```
   kubectl get pv -w
   ```

   The example output is as follows\.

   ```
   NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   efs-pv   5Gi        RWX            Retain           Bound    default/efs-claim   efs-sc                  2m50s
   ```

   Don't proceed to the next step until the `STATUS` is `Bound`\.

1. Deploy the `app1` and `app2` sample applications from the `specs` directory\.

   ```
   kubectl apply -f specs/pod1.yaml
   kubectl apply -f specs/pod2.yaml
   ```

1. Watch the pods in the default namespace and wait for the `app1` and `app2` pods' `STATUS` to become `Running`\.

   ```
   kubectl get pods --watch
   ```
**Note**  
It may take a few minutes for the pods to reach the `Running` status\.

1. Describe the persistent volume\.

   ```
   kubectl describe pv efs-pv
   ```

   The example output is as follows\.

   ```
   Name:            efs-pv
   Labels:          none
   Annotations:     kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"v1","kind":"PersistentVolume","metadata":{"annotations":{},"name":"efs-pv"},"spec":{"accessModes":["ReadWriteMany"],"capaci...
                    pv.kubernetes.io/bound-by-controller: yes
   Finalizers:      [kubernetes.io/pv-protection]
   StorageClass:    efs-sc
   Status:          Bound
   Claim:           default/efs-claim
   Reclaim Policy:  Retain
   Access Modes:    RWX
   VolumeMode:      Filesystem
   Capacity:        5Gi
   Node Affinity:   none
   Message:
   Source:
       Type:              CSI (a Container Storage Interface (CSI) volume source)
       Driver:            efs.csi.aws.com
       VolumeHandle:      fs-582a03f3
       ReadOnly:          false
       VolumeAttributes:  none
   Events:                none
   ```

   The Amazon EFS file system ID is listed as the `VolumeHandle`\.

1. Verify that the `app1` pod is successfully writing data to the volume\.

   ```
   kubectl exec -ti app1 -- tail /data/out1.txt
   ```

   The example output is as follows\.

   ```
   ...
   Mon Mar 22 18:18:22 UTC 2021
   Mon Mar 22 18:18:27 UTC 2021
   Mon Mar 22 18:18:32 UTC 2021
   Mon Mar 22 18:18:37 UTC 2021
   ...
   ```

1. Verify that the `app2` pod shows the same data in the volume that `app1` wrote to the volume\.

   ```
   kubectl exec -ti app2 -- tail /data/out1.txt
   ```

   The example output is as follows\.

   ```
   ...
   Mon Mar 22 18:18:22 UTC 2021
   Mon Mar 22 18:18:27 UTC 2021
   Mon Mar 22 18:18:32 UTC 2021
   Mon Mar 22 18:18:37 UTC 2021
   ...
   ```

1. When you finish experimenting, delete the resources for this sample application to clean up\.

   ```
   kubectl delete -f specs/
   ```

   You can also manually delete the file system and security group that you created\.

------