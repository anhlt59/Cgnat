# !/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from os import path
from datetime import datetime

# Log
PATH = path.dirname(path.abspath(__file__))
FILE_LOG = '.'.join([datetime.strftime(datetime.now(), "%Y-%m-%d"), 'log'])
LOG_PATH = path.join(PATH, 'log', FILE_LOG)

# GiangLMC configuration
path_jsnap = path.join(PATH, 'processes')
command_jsnap = ' && jsnap '
pass_config = ' -l noctool -p noctool@123 {}'.format(path_jsnap)
timeout = 15
RESULT = {"result": False, "data": []}


class AutoTicket(object):
    """Auto Ticket config."""

    URL = "http://172.30.13.69:3000/nafautoticket/listalertinfo/"
    HEADERS = {
        "Accept": "application/json",
        "Authorization": "Basic bm9jOm5vY0AxMjM7Ow==",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json"
    }
    PAYLOAD = {
        "AlertPlan": "Hệ thống Core IP",
        "KeyWord": "API_INPUT_NOCNET_CGNAT_TOOL",
        "HostName": "LANP024.038/HO_FTTHNew",
        "EventID": 'period_time',
        "EventType": 0,
        "ObjectID": 143239,
        "Output": "[]",
        "ServiceName": "Testing CGNAT API",
        "HostState": "None",
        "ServiceState": "critical",
        "EventDateTime": "2018-10-09T11:00:10"
    }


