import re

def reg_match(text, pattern):
  match = re.search(pattern, text)
  if match:
    return match.group(1)
  else:
    return None