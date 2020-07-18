import json

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

from core.models import Logging, Admin
from core.telegram_api import invoke_telegram
from vk_graph_bot import settings


@csrf_exempt
def telegram_hook(request):
    update = json.loads(request.body)
    message = update.get('message')
    text = None

    if message is None:
        return HttpResponse('OK')

    text = message.get('text')

    if text is None:
        return HttpResponse('OK')

    command = text.split()[0]

    if command == '/user_graph' or command == '/group_graph':
        try:
            vk_id = int(text.split()[1])
            if command == '/user_graph':
                invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'], text=f'id юзера {vk_id}')
                Logging.objects.create(user_id=update['message']['chat']['id'], command='user_graph')
            elif command == '/group_graph':
                invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'], text=f'id группы {vk_id}')
                Logging.objects.create(user_id=update['message']['chat']['id'], command='group_graph')

        except IndexError:
            invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'], text='Вы не ввели id')
        except ValueError:
            invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'], text='id должен быть целым числом')

    elif command == '/stats':
        try:
            admin = Admin.objects.get(tg_id=int(update['message']['chat']['id']))
            users = len(Logging.objects.all())
            unic_users = len(Logging.objects.order_by().values_list('user_id').distinct())

            invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'],
                            text=f'Уникальных пользователей: {unic_users}\n Всего пользователей: {users}')

        except:
            invoke_telegram('sendMessage', chat_id=update['message']['chat']['id'],
                            text=f'Нет прав')

    elif command == '/add_admin' and settings.ADMIN_ID == int(update['message']['chat']['id']):
        tg_id = int(text.split()[1])
        Admin.objects.create(tg_id=tg_id)
    elif command == '/delete_admin' and settings.ADMIN_ID == int(update['message']['chat']['id']):
        tg_id = int(text.split()[1])
        Admin.objects.get(tg_id=tg_id).delete()


    return HttpResponse('OK')