class KibanaConfig(object):
    """Kibana config."""
    LOG = {'_shards': {'failed': 0, 'successful': 130, 'total': 130},
           'hits': {'hits': [{'_id': 'AWb-05Nt_RCHcO4xIUOX',
                              '_index': 'logstash-2018.11.10',
                              '_score': 1.0,
                              '_source': {'@timestamp': '2018-28-12T18:12:50.574Z',
                                          '@version': '1',
                                          'host': '118.70.0.137',
                                          'logsource': 'HNI-MX960-LAB',
                                          'message': '<27>Nov 11 01:12:50 '
                                          'HNI-MX960-LAB spd[12821]: '
                                          '%DAEMON-3-SPD_CONN_OPEN_FAILURE: '
                                          'spd_nat_src_pool_set_query: unable '
                                          'to open connection to ms-11/0/0 '
                                          '(Network is down)',
                                          'syslog_facility': 'daemon',
                                          'syslog_facility_code': 3,
                                          'syslog_pri': '27',
                                          'syslog_severity': 'error',
                                          'syslog_severity_code': 3,
                                          'syslog_timestamp': 'Dec 28 15:38:00',
                                          'tags': ['nocftel',
                                                   '_grokparsefailure',
                                                   'got_syslog_pri'],
                                          'type': 'syslog'},
                              '_type': 'syslog'},

                             {'_id': 'AWb-1TNE_RCHcO4xIWvr',
                              '_index': 'logstash-2018.11.10',
                              '_score': 1.0,
                              '_source': {'@timestamp': '2018-28-12T18:14:36.265Z',
                                          '@version': '1',
                                          'host': '118.70.0.137',
                                          'logsource': 'HNI-MX960-LAB',
                                          'message': '<27>Nov 11 01:14:36 '
                                          'HNI-MX960-LAB : %DAEMON-3: (FPC '
                                          'Slot 11, PIC Slot 0)  ms02 '
                                          'mspmand[230]: Unexpected shutdown '
                                          'of connection to datapath-traced, '
                                          'trying to reconnect',
                                          'syslog_facility': 'daemon',
                                          'syslog_facility_code': 3,
                                          'syslog_pri': '27',
                                          'syslog_severity': 'error',
                                          'syslog_severity_code': 3,
                                          'syslog_timestamp': 'Dec 28 15:39:00',
                                                              'tags': ['nocftel',
                                                                       '_grokparsefailure',
                                                                       'got_syslog_pri'],
                                                              'type': 'syslog'},
                              '_type': 'syslog'},

                             {'_id': 'AWb-1LmM_RCHcO4xIWED',
                              '_index': 'logstash-2018.11.10',
                              '_score': 1.0,
                              '_source': {'@timestamp': '2018-28-12T18:14:05.389Z',
                                          '@version': '1',
                                          'host': '118.70.0.137',
                                          'logsource': 'HNI-MX960-LAB',
                                          'message': '<27>Nov 11 01:14:05 '
                                          'HNI-MX960-LAB spd[12821]: '
                                          '%DAEMON-3-SPD_CONN_OPEN_FAILURE: '
                                          'spd_nat_src_pool_set_query: unable '
                                          'to open connection to ms-11/0/0 '
                                          '(Connection refused)',
                                          'syslog_facility': 'daemon',
                                          'syslog_facility_code': 3,
                                          'syslog_pri': '27',
                                          'syslog_severity': 'error',
                                          'syslog_severity_code': 3,
                                          'syslog_timestamp': 'Dec 28 15:40:00',
                                          'tags': ['nocftel',
                                                   '_grokparsefailure',
                                                   'got_syslog_pri'],
                                          'type': 'syslog'},
                              '_type': 'syslog'}],
                    'max_score': 1.0,
                    'total': 100},
           'timed_out': False,
           'took': 133}
    # result
    RESULT = {"result": False, "data": []}
    # query time
    QUERY_TIME = 300
    # query for ElasticSearch
    QUERY_ELASTIC = {
        "from": 0, "size": 1000,
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "@timestamp": {
                                        "from": 'past',
                                        "to": 'now'
                                    }
                                }
                            },
                            {
                                "fquery": {
                                    "query": {
                                        "bool": {"should": [
                                            {
                                                "query_string": {
                                                    "query": '118.70.0.100'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.70.0.137'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.70.0.251'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.70.0.1'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.69.185.193'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.69.185.225'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.69.185.251'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.69.185.252'
                                                }
                                            },
                                            {
                                                "query_string": {
                                                    "query": '118.69.255.251'
                                                }
                                            },
                                        ]
                                        }
                                    }
                                }
                            },
                            {
                                "fquery": {
                                    "query": {
                                        "bool": {"should": [
                                            {
                                                "query_string":
                                                {
                                                    "query": "message:(\"SPD_CONN_OPEN_FAILURE\")"
                                                }
                                            },
                                            {
                                                "query_string":
                                                {
                                                    "query": "message:(\"mspsmd_connection_shutdown\")"
                                                }

                                            },
                                            {
                                                "query_string":
                                                {
                                                    "query": "message:(\"ECC errors uncorrectable\")"
                                                }
                                            },
                                            {
                                                "query_string":
                                                {
                                                    "query": "message:(\"Unexpected shutdown of connection to datapath-traced\")"
                                                }
                                            },
                                        ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
    # Regex to match err
    REG_ERR = r'(SPD_CONN_OPEN_FAILURE)|'\
        r'(mspsmd_connection_shutdown)|'\
        r'(ECC\serrors\suncorrectable)|'\
        r'(Unexpected\sshutdown\sof\sconnection\sto\sdatapath-traced)'
    # Regex to match fpc_slot, pic_slot
    REG_PIC = [r'FPC\sSlot\s(\d+),\sPIC\sSlot\s(\d+)',
               r'SPD_CONN_OPEN_FAILURE.+\-(\d+)\/(\d+)']


class AoptConfig(object):
    """Aopt config."""

    # account AOPT
    USERNAME = 'anhlt59'
    PASSWORD = '1234567890'

    # shutdown PIC
    COMMAND_SHUTDOWN = 'request chassis pic pic-slot {{b}} fpc-slot {{a}} offline\n'\
                       'show chassis fpc pic-status {{a}} | match "PIC {{b}}"\n'\
                       'edit\n'\
                       'rollback 0\n'\
                       'set chassis fpc {{a}} pic {{b}} power off\n'\
                       'show | compare\n'\
                       'commit check\n'\
                       'commit\n'

    PATTERN_SHUTDOWN = r'((pic\s{{b}}\soffline)|'\
                       r'(pic\s{{b}}\sis\salready\soffline))'
    # reboot PIC
    COMMAND_REBOOT = 'request chassis pic pic-slot {{b}} fpc-slot {{a}} offline\n'\
                     'show chassis fpc pic-status {{a}} | match "PIC {{b}}"\n'\
                     'request chassis pic pic-slot {{b}} fpc-slot {{a}} online\n'\
                     'show chassis fpc pic-status {{a}} | match "PIC {{b}}"\n'

    PATTERN_REBOOT = r'((pic\s{{b}}\soffline)|'\
                     r'(pic\s{{b}}\sis\salready\soffline))'\
                     r'.+(pic\s{{b}}\sonline)'

    # uptime check command
    UPTIME_COMMAND = "show chassis pic pic-slot {{b}} fpc-slot {{a}} | display json"

    # traffic check command
    TRAFFIC_COMMAND = 'show interfaces mams-{{a}}/{{b}}/0 | match "Physical Link|Input rate|Output rate"'

    COMMAND_OFFLINE = "show chassis pic pic-slot {{b}} fpc-slot {{a}}"
    PATTERN_OFFLINE = 'Online'


class OpsviewConfig(object):
    """Opsview Config."""

    # account Opsview
    USERNAME = 'anhlt59'
    PASSWORD = '1234567890'
    # result
    RESULT = {"result": False, "data": []}
    # address opsview
    OPS_ADDR = "210.245.0.226"
    # list CGNAT
    MAP_CGNAT = {
        "HCM-CGNAT-01": "118.69.185.193",
        "HCM-CGNAT-02": "118.69.185.225",
        "HCM-CGNAT-03": "118.69.185.251",
        "HN-CGNAT-01": "118.70.0.100",
        "HCM-CGNAT-04": "118.69.185.252",
        "HCM-CGNAT-05": "118.69.255.251",
        "HN-CGNAT-02": "118.70.0.137",
        "HN-CGNAT-03": "118.70.0.251",
        "HNI-NIX-01": "118.70.0.1",
        "HNI-MX960-LAB": '118.70.0.137'}


# huydx6 configuration

def config(filename='database.ini', section='mysql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    filename = path.join(PATH, filename)
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        db['port'] = int(db['port'])  # convert port to integer
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db
