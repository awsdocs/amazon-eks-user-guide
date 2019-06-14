# Deploy a Mesh Connected Service<a name="deploy-mesh-connected-service"></a>

In this topic, you deploy a sample application on Kubernetes\. The application deploys mesh, virtual service, and virtual node Kubernetes custom resources\. Kubernetes automatically creates mesh, virtual service, and virtual node resources in App Mesh and injects the App Mesh sidecar images into Kubernetes pods\.

## Prerequisites<a name="prerequisites"></a>

Before you deploy the sample application, you must meet the following prerequisites:
+ Meet all of the prerequisites in [Tutorial: Configure App Mesh Integration with Kubernetes](mesh-k8s-integration.md)\.
+ Have the App Mesh controller for Kubernetes and the App Mesh sidecar injector for Kubernetes installed and configured\. When you install the sidecar injector, specify *color\-mesh* as the name of your mesh\. To learn more about the controller and sidecar injector and how to install and configure them, see [Tutorial: Configure App Mesh Integration with Kubernetes](mesh-k8s-integration.md)\.

## Deploy a Sample Application<a name="deploy-sample-application"></a>

The sample application consists of two components:
+ **ColorGateway** – A simple http service written in Go that is exposed to external clients and that responds to *http://service\-name:port/color*\. The gateway responds with a color retrieved from *color\-teller* and a histogram of colors observed at the server that responded up to the point when you made the request\.
+ **ColorTeller** – A simple http service written in Go that is configured to return a color\. Multiple variants of the service are deployed\. Each service is configured to return a specific color\.

1. To deploy the color mesh sample application, download the following file and apply it to your Kubernetes cluster with the following command\.

   ```
   curl https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/v0.1.0/examples/color.yaml | kubectl apply -f -
   ```

