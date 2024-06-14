# Machine learning inference using AWS Inferentia<a name="inferentia-support"></a>

This topic describes how to create an Amazon EKS cluster with nodes running [Amazon EC2 Inf1](https://aws.amazon.com/ec2/instance-types/inf1/) instances and \(optionally\) deploy a sample application\. Amazon EC2 Inf1 instances are powered by [AWS Inferentia](https://aws.amazon.com/machine-learning/inferentia/) chips, which are custom built by AWS to provide high performance and lowest cost inference in the cloud\. Machine learning models are deployed to containers using [AWS Neuron](https://aws.amazon.com/machine-learning/neuron/), a specialized software development kit \(SDK\) consisting of a compiler, runtime, and profiling tools that optimize the machine learning inference performance of Inferentia chips\. AWS Neuron supports popular machine learning frameworks such as TensorFlow, PyTorch, and MXNet\.

**Note**  
Neuron device logical IDs must be contiguous\. If a Pod requesting multiple Neuron devices is scheduled on an `inf1.6xlarge` or `inf1.24xlarge` instance type \(which have more than one Neuron device\), that Pod will fail to start if the Kubernetes scheduler selects non\-contiguous device IDs\. For more information, see [Device logical IDs must be contiguous](https://github.com/aws/aws-neuron-sdk/issues/110) on GitHub\.

## Prerequisites<a name="inferentia-prerequisites"></a>
+ Have `eksctl` installed on your computer\. If you don't have it installed, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
+ Have `kubectl` installed on your computer\. For more information, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ \(Optional\) Have `python3` installed on your computer\. If you don't have it installed, then see [Python downloads](https://www.python.org/downloads/) for installation instructions\.

## Create a cluster<a name="create-cluster-inferentia"></a>

**To create a cluster with Inf1 Amazon EC2 instance nodes**

1. Create a cluster with Inf1 Amazon EC2 instance nodes\. You can replace `inf1.2xlarge` with any [Inf1 instance type](https://aws.amazon.com/ec2/instance-types/inf1/)\. The `eksctl` utility detects that you are launching a node group with an `Inf1` instance type and will start your nodes using one of the Amazon EKS optimized accelerated Amazon Linux AMIs\. 
**Note**  
You can't use [IAM roles for service accounts](iam-roles-for-service-accounts.md) with TensorFlow Serving\.

   ```
   eksctl create cluster \
       --name inferentia \
       --region region-code \
       --nodegroup-name ng-inf1 \
       --node-type inf1.2xlarge \
       --nodes 2 \
       --nodes-min 1 \
       --nodes-max 4 \
       --ssh-access \
       --ssh-public-key your-key \
       --with-oidc
   ```
**Note**  
Note the value of the following line of the output\. It's used in a later \(optional\) step\.  

   ```
   [9]  adding identity "arn:aws:iam::111122223333:role/eksctl-inferentia-nodegroup-ng-in-NodeInstanceRole-FI7HIYS3BS09" to auth ConfigMap
   ```

   When launching a node group with `Inf1` instances, `eksctl` automatically installs the AWS Neuron Kubernetes device plugin\. This plugin advertises Neuron devices as a system resource to the Kubernetes scheduler, which can be requested by a container\. In addition to the default Amazon EKS node IAM policies, the Amazon S3 read only access policy is added so that the sample application, covered in a later step, can load a trained model from Amazon S3\.

1. Make sure that all Pods have started correctly\.

   ```
   kubectl get pods -n kube-system
   ```

   Abbreviated output:

   ```
   NAME                                   READY   STATUS    RESTARTS   AGE
   [...]
   neuron-device-plugin-daemonset-6djhp   1/1     Running   0          5m
   neuron-device-plugin-daemonset-hwjsj   1/1     Running   0          5m
   ```

## \(Optional\) Deploy a TensorFlow Serving application image<a name="deploy-tensorflow-serving-application"></a>

A trained model must be compiled to an Inferentia target before it can be deployed on Inferentia instances\. To continue, you will need a [Neuron optimized TensorFlow](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-guide/neuron-frameworks/tensorflow-neuron/index.html) model saved in Amazon S3\. If you don't already have a SavedModel, please follow the tutorial for [creating a Neuron compatible ResNet50 model](https://docs.aws.amazon.com/dlami/latest/devguide/tutorial-inferentia-tf-neuron.html) and upload the resulting SavedModel to S3\. ResNet\-50 is a popular machine learning model used for image recognition tasks\. For more information about compiling Neuron models, see [The AWS Inferentia Chip With DLAMI](https://docs.aws.amazon.com/dlami/latest/devguide/tutorial-inferentia.html) in the AWS Deep Learning AMI Developer Guide\.

The sample deployment manifest manages a pre\-built inference serving container for TensorFlow provided by AWS Deep Learning Containers\. Inside the container is the AWS Neuron Runtime and the TensorFlow Serving application\. A complete list of pre\-built Deep Learning Containers optimized for Neuron is maintained on GitHub under [Available Images](https://github.com/aws/deep-learning-containers/blob/master/available_images.md#neuron-inference-containers)\. At start\-up, the DLC will fetch your model from Amazon S3, launch Neuron TensorFlow Serving with the saved model, and wait for prediction requests\.

The number of Neuron devices allocated to your serving application can be adjusted by changing the `aws.amazon.com/neuron` resource in the deployment yaml\. Please note that communication between TensorFlow Serving and the Neuron runtime happens over GRPC, which requires passing the `IPC_LOCK` capability to the container\.

1. Add the `AmazonS3ReadOnlyAccess` IAM policy to the node instance role that was created in step 1 of [Create a cluster](#create-cluster-inferentia)\. This is necessary so that the sample application can load a trained model from Amazon S3\.

   ```
   aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
       --role-name eksctl-inferentia-nodegroup-ng-in-NodeInstanceRole-FI7HIYS3BS09
   ```

1. Create a file named `rn50_deployment.yaml` with the following contents\. Update the region\-code and model path to match your desired settings\. The model name is for identification purposes when a client makes a request to the TensorFlow server\. This example uses a model name to match a sample ResNet50 client script that will be used in a later step for sending prediction requests\. 

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
         containers:
           - name: eks-neuron-test
             image: 763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-inference-neuron:1.15.4-neuron-py37-ubuntu18.04
             command:
               - /usr/local/bin/entrypoint.sh
             args:
               - --port=8500
               - --rest_api_port=9000
               - --model_name=resnet50_neuron
               - --model_base_path=s3://your-bucket-of-models/resnet50_neuron/
             ports:
               - containerPort: 8500
               - containerPort: 9000
             imagePullPolicy: IfNotPresent
             env:
               - name: AWS_REGION
                 value: "us-east-1"
               - name: S3_USE_HTTPS
                 value: "1"
               - name: S3_VERIFY_SSL
                 value: "0"
               - name: S3_ENDPOINT
                 value: s3.us-east-1.amazonaws.com
               - name: AWS_LOG_LEVEL
                 value: "3"
             resources:
               limits:
                 cpu: 4
                 memory: 4Gi
                 aws.amazon.com/neuron: 1
               requests:
                 cpu: "1"
                 memory: 1Gi
             securityContext:
               capabilities:
                 add:
                   - IPC_LOCK
   ```

1. Deploy the model\.

   ```
   kubectl apply -f rn50_deployment.yaml
   ```

1. Create a file named `rn50_service.yaml` with the following contents\. The HTTP and gRPC ports are opened for accepting prediction requests\.

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
   kubectl apply -f rn50_service.yaml
   ```

## \(Optional\) Make predictions against your TensorFlow Serving service<a name="make-predictions-against-tensorflow-service"></a>

1. To test locally, forward the gRPC port to the `eks-neuron-test` service\.

   ```
   kubectl port-forward service/eks-neuron-test 8500:8500 &
   ```

1. Create a Python script called `tensorflow-model-server-infer.py` with the following content\. This script runs inference via gRPC, which is service framework\.

   ```
   import numpy as np
      import grpc
      import tensorflow as tf
      from tensorflow.keras.preprocessing import image
      from tensorflow.keras.applications.resnet50 import preprocess_input
      from tensorflow_serving.apis import predict_pb2
      from tensorflow_serving.apis import prediction_service_pb2_grpc
      from tensorflow.keras.applications.resnet50 import decode_predictions
      
      if __name__ == '__main__':
          channel = grpc.insecure_channel('localhost:8500')
          stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
          img_file = tf.keras.utils.get_file(
              "./kitten_small.jpg",
              "https://raw.githubusercontent.com/awslabs/mxnet-model-server/master/docs/images/kitten_small.jpg")
          img = image.load_img(img_file, target_size=(224, 224))
          img_array = preprocess_input(image.img_to_array(img)[None, ...])
          request = predict_pb2.PredictRequest()
          request.model_spec.name = 'resnet50_inf1'
          request.inputs['input'].CopyFrom(
              tf.make_tensor_proto(img_array, shape=img_array.shape))
          result = stub.Predict(request)
          prediction = tf.make_ndarray(result.outputs['output'])
          print(decode_predictions(prediction))
   ```

1. Run the script to submit predictions to your service\.

   ```
   python3 tensorflow-model-server-infer.py
   ```

   An example output is as follows\.

   ```
   [[(u'n02123045', u'tabby', 0.68817204), (u'n02127052', u'lynx', 0.12701613), (u'n02123159', u'tiger_cat', 0.08736559), (u'n02124075', u'Egyptian_cat', 0.063844085), (u'n02128757', u'snow_leopard', 0.009240591)]]
   ```