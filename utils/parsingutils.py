import os

def firstSubstring(lines, substr): 
  result = -1
  for (i, s) in enumerate(lines):
      if substr in s:
          result = i
          break
  return result

def replaceFirstSubstring(lines, original, new):
  index = firstSubstring(lines, original)
  if (index == -1):
    return False
  lines[index] = lines[index].replace(original, new)
  return True

def getStructName(lines):
  for i, line in enumerate(lines):
    if "struct" in line:
        words = line.split()
        for j, word in enumerate(words):
            if word == "struct":
              return words[j+1], i

def get_authoring_class_definition(lines, append):
  structName, index = getStructName(lines)
  lines[index] = f"public class {structName}{append} : MonoBehaviour\n"

def insert_list(original_list, insert_list, start_index):
  original_list[start_index:start_index] = insert_list
  return original_list

def remove_extension(file_name):
  return file_name[:file_name.rfind(".")]

def update_filename(file_path):
  # Split the file path into the directory and file name
  directory, file_name = os.path.split(file_path)
  # Split the file name into the name and extension
  name, ext = os.path.splitext(file_name)
  isMetaFile = '.cs.meta' in file_path
  if (isMetaFile):
    name, ext2 = os.path.splitext(name)

  # Append "Authoring" to the name
  new_name = name + "Authoring"
  # Join the directory, new name, and extension to create the new file path
  if (isMetaFile):
    new_file_path = os.path.join(directory, new_name + ext2 + ext)
  else:
    new_file_path = os.path.join(directory, new_name + ext)

  # Rename the file
  os.rename(file_path, new_file_path)

def replace_file_text(file_path, lines_to_insert):
  with open(file_path, "w", encoding="utf-8") as file:
    for line in lines_to_insert:
        file.write(line)

def LoadFileIntoMemory(lines, path):
    with open(path, encoding='utf8') as file:
      for line in file:
        lines.append(line)
    return file

def get_variable_names(struct_str):
    variable_names = []
    for line in struct_str:
        if "public" in line and "(" not in line and "{" not in line and "}" not in line and "get" not in line and ";" in line and "=>" not in line:
          variable_name = line.split(" ")[-1]
          variable_name = variable_name.replace(';', '')
          variable_name = variable_name.replace(' ', '')
          variable_name = variable_name.replace('\n', '')
          variable_names.append(variable_name)
    return variable_names