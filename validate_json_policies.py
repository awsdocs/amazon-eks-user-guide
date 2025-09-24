#!/usr/bin/env python3

import os
import json
import sys
import tempfile
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import concurrent.futures
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import time

# Output file for validation results
OUTPUT_FILE = "json_policy_validation_results.txt"

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

# Cache for policy validation results to avoid repeated validations of the same policy
policy_validation_cache = {}

def validate_policy(policy_content):
    """Run AWS Access Analyzer validate-policy on the policy content."""
    # Use cache if we've already validated this exact policy
    if policy_content in policy_validation_cache:
        return policy_validation_cache[policy_content]
        
    try:
        # Auto-detect policy type (CPU-bound but lightweight)
        policy_type = detect_policy_type(policy_content)
        
        # Create a temporary file with the processed content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(policy_content)
        
        try:
            # Add timeout to subprocess to avoid hanging
            # This is a network-bound operation (calling AWS CLI)
            cmd = [
                "aws", "accessanalyzer", "validate-policy",
                "--policy-document", f"file://{temp_file_path}",
                "--policy-type", policy_type
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,  # Don't raise exception on non-zero exit
                timeout=45    # Increased timeout for network operations
            )
            
            # Try to parse the output as JSON
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    # Add the detected policy type to the result
                    output["policy_type"] = policy_type
                    
                    # Cache the result to avoid repeated validations
                    policy_validation_cache[policy_content] = output
                    
                    return output
                except json.JSONDecodeError:
                    error_result = {"error": "Failed to parse JSON output", "stdout": result.stdout, "stderr": result.stderr}
                    policy_validation_cache[policy_content] = error_result
                    return error_result
            else:
                error_result = {"error": "No output from command", "stderr": result.stderr}
                policy_validation_cache[policy_content] = error_result
                return error_result
        
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    except subprocess.TimeoutExpired:
        error_result = {"error": "Command timed out after 45 seconds"}
        policy_validation_cache[policy_content] = error_result
        return error_result
    except Exception as e:
        error_result = {"error": str(e)}
        policy_validation_cache[policy_content] = error_result
        return error_result

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

def process_policy(policy_content, source_file, policy_index=1):
    """Process a single policy and return the validation results."""
    # Initialize the output list
    output = []
    rel_path = os.path.relpath(source_file)
    
    # File and policy header
    output.append(f"File: {rel_path}")
    output.append("-" * 80)
    
    # Check if the policy contains any placeholders using the dictionary keys
    found_placeholders = [placeholder for placeholder in PLACEHOLDERS if placeholder in policy_content]
    
    if found_placeholders:
        output.append("Note: Replaced placeholders for validation:")
        for placeholder in found_placeholders:
            output.append(f"  - {placeholder} → {PLACEHOLDERS[placeholder]}")
        output.append("")
    
    # Preprocess the policy
    processed_policy = preprocess_policy(policy_content)
    
    # Validate the processed policy
    result = validate_policy(processed_policy)
    
    policy_type = result.get("policy_type", "UNKNOWN")
    output.append(f"Policy Type: {policy_type}")
    
    # Initialize findings_count to avoid reference before assignment
    findings_count = 0
    
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

def find_json_files(directory):
    """Find all .json files in the directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)

def process_json_file(file_path):
    """Process a single JSON file and validate it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            policy_content = f.read()
        
        # Validate the JSON format
        try:
            json.loads(policy_content)
        except json.JSONDecodeError as e:
            return {
                "output": f"File: {os.path.relpath(file_path)}\n{'-' * 80}\nError: Invalid JSON format - {str(e)}\n{'=' * 80}\n",
                "has_findings": True,
                "findings_count": 1,
                "policy_type": "UNKNOWN"
            }
        
        # Process the policy
        return process_policy(policy_content, file_path)
    except Exception as e:
        return {
            "output": f"File: {os.path.relpath(file_path)}\n{'-' * 80}\nError processing file: {str(e)}\n{'=' * 80}\n",
            "has_findings": True,
            "findings_count": 1,
            "policy_type": "UNKNOWN"
        }

