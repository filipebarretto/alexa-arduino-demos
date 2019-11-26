# -*- coding: utf-8 -*-

import six
import boto3
import json


iot = boto3.client('iot-data', region_name='us-east-1')
IOT_TOPIC = "iot_arduino_demos_actuators"

def iot_command(command):
    response = iot.publish(
                       topic=IOT_TOPIC,
                       qos=1,
                       payload=json.dumps({"command": command})
    )


def get_slots(slots):
    items = []
    resolved_slot = None
    for _, slot in six.iteritems(slots):
        print(slot)
        if slot.value is not None:
            resolved_slot = slot.value
            items.append(slot.value.lower())
    return items
