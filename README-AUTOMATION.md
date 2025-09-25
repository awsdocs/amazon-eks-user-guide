# README-AUTOMATION.md
This file includes details about generating automated content in this package.

## NAME: GitHub Sync Script
**RUN INSTRUCTIONS:** [Instructions for running the GitHub sync script (Quip/WorkDocs link)](https://quip-amazon.com/PL0vAsCa3p10/How-to-Run-the-GitHub-Sync-Script-AmazonEKSDocs)  

**SCRIPT/CODE LOCATION:** [`sync-github.sh`](./sync-github.sh)  
The script is located at the top level of this package.

**DOC PAGES:** [Amazon EKS User Guide – GitHub Repository](https://github.com/awsdocs/amazon-eks-user-guide)  
The script keeps the public GitHub repo (`awsdocs/amazon-eks-user-guide`) in sync with the internal GitFarm repository for the Amazon EKS User Guide. Unlike most other AWS documentation, the EKS User Guide is open source. For this reason, it is important to run the sync script **regularly (at least once or twice a week, if not more often)** to ensure contributions and changes remain aligned between the public and internal repositories.