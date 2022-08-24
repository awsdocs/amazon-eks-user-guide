# Cost monitoring<a name="cost-monitoring"></a>

Amazon EKS supports Kubecost, which you can use to monitor your costs broken down by Kubernetes resources including pods, nodes, namespaces, and labels\. As a Kubernetes platform administrator and finance leader, you can use Kubecost to visualize a breakdown of Amazon EKS charges, allocate costs, and charge back organizational units such as application teams\. You can provide your internal teams and business units with transparent and accurate cost data based on their actual AWS bill\. Moreover, you can also get customized recommendations for cost optimization based on their infrastructure environment and usage patterns within their clusters\. For more information about Kubecost, see the [https://guide.kubecost.com](https://guide.kubecost.com) documentation\.

Amazon EKS provides an AWS optimized bundle of Kubecost for cluster cost visibility\. You can use your existing AWS support agreements to obtain support\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.22`, you can use `kubectl` version `1.21`,`1.22`, or `1.23` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Helm version 3\.9\.0 or later configured on your device or AWS CloudShell\. To install or update Helm, see [Using Helm with Amazon EKS](helm.md)\.
+ If your cluster is version `1.23` or later, you must have the [Amazon EBS CSI driver](ebs-csi.md) installed on your cluster\.

**Note**  
You can't run Kubecost on Fargate nodes\.

**To install Kubecost**

1. Install Kubecost with the following command\. You can replace *1\.96\.0* with a later version\. You can see the available versions at [kubecost/cost\-analyzer](https://gallery.ecr.aws/kubecost/cost-analyzer) in the Amazon ECR Public Gallery\.

   ```
   helm upgrade -i kubecost oci://public.ecr.aws/kubecost/cost-analyzer --version 1.96.0 \
       --namespace kubecost --create-namespace \
       -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/develop/cost-analyzer/values-eks-cost-monitoring.yaml
   ```

   Kubecost releases new versions regularly\. You can update your version using [helm upgrade](https://helm.sh/docs/helm/helm_upgrade/)\. The installation includes a local Prometheus server and `kube-state-metrics`\. If your environment already meets some of the prerequisites, you can customize your deployment\. For more information, see the [sample configuration file](https://github.com/kubecost/cost-analyzer-helm-chart/blob/develop/cost-analyzer/values-eks-cost-monitoring.yaml) on GitHub\.

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