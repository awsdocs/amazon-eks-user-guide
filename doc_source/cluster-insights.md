# Cluster insights<a name="cluster-insights"></a>

Amazon EKS cluster insights provide recommendations to help you follow Amazon EKS and Kubernetes best practices\. Every Amazon EKS cluster undergoes automatic, recurring checks against an Amazon EKS curated list of insights\. These insight checks are fully managed by Amazon EKS and offer recommendations on how to address any findings\. 

**Recommended usage of cluster insights:**
+ Before updating your cluster Kubernetes version, check cluster insights in the [EKS console\.](https://console.aws.amazon.com/eks/home#/clusters)
+ If your cluster has identified issues, review them and make appropriate fixes\. The issues include links to Amazon EKS and Kubernetes\.
+ After fixing issues, wait for the cluster insights to refresh\. If all issues have been resolved, [update your cluster\.](update-cluster.md)

Currently, Amazon EKS only returns insights related to Kubernetes version upgrade readiness\.

Upgrade insights identify possible issues that could impact Kubernetes cluster upgrades\. This minimizes the effort that administrators spend preparing for upgrades and increases the reliability of applications on newer Kubernetes versions\. Clusters are automatically scanned by Amazon EKS against a list of possible Kubernetes version upgrade impacting issues\. Amazon EKS frequently updates the list of insight checks based on reviews of changes made in each Kubernetes version release\.

Amazon EKS upgrade insights speed up the testing and verification process for new versions\. They also allow cluster administrators and application developers to leverage the newest Kubernetes capabilities by highlighting concerns and offering remediation advice\. To see the list of insight checks performed and any relevant issues that Amazon EKS has identified, you can call the Amazon EKS `ListInsights` API operation or look in the Amazon EKS console\.

Cluster insights update periodically\. You cannot manually refresh cluster insights\. If you fix a cluster issue, it will take some time for cluster insights to update\. To determine if a fix was successful, compare the time the change deployed to the "last refresh time" of the cluster insight\. 

## View cluster insights \(Console\)<a name="cluster-insights-console"></a>

**To view the insights of an Amazon EKS cluster:**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. From the cluster list, choose the name of the Amazon EKS cluster for which you want to see the insights\.

1. Choose the **Upgrade Insights** tab\.

1. On the **Upgrade Insights** page you will see the following fields:
   + **Name** – The check that was performed by Amazon EKS against the cluster\.
   + **Insight status** – An insight with a status of "Error" typically means the impacted Kubernetes version is N\+1 of the current cluster version, while a status of "Warning" means the insight applies to a future Kubernetes version N\+2 or more\. An insight with status of "Passing" means Amazon EKS has not found any issues associated with this insight check in your cluster\. An insight status of "Unknown" means Amazon EKS is unable to determine if your cluster is impacted by this insight check\.
   + **Version** – The Kubernetes version that the insight checked for possible issues\.
   + **Last refresh time \(UTC\-5:00\)** – The time the status of the insight was last refreshed for this cluster\.
   + **Last transition time \(UTC\-5:00\)** – The time the status of this insight last changed\.
   + **Description** – Information from the insight check, which includes the alert and recommended actions for remediation\.

## View cluster insights \(AWS CLI\)<a name="cluster-insights-cli"></a>

**To view the insights of an Amazon EKS cluster:**

1. Determine which cluster you would like to check for insights\. The following command lists the insights for a specified cluster\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `region-code` with the code for your AWS Region\.
   + Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks list-insights --region region-code --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "insights": [
           {
               "category": "UPGRADE_READINESS", 
               "name": "Deprecated APIs removed in Kubernetes v1.29", 
               "insightStatus": {
                   "status": "PASSING", 
                   "reason": "No deprecated API usage detected within the last 30 days."
               }, 
               "kubernetesVersion": "1.29", 
               "lastTransitionTime": 1698774710.0, 
               "lastRefreshTime": 1700157422.0, 
               "id": "123e4567-e89b-42d3-a456-579642341238", 
               "description": "Checks for usage of deprecated APIs that are scheduled for removal in Kubernetes v1.29. Upgrading your cluster before migrating to the updated APIs supported by v1.29 could cause application impact."
           }
       ]
   }
   ```

1. For descriptive information about the insight, run the following command\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `region-code` with the code for your AWS Region\.
   + Replace `123e4567-e89b-42d3-a456-579642341238` with the insight ID retrieved from listing the cluster insights\.
   + Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-insight --region region-code --id 123e4567-e89b-42d3-a456-579642341238 --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "insight": {
           "category": "UPGRADE_READINESS", 
           "additionalInfo": {
               "EKS update cluster documentation": "https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html", 
               "Kubernetes v1.29 deprecation guide": "https://kubernetes.io/docs/reference/using-api/deprecation-guide/#v1-29"
           }, 
           "name": "Deprecated APIs removed in Kubernetes v1.29", 
           "insightStatus": {
               "status": "PASSING", 
               "reason": "No deprecated API usage detected within the last 30 days."
           }, 
           "kubernetesVersion": "1.29", 
           "recommendation": "Update manifests and API clients to use newer Kubernetes APIs if applicable before upgrading to Kubernetes v1.29.", 
           "lastTransitionTime": 1698774710.0, 
           "lastRefreshTime": 1700157422.0, 
           "categorySpecificSummary": {
               "deprecationDetails": [
                   {
                       "usage": "/apis/flowcontrol.apiserver.k8s.io/v1beta2/flowschemas", 
                       "replacedWith": "/apis/flowcontrol.apiserver.k8s.io/v1beta3/flowschemas", 
                       "stopServingVersion": "1.29", 
                       "clientStats": [], 
                       "startServingReplacementVersion": "1.26"
                   }, 
                   {
                       "usage": "/apis/flowcontrol.apiserver.k8s.io/v1beta2/prioritylevelconfigurations", 
                       "replacedWith": "/apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations", 
                       "stopServingVersion": "1.29", 
                       "clientStats": [], 
                       "startServingReplacementVersion": "1.26"
                   }
               ]
           }, 
           "id": "f6a11fe4-77f7-48c6-8326-9a13f022ecb3", 
           "resources": [], 
           "description": "Checks for usage of deprecated APIs that are scheduled for removal in Kubernetes v1.29. Upgrading your cluster before migrating to the updated APIs supported by v1.29 could cause application impact."
       }
   }
   ```