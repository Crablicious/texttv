import urllib.request
from html.parser import HTMLParser
from tbls import color_tbl, header_tbl


class TextSnippet:
    def __init__(self, text, style=['W', 'BK', '0'], url=None):
        self.text = text
        self.style = style
        self.url = url

    def __str__(self):
        return "Text: '{', Style: '{}', Url: '{}".format(
            self.text, self.style, self.url)


class TTVPage:
    def __init__(self, page_num):
        self.page_n = 0
        self.page_i = 0
        parser = TTVHTMLParser()
        url = self._create_url(page_num)
        page = self._fetch_page(url)
        # This flow should be fine even if no internet.
        # TODO: remove this if.
        if page:
            parser.feed(page)
            self.snippets = parser.get_snippets()
            self.page_n = len(self.snippets)
        else:
            self.snippets = []

    def _fetch_page(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                raw_page = response.read()
                # TODO: svt uses utf-8, this is kind of fine.
                return raw_page.decode('utf-8')
        # All these errors that disappear with curses...
        except urllib.request.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return None
        except urllib.request.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return None
        except Exception as e:
            print('We failed something weird in fetch_page.')
            print('Reason: ', e.reason)
            return None

    def _create_url(self, page_num):
        return 'https://www.svt.se/svttext/tv/pages/' + page_num + '.html'

    def get_page(self):
        return self.snippets[self.page_i]

    def get_page_n(self, i=0):
        """Returns page n in snippet form, -1 last one"""
        if i < 0:
            self.page_i = self.page_n - 1
            return self.snippets[-1]
        elif i < self.page_n:
            self.page_i = i
            return self.snippets[i]
        else:
            return []

    def next(self) -> bool:
        """Return next page (or not if impossible)"""
        if self.page_i < self.page_n - 1:
            self.page_i += 1
            return True
        else:
            return False

    def prev(self) -> bool:
        """Return previous page (or not if impossible)"""
        if self.page_i > 0:
            self.page_i -= 1
            return True
        else:
            return False


class TTVHTMLParser(HTMLParser):
    def __init__(self):
        super(TTVHTMLParser, self).__init__()
        self.style_stack = [['W', 'BK', '0']]
        self.url = None
        self.snippets = []
        self.tot_snippets = []
        self.in_pre = False
        self.background = None

    def get_snippets(self):
        return self.tot_snippets

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.in_pre = True
        if self.in_pre:
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self.url = attr[1]
                        break  # One link per <a>
            elif tag == 'span':
                for attr in attrs:
                    if attr[0] == 'style':
                        self.background = ''.join([c for c in attr[1] if c.isdigit()])
                    if attr[0] == 'class':
                        style = attr[1].split(' ')
                        fg = 'W'
                        bg = 'BK'
                        text_attr = '0'
                        for s in self.style_stack[-1]:
                            if s in color_tbl.keys():
                                fg = s
                            elif 'bg' in s:
                                bg = s.strip('bg')
                            else:
                                text_attr = s
                        for s in style:
                            if s in color_tbl.keys():
                                fg = s
                            elif 'bg' in s:
                                bg = s.strip('bg')
                            else:
                                text_attr = s
                        self.style_stack.append([fg, bg, text_attr])

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre = False
            self.tot_snippets.append(self.snippets)
            self.snippets = []
        if self.in_pre and tag == 'span':
            self.style_stack.pop()

    def handle_data(self, data):
        if self.in_pre:
            style = self.style_stack[-1][:]  # copy of last style
            if self.url:
                style.append('UL')

            if self.background:
                try:
                    data = header_tbl[self.background]
                except KeyError as e:
                    print("Header character not mapped.", e)
                finally:
                    self.background = None

            self.snippets.append(TextSnippet(data, style, self.url))
            self.url = None
