#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ruamel import yaml

yaml_path = '/home/pi/.homeassistant/configuration.yaml'
config_yaml_path = '../db/db.yaml'


# 获取userId
def get_user_id():
    yaml_file = open(config_yaml_path, 'r', encoding='utf8')
    yaml_config = yaml.round_trip_load(yaml_file)
    yaml_file.close()
    return yaml_config['userId']


# 获取配置文件
def get_config():
    yaml_file = open(yaml_path, 'r', encoding='utf8')
    yaml_config = yaml.round_trip_load(yaml_file)
    yaml_file.close()
    return yaml_config


# 写入配置文件
def set_config(yaml_config):
    with open(yaml_path, 'w+', encoding='utf8') as outfile:
        yaml.dump(yaml_config, outfile,
                  Dumper=yaml.RoundTripDumper,
                  block_seq_indent=2,
                  default_flow_style=False,
                  allow_unicode=True)
    yaml_file = open(yaml_path, 'r', encoding='utf8')
    yaml_config = yaml_file.read() \
        .replace("  name:",                 "    name:")  \
        .replace("  host:",                 "    host:")  \
        .replace("  token:",                "    token:")\
        .replace("  model:",                "    model:")\
        .replace("  hosts:",                "    hosts:")\
        .replace("  interval_seconds:",     "    interval_seconds:")\
        .replace("  exclude:",              "    exclude:")\
        .replace("    - 192.168.3.1",       "      - 192.168.3.1")\
        .replace("  consider_home",         "    consider_home")\
        .replace("  target_sensor:",        "    target_sensor:")\
        .replace("  scan_interval:",        "    scan_interval:")\
        .replace("  sensor:",               "    sensor:")\
        .replace("  pin:",                  "    pin:")\
        .replace("  monitored_conditions:", "    monitored_conditions:")\
        .replace("    - temperature",       "      - temperature")\
        .replace("    - humidity",          "      - humidity")\
        .replace("  app_id:",               "    app_id:")\
        .replace("  api_key:",              "    api_key:")\
        .replace("  secret_key:",           "    secret_key:")\
        .replace("  speed:",                "    speed:")\
        .replace("  pitch:",                "    pitch:")\
        .replace("  volume:",               "    volume:")\
        .replace("  person:",               "    person:")\
        .replace("  pin:",                  "    pin:")
    yaml_file.close()
    yaml_file = open(yaml_path, 'w', encoding='utf8')
    yaml_file.write(yaml_config)
    yaml_file.close()


# 添加开关
def add_switch(platform, word, name, host, token, model):
    yaml_config = get_config()
    yaml_config['switch'].append(
        {
            "platform": platform,
            "word": word,
            "name": name,
            "host": host,
            "token": token,
            "model": model
        }
    )
    set_config(yaml_config)


# 修改开关[根据名字]
def edit_switch(platform, word, name, host, token, model):
    yaml_config = get_config()
    for switch in yaml_config['switch']:
        if switch['name'] == name:
            switch['platform'] = platform
            switch['word'] = word
            switch['host'] = host
            switch['token'] = token
            switch['model'] = model
    set_config(yaml_config)


# 修改开关[所有]
def edit_switch_all(switch_list):
    yaml_config = get_config()
    yaml_config['switch'] = switch_list
    set_config(yaml_config)


# 删除开关
def del_switch(name):
    yaml_config = get_config()
    new_switch_list = []
    for switch in yaml_config['switch']:
        if switch['name'] != name:
            new_switch_list.append(switch)
    yaml_config['switch'] = new_switch_list
    set_config(yaml_config)
