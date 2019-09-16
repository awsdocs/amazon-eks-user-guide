# Installing the Kubernetes Metrics Server<a name="metrics-server"></a>

The Kubernetes metrics server is an aggregator of resource usage data in your cluster, and it is not deployed by default in Amazon EKS clusters\. This topic explains how to deploy the Kubernetes metrics server on your Amazon EKS cluster\.

**Note**  
The Kubernetes metrics server must be installed on your cluster to use the [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)\.

**To install `metrics-server` from GitHub on an Amazon EKS cluster using `curl` and `jq`**

If you have a macOS or Linux system with `curl`, `tar`, `gzip`, and the `jq` JSON parser installed, you can download, extract, and install the latest release with the following commands\. Otherwise, use the next procedure to download the latest version using a web browser\.

1. Open a terminal window and navigate to a directory where you would like to download the latest `metrics-server` release\. 

1. Copy and paste the commands below into your terminal window and type **Enter** to execute them\. These commands download the latest release, extract it, and apply the version 1\.8\+ manifests to your cluster\.

   ```
   DOWNLOAD_URL=$(curl --silent "https://api.github.com/repos/kubernetes-incubator/metrics-server/releases/latest" | jq -r .tarball_url)
   DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
   curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
   mkdir metrics-server-$DOWNLOAD_VERSION
   tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
   kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command:

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```

**To install `metrics-server` from GitHub on an Amazon EKS cluster using a web browser**

1. Download and extract the latest version of the metrics server code from GitHub\.

   1. Navigate to the latest release page of the `metrics-server` project on GitHub \([https://github\.com/kubernetes\-incubator/metrics\-server/releases/latest](https://github.com/kubernetes-incubator/metrics-server/releases/latest)\), then choose a source code archive for the latest release to download it\.

      ```
      curl --remote-name --location https://github.com/kubernetes-incubator/metrics-server/archive/v0.3.4.tar.gz
      ```

   1. Navigate to your downloads folder and extract the source code archive\. For example, if you downloaded the `.tar.gz` archive on a macOS or Linux system, use the following command to extract \(substituting your release version\)\. 

      ```
      tar -xzf v0.3.4.tar.gz
      ```

1. <a name="apply-metrics-server-step"></a>Apply all of the YAML manifests in the `metrics-server-0.3.4/deploy/1.8+` directory \(substituting your release version\)\.

   ```
   kubectl apply -f metrics-server-0.3.4/deploy/1.8+/
   ```

1. Verify that the `metrics-server` deployment is running the desired number of pods with the following command:

   ```
   kubectl get deployment metrics-server -n kube-system
   ```

   Output:

   ```
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1         1         1            1           56m
   ```
