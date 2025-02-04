#!/bin/bash

FILES=(
    "pod-id-how-it-works.adoc"
    "pod-id-agent-setup.adoc"
    "pod-id-association.adoc"
    "pod-id-configure-pods.adoc"
    "pod-id-abac.adoc"
    "pod-id-minimum-sdk.adoc"
    "pod-id-agent-config-ipv6.adoc"
    "pod-id-role.adoc"
)


for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        python3 process_doc.py "$file"
    else
        echo "Warning: $file not found"
    fi
done
