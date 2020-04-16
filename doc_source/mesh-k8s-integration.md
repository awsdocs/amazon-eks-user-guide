# Tutorial: Configure App Mesh integration with Kubernetes<a name="mesh-k8s-integration"></a>

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that makes it easy to monitor and control services\. App Mesh standardizes how your services communicate, giving you end\-to\-end visibility and helping to ensure high availability for your applications\.

App Mesh gives you consistent visibility and network traffic controls for every service in an application\. For more information, see the [App Mesh User Guide](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html)\.

When you integrate AWS App Mesh with Kubernetes, you manage App Mesh resources, such as virtual services and virtual nodes, through Kubernetes\. You also automatically add the App Mesh sidecar container images to Kubernetes pod specifications\. This tutorial guides you through the installation of the following open source components that enable this integration:
+ **App Mesh controller for Kubernetes** – The controller is accompanied by the deployment of three Kubernetes custom resource definitions: `mesh`, `virtual service`, and `virtual node`\. The controller watches for creation, modification, and deletion of the custom resources and makes changes to the corresponding App Mesh `[mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html)`, `[virtual service](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html)` \(including `[virtual router](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html)` and `[route](https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html)`\), and `[virtual node](https://docs.aws.amazon.com/app-mesh/latest/userguide/irtual_nodes.html)` resources through the App Mesh API\. To learn more or contribute to the controller, see the [GitHub project](https://github.com/aws/aws-app-mesh-controller-for-k8s)\.
+  **App Mesh sidecar injector for Kubernetes** – The injector installs as a webhook and injects the following containers into Kubernetes pods that are running in specific, labeled namespaces\. To learn more or contribute, see the [GitHub project](https://github.com/aws/aws-app-mesh-inject)\.
  + **App Mesh Envoy proxy** –Envoy uses the configuration defined in the App Mesh control plane to determine where to send your application traffic\.\. 
  + **App Mesh proxy route manager **– The route manager sets up a pod’s network namespace with `iptables` rules that route ingress and egress traffic through Envoy\.


|  | 
| --- |
| The features discussed in this topic are available as an open\-source beta\. This means that these features are well tested\. Support for the features will not be dropped, though details may change\. If the schema or schematics of a feature changes, instructions for migrating to the next version will be provided\. This migration may require deleting, editing, and re\-creating Kubernetes API objects\. | 

## Prerequisites<a name="mesh-k8s-integration-prerequisites"></a>
+ An existing understanding of App Mesh concepts\. For more information, see [What is AWS App Mesh\.](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html)
+ An existing Kubernetes cluster running version 1\.13 or later\. If you don't have an existing cluster, you can deploy one using the [Getting Started with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) guide\. 
+ The AWS CLI version 1\.18\.16 or later installed\. To install or upgrade the, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\. 
+ A `kubectl` client that is configured to communicate with your Kubernetes cluster\. If you're using Amazon Elastic Kubernetes Service, you can use the instructions for installing `[kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)` and configuring a `[kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)` file\.
+ Helm version 3\.0 or later installed\. If you don't have Helm installed, you can install it by completing the instructions in [Using Helm with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/helm.html)\.

## Step 1: Install the integration components<a name="install-controller"></a>

Install the integration components one time to each cluster that hosts pods that you want to use with App Mesh

**To install the integration components**

1. Add the `eks-charts` repository to Helm\.

   ```
   helm repo add eks https://aws.github.io/eks-charts
   ```

1. Install the App Mesh Kubernetes custom resource definitions \(CRD\)\.

   ```
   kubectl apply -k github.com/aws/eks-charts/stable/appmesh-controller/crds?ref=master
   ```

1. Create a Kubernetes namespace for the controller\.

   ```
   kubectl create ns appmesh-system
   ```

1. Set the following variables\. Replace `cluster-name` and `region-code` with the values for your existing cluster\.

   ```
   export CLUSTER_NAME=cluster-name
   export AWS_REGION=region-code
   ```

1. Create an OpenID Connect \(OIDC\) identity provider for your cluster\. If you don't have `eksctl` installed, you can install it with the instructions in [Installing or Upgrading `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)\. If you'd prefer to create the provider using the console, see [Enabling IAM Roles for Service Accounts on your Cluster](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)\.

   ```
   eksctl utils associate-iam-oidc-provider \
       --region=$AWS_REGION \
       --cluster $CLUSTER_NAME \
       --approve
   ```

1. Create an IAM role, attach the [AWSAppMeshFullAccess](https://console.aws.amazon.com/iam/home?#policies/arn:aws:iam::aws:policy/AWSAppMeshFullAccess$jsonEditor) and [AWSCloudMapFullAccess](https://console.aws.amazon.com/iam/home?#policies/arn:aws:iam::aws:policy/AWSCloudMapFullAccess$jsonEditor) AWS managed policies to it, and bind it to the `appmesh-controller` Kubernetes service account\. The role enables the controller to add, remove, and change App Mesh resources\.
**Note**  
The command creates an AWS IAM role with an auto\-generated name\. You are not able to specify the IAM role name that is created\.

   ```
   eksctl create iamserviceaccount \
       --cluster $CLUSTER_NAME \
       --namespace appmesh-system \
       --name appmesh-controller \
       --attach-policy-arn  arn:aws:iam::aws:policy/AWSCloudMapFullAccess,arn:aws:iam::aws:policy/AWSAppMeshFullAccess \
       --override-existing-serviceaccounts \
       --approve
   ```

   If you prefer to create the service account using the AWS Management Console or AWS CLI, see [Creating an IAM Role and Policy for your Service Account](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html#create-service-account-iam-role)\. If you use the AWS Management Console or AWS CLI to create the account, you also need to map the role to a Kubernetes service account\. For more information, see [Specifying an IAM Role for your Service Account](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)\. 

1. Deploy the App Mesh controller\. For a list of all configuration options, see [Configuration](https://github.com/aws/eks-charts/blob/master/stable/appmesh-controller/README.md#configuration) on GitHub\.

   ```
   helm upgrade -i appmesh-controller eks/appmesh-controller \
       --namespace appmesh-system \
       --set region=$AWS_REGION \
       --set serviceAccount.create=false \
       --set serviceAccount.name=appmesh-controller
   ```

1. Confirm that the controller version is `v0.3.0` or later\. You can view the [change log](https://github.com/aws/aws-app-mesh-controller-for-k8s/blob/master/CHANGELOG.md) on GitHub\.

   ```
   kubectl get deployment -n appmesh-system appmesh-controller -o json  | jq -r ".spec.template.spec.containers[].image" | cut -f2 -d ':'
   ```

1. Install the App Mesh sidecar injector and create a mesh with the name *my\-mesh*\. For a list of all configuration options, see [Configuration](https://github.com/aws/eks-charts/tree/master/stable/appmesh-inject#configuration) on GitHub\. 

   ```
   helm upgrade -i appmesh-inject eks/appmesh-inject \
       --namespace appmesh-system \
       --set mesh.name=my-mesh \
       --set mesh.create=true
   ```
**Note**  
If you view the log for the running container, you may see a line that includes the following text, which can be safely ignored\.  

   ```
   Neither --kubeconfig nor --master was specified. Using the inClusterConfig. This might not work.
   ```

## Step 2: Deploy App Mesh resources<a name="configure-mesh"></a>

When you deploy an application in Kubernetes, you also create the Kubernetes custom resources so that the controller can create the corresponding App Mesh resources\.

**To deploy App Mesh resources**

1. Create a Kubernetes namespace to deploy App Mesh resources to\.

   ```
   kubectl create ns my-app-1
   ```

1. Create an App Mesh virtual node\. A virtual node acts as a logical pointer to a Kubernetes deployment\.

   1. Create a file named `virtual-node.yaml` with the following contents\. The file will be used to create an App Mesh virtual node named `my-service-a` in the *`my-app-1`* namespace\. The virtual node represents a Kubernetes service that is created in a later step\. The virtual node will communicate to a backend virtual service named *`my-service-b.my-app-1.svc.cluster.local`*, but it is not created in this tutorial\.

      ```
      apiVersion: appmesh.k8s.aws/v1beta1
      kind: VirtualNode
      metadata:
        name: my-service-a
        namespace: my-app-1
      spec:
        meshName: my-mesh
        listeners:
          - portMapping:
              port: 9000
              protocol: http
        serviceDiscovery:
          dns:
            hostName: my-service-a.my-app-1.svc.cluster.local
        backends:
          - virtualService:
              virtualServiceName: my-service-b.my-app-1.svc.cluster.local
      ```

      Virtual nodes have capabilities, such as end\-to\-end encryption and health checks, that aren't covered in this tutorial\. For more information, see [Virtual nodes](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html)\. To see all available settings for a virtual node that you can set in the preceding spec, run the following command\.

      ```
      aws appmesh create-virtual-node --generate-cli-skeleton yaml-input
      ```

   1. Deploy the virtual node\.

      ```
      kubectl apply -f virtual-node.yaml
      ```

   1. View all of the resources in the `my-app-1` namespace\.

      ```
      kubectl -n my-app-1 get all
      ```

      Output

      ```
      NAME                           AGE
      mesh.appmesh.k8s.aws/my-mesh   17m
      
      NAME                                            AGE
      virtualnode.appmesh.k8s.aws/my-service-a   16m
      ```

      This output shows the mesh and the virtual node that exist in the *`my-app-1`* namespace\.

   1.  Confirm that the virtual node was created in App Mesh\.
**Note**  
Even though the name of the virtual node created in Kubernetes is `my-service-a`, the name of the virtual node created in App Mesh is `my-service-a-my-app-1`\. The controller appends the Kubernetes namespace name to the App Mesh virtual node name when it creates the App Mesh resource\. The namespace name is added because in Kubernetes you can create virtual nodes with the same name in different namespaces, but in App Mesh a virtual node name must be unique within a mesh\.

      ```
      aws appmesh describe-virtual-node --mesh-name my-mesh --virtual-node-name my-service-a-my-app-1
      ```

      Output

      ```
      {
          "virtualNode": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualNode/my-service-a-my-app-1",
                  "createdAt": "2020-03-20T08:18:19.510000-05:00",
                  "lastUpdatedAt": "2020-03-20T08:18:19.510000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "backends": [
                      {
                          "virtualService": {
                              "virtualServiceName": "my-service-b.my-app-1.svc.cluster.local"
                          }
                      }
                  ],
                  "listeners": [
                      {
                          "portMapping": {
                              "port": 9000,
                              "protocol": "http"
                          }
                      }
                  ],
                  "serviceDiscovery": {
                      "dns": {
                          "hostname": "my-service-a.my-app-1.svc.cluster.local"
                      }
                  }
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualNodeName": "my-service-a-my-app-1"
          }
      }
      ```

      Note the value of `arn` in the preceding output\. You will use it in a later step\.

1. Create an App Mesh virtual service, virtual router, and route\. A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router\. Dependent services call your virtual service by its name\. The requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service\.

   1. Create a file named `virtual-service.yaml` with the following contents\. The file will be used to create a virtual service that uses a virtual router provider to route traffic to the virtual node named `my-service-a` that was created in the previous step\. The value for `name` is the fully qualified domain name \(FQDN\) of the actual Kubernetes service that this virtual service abstracts\. The service is created in [Step 3: Create or update services](#integration-update-services)\. The controller will create the App Mesh virtual service, virtual router, and route resources\. You can specify many more capabilities for your routes and use protocols other than `http`\. For more information, see the App Mesh [Virtual services](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html), [Virtual router](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html), and [Route](https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html) documentation\. 

      ```
      apiVersion: appmesh.k8s.aws/v1beta1
      kind: VirtualService
      metadata:
        name: my-service-a.my-app-1.svc.cluster.local
        namespace: my-app-1
      spec:
        meshName: my-mesh
        virtualRouter:
          name: my-service-a-virtual-router
          listeners:
            - portMapping:
                port: 9080
                protocol: http
        routes:
          - name: my-service-a-route
            http:
              match:
                prefix: /
              action:
                weightedTargets:
                  - virtualNodeName: my-service-a
                    weight: 1
      ```

      To see all available settings for a virtual service, virtual router, and route that you can set in the preceding spec, run any of the following commands\.

      ```
      aws appmesh create-virtual-service --generate-cli-skeleton yaml-input
      aws appmesh create-virtual-router --generate-cli-skeleton yaml-input
      aws appmesh create-route --generate-cli-skeleton yaml-input
      ```

   1. Create the virtual service\.

      ```
      kubectl apply -f virtual-service.yaml
      ```

   1. View the virtual service resource\.

      ```
      kubectl describe virtualservice my-service-a.my-app-1.svc.cluster.local -n my-app-1
      ```

      Abbreviated output

      ```
      Name:         my-service-a.my-app-1.svc.cluster.local
      Namespace:    my-app-1
      Labels:       <none>
      Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"appmesh.k8s.aws/v1beta1","kind":"VirtualService","metadata":{"annotations":{},"name":"my-service-a.my-app-1.svc.cluster.loc...
      API Version:  appmesh.k8s.aws/v1beta1
      Kind:         VirtualService
      ...
      Spec:
        Mesh Name:  my-mesh
        Routes:
          Http:
            Action:
              Weighted Targets:
                Virtual Node Name:  my-service-a
                Weight:             1
            Match:
              Prefix:  /
          Name:        my-service-a-route
        Virtual Router:
          Listeners:
            Port Mapping:
              Port:      9080
              Protocol:  http
          Name:          my-service-a-virtual-router
      Status:
        Conditions:
          Last Transition Time:  2020-03-20T13:24:37Z
          Status:                True
          Type:                  VirtualRouterActive
          Last Transition Time:  2020-03-20T13:24:37Z
          Status:                True
          Type:                  RoutesActive
          Last Transition Time:  2020-03-20T13:24:38Z
          Status:                True
          Type:                  VirtualServiceActive
      Events:                    <none>
      ```

   1. Confirm that the virtual service was created in your mesh\. The Kubernetes controller did not append the Kubernetes namespace name to the App Mesh virtual service name when it created the virtual service in App Mesh because the virtual service's name is a unique FQDN\.

      ```
      aws appmesh describe-virtual-service --virtual-service-name my-service-a.my-app-1.svc.cluster.local --mesh-name=my-mesh
      ```

      Output

      ```
      {
          "virtualService": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualService/my-service-a.my-app-1.svc.cluster.local",
                  "createdAt": "2020-03-20T08:24:37.434000-05:00",
                  "lastUpdatedAt": "2020-03-20T08:24:37.434000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "provider": {
                      "virtualRouter": {
                          "virtualRouterName": "my-service-a-virtual-router-my-app-1"
                      }
                  }
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualServiceName": "my-service-a.my-app-1.svc.cluster.local"
          }
      }
      ```

   1. Confirm that the virtual router was created in your mesh\.
**Note**  
Though the virtual router created in Kubernetes is `my-service-a-virtual-router`, the name of the virtual router created in App Mesh is `my-service-a-virtual-router-my-app-1`\.

      ```
      aws appmesh describe-virtual-router --virtual-router-name my-service-a-virtual-router-my-app-1 --mesh-name=my-mesh
      ```

      Output

      ```
      {
          "virtualRouter": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router-my-app-1",
                  "createdAt": "2020-03-20T08:24:37.285000-05:00",
                  "lastUpdatedAt": "2020-03-20T08:24:37.285000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "listeners": [
                      {
                          "portMapping": {
                              "port": 9080,
                              "protocol": "http"
                          }
                      }
                  ]
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualRouterName": "my-service-a-virtual-router-my-app-1"
          }
      }
      ```

   1. Confirm that the route was created in your mesh\. The Kubernetes controller did not append the Kubernetes namespace name to the App Mesh route name when it created the route in App Mesh because route names are unique to a virtual router\.

      ```
      aws appmesh describe-route --route-name my-service-a-route --virtual-router-name my-service-a-virtual-router-my-app-1 --mesh-name my-mesh
      ```

      Output

      ```
      {
          "route": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router-my-app-1/route/my-service-a-route",
                  "createdAt": "2020-03-20T08:24:37.331000-05:00",
                  "lastUpdatedAt": "2020-03-20T08:24:37.331000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "routeName": "my-service-a-route",
              "spec": {
                  "httpRoute": {
                      "action": {
                          "weightedTargets": [
                              {
                                  "virtualNode": "my-service-a-my-app-1",
                                  "weight": 1
                              }
                          ]
                      },
                      "match": {
                          "prefix": "/"
                      }
                  }
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualRouterName": "my-service-a-virtual-router-my-app-1"
          }
      }
      ```

## Step 3: Create or update services<a name="integration-update-services"></a>

Any pods that you want to use with App Mesh must have the App Mesh sidecar containers added to them\. The injector automatically adds the sidecar containers to any pod deployed into a namespace that you specify\.

**To create or update services**

1. To enable sidecar injection for the namespace, label the namespace\.

   ```
   kubectl label namespace my-app-1 appmesh.k8s.aws/sidecarInjectorWebhook=enabled
   ```

1.  Enable proxy authorization\. We recommend that you enable each Kubernetes deployment to stream the configuration for its own App Mesh virtual node\.

   1. Create a file named `proxy-auth.json` with the following contents\. 

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": "appmesh:StreamAggregatedResources",
                  "Resource": [
                      "arn:aws:appmesh:region-code:111122223333:mesh/my-mesh/virtualNode/my-service-a-my-app-1"
                  ]
              }
          ]
      }
      ```

   1. Create the policy\.

      ```
      aws iam create-policy --policy-name my-policy --policy-document file://proxy-auth.json
      ```

      Note the ARN of the policy in the output returned\. You'll use it in the next step\.

   1. Create an IAM role, attach the policy you created in the previous step to it, create a Kubernetes service account and bind the policy to the Kubernetes service account\. The role enables the controller to add, remove, and change App Mesh resources\.

      ```
      eksctl create iamserviceaccount \
          --cluster $CLUSTER_NAME \
          --namespace my-app-1 \
          --name my-service-a \
          --attach-policy-arn  arn:aws:iam::111122223333:policy/my-policy \
          --override-existing-serviceaccounts \
          --approve
      ```

      If you prefer to create the service account using the AWS Management Console or AWS CLI, see [Creating an IAM Role and Policy for your Service Account](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html#create-service-account-iam-role)\. If you use the AWS Management Console or AWS CLI to create the account, you also need to map the role to a Kubernetes service account\. For more information, see [Specifying an IAM Role for your Service Account](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)\. 

1. Create a Kubernetes service and deployment\. If you have an existing deployment that you want to use with App Mesh, you need to update its namespace to *`my-app-1`* so that the sidecar containers are automatically added to the pods and the pods are redeployed\.

   1. Create a file named `example-service.yaml` with the following contents\.

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: my-service-a
        namespace: my-app-1
        labels:
          app: nginx
      spec:
        selector:
          app: nginx
        ports:
          - protocol: TCP
            port: 80
            targetPort: 9376
      ---
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-service-a
        namespace: my-app-1
        labels:
          app: nginx
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: nginx
        template:
          metadata:
            labels:
              app: nginx
          spec:
            serviceAccountName: my-service-a
            containers:
            - name: nginx
              image: nginx:1.14.2
              ports:
              - containerPort: 80
      ```

      You can override the default behavior of the injector for individual pods\. For example, notice in the preceding spec that the name of the deployment is *`my-service-a`*\. By default, this name must be the same as the name of the virtual node that you created in [Step 2: Deploy App Mesh resources](#configure-mesh)\. If you want the name of the virtual node to be different than the name of the deployment, then you must add an annotation to your spec for the `virtualNode` setting\. To familiarize yourself with the settings that you can override, see [Default behavior and how to override](https://github.com/aws/aws-app-mesh-inject/blob/master/README.md#default-behavior-and-how-to-override) on GitHub\.

   1. Deploy the service\.

      ```
      kubectl apply -f example-service.yaml
      ```

   1. View the service and deployment\.

      ```
      kubectl -n my-app-1 get pods
      ```

      Output

      ```
      NAME                            READY   STATUS    RESTARTS   AGE
      my-service-a-658c47c864-g9p9l   2/2     Running   0          26s
      my-service-a-658c47c864-grn8w   2/2     Running   0          26s
      my-service-a-658c47c864-lc5qk   2/2     Running   0          26s
      ```

   1. View the details for one of the pods that was deployed\.

      ```
      kubectl -n my-app-1 describe pod my-service-a-7fd6966748-79674
      ```

      Abbreviated output

      ```
      Name:           my-service-a-658c47c864-g9p9l
      Namespace:      my-app-1
      ...
      Init Containers:
        proxyinit:
          Container ID:   docker://5f45b51566681be12eb851d48a47199e5a09d8661a16296bca826c93d3703ae6
          Image:          111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2
          Image ID:       docker-pullable://111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager@sha256:1111111111111111111111111111111111111111111111111111111111111111
          Port:           <none>
          Host Port:      <none>
          State:          Terminated
            Reason:       Completed
            Exit Code:    0
            Started:      Fri, 20 Mar 2020 08:37:05 -0500
            Finished:     Fri, 20 Mar 2020 08:37:06 -0500
          Ready:          True
          Restart Count:  0
          Requests:
            cpu:     10m
            memory:  32Mi
          Environment:
            APPMESH_START_ENABLED:         1
            APPMESH_IGNORE_UID:            1337
            APPMESH_ENVOY_INGRESS_PORT:    15000
            APPMESH_ENVOY_EGRESS_PORT:     15001
            APPMESH_APP_PORTS:             80
            APPMESH_EGRESS_IGNORED_IP:     169.254.169.254
            APPMESH_EGRESS_IGNORED_PORTS:  22
            AWS_ROLE_ARN:                  arn:aws:iam::111122223333:role/eksctl-appmesh-1-addon-iamserviceaccount-my-Role1-MVK5HIHHL4WT
            AWS_WEB_IDENTITY_TOKEN_FILE:   /var/run/secrets/eks.amazonaws.com/serviceaccount/token
          Mounts:
            /var/run/secrets/eks.amazonaws.com/serviceaccount from aws-iam-token (ro)
            /var/run/secrets/kubernetes.io/serviceaccount from my-service-a-token-s29ls (ro)
      Containers:
        nginx:
          Container ID:   docker://022c01578fa71129213a0de9df0748ff410f468739edc872bb1888843020bd88
          Image:          nginx:1.14.2
          Image ID:       docker-pullable://nginx@sha256:1111111111111111111111111111111111111111111111111111111111111111
          Port:           80/TCP
          Host Port:      0/TCP
          State:          Running
            Started:      Fri, 20 Mar 2020 08:37:11 -0500
          Ready:          True
          Restart Count:  0
          Environment:
            AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/eksctl-appmesh-1-addon-iamserviceaccount-my-Role1-MVK5HIHHL4WT
            AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
          Mounts:
            /var/run/secrets/eks.amazonaws.com/serviceaccount from aws-iam-token (ro)
            /var/run/secrets/kubernetes.io/serviceaccount from my-service-a-token-s29ls (ro)
        envoy:
          Container ID:   docker://742934a0722734762890ae925a4c143b739ba114ab33acf14919c4069773f492
          Image:          840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.12.2.1-prod
          Image ID:       docker-pullable://840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy@sha256:1111111111111111111111111111111111111111111111111111111111111111
          Port:           9901/TCP
          Host Port:      0/TCP
          State:          Running
            Started:      Fri, 20 Mar 2020 08:37:18 -0500
          Ready:          True
          Restart Count:  0
          Requests:
            cpu:     10m
            memory:  32Mi
          Environment:
            APPMESH_VIRTUAL_NODE_NAME:    mesh/my-mesh/virtualNode/my-service-a-my-app-1
            APPMESH_PREVIEW:              0
            ENVOY_LOG_LEVEL:              info
            AWS_REGION:                   us-west-2
            AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/eksctl-appmesh-1-addon-iamserviceaccount-my-Role1-MVK5HIHHL4WT
            AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
          Mounts:
            /var/run/secrets/eks.amazonaws.com/serviceaccount from aws-iam-token (ro)
            /var/run/secrets/kubernetes.io/serviceaccount from my-service-a-token-s29ls (ro)
      ...
      ```

      In the preceding output, you can see that the `proxyinit` and `envoy` containers were added to the pod\.

## Step 4: Clean up<a name="remove-integration"></a>

Remove all of the example resources created in this tutorial\. The controller also removes the resources that were created in App Mesh\.

```
kubectl delete namespace my-app-1
```

\(Optional\) You can remove the Kubernetes integration components\.

```
helm delete appmesh-controller -n appmesh-system
helm delete appmesh-inject -n appmesh-system
```