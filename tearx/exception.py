import traceback

import pathlib

from renderer import ANSI

import json

def make_exception(err, data, epilog):
    print(f"{ANSI.fg_red}Fatal error!{ANSI.reset}")
    print(traceback.format_exc())

    print(f"\n{ANSI.fg_blue}Relevant data:{ANSI.reset}")
    for point in data:
        print(json.dumps(point, indent=4))

    print(f"\n{ANSI.fg_blue}{epilog}{ANSI.reset}")
    exit(1)

def dump_response(response):
    main_path = Path.home() / '.tearx'
    with open(main_path / 'response.html', "w") as f:
        f.write(str(response))