1. View the resources deployed by the sample application with the following command\.

   ```
   kubectl -n appmesh-demo get all
   ```

   In the output, you see a collection of virtual services, virtual nodes, and mesh custom resources along with native Kubernetes deployments, pods, and services\. Your output will be similar to the following output\.

   ```
   NAME                                     READY     STATUS    RESTARTS   AGE
   pod/colorgateway-cc6464d75-4ktj4         2/2       Running   0          37s
   pod/colorteller-86664b5956-6h26c         2/2       Running   0          36s
   pod/colorteller-black-6787756c7b-dw82f   2/2       Running   0          36s
   pod/colorteller-blue-55d6f99dc6-f5wgd    2/2       Running   0          36s
   pod/colorteller-red-578866ffb-x9m7w      2/2       Running   0          35s
   
   NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
   service/colorgateway        ClusterIP   10.100.21.147    <none>        9080/TCP   37s
   service/colorteller         ClusterIP   10.100.187.50    <none>        9080/TCP   37s
   service/colorteller-black   ClusterIP   10.100.61.36     <none>        9080/TCP   36s
   service/colorteller-blue    ClusterIP   10.100.254.230   <none>        9080/TCP   36s
   service/colorteller-red     ClusterIP   10.100.90.38     <none>        9080/TCP   36s
   
   NAME                                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/colorgateway        1         1         1            1           37s
   deployment.apps/colorteller         1         1         1            1           36s
   deployment.apps/colorteller-black   1         1         1            1           36s
   deployment.apps/colorteller-blue    1         1         1            1           36s
   deployment.apps/colorteller-red     1         1         1            1           36s
   
   NAME                                           DESIRED   CURRENT   READY     AGE
   replicaset.apps/colorgateway-cc6464d75         1         1         1         37s
   replicaset.apps/colorteller-86664b5956         1         1         1         36s
   replicaset.apps/colorteller-black-6787756c7b   1         1         1         36s
   replicaset.apps/colorteller-blue-55d6f99dc6    1         1         1         36s
   replicaset.apps/colorteller-red-578866ffb      1         1         1         35s
   
   NAME                                                       AGE
   virtualservice.appmesh.k8s.aws/colorgateway.appmesh-demo   37s
   virtualservice.appmesh.k8s.aws/colorteller.appmesh-demo    37s
   
   NAME                              AGE
   mesh.appmesh.k8s.aws/color-mesh   38s
   
   NAME                                            AGE
   virtualnode.appmesh.k8s.aws/colorgateway        39s
   virtualnode.appmesh.k8s.aws/colorteller         39s
   virtualnode.appmesh.k8s.aws/colorteller-black   39s
   virtualnode.appmesh.k8s.aws/colorteller-blue    39s
   virtualnode.appmesh.k8s.aws/colorteller-red     38s
   ```

   You can use the AWS Management Console or AWS CLI to see the App Mesh `mesh`, `virtual service`, `virtual router`, `route`, and `virtual node` resources that were automatically created by the controller\. All of the resources were deployed to the `appmesh-demo` namespace, which was labelled with `appmesh.k8s.aws/sidecarInjectorWebhook: enabled`\. Since the injector saw this label for the namespace, it injected the App Mesh sidecar container images into each of the pods\. Using `kubectl describe pod <pod-name> -n appmesh-demo`, you can see that the [App Mesh sidecar container images](https://docs.aws.amazon.com/eks/latest/userguide/mesh-gs-k8s.html#mesh-gs-k8s-update-microservices) are included in each of the pods that were deployed\.

## Run Application<a name="run-sample-application"></a>

Complete the following steps to run the application\.

1. In a terminal, use the following command to create a container in the *appmesh\-demo* namespace that has `curl` installed and open a shell to it\. In later steps, this terminal is referred to as* Terminal A*\.

   ```
   kubectl run -n appmesh-demo -it curler --image=tutum/curl /bin/bash
   ```

1. From *Terminal A*, run the following command to curl the color gateway in the color mesh application 100 times\. The gateway routes traffic to separate virtual nodes that return either white, black, or blue as a response\. 

   ```
   for i in {1..100}; do curl colorgateway:9080/color; echo; done
   ```

   100 responses are returned\. Each response looks similar to the following text:

   ```
   {"color":"blue", "stats": {"black":0.36,"blue":0.32,"white":0.32}}
   ```

   In this line of output, the colorgateway routed the request to the blue virtual node\. The numbers for each color denote the percentage of responses from each virtual node\. The number for each color in each response is cumulative over time\. The percentage is similar for each color because, by default, the weighting defined for each virtual node is the same in the *color\.yaml* file you used to install the sample application\.

   Leave *Terminal A* open\.

## Change Configuration<a name="change-configuration"></a>

Change the configuration and run the application again to see the effect of the changes\.

1. In a separate terminal from *Terminal A*, edit the *colorteller\.appmesh\-demo* virtual service with the following command\.

   ```
   kubectl edit VirtualService colorteller.appmesh-demo -n appmesh-demo
   ```

   In the editor, you can see that the *weight* value of each **virtualNodeName** is *1*\. Because the weight of each virtual node is the same, traffic routed to each virtual node is approximately even\. To route all traffic to the black node only, change the values for **colorteller\.appmesh\-demo** and **colorteller\-blue** to *0*, as shown in the following text\. Save the configuration and exit the editor\.

   ```
   spec:
     meshName: color-mesh
     routes:
     - http:
         action:
           weightedTargets:
           - virtualNodeName: colorteller.appmesh-demo
             weight: 0
           - virtualNodeName: colorteller-blue
             weight: 0
           - virtualNodeName: colorteller-black.appmesh-demo
             weight: 1
   ```

1. In *Terminal A*, run `curl` again with the following command\.

   ```
   for i in {1..100}; do curl colorgateway:9080/color; echo; done
   ```

   This time, all lines of output look similar to the following text\.

   ```
   {"color":"black", "stats": {"black":0.64,"blue":0.18,"white":0.19}}
   ```

   Black is the response every time because the gateway is now routing all traffic to the black virtual node\. Even though all traffic is now going to black, the white and blue virtual nodes still have response percentages, because the numbers are based on relative percentages over time\. When you executed the requests in a previous step, white and blue responded, which is why they still have response percentages\. You can see that the relative percentages decrease for white and blue with each response, while the percentage for black increases\.

## Remove Application<a name="remove-application"></a>

When you've finished with the sample application, you can remove it by completing the following steps\.

1. Use the following commands to remove the sample application and the App Mesh resources that were created\.

   ```
   kubectl delete namespace appmesh-demo
   kubectl delete mesh color-mesh
   ```

1. Optional: If you want to remove the controller and sidecar injector, see [Remove integration components](mesh-k8s-integration.md#remove-integration.title)\.