import argparse
import curses
from texttv.page_handler import run_ttv, is_valid_page


def get_config():
    parser = argparse.ArgumentParser(description='An SVT Text-TV browser. Navigate with p, n or arrow keys. Select a page with space bar or enter. Quit with q.')
    parser.add_argument('page', nargs='?', type=str, default='100', help='startpage to display')
    args = parser.parse_args()
    if is_valid_page(args.page):
        return args.page
    else:
        print("'{}' is not a valid page. [100, 999] is the valid range.".format(args.page))
        return None


def main():
    page_num = get_config()
    if page_num:
        try:
            curses.wrapper(run_ttv, page_num=page_num)
        except curses.error:
            print("Terminal not big enough.")


if __name__ == "__main__":
    main()
