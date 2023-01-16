import argparse
import os
from utils.parsingutils import *

BAKER_NEEDED = "// Run stage 2 for baker in DotsUpgrade script after upgrading to Entities 1.0\n"

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir', required="true", help="The top level directory containing all of the .cs files that need to be updated.")
    parser.add_argument('--stage', default='1', choices=['1', '2'], help="Select stage 1 to update the file to add the monobehaviour authoring component. After stage 1 is complete, update to Entities 1.0, and then run stage 2 to create the Baker")
    parser.add_argument('--commit', default='false', choices=['true', 'false'], help="Set to false to merely print out potential results, no files will be changed. True will update the files")

    args = parser.parse_args()
    commit = args.commit == 'true'

    if (args.stage == '1'):
      generateAuthoringMonobehaviours(args.dir, commit)
    else:
      generateBaker(args.dir, commit)


def generateBaker(rootdir, commit):
  for subdir, dirs, files in os.walk(rootdir):
    for file in files:
      if file.lower().endswith('.cs'):
        generateBakerComponentForFile(file, subdir, commit)

# Stage 2 process for a given file. Generates the "Baker" monobehavior code that sets the
# actual component data based on the Authoring monobehavior data.
def generateBakerComponentForFile(filename, subdir, commit):
  filePath = os.path.join(subdir, filename).replace("\\","/")
  if not needsUpgrade(filePath, BAKER_NEEDED):
    return
  
  print(f'Generating Baker for file {filename}')
  originalLines = []

  file = LoadFileIntoMemory(originalLines, filePath)
  struct_begin, struct_end = GetComponentBody(originalLines, 'struct')
  structLines = originalLines[struct_begin:struct_end]
  name, _ = getStructName(structLines)
  variables = get_variable_names(structLines)
  bakerName = name + 'Baker'
  monoName = name + 'Authoring'

  bakerLines = [f'  public class {bakerName} : Baker<{monoName}>\n'] 
  bakerLines += ["  {\n"]
  bakerLines += [f"    public override void Bake({monoName} authoring)\n"]
  bakerLines += ["    {\n"]
  bakerLines += [f"      AddComponent(new {name}\n"]
  bakerLines += ["      {\n"]

  for variable in variables:
    bakerLines += [f"       {variable} = authoring.{variable},\n"]

  bakerLines += ["      });\n"]
  bakerLines += ["    }\n"]
  bakerLines += ["  }\n"]

  originalLines = originalLines[1:]
  _, author_end = GetComponentBody(originalLines, 'class')
  finalLines = insert_list(originalLines, bakerLines, author_end + 1)

  if (commit):
    replace_file_text(file.name, finalLines)
  else:
    print(*finalLines, sep='')


def generateAuthoringMonobehaviours(rootdir, commit):
  for subdir, dirs, files in os.walk(rootdir):
    for file in files:
      if file.lower().endswith('.cs'):
        generateAuthoringComponentForFile(file, subdir, commit)

# Stage 1 process for a given file. Generates the "Authoring" monobehavior code corresponding to 
# the IComponentData or IBufferElementData
def generateAuthoringComponentForFile(filename, subdir, commit):
  file = os.path.join(subdir, filename).replace("\\","/")
  if not needsUpgrade(file, '[GenerateAuthoringComponent]'):
    return
  
  print(f'Generating authoring monobehavior for file {filename}')

  lines = []
  file = LoadFileIntoMemory(lines, file)  
  lines = [s for s in lines if 'GenerateAuthoringComponent' not in s]

  struct_begin, struct_end = GetComponentBody(lines, 'struct')
  monoLines = lines[struct_begin:struct_end + 1]

  get_authoring_class_definition(monoLines, "Authoring")
  
  replaceFirstSubstring(monoLines, 'struct', 'class')
  monoLines = ["\n"] + monoLines

  lines = insert_list(lines, monoLines, struct_end + 1)
  lines = [BAKER_NEEDED] + ['using UnityEngine;\n'] + lines

  if (commit):
    replace_file_text(file.name, lines)
    update_filename(file.name)
    update_filename(file.name + '.meta')
  else:
    print(*lines, sep='')

def GetComponentBody(lines, keyword):
    struct_begin = -1
    struct_end = -1
    curly_brace_count = 0
    for i, line in enumerate(lines):
      if keyword in line and struct_begin == -1:
          struct_begin = i
          continue
      if struct_begin != -1:
          curly_brace_count += line.count("{") - line.count("}")
          if curly_brace_count == 0:
              struct_end = i
              break
    return struct_begin,struct_end

def needsUpgrade(file, str):
  with open(file) as file:
    for line in file:
        if str in line:
          return True
  return False

if __name__ == "__main__":
  main()