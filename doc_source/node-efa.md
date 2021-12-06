# Machine learning training using Elastic Fabric Adapter<a name="node-efa"></a>

This topic describes how to integrate Elastic Fabric Adapter \(EFA\) with pods deployed in your Amazon EKS cluster\. Elastic Fabric Adapter \(EFA\) is a network interface for Amazon EC2 instances that enables you to run applications requiring high levels of inter\-node communications at scale on AWS\. Its custom\-built operating system bypass hardware interface enhances the performance of inter\-instance communications, which is critical to scaling these applications\. With EFA, High Performance Computing \(HPC\) applications using the Message Passing Interface \(MPI\) and Machine Learning \(ML\) applications using NVIDIA Collective Communications Library \(NCCL\) can scale to thousands of CPUs or GPUs\. As a result, you get the application performance of on\-premises HPC clusters with the on\-demand elasticity and flexibility of the AWS cloud\. Integrating EFA with applications running on Amazon EKS clusters can reduce the time to complete large scale distributed training workloads without having to add additional instances to your cluster\. For more information about EFA, [Elastic Fabric Adapter](http://aws.amazon.com/hpc/efa/)\.

The EFA plugin described in this topic fully supports Amazon EC2 `[P4d](http://aws.amazon.com/ec2/instance-types/p4/)` instances, which represent the current state of the art in distributed machine learning in the cloud\. Each `p4d.24xlarge` instance has eight NVIDIA A100 GPUs, and 400 Gbps GPUDirectRDMA over EFA\. GPUDirectRDMA enables you to have direct GPU\-to\-GPU communication across nodes with CPU bypass, increasing collective communication bandwidth and lowering latency\. Amazon EKS and EFA integration with `P4d` instances provides a seamless method to take advantage of the highest performing Amazon EC2 computing instance for distributed machine learning training\.

**Prerequisites**
+ An existing 1\.19 or later Amazon EKS cluster\. If you don't have an existing cluster, use one of our [Getting started with Amazon EKS](getting-started.md) guides to create one\. Your cluster must be deployed in a VPC that has at least one private subnet with enough available IP addresses to deploy nodes in\. The private subnet must have outbound internet access provided by an external device, such as a NAT gateway\.

  If you plan to use `eksctl` to create your node group, `eksctl` can also create a 1\.19 cluster for you\. 
+ The AWS CLI version 2\.3\.7 or later or 1\.22\.8 or later installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)in the AWS Command Line Interface User Guide\. 
+ `Kubectl` version or later installed on your computer or AWS CloudShell\. To install or upgrade `kubectl`, see [Installing `kubectl`](install-kubectl.md)\.
+ You must have the VPC CNI version 1\.7\.10 installed before launching worker nodes that support multiple Elastic Fabric Adapters, such as the `p4d.24xlarge`\. For more information about updating your CNI version, see [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on)\.

## Create node group<a name="efa-create-nodegroup"></a>

The following procedure helps you create a node group with a `p4d.24xlarge` backed node group with EFA interfaces and GPUDirect RDMA, and run an example NVIDIA Collective Communications Library \(NCCL\) test for multi\-node NCCL Performance using EFAs\. The example can be used a template for distributed deep learning training on Amazon EKS using EFAs\.

1. Determine which Availability Zones that Amazon EC2 instances that support EFA are available in for the region that your cluster is in

   1. Determine which Amazon EC2 instance types that support EFA are available in the Region that your cluster is in\.

      ```
      aws ec2 describe-instance-types \
          --region us-west-2 \
          --filters Name=network-info.efa-supported,Values=true \
          --query "InstanceTypes[*].[InstanceType]" \
          --output text
      ```

   1. Determine which Availability Zones the instance you select from the previous output is available in\.

      ```
      aws ec2 describe-instance-type-offerings \
          --location-type availability-zone \
          --filters Name=instance-type,Values=p4d.24xlarge \
          --region us-west-2 \
          --output table
      ```

      The Availability Zone name is listed in the `Location` column of the output returned from the previous command\.

