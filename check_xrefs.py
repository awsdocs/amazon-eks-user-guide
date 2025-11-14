#!/usr/bin/env python3
"""
AsciiDoc Cross-Reference Checker

This script analyzes all .adoc files in a directory to find broken cross-references.
It supports both xref: and <<>> syntax and checks against explicit and auto-generated section IDs.
"""

import re
import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from dataclasses import dataclass
from typing import Set, List, Tuple
import sys


@dataclass
class XRefInfo:
    """Information about a cross-reference"""
    file_path: str
    line_number: int
    xref_id: str
    xref_type: str  # 'xref' or 'angle_bracket'


@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    file_path: str
    section_ids: Set[str]
    xrefs: List[XRefInfo]
    errors: List[str]


def normalize_id(text: str) -> str:
    """
    Normalize a section header to an auto-generated ID.
    Based on AsciiDoc rules with idseparator: -
    """
    # Convert to lowercase
    text = text.lower()
    # Remove formatting and special chars, replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def extract_section_ids(content: str, lines: List[str]) -> Set[str]:
    """
    Extract all section IDs from file content.
    Supports:
    - [[id]] syntax (standalone or inline)
    - [#id] syntax (standalone or inline)
    - Auto-generated IDs from section headers
    """
    section_ids = set()

    # Pattern for explicit [[id]] or [[id,title]] syntax (standalone or inline)
    # This pattern works for both "[[id]]" on its own line and "=== Title [[id]]" inline
    explicit_bracket_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    for match in explicit_bracket_pattern.finditer(content):
        # Handle [[id,title]] syntax - ID is the part before the comma
        id_text = match.group(1)
        section_id = id_text.split(',')[0].strip()
        section_ids.add(section_id)

    # Pattern for [#id] syntax (standalone or inline)
    explicit_hash_pattern = re.compile(r'\[#([^\]]+)\]')
    for match in explicit_hash_pattern.finditer(content):
        section_id = match.group(1).split(',')[0].strip()
        section_ids.add(section_id)

    # Pattern for section headers (=, ==, ===, etc.)
    # Auto-generate IDs from section titles
    section_header_pattern = re.compile(r'^(=+)\s+(.+)$', re.MULTILINE)
    for match in section_header_pattern.finditer(content):
        header_text = match.group(2).strip()
        # Remove inline IDs like [[id]] or [#id] from the header text before auto-generating ID
        header_text = re.sub(r'\[\[[^\]]+\]\]', '', header_text)
        header_text = re.sub(r'\[#[^\]]+\]', '', header_text)
        # Remove inline formatting like *bold*, _italic_, etc.
        header_text = re.sub(r'\*\*?([^*]+)\*\*?', r'\1', header_text)
        header_text = re.sub(r'__?([^_]+)__?', r'\1', header_text)
        header_text = re.sub(r'`([^`]+)`', r'\1', header_text)
        # Remove links
        header_text = re.sub(r'https?://[^\s\[]+', '', header_text)
        header_text = re.sub(r'link:[^\[]+\[[^\]]*\]', '', header_text)

        auto_id = normalize_id(header_text)
        if auto_id:
            section_ids.add(auto_id)

    return section_ids


def extract_xrefs(content: str, file_path: str) -> List[XRefInfo]:
    """
    Extract all cross-references from file content.
    Supports:
    - xref:id[...] syntax
    - <<id>> syntax
    - <<id,text>> syntax
    """
    xrefs = []
    lines = content.split('\n')

    # Pattern for xref:id[...] syntax
    xref_pattern = re.compile(r'xref:([a-zA-Z0-9_-]+)(?:\[[^\]]*\])?')

    # Pattern for <<id>> or <<id,text>> syntax
    angle_bracket_pattern = re.compile(r'<<([a-zA-Z0-9_-]+)(?:,[^>]*)?>>')

    for line_num, line in enumerate(lines, 1):
        # Find xref: references
        for match in xref_pattern.finditer(line):
            xref_id = match.group(1)
            xrefs.append(XRefInfo(
                file_path=file_path,
                line_number=line_num,
                xref_id=xref_id,
                xref_type='xref'
            ))

        # Find <<>> references
        for match in angle_bracket_pattern.finditer(line):
            xref_id = match.group(1)
            xrefs.append(XRefInfo(
                file_path=file_path,
                line_number=line_num,
                xref_id=xref_id,
                xref_type='angle_bracket'
            ))

    return xrefs


