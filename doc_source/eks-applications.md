# Workloads<a name="eks-applications"></a>

Your workloads are deployed in containers, which are deployed in pods in Kubernetes\. A pod includes one or more containers\. Typically, one or more pods that provide the same service are deployed in a Kubernetes service\. Once you've deployed multiple pods that provide the same service, you can:
+ Vertically scale pods up or down with the Kubernetes [Vertical Pod Autoscaler](vertical-pod-autoscaler.md)\.
+ Horizontally scale the number of pods needed to meet demand up or down with the Kubernetes [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md)\.
+ Create an external \(for internet\-accessible pods\) or an internal \(for private pods\) [load balancer](load-balancing.md) to balance network traffic across pods\. The load balancer routes traffic at Layer 4 of the OSI model\.
+ Create an [Application load balancing on Amazon EKS](alb-ingress.md) to balance application traffic across pods\. The application load balancer routes traffic at Layer 7 of the OSI model\.
+ If you're new to Kubernetes, this topic helps you [Deploy a sample Linux workload](sample-deployment.md)\.