from collections import OrderedDict
import glob
import json
from pathlib import Path
from pprint import pprint
import re
import shutil


MAPPING = {
    "GenPromptXP/count_sum/stratum_0/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_0/corpus/baseline",
    "GenPromptXP/count_sum/stratum_0/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_0/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/count_sum/stratum_0/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_0/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",

    "GenPromptXP/count_sum/stratum_1/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_1/corpus/baseline",
    "GenPromptXP/count_sum/stratum_1/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_1/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/count_sum/stratum_1/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_1/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",

    "GenPromptXP/count_sum/stratum_2/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_2/corpus/baseline",
    "GenPromptXP/count_sum/stratum_2/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_2/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/count_sum/stratum_2/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/count_sum/stratum_2/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",

    "GenPromptXP/pset_length/stratum_0/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_0/corpus/baseline",
    "GenPromptXP/pset_length/stratum_0/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_0/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/pset_length/stratum_0/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_0/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",

    "GenPromptXP/pset_length/stratum_1/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_1/corpus/baseline",
    "GenPromptXP/pset_length/stratum_1/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_1/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/pset_length/stratum_1/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_1/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",

    "GenPromptXP/pset_length/stratum_2/corpus/A": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_2/corpus/baseline",
    "GenPromptXP/pset_length/stratum_2/corpus/B": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_2/corpus/GPT_3_Turbo_16K/text2kg_prompt3",
    "GenPromptXP/pset_length/stratum_2/corpus/C": "/DATA/MarkupAutomator/data/WDC/GenPromptXP/pset_length/stratum_2/corpus/GPT_4_Turbo_Preview/text2kg_prompt3",
}

def prettify(stub):
    if isinstance(stub, dict):
        clone = {k: prettify(v) for k, v in stub.items()}
        at_dict = dict(
            sorted(
                [ (k, v) for k, v in clone.items() if isinstance(k, str) and k.startswith("@") ], 
                key=lambda item: item[0]
            )
        )

        remaining_dict = dict(
            sorted(
                [ (k, v) for k, v in clone.items() if isinstance(k, str) and not k.startswith("@") ], 
                key=lambda item: item[0]
            )
        )

        clone = OrderedDict()
        clone.update(at_dict)
        clone.update(remaining_dict)

        return clone
    elif isinstance(stub, list):
        return [prettify(elem) for elem in stub]
    return stub


for dst, src in MAPPING.items():
    filtered_jsonlds = glob.glob(f"{src}/*_semantic_*_filtered.jsonld")
    for filtered_jsonld in filtered_jsonlds:

        dst_filename = f"{dst}/{re.sub(r'_semantic_(pred|expected)_filtered', '', Path(filtered_jsonld).stem)}.jsonld"
        # Sort jsonld dict by keys
        data = None
        with open(filtered_jsonld, "r") as fr, open(dst_filename, "w") as fw:
            data = json.load(fr)
            data = prettify(data)
        
            json.dump(data, fw, indent=4)
            print(f"Updated {dst_filename}")    