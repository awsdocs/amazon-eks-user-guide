# Amazon EKS optimized Windows AMI versions<a name="eks-ami-versions-windows"></a>

This topic lists versions of the Amazon EKS optimized Windows AMIs and their corresponding versions of `kubelet`, Docker, `containerd`, and `csi-proxy`\.

The Amazon EKS optimized AMI metadata, including the AMI ID, for each variant can be retrieved programmatically\. For more information, see [Retrieving Amazon EKS optimized Windows AMI IDs](retrieve-windows-ami-id.md)\.

AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version-release_date
```

**Note**  
Amazon EKS managed node groups support the November 2022 and later releases of the Windows AMIs\.

## Amazon EKS optimized Windows Server 2022 Core AMI<a name="eks-ami-versions-windows-2022-core"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2022 Core AMI\.

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.13 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.23 ]


**Kubernetes version `1.23`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.23\-2023\.04\.11 | 1\.23\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.23\-2023\.03\.27 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.23\-2023\.03\.20 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.02\.14 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.23 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.11 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.12\.13 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.11\.08 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.10\.11 | 1\.23\.12 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 

------

## Amazon EKS optimized Windows Server 2022 Full AMI<a name="eks-ami-versions-windows-2022-full"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2022 Full AMI\.

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.14 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.23 ]


**Kubernetes version `1.23`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.23\-2023\.04\.11 | 1\.23\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.23\-2023\.03\.27 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.23\-2023\.03\.20 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.02\.14 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.23 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.11 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.12\.14 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.11\.08 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.10\.11 | 1\.23\.12 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 

------

## Amazon EKS optimized Windows Server 2019 Core AMI<a name="eks-ami-versions-windows-2019-core"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2019 Core AMI\.

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.13 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.11\.08 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.23 ]


**Kubernetes version `1.23`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.23\-2023\.04\.11 | 1\.23\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.23\-2023\.03\.27 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.23\-2023\.03\.20 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.02\.14 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.23 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.11 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.12\.14 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.11\.08 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.10\.12 | 1\.23\.12 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.10\.12 | 1\.23\.12 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.09\.13 | 1\.23\.9 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.08\.09 | 1\.23\.7 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.22 ]


**Kubernetes version `1.22`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.22\-2023\.04\.11 | 1\.22\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.22\-2023\.03\.27 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.22\-2023\.03\.20 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.02\.14 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.01\.23 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.01\.11 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.12\.14 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.11\.08 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.10\.12 | 1\.22\.15 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.09\.13 | 1\.22\.12 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.08\.09 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.07\.20 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.06\.17 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.05\.16 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.04\.14 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.21 ]


**Kubernetes version `1.21`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | 
| --- | --- | --- | --- | --- | 
| 1\.21\-2023\.02\.14 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2023\.01\.23 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2023\.01\.11 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.12\.13 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.11\.08 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.10\.12 | 1\.21\.14 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\.2022\.09\.13 | 1\.21\.14 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.08\.09 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\-2022\.07\.20 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\-2022\.06\.17 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\-2022\.05\.16 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\-2022\.04\.14 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2021\.03\.10 | 1\.21\.5 | 20\.10\.9 | 1\.6\.1 | N/A | 
| 1\.21\.2022\.02\.23 | 1\.21\.5 | 20\.10\.9 | N/A | N/A | 
| 1\.21\.2022\.01\.18 | 1\.21\.5 | 20\.10\.9 | N/A | N/A | 
| 1\.21\.2021\.12\.21 | 1\.21\.5 | 20\.10\.8 | N/A | N/A | 
| 1\.21\-2021\.10\.14 | 1\.21\.4 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.11\.10 | 1\.21\.4 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.09\.16 | 1\.21\.2 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.08\.12 | 1\.21\.2 | 20\.10\.6 | N/A | N/A | 

------
#### [ Kubernetes version 1\.20 ]


**Kubernetes version `1.20`**  

| AMI version | `kubelet` version | Docker version | `csi-proxy` version | 
| --- | --- | --- | --- | 
| 1\.20\-2022\.11\.08 | 1\.20\.15 | 20\.10\.21 | 1\.1\.1 | 
| 1\.20\-2022\.10\.12 | 1\.20\.15 | 20\.10\.17 | 1\.1\.1 | 
| 1\.20\-2022\.09\.13 | 1\.20\.15 | 20\.10\.17 | 1\.1\.1 | 
| 1\.20\-2022\.08\.09 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.07\.20 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.06\.17 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.05\.16 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.04\.14 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.03\.10 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2022\.02\.23 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2022\.01\.8 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2021\.12\.21 | 1\.20\.11 | 20\.10\.8 | N/A | 
| 1\.20\-2021\.11\.10 | 1\.20\.10 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.10\.14 | 1\.20\.10 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.09\.16 | 1\.20\.7 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.08\.12 | 1\.20\.4 | 20\.10\.6 | N/A | 
| 1\.20\-2021\.07\.14 | 1\.20\.4 | 20\.10\.6 | N/A | 
| 1\.20\-2021\.06\.16 | 1\.20\.4 | 20\.10\.5 | N/A | 
| 1\.20\-2021\.05\.18 | 1\.20\.4 | 20\.10\.4 | N/A | 

------

## Amazon EKS optimized Windows Server 2019 Full AMI<a name="eks-ami-versions-windows-2019-full"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2019 Full AMI\.

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.14 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.12 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.23 ]


**Kubernetes version `1.23`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.23\-2023\.04\.11 | 1\.23\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.23\-2023\.03\.27 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.23\-2023\.03\.20 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.02\.14 | 1\.23\.16 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.23 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2023\.01\.11 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.12\.14 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.11\.08 | 1\.23\.12 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.10\.12 | 1\.23\.12 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.09\.13 | 1\.23\.9 | 20\.10\.17 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.23\-2022\.08\.09 | 1\.23\.7 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.22 ]


**Kubernetes version `1.22`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | --- | 
| 1\.22\-2023\.04\.11 | 1\.22\.17 | 20\.10\.21 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.22\-2023\.03\.27 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | Installed a [domainless gMSA plugin](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.22\-2023\.03\.20 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.02\.14 | 1\.22\.17 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.01\.23 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2023\.01\.11 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.12\.14 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.11\.08 | 1\.22\.15 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.10\.12 | 1\.22\.15 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.09\.13 | 1\.22\.12 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 |  | 
| 1\.22\-2022\.08\.09 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.07\.20 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.06\.17 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.05\.16 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 
| 1\.22\-2022\.04\.14 | 1\.22\.6 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.21 ]


**Kubernetes version `1.21`**  

| AMI version | `kubelet` version | Docker version | `containerd` version | `csi-proxy` version | 
| --- | --- | --- | --- | --- | 
| 1\.21\-2023\.02\.14 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2023\.01\.23 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2023\.01\.11 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.12\.14 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.11\.08 | 1\.21\.14 | 20\.10\.21 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\-2022\.10\.12 | 1\.21\.14 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\.2022\.09\.13 | 1\.21\.14 | 20\.10\.17 | 1\.5\.13 | 1\.1\.1 | 
| 1\.21\.2022\.08\.11 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2022\.07\.20 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2022\.06\.17 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2022\.05\.16 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2022\.04\.14 | 1\.21\.5 | 20\.10\.9 | 1\.6\.2 | 1\.1\.1 | 
| 1\.21\.2022\.03\.10 | 1\.21\.5 | 20\.10\.9 | 1\.6\.1 | N/A | 
| 1\.21\.2022\.02\.23 | 1\.21\.5 | 20\.10\.9 | N/A | N/A | 
| 1\.21\.2022\.01\.18 | 1\.21\.5 | 20\.10\.9 | N/A | N/A | 
| 1\.21\.2021\.12\.21 | 1\.21\.5 | 20\.10\.8 | N/A | N/A | 
| 1\.21\-2021\.11\.10 | 1\.21\.4 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.10\.14 | 1\.21\.4 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.09\.16 | 1\.21\.2 | 20\.10\.7 | N/A | N/A | 
| 1\.21\-2021\.08\.12 | 1\.21\.2 | 20\.10\.6 | N/A | N/A | 

------
#### [ Kubernetes version 1\.20 ]


**Kubernetes version `1.20`**  

| AMI version | `kubelet` version | Docker version | `csi-proxy` version | 
| --- | --- | --- | --- | 
| 1\.20\-2022\.11\.08 | 1\.20\.15 | 20\.10\.21 | 1\.1\.1 | 
| 1\.20\-2022\.10\.12 | 1\.20\.15 | 20\.10\.17 | 1\.1\.1 | 
| 1\.20\-2022\.09\.13 | 1\.20\.15 | 20\.10\.17 | 1\.1\.1 | 
| 1\.20\-2022\.08\.09 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.07\.20 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.06\.17 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.05\.16 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.04\.14 | 1\.20\.11 | 20\.10\.9 | 1\.1\.1 | 
| 1\.20\-2022\.03\.10 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2022\.02\.23 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2022\.01\.8 | 1\.20\.11 | 20\.10\.9 | N/A | 
| 1\.20\-2021\.12\.21 | 1\.20\.11 | 20\.10\.8 | N/A | 
| 1\.20\-2021\.11\.10 | 1\.20\.10 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.10\.14 | 1\.20\.10 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.09\.16 | 1\.20\.7 | 20\.10\.7 | N/A | 
| 1\.20\-2021\.08\.12 | 1\.20\.4 | 20\.10\.6 | N/A | 
| 1\.20\-2021\.07\.14 | 1\.20\.4 | 20\.10\.6 | N/A | 
| 1\.20\-2021\.06\.16 | 1\.20\.4 | 20\.10\.5 | N/A | 
| 1\.20\-2021\.05\.18 | 1\.20\.4 | 20\.10\.4 | N/A | 

------