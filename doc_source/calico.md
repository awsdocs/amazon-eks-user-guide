# Installing the Calico network policy engine add\-on<a name="calico"></a>

[Project Calico](https://www.projectcalico.org/) is a network policy engine for Kubernetes\. With Calico network policy enforcement, you can implement network segmentation and tenant isolation\. This is useful in multi\-tenant environments where you must isolate tenants from each other or when you want to create separate environments for development, staging, and production\. Network policies are similar to AWS security groups in that you can create network ingress and egress rules\. Instead of assigning instances to a security group, you assign network policies to pods using pod selectors and labels\.

**Considerations**
+ Calico is not supported when using Fargate with Amazon EKS\.
+ Calico adds rules to `iptables` on the node that may be higher priority than existing rules that you've already implemented outside of Calico\. Consider adding existing `iptables` rules to your Calico policies to avoid having rules outside of Calico policy overridden by Calico\.
+ If you're using the Amazon VPC CNI add\-on version `1.10` or earlier, [security groups for pods](security-groups-for-pods.md) traffic flow to pods on branch network interfaces is not subjected to Calico network policy enforcement and is limited to Amazon EC2 security group enforcement only\. If you're using `1.11.0` or later of the Amazon VPC CNI add\-on, traffic flow to pods on branch network interfaces is subject to Calico network policy enforcement if you set `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard` for the Amazon VPC CNI add\-on\.
+ The IP family setting for your cluster must be `IPv4`\. You can't use the Calico network policy engine add\-on if your cluster was created to use the `IPv6` family\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.24`, you can use `kubectl` version `1.23`, `1.24`, or `1.25` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

The following procedure shows you how to install Calico on Linux nodes in your Amazon EKS cluster\. To install Calico on Windows nodes, see [Using Calico on Amazon EKS Windows Containers](http://aws.amazon.com/blogs/containers/open-source-calico-for-windows-containers-on-amazon-eks/)\.

## Install Calico on your Amazon EKS Linux nodes<a name="calico-install"></a>

**Important**  
Amazon EKS doesn't maintain the charts used in the following procedures\. The recommended way to install Calico on Amazon EKS is by using the [Calico Operator](https://github.com/tigera/operator)\. If you encounter issues during installation and usage of Calico, submit issues to [Calico Operator](https://github.com/tigera/operator) and the [Calico](https://github.com/projectcalico/calico) project directly\. You should always contact Tigera for compatibility of any new Calico operator and Calico versions before installing them on your cluster\.

**Prerequisite**  
Helm version `3.0` or later installed on your computer\. To install or upgrade Helm, see [Using Helm with Amazon EKS](helm.md)\.

**To install Calico using Helm**

1. Install Calico version `3.25` using the Tigera instructions\. For more information, see [Install Calico](https://docs.tigera.io/calico/3.25/getting-started/kubernetes/helm#install-calico) in the Calico documentation\.

1. View the resources in the `tigera-operator` namespace\.

   ```
   kubectl get all -n tigera-operator
   ```

   The example output is as follows\.

   ```
   NAME                                   READY   STATUS    RESTARTS   AGE
   pod/tigera-operator-768d489967-6cv58   1/1     Running   0          27m
   
   NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/tigera-operator   1/1     1            1           27m
   
   NAME                                         DESIRED   CURRENT   READY   AGE
   replicaset.apps/tigera-operator-768d489967   1         1         1       27m
   ```

   The values in the `DESIRED` and `READY` columns for the `replicaset` should match\.

1. View the resources in the `calico-system` namespace\.

   ```
   kubectl get all -n calico-system
   ```

   The example output is as follows\.

   ```
   NAME                                         READY   STATUS    RESTARTS   AGE
   pod/calico-kube-controllers-55c98678-gh6cc   1/1     Running   0          4m29s
   pod/calico-node-khw4w                        1/1     Running   0          4m29s
   pod/calico-node-rrz8k                        1/1     Running   0          4m29s
   pod/calico-typha-696bcd55cb-49prr            1/1     Running   0          4m29s
   pod/csi-node-driver-6v2z5                    2/2     Running   0          4m29s
   pod/csi-node-driver-wrw2d                    2/2     Running   0          4m29s
   
   NAME                                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
   service/calico-kube-controllers-metrics   ClusterIP   None           <none>        9094/TCP   4m23s
   service/calico-typha                      ClusterIP   10.100.67.39   <none>        5473/TCP   4m30s
   
   NAME                             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
   daemonset.apps/calico-node       2         2         2       2            2           kubernetes.io/os=linux   4m29s
   daemonset.apps/csi-node-driver   2         2         2       2            2           kubernetes.io/os=linux   4m29s
   
   NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/calico-kube-controllers   1/1     1            1           4m29s
   deployment.apps/calico-typha              1/1     1            1           4m29s
   
   NAME                                               DESIRED   CURRENT   READY   AGE
   replicaset.apps/calico-kube-controllers-55c98678   1         1         1       4m29s
   replicaset.apps/calico-typha-696bcd55cb            1         1         1       4m29s
   ```

   The values in the `DESIRED` and `READY` columns for the `calico-node` `daemonset` should match\. The values in the `DESIRED` and `READY` columns for the two `replicasets` should also match\. The number in the `DESIRED` column for `daemonset.apps/calico-node` varies based on the number of nodes in your cluster\.

1. Confirm that the logs for one of your `calico-node`, `calico-typha`, and `tigera-operator` pods don't contain `ERROR`\. Replace the values in the following commands with the values returned in your output for the previous steps\. 

   ```
   kubectl logs tigera-operator-768d489967-6cv58 -n tigera-operator | grep ERROR
   kubectl logs calico-node-khw4w -c calico-node -n calico-system | grep ERROR
   kubectl logs calico-typha-696bcd55cb-49prr -n calico-system | grep ERROR
   ```

   If no output is returned from the previous commands, then `ERROR` doesn't exist in your logs and everything should be running correctly\. 

1. If you're using version `1.9.3` or later of the Amazon VPC CNI plugin for Kubernetes, then enable the plugin to add the pod IP address to an annotation in the `calico-kube-controllers-55c98678-gh6cc` pod spec\. For more information about this setting, see [https://github.com/aws/amazon-vpc-cni-k8s#annotate_pod_ip-v193](https://github.com/aws/amazon-vpc-cni-k8s#annotate_pod_ip-v193) on GitHub\.

   1. See which version of the plugin is installed on your cluster with the following command\.

      ```
      kubectl describe daemonset aws-node -n kube-system | grep amazon-k8s-cni: | cut -d ":" -f 3
      ```

      The example output is as follows\.

      ```
      v1.12.2-eksbuild.1
      ```

   1. Create a configuration file that you can apply to your cluster that grants the `aws-node` Kubernetes `clusterrole` the permission to patch pods\.

      ```
      cat << EOF > append.yaml
      - apiGroups:
        - ""
        resources:
        - pods
        verbs:
        - patch
      EOF
      ```

   1. Apply the updated permissions to your cluster\.

      ```
      kubectl apply -f <(cat <(kubectl get clusterrole aws-node -o yaml) append.yaml)
      ```

   1. Set the environment variable for the plugin\.

      ```
      kubectl set env daemonset aws-node -n kube-system ANNOTATE_POD_IP=true
      ```

   1. Delete the `calico-kube-controllers-55c98678-gh6cc`

      ```
      kubectl delete pod calico-kube-controllers-55c98678-gh6cc -n calico-system
      ```

   1. View the pods in the `calico-system` namespace again to see the ID of the new `calico-kube-controllers` pod that Kubernetes replaced the `calico-kube-controllers-55c98678-gh6cc` pod that you deleted in the previous step with\.

      ```
      kubectl get pods -n calico-system
      ```

   1. Confirm that the `vpc.amazonaws.com/pod-ips` annotation is added to the new `calico-kube-controllers` pod\. 

      1. Replace *5cd7d477df*\-*2xqpd* with the ID for the pod returned in a previous step\.

        ```
        kubectl describe pod calico-kube-controllers-5cd7d477df-2xqpd -n calico-system | grep vpc.amazonaws.com/pod-ips
        ```

        The example output is as follows\.

        ```
        vpc.amazonaws.com/pod-ips: 192.168.25.9
        ```

## Stars policy demo<a name="calico-stars-demo"></a>

This section walks through the [Stars policy demo](https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/) provided by the Project Calico documentation and isn't necessary for Calico functionality on your cluster\. The demo creates a front\-end, back\-end, and client service on your Amazon EKS cluster\. The demo also creates a management graphical user interface that shows the available ingress and egress paths between each service\. We recommend that you complete the demo on a cluster that you don't run production workloads on\. 

Before you create any network policies, all services can communicate bidirectionally\. After you apply the network policies, you can see that the client can only communicate with the front\-end service, and the back\-end only accepts traffic from the front\-end\.

**To run the Stars policy demo**

1. Apply the front\-end, back\-end, client, and management user interface services:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/00-namespace.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/01-management-ui.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/02-backend.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/03-frontend.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/04-client.yaml
   ```

1. View all pods on the cluster\.

   ```
   kubectl get pods -A
   ```

   The example output is as follows\.

   In your output, you should see pods in the namespaces shown in the following output\. Your pod *NAMES* and the number of pods in the `READY` column are different than those in the following output\. Don't continue until you see pods with similar names and they all have `Running` in the `STATUS` column\.

   ```
   NAMESPACE         NAME                                       READY   STATUS    RESTARTS   AGE
   ...
   client            client-xlffc                               1/1     Running   0          5m19s
   ...
   management-ui     management-ui-qrb2g                        1/1     Running   0          5m24s
   stars             backend-sz87q                              1/1     Running   0          5m23s
   stars             frontend-cscnf                             1/1     Running   0          5m21s
   ...
   ```

1. To connect to the management user interface, forward your local port 9001 to the `management-ui` service running on your cluster:

   ```
   kubectl port-forward service/management-ui -n management-ui 9001
   ```

1. Open a browser on your local system and point it to [http://localhost:9001/](http://localhost:9001/)\. You should see the management user interface\. The **C** node is the client service, the **F** node is the front\-end service, and the **B** node is the back\-end service\. Each node has full communication access to all other nodes, as indicated by the bold, colored lines\.  
![\[Open network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-default.png)

1. Apply the following network policies to isolate the services from each other:

   ```
   kubectl apply -n stars -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/default-deny.yaml
   kubectl apply -n client -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/default-deny.yaml
   ```

1. Refresh your browser\. You see that the management user interface can no longer reach any of the nodes, so they don't show up in the user interface\.

1. Apply the following network policies to allow the management user interface to access the services:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/allow-ui.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/allow-ui-client.yaml
   ```

1. Refresh your browser\. You see that the management user interface can reach the nodes again, but the nodes cannot communicate with each other\.  
![\[UI access network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-no-traffic.png)

1. Apply the following network policy to allow traffic from the front\-end service to the back\-end service:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/backend-policy.yaml
   ```

1. Refresh your browser\. You see that the front\-end can communicate with the back\-end\.  
![\[Front-end to back-end policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-front-end-back-end.png)

1. Apply the following network policy to allow traffic from the client to the front\-end service\.

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/policies/frontend-policy.yaml
   ```

1. Refresh your browser\. You see that the client can communicate to the front\-end service\. The front\-end service can still communicate to the back\-end service\.  
![\[Final network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-final.png)

1. \(Optional\) When you are done with the demo, you can delete its resources\.

   ```
   kubectl delete -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/04-client.yaml
   kubectl delete -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/03-frontend.yaml
   kubectl delete -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/02-backend.yaml
   kubectl delete -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/01-management-ui.yaml
   kubectl delete -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/tutorials/stars-policy/manifests/00-namespace.yaml
   ```

   Even after deleting the resources, there can still be `iptables` rules on the nodes that might interfere in unexpected ways with networking in your cluster\. The only sure way to remove Calico is to terminate all of the nodes and recycle them\. To terminate all nodes, either set the Auto Scaling Group desired count to 0, then back up to the desired number, or just terminate the nodes\. If you are unable to recycle the nodes, then see [Disabling and removing Calico Policy](https://github.com/projectcalico/calico/blob/master/calico/hack/remove-calico-policy/remove-policy.md) in the Calico GitHub repository for a last resort procedure\.

## Remove Calico<a name="remove-calico"></a>

Remove Calico from your cluster using Helm\.

```
helm uninstall calico
```