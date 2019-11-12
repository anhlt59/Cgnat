#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb


def connect_db(config, logger):
    """
    Initialize the connection to the database
    username: pic_cgnat database's username
    password: pic_cgnat database's password
    Return: Connection object
    """
    conn = None
    try:
        # read connection parameters
        params = config.config()
        # connect to the MySQL server
        # print('Connecting to the MySQL database...')
        conn = MySQLdb.connect(**params)
    except Exception as err:
        logger.error("Error database in connect_db(): {}".format(str(err)))
    return conn


def insert_data_to_error_devices(config, device_name, device_ip, fpc_slot,
                                 pic_slot, card, log_message,
                                 time_stamp, logger):
    """
    Insert data into table named error_devices
    device_name: name of device
    device_ip: ip of device
    fpc_slot & pic_slot: fpt slot number & pic slot number
    card: name of error card
    log_message: error message from error card on device
    time_stamp: time of error warning
    Return: None
    """
    conn = connect_db(config, logger)
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO error_devices(id, device_name, device_ip,
                                               fpc_slot, pic_slot, card,
                                               log_message, time_stamp)
                    VALUES(NULL, % s, % s, % s, % s,
                           % s, % s, % s)''', (device_name,
                                               device_ip, fpc_slot, pic_slot,
                                               card, log_message, time_stamp))
        conn.commit()
        print('success')
    except Exception as err:
        logger.error(
            "Error database in insert_data_to_error_devices(): {}".format(str(err)))
    cur.close()
    conn.close()


def insert_data_to_history(config, device_name, device_ip, fpc_slot, pic_slot,
                           card, status, msg_aopt, reason, time_stamp, logger):
    """
    Insert data into table named history
    device_name: name of device
    device_ip: ip of device
    fpc_slot & pic_slot: fpt slot number & pic slot number
    card: name of error card
    status: either 'reboot' or 'shutdown'
    msg_aopt: report AOPT's execute result
    reason: "Đã reboot/shutdown >=2 lần trong 120 phút"
    time_stamp: reboot/shutdown time
    Return None
    """
    conn = connect_db(config, logger)
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO history(id, device_name, device_ip,
                                         fpc_slot, pic_slot, card,
                                         status, msg_aopt, reason, time_stamp)
                    VALUES(NULL, % s, % s, % s, % s, % s,
                           % s, % s, % s, % s)''', (device_name,
                                                    device_ip, fpc_slot, pic_slot, card,
                                                    status, msg_aopt, reason, time_stamp))
        conn.commit()
    except Exception as err:
        logger.error(
            "Error database in insert_data_to_history(): {}".format(str(err)))
    cur.close()
    conn.close()
