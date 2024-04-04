# Amazon EKS Kubernetes versions<a name="kubernetes-versions"></a>

Kubernetes rapidly evolves with new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions \(such as `1.29`\) on average once every four months\. Amazon EKS follows the upstream release and deprecation cycle for minor versions\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\.

A minor version is under standard support in Amazon EKS for the first 14 months after it's released\. Once a version is past the end of standard support date, it automatically enters extended support for the next 12 months\. Extended support allows you to stay at a specific Kubernetes version for longer at an additional cost per cluster hour\. If you haven’t updated your cluster before the extended support period ends, your cluster is auto\-upgraded to the oldest currently supported extended version\.

We recommend that you create your cluster with the latest available Kubernetes version supported by Amazon EKS\. If your application requires a specific version of Kubernetes, you can select older versions\. You can create new Amazon EKS clusters on any version offered in standard or extended support\.

[![AWS Videos](http://img.youtube.com/vi/https://www.youtube.com/embed/_dJdAZ_J_jw/0.jpg)](http://www.youtube.com/watch?v=https://www.youtube.com/embed/_dJdAZ_J_jw)

## Available versions on standard support<a name="available-versions"></a>

The following Kubernetes versions are currently available in Amazon EKS standard support:
+ `1.29`
+ `1.28`
+ `1.27`
+ `1.26`
+ `1.25`

For important changes to be aware of for each version in standard support, see [Release notes for standard support versions](kubernetes-versions-standard.md)\.

## Available versions on extended support<a name="available-versions-extended"></a>

The following Kubernetes versions are currently available in Amazon EKS extended support:
+ `1.24`
+ `1.23`

For important changes to be aware of for each version in extended support, see [Release notes for extended support versions](kubernetes-versions-extended.md)\.

The following Kubernetes versions are currently available in Amazon EKS extended support, with the additional requirement that **you cannot create new clusters with these versions**: 
+ `1.22`
+ `1.21`

  For information on these versions, see [Release notes for versions 1\.21 and 1\.22](kubernetes-versions-1-21-1-22.md)

## Amazon EKS Kubernetes release calendar<a name="kubernetes-release-calendar"></a>

The following table shows important release and support dates to consider for each Kubernetes version\.

**Note**  
Dates with only a month and a year are approximate and are updated with an exact date when it's known\.


| Kubernetes version | Upstream release | Amazon EKS release | End of standard support | End of extended support | 
| --- | --- | --- | --- | --- | 
| 1\.29 | December 13, 2023 | January 23, 2024 | March 23, 2025  | March 23, 2026 | 
| 1\.28 | August 15, 2023 | September 26, 2023 | November 26, 2024  | November 26, 2025 | 
| 1\.27 | April 11, 2023 | May 24, 2023 | July 24, 2024 | July 24, 2025 | 
| 1\.26 | December 9, 2022 | April 11, 2023 | June 11, 2024 | June 11, 2025 | 
| 1\.25 | August 23, 2022 | February 22, 2023 | May 1, 2024 | May 1, 2025 | 
| 1\.24 | May 3, 2022 | November 15, 2022 | January 31, 2024 | January 31, 2025 | 
| 1\.23 | December 7, 2021 | August 11, 2022 | October 11, 2023 | October 11, 2024 | 
| 1\.22 | August 4, 2021 | April 4, 2022 | June 4, 2023 | September 1, 2024 | 
| 1\.21 | April 8, 2021 | July 19, 2021 | February 16, 2023 | July 15, 2024 | <a name="version-deprecation"></a>

## Amazon EKS version FAQs<a name="version-faqs"></a>

**How many Kubernetes versions are available in standard support?**  
In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to offering standard support for at least four production\-ready versions of Kubernetes at any given time\. We will announce the end of standard support date of a given Kubernetes minor version at least 60 days in advance\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the end of standard support date of a Kubernetes version on Amazon EKS will be on or after the date that the Kubernetes project stops supporting the version upstream\.

**How long does a Kubernetes receive standard support by Amazon EKS?**  
A Kubernetes version received standard support for 14 months after first being available on Amazon EKS\. This is true even if upstream Kubernetes no longer support a version that's available on Amazon EKS\. We backport security patches that are applicable to the Kubernetes versions that are supported on Amazon EKS\.

**Am I notified when standard support is ending for a Kubernetes version on Amazon EKS?**  
Yes\. If any clusters in your account are running the version nearing the end of support, Amazon EKS sends out a notice through the AWS Health Dashboard approximately 12 months after the Kubernetes version was released on Amazon EKS\. The notice includes the end of support date\. This is at least 60 days from the date of the notice\.

**Which Kubernetes features are supported by Amazon EKS?**  
Amazon EKS supports all generally available \(GA\) features of the Kubernetes API\. Starting with Kubernetes version `1.24`, new beta APIs aren't enabled in clusters by default\. However, previously existing beta APIs and new versions of existing beta APIs continue to be enabled by default\. Alpha features aren't supported\.

**Are Amazon EKS managed node groups automatically updated along with the cluster control plane version?**  
No\. A managed node group creates Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update your control plane\. For more information, see [Updating a managed node group](update-managed-node-group.md)\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Are self\-managed node groups automatically updated along with the cluster control plane version?**  
No\. A self\-managed node group includes Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update the control plane version on your behalf\. A self\-managed node group doesn't have any indication in the console that it needs updating\. You can view the `kubelet` version installed on a node by selecting the node in the **Nodes** list on the **Overview** tab of your cluster to determine which nodes need updating\. You must manually update the nodes\. For more information, see [Self\-managed node updates](update-workers.md)\.  
The Kubernetes project tests compatibility between the control plane and nodes for up to three minor versions\. For example, `1.26` nodes continue to operate when orchestrated by a `1.29` control plane\. However, running a cluster with nodes that are persistently three minor versions behind the control plane isn't recommended\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Are Pods running on Fargate automatically upgraded with an automatic cluster control plane version upgrade?**  
No\. We strongly recommend running Fargate Pods as part of a replication controller, such as a Kubernetes deployment\. Then do a rolling restart of all Fargate Pods\. The new version of the Fargate Pod is deployed with a `kubelet` version that's the same version as your updated cluster control plane version\. For more information, see [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment) in the Kubernetes documentation\.  
If you update the control plane, you must still update the Fargate nodes yourself\. To update Fargate nodes, delete the Fargate Pod represented by the node and redeploy the Pod\. The new Pod is deployed with a `kubelet` version that's the same version as your cluster\.

## Amazon extended support FAQs<a name="extended-support-faqs"></a>

**The standard support and extended support terminology is new to me\. What do those terms mean?**  
Standard support for a Kubernetes version in Amazon EKS begins when a Kubernetes version is released on Amazon EKS, and will end 14 months after the release date\. Extended support for a Kubernetes version will begin immediately after the end of standard support, and will end after the next 12 months\. For example, standard support for version `1.23` in Amazon EKS ends on October 11, 2023\. Extended support for version `1.23` began on October 12, 2023 and will end on October 11, 2024\.

**What do I need to do to get extended support for Amazon EKS clusters?**  
You don’t have to take any action to get extended support for your Amazon EKS clusters\. Standard support will begin when a Kubernetes version is released on Amazon EKS, and will end 14 months after the release date\. Extended support for a Kubernetes version will begin immediately after the end of standard support, and will end after the next 12 months\. Clusters that are running on a Kubernetes version past the end of standard support will automatically be onboarded to extended support\.

**For which Kubernetes versions can I get extended support?**  
Extended support is available for Kubernetes versions `1.23` and higher\. You can run clusters on any version for up to 12 months after the end of standard support for that version\. This means that each version will be supported for 26 months in Amazon EKS \(14 months of standard support plus 12 months of extended support\)\.

**What if I don’t want to use extended support?**  
If you don’t want to be automatically enrolled in extended support, you can upgrade your cluster to a Kubernetes version that’s in standard Amazon EKS support\. Clusters that aren’t upgraded to a Kubernetes version in standard support will automatically enter extended support\.

**What will happen at the end of 12 months of extended support?**  
Clusters running on a Kubernetes version that has completed its 26\-month lifecycle \(14 months of standard support plus 12 months of extended support\) will be auto\-upgraded to the next version\.  
On the end of extended support date, you can no longer create new Amazon EKS clusters with the unsupported version\. Existing control planes are automatically updated by Amazon EKS to the earliest supported version through a gradual deployment process after the end of support date\. After the automatic control plane update, make sure to manually update cluster add\-ons and Amazon EC2 nodes\. For more information, see [Update the Kubernetes version for your Amazon EKS cluster](update-cluster.md#update-existing-cluster)\.

**When exactly is my control plane automatically updated after the end of extended support date?**  
Amazon EKS can't provide specific time frames\. Automatic updates can happen at any time after the end of extended support date\. You won't receive any notification before the update\. We recommend that you proactively update your control plane without relying on the Amazon EKS automatic update process\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

**Can I leave my control plane on a Kubernetes version indefinitely?**  
No\. Cloud security at AWS is the highest priority\. Past a certain point \(usually one year\), the Kubernetes community stops releasing common vulnerabilities and exposures \(CVE\) patches and discourages CVE submission for unsupported versions\. This means that vulnerabilities specific to an older version of Kubernetes might not even be reported\. This leaves clusters exposed with no notice and no remediation options in the event of a vulnerability\. Given this, Amazon EKS doesn't allow control planes to stay on a version that reached end of extended support\.

**Is there additional cost to get extended support?**  
Yes, there is additional cost for Amazon EKS clusters running in extended support\. For pricing details, see [Amazon EKS extended support for Kubernetes version pricing](https://aws.amazon.com/blogs/containers/amazon-eks-extended-support-for-kubernetes-versions-pricing/) on the AWS blog\.

**What is included in extended support?**  
Amazon EKS clusters in Extended Support receive ongoing security patches for the Kubernetes control plane\. Additionally, Amazon EKS will release patches for the Amazon VPC CNI, `kube-proxy`, and CoreDNS add\-ons for Extended Support versions\. Amazon EKS will also release patches for AWS\-published Amazon EKS optimized AMIs for Amazon Linux, Bottlerocket, and Windows, as well as Amazon EKS Fargate nodes for those versions\. All clusters in Extended Support will continue to get access to technical support from AWS\.  
Extended Support for Amazon EKS optimized Windows AMIs that are published by AWS isn't available for Kubernetes version `1.23` but is available for Kubernetes version `1.24` and higher\.

**Are there any limitations to patches for non\-Kubernetes components in extended support?**  
While Extended Support covers all of the Kubernetes specific components from AWS, it will only provide support for AWS\-published Amazon EKS optimized AMIs for Amazon Linux, Bottlerocket, and Windows at all times\. This means, you will potentially have newer components \(such as OS or kernel\) on your Amazon EKS optimized AMI while using Extended Support\. For example, once Amazon Linux 2 reaches the [end of its lifecycle in 2025](https://aws.amazon.com/amazon-linux-2/faqs/), the Amazon EKS optimized Amazon Linux AMIs will be built using a newer Amazon Linux OS\. Amazon EKS will announce and document important support lifecycle discrepancies such as this for each Kubernetes version\.

**Can I create new clusters using a version on extended support?**  
Yes, with the exclusion of `1.22` and `1.21`\. For example, you can create a `1.23` cluster, but not a `1.22` cluster\.