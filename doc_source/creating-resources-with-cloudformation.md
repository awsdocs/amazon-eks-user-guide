# Creating Amazon EKS resources with AWS CloudFormation<a name="creating-resources-with-cloudformation"></a>

Amazon EKS is integrated with AWS CloudFormation, a service that helps you model and set up your AWS resources so that you can spend less time creating and managing your resources and infrastructure\. You create a template that describes all the AWS resources that you want, for example an Amazon EKS cluster, and AWS CloudFormation takes care of provisioning and configuring those resources for you\. 

When you use AWS CloudFormation, you can reuse your template to set up your Amazon EKS resources consistently and repeatedly\. Just describe your resources once, and then provision the same resources over and over in multiple AWS accounts and Regions\.

## Amazon EKS and AWS CloudFormation templates<a name="working-with-templates"></a>

To provision and configure resources for Amazon EKS and related services, you must understand [AWS CloudFormation templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html)\. Templates are formatted text files in JSON or YAML\. These templates describe the resources that you want to provision in your AWS CloudFormation stacks\. If you're unfamiliar with JSON or YAML, you can use AWS CloudFormation Designer to help you get started with AWS CloudFormation templates\. For more information, see [What is AWS CloudFormation Designer?](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/working-with-templates-cfn-designer.html) in the *AWS CloudFormation User Guide*\.

Amazon EKS supports creating clusters and node groups  in AWS CloudFormation\. For more information, including examples of JSON and YAML templates for your Amazon EKS resources, see [Amazon EKS resource type reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EKS.html) in the *AWS CloudFormation User Guide*\.

## Learn more about AWS CloudFormation<a name="learn-more-cloudformation"></a>

To learn more about AWS CloudFormation, see the following resources:
+ [AWS CloudFormation](http://aws.amazon.com/cloudformation/)
+ [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
+ [AWS CloudFormation Command Line Interface User Guide](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html)

## Use App Mesh with Kubernetes<a name="gs-app-mesh"></a>

App Mesh is a service mesh that makes it easy to monitor and control services\. App Mesh standardizes how your services communicate, giving you end\-to\-end visibility and helping to ensure high availability for your applications\. App Mesh gives you consistent visibility and network traffic controls for every service in an application\. You can get started using App Mesh with Kubernetes by completing the [Getting started with AWS App Mesh and Kubernetes](https://docs.aws.amazon.com/app-mesh/latest/userguide/getting-started-kubernetes.html) tutorial in the AWS App Mesh User Guide\. The tutorial recommends that you have an existing Kubernetes cluster and applications deployed that you want to use App Mesh with\.