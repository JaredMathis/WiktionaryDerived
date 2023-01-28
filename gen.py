from common import file_json_read, http_get_cached
from urllib.parse import quote    
from bs4 import BeautifulSoup, NavigableString

words = file_json_read('../BibleVersions/gitignore/spanish_words.json')

def words_download(words):
    for word in words:
        print(word)
        try:
            http_get_cached('https://en.wiktionary.org/wiki/' + quote(word))
        except:
            print('error')

def html_parse(s):
    b = BeautifulSoup(s, features="html.parser")
    return b

def list_single(list):
    assert len(list) == 1
    return list[0]

definitions = {}

previous_h4s = {}

def word_each(words):
    skips = ['Letter', 'Derived terms', 'Antonyms', 'Usage notes', 'Alternative forms']
    for word in words:
        if word == 'jesucristo':
            word = 'Jesucristo'
        if word == 'santiago':
            word = 'Santiago'

        definitions[word] = []

        try:
            html = http_get_cached('https://en.wiktionary.org/wiki/' + quote(word))
        except:
            print('error ')
            return

        parsed = html_parse(html)
        h2s = parsed.find_all('h2')

        spanish = list_single([h2 for h2 in h2s if h2.text == 'Spanish[edit]'])
        spanish_index = h2s.index(spanish)
        next_index = spanish_index + 1
        assert next_index > 0
        spanish_next = h2s[next_index]

        current = spanish
        while current != spanish_next:
            if current.name == 'h4':
                previous_h4 = current.text
            if current.name == 'ol':
                skip_next_ol = False
                for s in skips:
                    if current.text.startswith(s):
                        skip_next_ol = True
                if not skip_next_ol:
                    previous_h4s[previous_h4] = True
                    for li in current.contents:
                        if isinstance(li, NavigableString):
                            continue
                        value = ''
                        for c in li.contents:
                            if c.name in ['dl','ul']:
                                continue
                            value += c.text
                        if value.startswith('('):
                            continue
                        if value in definitions[word]:
                            continue
                        definitions[word].append(value)

            current = current.next_sibling
            if current == None:
                break

word_each(words)
print(previous_h4s)

