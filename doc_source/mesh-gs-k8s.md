# Getting Started with AWS App Mesh and Kubernetes<a name="mesh-gs-k8s"></a>

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that makes it easy to monitor and control microservices\. App Mesh standardizes how your microservices communicate, giving you end\-to\-end visibility and helping to ensure high\-availability for your applications\.

App Mesh gives you consistent visibility and network traffic controls for every microservice in an application\. For more information, see the [AWS App Mesh User Guide](https://docs.aws.amazon.com//app-mesh/latest/userguide/)\.

This topic helps you to use AWS App Mesh with an existing microservice application running on Amazon EKS or Kubernetes on Amazon EC2\.

## Prerequisites<a name="mesh-gs-k8s-prerequisites"></a>

App Mesh supports microservice applications that use service discovery naming for their components\. To use this getting started guide, you must have a microservice application running on Amazon EKS or Kubernetes on AWS\.

Kubernetes `kube-dns` and `coredns` are supported\. For more information, see [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) in the Kubernetes documentation\.

## Step 1: Create Your Service Mesh<a name="mesh-gs-k8s-create-mesh"></a>

A service mesh is a logical boundary for network traffic between the services that reside within it\. For more information, see [Service Meshes](https://docs.aws.amazon.com//app-mesh/latest/userguide/meshes.html) in the *AWS App Mesh User Guide*\.

After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh\.

**To create a new service mesh with the AWS Management Console**

1. Open the App Mesh console at [https://console\.aws\.amazon\.com/appmesh/](https://console.aws.amazon.com/appmesh/)\.

1. Choose **Create mesh**\.

1. For **Mesh name**, specify a name for your service mesh\.

1. Choose **Create mesh** to finish\.

## Step 2: Create Your Virtual Nodes<a name="mesh-gs-k8s-create-virtual-nodes"></a>

A virtual node acts as a logical pointer to a particular task group, such as a Kubernetes deployment\. For more information, see [Virtual Nodes](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_nodes.html) in the *AWS App Mesh User Guide*\.

When you create a virtual node, you must specify the DNS service discovery hostname for your task group\. Any inbound traffic that your virtual node expects should be specified as a *listener*\. Any outbound traffic that your virtual node expects to reach should be specified as a *backend*\.

You must create virtual nodes for each microservice in your application\.

**To create a virtual node in the AWS Management Console\.**

1. Choose the mesh that you created in the previous steps\.

1. Choose **Virtual nodes** in the left navigation\.

1. Choose **Create virtual node**\.

1. For **Virtual node name**, choose a name for your virtual node\.

1. For **Service discovery method**, choose **DNS** for services that use DNS service discovery and then specify the hostname for **DNS hostname**\. Otherwise, choose **None** if your virtual node doesn't expect any ingress traffic\.

1. To specify any backends \(for egress traffic\) for your virtual node, or to configure inbound and outbound access logging information, choose **Additional configuration**\.

   1. To specify a backend, choose **Add backend** and enter a virtual service name or full for the virtual service that your virtual node communicates with\. Repeat this step until all of your virtual node backends are accounted for\.

   1. To configure logging, enter the HTTP access logs path that you want Envoy to use\. We recommend the `/dev/stdout` path so that you can use Docker log drivers to export your Envoy logs to a service such as Amazon CloudWatch Logs\.
**Note**  
Logs must still be ingested by an agent in your application and sent to a destination\. This file path only instructs Envoy where to send the logs\.

1. If your virtual node expects ingress traffic, specify a **Port** and **Protocol** for that **Listener**\.

1. If you want to configure health checks for your listener, ensure that **Health check enabled** is selected and then complete the following substeps\. If not, clear this check box\.

   1. For **Health check protocol**, choose to use an HTTP or TCP health check\.

   1. For **Health check port**, specify the port that the health check should run on\.

   1. For **Healthy threshold**, specify the number of consecutive successful health checks that must occur before declaring the listener healthy\.

   1. For **Health check interval**, specify the time period in milliseconds between each health check execution\.

   1. For **Path**, specify the destination path for the health check request\. This is required only if the specified protocol is HTTP\. If the protocol is TCP, this parameter is ignored\.

   1. For **Timeout period**, specify the amount of time to wait when receiving a response from the health check, in milliseconds\.

   1. For **Unhealthy threshold**, specify the number of consecutive failed health checks that must occur before declaring the listener unhealthy\.

1. Chose **Create virtual node** to finish\.

1. Repeat this procedure as necessary to create virtual nodes for each remaining microservice in your application\.

## Step 3: Create Your Virtual Routers<a name="mesh-gs-k8s-create-virtual-routers"></a>

Virtual routers handle traffic for one or more virtual services within your mesh\. After you create a virtual router, you can create and associate routes for your virtual router that direct incoming requests to different virtual nodes\. For more information, see [Virtual Routers](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_routers.html) in the *AWS App Mesh User Guide*\.

Create virtual routers for each microservice in your application\.

**Creating a virtual router in the AWS Management Console\.**

1. Choose **Virtual routers** in the left navigation\.

1. Choose **Create virtual router**\.

1. For **Virtual router name**, specify a name for your virtual router\. Up to 255 letters, numbers, hyphens, and underscores are allowed\.

1. For **Listener**, specify a **Port** and **Protocol** for your virtual router\.

1. Choose **Create virtual router** to finish\.

1. Repeat this procedure as necessary to create virtual routers for each remaining microservice in your application\.

## Step 4: Create Your Routes<a name="mesh-gs-k8s-create-routes"></a>

A route is associated with a virtual router, and it's used to match requests for a virtual router and distribute traffic accordingly to its associated virtual nodes\. For more information, see [Routes](https://docs.aws.amazon.com//app-mesh/latest/userguide/routes.html) in the *AWS App Mesh User Guide*\.

Create routes for each microservice in your application\.

**Creating a route in the AWS Management Console\.**

1. Choose **Virtual routers** in the left navigation\.

1. Choose the router that you want to associate a new route with\.

1. In the **Routes** table, choose **Create route**\.

1. For **Route name**, specify the name to use for your route\.

1. For **Route type**, choose the protocol for your route\.

1. For **Virtual node name**, choose the virtual node that this route will serve traffic to\.

1. For **Weight**, choose a relative weight for the route\. The total weight for all routes must be less than 100\.

1. To use HTTP path\-based routing, choose **Additional configuration** and then specify the path that the route should match\. For example, if your virtual service name is `my-service.local` and you want the route to match requests to `my-service.local/metrics`, your prefix should be `/metrics`\.

1. Choose **Create route** to finish\.

1. Repeat this procedure as necessary to create routes for each remaining microservice in your application\.

## Step 5: Create Your Virtual Services<a name="mesh-gs-k8s-create-virtual-services"></a>

A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router\. Dependent services call your virtual service by its `virtualServiceName`, and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service\. For more information, see [Virtual Services](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_services.html) in the *AWS App Mesh User Guide*\.

Create virtual services for each microservice in your application\.

**Creating a virtual service in the AWS Management Console\.**

1. Choose **Virtual services** in the left navigation\.

1. Choose **Create virtual service**\.

1. For **Virtual service name**, choose a name for your virtual service\. We recommend that you use the service discovery name of the real service that you're targeting \(such as `my-service.default.svc.cluster.local`\)\.

1. For **Provider**, choose the provider type for your virtual service:
   + If you want the virtual service to spread traffic across multiple virtual nodes, select **Virtual router** and then choose the virtual router to use from the drop\-down menu\.
   + If you want the virtual service to reach a virtual node directly, without a virtual router, select **Virtual node** and then choose the virtual node to use from the drop\-down menu\.
   + If you don't want the virtual service to route traffic at this time \(for example, if your virtual nodes or virtual router doesn't exist yet\), choose **None**\. You can update the provider for this virtual service later\.

1. Choose **Create virtual service** to finish\.

1. Repeat this procedure as necessary to create virtual services for each remaining microservice in your application\.

## Step 6: Updating Your Microservice Pod Specifications<a name="mesh-gs-k8s-update-microservices"></a>

After you have created your service mesh, virtual nodes, virtual routers, routes, and virtual services, you must update your microservices to be compatible with App Mesh\.

App Mesh vends the following custom container images that you must add to your Kubernetes pod specifications\.
+ App Mesh Envoy container image: `111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.9.1.0-prod`
+ App Mesh proxy route manager: `111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:latest`

The following is an example Kubernetes pod specification that you can merge with your existing application\. Substitute your mesh name and virtual node name for the `APPMESH_VIRTUAL_NODE_NAME` value, and a list of ports that your application listens on for the `APPMESH_APP_PORTS` value\. Substitute the Amazon EC2 instance AWS Region for the `AWS_REGION` value\.

Update each microservice pod specification in your application to include these containers, and then deploy the new specifications to update your microservices and start using App Mesh with your Kubernetes application\.

**Example Kubernetes pod spec**  

```
spec:
  containers:
    - name: envoy
      image: 111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.9.1.0-prod
      securityContext:
        runAsUser: 1337
      env:
        - name: "APPMESH_VIRTUAL_NODE_NAME"
          value: "mesh/meshName/virtualNode/virtualNodeName"
        - name: "ENVOY_LOG_LEVEL"
          value: "info"
        - name: "AWS_REGION"
          value: "aws_region_name"
  initContainers:
    - name: proxyinit
      image: 111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:latest
      securityContext:
        capabilities:
          add: 
            - NET_ADMIN
      env:
        - name: "APPMESH_START_ENABLED"
          value: "1"
        - name: "APPMESH_IGNORE_UID"
          value: "1337"
        - name: "APPMESH_ENVOY_INGRESS_PORT"
          value: "15000"
        - name: "APPMESH_ENVOY_EGRESS_PORT"
          value: "15001"
        - name: "APPMESH_APP_PORTS"
          value: "application_port_list"
        - name: "APPMESH_EGRESS_IGNORED_IP"
          value: "169.254.169.254"
```