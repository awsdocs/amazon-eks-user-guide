--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Verifying a container image during deployment<a name="image-verification"></a>
+  [Gatekeeper and Ratify](https://ratify.dev/docs/1.0/quickstarts/ratify-on-aws) – Use Gatekeeper as the admission controller and Ratify configured with an AWS Signer plugin as a web hook for validating signatures\.
+  [Kyverno](https://github.com/nirmata/kyverno-notation-aws) – A Kubernetes policy engine configured with an AWS Signer plugin for validating signatures\.

**Note**  
Before verifying container image signatures, configure the [Notation](https://github.com/notaryproject/notation#readme) trust store and trust policy, as required by your selected admission controller\.