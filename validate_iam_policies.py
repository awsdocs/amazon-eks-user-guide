#!/usr/bin/env python3

import os
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime
import concurrent.futures
from tqdm import tqdm

# Directory containing the extracted JSON policy files
JSON_DIR = "latest/ug/iam-json"
# Output file for validation results
OUTPUT_FILE = "policy_validation_results.txt"

def find_json_files(directory):
    """Find all .json files in the directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)

def preprocess_policy(json_file):
    """
    Read the policy file, replace placeholders with valid values, and return the processed content.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholders with valid values
        processed_content = content.replace('{arn-aws}', 'arn:aws:')
        processed_content = processed_content.replace('<account-id>', '123456789012')
        processed_content = processed_content.replace('{aws}', 'aws')
        processed_content = processed_content.replace('<aws-region>', 'us-east-1')
        processed_content = processed_content.replace('AWS_REGION', 'us-east-1')
        processed_content = processed_content.replace('region-code', 'us-east-1')
        processed_content = processed_content.replace('AWS_ACCOUNT_ID', '123456789012')
        processed_content = processed_content.replace('TRUST_ANCHOR_ARN', 'arn:aws:rolesanywhere:us-east-1:123456789012:trust-anchor/TA_ID')
        processed_content = processed_content.replace('TRUST_ANCHOR_ID', 'arn:aws:rolesanywhere:us-east-1:123456789012:trust-anchor/TA_ID')
        processed_content = processed_content.replace('custom-key-arn', 'arn:aws:kms:us-east-1:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab')
        
        return processed_content
    except Exception as e:
        return None, str(e)

def detect_policy_type(policy_content):
    """
    Detect if a policy is a resource policy or an identity policy.
    Resource policies typically have a "Principal" element.
    Identity policies typically don't have a "Principal" element.
    """
    try:
        policy = json.loads(policy_content)
        
        # Check if this is a policy document with a Statement
        if "Statement" not in policy:
            # Default to identity policy if we can't determine
            return "IDENTITY_POLICY"
        
        # Check if any statement has a Principal element
        statements = policy["Statement"]
        if not isinstance(statements, list):
            statements = [statements]
        
        for statement in statements:
            if "Principal" in statement:
                return "RESOURCE_POLICY"
        
        # If no Principal is found, it's likely an identity policy
        return "IDENTITY_POLICY"
    except Exception as e:
        # Default to identity policy if we can't parse the JSON
        return "IDENTITY_POLICY"

