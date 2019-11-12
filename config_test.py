"""File config for test."""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio


KIBANA = {"result": True, "data": [{'card': '11/0/0',
                                    'device_ip': '118.70.0.137',
                                    'device_name': 'HNI-MX960-LAB',
                                    'fpc_slot': '11',
                                    'log_message': 'SPD_CONN_OPEN_FAILURE',
                                    'pic_slot': '0',
                                    'time_stamp': '2018-12-26 16:50:00'}]}

# KIBANA_LOG_1 = {"result": True, "data": [{'card': '11/0/0',
#                                           'device_ip': '118.70.0.137',
#                                           'device_name': 'HNI-TEST',
#                                           'fpc_slot': '11',
#                                           'log_message': 'SPD_CONN_OPEN_FAILURE',
#                                           'pic_slot': '0',
#                                           'time_stamp': '2018-09-23 07:17:02'}]}


# KIBANA_LOG_2 = {"result": True, "data": [{'card': '11/0/0',
#                                           'device_ip': '118.70.0.137',
#                                           'device_name': 'HNI-TEST',
#                                           'fpc_slot': '11',
#                                           'log_message': 'Unexpected shutdown of connection' +
#                                           'to datapath-traced',
#                                           'pic_slot': '0',
#                                           'time_stamp': '2018-10-17 12:50:10'},
#                                          {'card': '11/1/0',
#                                           'device_ip': '118.70.0.137',
#                                           'device_name': 'HNI-TEST',
#                                           'fpc_slot': '11',
#                                           'log_message': 'Unexpected shutdown of connection to' +
#                                           'datapath-traced',
#                                           'pic_slot': '1',
#                                           'time_stamp': '2018-10-16 13:50:27'},
#                                          {'card': '11/2/0',
#                                           'device_ip': '118.70.0.137',
#                                           'device_name': 'HNI-TEST',
#                                           'fpc_slot': '11',
#                                           'log_message': 'Unexpected shutdown of connection to' +
#                                           'datapath-traced',
#                                           'pic_slot': '2',
#                                           'time_stamp': '2018-10-16 13:50:27'}]}


LOG_1 = [{'device_name': 'HNI-TEST',
          'device_ip': '118.70.0.137',
          'fpc_slot': '11',
          'pic_slot': '0',
          'card': '11/0/0',
          'status': 'OK',
          'msg_aopt': 'Shutdown by AOPT',
          'reason': 'Da reboot/shutdown >= 2 lan trong 120 phut',
          'time_stamp': '2018-09-23 07:17:02'}
         ]


LOG_2 = [{'device_name': 'HNI-TEST',
          'device_ip': '118.70.0.137',
          'fpc_slot': '11',
          'pic_slot': '0',
          'card': '11/0/0',
          'status': 'OK',
          'msg_aopt': 'Shutdown by AOPT',
          'reason': 'Da reboot/shutdown >= 2 lan trong 120 phut',
          'time_stamp': '2018-09-23 07:17:02'},
         {'device_name': 'HNI-TEST',
          'device_ip': '118.70.0.137',
          'fpc_slot': '11',
          'pic_slot': '1',
          'card': '11/1/0',
          'status': 'OK',
          'msg_aopt': 'Shutdown by AOPT',
          'reason': 'Da reboot/shutdown >= 2 lan trong 120 phut',
          'time_stamp': '2018-09-23 07:17:02'},
         {'device_name': 'HNI-TEST',
          'device_ip': '118.70.0.137',
          'fpc_slot': '11',
          'pic_slot': '2',
          'card': '11/2/0',
          'status': 'OK',
          'msg_aopt': 'Shutdown by AOPT',
          'reason': 'Da reboot/shutdown >= 2 lan trong 120 phut',
          'time_stamp': '2018-09-23 07:17:02'},
         ]


async def uptime_check(n):
    """Test."""
    await asyncio.sleep(12)
    return n


async def shutdown_pic(n):
    """Test."""
    await asyncio.sleep(12)
    return n


async def reboot_pic(n):
    """Test."""
    await asyncio.sleep(12)
    return n


async def picup_traffic_check(n):
    """Test."""
    await asyncio.sleep(12)
    return n


async def traffic_check_by_hour(n):
    """Test."""
    await asyncio.sleep(12)
    return n
syncio.sleep(12)
return n
syncio.sleep(12)
return n
n n
syncio.sleep(12)
return n
io.sleep(12)
return n
syncio.sleep(12)
return n
syncio.sleep(12)
return n
syncio.sleep(12)
return n
syncio.sleep(12)
return n
syncio.sleep(12)
return n
n n
syncio.sleep(12)
return n
n n
syncio.sleep(12)
return n
n n
synio.sleep(12)
return n
