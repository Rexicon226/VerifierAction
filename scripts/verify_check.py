import json
import requests
import os

# Declare Constants
PATH = '/home/runner/work/'
SWINFO_FILENAME = "swinfo.json"
CSPROJ_EXTENSION = ".csproj"
VERSION_CHECK_TAG = "<VersionCheckUrl>(.*?)</VersionCheckUrl>"

# Custom Error Classes
class ResolutionError(Exception):
    pass

class ReturnCodeError(Exception):
    pass

# Find swinfo.json and .csproj files recursively
swinfo_paths = []
csproj_paths = []

for root, _, files in os.walk(PATH):
    if SWINFO_FILENAME in files:
        swinfo_paths.append(os.path.join(root, SWINFO_FILENAME))
    for file_name in files:
        if CSPROJ_EXTENSION in file_name:
            print(file_name)
            csproj_paths.append(os.path.join(root, file_name))
        
swinfo_count = len(swinfo_paths)
csproj_count = len(csproj_paths)

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
            
        print("Verify Check was successful as far as we could tell. If any other issues arise, please contact the KSP2 Modding Society Discord.")
else:
     for csproj_path in zip(csproj_paths):
        print(csproj_paths)
        with open(csproj_path) as csproj_file:
            csproj_contents = csproj_file.read()
            print("got to the end of the csproj")
