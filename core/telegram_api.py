import requests
import logging

from vk_graph_bot import settings


URL = 'https://api.telegram.org'
logger = logging.getLogger(__name__)


def invoke_telegram(method, photo=None, **kwargs):
    if photo:
        resp = requests.post(f'{URL}/bot{settings.TELEGRAM_BOT_TOKEN}/{method}', data=kwargs, files={'photo': photo})
    else:
        resp = requests.post(f'{URL}/bot{settings.TELEGRAM_BOT_TOKEN}/{method}', data=kwargs)
    logger.info('Response %s %s' % (resp, resp.content))
    return resp


