# Inferentia support<a name="inferentia-support"></a>

This topic describes how to create an Amazon EKS cluster with worker nodes running [Amazon EC2 Inf1](http://aws.amazon.com/ec2/instance-types/inf1/) instances and \(optionally\) deploy a sample application\. Amazon EC2 Inf1 instances are powered by [AWS Inferentia](http://aws.amazon.com/machine-learning/inferentia/) chips, which are custom built by AWS to provide high performance and lowest cost inference in the cloud\. Machine learning models are deployed to containers using [AWS Neuron](http://aws.amazon.com/machine-learning/neuron/), a specialized software development kit \(SDK\) consisting of a compiler, run\-time, and profiling tools that optimize the machine learning inference performance of Inferentia chips\. AWS Neuron supports popular machine learning frameworks such as TensorFlow, PyTorch, and MXNet\.

## Considerations<a name="inferentia-considerations"></a>
+ Inf1 instances are supported on Amazon EKS clusters running Kubernetes version 1\.14 and later\.
+ Neuron device logical IDs must be contiguous\. If a pod requesting multiple Neuron devices is scheduled on an `inf1.6xlarge` or `inf1.24xlarge` instance type \(which have more than one Neuron device\), that pod will fail to start if the Kubernetes scheduler selects non\-contiguous device IDs\. For more information, see [Device logical IDs must be contiguous](https://github.com/aws/aws-neuron-sdk/issues/110) on GitHub\.
+ Amazon EC2 Inf1 instances are not currently supported with managed node groups\.

## Prerequisites<a name="inferentia-prerequisites"></a>
+ Have `eksctl` installed on your computer\. If you don't have it installed, see [Install `eksctl`](getting-started-eksctl.md#install-eksctl) for installation instructions\.
+ Have `kubectl` installed on your computer\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ \(Optional\) Have `python3` installed on your computer\. If you don't have it installed, then see [Python downloads](https://www.python.org/downloads/) for installation instructions\.

## Create a cluster<a name="create-cluster-inferentia"></a>

**To create a cluster with Inf1 worker node instances**

1. Create a cluster with Inf1 worker nodes\. You can replace *inf1\.2xlarge* with any [Inf1 instance type](http://aws.amazon.com/ec2/instance-types/inf1/)\. `eksctl` detects that you are launching a node group with an Inf1 instance type and will start your worker nodes using the [EKS\-optimized accelerated AMI](eks-linux-ami-versions.md#eks-gpu-ami-versions)\.
**Note**  
You can't use [IAM roles for service accounts](iam-roles-for-service-accounts.md) with TensorFlow Serving\.

   ```
   eksctl create cluster \
       --name inferentia \
       --version 1.16 \
       --region region-code \
       --nodegroup-name ng-inf1 \
       --node-type inf1.2xlarge \
       --nodes 2 \
       --nodes-min 1 \
       --nodes-max 4
   ```
**Note**  
Note the value of the following line of the output\. It's used in a later \(optional\) step\.  

   ```
   [ℹ]  adding identity "arn:aws:iam::111122223333:role/eksctl-inferentia-nodegroup-ng-in-NodeInstanceRole-FI7HIYS3BS09" to auth ConfigMap
   ```

   When launching a node group with Inf1 instances, `eksctl` automatically installs the AWS Neuron Kubernetes device plugin\. This plugin advertises Neuron devices as a system resource to the Kubernetes scheduler, which can be requested by a container\. In addition to the default Amazon EKS worker node IAM policies, the Amazon S3 read only access policy is added so that the sample application, covered in a later step, can load a trained model from Amazon S3\.

1. Make sure that all pods have started correctly\.

   ```
   kubectl get pods -n kube-system
   ```

   Output

   ```
   NAME                                   READY   STATUS    RESTARTS   AGE
   aws-node-kx2m8                         1/1     Running   0          5m
   aws-node-q57pf                         1/1     Running   0          5m
   coredns-86d5cbb4bd-56dz2               1/1     Running   0          5m
   coredns-86d5cbb4bd-d6n4z               1/1     Running   0          5m
   kube-proxy-75zx6                       1/1     Running   0          5m
   kube-proxy-plkfq                       1/1     Running   0          5m
   neuron-device-plugin-daemonset-6djhp   1/1     Running   0          5m
   neuron-device-plugin-daemonset-hwjsj   1/1     Running   0          5m
   ```

## \(Optional\) Create a Neuron TensorFlow Serving application image<a name="create-neuron-tensorflow-application"></a>

**Note**  
Neuron will soon be available pre\-installed in [AWS Deep Learning Containers](https://docs.aws.amazon.com/deep-learning-containers/latest/devguide/what-is-dlc.html)\. For updates, check [AWS Neuron](http://aws.amazon.com/machine-learning/neuron/)\.

1. Create an Amazon ECR repository to store your application image\.

   ```
   aws ecr create-repository --repository-name tensorflow-model-server-neuron
   ```

   Note the `repositoryUri` returned in the output for use in a later step\.

1. Create a Dockerfile named `Dockerfile.tf-serving` with the following contents\. The Dockerfile contains the commands to build a [Neuron optimized TensorFlow Serving](https://github.com/aws/aws-neuron-sdk/blob/master/docs/tensorflow-neuron/tutorial-tensorflow-serving.md) application image\. Neuron TensorFlow Serving uses the same API as normal TensorFlow Serving\. The only differences are that the saved model must be compiled for Inferentia and the entry point is a different binary\.

   ```
   FROM amazonlinux:2
   
   RUN yum install -y awscli
   
   RUN echo $'[neuron] \n\
   name=Neuron YUM Repository \n\
   baseurl=https://yum.repos.neuron.amazonaws.com \n\
   enabled=1' > /etc/yum.repos.d/neuron.repo
   
   RUN rpm --import https://yum.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB
   
   RUN yum install -y tensorflow-model-server-neuron
   ```

1. Log your Docker client into your ECR repository\.

   ```
   aws ecr get-login-password \
       --region region-code \
       | docker login \
       --username AWS \
       --password-stdin 111122223333.dkr.ecr.region-code.amazonaws.com
   ```

1. Build the Docker image and upload it to the Amazon ECR repository created in a previous step\.

   ```
   docker build . -f Dockerfile.tf-serving -t tensorflow-model-server-neuron
   docker tag tensorflow-model-server-neuron:latest 111122223333.dkr.ecr.region-code.amazonaws.com/tensorflow-model-server-neuron:1.15.0
   docker push 111122223333.dkr.ecr.region-code.amazonaws.com/tensorflow-model-server-neuron:1.15.0
   ```
**Note**  
If you receive permission related issues from Docker, then you may need to configure Docker for non\-root user use\. For more information, see [Manage Docker as a non\-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) in the Docker documentation\. 

## \(Optional\) Deploy a TensorFlow Serving application image<a name="deploy-tensorflow-serving-application"></a>

A trained model must be compiled to an Inferentia target before it can be deployed on Inferentia instances\. To continue, you will need a [Neuron optimized TensorFlow](https://github.com/aws/aws-neuron-sdk/tree/master/docs/tensorflow-neuron) model saved in Amazon S3\. If you don’t already have a saved model, then you can follow the tutorial in the AWS Neuron documentation to [create a Neuron compatible BERT\-Large model](https://github.com/aws/aws-neuron-sdk/tree/master/src/examples/tensorflow/bert_demo#running-tensorflow-bert-large-with-aws-neuron) and upload it to S3\. [BERT](https://en.wikipedia.org/wiki/BERT_(language_model)) is a popular machine learning technique used for understanding natural language tasks\. For more information about compiling Neuron models, see [The AWS Inferentia Chip With DLAMI](https://docs.aws.amazon.com/dlami/latest/devguide/tutorial-inferentia.html) in the AWS Deep Learning AMI Developer Guide\.

The sample deployment manifest manages two containers: The Neuron runtime container image and the TensorFlow Serving application\. For more information about the Neuron container image, see [Tutorial: Neuron container tools](https://github.com/aws/aws-neuron-sdk/tree/master/docs/neuron-container-tools) on GitHub\. The Neuron runtime runs as a sidecar container image and is used to interact with the Inferentia chips on your worker nodes\. The two containers communicate over a Unix domain socket placed in a shared mounted volume\. At start\-up, the application image will fetch your model from Amazon S3, launch Neuron TensorFlow Serving with the saved model, and wait for prediction requests\.

The number of Inferentia devices can be adjusted using the `aws.amazon.com/neuron` resource in the Neuron runtime container specification\. The runtime expects 128 2\-MB pages per Inferentia device, therefore, `hugepages-2Mi` has to be set to `256 x the number of Inferentia devices`\. In order to access Inferentia devices, the Neuron runtime requires `SYS_ADMIN` and `IPC_LOCK` capabilities, however, the runtime drops these capabilities at initialization, before opening a gRPC socket\.

1. Add the `AmazonS3ReadOnlyAccess` IAM policy to the worker node instance role that was created in step 1 of [Create a cluster](#create-cluster-inferentia)\. This is necessary so that the sample application can load a trained model from Amazon S3\.

   ```
   aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
       --role-name eksctl-inferentia-nodegroup-ng-in-NodeInstanceRole-FI7HIYS3BS09
   ```

1. Create a file named `bert_deployment.yaml` with the contents below\. Update *111122223333*, *region\-code*, and *bert/saved\_model* with your account ID, Region code, and saved model name and location\. The model name is for identification purposes when a client makes a request to the TensorFlow server\. This example uses a model name to match a sample BERT client script that will be used in a later step for sending prediction requests\. You can also replace *1\.0\.7865\.0* with a later version\. For the latest version, see [Neuron Runtime Release Notes](https://github.com/aws/aws-neuron-sdk/blob/master/release-notes/neuron-runtime.md) on GitHub or enter the following command\.

   ```
   aws ecr list-images --repository-name neuron-rtd --registry-id 790709498068 --region us-west-2
   ```

   ```
   kind: Deployment
   apiVersion: apps/v1
   metadata:
     name: eks-neuron-test
     labels:
       app: eks-neuron-test
       role: master
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: eks-neuron-test
         role: master
     template:
       metadata:
         labels:
           app: eks-neuron-test
           role: master
       spec:
         volumes:
           - name: sock
             emptyDir: {}
         containers:
           - name: eks-neuron-test
             image: 111122223333.dkr.ecr.region-code.amazonaws.com/tensorflow-model-server-neuron:1.15.0
             command:
               - /usr/local/bin/tensorflow_model_server_neuron
             args:
               - --port=9000
               - --rest_api_port=8500
               - --model_name=bert_mrpc_hc_gelus_b4_l24_0926_02
               - --model_base_path=s3://bert/saved_model
             ports:
               - containerPort: 8500
               - containerPort: 9000
             imagePullPolicy: IfNotPresent
             env:
               - name: AWS_REGION
                 value: "region-code"
               - name: S3_USE_HTTPS
                 value: "1"
               - name: S3_VERIFY_SSL
                 value: "0"
               - name: AWS_LOG_LEVEL
                 value: "3"
               - name: NEURON_RTD_ADDRESS
                 value: unix:/sock/neuron.sock
             resources:
               limits:
                 cpu: 4
                 memory: 4Gi
               requests:
                 cpu: "1"
                 memory: 1Gi
             volumeMounts:
               - name: sock
                 mountPath: /sock
           - name: neuron-rtd
             image: 790709498068.dkr.ecr.region-code.amazonaws.com/neuron-rtd:1.0.7865.0
             securityContext:
               capabilities:
                 add:
                   - SYS_ADMIN
                   - IPC_LOCK
             volumeMounts:
               - name: sock
                 mountPath: /sock
             resources:
               limits:
                 hugepages-2Mi: 256Mi
                 aws.amazon.com/neuron: 1
               requests:
                 memory: 1024Mi
   ```

1. Deploy the model\.

   ```
   kubectl apply -f bert_deployment.yaml
   ```

1. Create a file named `bert_service.yaml` with the following contents\. The HTTP and gRPC ports are opened for accepting prediction requests\.

   ```
   kind: Service
   apiVersion: v1
   metadata:
     name: eks-neuron-test
     labels:
       app: eks-neuron-test
   spec:
     type: ClusterIP
     ports:
       - name: http-tf-serving
         port: 8500
         targetPort: 8500
       - name: grpc-tf-serving
         port: 9000
         targetPort: 9000
     selector:
       app: eks-neuron-test
       role: master
   ```

1. Create a Kubernetes service for your TensorFlow model Serving application\.

   ```
   kubectl apply -f bert_service.yaml
   ```

## \(Optional\) Make predictions against your TensorFlow Serving service<a name="make-predictions-against-tensorflow-service"></a>

1. To test locally, forward the gRPC port to the `eks-neuron-test` service\.

   ```
   kubectl port-forward svc/eks-neuron-test 9000:9000 &
   ```

1. Download the sample BERT client from the Neuron GitHub repository\.

   ```
   curl https://raw.githubusercontent.com/aws/aws-neuron-sdk/master/src/examples/tensorflow/k8s_bert_demo/bert_client.py > bert_client.py
   ```

1. Run the script to submit predictions to your service\.

   ```
   python3 bert_client.py
   ```

   Output

   ```
   ...
   Inference successful: 0
   Inference successful: 1
   Inference successful: 2
   Inference successful: 3
   Inference successful: 4
   Inference successful: 5
   Inference successful: 6
   Inference successful: 7
   Inference successful: 8
   Inference successful: 9
   ...
   Inference successful: 91
   Inference successful: 92
   Inference successful: 93
   Inference successful: 94
   Inference successful: 95
   Inference successful: 96
   Inference successful: 97
   Inference successful: 98
   Inference successful: 99
   Ran 100 inferences successfully. Latency
   ```