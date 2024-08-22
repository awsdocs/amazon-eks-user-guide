# Manage CoreDNS for DNS in Amazon EKS clusters<a name="managing-coredns"></a>

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. The CoreDNS Pods can be deployed to Fargate nodes if your cluster includes an [Define which Pods use AWS Fargate when launched](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\. For more information about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) in the Kubernetes documentation\.

The following table lists the latest version of the Amazon EKS add\-on type for each Kubernetes version\.<a name="coredns-versions"></a>


| Kubernetes version | `1.30` | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | 
|  | v1\.11\.1\-eksbuild\.9 | v1\.11\.1\-eksbuild\.9 | v1\.10\.1\-eksbuild\.11 | v1\.10\.1\-eksbuild\.11 | v1\.9\.3\-eksbuild\.15 | v1\.9\.3\-eksbuild\.15 | v1\.9\.3\-eksbuild\.15 | v1\.8\.7\-eksbuild\.10 | 

**Important**  
If you're self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\. For more information about updating the self\-managed type of this add\-on, see [Update the CoreDNS Amazon EKS self\-managed add\-on](coredns-add-on-self-managed-update.md)\.

## Important CoreDNS upgrade considerations<a name="coredns-upgrade"></a>
+ To improve the stability and availability of the CoreDNS Deployment, versions `v1.9.3-eksbuild.6` and later and `v1.10.1-eksbuild.3` are deployed with a `PodDisruptionBudget`\. If you've deployed an existing `PodDisruptionBudget`, your upgrade to these versions might fail\. If the upgrade fails, completing one of the following tasks should resolve the issue:
  + When doing the upgrade of the Amazon EKS add\-on, choose to override the existing settings as your conflict resolution option\. If you've made other custom settings to the Deployment, make sure to back up your settings before upgrading so that you can reapply your other custom settings after the upgrade\.
  + Remove your existing `PodDisruptionBudget` and try the upgrade again\.
+ In EKS add\-on versions `v1.9.3-eksbuild.3` and later and `v1.10.1-eksbuild.6` and later, the CoreDNS Deployment sets the `readinessProbe` to use the `/ready` endpoint\. This endpoint is enabled in the `Corefile` configuration file for CoreDNS\.

  If you use a custom `Corefile`, you must add the `ready` plugin to the config, so that the `/ready` endpoint is active in CoreDNS for the probe to use\.
+ In EKS add\-on versions `v1.9.3-eksbuild.7` and later and `v1.10.1-eksbuild.4` and later, you can change the `PodDisruptionBudget`\. You can edit the add\-on and change these settings in the **Optional configuration settings** using the fields in the following example\. This example shows the default `PodDisruptionBudget`\.

  ```
  {
      "podDisruptionBudget": {
          "enabled": true,
          "maxUnavailable": 1
          }
  }
  ```

  You can set `maxUnavailable` or `minAvailable`, but you can't set both in a single `PodDisruptionBudget`\. For more information about `PodDisruptionBudgets`, see [Specifying a `PodDisruptionBudget`](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#specifying-a-poddisruptionbudget) in the *Kubernetes documentation*\.

  Note that if you set `enabled` to `false`, the `PodDisruptionBudget` isn't removed\. After you set this field to `false`, you must delete the `PodDisruptionBudget` object\. Similarly, if you edit the add\-on to use an older version of the add\-on \(downgrade the add\-on\) after upgrading to a version with a `PodDisruptionBudget`, the `PodDisruptionBudget` isn't removed\. To delete the `PodDisruptionBudget`, you can run the following command:

  ```
  kubectl delete poddisruptionbudget coredns -n kube-system
  ```
+ In EKS add\-on versions `v1.10.1-eksbuild.5` and later, change the default toleration from `node-role.kubernetes.io/master:NoSchedule` to `node-role.kubernetes.io/control-plane:NoSchedule` to comply with KEP 2067\. For more information about KEP 2067, see [KEP\-2067: Rename the kubeadm "master" label and taint](https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/kubeadm/2067-rename-master-label-taint#renaming-the-node-rolekubernetesiomaster-node-taint) in the *Kubernetes Enhancement Proposals \(KEPs\)* on GitHub\.

  In EKS add\-on versions `v1.8.7-eksbuild.8` and later and `v1.9.3-eksbuild.9` and later, both tolerations are set to be compatible with every Kubernetes version\.
+ In EKS add\-on versions `v1.9.3-eksbuild.11` and `v1.10.1-eksbuild.7` and later, the CoreDNS Deployment sets a default value for `topologySpreadConstraints`\. The default value ensures that the CoreDNS Pods are spread across the Availability Zones if there are nodes in multiple Availability Zones available\. You can set a custom value that will be used instead of the default value\. The default value follows:

  ```
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels:
          k8s-app: kube-dns
  ```

### CoreDNS v`1.11` upgrade considerations<a name="coredns-upgrade-1.11"></a>
+ In EKS add\-on versions `v1.11.1-eksbuild.4` and later, the container image is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. The usage and troubleshooting of the CoreDNS image remains the same\.