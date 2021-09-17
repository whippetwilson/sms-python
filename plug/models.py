from django.db import models


# Create your models here.

def get_outbound_message(message_id, time, uuid, recipient, dispatch_date, sent_status, error_message):
    return {
        "messageId": message_id,
        "type": "OUTBOUND",
        "date": time,
        "text": "req.message",
        "uuid": uuid,
        "encoding": "ENC7BIT",
        "dstPort": -1,
        "srcPort": -1,
        "recipient": recipient,
        "dispatchDate": dispatch_date,
        "validityPeriod": -1,
        "statusReport": sent_status,
        "from": "",
        "messageStatus": "SUCCESS" if sent_status else "FAILED",
        "failureCause": "" if sent_status else "NO_ROUTE",
        "retryCount": 0,
        "priority": 0,
        "refNo": "",
        "errorMessage": error_message,
        "scheduledDeliveryDate": dispatch_date,
        "flashSms": False,
        "pduUserDataHeader": None,
        "pduUserData": None,
        "deliveryDelay": 0,
        "dcsmessageClass": "MSGCLASS_NONE",
        "gatewayId": "*"
    }
