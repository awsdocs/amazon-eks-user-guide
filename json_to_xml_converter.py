#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

# XML DOCTYPE declaration to be added at the beginning of each XML file
XML_DOCTYPE = '''<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "file://zonbook/docbookx.dtd"[
    <!ENTITY % xinclude SYSTEM "file://AWSShared/common/xinclude.mod">
    %xinclude;
    <!ENTITY % phrases-code-examples SYSTEM "file://AWSShared/code-samples/docs/phrases-code-examples.ent">
    %phrases-code-examples;
    <!ENTITY % phrases-shared SYSTEM "file://AWSShared/common/phrases-shared.ent">
    %phrases-shared;
]>'''

def find_json_files(directory):
    """Find all .json files in the given directory."""
    return list(Path(directory).glob('*.json'))

def convert_json_to_xml(json_file_path, output_dir):
    """Convert a JSON file to XML with the specified DOCTYPE and userinput tag."""
    try:
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the XML content
        xml_content = f"{XML_DOCTYPE}\n<userinput>\n{content}\n</userinput>"
        
        # Create output filename by replacing .json with .xml
        output_filename = os.path.basename(json_file_path).replace('.json', '.xml')
        output_path = os.path.join(output_dir, output_filename)
        
        # Write the XML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
            
        return True
    except Exception as e:
        print(f"Error converting {json_file_path}: {e}")
        return False

def main():
    # Get the input and output directories from command line or use defaults
    input_dir = sys.argv[1] if len(sys.argv) > 1 else 'tcx5_waivers_output'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'xml_output'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Searching for JSON files in {input_dir}...")
    json_files = find_json_files(input_dir)
    print(f"Found {len(json_files)} JSON files")
    
    successful_conversions = 0
    
    for json_file in json_files:
        if convert_json_to_xml(json_file, output_dir):
            successful_conversions += 1
    
    print(f"Conversion complete. Successfully converted {successful_conversions} out of {len(json_files)} JSON files.")
    print(f"XML files have been saved to the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
