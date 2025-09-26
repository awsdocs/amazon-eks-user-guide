#!/bin/bash
# Script to deploy XML files and metadata to AWSIAMPolicyExampleReservoir and validate them

set -e  # Exit immediately if a command exits with a non-zero status

# Define paths
METADATA_FILE="AmazonEKSDocs_metadata.yaml"
XML_SOURCE_DIR="xml_output"
JSON_DIR="tcx5_waivers_output"
REPO_BASE="/home/gcline/workplace/eks/src"
IAM_REPO="${REPO_BASE}/AWSIAMPolicyExampleReservoir"
LINTER_REPO="${REPO_BASE}/TCXIAMPolicyExampleLinter"
METADATA_TARGET_DIR="${IAM_REPO}/.doc_gen/metadata"
XML_TARGET_DIR="${IAM_REPO}/snippet_files/AmazonEKSDocs"

echo "Starting deployment and validation process..."

# Pre-step 1: Cleanup old files
echo "Pre-step 1: Cleaning up old files..."
rm -rf "${JSON_DIR}" "${XML_SOURCE_DIR}" "${METADATA_FILE}"
mkdir -p "${JSON_DIR}" "${XML_SOURCE_DIR}"
echo "Cleanup completed."

# Pre-step 2: Run extract with uv run
echo "Pre-step 2: Running extract_tcx5_waivers.py with uv run..."
uv run extract_tcx5_waivers.py
echo "Extraction completed."

# Pre-step 3: Run convert
echo "Pre-step 3: Running json_to_xml_converter.py..."
python3 json_to_xml_converter.py
echo "Conversion completed."

# Pre-step 4: Generate metadata
echo "Pre-step 4: Running generate_metadata.py..."
python3 generate_metadata.py
echo "Metadata generation completed."

# Step 1: Copy the metadata file
echo "Step 1: Copying metadata file to ${METADATA_TARGET_DIR}/${METADATA_FILE}"
mkdir -p "${METADATA_TARGET_DIR}"
if [ -f "${METADATA_FILE}" ]; then
    cp "${METADATA_FILE}" "${METADATA_TARGET_DIR}/${METADATA_FILE}"
    echo "Metadata file copied successfully."
else
    echo "Error: Metadata file ${METADATA_FILE} not found."
    exit 1
fi

# Step 2: Replace the contents of the XML target directory
echo "Step 2: Replacing XML files in ${XML_TARGET_DIR}"
mkdir -p "${XML_TARGET_DIR}"
rm -rf "${XML_TARGET_DIR:?}"/*  # Safety check with :? to ensure variable is not empty
if [ -d "${XML_SOURCE_DIR}" ] && [ "$(ls -A ${XML_SOURCE_DIR})" ]; then
    cp -r "${XML_SOURCE_DIR}"/* "${XML_TARGET_DIR}/"
    echo "XML files copied successfully."
else
    echo "Error: XML source directory ${XML_SOURCE_DIR} is empty or does not exist."
    exit 1
fi

# Step 3: Run brazil-build and tcx_policy_linter in the linter repo
echo "Step 3: Running linter in ${LINTER_REPO}"
cd "${LINTER_REPO}" || { echo "Failed to change directory to ${LINTER_REPO}"; exit 1; }
echo "Running brazil-build..."
brazil-build
echo "Running tcx_policy_linter..."
brazil-runtime-exec tcx_policy_linter ../AWSIAMPolicyExampleReservoir --file_or_folder snippet_files/AmazonEKSDocs/
echo "Linting completed."

# Step 4: Run brazil-build validate in the IAM repo
echo "Step 4: Running validation in ${IAM_REPO}"
cd "${IAM_REPO}" || { echo "Failed to change directory to ${IAM_REPO}"; exit 1; }
echo "Running brazil-build validate..."
brazil-build validate -Dpackage=AmazonEKSDocs
echo "Validation completed."

echo "Deployment and validation process completed successfully!"
