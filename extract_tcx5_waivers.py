#!/usr/bin/env python3
import os
import json
import re
import sys
from pathlib import Path

# Dictionary of placeholders and their replacements
PLACEHOLDERS = {
    '{arn-aws}': 'arn:aws:',
    '<account-id>': '123456789012',
    '{aws}': 'aws',
    '<aws-region>': 'us-east-1',
    'AWS_REGION': 'us-east-1',
    'region-code': 'us-east-1',
    'AWS_ACCOUNT_ID': '123456789012',
    'TRUST_ANCHOR_ARN': 'arn:aws:rolesanywhere:us-east-1:123456789012:trust-anchor/TA_ID',
    'TRUST_ANCHOR_ID': 'arn:aws:rolesanywhere:us-east-1:123456789012:trust-anchor/TA_ID',
    'custom-key-arn': 'arn:aws:kms:us-east-1:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab',
    '<111122223333>': '123456789012',
    '<region-code>': 'us-east-1',
    '<EXAMPLED539D4633E53DE1B71EXAMPLE>': 'EXAMPLED539D4633E53DE1B71EXAMPLE',
    '$account_id': '123456789012',
    '<Namespace>': 'Namespace',
    '<ServiceAccount>': 'ServiceAccount',
    '<us-east-1>': 'us-east-1'
}

def preprocess_policy(policy_content):
    """
    Process a policy string, replace placeholders with valid values.
    """
    # Replace all placeholders using the dictionary
    processed_content = policy_content
    for placeholder, replacement in PLACEHOLDERS.items():
        processed_content = processed_content.replace(placeholder, replacement)
    
    return processed_content

def find_adoc_files(root_dir):
    """Find all .adoc files in the given directory recursively."""
    return list(Path(root_dir).glob('**/*.adoc'))

def extract_waiver_content(file_path):
    """Extract content between ---- markers around {tcx5-waiver} instances."""
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all instances of {tcx5-waiver}
        waiver_positions = [m.start() for m in re.finditer(r'\{tcx5-waiver\}', content)]
        
        if not waiver_positions:
            return []
            
        lines = content.split('\n')
        line_positions = [0]
        current_pos = 0
        
        # Calculate the position of each line start in the content
        for line in lines:
            current_pos += len(line) + 1  # +1 for the newline character
            line_positions.append(current_pos)
        
        for waiver_pos in waiver_positions:
            # Find which line contains the waiver
            waiver_line_idx = next(i for i, pos in enumerate(line_positions) if pos > waiver_pos) - 1
            
            # Search backwards for the preceding ---- marker
            start_line_idx = None
            for i in range(waiver_line_idx, -1, -1):
                if lines[i].strip() == '----':
                    start_line_idx = i
                    break
            
            if start_line_idx is None:
                print(f"Warning: Could not find starting ---- marker for {{tcx5-waiver}} at line {waiver_line_idx + 1} in {file_path}")
                continue
                
            # Search forwards for the following ---- marker
            end_line_idx = None
            for i in range(waiver_line_idx + 1, len(lines)):
                if lines[i].strip() == '----':
                    end_line_idx = i
                    break
            
            if end_line_idx is None:
                print(f"Warning: Could not find ending ---- marker for {{tcx5-waiver}} at line {waiver_line_idx + 1} in {file_path}")
                continue
            
            # Extract the content between the markers (excluding the markers themselves)
            extracted_content = lines[start_line_idx + 1:end_line_idx]
            
            # Remove {tcx5-waiver} from the extracted content and filter out lines starting with "cat >" or "EOF"
            cleaned_content = []
            for line in extracted_content:
                cleaned_line = line.replace('{tcx5-waiver}', '')
                # Skip lines that begin with "cat >" or "EOF"
                if not cleaned_line.strip().startswith(("cat >", "EOF")):
                    cleaned_content.append(cleaned_line)
            
            results.append({
                'file': str(file_path),
                'raw_content': cleaned_content
            })
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        
    return results

def main():
    # Get the root directory from command line or use current directory
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'tcx5_waivers_output'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Searching for .adoc files in {root_dir}...")
    adoc_files = find_adoc_files(root_dir)
    print(f"Found {len(adoc_files)} .adoc files")
    
    total_waivers = 0
    file_counter = 0
    
    for file_path in adoc_files:
        file_counter += 1
        if file_counter % 50 == 0:
            print(f"Processed {file_counter}/{len(adoc_files)} files...")
            
        waivers = extract_waiver_content(file_path)
        
        for i, waiver in enumerate(waivers):
            total_waivers += 1
            # Create a unique filename based on the source file and position
            base_filename = os.path.basename(file_path).replace('.adoc', '')
            output_filename = f"{base_filename}_waiver_{i+1}.json"
            output_path = os.path.join(output_dir, output_filename)
            
            # Check if the content contains any placeholders
            raw_content = '\n'.join(waiver['raw_content'])
            found_placeholders = [placeholder for placeholder in PLACEHOLDERS if placeholder in raw_content]
            
            if found_placeholders:
                print(f"Found placeholders in {output_filename}: {', '.join(found_placeholders)}")
                # Replace placeholders with their values
                processed_content = preprocess_policy(raw_content)
                # Write the processed content to the file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
            else:
                # Write the raw content directly to the file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(raw_content)
    
    print(f"Extraction complete. Found {total_waivers} instances of {{tcx5-waiver}} across {len(adoc_files)} files.")
    print(f"JSON files have been saved to the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
