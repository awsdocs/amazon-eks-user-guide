# Set up AWS CLI<a name="install-awscli"></a>

## <a name="w24aac15c12b3"></a>

The [AWS CLI](https://aws.amazon.com/cli/) is a command line tool for working with AWS services, including Amazon EKS\. It is also used to authenticate IAM users or roles for access to the Amazon EKS cluster and other AWS resources from your local machine\. To provision resources in AWS from the command line, you need to obtain an AWS access key ID and secret key to use in the command line\. Then you need to configure these credentials in the AWS CLI\. If you haven't already installed the AWS CLI, see [Install or update the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

### To create an access key<a name="w24aac15c12b3b3"></a>

1. Sign into the [AWS Management Console](https://console.aws.amazon.com/)\.

1. In the top right, choose your AWS user name to open the navigation menu\. For example, choose **`webadmin`**\. Then choose **Security credentials**\.

1. Under **Access keys**, choose **Create access key**\.

1. Choose **Command Line Interface \(CLI\)**, then choose **Next**\.

1. Choose **Create access key**\.

1. Choose **Download \.csv file**\.

### To configure the AWS CLI<a name="w24aac15c12b3b5"></a>

After installing the AWS CLI, do the following steps to configure it\. For more information, see [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the *AWS Command Line Interface User Guide*\.

1. In a terminal window, enter the following command:

   ```
   aws configure
   ```

   Optionally, you can configure a named profile, such as `--profile cluster-admin`\. If you configure a named profile in the AWS CLI, you must **always** pass this flag in subsequent commands\.

1. Enter your AWS credentials\. For example:

   ```
   AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
   AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   Default region name [None]: region-code
   Default output format [None]: json
   ```

### To get a security token<a name="w24aac15c12b3b7"></a>

If needed, run the following command to get a new security token for the AWS CLI\. For more information, see [https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html](https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html) in the *AWS CLI Command Reference*\.

By default, the token is valid for 15 minutes\. To change the default session timeout, pass the `--duration-seconds` flag\. For example:

```
aws sts get-session-token --duration-seconds 3600
```

This command returns the temporary security credentials for an AWS CLI session\. You should see the following response output:

```
{
    "Credentials": {
        "AccessKeyId": "ASIA5FTRU3LOEXAMPLE",
        "SecretAccessKey": "JnKgvwfqUD9mNsPoi9IbxAYEXAMPLE",
        "SessionToken": "VERYLONGSESSIONTOKENSTRING",
        "Expiration": "2023-02-17T03:14:24+00:00"
    }
}
```

### To verify the user identity<a name="w24aac15c12b3b9"></a>

If needed, run the following command to verify the AWS credentials for your IAM user identity \(such as `ClusterAdmin`\) for the terminal session\.

```
aws sts get-caller-identity
```

This command returns the Amazon Resource Name \(ARN\) of the IAM entity that's configured for the AWS CLI\. You should see the following example response output:

```
{
    "UserId": "AKIAIOSFODNN7EXAMPLE",
    "Account": "01234567890",
    "Arn": "arn:aws:iam::01234567890:user/ClusterAdmin"
}
```

## Next steps<a name="install-awscli-next-steps"></a>
+ [Set up `kubectl` and `eksctl`](install-kubectl.md)
+ [Quickstart: Deploy a web app and store data](quickstart.md)