# Create a `kubeconfig` for Amazon EKS<a name="create-kubeconfig"></a>

In this section, you create a `kubeconfig` file for your cluster\. The code block below shows the `kubeconfig` elements to add to your configuration\. If you have an existing configuration and you are comfortable working with `kubeconfig` files, you can merge these elements into your existing setup\. Be sure to replace the *<endpoint\-url>* value with the full endpoint URL \(for example, *https://API\_SERVER\_ENDPOINT\.yl4\.us\-west\-2\.eks\.amazonaws\.com*\) that was created for your cluster, replace the *<base64\-encoded\-ca\-cert>* with the `certificateAuthority.data` value you retrieved earlier, and replace the *<cluster\-name>* with your cluster name\.

Optionally, you can uncomment the `-r` and `<role-arn>` lines and substitute an IAM role ARN to use with your user\. If you manage multiple AWS credential profiles, you can either set the `AWS_PROFILE` variable in your shell or specify the environment variable value for the authenticator to use in your kubeconfig as shown below\.

```
apiVersion: v1
clusters:
- cluster:
    server: <endpoint-url>
    certificate-authority-data: <base64-encoded-ca-cert>
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: heptio-authenticator-aws
      args:
        - "token"
        - "-i"
        - "<cluster-name>"
        # - "-r"
        # - "<role-arn>"
      # env:
        # - name: AWS_PROFILE
        #   value: "<aws-profile>"
```

If you do not have an existing configuration, or to add the Amazon EKS cluster without modifying your existing configuration files, you can use the following procedure to add the Amazon EKS cluster to your configuration\.

**To retrieve your cluster information with the AWS CLI**

When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. These must be added to your kubectl configuration so that you can communicate with your cluster\.

1. Retrieve the `endpoint` for your cluster\. Use this for the *<endpoint\-url>* in your `kubeconfig` file\.

   ```
   aws eks describe-cluster --cluster-name devel  --query cluster.endpoint
   ```

1. Retrieve the `certificateAuthority.data` for your cluster\. Use this for the *<base64\-encoded\-ca\-cert>* in your `kubeconfig` file\.

   ```
   aws eks describe-cluster --cluster-name devel  --query cluster.certificateAuthority.data
   ```

**To create your `kubeconfig` file**

1. Create the default kubectl folder if it does not already exist\.

   ```
   mkdir -p ~/.kube
   ```

1. Open your favorite text editor and copy the above `kubeconfig` code block into it\.

1. Replace the *<endpoint\-url>* with the endpoint URL that was created for your cluster\.

1. Replace the *<base64\-encoded\-ca\-cert>* with the `certificateAuthority.data` that was created for your cluster\.

1. Replace the *<cluster\-name>* with your cluster name\.

1. Save the file to the default kubectl folder, with your cluster name in the file name\. For example, if your cluster name is *devel*, save the file to `~/.kube/config-devel`\.

1. Add that file path to your `KUBECONFIG` environment variable so that kubectl knows where to look for your cluster configuration\.

   ```
   export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel
   ```

1. \(Optional\) Add the configuration to your shell initialization file so that it is configured when you open a shell\.
   + For Bash shells on macOS:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel' >> ~/.bash_profile
     ```
   + For Bash shells on Linux:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel' >> ~/.bashrc
     ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive the error `"heptio-authenticator-aws": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```