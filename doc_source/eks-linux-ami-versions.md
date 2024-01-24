# Amazon EKS optimized Amazon Linux AMI versions<a name="eks-linux-ami-versions"></a>

Amazon EKS optimized Amazon Linux AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version.k8s_patch_version-release_date
```

Each AMI release includes various versions of `kubelet`, Docker, the Linux kernel, and `containerd`\. The accelerated AMI also includes various versions of the NVIDIA driver\. You can find this version information in the [Changelog](https://github.com/awslabs/amazon-eks-ami/blob/master/CHANGELOG.md) on GitHub\.

------
#### [ Kubernetes version 1\.29 ]


**Kubernetes version `1.29`**  

| AMI version | `kubelet` version | Kernel version | `containerd` version | NVIDIA driver version | 
| --- | --- | --- | --- | --- | 
| 1\.29\.0\-20240117 | 1\.29\.0 | 5\.10\.205\-195\.804\.amzn2 | 1\.7\.2\-1\.amzn2\.0\.1 | N/A | 

------