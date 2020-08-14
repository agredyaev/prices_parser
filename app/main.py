import argparse
from models import *
from grabber import *
from tqdm import tqdm
from config import Config
from itertools import chain
from multiprocessing import Pool, cpu_count

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('sample.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def arg_parser():
    parser = argparse.ArgumentParser(description='Process some cities names')
    parser.add_argument('-l', '--log', action='store_true',
                        default=False, help='to clean up log file')
    parser.add_argument('-e', '--elapsed', action='store_true',
                        default=False, help='to clean up elapsed links file')
    parser.add_argument('names', nargs='*',
                        help='Availible options:moskva ekaterinburg ufa omsk voronezh kazan volgograd sankt-peterburg perm')

    args = parser.parse_args()

    for name, val in zip(('sample', 'elapsed'), (args.log, args.elapsed)):
        if val:
            with open(f'{name}.log', 'w'):
                pass
    return args.names


def make_input(url):
    return InputMaker(url).make_input()


def get_links():
    try:
        links = make_links(arg_parser())
        pool = Pool(cpu_count() - 1)
        result = pool.map(make_input, links)
        pool.close()
        pool.join()
        return list(chain.from_iterable(result))
    except Exception:
        print('Falied to get retailes list')
        logger.exception('Falied to get retailes list')


def links_from_file():
    with open('input.txt') as file:
        return file.read().split()


def worker(url):
    try:
        data = InputParser(url).get_data()
        # insert data to db
        with db.atomic():
            Offers.insert_many(data, fields=FIELDS).execute()
        with open('elapsed.log', 'a') as file:
            file.write(f'{url}\n')
    except Exception:
        logger.exception(f'{url} failed to parse page')
# TODO: прописать более глубокие уровни исключений


def get_unfinished(links):
    with open('elapsed.log') as file:
        reader = file.read()
        return links if not reader else list(set(links) - set(reader.split()))


if __name__ == '__main__':
        # print(*get_links())
    db.connect()
    # tasks = get_unfinished(get_links())
    tasks = get_unfinished(links_from_file())
    pool = Pool(cpu_count() - 1)

    for _ in tqdm(pool.imap_unordered(worker, tasks), total=len(tasks)):
        pass

    pool.close()
    pool.join()
