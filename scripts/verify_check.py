import json
import requests
import os

# Declare Constants
PATH = '/home/runner/work/'
SWINFO_FILENAME = "swinfo.json"
CSPROJ_FILENAME = ".csproj"
DIRECTORY_BUILD_TARGETS_FILENAME = "Directory.Build.targets"
VERSION_CHECK_TAG = "<VersionCheckUrl>"

# Custom Error Classes
class ResolutionError(Exception):
    pass

class ReturnCodeError(Exception):
    pass

# Find swinfo.json and .csproj files recursively
swinfo_paths = []
csproj_paths = []
build_targets_paths = []

for root, _, files in os.walk(PATH):
    if SWINFO_FILENAME in files:
        swinfo_paths.append(os.path.join(root, SWINFO_FILENAME))
    if CSPROJ_FILENAME in files:
        csproj_paths.append(os.path.join(root, CSPROJ_FILENAME))
    if DIRECTORY_BUILD_TARGETS_FILENAME in files:
        build_targets_paths.append(os.path.join(root, DIRECTORY_BUILD_TARGETS_FILENAME))
        
swinfo_count = len(swinfo_paths)
csproj_count = len(csproj_paths)
build_targets_count = len(build_targets_paths)

if swinfo_count == 0 and csproj_count == 0:
    raise ResolutionError("No 'swinfo.json' or '.csproj' files were detected in your project directory. Please make sure there is at least one of them.")
elif swinfo_count > 1:
    raise ResolutionError("You have more than one 'swinfo.json' file in your project. Please resolve this.")
            
# Read contents and check validity of URL
if swinfo_count == 1:
    swinfo_path = swinfo_paths[0]
    with open(swinfo_path) as swinfo_file:
        contents = json.load(swinfo_file)
        check_url = contents.get("version_check")
        
        if not check_url:
            raise ResolutionError("No 'version_check' URL found in 'swinfo.json'.")
        
        response = requests.get(check_url)
        if response.status_code != 200:
            raise ReturnCodeError("The 'version_check' URL in 'swinfo.json' is incorrect or invalid. Please make sure there are no typos and it is a valid link to a swinfo.json or .csproj.")
else:
     for csproj_path, build_targets_path in zip(csproj_paths, build_targets_paths):
        with open(csproj_path) as csproj_file:
            csproj_contents = csproj_file.read()
            if VERSION_CHECK_TAG not in csproj_contents:
                continue  # Move to the next pair of files
            
            with open(build_targets_path) as build_targets_file:
                build_targets_contents = build_targets_file.read()
                match = re.search(VERSION_CHECK_TAG, build_targets_contents)
                if not match:
                    raise ResolutionError(f"No '{VERSION_CHECK_TAG}' found in '{build_targets_path}'.")
                
                check_url = match.group(1).strip()
                
                if not check_url:
                    raise ResolutionError(f"No URL found for '{VERSION_CHECK_TAG}' in '{build_targets_path}'.")
                
                response = requests.get(check_url)
                if response.status_code != 200:
                    raise ReturnCodeError(f"The URL '{check_url}' from '{build_targets_path}' is incorrect or invalid. Please make sure there are no typos and it is a valid
