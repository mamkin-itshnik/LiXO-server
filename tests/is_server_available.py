import os
import sys

import requests
from dotenv import load_dotenv


def get_vars():
    # env vars should be like: http 1.1.1.1 12345 /qawwedfweferg/
    return os.getenv('SCHEMA'), os.getenv('HOST'), os.getenv('PORT'), os.getenv('URL_PATH')


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    s, a, b, c = get_vars()
    url = f'{s}://{a}:{b}{c}'
    try:
        r = requests.get(url)
    except Exception as e:
        print('exception on connect')
        print(e)
        sys.exit(1)
    if 'Flask' not in r.text:
        print('wrong server response')
        sys.exit(2)
    print('ok')
    sys.exit(0)


if __name__ == '__main__':
    main()
