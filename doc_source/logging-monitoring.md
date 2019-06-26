# Logging and Monitoring in Amazon EKS<a name="logging-monitoring"></a>

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account\. These logs make it easy for you to secure and run your clusters\. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch\.

The following cluster control plane log types are available\. Each log type corresponds to a component of the Kubernetes control plane\. To learn more about these components, see [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/) in the Kubernetes documentation\.
+ **Kubernetes API server component logs \(`api`\)** – Your cluster's API server is the control plane component that exposes the Kubernetes API\. For more information, see [kube\-apiserver](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) in the Kubernetes documentation\.
+ **Audit \(`audit`\)** – Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster\. For more information, see [Auditing](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/) in the Kubernetes documentation\.
+ **Authenticator \(`authenticator`\)** – Authenticator logs are unique to Amazon EKS\. These logs represent the control plane component that Amazon EKS uses for Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) authentication using IAM credentials\. For more information, see [Managing Cluster Authentication](managing-auth.md)\.
+ **Controller manager \(`controllerManager`\)** – The controller manager manages the core control loops that are shipped with Kubernetes\. For more information, see [kube\-controller\-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) in the Kubernetes documentation\.
+ **Scheduler \(`scheduler`\)** – The scheduler component manages when and where to run pods in your cluster\. For more information, see [kube\-scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/) in the Kubernetes documentation\.

For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)\.

Amazon EKS is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service in Amazon EKS\. CloudTrail captures all API calls for Amazon EKS as events\. The calls captured include calls from the Amazon EKS console and code calls to the Amazon EKS API operations\. 

For more information, see [Logging Amazon EKS API Calls with AWS CloudTrail](logging-using-cloudtrail.md)\.