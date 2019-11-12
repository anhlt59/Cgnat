#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import time
import logging
from threading import Timer


logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
full_dir = os.path.join(base_dir, "jsnap-log")

# Load data in log file
def load_data(filename):
    with open(filename, 'rb') as datafile:
        result = datafile.read()
    datafile.close()
    return result


def create_logdir(full_dir, ip):

    log_dir = os.path.join(full_dir, ip)
    if not os.path.isdir(log_dir):
        try:
            try:
                os.mkdir(full_dir, 0o755)
            except:
                pass
            os.mkdir(log_dir, 0o755)
        except Exception as e:
            logger.debug('UNKNOWN - mkdir:  %s' % e)
            #print('UNKNOWN - mkdir:  %s' % e)
            return None
    return log_dir

def check_error(filename):
    error_log = ''
    total_log = ''
    check_content = False
    file_log = open(filename, 'r')
    for log in file_log:
        if 'CHECKING SECTION' in log:
            check_content = True

        if 'error' in log.lower() or 'fail' in log.lower():
            error_log += '   ' + log.strip() + '\n'

    if error_log != '':
        total_log += error_log + '\n'

    if check_content is False:
        total_log = file_log.read()
    file_log.close()

    return total_log


def compare_jsnap(config, ip_add, device_name, card_name):
    command_jsnap = config.command_jsnap
    pass_config = config.pass_config
    timeout = config.timeout
    RESULT = config.RESULT
    try:
        log_dir = create_logdir(full_dir, ip_add)
        current_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(int(time.time())))
        file_name = "check_" + device_name.lower() + "_card-" + card_name.replace("/", "-") + "_" + current_time + '.log'
        command = 'cd ' + log_dir + command_jsnap + '--check pre,post -t ' + ip_add + pass_config \
                  + "/check_cgnat_status_v1.c &>'" + log_dir + "/" + file_name + "'"
        # print(command)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #proc.communicate()
        timer = Timer(timeout, proc.kill)
        try:
            timer.start()
            proc.communicate()
        finally:
            timer.cancel()

        path = log_dir + "/" + file_name
        error_log = check_error(path)

        if error_log == '':
            msg = 'Run COMPARE Jsnap OK for box: ' + device_name
            RESULT['result'] = True
            RESULT['data'] = msg
            return RESULT
        else:
            msg = 'Run COMPARE Jsnap FAIL for box: ' + device_name
            RESULT['data'] = msg
            return RESULT
    except Exception as e:
        logger.debug(device_name, e)
        msg = 'Run COMPARE Jsnap FAIL for box: ' + device_name
        RESULT['data'] = msg
        return RESULT


def post_jsnap(config, ip_add, device_name, card_name):
    command_jsnap = config.command_jsnap
    pass_config = config.pass_config
    timeout = config.timeout
    RESULT = config.RESULT
    try:
        log_dir = create_logdir(full_dir, ip_add)
        current_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(int(time.time())))
        file_name = "post_" + device_name.lower() + "_card-" + card_name.replace("/", "-") + "_" + current_time + '.log'
        command = 'cd ' + log_dir + command_jsnap + '--snap post -t ' + ip_add + pass_config \
                  + "/check_cgnat_status_v1.c &>'" + log_dir + "/" + file_name + "'"
        # print(command)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #proc.communicate()
        timer = Timer(timeout, proc.kill)
        try:
            timer.start()
            proc.communicate()
        finally:
            timer.cancel()

        path = log_dir + "/" + file_name
        out = load_data(path)
        if b"CONNECTED" in out:
            msg = 'Run POST Jsnap COMPLETE for box: ' + device_name
            RESULT['result'] = True
            RESULT['data'] = msg
            return RESULT
        else:
            msg = 'Run POST Jsnap FAIL for box: ' + device_name
            RESULT['data'] = msg
            return RESULT
    except Exception as e:
        logger.debug(device_name, e)
        msg = 'Run POST JSNAP FAIL for box: ' + device_name
        RESULT['data'] = msg
        return RESULT


def pre_jsnap(config, ip_add, device_name, card_name):
    command_jsnap = config.command_jsnap
    pass_config = config.pass_config
    timeout = config.timeout
    RESULT = config.RESULT
    try:
        log_dir = create_logdir(full_dir, ip_add)
        #print("log_dir",log_dir) 
        current_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(int(time.time())))
        file_name = "pre_" + device_name.lower() + "_card-" + card_name.replace("/", "-") + "_" + current_time + '.log'
        command = 'cd ' + log_dir + command_jsnap + '--snap pre -t ' + ip_add + pass_config \
                  + "/check_cgnat_status_v1.c &>'" + log_dir + "/" + file_name + "'"
        #print(command)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #proc.communicate()
        timer = Timer(timeout, proc.kill)
        try:
            timer.start()
            proc.communicate()
        finally:
            timer.cancel()

        path = log_dir + "/" + file_name
        out = load_data(path)
        if b"CONNECTED" in out:
            msg = 'Run PRE Jsnap COMPLETE for box: ' + device_name
            RESULT['result'] = True
            RESULT['data'] = msg
            return RESULT
        else:
            msg = 'Run PRE Jsnap FAIL for box: ' + device_name
            RESULT['data'] = msg
            return RESULT
    except Exception as e:
        logger.debug(device_name, e)
        #print(device_name, e)
        msg = 'Run PRE Jsnap FAIL for box: ' + device_name
        RESULT['data'] = msg
        return RESULT