def main():
    """Main function to run the validation on JSON files."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Validate IAM policies in JSON files')
    parser.add_argument('directory', help='Directory containing JSON policy files to validate')
    parser.add_argument('--ci', action='store_true', help='Run in CI mode with machine-readable output')
    parser.add_argument('--output', default=OUTPUT_FILE, help=f'Output file for results (default: {OUTPUT_FILE})')
    args = parser.parse_args()
    
    start_time = time.time()
    
    # Ensure directory exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory {args.directory} does not exist.")
        sys.exit(1)
    
    # Find all .json files
    json_files = list(find_json_files(args.directory))
    total_files = len(json_files)
    
    if total_files == 0:
        print(f"No JSON files found in {args.directory}")
        sys.exit(0)
    
    print(f"Found {total_files} JSON files to validate.")
    
    # Prepare for statistics collection
    all_results = []
    files_with_findings = 0
    total_findings = 0
    identity_policies = 0
    resource_policies = 0
    
    # Use tqdm's thread_map for parallel processing with progress bar
    max_workers = min(20, total_files, os.cpu_count() * 4)  # Limit concurrent workers
    validation_results = thread_map(
        process_json_file,
        json_files,
        max_workers=max_workers,
        desc="Validating policies",
        unit="file"
    )
    
    # Filter out None values (from errors)
    all_results = [result for result in validation_results if result]
    
    # Count statistics from all results
    for result in all_results:
        # Count files with findings and total findings
        if result["has_findings"]:
            files_with_findings += 1
            total_findings += result["findings_count"]
        
        # Count policy types
        if result["policy_type"] == "IDENTITY_POLICY":
            identity_policies += 1
        elif result["policy_type"] == "RESOURCE_POLICY":
            resource_policies += 1
    
    # Sort results to maintain a consistent order in the output file
    all_results.sort(key=lambda x: x["output"].split("\n")[0] if "output" in x else "")
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Write results to the output file
    with open(args.output, 'w', encoding='utf-8') as out_file:
        if args.ci:
            # CI mode: Simplified output optimized for GitHub Actions
            out_file.write(f"TOTAL_FINDINGS={total_findings}\n")
            
            # Output details of any findings for easier debugging
            if total_findings > 0:
                out_file.write("\nDETAILED_FINDINGS:\n")
                for result in all_results:
                    if result.get("has_findings", False):
                        file_path = result["output"].split("\n")[0].split(":")[1].strip()
                        out_file.write(f"- {file_path}: {result['findings_count']} issue(s)\n")
                
                # Add detailed findings
                for result in all_results:
                    if result.get("has_findings", False):
                        out_file.write(result["output"])
            
            print(f"CI validation complete: Found {total_findings} issues in {total_files} policies")
            # Exit with non-zero code if findings exist (for GitHub Actions)
            if total_findings > 0:
                print("::error::IAM policy validation failed with findings")
                sys.exit(1)
        else:
            # Standard human-readable mode
            # Write header with nicely formatted summary at the top
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            out_file.write(f"IAM Policy Validation Results\n")
            out_file.write(f"Generated: {timestamp}\n")
            out_file.write("=" * 80 + "\n\n")
            
            # Write summary at the top
            out_file.write("SUMMARY\n")
            out_file.write("-" * 80 + "\n")
            out_file.write(f"Total JSON files scanned:      {total_files}\n")
            out_file.write(f"Files with findings:          {files_with_findings}\n")
            out_file.write(f"Total findings:               {total_findings}\n")
            out_file.write(f"Identity policies:            {identity_policies}\n")
            out_file.write(f"Resource policies:            {resource_policies}\n")
            out_file.write(f"Execution time:               {execution_time:.2f} seconds\n")
            out_file.write("-" * 80 + "\n\n")
            
            # Write detailed results, but skip files with no errors or only suppressed suggestions
            for result in all_results:
                # Only output detailed results if there are findings
                if result.get("has_findings", False):
                    out_file.write(result["output"])
            
            # Write summary at the bottom too for reference
            out_file.write(f"Summary:\n")
            out_file.write(f"Total JSON files scanned:      {total_files}\n")
            out_file.write(f"Files with findings:          {files_with_findings}\n")
            out_file.write(f"Total findings:               {total_findings}\n")
            out_file.write(f"Identity policies:            {identity_policies}\n")
            out_file.write(f"Resource policies:            {resource_policies}\n")
            out_file.write(f"Execution time:               {execution_time:.2f} seconds\n")
    
    if not args.ci:
        print(f"Validation complete in {execution_time:.2f} seconds. Results written to {args.output}")

if __name__ == "__main__":
    main()
