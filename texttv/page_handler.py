import curses
import collections
from texttv.utils import TTVPage
from texttv.tbls import color_tbl, attr_tbl


# https://code.activestate.com/recipes/52295/
class TTVWin:
    # Extension of Curses window, since I can't inherit from it.
    def __init__(self, win):
        # This is necessary to not trigger __setattr__
        self.__dict__['win'] = win
        self.__dict__['colors'] = {}

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


class PageCache(collections.OrderedDict):
    """OrderedDict with size limit"""
    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop("size", None)
        super(PageCache, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super(PageCache, self).__setitem__(key, value)
        self._limit_size()

    def setdefault(self, key, value=None):
        val = super(PageCache, self).setdefault(key, value)
        self._limit_size()
        return val

    def update(self, *args, **kwargs):
        super(PageCache, self).update(*args, **kwargs)
        self._limit_size()

    def _limit_size(self):
        if self.size:
            while len(self) > self.size:
                self.popitem(last=False)


def is_valid_page(page_num):
    try:
        return page_num.isdigit() and int(page_num) <= 999 and int(page_num) >= 100
    except ValueError:
        return False


def run_ttv(stdscr, page_num):
    win = TTVWin(stdscr)
    page_cache_sz = 10
    page_cache = PageCache(size=page_cache_sz)
    is_new_page = None
    while True:
        page = page_cache.setdefault(page_num, TTVPage(page_num))
        if is_new_page is not None:
            snippets = page.get_page_n(is_new_page)
            is_new_page = None
        else:
            snippets = page.get_page()
        win.load_page(snippets)

        c = win.getch()
        if c == ord('\n') or c == ord(' '):
            curses.echo()
            page_num = 'asdf'
            while not is_valid_page(page_num):
                win.addstr(1, 1, '   ')
                page_num = win.getstr(1, 1, 3).decode('utf-8')
                is_new_page = 0
            curses.noecho()
        elif c == ord('n') or c == curses.KEY_RIGHT:
            if not page.next() and is_valid_page(page_num):
                page_num = str(int(page_num) + 1)
                is_new_page = 0
        elif c == ord('p') or c == curses.KEY_LEFT:
            if not page.prev() and is_valid_page(page_num):
                page_num = str(int(page_num) - 1)
                is_new_page = -1
        elif c == ord('q'):
            break
        win.clear()
