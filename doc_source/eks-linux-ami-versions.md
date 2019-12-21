# Amazon EKS\-Optimized Linux AMI Versions<a name="eks-linux-ami-versions"></a>

This topic lists versions of the Amazon EKS\-optimized Linux AMIs and their corresponding versions of `kubelet`, Docker, the Linux kernel, and the[ Packer build script](eks-optimized-ami.md#eks-ami-build-scripts) configuration\.

The Amazon EKS\-optimized AMI metadata, including the AMI ID, for each variant can be retrieved programmatically\. For more information, see [Retrieving Amazon EKS\-Optimized AMI IDs](retrieve-ami-id.md)\.

AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version.k8s_patch_version-release_date
```

## Amazon EKS\-optimized AMI<a name="eks-al2-ami-versions"></a>

The table below lists the current and previous versions of the Amazon EKS\-optimized AMI\.

------
#### [ Kubernetes version 1\.14 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | 
| --- | --- | --- | --- | --- | 
|  1\.14\.7\-20190927  |  1\.14\.7  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  | 

------
#### [ Kubernetes version 1\.13 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | 
| --- | --- | --- | --- | --- | 
|  1\.13\.11\-20190927  |  1\.13\.11  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  | 

------
#### [ Kubernetes version 1\.12 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | 
| --- | --- | --- | --- | --- | 
|  1\.12\.10\-20190927  |  1\.12\.10  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  | 

------

## Amazon EKS\-optimized AMI with GPU Support<a name="eks-gpu-ami-versions"></a>

The table below lists the current and previous versions of the Amazon EKS\-optimized AMI with GPU support\.

------
#### [ Kubernetes version 1\.14 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | NVIDIA driver version | 
| --- | --- | --- | --- | --- | --- | 
|  1\.14\.7\-20190927  |  1\.14\.7  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  |  418\.87\.00  | 

------
#### [ Kubernetes version 1\.13 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | NVIDIA driver version | 
| --- | --- | --- | --- | --- | --- | 
|  1\.13\.11\-20190927  |  1\.13\.11  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  |  418\.87\.00  | 

------
#### [ Kubernetes version 1\.12 ]


| AMI version | `kubelet` version | Docker version | Kernel version | Packer version | NVIDIA driver version | 
| --- | --- | --- | --- | --- | --- | 
|  1\.12\.10\-20190927  |  1\.12\.10  |  18\.06\.1\-ce  |  4\.14\.146  |  v20190927  |  418\.87\.00  | 

------