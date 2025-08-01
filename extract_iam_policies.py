#!/usr/bin/env python3

import os
import re
import json
import sys
from pathlib import Path

# Directory to search for .adoc files
UG_DIR = "latest/ug"
# Directory to save extracted JSON files
JSON_DIR = "latest/ug/iam-json"

def is_iam_policy(json_str):
    """Check if the JSON string is an IAM policy."""
    try:
        policy = json.loads(json_str)
        # Check for common IAM policy elements
        if isinstance(policy, dict) and any(key in policy for key in ["Statement", "Version"]):
            # Further check if Statement is present and is a list or dict
            if "Statement" in policy and (isinstance(policy["Statement"], list) or isinstance(policy["Statement"], dict)):
                return True
    except json.JSONDecodeError:
        pass
    return False

def extract_json_blocks(file_path):
    """Extract JSON code blocks from an .adoc file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match JSON code blocks in AsciiDoc
    # This pattern looks for blocks that start with [source,json] or similar
    # and captures the JSON content between ---- delimiters
    pattern = r'(?:\[source(?:,|\s+)(?:json|JSON)(?:\s*,.*?)?\])\s*?(?:----+)\s*([\s\S]*?)(?:----+)'
    
    matches = re.finditer(pattern, content)
    
    results = []
    for match in matches:
        json_block = match.group(1).strip()
        if is_iam_policy(json_block):
            results.append({
                'json': json_block,
                'start': match.start(),
                'end': match.end(),
                'full_match': match.group(0)
            })
    
    return results, content

def generate_filename(file_path, index):
    """Generate a filename for the extracted JSON."""
    base_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(base_name)[0]
    return f"{name_without_ext}-policy-{index}.json"

def process_file(file_path):
    """Process a single .adoc file."""
    print(f"Processing {file_path}")
    
    json_blocks, original_content = extract_json_blocks(file_path)
    
    if not json_blocks:
        print(f"  No IAM policy JSON blocks found in {file_path}")
        return
    
    print(f"  Found {len(json_blocks)} IAM policy JSON blocks")
    
    # Make a copy of the content that we'll modify
    modified_content = original_content
    
    # Process each JSON block, starting from the end to avoid messing up offsets
    for i, block in reversed(list(enumerate(json_blocks))):
        json_str = block['json']
        
        # Generate filename for this JSON
        rel_path = os.path.relpath(file_path, UG_DIR)
        dir_part = os.path.dirname(rel_path)
        json_filename = generate_filename(file_path, i + 1)
        
        # Create subdirectory structure in JSON_DIR if needed
        if dir_part:
            json_subdir = os.path.join(JSON_DIR, dir_part)
            os.makedirs(json_subdir, exist_ok=True)
            json_filepath = os.path.join(json_subdir, json_filename)
        else:
            json_filepath = os.path.join(JSON_DIR, json_filename)
        
        # Write JSON to file
        with open(json_filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        print(f"  Extracted policy to {json_filepath}")
        
        # Calculate the relative path from the original file to the JSON file
        rel_json_path = os.path.relpath(json_filepath, os.path.dirname(file_path))
        
        # Create the include directive
        include_directive = f"[source,json]\n----\ninclude::{rel_json_path}[]\n----"
        
        # Replace the original JSON block with the include directive
        modified_content = modified_content[:block['start']] + include_directive + modified_content[block['end']:]
    
    # Write the modified content back to the file
    if modified_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"  Updated {file_path} with include directives")

def find_adoc_files(directory):
    """Find all .adoc files in the directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.adoc'):
                yield os.path.join(root, file)

def main():
    # Ensure JSON_DIR exists
    os.makedirs(JSON_DIR, exist_ok=True)
    
    # Find and process all .adoc files
    count = 0
    for file_path in find_adoc_files(UG_DIR):
        process_file(file_path)
        count += 1
    
    print(f"Processed {count} .adoc files")

if __name__ == "__main__":
    main()
