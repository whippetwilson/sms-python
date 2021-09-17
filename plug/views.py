from __future__ import print_function

import json
import uuid

from django.utils import timezone

import gammu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from plug.models import get_outbound_message
from sms import settings


@csrf_exempt
def send(request=None):
    _data = json.loads(request.body)
    to_send = []
    for data in _data:
        network = "others"
        recipient = str(data.get("recipient"))
        if recipient.startswith("256"):
            if recipient.startswith("25678") or recipient.startswith("25677"):
                network = "mtn"
            elif recipient.startswith("25675") or recipient.startswith("25670"):
                network = "airtel"
        config = f"{settings.BASE_DIR / 'gammu/.gammurc'}_{network}"
        __message = data.get("message")
        message_id = data.get("id")
        _message = {
            "Text": __message,
            "SMSC": {"Location": 1},
            "Number": int(recipient),
            "id": message_id,
            "config_path": config
        }
        to_send.append(_message)
    # Actually send the message
    sent = 0
    failed = 0
    total = len(to_send)
    outbound_messages = []
    for message in to_send:
        try:
            state_machine = gammu.StateMachine()
            config = message.get("config_path")
            state_machine.ReadConfig(Filename=config)
            state_machine.Init()
            reference = state_machine.SendSMS(message)
            sent = sent+1 if reference else sent+0
            sent_status = True if reference else False
            outbound_messages.append(
                get_outbound_message(reference, timezone.now(), message.get("id"),
                                     message.get("Number"), timezone.now(), sent_status, "", message.get('Text'))
            )
        except Exception as e:
            failed = failed + 1
            sent_status = False
            outbound_messages.append(
                get_outbound_message(None, timezone.now(), message.get("id"),
                                     message.get("Number"), timezone.now(), sent_status,
                                     json.loads(json.dumps(str(e))),
                                     message.get("Text"))
            )
    return JsonResponse({
        "sent": sent,
        "id": uuid.uuid4(),
        "provider": None,
        "sender": "",
        "total": total,
        "failed": failed,
        "outboundMessages": outbound_messages
    })
