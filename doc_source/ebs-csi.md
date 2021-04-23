# Amazon EBS CSI driver<a name="ebs-csi"></a>

The [ Amazon Elastic Block Store \(Amazon EBS\) Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) provides a CSI interface that allows Amazon Elastic Kubernetes Service \(Amazon EKS\) clusters to manage the lifecycle of Amazon EBS volumes for persistent volumes\.

This topic shows you how to deploy the Amazon EBS CSI Driver to your Amazon EKS cluster and verify that it works\. We recommend using version v0\.9\.0 of the driver\.

**Note**  
 The driver is not supported on Fargate\. Alpha features of the Amazon EBS CSI Driver are not supported on Amazon EKS clusters\. The driver is in Beta release\. It is well tested and supported by Amazon EKS for production use\. Support for the driver will not be dropped, though details may change\. If the schema or schematics of the driver changes, instructions for migrating to the next version will be provided\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) project on GitHub\.

**Prerequisites**
+ An existing cluster\. If you don't have one, see [Getting started with Amazon EKS](getting-started.md) to create one\.
+ An existing IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ AWS CLI version 1\.19\.7 or later or 2\.1\.26 installed on your computer or [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)\. To install or upgrade the AWS CLI , see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ `kubectl` version 1\.15 or later installed on your computer or [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)\. To install or upgrade kubectl, see [Installing `kubectl`](install-kubectl.md)\.

**To deploy the Amazon EBS CSI driver to an Amazon EKS cluster**

1. Create an IAM policy that allows the CSI driver's service account to make calls to AWS APIs on your behalf\. You can view the policy document [on GitHub](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/v0.9.0/docs/example-iam-policy.json)\.

   1. Download the IAM policy document from GitHub\.

      ```
      curl -o example-iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-ebs-csi-driver/v0.9.0/docs/example-iam-policy.json
      ```

   1. Create the policy\. You can change `AmazonEKS_EBS_CSI_Driver_Policy` to a different name, but if you do, make sure to change it in later steps too\.

      ```
      aws iam create-policy --policy-name AmazonEKS_EBS_CSI_Driver_Policy \
        --policy-document file://example-iam-policy.json
      ```