def analyze_file(file_path: Path) -> FileAnalysis:
    """
    Analyze a single .adoc file for section IDs and cross-references.
    """
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        section_ids = extract_section_ids(content, lines)
        xrefs = extract_xrefs(content, str(file_path))

        return FileAnalysis(
            file_path=str(file_path),
            section_ids=section_ids,
            xrefs=xrefs,
            errors=errors
        )

    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
        return FileAnalysis(
            file_path=str(file_path),
            section_ids=set(),
            xrefs=[],
            errors=errors
        )


def find_adoc_files(directory: str) -> List[Path]:
    """Find all .adoc files in the directory recursively."""
    path = Path(directory)
    return list(path.rglob('*.adoc'))


def main():
    """Main function to orchestrate the cross-reference checking."""

    # Configuration
    directory = 'latest/ug/'

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found")
        sys.exit(1)

    print(f"Analyzing .adoc files in {directory}...")

    # Find all .adoc files
    adoc_files = find_adoc_files(directory)
    print(f"Found {len(adoc_files)} .adoc files")

    # Analyze files in parallel
    all_section_ids = defaultdict(set)  # id -> set of files that define it
    all_xrefs = []
    file_errors = []

    print("\nAnalyzing files in parallel...")

    with ProcessPoolExecutor() as executor:
        # Submit all files for analysis
        future_to_file = {
            executor.submit(analyze_file, file_path): file_path
            for file_path in adoc_files
        }

        # Collect results as they complete
        completed = 0
        for future in as_completed(future_to_file):
            completed += 1
            if completed % 50 == 0:
                print(f"  Processed {completed}/{len(adoc_files)} files...")

            try:
                result = future.result()

                # Collect section IDs
                for section_id in result.section_ids:
                    all_section_ids[section_id].add(result.file_path)

                # Collect xrefs
                all_xrefs.extend(result.xrefs)

                # Collect errors
                if result.errors:
                    file_errors.extend(result.errors)

            except Exception as e:
                file_path = future_to_file[future]
                file_errors.append(f"Error processing {file_path}: {str(e)}")

    print(f"  Processed {len(adoc_files)}/{len(adoc_files)} files")

    # Report file processing errors
    if file_errors:
        print("\n" + "="*80)
        print("FILE PROCESSING ERRORS")
        print("="*80)
        for error in file_errors:
            print(f"  {error}")

    # Check for broken xrefs
    print("\n" + "="*80)
    print("CHECKING CROSS-REFERENCES")
    print("="*80)
    print(f"Total section IDs found: {len(all_section_ids)}")
    print(f"Total xrefs found: {len(all_xrefs)}")

    broken_xrefs = []
    for xref in all_xrefs:
        if xref.xref_id not in all_section_ids:
            broken_xrefs.append(xref)

    # Report results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)

    if not broken_xrefs:
        print("✓ No broken cross-references found!")
    else:
        print(f"✗ Found {len(broken_xrefs)} broken cross-references:\n")

        # Group by file for better readability
        broken_by_file = defaultdict(list)
        for xref in broken_xrefs:
            broken_by_file[xref.file_path].append(xref)

        for file_path in sorted(broken_by_file.keys()):
            print(f"\n{file_path}:")
            for xref in sorted(broken_by_file[file_path], key=lambda x: x.line_number):
                xref_syntax = f"xref:{xref.xref_id}[...]" if xref.xref_type == 'xref' else f"<<{xref.xref_id}>>"
                print(f"  Line {xref.line_number}: {xref_syntax}")

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files analyzed: {len(adoc_files)}")
    print(f"Section IDs found: {len(all_section_ids)}")
    print(f"Cross-references found: {len(all_xrefs)}")
    print(f"Broken cross-references: {len(broken_xrefs)}")

    # Check for duplicate section IDs
    duplicates = {id: files for id, files in all_section_ids.items() if len(files) > 1}
    if duplicates:
        print(f"\n⚠ Warning: Found {len(duplicates)} duplicate section IDs:")
        for section_id, files in sorted(duplicates.items()):
            print(f"\n  ID '{section_id}' defined in {len(files)} files:")
            for file_path in sorted(files):
                print(f"    - {file_path}")

    # Exit with error code if broken xrefs found
    sys.exit(1 if broken_xrefs else 0)


if __name__ == '__main__':
    main()
