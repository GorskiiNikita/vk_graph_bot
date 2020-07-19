from core.telegram_api import invoke_telegram
from vk_graph_bot.celery import app
import time


@app.task
def test(tg_id):
    time.sleep(5)
    invoke_telegram('sendMessage', chat_id=tg_id, text='test')


