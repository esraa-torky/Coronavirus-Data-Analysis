import re

html='  assa  '
text = re.compile("  ").sub('',html)
print(text)