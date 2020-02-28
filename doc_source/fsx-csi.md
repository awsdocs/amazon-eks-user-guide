# Amazon FSx for Lustre CSI Driver<a name="fsx-csi"></a>

The [Amazon FSx for Lustre Container Storage Interface \(CSI\) Driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of Amazon FSx for Lustre file systems\.

This topic shows you how to deploy the Amazon FSx for Lustre CSI Driver to your Amazon EKS cluster and verify that it works\. We recommend using version 0\.3\.0 of the driver\.

**Note**  
This driver is supported on Kubernetes version 1\.14 and later Amazon EKS clusters and worker nodes\. Alpha features of the Amazon FSx for Lustre CSI Driver are not supported on Amazon EKS clusters\. The driver is in Beta release\. It is well tested and supported by Amazon EKS for production use\. Support for the driver will not be dropped, though details may change\. If the schema or schematics of the driver changes, instructions for migrating to the next version will be provided\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon FSx for Lustre Container Storage Interface \(CSI\) Driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) project on GitHub\.

**Prerequisites**

You must have:
+ Version 1\.16\.308 or later of the AWS CLI installed\. You can check your currently\-installed version with the `aws --version` command\. To install or upgrade the AWS CLI, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ An existing Amazon EKS cluster\. If you don't currently have a cluster, see [Getting Started with Amazon EKS](getting-started.md) to create one\.
+ Version 0\.11\.1 or later of `eksctl` installed\. You can check your currently\-installed version with the `eksctl version` command\. To install or upgrade `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.
+ The latest version of `kubectl` installed that aligns to your cluster version\. You can check your currently\-installed version with the `kubectl version --short --client` command\. For more information, see [Installing `kubectl`](install-kubectl.md)\.

**To deploy the Amazon FSx for Lustre CSI Driver to an Amazon EKS cluster**

1. Create an AWS Identity and Access Management OIDC provider and associate it with your cluster\.

   ```
   eksctl utils associate-iam-oidc-provider \
       --region us-west-2 \
       --cluster prod \
       --approve
   ```

1. Create an IAM policy and service account that allows the driver to make calls to AWS APIs on your behalf\.

   1. Copy the following text and save it to a file named `fsx-csi-driver.json`\.

      ```
      {
         "Version":"2012-10-17",
         "Statement":[
            {
               "Effect":"Allow",
               "Action":[
                  "iam:CreateServiceLinkedRole",
                  "iam:AttachRolePolicy",
                  "iam:PutRolePolicy"
               ],
               "Resource":"arn:aws:iam::*:role/aws-service-role/s3.data-source.lustre.fsx.amazonaws.com/*"
            },
            {
               "Action":"iam:CreateServiceLinkedRole",
               "Effect":"Allow",
               "Resource":"*",
               "Condition":{
                  "StringLike":{
                     "iam:AWSServiceName":[
                        "fsx.amazonaws.com"
                     ]
                  }
               }
            },
            {
               "Effect":"Allow",
               "Action":[
                  "s3:ListBucket",
                  "fsx:CreateFileSystem",
                  "fsx:DeleteFileSystem",
                  "fsx:DescribeFileSystems"
               ],
               "Resource":[
                  "*"
               ]
            }
         ]
      }
      ```

   1. Create the policy\.

      ```
      aws iam create-policy \
          --policy-name Amazon_FSx_Lustre_CSI_Driver \
          --policy-document file://fsx-csi-driver.json
      ```

      Take note of the policy Amazon Resource Name \(ARN\) that is returned\.

1. Create a Kubernetes service account for the driver and attach the policy to the service account\. Replacing the ARN of the policy with the ARN returned in the previous step\.

   ```
   eksctl create iamserviceaccount \
       --region us-west-2 \
       --name fsx-csi-controller-sa \
       --namespace kube-system \
       --cluster prod \
       --attach-policy-arn arn:aws:iam::111122223333:policy/Amazon_FSx_Lustre_CSI_Driver \
       --approve
   ```

   Expected output:

   ```
   [ℹ]  eksctl version 0.11.0
   [ℹ]  using region us-west-2
   [ℹ]  1 iamserviceaccount (kube-system/fsx-csi-controller-sa) was included (based on the include/exclude rules)
   [!]  serviceaccounts that exists in Kubernetes will be excluded, use --override-existing-serviceaccounts to override
   [ℹ]  1 task: { 2 sequential sub-tasks: { create IAM role for serviceaccount "kube-system/fsx-csi-controller-sa", create serviceaccount "kube-system/fsx-csi-controller-sa" } }
   [ℹ]  building iamserviceaccount stack "eksctl-prod-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa"
   [ℹ]  deploying stack "eksctl-prod-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa"
   [ℹ]  created serviceaccount "kube-system/fsx-csi-controller-sa"
   ```

   Note the name of the AWS CloudFormation stack that was deployed\. In the example output above, the stack is named `eksctl-prod-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa`\.

1. Note the **Role ARN** for the role that was created\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Ensure that the console is set to the region that you created your IAM role in and then select **Stacks**\.

   1. Select the stack named `eksctl-prod-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa`\.

   1. Select the **Outputs** tab\. The **Role ARN** is listed on the **Output\(1\)** page\.

1. Deploy the driver with the following command\.

   ```
   kubectl apply -k github.com/kubernetes-sigs/aws-fsx-csi-driver/deploy/kubernetes/overlays/stable/?ref=master
   ```

   Expected output

   ```
   Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
   serviceaccount/fsx-csi-controller-sa configured
   clusterrole.rbac.authorization.k8s.io/fsx-csi-external-provisioner-role created
   clusterrolebinding.rbac.authorization.k8s.io/fsx-csi-external-provisioner-binding created
   deployment.apps/fsx-csi-controller created
   daemonset.apps/fsx-csi-node created
   csidriver.storage.k8s.io/fsx.csi.aws.com created
   ```

1. Patch the driver deployment to add the service account that you created in step 3, replacing the ARN with the ARN that you noted in step 4\.

   ```
   kubectl annotate serviceaccount -n kube-system fsx-csi-controller-sa \
    eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-NPFTLHJ5PJF5
   ```

**To deploy a Kubernetes storage class, persistent volume claim, and sample application to verify that the CSI driver is working**

This procedure uses the [Dynamic Volume Provisioning for Amazon S3 ](https://github.com/kubernetes-sigs/aws-fsx-csi-driver/tree/master/examples/kubernetes/dynamic_provisioning_s3)from the [Amazon FSx for Lustre Container Storage Interface \(CSI\) Driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) GitHub repository to consume a dynamically\-provisioned Amazon FSx for Lustre volume\.

1. Create an Amazon S3 bucket and a folder within it named `export` by creating and copying a file to the bucket\.

   ```
   aws s3 mb s3://fsx-csi
   echo test-file >> testfile
   aws s3 cp testfile s3://fsx-csi/export/testfile
   ```

1. Download the `storageclass` manifest with the following command\.

   ```
   curl -o storageclass.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning_s3/specs/storageclass.yaml
   ```

1. Edit the file and replace the existing, `alternate-colored` values with your own\.

   ```
   parameters:
     subnetId: subnet-056da83524edbe641
     securityGroupIds: sg-086f61ea73388fb6b
     s3ImportPath: s3://ml-training-data-000
     s3ExportPath: s3://ml-training-data-000/export
     deploymentType: SCRATCH_2
   ```
   + **subnetId** – The subnet ID that the Amazon FSx for Lustre file system should be created in\. Amazon FSx for Lustre is not supported in all availability zones\. Open the Amazon FSx for Lustre console at [https://console\.aws\.amazon\.com/fsx/](https://console.aws.amazon.com/fsx/) to confirm that the subnet that you want to use is in a supported availability zone\. The subnet can include your worker nodes, or can be a different subnet or VPC\. If the subnet that you specify is not the same subnet that you have worker nodes in, then your VPCs must be [connected](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html), and you must ensure that you have the necessary ports open in your security groups\.
   + **securityGroupIds** – The security group ID for your worker nodes\.
   + **s3ImportPath** – The Amazon Simple Storage Service data repository that you want to copy data from to the persistent volume\. Specify the `fsx-csi` bucket that you created in step 1\.
   + **s3ExportPath** – The Amazon S3 data repository that you want to export new or modified files to\. Specify the `fsx-csi/export` folder that you created in step 1\.
   + **deploymentType** - The file system deployment type, valid values are `SCRATCH_1`, `SCRATCH_2` and `PERSISTENT_1`. Check FSx for Lustre [Getting Started](https://docs.aws.amazon.com/fsx/latest/LustreGuide/getting-started-step1.html) for more deployment type details.
**Note**  
The Amazon S3 bucket for `s3ImportPath` and `s3ExportPath` must be the same, otherwise the driver cannot create the Amazon FSx for Lustre file system\. The `s3ImportPath` can stand alone\. A random path will be created automatically like `s3://ml-training-data-000/FSxLustre20190308T012310Z`\. The `s3ExportPath` cannot be used without specifying a value for `S3ImportPath`\.

