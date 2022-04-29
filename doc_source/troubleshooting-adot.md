# Troubleshooting issues in ADOT Amazon EKS add\-on<a name="troubleshooting-adot"></a>

This topic covers some of the common errors that you might encounter while using the ADOT Amazon EKS add\-on, including instructions on how to resolve them, workarounds, and frequently asked questions\.

## Common issues<a name="adot-symptoms"></a>

This section describes functional issues that you might encounter while using ADOT Amazon EKS add=on and troubleshooting steps\.

### error:` "code": "K8sResourceNotFound", "message": "cert-manager is not installed on this cluster. During preview, you are required to have previously installed cert-manager."`<a name="adot-cert"></a>

Ensure that the [cert\-manager](https://cert-manager.io/docs/) version installed is supported by the ADOT Amazon EKS add\-on and under version 1\.6\.0\.

### error:` "code": "AccessDenied", "message": "roles.rbac.authorization.k8s.io \"opentelemetry-operator-leader-election-role\" is forbidden: User \"eks:addon-manager\" cannot patch resource \"roles\" in API group \"rbac.authorization.k8s.io\" in the namespace \"opentelemetry-operator-system\"`<a name="adot-perm"></a>

You do not have permission to install the ADOT for Amazon EKS add\-on\. See [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](adot-manage.md#adot-install)\. If you have deleted the add\-on and are now reinstalling, ensure that you have [applied permissions](adot-reqts.md)\.

### Create add\-on error:` "status": "CREATE_FAILED"`<a name="adot-createfailed"></a>
+ Possibly a conflict\. You can overwrite conflicts by adding the flag: `--resolve-conflicts=OVERWRITE` and run the create command again\.
+ An unsupported architecture, such as ARM64\. Consult your logs to determine if this is the case\.

### Delete add\-on error:` "status": "DELETE_FAILED"`<a name="adot-deletefailed"></a>

You can remove the ADOT Operator from being managed by Amazon EKS add\-ons by adding the `--preserve` flag to your delete command\.