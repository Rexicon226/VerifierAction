"""
==========================================
Author: Rexicon226 <87927264+Rexicon226@users.noreply.github.com>
Co-authored-by: Mineinjava <65673396+Mineinjava@users.noreply.github.com>
Date:   20 May 2023
==========================================
"""

import json
import requests
import os

# Declare Variables

PATH = '/home/runner/work/'

swinfo_amount = 0
swinfo_path = ""

# Custom Error Classes

class ResolutionError(Exception):
    pass

class ReturnCodeError(Exception):
    pass

# Recursive search through the root, find swinfo.json

for root, subFolder, files in os.walk(PATH):
    for item in files:
        if item == "swinfo.json" :
            swinfo_amount += 1
            if swinfo_amount > 1:
                raise ResolutionError("You have more than one 'swinfo.json' file in your project, please resolve this.")
            swinfo_path = os.path.join(root, item)
            
if swinfo_amount == 0:
    raise ResolutionError("No 'swinfo.json' was detected in your project directory. Please make sure there is one.")
            
            
# Read contents

swinfo_file = open(swinfo_path)   

contents = json.load(swinfo_file)

swinfo_file.close()

# Check validity of URL

check_url = contents.get("version_check")

return_code = requests.get(check_url).status_code

if (return_code != 200):
    raise ReturnCodeError("The 'version_check' you have put into your 'swinfo.json' is incorrect / invalid. Please make sure there are no typos and it is a valid link to a swinfo.json or .csproj")
      
    

print("Verify Check was successful as far as we could tell. If any other issues arise, please contact the KSP2 Modding Society Discord.")