1. Create the `storageclass`\.

   ```
   kubectl apply -f storageclass.yaml
   ```

1. Download the persistent volume claim manifest\.

   ```
   curl -o claim.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning_s3/specs/claim.yaml
   ```

1. \(Optional\) Edit the `claim.yaml` file, changing the value for the following line to `2400 GiB` or a multiple of `3600 GiB`, to meet your storage requirements\.

   ```
   storage: 1200Gi
   ```

1. Create the persistent volume claim\.

   ```
   kubectl apply -f claim.yaml
   ```

1. Confirm that the file system is provisioned\.

   ```
   kubectl get pvc
   ```

   Expected output\.

   ```
   NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
   fsx-claim   Bound    pvc-15dad3c1-2365-11ea-a836-02468c18769e   1200Gi     RWX            fsx-sc         7m37s
   ```
**Note**  
The `STATUS` may show as `Pending` for 5\-10 minutes, before changing to `Bound`\. Don't continue with the next step until the `STATUS` is `Bound`\.

1. Deploy the sample application\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning_s3/specs/pod.yaml
   ```

1. Verify that the sample application is running\.

   ```
   kubectl get pods
   ```

   Expected output

   ```
   NAME      READY   STATUS              RESTARTS   AGE
   fsx-app   1/1     Running             0          8s
   ```

 **Access Amazon S3 files from the Amazon FSx for Lustre file system**

If you only want to import data and read it without any modification and creation, then you don't need a value for `s3ExportPath` in your `storageclass.yaml` file\. Verify that data was written to the Amazon FSx for Lustre file system by the sample app\.

```
kubectl exec -it fsx-app ls /data
```

Expected output\.

```
export  out.txt
```

The sample app wrote the `out.txt` file to the file system\.

**Archive files to the `s3ExportPath`**

For new files and modified files, you can use the Lustre user space tool to archive the data back to Amazon S3 using the value that you specified for `s3ExportPath`\.

1. Export the file back to Amazon S3\.

   ```
   kubectl exec -ti fsx-app -- lfs hsm_archive /data/out.txt
   ```
**Note**  
New files aren't synced back to Amazon S3 automatically\. In order to sync files to the `s3ExportPath`, you need to [install the Lustre client](https://docs.aws.amazon.com/fsx/latest/LustreGuide/install-lustre-client.html) in your container image and manually run the `lfs hsm_archive` command\. The container should run in privileged mode with the `CAP_SYS_ADMIN` capability\.
This example uses a lifecycle hook to install the Lustre client for demonstration purpose\. A normal approach is building a container image with the Lustre client\.

1. Confirm that the `out.txt` file was written to the `s3ExportPath` folder in Amazon S3\.

   ```
   aws s3 ls fsx-csi/export/
   ```

   Expected output

   ```
   2019-12-23 12:11:35       4553 out.txt
   2019-12-23 11:41:21         10 testfile
   ```
