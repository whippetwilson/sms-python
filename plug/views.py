from __future__ import print_function

import json

import gammu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sms import settings


@csrf_exempt
def send(request=None):
    data = json.loads(request.body)[0]
    network = "others"
    recipient = str(data.get("recipient"))
    if recipient.startswith("256"):
        if recipient.startswith("25678") or recipient.startswith("25677"):
            network = "mtn"
        elif recipient.startswith("25675") or recipient.startswith("25670"):
            network = "airtel"

    message = data.get("message")
    message_id = data.get("id")
    state_machine = gammu.StateMachine()
    config = f"{settings.BASE_DIR / 'gammu/.gammurc'}_{network}"
    state_machine.ReadConfig(Filename=config)
    state_machine.Init()
    message = {
        "Text": message,
        "SMSC": {"Location": 1},
        "Number": int(recipient),
    }
    # Actually send the message
    try:
        reference = state_machine.SendSMS(message)
        return JsonResponse(
            {
                "sent": True if reference else None,
                "reference": reference,
                "id": message_id
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                "sent": False,
                "message": json.loads(json.dumps(str(e))),
                "id": message_id
            }
        )
