# Configuring VT1 for your custom Amazon Linux AMI<a name="vt1"></a>

Custom Amazon Linux AMIs in Amazon EKS can support the VT1 video transcoding instance family for Amazon Linux 2 \(AL2\), Ubuntu 18, and Ubuntu 20\. VT1 supports the Xilinx U30 media transcoding cards with accelerated H\.264/AVC and H\.265/HEVC codecs\. To get the benefit of these accelerated instances, you must follow these steps: 

1. Create and launch a base AMI from AL2, Ubuntu 18, or Ubuntu 20\.

1. After the based AMI is launched, Install the [XRT driver](https://xilinx.github.io/video-sdk/) and runtime on the node\.

1. [Creating an Amazon EKS cluster](create-cluster.md)\.

1. Install the Kubernetes [FPGA plugin](https://github.com/Xilinx/FPGA_as_a_Service/tree/master/k8s-device-plugin) on your cluster\.

   ```
   kubectl apply -f fpga-device-plugin.yml
   ```

The plugin will now advertise Xilinx U30 devices per node on your Amazon EKS cluster\. You can use the FFMPEG docker image to run example video transcoding workloads on your Amazon EKS cluster\.