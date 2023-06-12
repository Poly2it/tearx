import requests

from parser import Article, QueryPage, parse_results

from cache import hash_query, read_cached, write_cache, get_cache_paths

from exception import make_exception, dump_response

import math

HOST = 'https://searx.fmac.xyz/search'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'

def search(
        query, 
        category='general', 
        language='en-US', 
        page='1', 
        time_range='', 
        image_proxy='1', 
        safesearch='0', 
        enabled_engines='', 
        disabled_engines=''):

    search_hash = hash_query(
        query,
        category, 
        language, 
        page, 
        time_range,
        image_proxy,
        safesearch,
        enabled_engines,
        disabled_engines)
    
    if category == 'general':
        # TODO: implement caching for other media types

        cached_item = read_cached(search_hash)

        if not cached_item == None:
            return cached_item

    params = {
        'q': query,
        'language': language,
        'pageno': page,
        'time_range': time_range,
        'safesearch': safesearch,
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

    params.update(categories[category])

    cookies = {
        'categories': category,
        'language': language,
        'locale': 'en',
        'autocomplete': '',
        'image_proxy': image_proxy,
        'method': 'GET',
        'safesearch': '1',
        'theme': 'simple',
        'results_on_new_tab': '0',
        'doi_resolver': 'oadoi.org',
        'simple_style': 'auto',
        'center_alignment': '1',
        'query_in_title': '0',
        'infinite_scroll': '0',
        'disabled_engines': disabled_engines,
        'enabled_engines': enabled_engines,
        'disabled_plugins': '',
        'enabled_plugins': '',
        'tokens': '',
        'maintab': '1',
        'enginetab': '1'
    }

    headers = {
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

    try:
        response_data = requests.get(HOST, params=params, headers=headers, cookies=cookies)
        
        response = response_data.content

        response_data.raise_for_status()

        parsed_response = parse_results(response)

        if category == 'general':
            write_cache(search_hash, parsed_response)

        return parsed_response

    except Exception as err:
        make_exception(err, [params, cookies, headers], 'Dumped response.')
        dump_response()

def open_cache(file):
    with open('response.txt', 'r') as f:
        cache = f.read()
    return parse_results(cache)