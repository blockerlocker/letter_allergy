import os, sys, urllib.request, re, json
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print(f"Working directory not named 'data'! Instead got '{Path.cwd().name}'. bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

MCVERSION = bldp.get_version(MCVERSION)

allergy_letter = input("What letter are you allergic to?\n\n>")
allergy_letter = allergy_letter[0]
if not re.match("[a-zA-Z]",allergy_letter):
    input(f"Character \"{allergy_letter}\" is not a valid letter. The program will end after you press Enter...")
    sys.exit()
allergy_letter = allergy_letter.lower()

bldp.remove_path("letter_allergy/tags/block")
bldp.remove_path("letter_allergy/tags/entity_type/all.json")
bldp.remove_path("letter_allergy/tags/item")
bldp.remove_path("letter_allergy/function/notify.mcfunction")
bldp.remove_path("letter_allergy/function/damage.mcfunction")
bldp.remove_path("../pack.mcmeta")

item_list = bldp.get_registry_data(MCVERSION,"item")
block_list = bldp.get_registry_data(MCVERSION,"block")
entity_type_list = bldp.get_registry_data(MCVERSION,"entity_type")

allergy_items = [item for item in item_list if allergy_letter in item]
allergy_blocks = [block for block in block_list if allergy_letter in block]
allergy_entity_types = [entity_type for entity_type in entity_type_list if allergy_letter in entity_type and not entity_type in ["item", "falling_block"]]

bldp.json_to_file({"values":allergy_items},"letter_allergy/tags/item","all")
bldp.json_to_file({"values":allergy_blocks},"letter_allergy/tags/block","all")
bldp.json_to_file({"values":allergy_entity_types},"letter_allergy/tags/entity_type","all")

bldp.string_to_file(f"title @s actionbar {{text:\"There is a {allergy_letter.upper()} nearby...\",color:yellow}}","letter_allergy/function","notify.mcfunction")

damage_function = [
    f"summon marker ~ ~ ~ {{UUID:uuid('5f5df95b-52e9-4cc5-aec5-43580b9b4491'),CustomName:\"the letter {allergy_letter.upper()}\"}}",
    "attribute @s knockback_resistance modifier add letter_allergy:temp 100 add_value",
    "damage @s 1 mob_attack by 5f5df95b-52e9-4cc5-aec5-43580b9b4491",
    "attribute @s knockback_resistance modifier remove letter_allergy:temp"
]

bldp.string_to_file("\n".join(damage_function),"letter_allergy/function","damage.mcfunction")

data_pack_format = bldp.get_version_data(MCVERSION)["data_pack_version"]

pack = {
    "pack": {
        "description": f"Players take damage when in the presence of any block, item, or mob that contains a {allergy_letter.upper()}.",
        "min_format": data_pack_format,
        "max_format": data_pack_format
    }
}

bldp.string_to_file(json.dumps(pack, indent=4),"../","pack.mcmeta")