1. Create an IAM role and attach the IAM policy to it\.

   1. View your cluster's OIDC provider URL\. Replace `<cluster_name>` \(including `<>`\) with your cluster name\. If the output from the command is `None`, review the **Prerequisites**\.

      ```
      aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
      ```

      Output

      ```
      https://oidc.eks.us-west-2.amazonaws.com/id/XXXXXXXXXX45D83924220DC4815XXXXX
      ```

   1. Create the IAM role\.

      1. Copy the following contents to a file named `trust-policy.json`\. Replace `<AWS_ACCOUNT_ID>` \(including `<>`\) with your account ID, `<REGION>` with your Region, and `<XXXXXXXXXX45D83924220DC4815XXXXX>` with the value returned in the previous step\.

         ```
         {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Principal": {
                 "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/oidc.eks.<REGION>.amazonaws.com/id/<XXXXXXXXXX45D83924220DC4815XXXXX>"
               },
               "Action": "sts:AssumeRoleWithWebIdentity",
               "Condition": {
                 "StringEquals": {
                   "oidc.eks.<REGION>.amazonaws.com/id/<XXXXXXXXXX45D83924220DC4815XXXXX>:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa"
                 }
               }
             }
           ]
         }
         ```

      1. Create the role\. You can change `AmazonEKS_EBS_CSI_DriverRole` to a different name, but if you do, make sure to change it in later steps too\.

         ```
         aws iam create-role \
           --role-name AmazonEKS_EBS_CSI_DriverRole \
           --assume-role-policy-document file://"trust-policy.json"
         ```

   1. Attach the IAM policy to the role\. Replace `<AWS_ACCOUNT_ID>` \(including `<>`\) with your account ID\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AmazonEKS_EBS_CSI_Driver_Policy \
        --role-name AmazonEKS_EBS_CSI_DriverRole
      ```

1. Deploy the driver using one of the following options\.
   + Deploy the driver so that it tags all Amazon EBS volumes that it creates with tags that your specify\.

     1. Clone the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to your computer\.

        ```
        git clone https://github.com/kubernetes-sigs/aws-ebs-csi-driver.git
        ```

     1. Navigate to the `base` example folder\.

        ```
        cd aws-ebs-csi-driver/deploy/kubernetes/base/
        ```

     1. Edit the `controller.yaml` file\. Find the section of the file with the following text and add `--extra-tags` to it\. The following text shows the section of the file with the existing and added text\. This example will cause the controller to add `department` and `environment` tags to all volumes it creates\.

        ```
        ...
        containers:
                - name: ebs-plugin
                  image: amazon/aws-ebs-csi-driver:latest
                  imagePullPolicy: IfNotPresent
                  args:
                    # - {all,controller,node} # specify the driver mode
                    - --endpoint=$(CSI_ENDPOINT)
                    - --logtostderr
                    - --v=5
                    - --extra-tags=department=accounting,environment=dev
        ...
        ```

     1. Apply the modified manifest to your cluster\.

        ```
        kubectl apply -k ../base
        ```
   + Deploy the driver so that it doesn't tag the Amazon EBS volumes that it creates with tags that your specify\. Use the command that corresponds to the Region that your cluster is in\.
**Note**  
This commands require version 1\.14 or later of `kubectl`\. You can see your `kubectl` version with the following command\. To install or upgrade your `kubectl` version, see [Installing `kubectl`](install-kubectl.md)\.  

     ```
     kubectl version --client --short
     ```
     + 
**Note**  
To see or download the `yaml` file manually, you can find it on the [aws\-ebs\-csi\-driver Github](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/deploy/kubernetes/overlays/stable/ecr)\.

       All Regions other than China Regions\.

       ```
       kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
       ```
     + Beijing and Ningxia China Regions\.

       ```
       kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable-cn/?ref=master"
       ```

1. Annotate the `ebs-csi-controller-sa` Kubernetes service account with the ARN of the IAM role that you created previously\. Replace the `<AWS_ACCOUNT_ID>` \(including `<>`\) with your account ID\. 

   ```
   kubectl annotate serviceaccount ebs-csi-controller-sa \
     -n kube-system \
     eks.amazonaws.com/role-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:role/AmazonEKS_EBS_CSI_DriverRole
   ```

1. Delete the driver pods\. They're automatically redeployed with the IAM permissions from the IAM policy assigned to the role\.

   ```
   kubectl delete pods \
     -n kube-system \
     -l=app=ebs-csi-controller
   ```

**To deploy a sample application and verify that the CSI driver is working**

This procedure uses the [Dynamic volume provisioning](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning) example from the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to consume a dynamically\-provisioned Amazon EBS volume\.

1. Clone the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to your local system\.

   ```
   git clone https://github.com/kubernetes-sigs/aws-ebs-csi-driver.git
   ```

1. Navigate to the `dynamic-provisioning` example directory\.

   ```
   cd aws-ebs-csi-driver/examples/kubernetes/dynamic-provisioning/
   ```

1. Deploy the `ebs-sc` storage class, `ebs-claim` persistent volume claim, and `app` sample application from the `specs` directory\.

   ```
   kubectl apply -f specs/
   ```

1. Describe the `ebs-sc` storage class\.

   ```
   kubectl describe storageclass ebs-sc
   ```

   Output:

   ```
   Name:            ebs-sc
   IsDefaultClass:  No
   Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"ebs-sc"},"provisioner":"ebs.csi.aws.com","volumeBindingMode":"WaitForFirstConsumer"}
   
   Provisioner:           ebs.csi.aws.com
   Parameters:            <none>
   AllowVolumeExpansion:  <unset>
   MountOptions:          <none>
   ReclaimPolicy:         Delete
   VolumeBindingMode:     WaitForFirstConsumer
   Events:                <none>
   ```

   Note that the storage class uses the `WaitForFirstConsumer` volume binding mode\. This means that volumes are not dynamically provisioned until a pod makes a persistent volume claim\. For more information, see [Volume Binding Mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) in the Kubernetes documentation\.

1. Watch the pods in the default namespace and wait for the `app` pod's status to become `Running`\.

   ```
   kubectl get pods --watch
   ```

1. List the persistent volumes in the default namespace\. Look for a persistent volume with the `default/ebs-claim` claim\.

   ```
   kubectl get pv
   ```

   Output:

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a   4Gi        RWO            Delete           Bound    default/ebs-claim   ebs-sc                  30s
   ```

1. Describe the persistent volume, replacing `<pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a>` \(including `<>`\) with the value from the output in the previous step\.

   ```
   kubectl describe pv <pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a>
   ```

   Output:

   ```
   Name:              pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a
   Labels:            <none>
   Annotations:       pv.kubernetes.io/provisioned-by: ebs.csi.aws.com
   Finalizers:        [kubernetes.io/pv-protection external-attacher/ebs-csi-aws-com]
   StorageClass:      ebs-sc
   Status:            Bound
   Claim:             default/ebs-claim
   Reclaim Policy:    Delete
   Access Modes:      RWO
   VolumeMode:        Filesystem
   Capacity:          4Gi
   Node Affinity:
     Required Terms:
       Term 0:        topology.ebs.csi.aws.com/zone in [us-west-2d]
   Message:
   Source:
       Type:              CSI (a Container Storage Interface (CSI) volume source)
       Driver:            ebs.csi.aws.com
       VolumeHandle:      <vol-0d651e157c6d93445>
       ReadOnly:          false
       VolumeAttributes:      storage.kubernetes.io/csiProvisionerIdentity=1567792483192-8081-ebs.csi.aws.com
   Events:                <none>
   ```

   The Amazon EBS volume ID is listed as the `VolumeHandle`\.

1. Verify that the pod is successfully writing data to the volume\.

   ```
   kubectl exec -it app -- cat /data/out.txt
   ```

   Output:

   ```
   Fri Jan 8 15:34:20 UTC 2021
   Fri Jan 8 15:34:25 UTC 2021
   Fri Jan 8 15:34:30 UTC 2021
   Fri Jan 8 15:34:35 UTC 2021
   Fri Jan 8 15:34:40 UTC 2021
   Fri Jan 8 15:34:45 UTC 2021
   ...
   ```

1. When you finish experimenting, delete the resources for this sample application to clean up\.

   ```
   kubectl delete -f specs/
   ```