# Install Kubecost and access dashboard<a name="cost-monitoring-kubecost"></a>

Amazon EKS supports Kubecost, which you can use to monitor your costs broken down by Kubernetes resources including Pods, nodes, namespaces, and labels\. This topic covers installing Kubecost, and accessing the Kubecost dashboard\. 

Amazon EKS provides an AWS optimized bundle of Kubecost for cluster cost visibility\. You can use your existing AWS support agreements to obtain support\. For more information about the available versions of Kubecost, see [Learn more about Kubecost](cost-monitoring-kubecost-bundles.md)\.

As a Kubernetes platform administrator and finance leader, you can use Kubecost to visualize a breakdown of Amazon EKS charges, allocate costs, and charge back organizational units such as application teams\. You can provide your internal teams and business units with transparent and accurate cost data based on their actual AWS bill\. Moreover, you can also get customized recommendations for cost optimization based on their infrastructure environment and usage patterns within their clusters\. 

**Note**  
Kubecost v2 introduces several major new features\. [Learn more about Kubecost v2\. ](cost-monitoring-kubecost-bundles.md#kubecost-v2)

For more information about Kubecost, see the [https://guide.kubecost.com](https://guide.kubecost.com) documentation\.

## Install Kubecost using Helm<a name="kubecost-helm"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Get started with Amazon EKS](getting-started.md)\. The cluster must have Amazon EC2 nodes because you can't run Kubecost on Fargate nodes\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.29`, you can use `kubectl` version `1.28`, `1.29`, or `1.30` with it\. To install or upgrade `kubectl`, see [Set up `kubectl` and `eksctl`](install-kubectl.md)\.
+ Helm version 3\.9\.0 or later configured on your device or AWS CloudShell\. To install or update Helm, see [Deploy applications with Helm on Amazon EKS](helm.md)\.
+ If your cluster is version `1.23` or later, you must have the [Store Kubernetes volumes with Amazon EBS](ebs-csi.md) installed on your cluster\.

1. Determine the version of Kubecost to install\. You can see the available versions at [kubecost/cost\-analyzer](https://gallery.ecr.aws/kubecost/cost-analyzer) in the Amazon ECR Public Gallery\. For more information about the compatibility of Kubecost versions and Amazon EKS, see the [Environment Requirements](https://docs.kubecost.com/install-and-configure/install/environment) in the Kubecost documentation\. 

1. Install Kubecost with the following command\. Replace *kubecost\-version* with the value retrieved from ECR, such as *1\.108\.1*\.

   ```
   helm upgrade -i kubecost oci://public.ecr.aws/kubecost/cost-analyzer --version kubecost-version \
       --namespace kubecost --create-namespace \
       -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/develop/cost-analyzer/values-eks-cost-monitoring.yaml
   ```

   Kubecost releases new versions regularly\. You can update your version using [https://helm.sh/docs/helm/helm_upgrade/](https://helm.sh/docs/helm/helm_upgrade/)\. By default, the installation includes a local [https://prometheus.io/](https://prometheus.io/) server and `kube-state-metrics`\. You can customize your deployment to use [Amazon Managed Service for Prometheus](https://aws.amazon.com/blogs/mt/integrating-kubecost-with-amazon-managed-service-for-prometheus/) by following the documentation in [Integrating with Amazon EKS cost monitoring](https://docs.aws.amazon.com/prometheus/latest/userguide/integrating-kubecost.html)\. For a list of all other settings that you can configure, see the [sample configuration file](https://github.com/kubecost/cost-analyzer-helm-chart/blob/develop/cost-analyzer/values-eks-cost-monitoring.yaml) on GitHub\.

   You can remove Kubecost from your cluster with the following commands\.

   ```
   helm uninstall kubecost --namespace kubecost
   kubectl delete ns kubecost
   ```

## Install Kubecost using Amazon EKS Add\-ons<a name="kubecost-addon"></a>

Amazon EKS Add\-ons reduce the complexity of upgrading Kubecost, and managing licenses\. EKS Add\-ons are integrated with the AWS marketplace\. 

1. View[ Kubecost in the AWS Marketplace console](https://aws.amazon.com/marketplace/seller-profile?id=983de668-2731-4c99-a7e2-74f27d796173) and subscribe\. 

1. Determine the name of your cluster, and the region\. Verify you are logged into the AWS CLI with sufficient permissions to manage EKS\. 

1. Create the Kubecost addon\.

   ```
   aws eks create-addon --addon-name kubecost_kubecost --cluster-name $YOUR_CLUSTER_NAME --region $AWS_REGION
   ```

Learn how to [remove an EKS Add\-on](removing-an-add-on.md), such as Kubecost\.

## Access Kubecost Dashboard<a name="kubecost-dashboard"></a>

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
![\[\]](http://docs.aws.amazon.com/eks/latest/userguide/images/kubecost.png)

1. To track costs at a cluster level, tag your Amazon EKS resources for billing\. For more information, see [Tagging your resources for billing](eks-using-tags.md#tag-resources-for-billing)\.

**You can also view the following information by selecting it in the left pane of the dashboard:**
+ **Cost allocation** – View monthly Amazon EKS costs and cumulative costs for each of your namespaces and other dimensions over the past seven days\. This is helpful for understanding which parts of your application are contributing to Amazon EKS spend\.
+ **Assets** – View the costs of the AWS infrastructure assets that are associated with your Amazon EKS resources\.