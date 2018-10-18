# Installing Calico on Amazon EKS<a name="calico"></a>

[Project Calico](https://www.projectcalico.org/) is a network policy engine for Kubernetes\. With Calico network policy enforcement, you can implement network segmentation and tenant isolation, which is useful in multi\-tenant environments where you need to isolate tenants from each other or when you want to create separate environments for development, staging, and production\. Network policies are similar to AWS security groups in that you can create network ingress and egress rules, but instead of assigning instances to a security group, you assign network policies to pods using pod selectors and labels\. The following procedure shows you how to install Calico on your Amazon EKS cluster\. 

**To install Calico on your Amazon EKS cluster**

1. Apply the Calico manifest from the [`aws/amazon-vpc-cni-k8s` GitHub project](https://github.com/aws/amazon-vpc-cni-k8s)\. This manifest creates daemon sets in the `kube-system` namespace\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.2/config/v1.2/calico.yaml
   ```

1. Watch the `kube-system` daemon sets and wait for the `calico-node` daemon set to have the `DESIRED` number of pods in the `READY` state\. When this happens, Calico is working\.

   ```
   kubectl get daemonset calico-node --namespace=kube-system
   ```

   Output:

   ```
   NAME          DESIRED   CURRENT   READY     UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
   calico-node   3         3         3         3            3           <none>          38s
   ```

## Stars Policy Demo<a name="calico-stars-demo"></a>

This section walks through the [Stars Policy Demo](https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/) provided by the Project Calico documentation\. The demo creates a front\-end, back\-end, and client service on your Amazon EKS cluster\. The demo also creates a visual management UI that shows the available ingress and egress paths between each service\. 

Before you create any network policies, all services can communicate bidirectionally\. After you apply the network policies, you can see that the client can only communicate with the front\-end service, and the backend can only communicate with the frontend\.

**To run the Stars Policy demo**

1. Apply the front\-end, back\-end, client, and management UI services\.

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/manifests/00-namespace.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/manifests/01-management-ui.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/manifests/02-backend.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/manifests/03-frontend.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/manifests/04-client.yaml
   ```

1. Wait for all of the pods to reach the `Running` status:

   ```
   kubectl get pods --all-namespaces --watch
   ```

1. To connect to the management UI, forward your local port 9001 to the `management-ui` service running on your cluster:

   ```
   kubectl port-forward service/management-ui -n management-ui 9001
   ```

1. Open a browser on your local system and point it to [http://localhost:9001/](http://localhost:9001/)\. You should see the management UI\. The **C** node is the client service, the **F** node is the front\-end service, and the **B** node is the back\-end service\. Each node has full communication access to all other nodes \(as indicated by the bold, colored lines\)\.  
![\[Open network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-default.png)

1. Apply the following network policies to isolate the services from each other:

   ```
   kubectl apply -n stars -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/default-deny.yaml
   kubectl apply -n client -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/default-deny.yaml
   ```

1. Refresh your browser, and you can see that the management UI can no longer reach any of the nodes, so they don't show up in the UI\.

1. Apply the following network policies to allow the management UI to access the services:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/allow-ui.yaml
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/allow-ui-client.yaml
   ```

1. Refresh your browser, and you can see that the management UI can reach the nodes again, but the nodes cannot communicate with each other\.  
![\[UI access network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-no-traffic.png)

1. Apply the following network policy to allow traffic from the front\-end service to the back\-end service:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/backend-policy.yaml
   ```

1. Apply the following network policy to allow traffic from the `client` namespace to the front\-end service:

   ```
   kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/tutorials/stars-policy/policies/frontend-policy.yaml
   ```  
![\[Final network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-final.png)

1. \(Optional\) When you are done with the demo, you can delete its resources with the following command:

   ```
   kubectl delete ns client stars management-ui
   ```