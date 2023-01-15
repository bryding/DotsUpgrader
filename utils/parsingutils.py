import os

def firstSubstring(lines, substr): 
  index, _ = next((i, s) for i, s in enumerate(lines) if substr in s)
  return index

def replaceFirstSubstring(lines, original, new):
  iComponentDataIndex = firstSubstring(lines, original)
  lines[iComponentDataIndex] = lines[iComponentDataIndex].replace(original, new)

def appendStructName(lines, append):
    for i, line in enumerate(lines):
        if "struct" in line:
            words = line.split()
            for j, word in enumerate(words):
                if word == "struct":
                    words[j+1] = words[j+1] + append
                    lines[i] = " ".join(words) + '\n'
                    return

def insert_list(original_list, insert_list, start_index, end_index):
  original_list[start_index:end_index] = insert_list
  return original_list

def remove_extension(file_name):
  return file_name[:file_name.rfind(".")]

def update_filename(file_path):
  # Split the file path into the directory and file name
  directory, file_name = os.path.split(file_path)
  # Split the file name into the name and extension
  name, ext = os.path.splitext(file_name)
  # Append "Authoring" to the name
  new_name = name + "Authoring"
  # Join the directory, new name, and extension to create the new file path
  new_file_path = os.path.join(directory, new_name + ext)
  # Rename the file
  os.rename(file_path, new_file_path)

def replace_file_text(file_path, lines_to_insert):
  with open(file_path, "w") as file:
    for line in lines_to_insert:
        file.write(line)