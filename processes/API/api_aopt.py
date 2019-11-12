#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from requests.packages import urllib3
urllib3.disable_warnings()


# get AOPT token before request infomation (Job info, run service)
def get_token(username, password, logger):
    url = "https://tool.fpt.net/api/v1/login"
    payload = {
        'username': username,
        'password': password
    }
    try:
        token_text = requests.post(url, data=payload)
        response = json.loads(token_text.text)
        if "token_key" in response:
            token = response["token_key"]
            return token
    except Exception as err:
        logger.error("Error api_aopt in get_token(): {}".format(str(err)))


# run command on device, return job_id if true
def run_command(token, ip_address, command, logger):
    url = "https://tool.fpt.net/api/v1/run_command"
    headers = {"content-type": "application/json"}
    payload = {
        "token": token,
        "device_ip": ip_address,
        "command": command

    }
    payload = json.dumps(payload)
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()
        return result["id"]
    except Exception as err:
        logger.error("Error api_aopt in run_command(): {}".format(str(err)))


# get command response from device
def get_command(token, job_id, logger):
    url = "https://tool.fpt.net/api/v1/get_command"
    headers = {'content-type': "application/json"}
    payload = {
        "token": token,
        "id": job_id
    }
    payload = json.dumps(payload)
    try:
        session = requests.Session()
        session.trust_env = False
        response = session.post(url, data=payload, headers=headers)
#       response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()
        output = result["output"]
        state = result["state"]
        # print result
        return output, state
    except Exception as err:
        logger.error("Error api_aopt in get_command(): {}".format(str(err)))
