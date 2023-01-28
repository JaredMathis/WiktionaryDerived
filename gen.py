from common import file_json_read, http_get_cached
from urllib.parse import quote    

words = file_json_read('../BibleVersions/gitignore/spanish_words.json')

for word in words[:10]:
    print(word)
    http_get_cached('https://en.wiktionary.org/wiki/' + quote(word))