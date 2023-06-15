from traffic import search

from args import get_args

from renderer import render

def main():
    args = get_args()
    response = search(query=args.query, safesearch=args.safesearch, language=args.language)
    render(response, args.compatibility, int(args.max_width))

if __name__ == '__main__':
    main()