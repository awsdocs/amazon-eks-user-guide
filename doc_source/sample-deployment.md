--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Deploy a sample application<a name="sample-deployment"></a>

In this topic, you deploy a sample application to your cluster\.

Though many variables are changeable in the following steps, we recommend only changing variable values where specified\. Once you have a better understanding of Kubernetes Pods, deployments, and services, you can experiment with changing other values\.

\+

```
kubectl create namespace eks-sample-app
```

1. Create a Kubernetes deployment\. This sample deployment pulls a container image from a public repository and deploys three replicas \(individual Pods\) of it to your cluster\. To learn more, see [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) in the Kubernetes documentation\. You can deploy the application to Linux or Windows nodes\. If you’re deploying to Fargate, then you can only deploy a Linux application\.  
 Linux   
   + The `amd64` or `arm64`values under the `kubernetes.io/arch` key mean that the application can be deployed to either hardware architecture \(if you have both in your cluster\)\. This is possible because this image is a multi\-architecture image, but not all are\. You can determine the hardware architecture that the image is supported on by viewing the [image details](https://gallery.ecr.aws/nginx/nginx) in the repository that you’re pulling it from\. When deploying images that don’t support a hardware architecture type, or that you don’t want the image deployed to, remove that type from the manifest\. For more information, see [Well\-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/) in the Kubernetes documentation\.

     The `kubernetes\.io/os: linux``nodeSelector` means that if you had Linux and Windows nodes \(for example\) in your cluster, the image would only be deployed to Linux nodes\. For more information, see [Well\-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/) in the Kubernetes documentation\.

     ```
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: eks-sample-linux-deployment
       namespace: eks-sample-app
       labels:
         app: eks-sample-linux-app
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: eks-sample-linux-app
       template:
         metadata:
           labels:
             app: eks-sample-linux-app
         spec:
           affinity:
             nodeAffinity:
               requiredDuringSchedulingIgnoredDuringExecution:
                 nodeSelectorTerms:
                 - matchExpressions:
                   - key: kubernetes.io/arch
                     operator: In
                     values:
                     - amd64
                     - arm64
           containers:
           - name: nginx
             image: public.ecr.aws/nginx/nginx:1.23
             ports:
             - name: http
               containerPort: 80
             imagePullPolicy: IfNotPresent
           nodeSelector:
             kubernetes.io/os: linux
     ```  
 Windows   
   + The `kubernetes\.io/os: windows``nodeSelector` means that if you had Windows and Linux nodes \(for example\) in your cluster, the image would only be deployed to Windows nodes\. For more information, see [Well\-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/) in the Kubernetes documentation\.

     ```
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: eks-sample-windows-deployment
       namespace: eks-sample-app
       labels:
         app: eks-sample-windows-app
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: eks-sample-windows-app
       template:
         metadata:
           labels:
             app: eks-sample-windows-app
         spec:
           affinity:
             nodeAffinity:
               requiredDuringSchedulingIgnoredDuringExecution:
                 nodeSelectorTerms:
                 - matchExpressions:
                   - key: beta.kubernetes.io/arch
                     operator: In
                     values:
                     - amd64
           containers:
           - name: windows-server-iis
             image: mcr.microsoft.com/windows/servercore:ltsc2019
             ports:
             - name: http
               containerPort: 80
             imagePullPolicy: IfNotPresent
             command:
             - powershell.exe
             - -command
             - "Add-WindowsFeature Web-Server; Invoke-WebRequest -UseBasicParsing -Uri 'https://dotnetbinaries.blob.core.windows.net/servicemonitor/2.0.1.6/ServiceMonitor.exe' -OutFile 'C:\\ServiceMonitor.exe'; echo '<html><body><br/><br/><marquee><H1>Hello EKS!!!<H1><marquee></body><html>' > C:\\inetpub\\wwwroot\\default.html; C:\\ServiceMonitor.exe 'w3svc'; "
           nodeSelector:
             kubernetes.io/os: windows
     ```

     1. Apply the deployment manifest to your cluster\.

        ```
        kubectl apply -f eks-sample-deployment.yaml
        ```  
 Linux   
 **\*** 

```
apiVersion: v1
kind: Service
metadata:
  name: eks-sample-linux-service
  namespace: eks-sample-app
  labels:
    app: eks-sample-linux-app
spec:
  selector:
    app: eks-sample-linux-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

 Windows   
 **\*** 

```
apiVersion: v1
kind: Service
metadata:
  name: eks-sample-windows-service
  namespace: eks-sample-app
  labels:
    app: eks-sample-windows-app
spec:
  selector:
    app: eks-sample-windows-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

1. Apply the service manifest to your cluster\.

   ```
   kubectl apply -f eks-sample-service.yaml
   ```

   1.  View all resources that exist in the `eks-sample-app` namespace\.

      ```
      kubectl get all -n eks-sample-app
      ```

      An example output is as follows\.

      If you deployed Windows resources, then all instances of ` linux ` in the following output are `windows`\. The other *example values* may be different from your output\.

      ```
      NAME                                               READY   STATUS    RESTARTS   AGE
      pod/eks-sample-linux-deployment-65b7669776-m6qxz   1/1     Running   0          27m
      pod/eks-sample-linux-deployment-65b7669776-mmxvd   1/1     Running   0          27m
      pod/eks-sample-linux-deployment-65b7669776-qzn22   1/1     Running   0          27m
      
      NAME                               TYPE         CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
      service/eks-sample-linux-service   ClusterIP    10.100.74.8     <none>        80/TCP    32m
      
      NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
      deployment.apps/eks-sample-linux-deployment 3/3     3            3           27m
      
      NAME                                                      DESIRED   CURRENT   READY   AGE
      replicaset.apps/eks-sample-linux-deployment-776d8f8fd8    3         3         3       27m
      ```

      In the output, you see the service and deployment that were specified in the sample manifests deployed in previous steps\. You also see three Pods\. This is because `3`replicas were specified in the sample manifest. For more information about Pods, see [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) in the Kubernetes documentation. Kubernetes automatically creates the `replicaset` resource, even though it isn’t specified in the sample manifests\. For more information about `ReplicaSets`, see [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) in the Kubernetes documentation\.

   1. View the details of the deployed service\. If you deployed a Windows service, replace ` linux ` with `windows`\.

      ```
      kubectl -n eks-sample-app describe service eks-sample-linux-service
      ```

      An example output is as follows\.

      If you deployed Windows resources, then all instances of ` linux ` in the following output are `windows`\. The other *example values* may be different from your output\.

      ```
      Name:              eks-sample-`linux`-service
      Namespace:         eks-sample-app
      Labels:            app=eks-sample-`linux`-app
      Annotations:       <none>
      Selector:          app=eks-sample-`linux`-app
      Type:              ClusterIP
      IP Families:       <none>
      IP:`10.100.74.8`IPs:`10.100.74.8`Port:              <unset>  80/TCP
      TargetPort:        80/TCP
      Endpoints:`192.168.24.212`:80,`192.168.50.185`:80,`192.168.63.93`:80
      Session Affinity:  None
      Events:            <none>
      ```

      In the previous output, the value for `IP:` is a unique IP address that can be reached from any node or Pod within the cluster, but it can’t be reached from outside of the cluster\. The values for `Endpoints` are IP addresses assigned from within your VPC to the Pods that are part of the service\.

      ```
      kubectl -n eks-sample-app describe pod eks-sample-linux-deployment-65b7669776-m6qxz
      ```

      Abbreviated output

      If you deployed Windows resources, then all instances of ` linux ` in the following output are `windows`\. The other ` example values ` may be different from your output\.

      ```
      Name:         eks-sample-`linux`-deployment-`65b7669776-m6qxz`Namespace:    eks-sample-app
      Priority:     0
      Node:         ip-`192-168-45-132`.`us-west-2`.compute.internal/`192.168.45.132`[...]
      IP:`192.168.63.93`IPs:
        IP:`192.168.63.93`Controlled By:  ReplicaSet/eks-sample-`linux`-deployment-`65b7669776`[...]
      Conditions:
        Type              Status
        Initialized       True
        Ready             True
        ContainersReady   True
        PodScheduled      True
      [...]
      Events:
        Type    Reason     Age    From                                                 Message
        ----    ------     ----   ----                                                 -------
        Normal  Scheduled  3m20s  default-scheduler                                    Successfully assigned eks-sample-app/eks-sample-`linux`-deployment-`65b7669776-m6qxz`to ip-`192-168-45-132`.`us-west-2`.compute.internal
      [...]
      ```

   1. Run a shell on the Pod that you described in the previous step, replacing ` 65b7669776-m6qxz ` with the ID of one of your Pods\.  
 Linux   
\*\*

```
kubectl exec -it eks-sample-linux-deployment-65b7669776-m6qxz -n eks-sample-app -- /bin/bash
```

 Windows   
\*\*

```
kubectl exec -it eks-sample-windows-deployment-65b7669776-m6qxz -n eks-sample-app -- powershell.exe
```

1. From the Pod shell, view the output from the web server that was installed with your deployment in a previous step\. You only need to specify the service name\. It is resolved to the service’s IP address by CoreDNS, which is deployed with an Amazon EKS cluster, by default\.  
 Linux   
\*\*

```
curl eks-sample-linux-service
```

\+

An example output is as follows\.

\+

```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
[...]
```

 Windows   
\*\*

```
Invoke-WebRequest -uri eks-sample-windows-service/default.html -UseBasicParsing
```

\+

An example output is as follows\.

\+

```
StatusCode        : 200
StatusDescription : OK
Content           : < h t m l > < b o d y > < b r / > < b r / > < m a r q u e e > < H 1 > H e l l o
                      E K S ! ! ! < H 1 > < m a r q u e e > < / b o d y > < h t m l >
```

1. From the Pod shell, view the DNS server for the Pod\.  
 Linux   
\*\*

```
cat /etc/resolv.conf
```

\+

An example output is as follows\.

\+

```
nameserver 10.100.0.10
search eks-sample-app.svc.cluster.local svc.cluster.local cluster.local`us-west-2`.compute.internal
options ndots:5
```

\+

In the previous output, `10.100.0.10` is automatically assigned as the `nameserver` for all Pods deployed to the cluster\.

 Windows   
\*\*

```
Get-NetIPConfiguration
```

\+

Abbreviated output

\+

```
InterfaceAlias       : vEthernet
[...]
IPv4Address          : 192.168.63.14
[...]
DNSServer            : 10.100.0.10
```

\+

In the previous output, `10.100.0.10` is automatically assigned as the DNS server for all Pods deployed to the cluster\. \. Disconnect from the Pod by typing `exit`\. \. Once you’re finished with the sample application, you can remove the sample namespace, service, and deployment with the following command\.

\+

```
kubectl delete namespace eks-sample-app
```

## Next Steps<a name="next-steps"></a>

After you deploy the sample application, you might want to try some of the following exercises: