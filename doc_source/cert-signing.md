# Certificate signing<a name="cert-signing"></a>

The Kubernetes Certificates API enables automation of [X\.509](https://www.itu.int/rec/T-REC-X.509) credential provisioning\. It features a command line interface for Kubernetes API clients to request and obtain [X\.509 certificates](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/) from a Certificate Authority \(CA\)\. A `CertificateSigningRequest` \(CSR\) resource is used to request that a denoted signer sign the certificate\. Then, the request is either approved or denied before it's signed\. Kubernetes supports both build\-in signers and custom signers with well\-defined behaviors\. This way, clients can predict what happens to their CSRs\. To learn more about certificate signing, see [signing requests](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/)\.

One of the built\-in signers is `kubernetes.io/legacy-unknown`\. The `v1beta1` API of CSR resource honored this legacy\-unknown signer\. However, the stable `v1` API of CSR doesn't allow the `signerName` to be set to `kubernetes.io/legacy-unknown`\.

Amazon EKS version `1.21` and earlier versions allowed the value `legacy-unknown` as the `signerName` in `v1beta1` CSR API\. This API enables the Amazon EKS Certificate Authority \(CA\) to generate certificates\. However, in Kubernetes version `1.22`, the `v1beta1` CSR API is replaced by the `v1` CSR API\. This API doesn't support the signerName of “legacy\-unknown\.” Given this, if you want to use Amazon EKS CA for generating certificates on version `1.22` and later, you need to use a [custom signer]()\. It was introduced in Amazon EKS version `1.22`\. To use the CSR `v1` API version and generate a new certificate, you must migrate any existing manifests and API clients\. Existing certificates that were created with the older `v1beta1` API are valid and function until the certificate expires\. This includes the following:

1. Trust distribution: None\. There's no standard trust or distribution for this signer in a Kubernetes cluster\.

1. Permitted subjects: Any

1. Permitted x509 extensions: Honors subjectAltName and key usage extensions and discards other extensions

1. Permitted key usages: Must not include usages beyond \["key encipherment", "digital signature", "server auth"\]

1. Expiration/certificate lifetime: 1 year \(default and maximum\) 

1. CA bit allowed/disallowed: Not allowed

## Example CSR generation with signerName<a name="csr-example"></a>

These steps shows how to generate a serving certificate for DNS name `myserver.default.svc` using `signerName: beta.eks.amazonaws.com/app-serving`\. Use this as a guide for your own environment\.

1. Run the `openssl genrsa -out myserver.key 2048` command to generate an RSA private key\.

   ```
   openssl genrsa -out myserver.key 2048
   ```

1. Run the following command to generate a certificate request\.

   ```
   openssl req -new -key myserver.key -out myserver.csr -subj "/CN=myserver.default.svc"
   ```

1. Generate a `base64` value for the CSR request\. Later, you'll use this value for the `request` value in your CSR\.

   ```
   cat myserver.csr | base64 -w 0 | tr -d "\n"
   ```

1. Create a file named `mycsr.yaml` with the following contents\. In the following example, `beta.eks.amazonaws.com/app-serving` is the `signerName`\. Replace `base64-value` with the value returned in the previous step\.

   ```
   apiVersion: certificates.k8s.io/v1
   kind: CertificateSigningRequest
   metadata:
     name: myserver
   spec:
     request: base64-value
     signerName: beta.eks.amazonaws.com/app-serving
     usages:
       - digital signature
       - key encipherment
       - server auth
   ```

1. Submit the CSR\.

   ```
   kubectl apply -f mycsr.yaml
   ```

1. Approve the serving certificate\.

   ```
   kubectl certificate approve myserver
   ```

1. Verify that the certificate was issued\.

   ```
   kubectl get csr myserver
   ```

   The example output is as follows\.

   ```
   NAME       AGE     SIGNERNAME                           REQUESTOR          CONDITION
   myserver   3m20s   beta.eks.amazonaws.com/app-serving   kubernetes-admin   Approved,Issued
   ```

1. Export the issued certificate:

   ```
   kubectl get csr myserver -o jsonpath='{.status.certificate}'| base64 -d > myserver.crt
   ```

## Certificate signing considerations for Kubernetes 1\.24 and later clusters<a name="csr-considerations"></a>

In Kubernetes `1.23` and earlier, `kubelet` serving certificates with unverifiable IP and DNS Subject Alternative Names \(SANs\) were automatically issued with the unverifiable SANs omitted from the provisioned certificate\. Starting from version `1.24`, `kubelet` serving certificates will be not be issued if any SAN can't be verified\. This will prevent `kubectl` exec and `kubectl` logs commands from working\.

If you’ll be upgrading an existing `1.23` or earlier cluster, you can do the following steps to see if you'll be affected\.

1. Create a new node\.

1. Run the following command\.

   ```
   kubectl get csr -A
   ```

   If this shows a CSR with a [http://kubernetes.io/kubelet-serving](http://kubernetes.io/kubelet-serving) signer that is `Approved` but not `Issued` for your new node, then you will be affected\.

1. As a temporary workaround, find your pending CSR request using the following command\.

   ```
   kubectl get csr -A
   ```

1. Run the following command to approve the certificate\. Replace `csr-name` with your own value\.

   ```
   kubectl certificate approve csr-name
   ```

In the long term, we recommend that you write an approving controller which can automatically validate and approve CSRs which contain IP or DNS SANs that Amazon EKS is unable to verify\.