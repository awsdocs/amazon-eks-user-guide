import sys
import re

def process_file(filename):
    # Read the file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove first = from lines starting with == but not ====
    processed_lines = []
    for line in lines:
        if re.match(r'^==(?!==$).*$', line):
            line = re.sub(r'^=', '', line)
        processed_lines.append(line)

    # Find the index of the line starting with "= "
    section_index = -1
    for i, line in enumerate(processed_lines):
        if line.lstrip().startswith('= '):
            section_index = i
            break

    if section_index == -1:
        print(f"Error: No line starting with '= ' found in {filename}")
        return

    # Insert all new content at once to avoid index shifting issues
    new_lines = processed_lines[:section_index + 1]  # Everything up to and including the heading
    new_lines.insert(0, "//!!NODE_ROOT <section>\n")  # Add ROOT at start
    
    # Add the new lines after the heading
    new_lines.extend([
        "\n:info_doctype: section\n",
        "\ninclude::../../attributes.txt[]\n"
    ])
    
    # Add the rest of the original content
    new_lines.extend(processed_lines[section_index + 1:])

    # Write back to file
    with open(filename, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    process_file(sys.argv[1])
