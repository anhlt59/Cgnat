"""Get kibana log."""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import re
import heapq
import time
from datetime import datetime
from collections import defaultdict
from elasticsearch import Elasticsearch


def get_kibana(config, logger):
    """Main get kibana log."""
    now = time.time()
    past = now - config.QUERY_TIME
    result = config.RESULT
    query = config.QUERY_ELASTIC
    query["query"]["filtered"]["filter"]["bool"]["must"][0]["range"]["@timestamp"]["from"] = int(
        past * 1000)
    query["query"]["filtered"]["filter"]["bool"]["must"][0]["range"]["@timestamp"]["to"] = int(
        now * 1000)
    # Connect to KIBANA
    try:
        es = Elasticsearch('118.69.247.119:9200', timeout=3)
        # get data
        log = es.search(index="logstash-*", body=query)
        # log = config.LOG
        # data format
        log = format_log(config, modify_log(config, log['hits']['hits']))
        if len(log) > 0:
            result.update({'data': log, 'result': True})
    except Exception as err:
        logger.error(
            "Error get_kibana_log in get_kibana(): {}".format(str(err)))
    return result


def format_log(config, log):
    """Sort log kibana."""
    d = defaultdict(lambda: {}, {})
    # Sort by ip
    for i in range(len(log)):
        if log[i]['card'] not in d[log[i]['device_ip']]:
            d[log[i]['device_ip']][log[i]['card']] = [log[i]]
        else:
            d[log[i]['device_ip']][log[i]['card']].append(log[i])
    # Sort by card
    result = []
    for host in d:
        for card in d[host]:
            # last log for each type_err and host (using time_stamp to compare)
            result.extend(heapq.nlargest(1, d[host][card],
                                         key=lambda x: time.strptime(
                                         x['time_stamp'], '%Y-%m-%d %H:%M:%S')))
    return result


def modify_log(config, log):
    """Format log kibana."""
    for i in range(len(log)):
        # regex to match type err
        type_err = re.search(config.REG_ERR, log[i]['_source']['message'])
        for pattern in config.REG_PIC:
            # regex to match fpc_slot, pic_slot
            re_pic = re.search(pattern, log[i]['_source']['message'])
            try:
                fpc_slot, pic_slot = re_pic.group(1), re_pic.group(2)
                time_stamp = ' '.join([log[i]['_source']['@timestamp'].split('T')[0],
                                       log[i]['_source']['syslog_timestamp'].split(' ')[-1]])
                time_stamp = datetime.strptime(time_stamp, '%Y-%d-%m %H:%M:%S')
                log[i] = {
                    'device_ip': log[i]['_source']['host'],
                    'device_name': log[i]['_source']['logsource'],
                    'fpc_slot': fpc_slot,
                    'pic_slot': pic_slot,
                    'log_message': type_err.group(),
                    'time_stamp': time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'card': '{}/{}/0'.format(fpc_slot, pic_slot)
                }
                break
            except:
                pass
    return log
