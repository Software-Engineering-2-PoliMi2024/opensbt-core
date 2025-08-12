"""
Requirements Aggregator Script

This script is designed to recursively search through a given directory for all `requirements.txt` files
and aggregate their contents into a single list of unique requirements. It is particularly useful for
projects with multiple submodules or components, each having its own `requirements.txt` file.

How it works:
1. The script takes a directory path as input.
2. It traverses the directory structure, identifying all `requirements.txt` files.
3. It reads each file, extracts non-commented lines, and adds them to a set to ensure uniqueness.
4. Finally, it prints the sorted list of unique requirements to the console.

Usage:
Run the script from the command line with the following syntax:
    python gather_requirements.py <path>

Replace `<path>` with the directory path you want to scan.
"""

import os


def gather_requirements(dir_path):
    requirements = set()
    for root, dirs, files in os.walk(dir_path):
        if 'requirements.txt' in files:
            req_path = os.path.join(root, 'requirements.txt')
            with open(req_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        requirements.add(line)
    return requirements


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python gather_requirements.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    reqs = gather_requirements(path)

    print('\n'.join(sorted(reqs)))
