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

links = {}

def word_each(words):
    skips = ['Letter', 'Derived terms', 'Antonyms', 'Usage notes', 'Alternative forms', 'Descendants', 'Further reading', 'See also', 'Descendants', 'Related terms']
    for word in words:
        if word == 'jesucristo':
            word = 'Jesucristo'
        if word == 'santiago':
            word = 'Santiago'

        definitions[word] = []
        links[word] = []

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
            if current.name in ['h4', 'h3']:
                previous_heading = current.text
            if current.name == 'ol':
                skip_next_ol = False
                for s in skips:
                    if previous_heading.startswith(s):
                        skip_next_ol = True
                if not skip_next_ol:
                    previous_h4s[previous_heading] = True
                    for li in current.contents:
                        if isinstance(li, NavigableString):
                            continue
                        value = ''
                        for c in li.contents:
                            if c.name in ['dl','ul']:
                                continue
                            value += c.text
                         
                        for d in li.descendants:
                            if isinstance(d, NavigableString):
                                continue
                            if d.has_attr('class') and 'Latn' in d['class'] and d.has_attr('lang') and d['lang'] == 'es':
                                cs = d.contents
                                if len(cs) == 1 and list_single(cs).name == 'a':
                                    if (d.text in links[word]):
                                        continue
                                    links[word].append(d.text)
                        # if value.startswith('('):
                        #     continue
                        value = value.strip().replace('\n', ' ').replace('\xa0', ' ')
                        if value in definitions[word]:
                            continue
                        
                        definitions[word].append(value)

            current = current.next_sibling
            if current == None:
                break

word_each(words)

roots = {}

for d in definitions:
    if len(definitions[d]) == 1:
        d_def = list_single(definitions[d])
        if (len(links[d]) > 1):
            assert len(links[d]) == 2
            assert " combined with " in d_def
        
        if d not in roots:
            roots[d] = links[d]

print(roots)
print(previous_h4s)

