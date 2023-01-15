import argparse
import os
from utils.parsingutils import *


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir', default="./sandbox/forModify", help="The top level directory containing all of the .cs files that need to be updated.")
    parser.add_argument('--stage', default='1', choices=['1', '2'], help="Select stage 1 to update the file to add the monobehaviour authoring component. After stage 1 is complete, update to Entities 1.0, and then run stage 2 to create the Baker")

    args = parser.parse_args()

    if (args.stage == '1'):
      generateAuthoringMonobehaviours(args.dir)
    

def generateAuthoringMonobehaviours(rootdir):
  for subdir, dirs, files in os.walk(rootdir):
    for file in files:
      if file.lower().endswith('.cs'):
        processFile(file, subdir)

def processFile(filename, subdir):
  file = os.path.join(subdir, filename).replace("\\","/")
  if not needsUpgrade(file):
    return
  
  print(f'Processing {filename}')

  lines = []

  with open(file) as file:
    for line in file:
      lines.append(line)
  
  lines = [s for s in lines if 'GenerateAuthoringComponent' not in s]

  struct_begin = -1
  struct_end = -1
  curly_brace_count = 0
  for i, line in enumerate(lines):
    if "struct" in line and struct_begin == -1:
        struct_begin = i
        continue
    if struct_begin != -1:
        curly_brace_count += line.count("{") - line.count("}")
        if curly_brace_count == 0:
            struct_end = i
            break

  monoLines = lines[struct_begin:struct_end + 1]

  appendStructName(monoLines, "Authoring")
  replaceFirstSubstring(monoLines, 'IComponentData', 'Monobehaviour')
  replaceFirstSubstring(monoLines, 'struct', 'class')
  monoLines = ["\n"] + monoLines

  lines = insert_list(lines, monoLines, struct_end + 1, struct_end + 1)

  print(file.name)
  replace_file_text(file.name, lines)

  update_filename(file.name)

  print(*lines, sep='')


def needsUpgrade(file):
  with open(file) as file:
    for line in file:
        if '[GenerateAuthoringComponent]' in line:
          return True
  return False

if __name__ == "__main__":
  main()