1. Create a node group using either `eksctl` or the AWS CLI and AWS CloudFormation\.

------
#### [ eksctl ]

**Prerequisite**  
`Eksctl` version 0\.75\.0 or later installed on your computer or AWS CloudShell\. To install or upgrade `eksctl`, see [The `eksctl` command line utility](eksctl.md)\.

   1. Copy the following contents to a file named `efa-cluster.yaml`\. Replace the *example values* with your own\. You can replace *p4d\.24xlarge* with a different instance, but if you do, make sure that the values for `availabilityZones` are Availability Zones that were returned for the instance type in step 1\.

      ```
      apiVersion: eksctl.io/v1alpha5
      kind: ClusterConfig
      
      metadata:
        name: my-efa-cluster
        region: us-west-2
        version: "1.19"
      
      iam:
        withOIDC: true
      
      availabilityZones: ["us-west-2a", "us-west-2c"]  
      
      managedNodeGroups:
        - name: my-efa-ng
          instanceType: p4d.24xlarge
          minSize: 1
          desiredCapacity: 2
          maxSize: 3
          availabilityZones: ["us-west-2a"]
          volumeSize: 300
          privateNetworking: true
          efaEnabled: true
      ```

   1. Create a managed node group in an existing cluster\.

      ```
      eksctl create nodegroup -f efa-cluster.yaml
      ```

      If you don't have an existing cluster, you can run the following command to create a cluster and the node group\.

      ```
      eksctl create cluster -f efa-cluster.yaml
      ```

