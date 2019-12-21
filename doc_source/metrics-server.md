# Installing the Kubernetes Metrics Server<a name="metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. The metrics server is commonly used by other Kubernetes add ons, such as the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) or the [Kubernetes Dashboard](dashboard-tutorial.md)\. For more information, see [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/) in the Kubernetes documentation\. This topic explains how to deploy the Kubernetes metrics server on your Amazon EKS cluster\.

Choose the tab below that corresponds to your desired installation method:

------
#### [ curl and jq ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using `curl` and `jq`**

If you have a macOS or Linux system with `curl`, `tar`, `gzip`, and the `jq` JSON parser installed, you can download, extract, and install the latest release with the following commands\. Otherwise, use the next procedure to download the latest version using a web browser\.

1. Open a terminal window and navigate to a directory where you would like to download the latest `metrics-server` release\. 

1. Copy and paste the commands below into your terminal window and type **Enter** to execute them\. These commands download the latest release, extract it, and apply the version 1\.8\+ manifests to your cluster\.

   ```
   DOWNLOAD_URL=$(curl -Ls "https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest" | jq -r .tarball_url)
   DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
   curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
   mkdir metrics-server-$DOWNLOAD_VERSION
   tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
   kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------
#### [ Web browser ]

**To install `metrics-server` from GitHub on an Amazon EKS cluster using a web browser**

1. Download and extract the latest version of the metrics server code from GitHub\.

   1. Navigate to the latest release page of the `metrics-server` project on GitHub \([https://github\.com/kubernetes\-sigs/metrics\-server/releases/latest](https://github.com/kubernetes-sigs/metrics-server/releases/latest)\), then choose a source code archive for the latest release to download it\.
**Note**  
If you are downloading to a remote server, you can use the following `curl` command, substituting the red text with the latest version number\.  

      ```
      curl -o v0.3.6.tar.gz https://github.com/kubernetes-sigs/metrics-server/archive/v0.3.6.tar.gz
      ```

   1. Navigate to your downloads location and extract the source code archive\. For example, if you downloaded the `.tar.gz` archive, use the following command to extract \(substituting your release version\)\. 

      ```
      tar -xzf v0.3.6.tar.gz
      ```

1. Apply all of the YAML manifests in the `metrics-server-0.3.6/deploy/1.8+` directory \(substituting your release version\)\.

   ```
   kubectl apply -f metrics-server-0.3.6/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command\.

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

------