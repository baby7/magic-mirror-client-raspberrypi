"""
HomeAssistant API Function
Author: 七仔的博客(www.baby7blog.com)
"""
import requests

base_url = "http://192.168.3.11:8123/"
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5NGIzZjRlYzIwOTA0ZTJkYTAzYjQyMTYzMDk1MmRlYSIsImlhdCI6MTU5MjU4NDEyNCwiZXhwIjoxOTA3OTQ0MTI0fQ.jTtjvLPvFDL5WXu1ByI_1liUYmxYk6iib7I93KAhLRg",
    "content-type": "application/json",
}


# 调用服务
def call_service(model, service, json):
    print("call_service")
    requests.post(base_url + "api/services/" + model + "/" + service, headers=headers, json=json)


# 获取状态
def get_state(entity_id):
    print("get_state")
    res = requests.get(base_url + "api/states/" + entity_id, headers=headers, json={})
    return res.json()


# 设置灯亮度[3-255]
def set_light_brightness(entity_id, brightness):
    json = {
        "entity_id": "light." + entity_id,
        "brightness_pct": brightness,
    }
    if get_state("light." + entity_id)["state"] == "on":
        call_service("light", "toggle", json)
        call_service("light", "toggle", json)
    else:
        call_service("light", "toggle", json)


# 设置灯色温[175-333]
def set_light_color_temp(entity_id, color_temp):
    json = {
        "entity_id": "light." + entity_id,
        "color_temp": color_temp
    }
    if get_state("light." + entity_id)["state"] == "on":
        call_service("light", "toggle", json)
        call_service("light", "toggle", json)
    else:
        call_service("light", "toggle", json)


# 同时设置灯的亮度和色温 - 亮度[3-255],色温[175-333]
def set_light(entity_id, brightness, color_temp):
    json_brightness = {
        "entity_id": "light." + entity_id,
        "brightness_pct": brightness,
    }
    json_color_temp = {
        "entity_id": "light." + entity_id,
        "color_temp": color_temp
    }
    json = {
        "entity_id": "light." + entity_id,
        "brightness_pct": brightness,
        "color_temp": color_temp
    }
    if get_state("light." + entity_id)["state"] == "on":
        call_service("light", "toggle", json_brightness)
        call_service("light", "toggle", json_color_temp)
    else:
        call_service("light", "toggle", json)


# 打开开关
def open_switch(entity_id):
    json = {
        "entity_id": "switch." + entity_id,
    }
    call_service("switch", "turn_on", json)


# 关闭开关
def close_switch(entity_id):
    json = {
        "entity_id": "switch." + entity_id,
    }
    call_service("switch", "turn_off", json)
