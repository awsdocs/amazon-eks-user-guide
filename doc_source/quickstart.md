# Quickstart: Deploy a web app and store data<a name="quickstart"></a>

This quickstart tutorial shows the steps to deploy the 2048 game sample application and persist its data on an Amazon EKS cluster using [eksctl](https://eksctl.io/)\. eksctl is an infrastructure\-as\-code utility leveraging [AWS CloudFormation](https://aws.amazon.com/cloudformation/), allowing you to set up a fully\-functional cluster, complete with all the essential components\. These components include a Amazon VPC and an IAM role tailored to provide permissions to the AWS services we've defined\. As we progress, we'll walk you through the cluster setup process, incorporating Amazon EKS [Amazon EKS add\-ons](eks-add-ons.md)to power your cluster with operational capabilities\. Finally, you'll deploy a sample workload with the custom annotations required to fully integrate with AWS services\.

## In this tutorial<a name="quickstart-in-tutorial"></a>

Using the eksctl cluster template that follows, you'll build an Amazon EKS cluster with managed node groups\. It configures the following components:

**VPC Configuration**  
When using the eksctl cluster template that follows, eksctl automatically creates an IPv4 Virtual Private Cloud \(VPC\) for the cluster\. By default, eksctl configures a VPC that addresses all [networking requirements](network-reqs.md), in addition to creating both public and private endpoints\.

**Instance type**  
Utilize the [t3\.medium instance type](choosing-instance-type.md)\. This instance type offers a well\-balanced combination of compute, memory, and network resources—ideal for applications with moderate CPU usage that may experience occasional spikes in demand\.

**Authentication**  
Establish the IRSA mappings to facilitate communication between Kubernetes pods and AWS services\. The template is configured to set up an [OpenID Connect \(OIDC\) endpoint](enable-iam-roles-for-service-accounts.md) for authentication and authorization\. It also establishes a service account for the [AWS Load Balancer Controller \(LBC\)](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/), a controller responsible for exposing applications and managing traffic\.

**Data Persistence**  
Integrate the [AWS EBS CSI Driver](ebs-csi.md#managing-ebs-csi) managed add\-on to ensure the persistence of application data, even in scenarios involving pod restarts or failures\. The template is configured to install the add\-on and establish a service account

**External App Access**  
Set up and integrate with the AWS Load Balancer Controller \(LBC\) add\-on to expose the [2048 game application](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.6.0/docs/examples/2048/2048_full.yaml), using the LBC to dynamically provision an Application Load Balancer \(ALB\)\.

## Prerequisites<a name="quickstart-prereqs"></a>
+ [Set up to use Amazon EKS](setting-up.md)
+ [Install Helm](https://helm.sh/docs/intro/install/)

## Step 1: Configure the cluster<a name="quickstart-config-cluster"></a>

In this section, you'll create a managed node group\-based cluster using [t3\.medium](https://aws.amazon.com/ec2/instance-types/) instances containing two nodes\. The configuration includes a service account for [AWS Load Balancer Controller \(LBC\)](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/deploy/installation/) add\-on, and installation of the latest version of the [AWS Amazon EBS CSI driver](ebs-csi.md#managing-ebs-csi.title)\. For all available `eksctl` add\-ons, see [Discovering addons](https://eksctl.io/usage/addons/#discovering-addons) in `eksctl` documentation\.
+ Create a `cluster-config.yaml` file and paste the following contents into it\. Replace *region\-code* with a valid region, such as `us-east-1`

  Example output is as follows:

  ```
  apiVersion: eksctl.io/v1alpha5
  kind: ClusterConfig
  
  metadata:
    name: web-quickstart
    region: region-code
  
  managedNodeGroups:
    - name: eks-mng
      instanceType: t3.medium
      desiredCapacity: 2
  
  iam:
    withOIDC: true
    serviceAccounts:
    - metadata:
        name: aws-load-balancer-controller
        namespace: kube-system
      wellKnownPolicies:
        awsLoadBalancerController: true
  
  addons:
    - name: aws-ebs-csi-driver
      wellKnownPolicies: # Adds an IAM service account
        ebsCSIController: true
        
  cloudWatch:
   clusterLogging:
     enableTypes: ["*"]
     logRetentionInDays: 30
  ```

## Step 2: Create the cluster<a name="quickstart-create-cluster"></a>

Now, we're ready to create our Amazon EKS cluster\. This process takes several minutes to complete\. If you'd like to monitor the status, see the [AWS CloudFormation](https://console.aws.amazon.com/cloudformation) console\.
+ Create the Amazon EKS cluster and specify the cluster\-config\.yaml\.

  ```
  eksctl create cluster -f cluster-config.yaml
  ```
**Note**  
If you receive an `Error: checking STS access` in the response, make sure that you're using the correct user identity for the current shell session\. You may also need to specify a named profile \(for example, `--profile clusteradmin`\) or get a new security token for the AWS CLI\.

  Upon completion, you should see the following response output:

  ```
  2024-07-04 21:47:53 [✔]  EKS cluster "web-quickstart" in "region-code" region is ready
  ```

## Step 3: Set up external access to applications using the AWS Load Balancer Controller \(LBC\)<a name="quickstart-lbc"></a>

With the cluster operational, our next step is making its containerized applications accessible externally\. This is accomplished by deploying an [Application Load Balancer \(ALB\)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) to direct traffic outside the cluster to our services, in other words, our applications\. When we created our cluster, we established an [IAM Roles for Service Accounts \(IRSA\)](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up-enable-IAM.html) for the [ Load Balancer Controller \(LBC\)](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/) with the permissions needed to dynamically create ALBs, facilitating external traffic routing to our Kubernetes services\. In this section, we'll set up the AWS LBC on our cluster\.

**To configure environment variables**

1. Set the `CLUSTER_REGION` environment variable for your Amazon EKS cluster\. Replace the sample value for *`region-code`*\.

   ```
   export CLUSTER_REGION=region-code
   ```

1. Set the `CLUSTER_VPC` environment variable for your Amazon EKS cluster\.

   ```
   export CLUSTER_VPC=$(aws eks describe-cluster --name web-quickstart --region $CLUSTER_REGION --query "cluster.resourcesVpcConfig.vpcId" --output text)
   ```

**To install the AWS Load Balancer Controller \(LBC\)**

The AWS Load Balancer Controller \(LBC\) leverages Custom Resource Definitions \(CRDs\) in Kubernetes to manage AWS Elastic Load Balancers \(ELBs\)\. These CRDs define custom resources such as load balancers and TargetGroupBindings, enabling the Kubernetes cluster to recognize and manage them\.

1. Use [Helm](https://helm.sh/docs/intro/install/) to add the Amazon EKS chart repository to Helm\.

   ```
   helm repo add eks https://aws.github.io/eks-charts
   ```

1. Update the repositories to ensure Helm is aware of the latest versions of the charts:

   ```
   helm repo update eks
   ```

1. Run the following [Helm](https://helm.sh/docs/intro/install/) command to simultaneously install the Custom Resource Definitions \(CRDs\) and the main controller for the AWS Load Balancer Controller \(AWS LBC\)\. To skip the CRD installation, pass the `--skip-crds` flag, which might be useful if the CRDs are already installed, if specific version compatibility is required, or in environments with strict access control and customization needs\.

   ```
   helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
       --namespace kube-system \
       --set clusterName=web-quickstart \
       --set serviceAccount.create=false \
       --set region=${CLUSTER_REGION} \
       --set vpcId=${CLUSTER_VPC} \
       --set serviceAccount.name=aws-load-balancer-controller
   ```

   You should see the following response output:

   ```
   NAME: aws-load-balancer-controller
   LAST DEPLOYED: Wed July 3 19:43:12 2024
   NAMESPACE: kube-system
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   AWS Load Balancer controller installed!
   ```

## Step 4: Deploy the 2048 game sample application<a name="quickstart-deploy-game"></a>

Now that the load balancer is set up, it's time to enable external access for containerized applications in the cluster\. In this section, we walk you through the steps to deploy the popular “2048 game” as a sample application within the cluster\. The provided manifest includes custom annotations for the Application Load Balancer \(ALB\), specifically the ['scheme' annotation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/guide/ingress/ingress_class/#specscheme) and ['target\-type' annotation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/guide/ingress/annotations/#target-type)\. These annotations integrate with and instruct the AWS Load Balancer Controller \(LBC\) to handle incoming HTTP traffic as "internet\-facing" and route it to the appropriate service in the 'game\-2048' namespace using the target type "ip"\. For more annotations, see [Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.8/guide/ingress/annotations/) in the AWS LBC documentation\.

1. Create a Kubernetes namespace called `game-2048` with the `--save-config` flag\.

   ```
   kubectl create namespace game-2048 --save-config
   ```

   You should see the following response output:

   ```
   namespace/game-2048 created
   ```

1. Deploy the [2048 Game Sample application](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml)\.

   ```
   kubectl apply -n game-2048 -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml
   ```

   This manifest sets up a Kubernetes Deployment, Service, and Ingress for the `game-2048` namespace, creating the necessary resources to deploy and expose the `game-2048` application within the cluster\. It includes the creation of a service named `service-2048` that exposes the deployment on port `80`, and an Ingress resource named `ingress-2048` that defines routing rules for incoming HTTP traffic and annotations for an internet\-facing Application Load Balancer \(ALB\)\. You should see the following response output: 

   ```
   namespace/game-2048 configured
   deployment.apps/deployment-2048 created
   service/service-2048 created
   ingress.networking.k8s.io/ingress-2048 created
   ```

1. Run the following command to get the Ingress resource for the `game-2048` namespace\.

   ```
   kubectl get ingress -n game-2048
   ```

   You should see the following response output:

   ```
   NAME           CLASS   HOSTS   ADDRESS                                                                    PORTS   AGE
   ingress-2048   alb     *       k8s-game2048-ingress2-eb379a0f83-378466616.region-code.elb.amazonaws.com   80      31s
   ```

   You'll need to wait several minutes for the Application Load Balancer \(ALB\) to provision before you begin the following steps\.

1. Open a web browser and enter the `ADDRESS` from the previous step to access the web application\. For example, `k8s-game2048-ingress2-eb379a0f83-378466616.`*`region-code`*`.elb.amazonaws.com`\. You should see the 2048 game in your browser\. Play\!  
![\[\]](http://docs.aws.amazon.com/eks/latest/userguide/images/quick2048.png)

## Step 5: Persist Data using the Amazon EBS CSI Driver nodes<a name="quickstart-persist-data"></a>

Now that the 2048 game is up and running on your Amazon EKS cluster, it's time to ensure that your game data is safely persisted using the [Amazon EBS CSI Driver](ebs-csi.md) managed add\-on\. This add\-on was installed on our cluster during the creation process\. This integration is essential for preserving game progress and data even as Kubernetes pods or nodes are restarted or replaced\.

1. Create a [Storage Class](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/examples/kubernetes/dynamic-provisioning/manifests/storageclass.yaml) for the EBS CSI Driver:

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-ebs-csi-driver/master/examples/kubernetes/dynamic-provisioning/manifests/storageclass.yaml
   ```

1. Create a Persistent Volume Claim \(PVC\) to request storage for your game data\. Create a file named `ebs-pvc.yaml` and add the following content to it:

   ```
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: game-data-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 10Gi
     storageClassName: ebs-sc
   ```

1. Apply the PVC to your cluster:

   ```
   kubectl apply -f ebs-pvc.yaml
   ```

   You should see the following response output:

   ```
   persistentvolumeclaim/game-data-pvc created
   ```

1. Now, you need to update your 2048 game deployment to use this PVC for storing data\. The following deployment is configured to use the PVC for storing game data\. Create a file named `ebs-deployment.yaml` and add the following contents to it:

   ```
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     namespace: game-2048
     name: deployment-2048
   spec:
     replicas: 3  # Adjust the number of replicas as needed
     selector:
       matchLabels:
         app.kubernetes.io/name: app-2048
     template:
       metadata:
         labels:
           app.kubernetes.io/name: app-2048
       spec:
         containers:
           - name: app-2048
             image: public.ecr.aws/l6m2t8p7/docker-2048:latest
             imagePullPolicy: Always
             ports:
               - containerPort: 80
             volumeMounts:
               - name: game-data
                 mountPath: /var/lib/2048
         volumes:
           - name: game-data
             persistentVolumeClaim:
               claimName: game-data-pvc
   ```

1. Apply the updated deployment:

   ```
   kubectl apply -f ebs-deployment.yaml
   ```

   You should see the following response output:

   ```
   deployment.apps/deployment-2048 configured
   ```

With these steps, your 2048 game on Amazon EKS is now set up to persist data using the Amazon EBS CSI Driver\. This ensures that your game progress and data are safe even in the event of pod or node failures\. If you liked this tutorial, let us know by providing feedback so we're able to provide you with more use case\-specific quickstart tutorials like this one\.

## Step 6: Delete your cluster and nodes<a name="quickstart-delete-cluster"></a>

After you've finished with the cluster and nodes that you created for this tutorial, you should clean up by deleting the cluster and nodes with the following command\. If you want to do more with this cluster before you clean up, see Next steps\.

```
eksctl delete cluster -f ./cluster-config.yaml
```

Upon completion, you should see the following response output:

```
2024-07-05 17:26:44 [✔] all cluster resources were deleted
```

## Next steps<a name="quickstart-next-steps"></a>

The following documetation topics help you to extend the functionality of your cluster:
+ The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html#iam-term-principal) that created the cluster is the only principal that can make calls to the Kubernetes API server with `kubectl` or the AWS Management Console\. If you want other IAM principals to have access to your cluster, then you need to add them\. For more information, see [Grant IAM users and roles access to Kubernetes APIs](grant-k8s-access.md) and [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions)\.
+ Before deploying a cluster for production use, we recommend familiarizing yourself with all of the settings for [clusters](create-cluster.md) and [nodes](eks-compute.md)\. Some settings \(such as enabling SSH access to Amazon EC2 nodes\) must be made when the cluster is created\.
+ To increase security for your cluster, [configure the Amazon VPC Container Networking Interface plugin to use IAM roles for service accounts](cni-iam-role.md)\.

To explore ways to create different types of clusters:
+ [EKS Cluster Setup on AWS Community](https://community.aws/tags/eks-cluster-setup)