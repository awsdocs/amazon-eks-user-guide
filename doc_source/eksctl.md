# Installing or updating `eksctl`<a name="eksctl"></a>

`eksctl` is a simple command line tool for creating and managing Kubernetes clusters on Amazon EKS\. `eksctl` provides the fastest and easiest way to create a new cluster with nodes for Amazon EKS\. For the official documentation, see [https://eksctl\.io/](https://eksctl.io/)\.

Determine whether you already have `eksctl` installed on your device\.

```
eksctl version
```

If you have `eksctl` installed in the path of your device, the example output is as follows\. If you want to update the version that you currently have installed with a later version, make sure to install the new version in the same location that your current version is in\.

```
0.160.0
```

If you receive no output, then you either don't have `eksctl` installed, or it's not installed in a location that's in your device's path\.

For instructions on installing or updating `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.