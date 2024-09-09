# Run machine learning training on Amazon EKS with Elastic Fabric Adapter<a name="node-efa"></a>

This topic describes how to integrate Elastic Fabric Adapter \(EFA\) with Pods deployed in your Amazon EKS cluster\. Elastic Fabric Adapter \(EFA\) is a network interface for Amazon EC2 instances that enables you to run applications requiring high levels of inter\-node communications at scale on AWS\. Its custom\-built operating system bypass hardware interface enhances the performance of inter\-instance communications, which is critical to scaling these applications\. With EFA, High Performance Computing \(HPC\) applications using the Message Passing Interface \(MPI\) and Machine Learning \(ML\) applications using NVIDIA Collective Communications Library \(NCCL\) can scale to thousands of CPUs or GPUs\. As a result, you get the application performance of on\-premises HPC clusters with the on\-demand elasticity and flexibility of the AWS cloud\. Integrating EFA with applications running on Amazon EKS clusters can reduce the time to complete large scale distributed training workloads without having to add additional instances to your cluster\. For more information about EFA, [Elastic Fabric Adapter](https://aws.amazon.com/hpc/efa/)\.

## Instance types with EFA<a name="efa-instances"></a>

The *AWS EFA Kubernetes Device Plugin* supports all Amazon EC2 instance types that have EFA\. To see a list of all instance types that have EFA, see [Supported instance types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html#efa-instance-types) in the *Amazon EC2 User Guide*\. However, to run ML applications quickly, we recommend that an instance has hardware acceleration chips such as nVidia GPUs, [AWS Inferentia](https://aws.amazon.com/machine-learning/inferentia/) chips, or [AWS Trainium](https://aws.amazon.com/machine-learning/trainium/) chips, in addition to the EFA\. To see a list of instance types that have hardware acceleration chips and EFA, see [Accelerated computing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html#efa-instance-types) in the *Amazon EC2 User Guide*\.

As you compare instance types to choose between them, consider the number of EFA network cards available for that instance type as well as the number of accelerator cards, amount of CPU, and amount of memory\. You can assign up to one EFA per network card\. An EFA counts as a network interface\.\. To see how many EFA are available for each instance types that have EFA, see the [Network cards](AWSEC2/latest/UserGuide/using-eni.html#network-cards) list in the *Amazon EC2 User Guide*\.

## Prerequisites<a name="efa-prereqs"></a>
+ An existing Amazon EKS cluster\. If you don't have an existing cluster, use one of our [Get started with Amazon EKS](getting-started.md) guides to create one\. Your cluster must be deployed in a VPC that has at least one private subnet with enough available IP addresses to deploy nodes in\. The private subnet must have outbound internet access provided by an external device, such as a NAT gateway\.

  If you plan to use `eksctl` to create your node group, `eksctl` can also create a cluster for you\. 
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.29`, you can use `kubectl` version `1.28`, `1.29`, or `1.30` with it\. To install or upgrade `kubectl`, see [Set up `kubectl` and `eksctl`](install-kubectl.md)\.
+ You must have the Amazon VPC CNI plugin for Kubernetes version `1.7.10` or later installed before launching worker nodes that support multiple Elastic Fabric Adapters, such as the `p4d` or `p5`\. For more information about updating your Amazon VPC CNI plugin for Kubernetes version, see [Assign IPs to Pods with the Amazon VPC CNI](managing-vpc-cni.md)\.

**Important**  
An important consideration required for adopting EFA with Kubernetes is configuring and managing Huge Pages as a resource in the cluster\. For more information, see [Manage Huge Pages](https://kubernetes.io/docs/tasks/manage-hugepages/scheduling-hugepages/) in the Kubernetes documentation\. Amazon EC2 instances with the EFA driver installed pre\-allocate 5128 2MiB Huge Pages, which you can request as resources to consume in your job specifications\.

## Create node group<a name="efa-create-nodegroup"></a>

The following procedure helps you create a node group with a `p4d.24xlarge` backed node group with EFA interfaces and GPUDirect RDMA, and run an example NVIDIA Collective Communications Library \(NCCL\) test for multi\-node NCCL Performance using EFAs\. The example can be used a template for distributed deep learning training on Amazon EKS using EFAs\.

1. Determine which Amazon EC2 instance types that support EFA are available in the AWS Region that you want to deploy nodes in\. Replace `region-code` with the AWS Region that you want to deploy your node group in\.

   ```
   aws ec2 describe-instance-types --region region-code \
       --filters Name=network-info.efa-supported,Values=true \
       --query "InstanceTypes[*].[InstanceType]" --output text
   ```

   When you deploy nodes, the instance type that you want to deploy must be available in the AWS Region that your cluster is in\.

1. Determine which Availability Zones that the instance type that you want to deploy is available in\. In this tutorial, the `p5.48xlarge` instance type is used and must be returned in the output for the AWS Region that you specified in the previous step\. When you deploy nodes in a production cluster, replace `p5.48xlarge` with any instance type returned in the previous step\. 

   ```
   aws ec2 describe-instance-type-offerings --region region-code \
       --location-type availability-zone --filters Name=instance-type,Values=p4d.24xlarge,p5.48xlarge \
       --query 'InstanceTypeOfferings[*].Location' --output text
   ```

   An example output is as follows\.

   ```
   us-west-2a    us-west-2c    us-west-2b
   ```

   Note the Availability Zones returned for use in later steps\. When you deploy nodes to a cluster, your VPC must have subnets with available IP addresses in one of the Availability Zones returned in the output\.

1. Create a node group using `eksctl`\.

**Prerequisite**  
Version `0.190.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

   1. Copy the following contents to a file named `efa-cluster.yaml`\. Replace the `example values` with your own\. You can replace `p5.48xlarge` with a different instance, but if you do, make sure that the values for `availabilityZones` are Availability Zones that were returned for the instance type in step 1\.

      ```
      apiVersion: eksctl.io/v1alpha5
      kind: ClusterConfig
      
      metadata:
        name: my-efa-cluster
        region: region-code
        version: "1.XX"
      
      iam:
        withOIDC: true
      
      availabilityZones: ["us-west-2a", "us-west-2c"]  
      
      managedNodeGroups:
        - name: my-efa-ng
          instanceType: p5.48xlarge
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
**Note**  
Because the instance type used in this example has GPUs, `eksctl` automatically installs the NVIDIA Kubernetes device plugin on each instance for you\.

1. Deploy the EFA Kubernetes device plugin\.

   The EFA Kubernetes device plugin detects and advertises EFA interfaces as allocatable resources to Kubernetes\. An application can consume the extended resource type `vpc.amazonaws.com/efa` in a Pod request spec just like CPU and memory\. For more information, see [Consuming extended resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#consuming-extended-resources) in the Kubernetes documentation\. Once requested, the plugin automatically assigns and mounts an EFA interface to the Pod\. Using the device plugin simplifies EFA setup and does not require a Pod to run in privileged mode\.

   ```
   helm repo add eks https://aws.github.io/eks-charts
   helm install aws-efa-k8s-device-plugin --namespace kube-system eks/aws-efa-k8s-device-plugin
   ```

## \(Optional\) Test the performance of the EFA<a name="efa-application"></a>

We recommend that you test the EFA setup\. You can use the [NCCL Tests](https://github.com/aws-samples/awsome-distributed-training/tree/main/micro-benchmarks/nccl-tests) in the `aws-samples/awsome-distributed-training` repository on GitHub\. [NCCL Tests](https://github.com/NVIDIA/nccl-tests) evaluate the performance of the network using the Nvidia Collective Communication Library\. The following steps submit NCCL tests on Amazon EKS\.

1. 

**Deploy the Kubeflow MPI Operator**

   For the NCCL tests you can apply the Kubeflow MPI Operator\. The MPI Operator makes it easy to run Allreduce\-style distributed training on Kubernetes\. For more information, see [MPI Operator](https://github.com/kubeflow/mpi-operator) on GitHub\.

1. 

**Run the multi\-node NCCL Performance Test to verify GPUDirectRDMA/EFA**

   To verify NCCL performance with GPUDirectRDMA over EFA, run the standard NCCL Performance test\. For more information, see the official [NCCL\-Tests](https://github.com/NVIDIA/nccl-tests.git) repo on GitHub\.

   Complete the following steps to run a two node NCCL Performance Test\. In the example NCCL test job, each worker requests eight GPUs, 5210Mi of `hugepages-2Mi`, four EFAs, and 8000Mi of memory, which effectively means each worker consumes all the resources of a `p5.48xlarge` instance\.

   1. 

**Create the MPIJob manifest**

      Copy the following to a file named `nccl-tests.yaml`:

      ```
      apiVersion: kubeflow.org/v2beta1
      kind: MPIJob
      metadata:
        name: nccl-tests
      spec:
        runPolicy:
          cleanPodPolicy: Running
          backoffLimit: 20
        slotsPerWorker: 8
        mpiReplicaSpecs:
          Launcher:
            replicas: 1
            template:
               spec:
                restartPolicy: OnFailure
                containers:
                - image: public.ecr.aws/hpc-cloud/nccl-tests:latest
                  imagePullPolicy: IfNotPresent
                  name: test-nccl-launcher
                  env:
                   - name: PATH
                     value: $PATH:/opt/amazon/efa/bin:/usr/bin
                   - name: LD_LIBRARY_PATH
                     value: /opt/amazon/openmpi/lib:/opt/nccl/build/lib:/opt/amazon/efa/lib:/opt/aws-ofi-nccl/install/lib:/usr/local/nvidia/lib:$LD_LIBRARY_PATH
                   - name: NCCL_DEBUG
                     value: INFO
                   - name: NCCL_BUFFSIZE
                     value: '8388608'
                   - name: NCCL_P2P_NET_CHUNKSIZE
                     value: '524288'
                   - name: NCCL_TUNER_PLUGIN
                     value: /opt/aws-ofi-nccl/install/lib/libnccl-ofi-tuner.so
                  command:
                  - /opt/amazon/openmpi/bin/mpirun
                  - --allow-run-as-root
                  - --tag-output
                  - -np
                  - "16"
                  - -N
                  - "8"
                  - --bind-to
                  - none
                  - -x
                  - PATH
                  - -x
                  - LD_LIBRARY_PATH
                  - -x
                  - NCCL_DEBUG=INFO
                  - -x
                  - NCCL_BUFFSIZE
                  - -x
                  - NCCL_P2P_NET_CHUNKSIZE
                  - -x
                  - NCCL_TUNER_PLUGIN
                  - --mca
                  - pml
                  - ^cm,ucx
                  - --mca
                  - btl
                  - tcp,self
                  - --mca
                  - btl_tcp_if_exclude
                  - lo,docker0,veth_def_agent
                  - /opt/nccl-tests/build/all_reduce_perf
                  - -b
                  - "8"
                  - -e
                  - "16G"
                  - -f
                  - "2"
                  - -g
                  - "1"
                  - -c
                  - "1"
                  - -n
                  - "100"
          Worker:
            replicas: 2
            template:
              spec:
                nodeSelector:
                  node.kubernetes.io/instance-type: "p5.48xlarge"
                containers:
                - image: public.ecr.aws/hpc-cloud/nccl-tests:latest
                  imagePullPolicy: IfNotPresent
                  name: nccl-tests-worker
                  volumeMounts:
                  - name: shmem
                    mountPath: /dev/shm
                  resources:
                    limits:
                      nvidia.com/gpu: 8
                      hugepages-2Mi: 5120Mi
                      vpc.amazonaws.com/efa: 32
                      memory: 32000Mi
                    requests:
                      nvidia.com/gpu: 8
                      hugepages-2Mi: 5120Mi
                      vpc.amazonaws.com/efa: 32
                      memory: 32000Mi
                volumes:
                - name: shmem
                  hostPath:
                    path: /dev/shm
      ```

   1. 

**Apply the NCCL\-tests MPIJob**

      Submit the `MPIJob` by applying the manifest\. This will create two `p5.48xlarge` Amazon EC2 instances\.

      ```
      kubectl apply -f nccl-tests.yaml
      ```

      An example output is as follows\.

      ```
      mpijob.kubeflow.org/nccl-tests created
      ```

   1. 

**Verify that the job started pods**

      View your running Pods\.

      ```
      kubectl get pods
      ```

      An example output is as follows\.

      ```
      NAME                             READY   STATUS     RESTARTS   AGE
      nccl-tests-launcher-nbql9    0/1     Init:0/1   0          2m49s
      nccl-tests-worker-0          1/1     Running    0          2m49s
      nccl-tests-worker-1          1/1     Running    0          2m49s
      ```

      The MPI Operator creates a launcher Pod and 2 worker Pods \(one on each node\)\.

   1. 

**Verify that the job is running successfully with the logs**

      View the log for the `nccl-tests-launcher` Pod\. Replace `nbql9` with the value from your output\.

      ```
      kubectl logs -f nccl-tests-launcher-nbql9
      ```

If the test completed successfully, you can deploy your applications that use the Nvidia Collective Communication Library\.