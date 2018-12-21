# Installing CoreDNS<a name="coredns"></a>

New Amazon EKS clusters created with Kubernetes version 1\.11 ship with [CoreDNS](https://coredns.io/) as the default DNS and service discovery provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to 1\.11, and you would like to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\.

You can check to see if your cluster is already running CoreDNS with the following command:

```
kubectl get pod -n kube-system -l k8s-app=kube-dns
```

If the output shows `coredns` in the pod names, then you are already running CoreDNS in your cluster\. If not, use the following procedure to update your DNS and service discovery provider to CoreDNS\.

**To install CoreDNS on an updated Amazon EKS cluster**

1. Add the `{"eks.amazonaws.com/component": "kube-dns"}` selector to the `kube-dns` deployment for your cluster \(this is to prevent the two DNS deployments from competing for control of the same set of labels\)\.

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
      curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-12-10/dns.yaml
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

   1. Query the `coredns` pod to ensure that it is receiving requests\.

      ```
      kubectl get --raw /api/v1/namespaces/kube-system/pods/$COREDNS_POD:9153/proxy/metrics \
      | grep 'coredns_dns_request_count_total'
      ```
**Note**  
It may take several minutes for the expected output to return properly, depending on the rate of DNS requests in your cluster\.

      Expected output \(the number in red is the DNS request count total\):

      ```
      # HELP coredns_dns_request_count_total Counter of DNS requests made per zone, protocol and family.
      # TYPE coredns_dns_request_count_total counter
      coredns_dns_request_count_total{family="1",proto="udp",server="dns://:53",zone="."} 23
      ```

1. Scale down the `kube-dns` deployment to 0 replicas\.

   ```
   kubectl  scale -n kube-system deployment/kube-dns --replicas=0
   ```

1. Clean up the old `kube-dns` resources\.

   ```
   kubectl delete -n kube-system deployment/kube-dns serviceaccount/kube-dns configmap/kube-dns
   ```