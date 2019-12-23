# Tutorial: Configure App Mesh Integration with Kubernetes<a name="mesh-k8s-integration"></a>

When you use AWS App Mesh with Kubernetes, you manage App Mesh resources, such as virtual services and virtual nodes, that align to Kubernetes resources, such as services and deployments\. You also add the App Mesh sidecar container images to Kubernetes pod specifications\. This tutorial guides you through the installation of the following open source components that automatically complete these tasks for you when you work with Kubernetes resources:
+ **App Mesh controller for Kubernetes** – The controller is accompanied by the deployment of three Kubernetes custom resource definitions: `mesh`, `virtual service`, and `virtual node`\. The controller watches for creation, modification, and deletion of the custom resources and makes changes to the corresponding App Mesh `[mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html)`, `[virtual service](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html)` \(including `[virtual router](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html)` and `[route](https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html)`\), and `[virtual node](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html)` resources through the App Mesh API\. To learn more or contribute to the controller, see the [GitHub project](https://github.com/aws/aws-app-mesh-controller-for-k8s)\.
+  **App Mesh sidecar injector for Kubernetes** – The injector installs as a webhook and injects the [App Mesh sidecar container images](https://docs.aws.amazon.com/eks/latest/userguide/mesh-gs-k8s.html#mesh-gs-k8s-update-microservices) into Kubernetes pods running in specific, labeled namespaces\. To learn more or contribute, see the [GitHub project](https://github.com/aws/aws-app-mesh-inject)\.


|  | 
| --- |
| The features discussed in this topic are available as an open\-source beta\. This means that these features are well tested\. Support for the features will not be dropped, though details may change\. If the schema or schematics of a feature changes, instructions for migrating to the next version will be provided\. This migration may require deleting, editing, and re\-creating Kubernetes API objects\. | 

## Prerequisites<a name="mesh-k8s-integration-prerequisites"></a>

To use the controller and sidecar injector, you must have the following resources:
+ An existing Kubernetes cluster running version 1\.11 or later\. If you don't have an existing cluster, you can deploy one using the [Getting Started with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) guide\. 
+ A `kubectl` client that is configured to communicate with your Kubernetes cluster\. If you're using Amazon Elastic Kubernetes Service, you can use the instructions for installing `[kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)` and configuring a `[kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)` file\.
+  [jq](https://stedolan.github.io/jq/download/) and Open SSL installed\.

## Step 1: Install the Controller and Custom Resources<a name="install-controller"></a>

To install the controller and Kubernetes custom resource definitions, complete the following steps\.

1. The controller requires that your account and your Kubernetes worker nodes are able to work with App Mesh resources\. [Attach](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) the [AWSAppMeshFullAccess](https://console.aws.amazon.com/iam/home?region=us-west-2#/policies/arn:aws:iam::aws:policy/AWSAppMeshFullAccess$jsonEditor) policy to the role that is attached to your Kubernetes worker nodes\. If you are using a pod identity solution, make sure that the controller pod is bound to the policy\. 

1. To create the Kubernetes custom resources and launch the controller, download the following yaml file and apply it to your cluster with the following command\.

   ```
   curl https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/master/deploy/all.yaml | kubectl apply -f -
   ```

   A Kubernetes namespace named `appmesh-system` is created and a container running the controller is deployed into the namespace\.

1. Confirm that the controller is running with the following command\.

   ```
   kubectl rollout status deployment app-mesh-controller -n appmesh-system
   ```

   If the controller is running, the following output is returned\.

   ```
   deployment "app-mesh-controller" successfully rolled out
   ```

1. Confirm that the Kubernetes custom resources for App Mesh were created with the following command\.

   ```
   kubectl get crd
   ```

   If the custom resources were created, output similar to the following is returned\.

   ```
   NAME                               CREATED AT
   meshes.appmesh.k8s.aws             2019-05-08T14:17:26Z
   virtualnodes.appmesh.k8s.aws       2019-05-08T14:17:26Z
   virtualservices.appmesh.k8s.aws    2019-05-08T14:17:26Z
   ```

## Step 2: Install the Sidecar Injector<a name="install-injector"></a>

### <a name="installation"></a>

To install the sidecar injector, complete the following steps\. If you'd like to see the controller and injector in action, complete the steps in this section, but replace *`my-mesh`* in the first step with `color-mesh,` and then see [Deploy a Mesh Connected Service](deploy-mesh-connected-service.md)\.

1. Export the name of the mesh you want to create with the following command\. 

   ```
   export MESH_NAME=my-mesh
   ```
   
2. Export the region of the mesh you want to create with the following command\. 

   ```
   export MESH_REGION=<EKS_CLUSTER_REGION>
   ```

3. Download and execute the sidecar injector installation script with the following command\.

   ```
   curl https://raw.githubusercontent.com/aws/aws-app-mesh-inject/master/scripts/install.sh | bash
   ```

   A Kubernetes namespace named `appmesh-inject` was created and a container running the injector was deployed into the namespace\. If the injector successfully installed, the last several lines of the output returned are similar to the following text\.

   ```
   deployment.apps/aws-app-mesh-inject configured
   mutatingwebhookconfiguration.admissionregistration.k8s.io/aws-app-mesh-inject configured
   waiting for aws-app-mesh-inject to start
   deployment "aws-app-mesh-inject" successfully rolled out
   Mesh name has been set up
   App Mesh image has been set up
   The injector is ready
   ```

## Step 3: Configure App Mesh<a name="configure-app-mesh"></a>

When you deploy an application in Kubernetes, you also create the Kubernetes custom resources so that the controller can create the corresponding App Mesh resources\. Additionally, you must enable sidecar injection so that the [App Mesh sidecar container images](https://docs.aws.amazon.com/eks/latest/userguide/mesh-gs-k8s.html#mesh-gs-k8s-update-microservices) are deployed in each Kubernetes pod\. 

### Create Kubernetes Custom Resources<a name="custom-resources"></a>

You can deploy mesh, virtual service, and virtual node custom resources in Kubernetes, which then triggers the controller to create the corresponding resources in App Mesh through the App Mesh API\.

#### Create a Mesh<a name="mesh"></a>

When you create a mesh custom resource, you trigger the creation of an App Mesh mesh\. The mesh name that you specify must be the same as the mesh name you exported when you [installed the sidecar injector](#install-injector)\. If the mesh name that you specify already exists, a new mesh is not created\.

```
apiVersion: appmesh.k8s.aws/v1beta1
kind: Mesh
metadata:
  name: my-mesh
```

#### Create a Virtual Service<a name="virtual-service"></a>

When you create a virtual service custom resource, you trigger the creation of an App Mesh virtual service, virtual router, and one or more routes containing a route configuration\. The virtual service allows requests from one application in the mesh to be routed to a number of virtual nodes that make up a service\.

```
apiVersion: appmesh.k8s.aws/v1beta1
kind: VirtualService
metadata:
  name: my-svc-a
  namespace: my-namespace
spec:
  meshName: my-mesh
  routes:
    - name: route-to-svc-a
      http:
        match:
          prefix: /
        action:
          weightedTargets:
            - virtualNodeName: my-app-a
              weight: 1
```

#### Create a Virtual Node<a name="virtual-node"></a>

When you create a virtual node custom resource, you trigger the creation of an App Mesh virtual node\. The virtual node contains listener, back\-end, and service discovery configuration\.

```
apiVersion: appmesh.k8s.aws/v1beta1
kind: VirtualNode
metadata:
  name: my-app-a
  namespace: my-namespace
spec:
  meshName: my-mesh
  listeners:
    - portMapping:
        port: 9000
        protocol: http
  serviceDiscovery:
    dns:
      hostName: my-app-a.my-namespace.svc.cluster.local
  backends:
    - virtualService:
        virtualServiceName: my-svc-a
```

### Sidecar Injection<a name="sidecar-injection"></a>

You enable sidecar injection for a Kubernetes namespace\. When necessary, you can override the injector's default behavior for each pod you deploy in a Kubernetes namespace that you've enabled the injector for\.

#### Enable Sidecar Injection for a Namespace<a name="enable-sidecar"></a>

To enable the sidecar injector for a Kubernetes namespace, label the namespace with the following command\.

```
kubectl label namespace my-namespace appmesh.k8s.aws/sidecarInjectorWebhook=enabled
```

 The [App Mesh sidecar container images](https://docs.aws.amazon.com/eks/latest/userguide/mesh-gs-k8s.html#mesh-gs-k8s-update-microservices) will be automatically injected into each pod that you deploy into the namespace\.

#### Override Sidecar Injector Default Behavior<a name="default-behavior"></a>

To override the default behavior of the injector when deploying a pod in a namespace that you've enabled the injector for, add any of the following annotations to your pod spec\.
+ *appmesh\.k8s\.aws/mesh:* mesh\-name** – Add when you want to use a different mesh name than the one that you specified when you installed the injector\.
+ *appmesh\.k8s\.aws/ports: "*ports*"* – Specify particular ports when you don't want all of the container ports defined in a pod spec passed to the sidecars as application ports\.
+ *appmesh\.k8s\.aws/egressIgnoredPorts: *ports** – Specify a comma separated list of port numbers for outbound traffic that you want ignored\. By default all outbound traffic ports will be routed, except port 22 \(SSH\)\.
+ *appmesh\.k8s\.aws/virtualNode: *virtual\-node\-name** – Specify your own name if you don't want the virtual node name passed to the sidecars to be `<deployment name>--<namespace>`\.
+  *appmesh\.k8s\.aws/sidecarInjectorWebhook: disabled* – Add when you don't want the injector enabled for a pod\.

```
apiVersion: appmesh.k8s.aws/v1beta1
kind: Deployment
spec:
    metadata:
      annotations:
        appmesh.k8s.aws/mesh: my-mesh2
        appmesh.k8s.aws/ports: "8079,8080"
        appmesh.k8s.aws/egressIgnoredPorts: "3306"
        appmesh.k8s.aws/virtualNode: my-app
        appmesh.k8s.aws/sidecarInjectorWebhook: disabled
```

## Step 4: Remove Integration Components \(Optional\)<a name="remove-integration"></a>

If you need to remove the Kubernetes integration components, run the following commands\.

```
kubectl delete crd meshes.appmesh.k8s.aws
kubectl delete crd virtualnodes.appmesh.k8s.aws
kubectl delete crd virtualservices.appmesh.k8s.aws
kubectl delete namespace appmesh-system
kubectl delete namespace appmesh-inject
```
