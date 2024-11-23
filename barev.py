# import os
# import re

# # Function to reverse and wrap string literals in replace method calls with quotation marks
# def reverse_replace_strings(line):
#     # Regex pattern to match replace method calls with two string arguments
#     pattern = r'(\w+)\.replace\((["\'])([^"\']*)\2,\s*(["\'])([^"\']*)\4\)'
    
#     # Function to reverse and wrap string literals in matched strings
#     def replace_function(match):
#         # Extract groups from the match
#         object_name = match.group(1)
#         first_string = match.group(3)
#         second_string = match.group(5)
        
#         # Reverse the string literals and wrap them in quotation marks
#         reversed_line = f"{object_name}.replace('{second_string}', '{first_string}')"
        
#         return reversed_line
    
#     # Use re.sub to replace matched patterns with reversed and wrapped string literals
#     reversed_line = re.sub(pattern, replace_function, line)
    
#     return reversed_line

# # Function to process Python files and modify replace method calls
# def process_python_files(input_directory):
#     # List all Python files in the input directory
#     python_files = [file for file in os.listdir(input_directory) if file.endswith('.py')]
    
#     # Process each Python file
#     for file_name in python_files:
#         file_path = os.path.join(input_directory, file_name)
        
#         # Read lines from the input Python file
#         with open(file_path, 'r') as f:
#             lines = f.readlines()
        
#         # Process each line to reverse and wrap string literals in replace method calls
#         processed_lines = [reverse_replace_strings(line) for line in lines]
        
#         # Write processed lines back to the Python file
#         with open(file_path, 'w') as f:
#             f.writelines(processed_lines)
        
#         print(f"Processed {len(lines)} lines in {file_name}")

# # Example usage:
# input_directory = "C:\\Users\\user\\Desktop\\Inventory\\Projects\\baport\\__pycache__"  # Replace with your input directory containing Python files

# # Process Python files in the specified directory
# process_python_files(input_directory)


import sys

def detect_encoding(filename):
    encodings = ['utf-8', 'latin-1', 'ascii', 'cp1252']
    for encoding in encodings:
        try:
            with open(filename, 'rb') as f:
                f.read().decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    return None

filename = sys.argv[1]
encoding = detect_encoding(filename)
if encoding:
    with open(filename, 'r', encoding=encoding) as f:
        print("Reversing "+ sys.argv[1])
        content = f.read()
else:
    print('Could not detect encoding')
    
# import all ba,bastd and _ba here or at the end check if the imports are used then  import them
content = content.replace('# ba_meta require api 8', '# ba_meta require api 7')
content = content.replace('# ba_meta require api 9', '# ba_meta require api 7')
content = content.replace('# ba_meta export bascenev1.GameActivity', '# ba_meta export game')
content = content.replace('bs', 'ba')
content = content.replace('bui', 'ba')
content = content.replace('babase', 'ba')
content = content.replace('bascenev1lib', 'bastd')
content = content.replace('baclassic', 'ba')
content = content.replace('bascenev1', 'ba')
content = content.replace('bauiv1', 'ba')


content = content.replace('_gameutils', 'gameutils')
content = content.replace('_mgen', '_generated')
content = content.replace('mesh', 'model')
content = content.replace('collision_mesh', 'collide_mesh')
content = content.replace('getcollisionmesh', 'getcollidemesh')
content = content.replace("PlayerT", "PlayerType")
content = content.replace(".get_v1_cloud_log", ".getlog")
content = content.replace(".apptimer", ".timer") # timetype=ba.TimeType.REAL
# content = content.replace('/ 1000', '')
# Depracation stuff
# internal stuff
content = content.replace(".app.plus", ".app")
content = content.replace(".app.classic", ".app")
content = content.replace("ba.time() * 1000", "ba.time(timeformat=ba.TimeFormat.MILLISECONDS)")
# content = content.replace("timetype=","")
# fix .play and with activity.context


# content = re.sub(r'bs\.Timer\(([^)]*)\bTimeType\.REAL\b([^)]*)\)', r'babase.AppTimer(\1\2)', content)
trademark = "# Reverse porting to api 7 made easier by baport/barev.(https://github.com/bombsquad-community/baport)\n"
with open(sys.argv[1], "w",  encoding=encoding) as f:
    f.write(trademark + content)