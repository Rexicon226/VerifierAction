import json
import requests
import os

# Declare Constants
PATH = '/home/runner/work/'
SWINFO_FILENAME = "swinfo.json"

# Custom Error Classes
class ResolutionError(Exception):
    pass

class ReturnCodeError(Exception):
    pass

# Find swinfo.json recursively
swinfo_paths = []
for root, _, files in os.walk(PATH):
    if SWINFO_FILENAME in files:
        swinfo_paths.append(os.path.join(root, SWINFO_FILENAME))
        
swinfo_count = len(swinfo_paths)
if swinfo_count == 0:
    raise ResolutionError("No 'swinfo.json' was detected in your project directory. Please make sure there is one.")
elif swinfo_count > 1:
    raise ResolutionError("You have more than one 'swinfo.json' file in your project, please resolve this.")
            
# Read contents and check validity of URL
swinfo_path = swinfo_paths[0]
with open(swinfo_path) as swinfo_file:
    contents = json.load(swinfo_file)
    check_url = contents.get("version_check")
    
    if not check_url:
        raise ResolutionError("No 'version_check' URL found in 'swinfo.json'.")
    
    response = requests.get(check_url)
    if response.status_code != 200:
        raise ReturnCodeError("The 'version_check' URL in 'swinfo.json' is incorrect or invalid. Please make sure there are no typos and it is a valid link to a swinfo.json or .csproj.")
      
print("Verification was successful. If any other issues arise, please contact the KSP2 Modding Society Discord.")