------
#### [  AWS CLI and AWS CloudFormation ]

   There are several requirements for EFA networking, including creating an EFA specific security group, creating an Amazon EC2 [placement group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html), and creating a launch template that specifies one or more EFA interfaces, and includes EFA driver installation as part of Amazon EC2 user data\. To learn more about EFA requirements, see [Get started with EFA and MPI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start.html) in the Amazon EC2 User Guide for Linux Instances\. The following steps create all of this for you\. Replace all *example values* with your own\.

   1. Set a few variables used in later steps\. Replace all of the *`example values`* with your own\. Replace `my-cluster` with the name of your existing cluster\. The value for `node_group_resources_name` is later used to create an AWS CloudFormation stack\. The value for `node_group_name` is later used to create the node group in your cluster\.

      ```
      cluster_name="my-cluster"
      cluster_region="us-west-2"
      node_group_resources_name="my-efa-nodegroup-resources"
      node_group_name="my-efa-nodegroup"
      ```

   1. Identify a private subnet in your VPC that is in the same Availability Zone as the instance type that you want to deploy is available in\.

      1. Retrieve the version of your cluster and store it in a variable for use in a later step\.

         ```
         cluster_version=$(aws eks describe-cluster \
             --name $cluster_name \
             --query "cluster.version" \
             --output text)
         ```

      1. Retrieve the VPC ID that your cluster is in and store it in a variable for use in a later step\.

         ```
         vpc_id=$(aws eks describe-cluster \
             --name $cluster_name \
             --query "cluster.resourcesVpcConfig.vpcId" \
             --output text)
         ```

      1. Retrieve the ID of the control plane security group for your cluster and store it in a variable for use in a later step\.

         ```
         control_plane_security_group=$(aws eks describe-cluster \
             --name $cluster_name \
             --query "cluster.resourcesVpcConfig.clusterSecurityGroupId" \
             --output text)
         ```

      1. Get the list of subnet IDs in your VPC that are in an Availability Zone returned in step 1\.

         ```
         aws ec2 describe-subnets \
             --filters "Name=vpc-id,Values=$vpc_id" "Name=availability-zone,Values=us-west-2a" \
             --query 'Subnets[*].SubnetId' \
             --output text
         ```

         If no output is returned, try a different Availability Zone returned in step 1\. If none of your subnets are in an Availability Zone returned in step 1, then you need to create a subnet in an Availability Zone returned in step 1\. If you have no room in your VPC to create another subnet, then you may need to create a new cluster in a new VPC\. 

      1. Determine whether the subnet is a private subnet by checking the route table for the subnet\.

         ```
         aws ec2 describe-route-tables \
             --filter Name=association.subnet-id,Values=subnet-0d403852a65210a29 \
             --query "RouteTables[].Routes[].GatewayId" \
             --output text
         ```

         Output

         ```
         local
         ```

         If the output is `local igw-02adc64c1b72722e2`, then the subnet is a public subnet\. You must select a private subnet in an Availability Zone returned in step 1\. Once you've identified a private subnet, note its ID for use in a later step\.

      1. Set a variable with the private subnet ID from the previous step for use in later steps\.

         ```
         subnet_id=your-subnet-id
         ```

   1. Download the AWS CloudFormation template\.

      ```
      curl -o efa-p4d-managed-nodegroup.yaml https://raw.githubusercontent.com/aws-samples/aws-efa-eks/main/cloudformation/efa-p4d-managed-nodegroup.yaml
      ```

   1. Copy the following text to your computer\. Replace *p4d\.24xlarge* with an instance type from step 1\. Replace *subnet\-0d403852a65210a29* with the ID of the private subnet that you identified in step 2\.b\.v\. Replace *path\-to\-downloaded\-cfn\-template* with the path to the `efa-p4d-managed-nodegroup.yaml` that you downloaded in the previous step\. Replace *your\-public\-key\-name* with the name of your public key\. Once you've made the replacements, run the modified command\.

      ```
      aws cloudformation create-stack \
          --stack-name ${node_group_resources_name} \
          --capabilities CAPABILITY_IAM \
          --template-body file://path-to-downloaded-cfn-template \
          --parameters \
             ParameterKey=ClusterName,ParameterValue=${cluster_name} \
             ParameterKey=ClusterControlPlaneSecurityGroup,ParameterValue=${control_plane_security_group} \
             ParameterKey=VpcId,ParameterValue=${vpc_id} \
             ParameterKey=SubnetId,ParameterValue=${subnet_id} \
             ParameterKey=NodeGroupName,ParameterValue=${node_group_name} \
             ParameterKey=NodeImageIdSSMParam,ParameterValue=/aws/service/eks/optimized-ami/${cluster_version}/amazon-linux-2-gpu/recommended/image_id \
             ParameterKey=KeyName,ParameterValue=your-public-key-name \
             ParameterKey=NodeInstanceType,ParameterValue=p4d.24xlarge
      ```

   1. Determine when the stack that you deployed in the previous step is deployed\.

      ```
      aws cloudformation wait stack-create-complete --stack-name $node_group_resources_name
      ```

      There is no output from the previous command, but your shell prompt doesn't return until the stack is created\.

   1. Create your node group using the resources created by the AWS CloudFormation stack in the previous step\.

      1. Retrieve information from the deployed AWS CloudFormation stack and store it in variables\.

         ```
         node_instance_role=$(aws cloudformation describe-stacks \
             --stack-name $node_group_resources_name \
             --query='Stacks[].Outputs[?OutputKey==`NodeInstanceRole`].OutputValue' \
             --output text)
         launch_template=$(aws cloudformation describe-stacks \
             --stack-name $node_group_resources_name \
             --query='Stacks[].Outputs[?OutputKey==`LaunchTemplateID`].OutputValue' \
             --output text)
         ```

      1. Create a managed node group that uses the launch template and node IAM role that were created in the previous step\.

         ```
         aws eks create-nodegroup \
             --cluster-name $cluster_name \
             --nodegroup-name $node_group_name \
             --node-role $node_instance_role \
             --subnets $subnet_id \
             --launch-template id=$launch_template,version=1
         ```

      1. Confirm that the nodes were created\.

         ```
         aws eks describe-nodegroup \
            --cluster-name ${cluster_name} \
            --nodegroup-name ${node_group_name} | jq -r .nodegroup.status
         ```

         Don't continue until the status returned from the previous command is `ACTIVE`\. It can take several minutes for the nodes to become ready\.

   1. Deploy the EFA Kubernetes device plugin\.

      The EFA Kubernetes device plugin detects and advertises EFA interfaces as allocatable resources to Kubernetes\. An application can consume the extended resource type `vpc.amazonaws.com/efa` in a pod request spec just like CPU and memory\. For more information, see [Consuming extended resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#consuming-extended-resources) in the Kubernetes documentation\. Once requested, the plugin automatically assigns and mounts an EFA interface to the pod\. Using the device plugin simplifies EFA setup and does not require a pod to run in privileged mode\.

      ```
      kubectl apply -f https://raw.githubusercontent.com/aws-samples/aws-efa-eks/main/manifest/efa-k8s-device-plugin.yml
      ```

   1. If you deployed an instance type with a GPU, deploy the NVIDIA Kubernetes device plugin\.

      ```
      kubetl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
      ```

------

## \(Optional\) Deploy a sample EFA compatible application<a name="efa-application"></a>

**Deploy the Kubeflow MPI Operator**  
For the NCCL tests you can apply the Kubeflow MPI Operator\. The MPI Operator makes it easy to run Allreduce\-style distributed training on Kubernetes\. For more information, see [MPI Operator](https://github.com/kubeflow/mpi-operator) on GitHub\.

```
kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v1alpha2/mpi-operator.yaml
```

**Run the multi\-node NCCL Performance Test to verify GPUDirectRDMA/EFA**  
To verify NCCL Performance with GPUDirectRDMA over EFA, run the standard NCCL Performance test\. For more information, see the official [NCCL\-Tests](https://github.com/NVIDIA/nccl-tests.git) repo on GitHub\. You can use the sample [Dockerfile](https://github.com/aws-samples/aws-efa-eks/blob/main/Dockerfile) that comes with this test already built for both CUDA 11\.2 and the latest version of EFA\. 

Alternately, you can download an AWS Docker image available from an [Amazon ECR repo](https://gallery.ecr.aws/w6p6i9i7/aws-efa-nccl-rdma)\. 

**Important**  
An important consideration required for adopting EFA with Kubernetes is configuring and managing Huge Pages as a resource in the cluster\. For more information, see [Manage Huge Pages](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/) in the Kubernetes documentation\. Amazon EC2 instances with the EFA driver installed pre\-allocate 5128 2M Huge Pages, which you can request as resources to consume in your job specifications\.

Complete the following steps to run a two node NCCL Performance Test\. In the example NCCL test job, each worker requests eight GPUs, 5210Mi of hugepages\-2Mi, four EFAs, and 8000Mi of memory, which effectively means each worker consumes all the resources of a `p4d.24xlarge` instance\.

1. Create the NCCL\-tests job\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws-samples/aws-efa-eks/main/examples/simple/nccl-efa-tests.yaml
   ```

   Output

   mpijob\.kubeflow\.org/nccl\-tests\-efa created

1. View your running pods\.

   ```
   kubectl get pods
   ```

   Output

   ```
   NAME                             READY   STATUS     RESTARTS   AGE
   nccl-tests-efa-launcher-nbql9  0/1     Init:0/1   0          2m49s
   nccl-tests-efa-worker-0          1/1     Running    0          2m49s
   nccl-tests-efa-worker-1          1/1     Running    0          2m49s
   ```

   The MPI Operator creates a launcher pod and 2 worker pods \(one on each node\)\.

1. View the log for the `efa-launcher` pod\. Replace `wzr8j` with the value from your output\.

   ```
   kubectl logs -f nccl-tests-efa-launcher-nbql9
   ```

For more examples, see the Amazon EKS [EFA samples](https://github.com/aws-samples/aws-efa-eks) repository on GitHub\.