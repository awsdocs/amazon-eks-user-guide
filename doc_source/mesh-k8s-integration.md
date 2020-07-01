# Tutorial: Configure App Mesh integration with Kubernetes<a name="mesh-k8s-integration"></a>

When you integrate AWS App Mesh with Kubernetes using the App Mesh controller for Kubernetes, you manage App Mesh resources, such as meshes, virtual services, virtual nodes, virtual routers, and routes through Kubernetes\. You also automatically add the App Mesh sidecar container images to Kubernetes pod specifications\. This tutorial guides you through the installation of the App Mesh controller for Kubernetes to enable this integration\.

The controller is accompanied by the deployment of the following Kubernetes custom resource definitions: `meshes`, `virtual services`, `virtual nodes`, and `virtual routers`\. The controller watches for creation, modification, and deletion of the custom resources and makes changes to the corresponding App Mesh `[mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html)`, `[virtual service](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html)`, `[virtual node](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html)`, and `[virtual router](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html)` \(including `[route](https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html)`\) resources through the App Mesh API\. To learn more or contribute to the controller, see the [GitHub project](https://github.com/aws/aws-app-mesh-controller-for-k8s)\.

The controller also installs a webhook that injects the following containers into Kubernetes pods that are labeled with a name that you specify\.
+ **App Mesh Envoy proxy** – Envoy uses the configuration defined in the App Mesh control plane to determine where to send your application traffic\. 
+ **App Mesh proxy route manager **– Updates `iptables` rules in a pod's network namespace that route ingress and egress traffic through Envoy\. This container runs as a Kubernetes init container inside of the pod\.

## Prerequisites<a name="mesh-k8s-integration-prerequisites"></a>
+ An existing understanding of App Mesh concepts\. For more information, see [What is AWS App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html)\.
+ An existing Kubernetes cluster running version 1\.13 or later\. If you don't have an existing cluster, you can deploy one using the [Getting Started with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) guide\. If you're running your own Kubernetes cluster on Amazon EC2, then ensure that Docker is authenticated to the Amazon ECR repository that the Envoy image is in\. For more information, see [Envoy image](https://docs.aws.amazon.com/app-mesh/latest/userguide/envoy.html) and [Registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth) in the AWS documentation and [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) in the Kubernetes documentation\.
+ The AWS CLI version 1\.18\.88 or later or 2\.0\.26 or later installed\. To install or upgrade the AWS CLI, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\. 
+ A `kubectl` client that is configured to communicate with your Kubernetes cluster\. If you're using Amazon Elastic Kubernetes Service, you can use the instructions for installing `[kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)` and configuring a `[kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)` file\.
+ Helm version 3\.0 or later installed\. If you don't have Helm installed, you can install it by completing the instructions in [Using Helm with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/helm.html)\.

## Step 1: Install the integration components<a name="install-controller"></a>

Install the integration components one time to each cluster that hosts pods that you want to use with App Mesh\.

**To install the integration components**

1. The remaining steps of this procedure require a cluster without a pre\-release version of the controller installed\. If you have installed a pre\-release version, or are not sure whether you have, you can download and run a script that will check to see whether a pre\-release version is installed on your cluster\.

   ```
   curl -o pre_upgrade_check.sh https://raw.githubusercontent.com/aws/eks-charts/master/stable/appmesh-controller/upgrade/pre_upgrade_check.sh
   ./pre_upgrade_check.sh
   ```

   If the script returns `Your cluster is ready for upgrade. Please proceed to the installation instructions` then you can proceed to the next step\. If a different message is returned, then you'll need to complete the upgrade steps before continuing\. For more information about upgrading a pre\-release version, see [Upgrade](https://github.com/aws/eks-charts/blob/master/stable/appmesh-controller/README.md#upgrade) on GitHub\.

1. Add the `eks-charts` repository to Helm\.

   ```
   helm repo add eks https://aws.github.io/eks-charts
   ```

1. Install the App Mesh Kubernetes custom resource definitions \(CRD\)\.

   ```
   kubectl apply -k "https://github.com/aws/eks-charts/stable/appmesh-controller/crds?ref=master"
   ```

1. Create a Kubernetes namespace for the controller\.

   ```
   kubectl create ns appmesh-system
   ```

1. Set the following variables for use in later steps\. Replace `cluster-name` and `region-code` with the values for your existing cluster\.

   ```
   export CLUSTER_NAME=cluster-name
   export AWS_REGION=region-code
   ```

1. \(Optional\) If you want to run the controller on Fargate, then you need to create a Fargate profile\. If you don't have `eksctl` installed, you can install it with the instructions in [Installing or Upgrading `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)\. If you'd prefer to create the profile using the console, see [Creating a Fargate profile](https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html#create-fargate-profile)\.

   ```
   eksctl create fargateprofile --cluster $CLUSTER_NAME --name appmesh-system --namespace appmesh-system
   ```

1. Create an OpenID Connect \(OIDC\) identity provider for your cluster\. If you don't have `eksctl` installed, you can install it with the instructions in [Installing or upgrading `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)\. If you'd prefer to create the provider using the console, see [Enabling IAM roles for service accounts on your cluster](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)\.

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

   If you prefer to create the service account using the AWS Management Console or AWS CLI, see [Creating an IAM role and policy for your service account](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html#create-service-account-iam-role)\. If you use the AWS Management Console or AWS CLI to create the account, you also need to map the role to a Kubernetes service account\. For more information, see [Specifying an IAM role for your service account](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)\. 

1. Deploy the App Mesh controller\. For a list of all configuration options, see [Configuration](https://github.com/aws/eks-charts/blob/master/stable/appmesh-controller/README.md#configuration) on GitHub\.

   ```
   helm upgrade -i appmesh-controller eks/appmesh-controller \
       --namespace appmesh-system \
       --set region=$AWS_REGION \
       --set serviceAccount.create=false \
       --set serviceAccount.name=appmesh-controller
   ```
**Important**  
If your cluster is in the `me-south-1` or `ap-east-1` Regions, then you need to add the following options to the previous command, replacing *`account`*, *`region-code`*, and `envoy-image-version` with the value returned from one of the following commands\.  

   ```
   aws ssm get-parameter --name "/aws/service/appmesh/envoy" --region me-south-1 --query "Parameter.Value" --output text
   ```

   ```
   aws ssm get-parameter --name "/aws/service/appmesh/envoy" --region ap-east-1 --query "Parameter.Value" --output text
   ```
Output  

   ```
   account-id.dkr.ecr.region-code.amazonaws.com/aws-appmesh-envoy:venvoy-image-version
   ```
`--set sidecar.image.repository=account-id.dkr.ecr.region-code.amazonaws.com/aws-appmesh-envoy`
`--set sidecar.image.tag=envoy-image-version`

1. Confirm that the controller version is `v1.0.0` or later\. You can review the [change log](https://github.com/aws/aws-app-mesh-controller-for-k8s/releases) on GitHub\.

   ```
   kubectl get deployment appmesh-controller \
       -n appmesh-system \
       -o json  | jq -r ".spec.template.spec.containers[].image" | cut -f2 -d ':'
   ```
**Note**  
If you view the log for the running container, you may see a line that includes the following text, which can be safely ignored\.  

   ```
   Neither -kubeconfig nor -master was specified. Using the inClusterConfig. This might not work.
   ```

## Step 2: Deploy App Mesh resources<a name="configure-app-mesh"></a>

When you deploy an application in Kubernetes, you also create the Kubernetes custom resources so that the controller can create the corresponding App Mesh resources\. The following procedure helps you deploy App Mesh resources with some of their features\. You can find example manifests for deploying other App Mesh resource features in the `v1beta2` sub\-folders of many of the feature folders listed at [App Mesh walkthroughs](https://github.com/aws/aws-app-mesh-examples/tree/master/walkthroughs) on GitHub\.

**Important**  
Once the controller has created an App Mesh resource, we recommend that you only make changes to, or delete the App Mesh resource, using the controller\. If you make changes to or delete the resource using App Mesh, the controller won't change or recreate the changed or deleted App Mesh resource for ten hours, by default\. You can configure this duration to be less\. For more information, see [Configuration](https://github.com/aws/eks-charts/blob/master/stable/appmesh-controller/README.md#configuration) on GitHub\.

**To deploy App Mesh resources**

1. Create a Kubernetes namespace to deploy App Mesh resources to\. 

   1. Save the following contents to a file named `namespace.yaml` on your computer\.

      ```
      apiVersion: v1
      kind: Namespace
      metadata:
        name: my-apps
        labels:
          mesh: my-mesh
          appmesh.k8s.aws/sidecarInjectorWebhook: enabled
      ```

   1. Create the namespace\.

      ```
      kubectl apply -f namespace.yaml
      ```

1. Create an App Mesh service mesh\.

   1. Save the following contents to a file named `mesh.yaml` on your computer\. The file will be used to create a mesh resource named `my-mesh`\. A service mesh is a logical boundary for network traffic between the services that reside within it\.

      ```
      apiVersion: appmesh.k8s.aws/v1beta2
      kind: Mesh
      metadata:
        name: my-mesh
      spec:
        namespaceSelector:
          matchLabels:
            mesh: my-mesh
      ```

   1. Create the mesh\.

      ```
      kubectl apply -f mesh.yaml
      ```

   1. View the details of the Kubernetes mesh resource that was created\.

      ```
      kubectl describe mesh my-mesh
      ```

      Output

      ```
      Name:         my-mesh
      Namespace:
      Labels:       <none>
      Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"appmesh.k8s.aws/v1beta2","kind":"Mesh","metadata":{"annotations":{},"name":"my-mesh"},"spec":{"namespaceSelector":{"matchLa...
      API Version:  appmesh.k8s.aws/v1beta2
      Kind:         Mesh
      Metadata:
        Creation Timestamp:  2020-06-17T14:51:37Z
        Finalizers:
          finalizers.appmesh.k8s.aws/mesh-members
          finalizers.appmesh.k8s.aws/aws-appmesh-resources
        Generation:        1
        Resource Version:  6295
        Self Link:         /apis/appmesh.k8s.aws/v1beta2/meshes/my-mesh
        UID:               111a11b1-c11d-1e1f-gh1i-j11k1l111m711
      Spec:
        Aws Name:  my-mesh
        Namespace Selector:
          Match Labels:
            Mesh:  my-mesh
      Status:
        Conditions:
          Last Transition Time:  2020-06-17T14:51:37Z
          Status:                True
          Type:                  MeshActive
        Mesh ARN:                arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh
        Observed Generation:     1
      Events:                    <none>
      ```

   1. View the details about the App Mesh service mesh that the controller created\.

      ```
      aws appmesh describe-mesh --mesh-name my-mesh
      ```

      Output

      ```
      {
          "mesh": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh",
                  "createdAt": "2020-06-17T09:51:37.920000-05:00",
                  "lastUpdatedAt": "2020-06-17T09:51:37.920000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {},
              "status": {
                  "status": "ACTIVE"
              }
          }
      }
      ```

1. Create an App Mesh virtual node\. A virtual node acts as a logical pointer to a Kubernetes deployment\.

   1. Save the following contents to a file named `virtual-node.yaml` on your computer\. The file will be used to create an App Mesh virtual node named `my-service-a` in the *`my-apps`* namespace\. The virtual node represents a Kubernetes service that is created in a later step\. The value for `hostname` is the fully qualified DNS hostname of the actual service that this virtual node represents\.

      ```
      apiVersion: appmesh.k8s.aws/v1beta2
      kind: VirtualNode
      metadata:
        name: my-service-a
        namespace: my-apps
      spec:
        podSelector:
          matchLabels:
            app: my-app-1
        listeners:
          - portMapping:
              port: 80
              protocol: http
        serviceDiscovery:
          dns:
            hostname: my-service-a.my-apps.svc.cluster.local
      ```

      Virtual nodes have capabilities, such as end\-to\-end encryption and health checks, that aren't covered in this tutorial\. For more information, see [Virtual nodes](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html)\. To see all available settings for a virtual node that you can set in the preceding spec, run the following command\.

      ```
      aws appmesh create-virtual-node --generate-cli-skeleton yaml-input
      ```

   1. Deploy the virtual node\.

      ```
      kubectl apply -f virtual-node.yaml
      ```

   1. View the details of the Kubernetes virtual node resource that was created\.

      ```
      kubectl describe virtualnode my-service-a -n my-apps
      ```

      Output

      ```
      Name:         my-service-a
      Namespace:    my-apps
      Labels:       <none>
      Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"appmesh.k8s.aws/v1beta2","kind":"VirtualNode","metadata":{"annotations":{},"name":"my-service-a","namespace":"my-app-1"},"s...
      API Version:  appmesh.k8s.aws/v1beta2
      Kind:         VirtualNode
      Metadata:
        Creation Timestamp:  2020-06-17T14:57:29Z
        Finalizers:
          finalizers.appmesh.k8s.aws/aws-appmesh-resources
        Generation:        2
        Resource Version:  22545
        Self Link:         /apis/appmesh.k8s.aws/v1beta2/namespaces/my-apps/virtualnodes/my-service-a
        UID:               111a11b1-c11d-1e1f-gh1i-j11k1l111m711
      Spec:
        Aws Name:  my-service-a_my-apps
        Listeners:
          Port Mapping:
            Port:      80
            Protocol:  http
        Mesh Ref:
          Name:  my-mesh
          UID:   111a11b1-c11d-1e1f-gh1i-j11k1l111m711
        Pod Selector:
          Match Labels:
            App:  nginx
        Service Discovery:
          Dns:
            Hostname:  my-service-a.my-apps.svc.cluster.local
      Status:
        Conditions:
          Last Transition Time:  2020-06-17T14:57:29Z
          Status:                True
          Type:                  VirtualNodeActive
        Observed Generation:     2
        Virtual Node ARN:        arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualNode/my-service-a_my-apps
      Events:                    <none>
      ```

   1. View the details of the virtual node that the controller created in App Mesh\.
**Note**  
Even though the name of the virtual node created in Kubernetes is `my-service-a`, the name of the virtual node created in App Mesh is `my-service-a_my-app-1`\. The controller appends the Kubernetes namespace name to the App Mesh virtual node name when it creates the App Mesh resource\. The namespace name is added because in Kubernetes you can create virtual nodes with the same name in different namespaces, but in App Mesh a virtual node name must be unique within a mesh\.

      ```
      aws appmesh describe-virtual-node --mesh-name my-mesh --virtual-node-name my-service-a_my-apps
      ```

      Output

      ```
      {
          "virtualNode": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualNode/my-service-a_my-apps",
                  "createdAt": "2020-06-17T09:57:29.840000-05:00",
                  "lastUpdatedAt": "2020-06-17T09:57:29.840000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "backends": [],
                  "listeners": [
                      {
                          "portMapping": {
                              "port": 80,
                              "protocol": "http"
                          }
                      }
                  ],
                  "serviceDiscovery": {
                      "dns": {
                          "hostname": "my-service-a.my-apps.svc.cluster.local"
                      }
                  }
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualNodeName": "my-service-a_my-apps"
          }
      }
      ```

1. Create an App Mesh virtual router\. Virtual routers handle traffic for one or more virtual services within your mesh\.

   1. Save the following contents to a file named `virtual-router.yaml` on your computer\. The file will be used to create a virtual router to route traffic to the virtual node named `my-service-a` that was created in the previous step\. The controller will create the App Mesh virtual router and route resources\. You can specify many more capabilities for your routes and use protocols other than `http`\. For more information, see [Virtual routers](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html) and [Routes](https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html)\. Notice that the virtual node name referenced is the Kubernetes virtual node name, not the App Mesh virtual node name that was created in App Mesh by the controller\.

      ```
      apiVersion: appmesh.k8s.aws/v1beta2
      kind: VirtualRouter
      metadata:
        namespace: my-apps
        name: my-service-a-virtual-router
      spec:
        listeners:
          - portMapping:
              port: 80
              protocol: http
        routes:
          - name: my-service-a-route
            httpRoute:
              match:
                prefix: /
              action:
                weightedTargets:
                  - virtualNodeRef:
                      name: my-service-a
                    weight: 1
      ```

      \(Optional\) To see all available settings for a virtual router that you can set in the preceding spec, run any of the following command\.

      ```
      aws appmesh create-virtual-router --generate-cli-skeleton yaml-input
      ```

      To see all available settings for a route that you can set in the preceding spec, run any of the following command\.

      ```
      aws appmesh create-route --generate-cli-skeleton yaml-input
      ```

   1. Deploy the virtual router\.

      ```
      kubectl apply -f virtual-router.yaml
      ```

   1. View the Kubernetes virtual router resource that was created\.

      ```
      kubectl describe virtualrouter my-service-a-virtual-router -n my-apps
      ```

      Abbreviated output

      ```
      Name:         my-service-a-virtual-router
      Namespace:    my-app-1
      Labels:       <none>
      Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"appmesh.k8s.aws/v1beta2","kind":"VirtualRouter","metadata":{"annotations":{},"name":"my-service-a-virtual-router","namespac...
      API Version:  appmesh.k8s.aws/v1beta2
      Kind:         VirtualRouter
      ...
      Spec:
        Aws Name:  my-service-a-virtual-router_my-apps
        Listeners:
          Port Mapping:
            Port:      80
            Protocol:  http
        Mesh Ref:
          Name:  my-mesh
          UID:   111a11b1-c11d-1e1f-gh1i-j11k1l111m711
        Routes:
          Http Route:
            Action:
              Weighted Targets:
                Virtual Node Ref:
                  Name:  my-service-a
                Weight:  1
            Match:
              Prefix:  /
          Name:        my-service-a-route
      Status:
        Conditions:
          Last Transition Time:  2020-06-17T15:14:01Z
          Status:                True
          Type:                  VirtualRouterActive
        Observed Generation:     1
        Route AR Ns:
          My - Service - A - Route:  arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router_my-apps/route/my-service-a-route
        Virtual Router ARN:          arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router_my-apps
      Events:                        <none>
      ```

   1. View the virtual router resource that the controller created in App Mesh\. You specify `my-service-a-virtual-router_my-app-1` for `name`, because when the controller created the virtual router in App Mesh, it appended the Kubernetes namespace name to the name of the virtual router\.

      ```
      aws appmesh describe-virtual-router --virtual-router-name my-service-a-virtual-router_my-apps --mesh-name my-mesh
      ```

      Output

      ```
      {
          "virtualRouter": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router_my-apps",
                  "createdAt": "2020-06-17T10:14:01.547000-05:00",
                  "lastUpdatedAt": "2020-06-17T10:14:01.547000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "listeners": [
                      {
                          "portMapping": {
                              "port": 80,
                              "protocol": "http"
                          }
                      }
                  ]
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualRouterName": "my-service-a-virtual-router_my-apps"
          }
      }
      ```

   1. View the route resource that the controller created in App Mesh\. A route resource was not created in Kubernetes because the route is part of the virtual router configuration in Kubernetes\. The route information was shown in the Kubernetes resource detail in sub\-step `c`\. The controller did not append the Kubernetes namespace name to the App Mesh route name when it created the route in App Mesh because route names are unique to a virtual router\.

      ```
      aws appmesh describe-route \
          --route-name my-service-a-route \
          --virtual-router-name my-service-a-virtual-router_my-apps \
          --mesh-name my-mesh
      ```

      Output

      ```
      {
          "route": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualRouter/my-service-a-virtual-router_my-apps/route/my-service-a-route",
                  "createdAt": "2020-06-17T10:14:01.577000-05:00",
                  "lastUpdatedAt": "2020-06-17T10:14:01.577000-05:00",
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
                                  "virtualNode": "my-service-a_my-apps",
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
              "virtualRouterName": "my-service-a-virtual-router_my-apps"
          }
      }
      ```

1. Create an App Mesh virtual service\. A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router\. Dependent services call your virtual service by its name\. Though the name doesn't matter to App Mesh, we recommend naming the virtual service the fully qualified domain name of the actual service that the virtual service represents\. By naming your virtual services this way, you don't need to change your application code to reference a different name\. The requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service\.

   1. Save the following contents to a file named `virtual-service.yaml` on your computer\. The file will be used to create a virtual service that uses a virtual router provider to route traffic to the virtual node named `my-service-a` that was created in a previous step\. The value for `awsName` in the `spec` is the fully qualified domain name \(FQDN\) of the actual Kubernetes service that this virtual service abstracts\. The Kubernetes service is created in [Step 3: Create or update services](#create-update-services)\. For more information, see [Virtual services](https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html)\.

      ```
      apiVersion: appmesh.k8s.aws/v1beta2
      kind: VirtualService
      metadata:
        name: my-service-a
        namespace: my-apps
      spec:
        awsName: my-service-a.my-apps.svc.cluster.local
        provider:
          virtualRouter:
            virtualRouterRef:
              name: my-service-a-virtual-router
      ```

      To see all available settings for a virtual service that you can set in the preceding spec, run the following command\.

      ```
      aws appmesh create-virtual-service --generate-cli-skeleton yaml-input
      ```

   1. Create the virtual service\.

      ```
      kubectl apply -f virtual-service.yaml
      ```

   1. View the details of the Kubernetes virtual service resource that was created\.

      ```
      kubectl describe virtualservice my-service-a -n my-apps
      ```

      Output

      ```
      Name:         my-service-a
      Namespace:    my-app-1
      Labels:       <none>
      Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"appmesh.k8s.aws/v1beta2","kind":"VirtualService","metadata":{"annotations":{},"name":"my-service-a","namespace":"my-app-1"}...
      API Version:  appmesh.k8s.aws/v1beta2
      Kind:         VirtualService
      Metadata:
        Creation Timestamp:  2020-06-17T15:48:40Z
        Finalizers:
          finalizers.appmesh.k8s.aws/aws-appmesh-resources
        Generation:        1
        Resource Version:  13598
        Self Link:         /apis/appmesh.k8s.aws/v1beta2/namespaces/my-apps/virtualservices/my-service-a
        UID:               111a11b1-c11d-1e1f-gh1i-j11k1l111m711
      Spec:
        Aws Name:  my-service-a.my-apps.svc.cluster.local
        Mesh Ref:
          Name:  my-mesh
          UID:   111a11b1-c11d-1e1f-gh1i-j11k1l111m711
        Provider:
          Virtual Router:
            Virtual Router Ref:
              Name:  my-service-a-virtual-router
      Status:
        Conditions:
          Last Transition Time:  2020-06-17T15:48:40Z
          Status:                True
          Type:                  VirtualServiceActive
        Observed Generation:     1
        Virtual Service ARN:     arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualService/my-service-a.my-apps.svc.cluster.local
      Events:                    <none>
      ```

   1. View the details of the virtual service resource that the controller created in App Mesh\. The Kubernetes controller did not append the Kubernetes namespace name to the App Mesh virtual service name when it created the virtual service in App Mesh because the virtual service's name is a unique FQDN\.

      ```
      aws appmesh describe-virtual-service --virtual-service-name my-service-a.my-apps.svc.cluster.local --mesh-name my-mesh
      ```

      Output

      ```
      {
          "virtualService": {
              "meshName": "my-mesh",
              "metadata": {
                  "arn": "arn:aws:appmesh:us-west-2:111122223333:mesh/my-mesh/virtualService/my-service-a.my-apps.svc.cluster.local",
                  "createdAt": "2020-06-17T10:48:40.182000-05:00",
                  "lastUpdatedAt": "2020-06-17T10:48:40.182000-05:00",
                  "meshOwner": "111122223333",
                  "resourceOwner": "111122223333",
                  "uid": "111a11b1-c11d-1e1f-gh1i-j11k1l111m711",
                  "version": 1
              },
              "spec": {
                  "provider": {
                      "virtualRouter": {
                          "virtualRouterName": "my-service-a-virtual-router_my-apps"
                      }
                  }
              },
              "status": {
                  "status": "ACTIVE"
              },
              "virtualServiceName": "my-service-a.my-apps.svc.cluster.local"
          }
      }
      ```

## Step 3: Create or update services<a name="create-update-services"></a>

Any pods that you want to use with App Mesh must have the App Mesh sidecar containers added to them\. The injector automatically adds the sidecar containers to any pod deployed with a label that you specify\.

1. Enable proxy authorization\. We recommend that you enable each Kubernetes deployment to stream only the configuration for its own App Mesh virtual node\.

   1. Save the following contents to a file named `proxy-auth.json` on your computer\. Make sure to replace the *alternate\-colored values* with your own\.

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": "appmesh:StreamAggregatedResources",
                  "Resource": [
                      "arn:aws:appmesh:region-code:111122223333:mesh/my-mesh/virtualNode/my-service-a_my-apps"
                  ]
              }
          ]
      }
      ```

   1. Create the policy\.

      ```
      aws iam create-policy --policy-name my-policy --policy-document file://proxy-auth.json
      ```

   1. Create an IAM role, attach the policy you created in the previous step to it, create a Kubernetes service account and bind the policy to the Kubernetes service account\. The role enables the controller to add, remove, and change App Mesh resources\.

      ```
      eksctl create iamserviceaccount \
          --cluster $CLUSTER_NAME \
          --namespace my-apps \
          --name my-service-a \
          --attach-policy-arn  arn:aws:iam::111122223333:policy/my-policy \
          --override-existing-serviceaccounts \
          --approve
      ```

      If you prefer to create the service account using the AWS Management Console or AWS CLI, see [Creating an IAM Role and policy for your service account](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html#create-service-account-iam-role)\. If you use the AWS Management Console or AWS CLI to create the account, you also need to map the role to a Kubernetes service account\. For more information, see [Specifying an IAM role for your service account](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)\.

1. \(Optional\) If you want to deploy your deployment to Fargate pods, then you need to create a Fargate profile\. If you don't have `eksctl` installed, you can install it with the instructions in [Installing or Upgrading `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)\. If you'd prefer to create the profile using the console, see [Creating a Fargate profile](https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html#create-fargate-profile)\.

   ```
   eksctl create fargateprofile --cluster my-cluster --region region-code --name my-service-a --namespace my-apps
   ```

1. Create a Kubernetes service and deployment\. If you have an existing deployment that you want to use with App Mesh, then you need to deploy a virtual node, as you did in sub\-step `3` of [Step 2: Deploy App Mesh resources](#configure-app-mesh), and update your deployment to make sure that its label matches the label that you set on the virtual node, so that the sidecar containers are automatically added to the pods and the pods are redeployed\.

   1. Save the following contents to a file named `example-service.yaml` on your computer\. If you change the namespace name and are using Fargate pods, make sure that the namespace name matches the namespace name that you defined in your Fargate profile\.

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: my-service-a
        namespace: my-apps
        labels:
          app: my-app-1
      spec:
        selector:
          app: my-app-1
        ports:
          - protocol: TCP
            port: 80
            targetPort: 80
      ---
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-service-a
        namespace: my-apps
        labels:
          app: my-app-1
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: my-app-1
        template:
          metadata:
            labels:
              app: my-app-1
          spec:
            serviceAccountName: my-service-a
            containers:
            - name: nginx
              image: nginx:1.19.0
              ports:
              - containerPort: 80
      ```
**Important**  
The value for the `app` `matchLabels` `selector` in the spec must match the value that you specified when you created the virtual node in sub\-step `3` of [Step 2: Deploy App Mesh resources](#configure-app-mesh), or the sidecar containers won't be injected into the pod\. In the previous example, the value for the label is `my-app-1`\.

   1. Deploy the service\.

      ```
      kubectl apply -f example-service.yaml
      ```

   1. View the service and deployment\.

      ```
      kubectl -n my-apps get pods
      ```

      Output

      ```
      NAME                            READY   STATUS    RESTARTS   AGE
      my-service-a-54776556f6-2cxd9   2/2     Running   0          10s
      my-service-a-54776556f6-w26kf   2/2     Running   0          18s
      my-service-a-54776556f6-zw5kt   2/2     Running   0          26s
      ```

   1. View the details for one of the pods that was deployed\.

      ```
      kubectl -n my-apps describe pod my-service-a-54776556f6-2cxd9
      ```

      Abbreviated output

      ```
      Name:         my-service-a-54776556f6-2cxd9
      Namespace:    my-app-1
      Priority:     0
      Node:         ip-192-168-44-157.us-west-2.compute.internal/192.168.44.157
      Start Time:   Wed, 17 Jun 2020 11:08:59 -0500
      Labels:       app=nginx
                    pod-template-hash=54776556f6
      Annotations:  kubernetes.io/psp: eks.privileged
      Status:       Running
      IP:           192.168.57.134
      IPs:
        IP:           192.168.57.134
      Controlled By:  ReplicaSet/my-service-a-54776556f6
      Init Containers:
        proxyinit:
          Container ID:   docker://e0c4810d584c21ae0cb6e40f6119d2508f029094d0e01c9411c6cf2a32d77a59
          Image:          111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2
          Image ID:       docker-pullable://111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager
          Port:           <none>
          Host Port:      <none>
          State:          Terminated
            Reason:       Completed
            Exit Code:    0
            Started:      Fri, 26 Jun 2020 08:36:22 -0500
            Finished:     Fri, 26 Jun 2020 08:36:22 -0500
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
            AWS_ROLE_ARN:                  arn:aws:iam::111122223333:role/eksctl-app-mesh-addon-iamserviceaccount-my-a-Role1-NMNCVWB6PL0N
            AWS_WEB_IDENTITY_TOKEN_FILE:   /var/run/secrets/eks.amazonaws.com/serviceaccount/token
          ...
      Containers:
        nginx:
          Container ID:   docker://be6359dc6ecd3f18a1c87df7b57c2093e1f9db17d5b3a77f22585ce3bcab137a
          Image:          nginx:1.19.0
          Image ID:       docker-pullable://nginx
          Port:           80/TCP
          Host Port:      0/TCP
          State:          Running
            Started:      Fri, 26 Jun 2020 08:36:28 -0500
          Ready:          True
          Restart Count:  0
          Environment:
            AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/eksctl-app-mesh-addon-iamserviceaccount-my-a-Role1-NMNCVWB6PL0N
            AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
          ...
        envoy:
          Container ID:   docker://905b55cbf33ef3b3debc51cb448401d24e2e7c2dbfc6a9754a2c49dd55a216b6
          Image:          840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.12.4.0-prod
          Image ID:       docker-pullable://840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy
          Port:           9901/TCP
          Host Port:      0/TCP
          State:          Running
            Started:      Fri, 26 Jun 2020 08:36:36 -0500
          Ready:          True
          Restart Count:  0
          Requests:
            cpu:     10m
            memory:  32Mi
          Environment:
            APPMESH_VIRTUAL_NODE_NAME:    mesh/my-mesh/virtualNode/my-service-a_my-apps
            APPMESH_PREVIEW:              0
            ENVOY_LOG_LEVEL:              info
            AWS_REGION:                   us-west-2
            AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/eksctl-app-mesh-addon-iamserviceaccount-my-a-Role1-NMNCVWB6PL0N
            AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
      ...
      Events:
        Type    Reason     Age   From                                                   Message
        ----    ------     ----  ----                                                   -------
        Normal  Pulling    30s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Pulling image "111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2"
        Normal  Pulled     23s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Successfully pulled image "111345817488.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-proxy-route-manager:v2"
        Normal  Created    21s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Created container proxyinit
        Normal  Started    21s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Started container proxyinit
        Normal  Pulling    20s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Pulling image "nginx:1.19.0"
        Normal  Pulled     16s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Successfully pulled image "nginx:1.19.0"
        Normal  Created    15s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Created container nginx
        Normal  Started    15s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Started container nginx
        Normal  Pulling    15s   kubelet, ip-192-168-44-157.us-west-2.compute.internal  Pulling image "840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.12.4.0-prod"
        Normal  Pulled     8s    kubelet, ip-192-168-44-157.us-west-2.compute.internal  Successfully pulled image "840364872350.dkr.ecr.us-west-2.amazonaws.com/aws-appmesh-envoy:v1.12.4.0-prod"
        Normal  Created    7s    kubelet, ip-192-168-44-157.us-west-2.compute.internal  Created container envoy
        Normal  Started    7s    kubelet, ip-192-168-44-157.us-west-2.compute.internal  Started container envoy
      ```

      In the preceding output, you can see that the `proxyinit` and `envoy` containers were added to the pod by the controller\. If you deployed the example service to Fargate, then the `envoy` container was added to the pod by the controller, but the `proxyinit` container was not\.

1. \(Optional\) Install add\-ons such as Prometheus, Grafana, AWS X\-Ray, Jaeger, and Datadog\. For more information, see [App Mesh add\-ons](https://github.com/aws/eks-charts#app-mesh-add-ons) on GitHub\. 

## Step 4: Clean up<a name="remove-integration"></a>

Remove all of the example resources created in this tutorial\. The controller also removes the resources that were created in the `my-mesh` App Mesh service mesh\.

```
kubectl delete namespace my-apps
```

If you created a Fargate profile for the example service, then remove it\.

```
eksctl delete fargateprofile --name my-service-a --cluster my-cluster --region region-code
```

Delete the mesh\.

```
kubectl delete mesh my-mesh
```

\(Optional\) You can remove the Kubernetes integration components\.

```
helm delete appmesh-controller -n appmesh-system
```

\(Optional\) If you deployed the Kubernetes integration components to Fargate, then delete the Fargate profile\.

```
eksctl delete fargateprofile --name appmesh-system --cluster my-cluster --region region-code
```