import json
import name_converter
from typing import Dict

with open("mona.json") as f:
    mona: Dict = json.load(f)

good = {"format": "GOOD", "dbVersion": 20, "source": "Genshin Optimizer", "version": 1}
good["artifacts"] = []
mona.pop("version")
for artifact_position, artifact_list in mona.items():
    good_art_slot = name_converter.slot.get(artifact_position, artifact_position)
    for artifact in artifact_list:
        set_name = artifact["setName"][0].upper() + artifact["setName"][1:]
        set_name = name_converter.set_name.get(set_name, set_name)
        good_art_dict = {
            "setKey": set_name,
            "rarity": artifact["star"],
            "level": artifact["level"],
            "slotKey": good_art_slot,
            "mainStatKey": name_converter.stats.get(
                artifact["mainTag"]["name"], artifact["mainTag"]["name"]
            ),
            "location": "",
            "lock": False,
            "exclude": False,
        }
        sub_stat_list = []
        for sub_stat in artifact["normalTags"]:
            sub_stat_key = name_converter.stats.get(sub_stat["name"], sub_stat["name"])
            if "_" in sub_stat_key:
                sub_stat_value = sub_stat["value"] * 100
            else:
                sub_stat_value = sub_stat["value"]
            sub_stat_list.append(
                {
                    "key": sub_stat_key,
                    "value": round(sub_stat_value, 1),
                }
            )
        good_art_dict["substats"] = sub_stat_list
        good["artifacts"].append(good_art_dict)

with open("good.json", "w+") as f:
    json.dump(good, f, indent=4)
