#!/usr/bin/env python3
"""
Generate metadata YAML files for XML policy files.

This script generates metadata YAML files for XML policy files in the format required
for the AWSIAMPolicyExampleReservoir package. It reads XML files from a specified
directory and creates a metadata file in the .doc_gen/metadata directory.

Usage:
    python3 generate_metadata.py

Configuration:
    Edit the constants at the top of the script to customize the metadata generation.
"""
import os
import sys
import yaml
from pathlib import Path

# Configuration constants - modify these values as needed
INPUT_DIR = 'xml_output'                                      # Directory containing XML files
OUTPUT_DIR = '.'                              # Output directory for metadata file
PACKAGE_NAME = 'AmazonEKSDocs'                                   # Doc package name
ALIAS = 'gcline'                                 # Your Amazon alias
NAME = 'EKS Documentation Team'                               # Your name
OWNER = 'AWS/Documentation/EKS'                               # Your documentation CTI
SERVICE_TITLE = 'Amazon EKS'                                  # Service name
SERVICE_URL = 'https://code.amazon.com/packages/AmazonEKSDocs'   # Link to the doc package
SYNOPSIS = 'Grants permissions for Amazon EKS operations.'    # Default synopsis for all policies

def find_xml_files(directory):
    """Find all .xml files in the given directory."""
    if os.path.exists(directory):
        return list(Path(directory).glob('*.xml'))
    else:
        print(f"Warning: Directory {directory} does not exist.")
        return []

def create_metadata_entry(xml_file, package_name, alias, name, owner, service_title, service_url, synopsis=None):
    """Create a metadata entry for an XML file."""
    # Extract the base filename without extension
    base_filename = os.path.basename(xml_file).replace('.xml', '')
    
    # Create a unique identifier for the policy
    policy_id = f"iam-policies.{package_name}.{base_filename}"
    
    # Generate a more descriptive title based on the filename
    title = ' '.join(word.capitalize() for word in base_filename.replace('_', ' ').split('-'))
    
    if not synopsis:
        synopsis = f"IAM policy example for {title.lower()}."
    
    # Create the metadata entry
    entry = {
        "category": "IAMPolicy",
        "languages": {
            "IAMPolicyGrammar": {
                "versions": [
                    {
                        "authors": [
                            {
                                "alias": alias,
                                "name": name
                            }
                        ],
                        "excerpts": [
                            {
                                "snippet_files": [
                                    f"snippet_files/{package_name}/{os.path.basename(xml_file)}"
                                ]
                            }
                        ],
                        "owner": owner,
                        "sdk_version": 1,
                        "source": {
                            "title": service_title,
                            "url": service_url
                        }
                    }
                ]
            }
        },
        "services": {
            "iam": {}
        },
        "synopsis": synopsis,
        "title": title,
        "title_abbrev": title
    }
    
    return policy_id, entry

def generate_metadata_file(xml_files, output_dir, package_name, alias, name, owner, service_title, service_url, synopsis=None):
    """Generate a metadata YAML file for the XML files."""
    metadata = {}
    
    for xml_file in xml_files:
        policy_id, entry = create_metadata_entry(
            xml_file, 
            package_name, 
            alias, 
            name, 
            owner, 
            service_title, 
            service_url,
            synopsis
        )
        metadata[policy_id] = entry
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the metadata file
    output_file = os.path.join(output_dir, f"{package_name}_metadata.yaml")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
    
    return output_file

def main():
    print(f"Searching for XML files in {INPUT_DIR}...")
    xml_files = find_xml_files(INPUT_DIR)
    print(f"Found {len(xml_files)} XML files")
    
    if not xml_files:
        print("No XML files found. Exiting.")
        return
    
    output_file = generate_metadata_file(
        xml_files,
        OUTPUT_DIR,
        PACKAGE_NAME,
        ALIAS,
        NAME,
        OWNER,
        SERVICE_TITLE,
        SERVICE_URL,
        SYNOPSIS
    )
    
    print(f"Metadata file generated: {output_file}")
    print(f"Generated metadata for {len(xml_files)} XML files.")
    print("\nTo use this metadata file:")
    print(f"1. Copy the XML files to the AWSIAMPolicyExampleReservoir package under snippet_files/{PACKAGE_NAME}/")
    print(f"2. Copy the metadata file to the AWSIAMPolicyExampleReservoir package under .doc_gen/metadata/")
    print("3. Include the policies in your documentation using xi:include")

if __name__ == "__main__":
    main()
