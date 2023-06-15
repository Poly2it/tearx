import requests

from parser import parse_response

from cache import search_cache, write_cache

HOST = 'https://searx.fmac.xyz/search'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'

HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-CSRFToken': 'a',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': HOST,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
}

def search(query, **kwargs):
    dargs = {
        'category': 'general',
        'language': 'en-US',
        'page': '1',
        'time_range': '',
        'image_proxy': '1',
        'safesearch': '0',
        'enabled_engines': '',
        'disabled_engines': ''
    }

    dargs.update(kwargs)

    result = search_cache((query, *dargs.values()))
    if result is None:
        result = search_host(query, **dargs)

    return result

    
def search_host(query, **kwargs):
    dargs = {
        'category': 'general',
        'language': 'en-US',
        'page': '1',
        'time_range': '',
        'image_proxy': '1',
        'safesearch': '0',
        'enabled_engines': '',
        'disabled_engines': ''
    }

    dargs.update(kwargs)

    params = {
        'q': query,
        'language': dargs['language'],
        'pageno': dargs['page'],
        'time_range': dargs['time_range'],
        'safesearch': dargs['safesearch'],
        'theme': 'simple'
    }
    
    categories = {
        "general": {'category_general': '1'},
        "images": {'category_images': '1'},
        "videos": {'category_videos': '1'},
        "news": {'category_news': '1'},
        "map": {'category_map': '1'},
        "music": {'category_music': '1'},
        "it": {'category_it': '1'},
        "science": {'category_science': '1'},
        "files": {'category_files': '1'},
        "social_media": {'category_social media': '1'}
    }

    params.update(categories[dargs['category']])

    cookies = {
        'categories': dargs['category'],
        'language': dargs['language'],
        'locale': 'en',
        'autocomplete': '',
        'image_proxy': dargs['image_proxy'],
        'method': 'GET',
        'safesearch': '1',
        'theme': 'simple',
        'results_on_new_tab': '0',
        'doi_resolver': 'oadoi.org',
        'simple_style': 'auto',
        'center_alignment': '1',
        'query_in_title': '0',
        'infinite_scroll': '0',
        'disabled_engines': dargs['disabled_engines'],
        'enabled_engines': dargs['enabled_engines'],
        'disabled_plugins': '',
        'enabled_plugins': '',
        'tokens': '',
        'maintab': '1',
        'enginetab': '1'
    }

    response = requests.get(HOST, params=params, headers=HEADERS, cookies=cookies) 
    response.raise_for_status()
    parsed_response = parse_response(response.content)

    write_cache((query, *dargs.values()), parsed_response)
    
    return(parsed_response)