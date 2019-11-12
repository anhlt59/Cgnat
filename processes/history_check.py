# !/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from .database import connect_db


def history_check(config, device_name, card, time_stamp, logger):
    """
    Get data from the history table to check the number of device's
    reboot/shutdown in the time interval 120 minutes from the error
    warning occured
    Return True if number of reboot/shutdown >= 2 else False
    """
    back_to_120_minutes = datetime.strptime(
        time_stamp, "%Y-%m-%d %H:%M:%S") - timedelta(hours=2)
    time_string_back_to_120_minutes = datetime.strftime(
        back_to_120_minutes, "%Y-%m-%d %H:%M:%S")
    try:
        conn = connect_db(config, logger)
        cur = conn.cursor()
        cur.execute(
            "SELECT * from history WHERE device_name=%s and card=%s and time_stamp > %s", (device_name, card, time_string_back_to_120_minutes))
        return len(cur.fetchall()) >= 2
    except Exception as err:
        logger.error(
            "Error history_check in history_check(): {}".format(str(err)))


def get_card_reboot(config, logger):
    """Get card reboot after 10'."""
    log = []

    time_back_to_8_minutes = datetime.strftime(
        datetime.now() - timedelta(minutes=8), "%Y-%m-%d %H:%M:%S")
    time_back_to_12_minutes = datetime.strftime(
        datetime.now() - timedelta(minutes=12), "%Y-%m-%d %H:%M:%S")
    try:
        conn = connect_db(config, logger)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM history WHERE status=%s and time_stamp < %s and time_stamp > %s",
            ('Reboot', time_back_to_8_minutes, time_back_to_12_minutes)
        )
        devices_up = cur.fetchall()

        for device in devices_up:
            device_pic_up = {}
            device_pic_up['device_name'] = device[1]
            device_pic_up['device_ip'] = device[2]
            device_pic_up['fpc_slot'] = device[3]
            device_pic_up['pic_slot'] = device[4]
            device_pic_up['card'] = device[5]
            device_pic_up['status'] = device[6]
            device_pic_up['msg_aopt'] = device[7]
            device_pic_up['reason'] = device[8]
            device_pic_up['time_stamp'] = device[9]
            log.append(device_pic_up)
        return log
    except Exception as err:
        logger.error(
            "Error history_check in get_card_reboot(): {}".format(str(err)))
        return []


def shutdown_check(config, device_name, card, logger):
    """Get card reboot after 10'."""
    time_back_to_8_minutes = datetime.strftime(
        datetime.now() - timedelta(minutes=0), "%Y-%m-%d %H:%M:%S")
    time_back_to_12_minutes = datetime.strftime(
        datetime.now() - timedelta(minutes=12), "%Y-%m-%d %H:%M:%S")
    try:
        conn = connect_db(config, logger)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM history WHERE device_name=%s and card=%s and time_stamp < %s and time_stamp > %s ORDER BY time_stamp DESC LIMIT 1",
            (device_name, card, time_back_to_8_minutes, time_back_to_12_minutes)
        )
        status = cur.fetchall()[0][6]
        print(status)
        return status == "Shutdown"

        # return len(cur.fetchall()) >= 1

    except Exception as err:
        logger.error(
            "Error history_check in shutdown_check(): {}".format(str(err)))
        return True
