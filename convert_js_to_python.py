''' Convert GEE JavaScript to Python script to be used in QGIS.

example:
$ python convert_js_to_python.py --input Image/band_math.py 
'''

import os
import argparse
from pathlib import Path

def dict_key_str(line):

    keys = """bands bestEffort bias collection color connectedness eeObject eightConnected format gain gamma
              geometry groupField groupName image iterations kernel labelBand leftField magnitude max maxDistance
              maxOffset maxPixels maxSize minBucketWidth min name normalize opacity palette patchWidth
              radius reducer referenceImage region rightField scale selectors shown sigma size source
              strokeWidth threshold units visParams width""".split()
    for key in keys:
        if ":" in line and key in line:
            line = line.replace(key + ":", "'" + key + "':")
    return line


def js_to_python(in_file, out_file):

    in_file_path = in_file
    out_file_path = out_file

    root_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isfile(in_file_path):
        in_file_path = os.path.join(root_dir, in_file_path)
    if not os.path.isfile(out_file_path):
        out_file_path = os.path.join(root_dir, out_file_path)
    
    bool_python = False
    add_github_url = False

    if add_github_url:
        github_url = "# GitHub URL: " + \
            "https://github.com/giswqs/qgis-earthengine-examples/tree/master/" + in_file + "\n\n"
    else:
        github_url = ""

    lines = []
    with open(in_file_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == 'import ee':
                bool_python = True

    output = ""

    if bool_python:   # only update the GitHub URL if it is already a gee Python script
        output = github_url + ''.join(map(str, lines))
    else:             # deal with JavaScript

        header = github_url + "import ee \n" + "from ee_plugin import Map \n"
        output = header + "\n"

        with open(in_file_path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("//", "#").replace(";",
                                                       "").replace("var ", "")
                line = line.replace("true", "True").replace("false", "False")
                line = line.replace("null", "{}")
                line = line.replace(".or", ".Or")
                line = line.replace(".and", '.And')
                line = line.replace(".not", '.Not')
                line = line.replace('visualize({', 'visualize(**{')

                line = dict_key_str(line).rstrip()

                if "= function" in line:
                    line = line.replace(" = function", "").replace("{", "")
                    line = "def " + line.rstrip() + ":"
                # if line.strip() == "}":
                #     line = ""

                # print(line)
                if line.lstrip().startswith("."):
                    output = output.rstrip() + " " + "\\" + "\n" + line + "\n"
                else:
                    output += line + "\n"

    # print(output)

    with open(out_file_path, 'w') as f:
        f.write(output)


if __name__ == '__main__':

    ## Convert one JavaScript file to Python
    root_dir = os.path.dirname(os.path.abspath(__file__))
    in_file_path = os.path.join(root_dir, "JavaScripts/NormalizedDifference.js")  # change this path to your JavaScript file
    out_file_path = os.path.splitext(in_file_path)[0] + ".py"
    js_to_python(in_file_path, out_file_path)
    print("Saved python script: {}".format(out_file_path))

    ## Convert all JavaScript files in a folder to Python
    in_dir = os.path.join(root_dir, "JavaScripts")   # change this path to your JavaScript folder
    for in_file_path in Path(in_dir).rglob('*.js'):
        out_file_path = os.path.splitext(in_file_path)[0] + ".py"
        js_to_python(in_file_path, out_file_path)
    print("Saved python script folder: {}".format(in_dir))

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--input', type=str,
    #                     help="Path to the input JavaScript file")
    # parser.add_argument('--output', type=str,
    #                     help="Path to the output Python file")
    # args = parser.parse_args()
    # js_to_python(args.input, args.output)