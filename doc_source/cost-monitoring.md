# Cost monitoring<a name="cost-monitoring"></a>

Amazon EKS supports Kubecost, which you can use to monitor your costs broken down by Kubernetes resources including pods, nodes, namespaces, and labels\. As a Kubernetes platform administrator and finance leader, you can use Kubecost to visualize a breakdown of Amazon EKS charges, allocate costs, and charge back organizational units such as application teams\. You can provide your internal teams and business units with transparent and accurate cost data based on their actual AWS bill\. Moreover, you can also get customized recommendations for cost optimization based on their infrastructure environment and usage patterns within their clusters\. For more information about Kubecost, see the [https://guide.kubecost.com](https://guide.kubecost.com) documentation\.

Amazon EKS provides an AWS optimized bundle of Kubecost for cluster cost visibility\. You can use your existing AWS support agreements to obtain support\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\. The cluster must have Amazon EC2 nodes because you can't run Kubecost on Fargate nodes\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.23`, you can use `kubectl` version `1.22`,`1.23`, or `1.24` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Helm version 3\.9\.0 or later configured on your device or AWS CloudShell\. To install or update Helm, see [Using Helm with Amazon EKS](helm.md)\.
+ If your cluster is version `1.23` or later, you must have the [Amazon EBS CSI driver](ebs-csi.md) installed on your cluster\.

**To install Kubecost**

1. Install Kubecost with the following command\. You can replace *1\.96\.0* with a later version\. You can see the available versions at [kubecost/cost\-analyzer](https://gallery.ecr.aws/kubecost/cost-analyzer) in the Amazon ECR Public Gallery\.

   ```
   helm upgrade -i kubecost oci://public.ecr.aws/kubecost/cost-analyzer --version 1.96.0 \
       --namespace kubecost --create-namespace \
       -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/develop/cost-analyzer/values-eks-cost-monitoring.yaml
   ```

   Kubecost releases new versions regularly\. You can update your version using [https://helm.sh/docs/helm/helm_upgrade/](https://helm.sh/docs/helm/helm_upgrade/)\. By default, the installation includes a local Prometheus server and `kube-state-metrics`\. You can customize your deployment to use [Amazon Managed Service for Prometheus](http://aws.amazon.com/blogs/mt/integrating-kubecost-with-amazon-managed-service-for-prometheus/) by following the documentation in [Integrating with Amazon EKS cost monitoring](https://docs.aws.amazon.com/prometheus/latest/userguide/integrating-kubecost.html)\. For a list of all other settings that you can configure, see the [sample configuration file](https://github.com/kubecost/cost-analyzer-helm-chart/blob/develop/cost-analyzer/values-eks-cost-monitoring.yaml) on GitHub\.

1. Make sure the required pods are running\.

   ```
   kubectl get pods -n kubecost
   ```

   The example output is as follows\.

   ```
   NAME                                          READY   STATUS    RESTARTS   AGE
   kubecost-cost-analyzer-b9788c99f-5vj5b        2/2     Running   0          3h27m
   kubecost-kube-state-metrics-99bb8c55b-bn2br   1/1     Running   0          3h27m
   kubecost-prometheus-server-7d9967bfc8-9c8p7   2/2     Running   0          3h27m
   ```

1. On your device, enable port\-forwarding to expose the Kubecost dashboard\.

   ```
   kubectl port-forward --namespace kubecost deployment/kubecost-cost-analyzer 9090
   ```

   Alternatively, you can use the [AWS Load Balancer Controller](aws-load-balancer-controller.md) to expose Kubecost and use Amazon Cognito for authentication, authorization, and user management\. For more information, see [How to use Application Load Balancer and Amazon Cognito to authenticate users for your Kubernetes web apps](http://aws.amazon.com/blogs/containers/how-to-use-application-load-balancer-and-amazon-cognito-to-authenticate-users-for-your-kubernetes-web-apps/)\.

1. On the same device that you completed the previous step on, open a web browser and enter the following address\.

   ```
   http://localhost:9090
   ```

   You see the Kubecost Overview page in your browser\. It might take 5–10 minutes for Kubecost to gather metrics\. You can see your Amazon EKS spend, including cumulative cluster costs, associated Kubernetes asset costs, and monthly aggregated spend\.  
![\[Kubecost dashboard\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubecost.png)

1. To track costs at a cluster level, tag your Amazon EKS resources for billing\. For more information, see [Tagging your resources for billing](eks-using-tags.md#tag-resources-for-billing)\.

**You can also view the following information by selecting it in the left pane of the dashboard:**
+ **Cost allocation** – View monthly Amazon EKS costs and cumulative costs for each of your namespaces and other dimensions over the past seven days\. This is helpful for understanding which parts of your application are contributing to Amazon EKS spend\.
+ **Assets** – View the costs of the AWS infrastructure assets that are associated with your Amazon EKS resources\.

**Additional features**
+ **Export cost metrics** – Amazon EKS optimized cost monitoring is deployed with Kubecost and Prometheus, which is an open\-source monitoring system and time series database\. Kubecost reads metric from Prometheus and then performs cost allocation calculations and writes the metrics back to Prometheus\. The Kubecost front\-end reads metrics from Prometheus and shows them on the Kubecost user interface\. The architecture is illustrated in the following diagram\.  
![\[Kubecost architecture\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubecost-architecture.png)

  With Prometheus pre\-installed, you can write queries to ingest Kubecost data into your current business intelligence system for further analysis\. You can also use it as a data source for your current Grafana dashboard to display Amazon EKS cluster costs that your internal teams are familiar with\. To learn more about how to write Prometheus queries, see the [Prometheus Configuration](https://github.com/opencost/opencost/blob/develop/PROMETHEUS.md) `readme` file on GitHub or use the example Grafana JSON models in the [Kubecost Github repository](https://github.com/kubecost/cost-analyzer-helm-chart/tree/develop/cost-analyzer) as references\.
+ **AWS Cost and Usage Report integration** – To perform cost allocation calculations for your Amazon EKS cluster, Kubecost retrieves the public pricing information of AWS services and AWS resources from the AWS Price List API\. You can also integrate Kubecost with **AWS Cost and Usage Report** to enhance the accuracy of the pricing information specific to your AWS account\. This information includes enterprise discount programs, reserved instance usage, savings plans, and spot usage\. To learn more about how the AWS Cost and Usage Report integration works, see [AWS Cloud Integration](https://guide.kubecost.com/hc/en-us/articles/4407595928087-AWS-Cloud-Integration#aws-cloud-integration) in the Kubecost documentation\.

## Remove Kubecost<a name="cost-monitoring-remove-kubecost"></a>

You can remove Kubecost from your cluster with the following commands\.

```
helm uninstall kubecost --namespace kubecost
kubectl delete ns kubecost
```

## Frequently asked questions<a name="cost-monitoring-faq"></a>

See the following common questions and answers about using Kubecost with Amazon EKS\.

### What is the difference between the custom bundle of Kubecost and the free version of Kubecost \(also known as OpenCost\)?<a name="cost-monitoring-faq-differences"></a>

AWS and Kubecost collaborated to offer a customized version of Kubecost\. This version includes a subset of commercial features at no additional charge\. In the customized Kubecost version, customers get all open source features of Kubecost, cost allocation features, integration with AWS Cost and Usage Reports (CUR) for accurate cost visibility, cost efficiency measurements, 15-days of metrics processing, authentication for the Kubecost endpoint using Amazon Cognito, and enterprise support\. The customized Kubecost version does not include multi-cloud support, optimization insights, alerts and governance, unlimited metrics processing, single sign on (SSO) and role based access control (RBAC) with SAML 2.0, and unnamed and future enterprise features of Kubecost\.


### Is there a charge for this functionality?<a name="cost-monitoring-faq-charge"></a>

No\. You can use this version of Kubecost at no additional charge\. If you want additional Kubecost capabilities that aren't included in this bundle, you can buy an enterprise license of Kubecost through the AWS Marketplace, or from Kubecost directly\.

### Is support available?<a name="cost-monitoring-faq-support"></a>

Yes\. You can open a support case with the AWS Support team at [Contact AWS](http://aws.amazon.com/contact-us/)\.

### Do I need a license to use Kubecost features provided by the Amazon EKS integration?<a name="cost-monitoring-faq-license"></a>

No\.

### Can I integrate Kubecost with AWS Cost and Usage Report for more accurate reporting?<a name="cost-monitoring-faq-cur"></a>

Yes\. You can configure Kubecost to ingest data from AWS Cost and Usage Report to get accurate cost visibility, including discounts, Spot pricing, reserved instance pricing, and others\. For more information, see [AWS Cloud Integration](https://guide.kubecost.com/hc/en-us/articles/4407595928087-AWS-Cloud-Integration) in the Kubecost documentation\.

### Does this version support cost management of self\-managed Kubernetes clusters on Amazon EC2?<a name="cost-monitoring-faq-self-managed"></a>

No\. This version is only compatible with Amazon EKS clusters\.

### Can Kubecost track costs for Amazon EKS on AWS Fargate?<a name="cost-monitoring-faq-fargate"></a>

Kubecost provides best effort to show cluster cost visibility for Amazon EKS on Fargate, but with lower accuracy than with Amazon EKS on Amazon EC2\. This is primarily due to the difference in how you're billed for your usage\. With Amazon EKS on Fargate, you're billed for consumed resources\. With Amazon EKS on Amazon EC2 nodes, you're billed for provisioned resources\. Kubecost calculates the cost of an Amazon EC2 node based on the node specification, which includes CPU, RAM, and ephemeral storage\. With Fargate, costs are calculated based on the requested resources for the Fargate pods\.

### How can I get updates and new versions of Kubecost?<a name="cost-monitoring-faq-updates"></a>

You can upgrade your Kubecost version using standard Helm upgrade procedures\. The latest versions are in the [Amazon ECR Public Gallery\.](https://gallery.ecr.aws/kubecost/cost-analyzer)

### Is the `kubectl-cost` CLI supported? How do I install it?<a name="cost-monitoring-faq-cli"></a>

Yes\. `Kubectl-cost` is an open source tool by Kubecost \(Apache 2\.0 License\) that provides CLI access to Kubernetes cost allocation metrics\. To install `kubectl-cost`, see [Installation](https://github.com/kubecost/kubectl-cost#installation) on GitHub\.

### Is the Kubecost user interface supported? How do I access it?<a name="cost-monitoring-faq-ui"></a>

Kubecost provides a web dashboard that you can access through `kubectl` port forwarding, an ingress, or a load balancer\. You can also use the AWS Load Balancer Controller to expose Kubecost and use Amazon Cognito for authentication, authorization\. and user management\. For more information, see [How to use Application Load Balancer and Amazon Cognito to authenticate users for your Kubernetes web apps](http://aws.amazon.com/blogs/containers/how-to-use-application-load-balancer-and-amazon-cognito-to-authenticate-users-for-your-kubernetes-web-apps/) on the AWS blog\.

### Is Amazon EKS Anywhere supported?<a name="cost-monitoring-faq-eks-a"></a>

No\.
