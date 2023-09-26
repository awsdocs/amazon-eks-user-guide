# Verifying a container image during deployment<a name="image-verification"></a>

If you use [AWS Signer](https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html) and want to verify signed container images at the time of deployment, you can use one of the following solutions:
+ [https://ratify.dev/docs/1.0/quickstarts/ratify-on-aws](https://ratify.dev/docs/1.0/quickstarts/ratify-on-aws) – Use Gatekeeper as the admission controller and Ratify configured with an AWS Signer plugin as a web hook for validating signatures\.
+ [https://github.com/nirmata/kyverno-notation-aws](https://github.com/nirmata/kyverno-notation-aws) – A Kubernetes policy engine configured with an AWS Signer plugin for validating signatures\.

**Note**  
Before verifying container image signatures, configure the [Notation](https://github.com/notaryproject/notation#readme) trust store and trust policy, as required by your selected admission controller\.