import curses


color_tbl = {'W': curses.COLOR_WHITE, 'B': curses.COLOR_BLUE, 'BK': curses.COLOR_BLACK, 'Y': curses.COLOR_YELLOW, 'C': curses.COLOR_CYAN, 'R': curses.COLOR_RED, 'G': curses.COLOR_GREEN, 'M': curses.COLOR_MAGENTA}

attr_tbl = {'0': curses.A_NORMAL, 'DH': curses.A_BOLD, 'UL': curses.A_UNDERLINE}

# https://en.wikipedia.org/wiki/Block_Elements
header_tbl = {'96': '▗', '40': '▗', '48': '▖', '36': '▖', '124':  '█', '127':  '█', '47': '█', '115':  '█', '119':  '█', '44': '▀', '35': '▀', '51': '▀', '112': '▄', '114': '▄', '104': '▐', '106': '▐', '52': '▌', '53': '▌', '42': '▐', '34': '▝', '98': '▝', '33': '▘', '49': '▘', '37': '▌', '117': '▙', '109': '▙', '45': '▙', '125': '▙', '116': '▙', '63': '█', '123': '█', '110': '▜', '111': '█', '39': '▛', '61': '▛', '55': '▛', '126': '▟', '122': '▟', '120': '▟', '107': '▜', '43': '▜', '38': '▞', '58': '▞', '54': '▞', '105': '▚', '121': '▚', '101': '▚', '57': '▚', '41': '▚', '102': '▞', '62': '▞'}
