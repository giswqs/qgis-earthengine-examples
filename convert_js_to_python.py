''' Convert GEE JavaScript to Python script to be used in QGIS.

example:
$ python convert_js_to_python.py --input Image/band_math.py 
'''

import os
import argparse

def dict_key_str(line):

    keys = ['bands', 'min', 'max', 'gain', 'bias', 'gamma', 'palette', 'opacity', 
    'format', 'radius', 'units', 'normalize', 'kernel', 'iterations', 'threshold', 
    'sigma', 'magnitude', 'size', 'connectedness', 'maxSize', 'eightConnected',
    'reducer', 'labelBand', 'color', 'source', 'maxDistance', 'referenceImage',
    'maxOffset', 'patchWidth', 'strokeWidth', 'width', 'geometry', 'scale', 'maxPixels',
    'collection', 'selectors']
    for key in keys:
        if ":" in line and key in line:
            line = line.replace(key + ":", "'" + key + "':")
    return line

def js_to_python(in_file):

    root_dir = os.path.dirname(os.path.abspath(__file__))
    in_file_path = os.path.join(root_dir, in_file)

    header = "import ee \n" + "from ee_plugin import Map \n"
    # print(header)

    output = header + "\n"

    with open(in_file_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("//", "#")
            line = line.replace(";", "")
            line = line.replace("var ", "")
            line = line.replace("true", "True")
            line = line.replace("false", "False")
            line = line.replace("null", "{}")
            # line = line.replace("or", "Or")
            # line = line.replace("and", 'And')
            line = dict_key_str(line)
            line = line.rstrip()

            # print(line)
            if line.lstrip().startswith("."):
                output = output.rstrip() + " " + "\\" + "\n" + line + "\n"
            else:
                output = output + line + "\n"

    print(output)

    with open(in_file_path, 'w') as f:
        f.write(output)            
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        help="Path to the input python file")
    # parser.add_argument('--image_path', type=str, help="Path to the input GeoTIFF image")
    # parser.add_argument('--save_path', type=str, help="Path where the output map will be saved")
    args = parser.parse_args()
    js_to_python(args.input)