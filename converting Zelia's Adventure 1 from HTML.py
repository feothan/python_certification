from bs4 import BeautifulSoup
from datetime import datetime

with open('Adventure1.html', 'r', encoding='utf-8') as file:
    Adventure1_html = file.read()

soup = BeautifulSoup(Adventure1_html, 'html.parser')

date_list = []

for tag in soup.find_all():
    for attr in ['add_date', 'last_modified']:  # lowercase because BS normalizes
        if tag.has_attr(attr):
            try:
                unix_time = int(tag[attr])
                date_list.append(datetime.fromtimestamp(unix_time))
            except ValueError:
                pass  # Skip non-integer values

# Remove duplicates (optional)
date_list = list(set(date_list))

# Sort chronologically
date_list.sort()

# Print
for dt in date_list:
    print(dt.strftime('%Y-%m-%d %H:%M:%S'))