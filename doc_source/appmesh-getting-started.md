# Getting Started with AWS App Mesh and Kubernetes<a name="appmesh-getting-started"></a>

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that helps you monitor and control microservices\. App Mesh standardizes how your microservices communicate, giving you end\-to\-end visibility into and helping to ensure high\-availability for your applications\. App Mesh gives you consistent visibility and network traffic controls for every microservice in an application\. For more information, see the [AWS App Mesh User Guide](https://docs.aws.amazon.com//app-mesh/latest/userguide/)\.

This topic helps you use AWS App Mesh with an actual microservice application that is running on Kubernetes\. You can either integrate Kubernetes with App Mesh resources by completing the steps in this topic or by installing the App Mesh Kubernetes integration components\. The integration components automatically complete the tasks in this topic for you, enabling you to integrate with App Mesh directly from Kubernetes\. For more information, see [Configure App Mesh Integration with Kubernetes](https://docs.aws.amazon.com/eks/latest/userguide/mesh-k8s-integration.html)\.

## Scenario<a name="scenario"></a>

To illustrate how to use App Mesh with Kubernetes, assume that you have an application with the following characteristics:
+ Includes two services named `serviceA` and `serviceB`\. 
+ Both services are registered to a namespace named `apps.local`\.
+ `ServiceA` communicates with `serviceB` over HTTP/2, port 80\.
+  You've already deployed version 2 of `serviceB` and registered it with the name `serviceBv2` in the `apps.local` namespace\.

You have the following requirements:
+ You want to send 75 percent of the traffic from `serviceA` to `serviceB` and 25 percent of the traffic to `serviceBv2` to ensure that `serviceBv2` is bug free before you send 100 percent of the traffic from `serviceA` to it\. 
+ You want to be able to easily adjust the traffic weighting so that 100 percent of the traffic goes to `serviceBv2` once it's proven to be reliable\. Once all traffic is being sent to to `serviceBv2`, you want to deprecate `serviceB`\.
+ You don't want to have to change any existing application code or service discovery registration for your actual services to meet the previous requirements\. 

To meet your requirements, you've decided to create an App Mesh service mesh with virtual services, virtual nodes, a virtual router, and a route\. After implementing your mesh, you update the pod specs for your services to use the Envoy proxy\. Once updated, your services communicate with each other through the Envoy proxy rather than directly with each other\.

## Prerequisites<a name="prerequisites"></a>

App Mesh supports microservice applications that are registered with a service discovery mechanism, such as DNS\. To use this getting started guide, we recommend that you have three existing services that are registered for service discovery\. You can create a service mesh and its resources even if the services don't exist, but you can't use the mesh until you have deployed actual services\.

If you don't already have Kubernetes running, then you can create an Amazon EKS cluster\. For more information, see [Getting Started with Amazon EKS using `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)\. If you don't already have some services running on Kubernetes, you can deploy a test application\. For more information, see [Launch a Guest Book Application](https://docs.aws.amazon.com/eks/latest/userguide/eks-guestbook.html)\.

The remaining steps assume that the actual services are named `serviceA`, `serviceB`, and `serviceBv2` and that all services are discoverable through a namespace named `apps.local`\.

## Step 1: Create a Mesh and Virtual Service<a name="create-mesh-and-virtual-service"></a>

A service mesh is a logical boundary for network traffic between the services that reside within it\. For more information, see [Service Meshes](https://docs.aws.amazon.com//app-mesh/latest/userguide/meshes.html) in the *AWS App Mesh User Guide*\. A virtual service is an abstraction of an actual service\. For more information, see [Virtual Services](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_services.html) in the *AWS App Mesh User Guide*\.

1. Open the App Mesh console first\-run wizard at [https://console\.aws\.amazon\.com/appmesh/get\-started](https://console.aws.amazon.com/appmesh/get-started)\.

1. For **Mesh name**, specify **apps**, since all of the services in the scenario are registered to the `apps.local` namespace\.

1. For **Virtual service name**, enter **serviceb\.apps\.local**, since the virtual service represents a service that is discoverable with that name, and you don't want to change your code to reference another name\. `ServiceA` from the scenario will be added in a later step\.

1. To continue, choose **Next**\.

## Step 2: Create a Virtual Node<a name="create-virtual-node"></a>

A virtual node acts as a logical pointer to an actual service\. For more information, see [Virtual Nodes](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_nodes.html) *in the AWS App Mesh User Guide*\.

1. For **Virtual node name**, enter **serviceB**, since one of the virtual nodes represents the actual service named `serviceB`\. 

1. For **Service discovery method**, choose `DNS` and specify the DNS\-registered hostname of the actual service that the virtual node represents, such as **serviceb\.apps\.local**\. Alternately, you can use AWS Cloud Map for service discovery\.

1. Based on the scenario, under **Listener**, specify **80** for **Port** and choose `http2` for **Protocol**\. Other protocols are also supported, as are health checks\.

1. To continue, choose **Next**\. You will create virtual nodes for `serviceA` and `serviceBv2` in a later step\.

## Step 3: Create a Virtual Router and Route<a name="create-virtual-router-and-route"></a>

Virtual routers route traffic for one or more virtual services within your mesh\. For more information, see [Virtual Routers](https://docs.aws.amazon.com//app-mesh/latest/userguide/virtual_routers.html) and [Routes](https://docs.aws.amazon.com//app-mesh/latest/userguide/routes.html) in the *AWS App Mesh User Guide*\.

1. For **Virtual router name,** enter **serviceB**\. Based on the scenario, `serviceB` doesn't initiate outbound communication with any other service\. Remember that the App Mesh virtual service named `serviceb.apps.local` that you created previously is an abstraction of your actual `serviceB`\. The virtual service named `serviceb.apps.local` will send traffic to the router\. 

1. Based on the scenario, under **Listener**, specify **80** for **Port** and choose `http2` for **Protocol**\. Other protocols are also supported\.

1. For **Route name**, enter **serviceB**\. 

1. For **Route type**, choose `http2`\.

1. For** Virtual node name**, select `serviceB` and enter **100** for **Weight**\. You'll change the weight in a later step once you've added the `serviceBv2` virtual node\. Though not covered in this guide, you can add additional filter criteria for the route and add a retry policy to cause the Envoy proxy to make multiple attempts to send traffic to a virtual node when it experiences a communication problem to a target\.

1. To continue, choose **Next**\.

## Step 4: Review and Create<a name="review-create"></a>

Review the settings against the previous instructions\. Choose **Edit** if you need to make any changes in any section\. Once you're satisfied with the settings, choose **Create mesh service**\.

## Step 5: Create Additional Resources<a name="create-additional-resources"></a>

To complete the scenario, you need to create two additional virtual nodes and one additional virtual service, and you need to modify the route that you created in a previous step\.

1. In the left navigation pane, select **Meshes**\.

1. Select the `apps` mesh that you created in a previous step\.

1. In the left navigation pane, select **Virtual nodes**\.

1. Choose **Create virtual node**\.

1. For **Virtual node name**, enter **serviceBv2**, for **Service discovery method**, choose `DNS`, and for **DNS hostname**, enter **servicebv2\.apps\.local**\.

1. For **Listener**, enter **80** for **Port** and select `http2` for **Protocol**\.

1. Choose **Create virtual node**\.

1. Choose **Create virtual node** again, and enter **serviceA** for the **Virtual node name**, for **Service discovery method**, choose `DNS`, and for **DNS hostname**, enter **servicea\.apps\.local**\.

1. Expand **Additional configuration**\.

1. Select **Add backend**\. Enter **serviceb\.apps\.local** since all outbound traffic from the `serviceA` virtual node is sent to the virtual service named `serviceb.apps.local`\. Though not covered in this guide, you can also specify a file path to write access logs to\.

1. Enter **80** for **Port**, choose `http2` for **Protocol**, and then choose **Create virtual node**\.

1. In the left navigation pane, select** Virtual routers** and then select the `serviceB` virtual router from the list\.

1. Under **Routes**, select the route named `ServiceB` that you created in a previous step, and choose **Edit**\.

1. Under **Virtual node name**, change the value of **Weight** for `serviceB` to **75**\.

1. Choose **Add target**, choose `serviceBv2` from the drop\-down list, and set the value of **Weight** to **25**\. Over time, you can continue to modify the weights until `serviceBv2` receives 100 percent of the traffic\. Once all traffic is sent to `serviceBv2`, you can deprecate the `serviceB` virtual node and actual service\. As you change weights, your code doesn't require any modification, because the `serviceb.apps.local` virtual service name doesn't change\.

1. Choose **Save**\.

1. In the left navigation pane, select** Virtual services** and then choose **Create virtual service**\.

1. Enter **servicea\.apps\.local** for **Virtual service name**, select `Virtual node` for **Provider**, select `serviceA` for **Virtual node**, and then choose **Create virtual service\.**

**Mesh summary**  
Before you created the service mesh, you had three actual services named `servicea.apps.local`, `serviceb.apps.local`, and `servicebv2.apps.local`\. In addition to the actual services, you now have a service mesh that contains the following resources that represent the actual services:
+ Two virtual services\. The proxy sends all traffic from the `servicea.apps.local` virtual service to the `serviceb.apps.local` virtual service through a virtual router\. 
+ Three virtual nodes named `serviceA`, `serviceB`, and `serviceBv2`\. The Envoy proxy uses the service discovery information configured for the virtual nodes to look up the IP addresses of the actual services\. 
+ One virtual router with one route that instructs the Envoy proxy to route 75 percent of inbound traffic to the `serviceB` virtual node and 25 percent of the traffic to the `serviceBv2` virtual node\. 

## Step 6: Update Microservices<a name="update-microservices"></a>

After creating your mesh, you need to complete the following tasks:
+ Authorize the Envoy proxy that you deploy with each  Kubernetes pod to read the configuration of one or more virtual nodes\. For more information about how to authorize the proxy, see [Proxy authorization](https://docs.aws.amazon.com//app-mesh/latest/userguide/proxy-authorization.html)\.
+ Update each of your existing Kubernetes pod specs to use the Envoy proxy\. 

App Mesh vends the following custom container images that you must add to your Kubernetes pod specifications:
+ App Mesh Envoy container image – `840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.11.2.0-prod`\. You can replace *us\-west\-2* with any Region that App Mesh is supported in\. For a list of supported regions, see [AWS Service Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#appmesh_region)\. Envoy uses the configuration defined in the App Mesh control plane to determine where to send your application traffic\. 

  You must use the App Mesh Envoy container image until the Envoy project team merges changes that support App Mesh\. For additional details, see the [GitHub roadmap issue](https://github.com/aws/aws-app-mesh-roadmap/issues/10)\.
+ App Mesh proxy route manager – `111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2`\. The route manager sets up a pod’s network namespace with `iptables` rules that route ingress and egress traffic through Envoy\.

Update each microservice pod specification in your application to include these containers, as shown in the following example\. Once updated, deploy the new specifications to update your microservices and start using App Mesh with your Kubernetes application\. The following example shows updating the `serviceB` pod specification, that aligns to the scenario\. To complete the scenario, you also need to update the `serviceBv2` and `serviceA` pod specifications by changing the values appropriately\. For your own applications, substitute your mesh name and virtual node name for the `APPMESH_VIRTUAL_NODE_NAME` value, and add a list of ports that your application listens on for the `APPMESH_APP_PORTS` value\. Substitute the Amazon EC2 instance AWS Region for the `AWS_REGION` value\.

**Example Kubernetes pod spec**  

```
spec:
  containers:
    - name: envoy
      image: 840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.11.2.0-prod
      securityContext:
        runAsUser: 1337
      env:
        - name: "APPMESH_VIRTUAL_NODE_NAME"
          value: "mesh/apps/virtualNode/serviceB"
        - name: "ENVOY_LOG_LEVEL"
          value: "info"
        - name: "AWS_REGION"
          value: "aws_region_name"
  initContainers:
    - name: proxyinit
      image: 111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2
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