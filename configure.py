from __future__ import print_function
import os
import sys
import json

def input2(printing):
    if sys.version_info.major < 3:
        return raw_input(printing)
    else:
        return input(printing)


def initialize():
    if not os.path.exists("cfg.json"):
        with open('cfg.json','w') as genfile:
            genjson = {"Filename": "none", "Sheetname": "none"}
            json.dump(genjson,genfile, ensure_ascii=False)

def config_one(question, original):
    print('Original Configuration data of %s' %(question))
    print(original)
    temp_name = input2(question+'? ')
    if temp_name == '':
        return original
    else:
        return temp_name

if __name__ == "__main__":
    initialize()
    print("\n========================================")
    print("CIMS-Pigle Configuration")
    print("GoogleSpreadsheet\'s Filename, GoogleSpreadsheet\'s Sheetname\n")
    print("for all of Question, it will show original value of configure file, you can leave it at that or overwrite each configuration")
    print("At each question of NUMBERS just press RETURN to leave, put information to overwrite\n")
    #
    with open('cfg.json', 'r') as infile:
        originaldic = json.load(infile)
    outputjson = dict()
    outputjson["Filename"] = config_one('Filename', originaldic["Filename"])
    print('')
    outputjson["Sheetname"] = config_one('Sheetname', originaldic["Sheetname"])
    print('')
    #
    jsonString = json.dumps(outputjson, indent=4)
    print('')
    print(jsonString)
    #
    with open('cfg.json', 'w') as outfile:
        json.dump(outputjson, outfile, ensure_ascii=False)
