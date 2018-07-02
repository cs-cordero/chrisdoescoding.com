import json
import os
import requests

hulu_access_token = os.environ.get('SP_ACCESS_TOKEN')
if not hulu_access_token:
    raise Exception('Could not find the Hulu Access Token!  Do not commit this'
                    ' token to source control.  Do a search in a browser and'
                    ' get your access token from the browser.')

url = 'https://mozart.hulu.com/v1.h2o/shows/6979/episodes'
get_params = {
    'include_seasons': True,
    'show_id': 6979,
    'sort': 'seasons_and_release',
    'video_type': 'episode',
    '_language': 'en',
    '_region': 'us',
    'items_per_page': 100,
    'position': 0,
    'region': 'us',
    'locale': 'en',
    'language': 'en',
    'require_ssl': 1,
    'access_token': hulu_access_token,
    'isHttps': True,
}
relevant_keys = ('id', 'description', 'duration', 'eid', 'episode_number',
                 'original_premiere_date', 'season_number', 'show_id', 'title',
                 'thumbnail_url', 'show')


def get_south_park_data():
    items_per_page = 100
    position = 0
    data = []
    while True:
        get_params.update({
            'position': position,
            'items_per_page': items_per_page,
        })
        response = requests.get(url, get_params).json()
        if not response['data']:
            break
        for episode in response['data']:
            video = episode['video']
            _dict = {key: video.get(key) for key in relevant_keys}
            data.append(_dict)
        position += 100
    return data


def write_data_to_file(data):
    with open('southpark.json', 'w') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    south_park_data = get_south_park_data()
    write_data_to_file(south_park_data)
