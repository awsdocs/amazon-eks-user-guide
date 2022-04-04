# Certificate signing<a name="cert-signing"></a>

The Kubernetes Certificates API enables automation of [X\.509](https://www.itu.int/rec/T-REC-X.509) credential provisioning\. It features a command line interface for Kubernetes API clients to request and obtain [X\.509 certificates](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/) from a Certificate Authority \(CA\)\. A `CertificateSigningRequest` \(CSR\) resource is used to request that a denoted signer sign the certificate\. Then, the request is either approved or denied before it's signed\. Kubernetes supports both build\-in signers and custom signers with well\-defined behaviors\. This way, clients can predict what happens to their CSRs\. To learn more about certificate signing, see [signing requests](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/)\.

One of the built\-in signers is `kubernetes.io/legacy-unknown`\. The `v1beta1` API of CSR resource honored this legacy\-unknown signer\. However, the stable v1 API of CSR doesn't allow the `signerName` to be set to `kubernetes.io/legacy-unknown`\.

Amazon EKS version 1\.21 and earlier versions allowed the value `legacy-unknown` as the `signerName` in v1beta1 CSR API\. This API enables the Amazon EKS Certificate Authority \(CA\) to generate certificates\. However, in Kubernetes version 1\.22, the v1b``eta1 CSR API is replaced by the v1 CSR API\. This API doesn't support the signerName of “legacy\-unknown\.” Given this, if you want to use Amazon EKS CA for generating certificates on version 1\.22 and later, you need to use a [custom signer]()\. It was introduced in Amazon EKS version 1\.22\. To use the CSR v1 API version and generate a new certificate, you must migrate any existing manifests and API clients\. Existing certificates that were created with the older `v1beta1` API are valid and function until the certificate expires\. This includes the following:

1. Trust distribution: None\. There's no standard trust or distribution for this signer in a Kubernetes cluster\.

1. Permitted subjects: Any

1. Permitted x509 extensions: Honors subjectAltName and key usage extensions and discards other extensions

1. Permitted key usages: Must not include usages beyond \["key encipherment", "digital signature", "server auth"\]

1. Expiration/certificate lifetime: 1 year \(default and maximum\) 

1. CA bit allowed/disallowed: Not allowed

## Example CSR generation with signerName<a name="csr-example"></a>

These steps shows how to generate a serving certificate with a `signerName` DNS name `myserver.default.svc`\. Use this as a guide for your own environment\.

1. Run the `openssl genrsa -out myserver.key 2048` command to generate an RSA private key\.

   ```
   openssl genrsa -out myserver.key 2048
   ```

1. Run the following command to generate a certificate request\.

   ```
   openssl req -new -key myserver.key -out myserver.csr -subj "/CN=myserver.default.svc"
   ```

1. Run the `cat myserver.csr | base64 -w 0 #` command to generate a base64 value for the CSR request\. Later, use this value for the `request` value in your CSR\.

   ```
   openssl req -new -key myserver.key -out myserver.csr -subj "/CN=myserver.default.svc"
   ```

1. Run the **kubectl apply \-f *myserver\.yaml*** command to submit the CSR\.

   ```
   kubectl apply -f mycsr.yaml
   ```

1. Create a `CertificateSigningRequest` YAML file\. In the following example, `myserver` is the `signerName`\.

   ```
   apiVersion: certificates.k8s.io/v1
   kind: CertificateSigningRequest
   metadata:
     name: myserver
   spec:
     request: [your-base64-value]
     signerName: beta.eks.amazonaws.com/app-serving
     usages:
       - digital signature
       - key encipherment
       - server auth
   ```

1. Run the `kubectl certificate approve myserver` command to approve the serving certificate\.

   ```
   kubectl certificate approve myserver
   ```

1. Run the `kubectl get csr myserver` command verify that the certificate has been issued\.

   The output is as follows\.

   ```
   NAME     AGE   SIGNERNAME                            REQUESTOR         REQUESTEDDURATION   CONDITION
   myserver 96s   beta.eks.amazonaws.com/app-serving    kubernetes-admin  <none>              Approved,Issued
   ```

1. Run the following command to verify that a certificate has been issued:

   ```
   kubectl get csr myserver -o jsonpath='{.status.certificate}'| base64 -d > myserver.crt
   ```

   Example output:

   ```
   NAME      AGE  SIGNERNAME                          REQUESTOR       REQUESTEDDURATION   CONDITION
   myserver  96s  beta.eks.amazonaws.com/app-serving  kubernetes-admin <none>             Approved,Issued
   ```

1. Export the issued certificate to the signed certificate `myserver.crt`\.

   ```
   kubectl get csr myserver -o jsonpath='{.status.certificate}'| base64 -d > myserver.crt
   ```