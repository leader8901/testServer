from random import random

import requests
from flask import Flask, request

from conf import (
    get_healthy_server,
    healthcheck,
    load_configuration,
    process_firewall_rules_flag,
    process_rules,
    process_rewrite_rules,
    transform_backends_from_config,
)

loadbalancer = Flask(__name__)

MAIL_BACKENDS = ['localhost:8081', 'localhost:8082']
YANDEX_BACKENDS = ['localhost:9081', 'localhost:9082']

config = load_configuration('balancer.yaml')
register = transform_backends_from_config(config)


@loadbalancer.route('/')
def router():
    host_header = request.headers['Host']
    if host_header == 'www.mail.ru':
        response = requests.get(f'http://{random.choice(MAIL_BACKENDS)}')
        return response.content, response.status_code
    elif host_header == 'www.yandex.ru':
        response = requests.get(f'http://{random.choice(YANDEX_BACKENDS)}')
        return response.content, response.status_code
    else:
        return 'Not Found', 404

@loadbalancer.route('/mail')
def mmail_path():
    response = requests.get(f'http://{random.choice(MAIL_BACKENDS)}')
    return response.content, response.status_code


@loadbalancer.route('/yandex')
def yandex_path():
    response = requests.get(f'http://{random.choice(YANDEX_BACKENDS)}')
    return response.content, response.status_code