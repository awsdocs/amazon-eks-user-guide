# Retrieve Amazon Linux AMI version information<a name="eks-linux-ami-versions"></a>

Amazon EKS optimized Amazon Linux AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version.k8s_patch_version-release_date
```

Each AMI release includes various versions of [https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/), the Linux kernel, and [https://containerd.io/](https://containerd.io/)\. The accelerated AMI also includes various versions of the NVIDIA driver\. You can find this version information in the [Changelog](https://github.com/awslabs/amazon-eks-ami/blob/main/CHANGELOG.md) on GitHub\.