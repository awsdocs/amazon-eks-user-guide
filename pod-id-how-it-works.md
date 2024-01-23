# How EKS Pod Identity works<a name="pod-id-how-it-works"></a>

Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\.

Amazon EKS Pod Identity provides credentials to your workloads with an additional *EKS Auth* API and an agent pod that runs on each node\.

In your add\-ons, such as *Amazon EKS add\-ons* and self\-managed controller, operators, and other add\-ons, the author needs to update their software to use the latest AWS SDKs\. For the list of compatibility between EKS Pod Identity and the add\-ons produced by Amazon EKS, see the previous section [EKS Pod Identity restrictions](pod-identities.md#pod-id-restrictions)\.

## Using EKS Pod Identities in your code<a name="pod-id-credentials"></a>

In your code, you can use the AWS SDKs to access AWS services\. You write code to create a client for an AWS service with an SDK, and by default the SDK searches in a chain of locations for AWS Identity and Access Management credentials to use\. After valid credentials are found, the search is stopped\. For more information about the default locations used, see the [Credential provider chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html#credentialProviderChain) in the AWS SDKs and Tools Reference Guide\.

EKS Pod Identities have been added to the *Container credential provider* which is searched in a step in the default credential chain\. If your workloads currently use credentials that are earlier in the chain of credentials, those credentials will continue to be used even if you configure an EKS Pod Identity association for the same workload\. This way you can safely migrate from other types of credentials by creating the association first, before removing the old credentials\.

The container credentials provider provides temporary credentials from an agent that runs on each node\. In Amazon EKS, the agent is the Amazon EKS Pod Identity Agent and on Amazon Elastic Container Service the agent is the `amazon-ecs-agent`\. The SDKs use environment variables to locate the agent to connect to\.

In contrast, *IAM roles for service accounts* provides a *web identity* token that the AWS SDK must exchange with AWS Security Token Service by using `AssumeRoleWithWebIdentity`\.

## How EKS Pod Identity Agent works with a Pod<a name="pod-id-agent-pod"></a>

1. When Amazon EKS starts a new pod that uses a service account with an EKS Pod Identity association, the cluster adds the following content to the Pod manifest:

   ```
       env:
       - name: AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE
         value: "/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/eks-pod-identity-token"
       - name: AWS_CONTAINER_CREDENTIALS_FULL_URI
         value: "http://169.254.170.23/v1/credentials"
       volumeMounts:
       - mountPath: "/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/"
         name: eks-pod-identity-token
     volumes:
     - name: eks-pod-identity-token
       projected:
         defaultMode: 420
         sources:
         - serviceAccountToken:
             audience: pods.eks.amazonaws.com
             expirationSeconds: 86400 # 24 hours
             path: eks-pod-identity-token
   ```

1. Kubernetes selects which node to run the pod on\. Then, the Amazon EKS Pod Identity Agent on the node uses the [AssumeRoleForPodIdentity](https://docs.aws.amazon.com/eks/latest/APIReference/API_auth_AssumeRoleForPodIdentity.html) action to retrieve temporary credentials from the EKS Auth API\.

1. The EKS Pod Identity Agent makes these credentials available for the AWS SDKs that you run inside your containers\.

1. You use the SDK in your application without specifying a credential provider to use the default credential chain\. Or, you specify the container credential provider\. For more information about the default locations used, see the [Credential provider chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html#credentialProviderChain) in the AWS SDKs and Tools Reference Guide\.

1. The SDK uses the environment variables to connect to the EKS Pod Identity Agent and retrieve the credentials\.
**Note**  
 If your workloads currently use credentials that are earlier in the chain of credentials, those credentials will continue to be used even if you configure an EKS Pod Identity association for the same workload\.