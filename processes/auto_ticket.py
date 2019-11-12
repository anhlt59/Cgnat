# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Auto SC ticket for NOC
We defined a period_time corresponding to Event_ID in payload
If this Event_ID is existed, we'll increase period_time with 1
and attempt again
"""

import requests
import json
from requests.packages import urllib3
urllib3.disable_warnings()


def auto_ticket(config, logger):
    period_time = 2211444
    url = config.URL
    headers = config.HEADERS
    payload = config.PAYLOAD
    payload['EventID'] = period_time

    # payload = json.dumps(payload)

    session = requests.Session()
    session.trust_env = False
    while True:
        try:
            period_time = period_time + 1
            payload['EventID'] = period_time
            response = session.post(url, data=json.dumps(payload),
                                    headers=headers, timeout=3)
            if response.status_code == 201:
                result = response.json()
                return result["id"]
        except Exception as err:
            logger.error("Error auto_ticket: {}".format(str(err)))
