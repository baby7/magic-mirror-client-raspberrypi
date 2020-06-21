"""
HomeAssistant API Function
Author: 七仔的博客(www.baby7blog.com)
"""
import requests

base_url = "http://192.168.3.11:8123/"
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhOWQ1NmVjMjUzMzY0YmViYTNmNGEzNWYwZmYxMmQ3YiIsImlhdCI6MTU5MjcxMjE0OCwiZXhwIjoxOTA4MDcyMTQ4fQ.-ZH_WywatucaQNzCWq1rXHbjfg6hK2lvutcq8__I1q4",
    "content-type": "application/json",
}


# 调用服务
def call_service(model, service, json):
    requests.post(base_url + "api/services/" + model + "/" + service, headers=headers, json=json)


# 获取状态
def get_state(entity_id):
    res = requests.get(base_url + "api/states/" + entity_id, headers=headers, json={})
    return res.json()


# **********************************************************************************************************************
# 模块：灯
# **********************************************************************************************************************
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


# **********************************************************************************************************************
# 模块：开关
# **********************************************************************************************************************
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


# **********************************************************************************************************************
# 模块：传感器
# **********************************************************************************************************************
# 获取温湿度
def get_temp_and_hum(entity_id_temp, entity_id_hum):
    return (get_state("sensor." + entity_id_temp)["state"],
            get_state("sensor." + entity_id_hum)["state"])