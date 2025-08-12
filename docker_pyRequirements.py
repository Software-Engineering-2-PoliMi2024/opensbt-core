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