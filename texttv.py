import curses
import urllib.request
from html.parser import HTMLParser
import argparse


color_tbl = {'W': curses.COLOR_WHITE, 'B': curses.COLOR_BLUE, 'BK': curses.COLOR_BLACK, 'Y': curses.COLOR_YELLOW, 'C': curses.COLOR_CYAN, 'R': curses.COLOR_RED, 'G': curses.COLOR_GREEN}
attr_tbl = {'0': curses.A_NORMAL, 'DH': curses.A_BOLD, 'UL': curses.A_UNDERLINE}
# https://en.wikipedia.org/wiki/Block_Elements
header_tbl = {'96': '▗', '40': '▗', '48': '▖', '36': '▖', '124':  '█', '127':  '█', '47': '█', '115':  '█', '119':  '█', '44': '▀', '35': '▀', '51': '▀', '112': '▄', '114': '▄', '104': '▐', '106': '▐', '52': '▌', '53': '▌', '42': '▐', '34': '▝', '98': '▝', '33': '▘', '49': '▘', '37': '▌', '117': '▙', '109': '▙', '45': '▙', '125': '▙', '116': '▙', '63': '█', '123': '█', '110': '▜', '111': '█', '39': '▛', '61': '▛', '55': '▛', '126': '▟', '122': '▟', '120': '▟', '107': '▜', '43': '▜', '38': '▞', '58': '▞', '54': '▞', '105': '▚', '121': '▚', '101': '▚', '57': '▚', '41': '▚', '102': '▞', '62': '▞'}


# https://code.activestate.com/recipes/52295/
class TTVWin:
    # Extension of Curses window, since I can't inherit from it.
    def __init__(self, win):
        # This is necessary to not trigger __setattr__
        self.__dict__['win'] = win
        self.__dict__['colors'] = {}
        curses.start_color()
        curses.curs_set(False)

    def load_page(self, snippets):
        for snippet in snippets:
            col_attr = self._parse_style(snippet.style)
            self.win.addstr(snippet.text, col_attr)
        self.win.refresh()

    def _parse_style(self, style):
        fg = color_tbl[style[0]]
        bg = color_tbl[style[1]]
        attrs = 0
        for a in style[2:]:
            attrs |= attr_tbl[a]

        fg_bg_str = style[0] + ' ' + style[1]
        if fg_bg_str not in self.colors:
            curses.init_pair(len(self.colors) + 1, fg, bg)
            self.colors[fg_bg_str] = len(self.colors) + 1
        col_attr = curses.color_pair(self.colors[fg_bg_str]) | attrs
        return col_attr

    def __getattr__(self, attr):
        return getattr(self.win, attr)

    def __setattr__(self, attr, value):
        return setattr(self.win, attr, value)


class TextSnippet:
    def __init__(self, text, style=['W', 'BK', '0'], url=None):
        self.text = text
        self.style = style
        self.url = url

    def __str__(self):
        return "Text: '{}', Style: '{}', Url: '{}".format(self.text, self.style, self.url)


class TTVHTMLParser(HTMLParser):
    def __init__(self):
        super(TTVHTMLParser, self).__init__()
        self.style_stack = [['W', 'BK', '0']]
        self.url = None
        self.snippets = []
        self.tot_snippets = []
        self.in_pre = False
        self.do_print = False
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


def fetch_page(url):
    try:
        with urllib.request.urlopen(url) as response:
            raw_page = response.read()
            # TODO: svt uses utf-8, this is kind of fine.
            return raw_page.decode('utf-8')
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


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('page', nargs='?', type=str, default='100')
    args = parser.parse_args()
    return args.page


def run_ttv(stdscr):
    new_page_num = get_config()
    win = TTVWin(stdscr)
    page_num = 0
    snippets_i = 0
    while True:
        if new_page_num != page_num:
            # Only loads if it's a new page.
            page_num = new_page_num
            url = 'https://www.svt.se/svttext/tv/pages/' + page_num + '.html'
            page = fetch_page(url)
            if not page:
                break
            parser = TTVHTMLParser()
            parser.feed(page)
            snippets = parser.get_snippets()
            if snippets_i == -1:  # start from last page if going backwards.
                snippets_i = len(snippets) - 1

        win.load_page(snippets[snippets_i])
        c = win.getch()
        if c == ord('\n') or c == ord(' '):
            curses.echo()
            new_page_num = 'abc'
            while not new_page_num.isdigit():
                win.addstr(1, 1, '   ')
                new_page_num = win.getstr(1, 1, 3).decode('utf-8')
            curses.noecho()
        elif c == ord('n') or c == curses.KEY_RIGHT:
            if snippets_i < len(snippets) - 1:
                snippets_i += 1
            else:
                snippets_i = 0
                new_page_num = str(int(page_num) + 1)
        elif c == ord('p') or c == curses.KEY_LEFT:
            if snippets_i > 0:
                snippets_i -= 1
            else:
                if page_num != '100':
                    snippets_i = -1
                    new_page_num = str(int(page_num) - 1)
        elif c == ord('q'):
            break
        win.clear()


def main():
    curses.wrapper(run_ttv)


if __name__ == "__main__":
    main()
