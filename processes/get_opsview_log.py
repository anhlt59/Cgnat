import time
import requests
import json
import re
import logging
from requests.packages import urllib3
urllib3.disable_warnings()


# Get token Opsview
def token_ops(user, password, ops_addr, logger):

    opsview_user = user
    opsview_password = password
    ops_token = ''

    payload = {
        'username': opsview_user,
        'password': opsview_password,
    }
    try:
        token_text = requests.post('https://' + ops_addr + '/rest/login',
                                   data=payload, verify=False)
        response = eval(token_text.text)
        if "token" in response:
            ops_token = response["token"]
        return ops_token
    except Exception as err:
        logger.error("Error get_opsview_log in token_ops(): {}".format(str(err)))


def get_host_config(user, token, ops_addr, hostname, config, logger):
    temp_device = {"device_name": "", "device_ip": "", "card": "",
                   "fpc_slot": "", "pic_slot": "", "log_message": "",
                   "time_stamp": ""}
    headers = {
        "Content-Type": "application/json",
        "X-Opsview-Username": user,
        "X-Opsview-Token": token,
    }
    list_temp_device = []
    temp_device["fpc_slot"] = []
    temp_device["pic_slot"] = []
    temp_device["log_message"] = []

    temp_device["device_name"] = hostname
    temp_device["device_ip"] = config.MAP_CGNAT[hostname]

    try:
        result = requests.get('https://' + ops_addr + '/rest/status/service?hostname=' + hostname, headers=headers,
                              verify=False)
        host_conf = json.loads(result.text)
        for service in host_conf['list'][0]['services']:
            current_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(int(service['last_check'])))
            if "Check bandwidth low threshold" in service['name'] and service['state'].lower() == "critical":
                mams = re.search(
                    r"\-((\d{1,2})\/(\d{1,2})\/(\d{1,2}))", service["output"])
                if mams:
                    card = mams.group(1)
                    fpc = mams.group(2)
                    pic = mams.group(3)
                    temp_device["card"] = str(card)
                    temp_device["fpc_slot"] = str(fpc)
                    temp_device["pic_slot"] = str(pic)
                    temp_device["log_message"] = "Critical card " + \
                        str(card) + " bandwidth low threshold"
                    temp_device["time_stamp"] = current_time
                else:
                    logger.debug(
                        hostname, ": Cannot find FPC and PIC by regex")
                list_temp_device.append(temp_device.copy())
        if len(list_temp_device) != 0:
            return list_temp_device
    except:
        logger.debug(hostname, ": Cannot get CGNAT by api")
    return False


def get_opsview(config):
    list_device = []
    logger = logging.getLogger(__name__)
    token = token_ops(config.USERNAME, config.PASSWORD,
                      config.OPS_ADDR, logger)
    for key in config.MAP_CGNAT:
        device = get_host_config(
            config.USERNAME, token, config.OPS_ADDR, key, config, logger)
        if device is not False:
            list_device += device
    result = config.RESULT
    if len(list_device) != 0:
        result['result'] = True
        result['data'] = list_device
        return result
    else:
        return result
