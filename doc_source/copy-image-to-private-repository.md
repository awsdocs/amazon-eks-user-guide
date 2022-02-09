# Copy a container image to a private repository<a name="copy-image-to-private-repository"></a>

This topic describes how to copy a container image to a private repository\. If your cluster nodes can't access the images in a container repository, copy your container images to a private repository\. You can either copy them to Amazon ECR or an alternative repository that your nodes have access to\.

**Prerequisites**
+ The Docker engine installed and configured on your computer\. For instructions, see [Install Docker Engine](https://docs.docker.com/engine/install/) in the Docker documentation\.
+ Version 2\.4\.9 or later or 1\.22\.30 or later of the AWS CLI installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ An interface VPC endpoint for Amazon ECR if you want your nodes to pull container images from a private Amazon ECR repository over Amazon's network\. For more information, see [Create the VPC endpoints for Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html#ecr-setting-up-vpc-create) in the Amazon Elastic Container Registry User Guide\.

Complete the following steps to pull a container image from a public repository and push it to an Amazon ECR private repository\. In the following examples that are provided in this topic, an [AWS Load Balancer Controller](aws-load-balancer-controller.md) image is pulled\. When you follow these steps, make sure to replace the *example values* with the actual values for your `registry/repository:tag`\. 

**To create a local copy of a container image**

1. If you don't already have an Amazon ECR private repository or another private repository, then create one\. An Amazon ECR private repository name must start with a letter\. It can only contain lowercase letters, numbers, hyphens \(\-\), underscores \(\_\), and forward slashes \(/\)\. For more information, see [Creating a private repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html) in the Amazon Elastic Container Registry User Guide\. 

   In this example, `amazon/` is a namespace that's used for organizational purposes only\. It's optional\. You can name your repository whatever you choose\. As a best practice, create a separate repository for each image\. We recommend this because image tags must be unique within a repository\.

   ```
   aws ecr create-repository --repository-name amazon/aws-alb-ingress-controller
   ```

1. Determine the registry, repository, and tag \(optional\) of the image that you want to pull\. This information is in the `registry/repository[:tag]` format\.

   Many of the Amazon EKS topics about installing add\-ons require that you apply a manifest or a Helm chart\. However, before you apply a manifest or install a Helm chart, first view the contents of the manifest or chart's values file\. That way, you can determine the image information that's required to pull the image\.

   For example, you can find the following line in the [manifest file](https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.3.1/v2_3_1_full.yaml) for version 2\.3\.1 of the AWS Load Balancer Controller\. In this example, the repository is `amazon/aws-alb-ingress-controller`\. The registry is `docker.io`\. However, it isn't listed because it's prepended by default when Docker or Kubernetes pulls the image\.

   ```
   image: amazon/aws-alb-ingress-controller:v2.3.1
   ```

   For version 2\.3\.1 of the AWS Load Balancer Controller Helm chart [values](https://github.com/aws/eks-charts/blob/master/stable/aws-load-balancer-controller/values.yaml), you see the following lines\. In this example, `amazon/aws-load-balancer-controller` is the repository\. `602401143452.dkr.ecr.us-west-2.amazonaws.com` is the registry\.

   ```
   image:
     repository: 602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon/aws-load-balancer-controller
     tag: v2.3.1
   ```

1. Pull the container image from the Docker Hub registry using the `docker pull` command\. Alternatively, pull the image using `docker.io/amazon/aws-alb-ingress-controller:v2.3.1`\.

   ```
   docker pull amazon/aws-alb-ingress-controller:v2.3.1
   ```

   If you are pulling from the Amazon ECR repository that's specified in the Helm chart, first authenticate to the registry\.

   ```
   aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 602401143452.dkr.ecr.region-code.amazonaws.com
   ```

   After authenticating to the registry, pull the image\.

   ```
   docker pull 602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon/aws-load-balancer-controller:v2.3.1
   ```
**Tip**  
You might be able to create a pull through cache rule for the public repository that you pull from\. Once a pull through cache is created for an external public registry, simply pull an image from that external public registry using your Amazon ECR private registry URI and then Amazon ECR creates a repository and caches that image\. When a cached image is pulled using the Amazon ECR private registry URI, Amazon ECR checks the remote registry to see if there is a new version of the image and will update your private registry on a regular interval\. For more information, see [Using pull through cache rules](https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html) in the Amazon Elastic Container Registry User Guide\.

1. Tag the image that you pulled with the Amazon ECR registry, repository, and tag\. The following example assumes that you pulled the image from the manifest file\. Replace *111122223333* with your account ID and *region\-code* with an [Amazon EKS](https://docs.aws.amazon.com/general/latest/gr/eks.html) and [Amazon ECR](https://docs.aws.amazon.com/general/latest/gr/ecr.html) supported AWS Region that your nodes have access to\.

   ```
   docker tag amazon/aws-alb-ingress-controller:v2.3.1 111122223333.dkr.ecr.region-code.amazonaws.com/amazon/aws-alb-ingress-controller:v2.3.1
   ```

1. Authenticate to the private Amazon ECR registry that you created in the first step\. For more information, see [Registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth) in the Amazon Elastic Container Registry User Guide\.

   ```
   aws ecr get-login-password --region region-code | docker login --username AWS --password-stdin 111122223333.dkr.ecr.region-code.amazonaws.com
   ```

1. Push the image to your private Amazon ECR repository\. For more information, see [Pushing a Docker image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) in the Amazon Elastic Container Registry User Guide\.

   ```
   docker push 111122223333.dkr.ecr.region-code.amazonaws.com/amazon/aws-alb-ingress-controller:v2.3.1
   ```

1. Update the install manifest that you used to determine the image in a previous step to use the `registry/repository:tag` for the image that you pushed\. If you're installing with a Helm chart, there's often an option to specify the `registry/repository:tag`\. When installing the chart, specify the `registry/repository:tag` for the image that you pushed to your Amazon ECR private repository\.