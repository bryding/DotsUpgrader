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
