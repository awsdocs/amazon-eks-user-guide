# Installing CoreDNS<a name="coredns"></a>

Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated from a 1\.10 cluster and you want to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\.

To check if your cluster is already running CoreDNS, use the following command\.

```
kubectl get pod -n kube-system -l k8s-app=kube-dns
```

If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, use the following procedure to update your DNS and service discovery provider to CoreDNS\.

**Note**  
The service for CoreDNS is still called `kube-dns` for backward compatibility\.

**To install CoreDNS on an updated Amazon EKS cluster with `kubectl`**

1. Add the `{"eks.amazonaws.com/component": "kube-dns"}` selector to the `kube-dns` deployment for your cluster\. This prevents the two DNS deployments from competing for control of the same set of labels\.

   ```
   kubectl patch -n kube-system deployment/kube-dns --patch \
   '{"spec":{"selector":{"matchLabels":{"eks.amazonaws.com/component":"kube-dns"}}}}'
   ```

1. Deploy CoreDNS to your cluster\.

   1. Set your cluster's DNS IP address to the `DNS_CLUSTER_IP` environment variable\.

      ```
      export DNS_CLUSTER_IP=$(kubectl get svc -n kube-system kube-dns -o jsonpath='{.spec.clusterIP}')
      ```

   1. Set your cluster's AWS Region to the `REGION` environment variable\.

      ```
      export REGION="us-west-2"
      ```

   1. Download the CoreDNS manifest from the Amazon EKS resource bucket\.

      ```
      curl -o dns.yaml https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-09-27/dns.yaml
      ```

   1. Replace the variable placeholders in the `dns.yaml` file with your environment variable values and apply the updated manifest to your cluster\. The following command completes this in one step\.

      ```
      cat dns.yaml | sed -e "s/REGION/$REGION/g" | sed -e "s/DNS_CLUSTER_IP/$DNS_CLUSTER_IP/g" | kubectl apply -f -
      ```

   1. Fetch the `coredns` pod name from your cluster\.

      ```
      COREDNS_POD=$(kubectl get pod -n kube-system -l eks.amazonaws.com/component=coredns \
      -o jsonpath='{.items[0].metadata.name}')
      ```

   1. Query the `coredns` pod to ensure that it's receiving requests\.

      ```
      kubectl get --raw /api/v1/namespaces/kube-system/pods/$COREDNS_POD:9153/proxy/metrics \
      | grep 'coredns_dns_request_count_total'
      ```
**Note**  
It might take several minutes for the expected output to return properly, depending on the rate of DNS requests in your cluster\.

      Expected output \(the number in red is the DNS request count total\):

      ```
      # HELP coredns_dns_request_count_total Counter of DNS requests made per zone, protocol and family.
      # TYPE coredns_dns_request_count_total counter
      coredns_dns_request_count_total{family="1",proto="udp",server="dns://:53",zone="."} 23
      ```

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   ```

   Output:

   ```
   coredns:v1.1.3
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.14:** `1.3.1`
   + **Kubernetes 1\.13:** `1.2.6`
   + **Kubernetes 1\.12:** `1.2.2`
   + **Kubernetes 1\.11:** `1.1.3`

   If your current `coredns` version doesn't match the recommendation for your cluster version, update the `coredns` deployment to use the recommended image with the following command, replacing the red text with your `coredns` version:

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
   coredns=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/coredns:v1.3.1
   ```

1. Scale down the `kube-dns` deployment to zero replicas\.

   ```
   kubectl scale -n kube-system deployment/kube-dns --replicas=0
   ```

1. Clean up the old `kube-dns` resources\.

   ```
   kubectl delete -n kube-system deployment/kube-dns serviceaccount/kube-dns configmap/kube-dns
   ```