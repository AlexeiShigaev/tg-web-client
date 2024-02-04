import configparser
from pathlib import Path
import os

PROJECT_DIR = Path(__file__).parent.resolve()


def get_config():
    conf = configparser.ConfigParser(allow_no_value=True)
    config_filename = os.path.join(PROJECT_DIR, 'config.ini')
    print("\nPROJECT_DIR:\t\t", PROJECT_DIR)
    print("config_filename:\t", config_filename)

    # if default config is npt exist
    if not os.path.isfile(config_filename):
        _create_default_config(conf, config_filename)

    conf.read(config_filename)

    # check config is valid
    _check_config(conf, config_filename)
    return conf


def _create_default_config(conf_parser, filename):
    conf_parser.add_section('telegram_api')
    conf_parser.set('telegram_api', '; obtain api keys here: https://core.telegram.org/api/obtaining_api_id')
    conf_parser.set('telegram_api', '; api_id and api_hash are needed for the application to work')
    conf_parser.set('telegram_api', 'api_id', '*api_id here*')
    conf_parser.set('telegram_api', 'api_hash', '*api_hash here*')
    conf_parser.set('telegram_api', 'bind_host', '*bind_host as str here*')
    conf_parser.set('telegram_api', 'bind_port', '*bind_port as int here*')
    conf_parser.set('telegram_api', 'uvicorn_workers', '*uvicorn_workers as int here*')
    conf_parser.set('telegram_api', '; in production set uvicorn_reload=False')
    conf_parser.set('telegram_api', 'uvicorn_reload', '*uvicorn_reload as BOOL here*')

    conf_parser.add_section('db')
    conf_parser.set('telegram_api', '; database_url=postgresql+asyncpg://username:userpasswd@host:port/dbname')
    conf_parser.set('db', 'database_url')

    conf_parser.write(open(filename, 'w'))


def _check_config(conf_parser, filename):
    api_id = conf_parser.get('telegram_api', 'api_id')
    api_hash = conf_parser.get('telegram_api', 'api_hash')

    if api_id == '*api_id here*' or api_hash == 'api_hash':
        print('Please, edit the config file: ' + filename)
        exit(1)


config = get_config()
