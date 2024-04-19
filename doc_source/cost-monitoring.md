# Cost monitoring<a name="cost-monitoring"></a>

Cost monitoring is an essential aspect of managing your Kubernetes clusters on Amazon EKS\. By gaining visibility into your cluster costs, you can optimize resource utilization, set budgets, and make data\-driven decisions about your deployments\. Amazon EKS provides two cost monitoring solutions, each with its own unique advantages, to help you track and allocate your costs effectively:

**AWS Billing split cost allocation data for Amazon EKS** — This native feature integrates seamlessly with the AWS Billing Console, allowing you to analyze and allocate costs using the same familiar interface and workflows you use for other AWS services\. With split cost allocation, you can gain insights into your Kubernetes costs directly alongside your other AWS spend, making it easier to optimize costs holistically across your AWS environment\. You can also leverage existing AWS Billing features like Cost Categories and Cost Anomaly Detection to further enhance your cost management capabilities\. For more information, see [Understanding split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html) in the AWS Billing User Guide\.

**Kubecost** — Amazon EKS supports Kubecost, a Kubernetes cost monitoring tool\. Kubecost offers a feature\-rich, Kubernetes\-native approach to cost monitoring, providing granular cost breakdowns by Kubernetes resources, cost optimization recommendations, and out\-of\-the\-box dashboards and reports\. Kubecost also retrieves accurate pricing data by integrating with the AWS Cost and Usage Report, ensuring you get a precise view of your Amazon EKS costs\. Learn how to [Install Kubecost](#install-kubecost-procedure)\.

## AWS Billing — Split Cost Allocation<a name="cost-monitoring-aws"></a>

**Cost monitoring using AWS split cost allocation data for Amazon EKS**  
You can use AWS split cost allocation data for Amazon EKS to get granular cost visibility for your Amazon EKS clusters\. This enables you to analyze, optimize, and chargeback cost and usage for your Kubernetes applications\. You allocate application costs to individual business units and teams based on Amazon EC2 CPU and memory resources consumed by your Kubernetes application\. Split cost allocation data for Amazon EKS gives visibility into cost per Pod, and enables you to aggregate the cost data per Pod using namespace, cluster, and other Kubernetes primitives\. The following are examples of Kubernetes primitives that you can use to analyze Amazon EKS cost allocation data\. 
+  Cluster name 
+  Deployment 
+  Namespace 
+  Node 
+  Workload Name 
+  Workload Type 

For more information about using split cost allocation data, see [Understanding split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html) in the AWS Billing User Guide\.

### Set up Cost and Usage Reports<a name="task-cur-setup"></a>

You can turn on Split Cost Allocation Data for EKS in the Cost Management Console, AWS Command Line Interface, or the AWS SDKs\.

Use the following for *Split Cost Allocation Data*:

1. Opt in to Split Cost Allocation Data\. For more information, see [Enabling split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/enabling-split-cost-allocation-data.html) in the AWS Cost and Usage Report User Guide\.

1. Include the data in a new or existing report\.

1. View the report\. You can use the Billing and Cost Management console or view the report files in Amazon Simple Storage Service\.

## Kubecost<a name="cost-monitoring-kubecost"></a>

Amazon EKS supports Kubecost, which you can use to monitor your costs broken down by Kubernetes resources including Pods, nodes, namespaces, and labels\. As a Kubernetes platform administrator and finance leader, you can use Kubecost to visualize a breakdown of Amazon EKS charges, allocate costs, and charge back organizational units such as application teams\. You can provide your internal teams and business units with transparent and accurate cost data based on their actual AWS bill\. Moreover, you can also get customized recommendations for cost optimization based on their infrastructure environment and usage patterns within their clusters\. For more information about Kubecost, see the [https://guide.kubecost.com](https://guide.kubecost.com) documentation\.

Amazon EKS provides an AWS optimized bundle of Kubecost for cluster cost visibility\. You can use your existing AWS support agreements to obtain support\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\. The cluster must have Amazon EC2 nodes because you can't run Kubecost on Fargate nodes\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Helm version 3\.9\.0 or later configured on your device or AWS CloudShell\. To install or update Helm, see [Using Helm with Amazon EKS](helm.md)\.
+ If your cluster is version `1.23` or later, you must have the [Amazon EBS CSI driver](ebs-csi.md) installed on your cluster\.

**To install Kubecost**

1. Determine the version of Kubecost to install\. You can see the available versions at [kubecost/cost\-analyzer](https://gallery.ecr.aws/kubecost/cost-analyzer) in the Amazon ECR Public Gallery\. For more information about the compability of Kubecost versions and Amazon EKS, see the [Environment Requirements](https://docs.kubecost.com/install-and-configure/install/environment) in the Kubecost documentation\. 

1. Install Kubecost with the following command\. Replace *kubecost\-version* with the value retreived from ECR, such as *1\.108\.1*\.

   ```
   helm upgrade -i kubecost oci://public.ecr.aws/kubecost/cost-analyzer --version kubecost-version \
       --namespace kubecost --create-namespace \
       -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/develop/cost-analyzer/values-eks-cost-monitoring.yaml
   ```

   Kubecost releases new versions regularly\. You can update your version using [https://helm.sh/docs/helm/helm_upgrade/](https://helm.sh/docs/helm/helm_upgrade/)\. By default, the installation includes a local [https://prometheus.io/](https://prometheus.io/) server and `kube-state-metrics`\. You can customize your deployment to use [Amazon Managed Service for Prometheus](https://aws.amazon.com/blogs/mt/integrating-kubecost-with-amazon-managed-service-for-prometheus/) by following the documentation in [Integrating with Amazon EKS cost monitoring](https://docs.aws.amazon.com/prometheus/latest/userguide/integrating-kubecost.html)\. For a list of all other settings that you can configure, see the [sample configuration file](https://github.com/kubecost/cost-analyzer-helm-chart/blob/develop/cost-analyzer/values-eks-cost-monitoring.yaml) on GitHub\.

1. Make sure the required Pods are running\.

   ```
   kubectl get pods -n kubecost
   ```

   An example output is as follows\.

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

   Alternatively, you can use the [AWS Load Balancer Controller](aws-load-balancer-controller.md) to expose Kubecost and use Amazon Cognito for authentication, authorization, and user management\. For more information, see [How to use Application Load Balancer and Amazon Cognito to authenticate users for your Kubernetes web apps](https://aws.amazon.com/blogs/containers/how-to-use-application-load-balancer-and-amazon-cognito-to-authenticate-users-for-your-kubernetes-web-apps/)\.

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

  With [https://prometheus.io/](https://prometheus.io/) pre\-installed, you can write queries to ingest Kubecost data into your current business intelligence system for further analysis\. You can also use it as a data source for your current [https://grafana.com/](https://grafana.com/) dashboard to display Amazon EKS cluster costs that your internal teams are familiar with\. To learn more about how to write Prometheus queries, see the [Prometheus Configuration](https://github.com/opencost/opencost/blob/develop/PROMETHEUS.md) `readme` file on GitHub or use the example Grafana JSON models in the [Kubecost Github repository](https://github.com/kubecost/cost-analyzer-helm-chart/tree/develop/cost-analyzer) as references\.
+ **AWS Cost and Usage Report integration** – To perform cost allocation calculations for your Amazon EKS cluster, Kubecost retrieves the public pricing information of AWS services and AWS resources from the AWS Price List API\. You can also integrate Kubecost with **AWS Cost and Usage Report** to enhance the accuracy of the pricing information specific to your AWS account\. This information includes enterprise discount programs, reserved instance usage, savings plans, and spot usage\. To learn more about how the AWS Cost and Usage Report integration works, see [AWS Cloud Billing Integration](https://docs.kubecost.com/install-and-configure/install/cloud-integration/aws-cloud-integrations) in the Kubecost documentation\.

### Remove Kubecost<a name="cost-monitoring-remove-kubecost"></a>

You can remove Kubecost from your cluster with the following commands\.

```
helm uninstall kubecost --namespace kubecost
kubectl delete ns kubecost
```

### Frequently asked questions<a name="cost-monitoring-faq"></a>

See the following common questions and answers about using Kubecost with Amazon EKS\.

#### What is the difference between the custom bundle of Kubecost and the free version of Kubecost \(also known as OpenCost\)?<a name="cost-monitoring-faq-differences"></a>

AWS and Kubecost collaborated to offer a customized version of Kubecost\. This version includes a subset of commercial features at no additional charge\. See the following table for features that are included with in the custom bundle of Kubecost\.


| Feature | Kubecost free tier | Amazon EKS optimized Kubecost custom bundle | Kubecost Enterprise | 
| --- | --- | --- | --- | 
| Deployment | User hosted | User hosted | User hosted or Kubecost hosted \(SaaS\) | 
| Number of clusters supported | Unlimited | Unlimited | Unlimited | 
| Databases supported | Local Prometheus | Local Prometheus or Amazon Managed Service for Prometheus | Prometheus, Amazon Managed Service for Prometheus, Cortex, or Thanos | 
| Database retention support | 15 days | Unlimited historical data | Unlimited historical data | 
| Kubecost API retention \(ETL\) | 15 days | 15 days | Unlimited historical data | 
| Cluster cost visibility | Single clusters | Unified multi\-cluster | Unified multi\-cluster | 
| Hybrid cloud visibility | \- | Amazon EKS and Amazon EKS Anywhere clusters | Multi\-cloud and hybrid\-cloud support | 
| Alerts and recurring reports | \- | Efficiency alerts, budget alerts, spend change alerts, and more supported | Efficiency alerts, budget alerts, spend change alerts, and more supported | 
| Saved reports | \- | Reports using 15 days data | Reports using unlimited historical data | 
| Cloud billing integration | Required for each individual cluster | Custom pricing support for AWS \(including multiple clusters and multiple accounts\) | Custom pricing support for AWS \(including multiple clusters and multiple accounts\) | 
| Savings recommendations | Single cluster insights | Single cluster insights | Multi\-cluster insights | 
| Governance: Audits | \- | \- | Audit historical cost events | 
| Single sign\-on \(SSO\) support | \- | Amazon Cognito supported | Okta, Auth0, PingID, KeyCloak | 
| Role\-based access control \(RBAC\) with SAML 2\.0 | \- | \- | Okta, Auth0, PingID, Keycloak | 
| Enterprise training and onboarding | \- | \- | Full\-service training and FinOps onboarding | 

**What is the Kubecost API retention \(ETL\) feature?**  
The Kubecost ETL feature aggregates and organizes metrics to surface cost visibility at various levels of granularity \(such as `namespace-level`, `pod-level`, and `deployment-level`\)\. For the custom Kubecost bundle, customers get data and insights from metrics for the last 15 days\.

**What is the alerts and recurring reports feature? What alerts and reports does it include?**  
Kubecost alerts allow teams to receive updates on real\-time Kubernetes spend as well as cloud spend\. Recurring reports enable teams to receive customized views of historical Kubernetes and cloud spend\. Both are configurable using the Kubecost UI or Helm values\. They support email, Slack, and Microsoft Teams\.

**What do saved reports include?**  
Kubecost saved reports are predefined views of cost and efficiency metrics\. They include cost by cluster, namespace, label, and more\.

**What is cloud billing integration?**  
Integration with AWS billing APIs allows Kubecost to display out\-of\-cluster costs \(such as Amazon S3\)\. Additionally, it allows Kubecost to reconcile Kubecost's in\-cluster predictions with actual billing data to account for spot usage, savings plans, and enterprise discounts\.

**What do savings recommendations include?**  
Kubecost provides insights and automation to help users optimize their Kubernetes infrastructure and spend\.

#### Is there a charge for this functionality?<a name="cost-monitoring-faq-charge"></a>

No\. You can use this version of Kubecost at no additional charge\. If you want additional Kubecost capabilities that aren't included in this bundle, you can buy an enterprise license of Kubecost through the AWS Marketplace, or from Kubecost directly\.

#### Is support available?<a name="cost-monitoring-faq-support"></a>

Yes\. You can open a support case with the AWS Support team at [Contact AWS](https://aws.amazon.com/contact-us/)\.

#### Do I need a license to use Kubecost features provided by the Amazon EKS integration?<a name="cost-monitoring-faq-license"></a>

No\.

#### Can I integrate Kubecost with AWS Cost and Usage Report for more accurate reporting?<a name="cost-monitoring-faq-cur"></a>

Yes\. You can configure Kubecost to ingest data from AWS Cost and Usage Report to get accurate cost visibility, including discounts, Spot pricing, reserved instance pricing, and others\. For more information, see [AWS Cloud Billing Integration](https://docs.kubecost.com/install-and-configure/install/cloud-integration/aws-cloud-integrations) in the Kubecost documentation\.

#### Does this version support cost management of self\-managed Kubernetes clusters on Amazon EC2?<a name="cost-monitoring-faq-self-managed"></a>

No\. This version is only compatible with Amazon EKS clusters\.

#### Can Kubecost track costs for Amazon EKS on AWS Fargate?<a name="cost-monitoring-faq-fargate"></a>

Kubecost provides best effort to show cluster cost visibility for Amazon EKS on Fargate, but with lower accuracy than with Amazon EKS on Amazon EC2\. This is primarily due to the difference in how you're billed for your usage\. With Amazon EKS on Fargate, you're billed for consumed resources\. With Amazon EKS on Amazon EC2 nodes, you're billed for provisioned resources\. Kubecost calculates the cost of an Amazon EC2 node based on the node specification, which includes CPU, RAM, and ephemeral storage\. With Fargate, costs are calculated based on the requested resources for the Fargate Pods\.

#### How can I get updates and new versions of Kubecost?<a name="cost-monitoring-faq-updates"></a>

You can upgrade your Kubecost version using standard Helm upgrade procedures\. The latest versions are in the [Amazon ECR Public Gallery\.](https://gallery.ecr.aws/kubecost/cost-analyzer)

#### Is the `kubectl-cost` CLI supported? How do I install it?<a name="cost-monitoring-faq-cli"></a>

Yes\. `Kubectl-cost` is an open source tool by Kubecost \(Apache 2\.0 License\) that provides CLI access to Kubernetes cost allocation metrics\. To install `kubectl-cost`, see [Installation](https://github.com/kubecost/kubectl-cost#installation) on GitHub\.

#### Is the Kubecost user interface supported? How do I access it?<a name="cost-monitoring-faq-ui"></a>

Kubecost provides a web dashboard that you can access through `kubectl` port forwarding, an ingress, or a load balancer\. You can also use the AWS Load Balancer Controller to expose Kubecost and use Amazon Cognito for authentication, authorization, and user management\. For more information, see [How to use Application Load Balancer and Amazon Cognito to authenticate users for your Kubernetes web apps](https://aws.amazon.com/blogs/containers/how-to-use-application-load-balancer-and-amazon-cognito-to-authenticate-users-for-your-kubernetes-web-apps/) on the AWS blog\.

#### Is Amazon EKS Anywhere supported?<a name="cost-monitoring-faq-eks-a"></a>

No\.