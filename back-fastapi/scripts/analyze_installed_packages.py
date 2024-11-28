import re
import subprocess


def get_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        requirements = [line.split('==')[0].strip() for line in file if line.strip() and not line.startswith('#')]
    return set(requirements)


def get_pipdeptree_packages():
    result = subprocess.run(['pipdeptree', '-fl'], stdout=subprocess.PIPE, text=True)
    packages = set()
    pattern = re.compile(r'[\s-]*([a-zA-Z0-9_\-.]+)==')
    for line in result.stdout.split('\n'):
        match = pattern.search(line)
        if match:
            package = match.group(1)
            packages.add(package)
    return packages


def main():
    requirements = get_requirements()
    installed_packages = get_pipdeptree_packages()

    unused_packages = requirements - installed_packages
    print("Packages in requirements.txt not found in pipdeptree dependencies:")
    for package in unused_packages:
        print(package)


if __name__ == "__main__":
    main()
