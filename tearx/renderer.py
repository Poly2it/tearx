import shutil

from math import *

class ANSI:
    # Text color
    fg_black = '\033[30m'
    fg_red = '\033[31m'
    fg_green = '\033[32m'
    fg_yellow = '\033[33m'
    fg_blue = '\033[34m'
    fg_magenta = '\033[35m'
    fg_cyan = '\033[36m'
    fg_white = '\033[37m'

    # Background color
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'
    bg_blue = '\033[44m'
    bg_magenta = '\033[45m'
    bg_cyan = '\033[46m'
    bg_white = '\033[47m'

    # Styles
    bold = '\033[1m'
    underline = '\033[4m'
    blink = '\033[5m'
    reverse = '\033[7m'

    # Reset
    reset = '\033[0m'

    @staticmethod
    def fg_color(hex):
        lv = len(hex)
        colors = tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return f"\033[38;2;{colors[0]};{colors[1]};{colors[2]}m"

    @staticmethod
    def bg_color(hex):
        lv = len(hex)
        colors = tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return f"\033[48;2;{colors[0]};{colors[1]};{colors[2]}m"

    @staticmethod
    def href(description, link):
        return '\x1b]8;;' + link + '\x1b\\' + description + '\x1b]8;;\x1b\\'

def truncate(string, max_length):
    return (string[:max_length - 3] + '...') if len(string) >= (max_length - 3) else string

def printnb(*args, **kwargs):
    print(*args, **kwargs, end='')

def split_paragraph(paragraph, max_length):
    joined_row = []
    joined_paragraph = ''
    row_length = 0
    for token in paragraph.split():
        row_length += len(token) + 1
        if row_length >= max_length:
            joined_paragraph += ' '.join(joined_row) + '\n'
            joined_row = []
            row_length = len(token)
        joined_row.append(token)
    return joined_paragraph.rstrip()

def render(response, compatibility, max_width):
    terminal_w, terminal_h = shutil.get_terminal_size((80, 20))
    terminal_w = min(max_width, terminal_w) if not max_width == -1 else terminal_w

    safesearch_readable = [
        "None",
        "Medium",
        "Full"
    ]

    printnb(
        'Query: ' + repr(response.query) + ANSI.reset + '\n' +
        'Language: ' + ANSI.bold + response.language + ANSI.reset + '  ' +
        'SafeSearch: ' + ANSI.bold + safesearch_readable[int(response.safesearch)] + ANSI.reset + '  '
    )

    if response.category == 'general':
        printnb('Results: ' + ANSI.bold + f'{int(response.meta.result_count):,}' + ANSI.reset)

    printnb('\n\n')

    for index, article in zip(range(5), response.articles):
        article_engines = truncate(" ".join(article.engines), terminal_w)
        article_title = truncate(article.title, (terminal_w - 2 - len(article_engines)))
        header_spacer = " " * (terminal_w - (len(article_engines) + len(article_title)))

        print(article_title + header_spacer + article_engines)

        if compatibility:
            print(ANSI.fg_blue + article.url + ANSI.reset)
        else:
            print(ANSI.fg_blue + ANSI.href(truncate(article.url, terminal_w), article.url) + ANSI.reset)

        if index == 0:
            print(split_paragraph(article.description, terminal_w - 10))

        printnb('\n')