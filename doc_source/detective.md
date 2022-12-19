# Amazon Detective

Amazon EKS is integrated with Amazon Detective, a service that automatically aggregates, distills, and organizes security data. You can review EKS Clusters in Detective to analyze cluster details, containers, and API activity. 

Amazon Detective is enabled for individual regions. Ensure Detective is enabled for each region you have an EKS cluster. Detective must be enabled for 24-48 hours before cluster data becomes available in the Detective Console. 

Detective organizes Kubernetes and AWS data into findings, including:

- EKS Cluster Details, including the IAM identity that created the cluster and the Service Role of the cluster. The AWS API and Kubernetes API activity of these IAM identities may be further investigated with Detective.
- Container details, such as the Image and Security context. Terminated pods may also be reviewed. 
- Kubernetes API Activity, including both overall trends in API activity and details on specific API calls. The section on newly observed API calls may be helpful to identify suspicious activity. 

## Review Findings for an EKS Cluster

**Prerequisite**

To review findings for an EKS cluster, Detective must have been [enabled](https://docs.aws.amazon.com/detective/latest/adminguide/detective-setup.html) in the region of the cluster for at least 48 hours. 

1. Open the Amazon Detective Console at https://console.aws.amazon.com/detective/.
2. From the navigation bar, select Search.
3. Change the Search Type to **EKS Cluster**. 
4. Enter the EKS Cluster Name or ARN. 


## Learn more about Amazon Detective

To learn more about Amazon Detective, see the following resources:
+ [Amazon Detective](http://aws.amazon.com/detective/)
+ [Amazon Detective User Guide](https://docs.aws.amazon.com/detective/index.html)

