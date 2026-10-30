import os, sys, urllib.request, re
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print(f"Working directory not named 'data'! Instead got '{Path.cwd().name}'. bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

volume_input = input("What volumes would you like to generate a test for? Enter in 16x16x16 format, separated by commas.\n> ")
volumes_raw = volume_input.split(",")
all_volumes = []
for volume in volumes_raw:
    volume_dimensions = re.split(r'[x: ]', volume)
    volume_dimensions = [int(dim) for dim in volume_dimensions if dim != ""]
    all_volumes.append(volume_dimensions)

block_id_input = input("What block are you testing for? Accepts block ids and block tags.\nIf no block is provided, a macro function is generated instead.\n> ")
if block_id_input == "":
    generate_macro = True
else:
    generate_macro = False

if generate_macro == False and ("#" in block_id_input or ":" in block_id_input):
    auto_path = block_id_input.replace(":","/").replace("#","")
    path_input = input(f"You have entered a block tag, would you like to specify a custom path? If not, the file will end up at \"bldp/predicate/block_in_volume/{auto_path}\"\n> ")
    if path_input == "":
        custom_path = f"bldp/predicate/block_in_volume/{auto_path}"
    else:
        custom_path = path_input
    
    use_custom_path = True
else:
    use_custom_path = False

for current_volume in all_volumes:
    predicate_template = {
        "type": "any_of",
        "terms": []
    }

    for x in range(0,current_volume[0]):
        for y in range(0,current_volume[1]):
            for z in range(0,current_volume[2]):
                subpredicate_entry = {
                    "type": "location_check",
                    "offsetX": x,
                    "offsetY": y,
                    "offsetZ": z,
                    "predicate": {
                        "block": {
                            "blocks": "$(id)"
                        }
                    }
                }

                if subpredicate_entry["offsetX"] == 0:
                    subpredicate_entry.pop("offsetX")
                if subpredicate_entry["offsetY"] == 0:
                    subpredicate_entry.pop("offsetY")
                if subpredicate_entry["offsetZ"] == 0:
                    subpredicate_entry.pop("offsetZ")

                predicate_template["terms"].append(subpredicate_entry)

    if generate_macro == True:
        predicate_string = str(predicate_template)
        predicate_string = predicate_string.replace("'","").replace(" ","")

        function = "\n".join([
            f"$execute if predicate {predicate_string} run return 1",
            "return 0"
        ])

        bldp.string_to_file(function,"bldp/function/block_in_volume",f"{current_volume[0]}x{current_volume[1]}x{current_volume[2]}.mcfunction")
    elif generate_macro == False:
        for subpredicate in predicate_template["terms"]:
            subpredicate["predicate"]["block"]["blocks"] = block_id_input

        if use_custom_path == True:
            path = custom_path
        else:
            path = f"bldp/predicate/block_in_volume/{block_id_input}"

        bldp.json_to_file(predicate_template,path,f"{current_volume[0]}x{current_volume[1]}x{current_volume[2]}")