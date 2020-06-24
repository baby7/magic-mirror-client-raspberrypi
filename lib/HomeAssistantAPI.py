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
# 设置灯亮度[1-100]
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


# **********************************************************************************************************************
# 模块：小米万能遥控器
# **********************************************************************************************************************
# 电视开关
def control_tv(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_dianshi"
    }
    call_service("remote", "send_command", json)


# 机顶盒开关
def control_box(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_jidinghe"
    }
    call_service("remote", "send_command", json)


# 风扇开关
def control_fan(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_fengshan"
    }
    call_service("remote", "send_command", json)


# 风扇风速
def control_fan_speed(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_fengshan_fengsu"
    }
    call_service("remote", "send_command", json)


# 风扇摇头
def control_fan_head(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_fengshan_yaotou"
    }
    call_service("remote", "send_command", json)


# 风扇定时
def control_fan_time(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_fengshan_dingshi"
    }
    call_service("remote", "send_command", json)


# 空调制冷
def control_air_conditioning_cold(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_kongtiao_zhileng"
    }
    call_service("remote", "send_command", json)


# 空调除湿
def control_air_conditioning_wet(entity_id):
    json = {
        "entity_id": "remote." + entity_id,
        "command": "control_kongtiao_chushi"
    }
    call_service("remote", "send_command", json)
