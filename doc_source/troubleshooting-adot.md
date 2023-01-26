# Troubleshooting issues in ADOT Amazon EKS add\-on<a name="troubleshooting-adot"></a>

This topic covers some of the common errors that you might encounter while using the AWS Distro for OpenTelemetry \(ADOT\) Amazon EKS add\-on\. The topic also includes instructions on how to resolve or workaround the common errors\.

## Error:` "code": "AccessDenied", "message": "roles.rbac.authorization.k8s.io \"opentelemetry-operator-leader-election-role\" is forbidden: User \"eks:addon-manager\" cannot patch resource \"roles\" in API group \"rbac.authorization.k8s.io\" in the namespace \"opentelemetry-operator-system\"`<a name="adot-perm"></a>

You don't have permission to install the ADOT for Amazon EKS add\-on\. See [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](adot-manage.md#adot-install)\. If you have deleted the add\-on and are now reinstalling, make sure that you have [applied the required permissions](adot-reqts.md)\.

## Error: `"status": "CREATE_FAILED"` or `"status": "UPDATE_FAILED"`<a name="adot-createfailed"></a>

This can happen due to the following reasons:
+ There might be a conflict\. You can overwrite conflicts by adding the `--resolve-conflicts=OVERWRITE` flag and running the `create` command again\.
+ If you're using an add\-on version earlier than `v0.51.0`, you may be on an unsupported architecture, such as `arm64`\. Consult your logs to determine if this is the case\. If so, updating your add\-on version may resolve this issue because `v0.51.0` and later are multi\-arch\.

## Delete add\-on error: `"status": "DELETE_FAILED"`<a name="adot-deletefailed"></a>

You can remove Amazon EKS management of the ADOT Operator add\-on by adding the `--preserve` flag to your `aws eks delete-addon` command\.