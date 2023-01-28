from common import file_json_read, http_get_cached
from urllib.parse import quote    

words = file_json_read('../BibleVersions/gitignore/spanish_words.json')

def words_download(words):
    for word in words:
        print(word)
        try:
            http_get_cached('https://en.wiktionary.org/wiki/' + quote(word))
        except:
            print('error')

words_download(words)