def validate_policy(json_file):
    """Run AWS Access Analyzer validate-policy on the JSON file with preprocessing."""
    try:
        # Preprocess the policy file
        processed_content = preprocess_policy(json_file)
        
        # Auto-detect policy type
        policy_type = detect_policy_type(processed_content)
        
        # Create a temporary file with the processed content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(processed_content)
        
        try:
            cmd = [
                "aws", "accessanalyzer", "validate-policy",
                "--policy-document", f"file://{temp_file_path}",
                "--policy-type", policy_type
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            
            # Try to parse the output as JSON
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    # Add the detected policy type to the result
                    output["policy_type"] = policy_type
                    return output
                except json.JSONDecodeError:
                    return {"error": "Failed to parse JSON output", "stdout": result.stdout, "stderr": result.stderr}
            else:
                return {"error": "No output from command", "stderr": result.stderr}
        
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    except Exception as e:
        return {"error": str(e)}

def format_findings(findings):
    """Format the findings into a readable string."""
    if not findings:
        return "No findings."
    
    result = []
    for finding in findings:
        finding_type = finding.get("findingType", "Unknown")
        finding_details = finding.get("findingDetails", "No details")
        locations = finding.get("locations", [])
        
        result.append(f"Finding Type: {finding_type}")
        result.append(f"Details: {finding_details}")
        
        if locations:
            result.append("Locations:")
            for location in locations:
                path = location.get("path", [])
                span = location.get("span", {})
                path_str = " > ".join(str(p) for p in path) if path else "N/A"
                start = span.get("start", {})
                end = span.get("end", {})
                start_str = f"line {start.get('line', 'N/A')}, col {start.get('column', 'N/A')}"
                end_str = f"line {end.get('line', 'N/A')}, col {end.get('column', 'N/A')}"
                
                result.append(f"  Path: {path_str}")
                result.append(f"  Span: {start_str} to {end_str}")
        
        result.append("")  # Empty line between findings
    
    return "\n".join(result)

def process_file(json_file):
    """Process a single JSON file and return the results."""
    rel_path = os.path.relpath(json_file)
    output = []
    
    # Initialize findings_count to avoid reference before assignment
    findings_count = 0
    
    # File header
    output.append(f"File: {rel_path}")
    output.append("-" * 80)
    
    # Check if the file contains placeholders
    with open(json_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
        has_arn_placeholder = '{arn-aws}' in original_content
        has_account_placeholder = '<account-id>' in original_content
        has_aws_placeholder = '{aws}' in original_content
        has_region_placeholder = '<aws-region>' in original_content
        has_aws_region_placeholder = 'AWS_REGION' in original_content
        has_region_code_placeholder = 'region-code' in original_content
        has_aws_account_id_placeholder = 'AWS_ACCOUNT_ID' in original_content
        has_trust_anchor_id_placeholder = 'TRUST_ANCHOR_ID' in original_content
        has_custom_key_arn_placeholder = 'custom-key-arn' in original_content
    
    if has_arn_placeholder or has_account_placeholder or has_aws_placeholder or has_region_placeholder or has_aws_region_placeholder or has_region_code_placeholder or has_aws_account_id_placeholder or has_trust_anchor_id_placeholder or has_custom_key_arn_placeholder:
        output.append("Note: Replaced placeholders for validation:")
        if has_arn_placeholder:
            output.append("  - {arn-aws} → arn:aws:")
        if has_account_placeholder:
            output.append("  - <account-id> → 123456789012")
        if has_aws_placeholder:
            output.append("  - {aws} → aws")
        if has_region_placeholder:
            output.append("  - <aws-region> → us-east-1")
        if has_aws_region_placeholder:
            output.append("  - AWS_REGION → us-east-1")
        if has_region_code_placeholder:
            output.append("  - region-code → us-east-1")
        if has_aws_account_id_placeholder:
            output.append("  - AWS_ACCOUNT_ID → 123456789012")
        if has_trust_anchor_id_placeholder:
            output.append("  - TRUST_ANCHOR_ID → arn:aws:rolesanywhere:us-east-1:123456789012:trust-anchor/TA_ID")
        if has_custom_key_arn_placeholder:
            output.append("  - custom-key-arn → arn:aws:kms:us-east-1:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab")
        output.append("")
    
    # Validate the policy
    result = validate_policy(json_file)
    
    policy_type = result.get("policy_type", "UNKNOWN")
    
    output.append(f"Policy Type: {policy_type}")
    
    if "error" in result:
        output.append(f"Error: {result['error']}")
        if "stderr" in result:
            output.append(f"Details: {result['stderr']}")
    else:
        # Filter out SUGGESTION findings
        all_findings = result.get("findings", [])
        findings = [f for f in all_findings if f.get("findingType") != "SUGGESTION"]
        
        # Suppress "Add a Resource or NotResource element" finding for trust policies (policies with Principal)
        resource_findings_suppressed = 0
        if policy_type == "RESOURCE_POLICY":
            # Count findings before suppression
            before_count = len(findings)
            
            # Filter out the specific finding for trust policies
            findings = [f for f in findings if not (
                f.get("findingDetails", "").strip() == "Add a Resource or NotResource element to the policy statement."
            )]
            
            # Calculate how many findings were suppressed
            resource_findings_suppressed = before_count - len(findings)
            
            if resource_findings_suppressed > 0:
                output.append(f"Suppressed {resource_findings_suppressed} 'Resource element' finding(s) for trust policy.")
        
        findings_count = len(findings)
        suggestions_count = len(all_findings) - len([f for f in all_findings if f.get("findingType") != "SUGGESTION"])
        
        if suggestions_count > 0:
            output.append(f"Suppressed {suggestions_count} suggestion(s).")
        
        if findings:
            output.append(f"Found {findings_count} issues:\n")
            output.append(format_findings(findings))
        else:
            output.append("No issues found. Policy is valid.")
    
    output.append("\n" + "=" * 80 + "\n")
    
    return {
        "output": "\n".join(output),
        "has_findings": findings_count > 0,
        "findings_count": findings_count,
        "policy_type": policy_type
    }

def main():
    # Ensure the JSON_DIR exists
    if not os.path.exists(JSON_DIR):
        print(f"Error: Directory {JSON_DIR} does not exist.")
        sys.exit(1)
    
    # Find all JSON files
    json_files = list(find_json_files(JSON_DIR))
    total_files = len(json_files)
    
    print(f"Found {total_files} policy files to validate.")
    
    # Process files in parallel with a progress bar
    results = []
    files_with_findings = 0
    total_findings = 0
    identity_policies = 0
    resource_policies = 0
    
    # Determine the number of workers (adjust based on your system)
    max_workers = min(32, os.cpu_count() + 4)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and create a mapping of futures to file paths for the progress bar
        future_to_file = {executor.submit(process_file, json_file): json_file for json_file in json_files}
        
        # Process results as they complete with a progress bar
        with tqdm(total=total_files, desc="Validating policies", unit="file") as progress_bar:
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result["has_findings"]:
                        files_with_findings += 1
                        total_findings += result["findings_count"]
                    
                    # Count policy types
                    if result["policy_type"] == "IDENTITY_POLICY":
                        identity_policies += 1
                    elif result["policy_type"] == "RESOURCE_POLICY":
                        resource_policies += 1
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                
                progress_bar.update(1)
    
    # Sort results to maintain a consistent order in the output file
    results.sort(key=lambda x: x["output"].split("\n")[0])
    
    # Write results to the output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        # Write header with nicely formatted summary at the top
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        out_file.write(f"IAM Policy Validation Results\n")
        out_file.write(f"Generated: {timestamp}\n")
        out_file.write("=" * 80 + "\n\n")
        
        # Write summary at the top
        out_file.write("SUMMARY\n")
        out_file.write("-" * 80 + "\n")
        out_file.write(f"Total files validated:  {total_files}\n")
        out_file.write(f"Files with findings:    {files_with_findings}\n")
        out_file.write(f"Total findings:         {total_findings}\n")
        out_file.write(f"Identity policies:      {identity_policies}\n")
        out_file.write(f"Resource policies:      {resource_policies}\n")
        out_file.write("-" * 80 + "\n\n")
        
        out_file.write(f"Found {total_files} policy files to validate.\n\n")
        
        # Write detailed results, but skip files with no errors or only suppressed suggestions
        for result in results:
            # Only output detailed results if there are findings
            if result["has_findings"]:
                out_file.write(result["output"])
        
        # Write summary at the bottom too for reference
        out_file.write(f"Summary:\n")
        out_file.write(f"Total files validated: {total_files}\n")
        out_file.write(f"Files with findings: {files_with_findings}\n")
        out_file.write(f"Total findings: {total_findings}\n")
        out_file.write(f"Identity policies: {identity_policies}\n")
        out_file.write(f"Resource policies: {resource_policies}\n")
    
    print(f"Validation complete. Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
