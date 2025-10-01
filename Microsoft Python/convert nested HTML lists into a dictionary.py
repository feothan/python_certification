from bs4 import BeautifulSoup
import json

def parse_dl_recursive(dl_element):
    result = {}

    # Loop through all <DT> elements directly inside this <DL>
    for dt in dl_element.find_all('dt', recursive=False):
        h3 = dt.find('h3')
        if h3:
            title = h3.get_text(strip=True)

            # Look for a sibling <dl> (not child!) – nested structure
            next_dl = dt.find_next_sibling('dl')
            if next_dl:
                result[title] = parse_dl_recursive(next_dl)
            else:
                result[title] = {}

    return result

# Load HTML using lxml parser
with open('../bookmarks.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

# Get the top-level <DL> under <H1>Bookmarks</H1>
root_dl = soup.find('h1', string='Bookmarks')
if root_dl:
    first_dl = root_dl.find_next('dl')
else:
    first_dl = soup.find('dl')  # fallback

# Recursively parse into a nested dictionary
nested_dict = parse_dl_recursive(first_dl)

# Save to JSON
with open('../bookmarks.json', 'w', encoding='utf-8') as f:
    json.dump(nested_dict, f, indent=2, ensure_ascii=False)

# Optional: display result
print(json.dumps(nested_dict, indent=2, ensure_ascii=False))
