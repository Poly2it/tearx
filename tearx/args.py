import argparse

from difflib import get_close_matches

from renderer import ANSI

def get_args():
    parser = argparse.ArgumentParser(
                        prog='tearx',
                        formatter_class=argparse.MetavarTypeHelpFormatter,
                        description='Search the web from your terminal like a true hacker.',
                        #epilog='Text at the bottom of help'
    )

    languages = {'ca', 'ca-ES', 'da', 'da-DK', 'de', 'de-AT', 'de-CH', 'de-DE', 'et', 'et-EE', 'en', 'en-AU', 'en-CA', 'en-GB', 'en-IE', 'en-IN', 'en-MY', 'en-NZ', 'en-PH', 'en-US', 'en-ZA', 'es', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'es-US', 'fr', 'fr-BE', 'fr-CA', 'fr-CH', 'fr-FR', 'hr', 'id', 'id-ID', 'it', 'it-CH', 'it-IT', 'lv', 'lt', 'hu', 'hu-HU', 'nl', 'nl-BE', 'nl-NL', 'nb', 'nb-NO', 'pl', 'pl-PL', 'pt', 'pt-BR', 'pt-PT', 'ro', 'ro-RO', 'sk', 'sl', 'fi', 'fi-FI', 'sv', 'sv-SE', 'vi', 'tr', 'tr-TR', 'is', 'cs', 'cs-CZ', 'el', 'el-GR', 'bg', 'bg-BG', 'ru', 'ru-RU', 'sr', 'uk', 'he', 'ar', 'hi', 'th', 'th-TH', 'zh', 'zh-CN', 'zh-HK', 'zh-TW', 'ja', 'ja-JP', 'ko', 'ko-KR'}

    parser.add_argument('query',
                        help="Your search query.",
                        type=str
                        )
    parser.add_argument('-sas', 
                        '--safesearch', 
                        choices=['0', '1', '2'],
                        type=str,
                        default='1',
                        required=False,
                        help="Use built-in censorship."
                        ) 
    parser.add_argument('-l', 
                        '--language', 
                        type=str,
                        default='en-US',
                        required=False,
                        help="Pass a language code to get results in different languages."
                        ) 
    parser.add_argument('-comp', 
                        '--compatibility', 
                        action='store_true',
                        required=False,
                        help="Avoid modern ansi sequences."
                        ) 
    parser.add_argument('-mxw', 
                        '--max-width', 
                        type=int,
                        default='-1',
                        required=False,
                        help="Set the max width for terminal output. Use -1 for unlimited."
                        ) 
    args = parser.parse_args()

    if not args.language in languages:
        matches = get_close_matches(args.language, languages)
        if len(matches) > 0:
            print(
                f"{ANSI.fg_red}[E]{ANSI.reset} '{args.language}' is not a valid language.\n\
                Did you mean {render_list(matches, ' or ')}?"
            )
        else:
            print(
                f"{ANSI.fg_red}[E]{ANSI.reset} '{args.language}' is not a valid language."
            )
        exit(1)

    return args

def render_list(list, separator_keyword):
    return ', '.join(list[:-1]) + separator_keyword + list[-1] if len(list) > 1 else list[0]