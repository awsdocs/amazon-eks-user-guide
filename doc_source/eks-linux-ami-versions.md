# Amazon EKS optimized Amazon Linux AMI versions<a name="eks-linux-ami-versions"></a>

Amazon EKS optimized Amazon Linux AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version.k8s_patch_version-release_date
```

In the past, this page included details about each AMI version release\. The details included the versions of `kubelet`, Docker, the Linux kernel, `containerd`, and the NVIDIA driver available in each new AMI version\. You can now find this information in the [Changelog](https://github.com/awslabs/amazon-eks-ami/blob/master/CHANGELOG.md) on GitHub\.