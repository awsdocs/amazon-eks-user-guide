# Pod security policy \(PSP\) removal FAQ<a name="pod-security-policy-removal-faq"></a>

`PodSecurityPolicy` was [deprecated in Kubernetes`1.21`](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/), and has been removed in Kubernetes`1.25`\. If you are using PodSecurityPolicy in your cluster, **then you must migrate to the built\-in Kubernetes Pod Security Standards \(PSS\) or to a policy\-as\-code solution before upgrading your cluster to version `1.25` to avoid interruptions to your workloads\.** Select any frequently asked question to learn more\.

## What is a PSP?<a name="pod-security-policy-removal-what-is"></a>

[PodSecurityPolicy](https://kubernetes.io/docs/concepts/security/pod-security-policy/) is a built\-in admission controller that allows a cluster administrator to control security\-sensitive aspects of Pod specification\. If a Pod meets the requirements of its PSP, the Pod is admitted to the cluster as usual\. If a Pod doesn't meet the PSP requirements, the Pod is rejected and can't run\.

## Is the PSP removal specific to Amazon EKS or is it being removed in upstream Kubernetes?<a name="pod-security-policy-removal-specific"></a>

This is an upstream change in the Kubernetes project, and not a change made in Amazon EKS\. PSP was deprecated in Kubernetes `1.21` and removed in Kubernetes `1.25`\. The Kubernetes community identified serious usability problems with PSP\. These included accidentally granting broader permissions than intended and difficulty in inspecting which PSPs apply in a given situation\. These issues couldn't be addressed without making breaking changes\. This is the primary reason why the Kubernetes community [decided to remove PSP](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/#why-is-podsecuritypolicy-going-away)\. 

## How can I check if I'm using PSPs in my Amazon EKS clusters?<a name="pod-security-policy-removal-check"></a>

To check if you're using PSPs in your cluster, you can run the following command:

```
kubectl get psp
```

To see the Pods that the PSPs in your cluster are impacting, run the following command\. This command outputs the Pod name, namespace, and PSPs:

```
kubectl get pod -A -o jsonpath='{range.items[?(@.metadata.annotations.kubernetes\.io/psp)]}{.metadata.name}{"\t"}{.metadata.namespace}{"\t"}{.metadata.annotations.kubernetes\.io/psp}{"\n"}'
```

## If I'm using PSPs in my Amazon EKS cluster, what can I do?<a name="pod-security-policy-removal-what-can"></a>

Before upgrading your cluster to `1.25`, you must migrate your PSPs to either one of these alternatives:
+  Kubernetes PSS\.
+  Policy\-as\-code solutions from the Kubernetes environment\.

In response to the PSP deprecation and the ongoing need to control Pod security from the start, the Kubernetes community created a built\-in solution with [\(PSS\)](https://kubernetes.io/docs/concepts/security/pod-security-standards/) and [Pod Security Admission \(PSA\)](https://kubernetes.io/docs/concepts/security/pod-security-admission/)\. The PSA webhook implements the controls that are defined in the PSS\.

 You can review best practices for migrating PSPs to the built\-in PSS in the [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/security/docs/pods/#pod-security-standards-pss-and-pod-security-admission-psa)\. We also recommend reviewing our blog on [Implementing Pod Security Standards in Amazon EKS](https://aws.amazon.com/blogs/containers/implementing-pod-security-standards-in-amazon-eks/)\. Additional references include [Migrate from PodSecurityPolicy to the Built\-In PodSecurity Admission Controller](https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/) and [Mapping PodSecurityPolicies to Pod Security Standards](https://kubernetes.io/docs/reference/access-authn-authz/psp-to-pod-security-standards/)\.

Policy\-as\-code solutions provide guardrails to guide cluster users and prevents unwanted behaviors through prescribed automated controls\. Policy\-as\-code solutions typically use [Kubernetes Dynamic Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) to intercept the Kubernetes API server request flow using a webhook call\. Policy\-as\-code solutions mutate and validate request payloads based on policies written and stored as code\. 

There are several open source policy\-as\-code solutions available for Kubernetes\. To review best practices for migrating PSPs to a policy\-as\-code solution, see the [Policy\-as\-code ](https://aws.github.io/aws-eks-best-practices/security/docs/pods/#policy-as-code-pac) section of the Pod Security page on GitHub\.

## I see a PSP called `eks.privileged` in my cluster\. What is it and what can I do about it?<a name="pod-security-policy-removal-privileged"></a>

Amazon EKS clusters with Kubernetes version `1.13` or higher have a default PSP that's named `eks.privileged`\. This policy is created in `1.24` and earlier clusters\. It isn't used in `1.25` and later clusters\. Amazon EKS automatically migrates this PSP to a PSS\-based enforcement\. No action is needed on your part\. 

## Will Amazon EKS make any changes to PSPs present in my existing cluster when I update my cluster to version `1.25`?<a name="pod-security-policy-removal-prevent"></a>

No\. Besides `eks.privileged`, which is a PSP created by Amazon EKS, no changes are made to other PSPs in your cluster when you upgrade to `1.25`\.

## Will Amazon EKS prevent a cluster update to version `1.25` if I haven't migrated off of PSP?<a name="pod-security-policy-removal-migrate"></a>

No\. Amazon EKS won't prevent a cluster update to version `1.25` if you didn't migrate off of PSP yet\.

## What if I forget to migrate my PSPs to PSS/PSA or to a policy\-as\-code solution before I update my cluster to version `1.25`? Can I migrate after updating my cluster?<a name="pod-security-policy-removal-forget"></a>

When a cluster that contains a PSP is upgraded to Kubernetes version `1.25`, the API server doesn't recognize the PSP resource in `1.25`\. This might result in Pods getting incorrect security scopes\. For an exhaustive list of implications, see [Migrate from PodSecurityPolicy to the Built\-In PodSecurity Admission Controller](https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/)\.

## How does this change impact pod security for Windows workloads?<a name="pod-security-policy-removal-impact"></a>

We don't expect any specific impact to Windows workloads\. PodSecurityContext has a field called `windowsOptions` in the `PodSpec v1` API for Windows Pods\. This uses PSS in Kubernetes `1.25`\. For more information and best practices about enforcing PSS for Windows workloads, see the [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/windows/docs/security/#pod-security-contexts) and Kubernetes [documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-runasusername/)\.