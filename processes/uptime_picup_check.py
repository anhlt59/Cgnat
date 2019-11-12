#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import re
from .API.api_aopt import get_token, run_command, get_command
from datetime import datetime


async def uptime_check(config, ip_address, pic_slot, fpc_slot, logger):
    """
    Get device's time interval via AOPT's API
    If device's time interval >= 15 minutes:
        return True else False
    """
    get_uptime_command = config.UPTIME_COMMAND.replace(
        '{{b}}', pic_slot).replace('{{a}}', fpc_slot)
    # Get token
    token = get_token(config.USERNAME, config.PASSWORD, logger)
    if token is None:
        return False
    # Run command
    job_id = run_command(token, ip_address, get_uptime_command, logger)
    if job_id is None:
        return False
    # Wait for AOPT
    await asyncio.sleep(12)
    # If Fail, retry get_command max 10 time, delay 3s
    for _ in range(10):
        try:
            output, state = get_command(token, job_id, logger)
            # Check result
            if state == 'SUCCESS' and output is not None:
                break
        except:
            state, output = 'FAIL', None
        await asyncio.sleep(3)

    if state == 'SUCCESS' and output is not None:
        uptimeRegex = re.compile(r'{"junos:seconds" : "(\d+)"}')
        try:
            match_uptime = uptimeRegex.search(output[2])
            uptime = match_uptime.group(1)
            # Return True if device's time interval >= 15 minutes else False
            return int(uptime) > 15 * 60
        except Exception as err:
            logger.error(
                "Error uptime_picup_check in uptime_check(): {}".format(str(err)))
    return False


async def picup_traffic_check(config, ip_address, pic_slot, fpc_slot, logger):
    """
    Get device's time status and traffic via AOPT's API
    Return True if physical device is up, input output rate > 15Mbps and
    (input and output) deviation not exceeding 10%
    """
    get_traffic_command = config.TRAFFIC_COMMAND.replace(
        '{{b}}', pic_slot).replace('{{a}}', fpc_slot)

    token = get_token(config.USERNAME, config.PASSWORD, logger)
    if token is None:
        return False

    job_id = run_command(token, ip_address, get_traffic_command, logger)
    if job_id is None:
        return False

    await asyncio.sleep(12)

    for _ in range(10):
        try:
            output, state = get_command(token, job_id, logger)
            print(output, state)
            # Check result
            if state == 'SUCCESS' and output is not None:
                break
        except:
            state, output = 'FAIL', None
            return
        await asyncio.sleep(3)

    if state == 'SUCCESS' and output is not None:
        # print(output)
        ioRegex = re.compile(
            r"Input rate\s*:\s*(\d+)(.|\r\n)*Output rate\s*:\s*(\d+)")
        try:
            match_ioRegex = ioRegex.search(output[2])
            inputRate = match_ioRegex.group(1)
            outputRate = match_ioRegex.group(3)
            return int(inputRate) >= 150 * 10 ^ 6 and int(outputRate) >= 150 * 10 ^ 6 and (abs(int(inputRate) - int(outputRate)) / max(int(inputRate), int(outputRate))) <= 0.1
        except Exception as err:
            logger.error(
                "Error uptime_picup_check in picup_traffic_check(): {}".format(str(err)))
    return False


async def traffic_check_by_hour(config, ip_address, pic_slot, fpc_slot, logger):
    """Traffic check between 00:00:00 to 06:00:00
    If sastisfying conditions: return True then handle this device error
    Else: return Fasle then does not handle this device error
    Outside hours: return True, too
    """
    hour_now = datetime.now().hour
    if hour_now > 6 or hour_now <= 0:
        get_traffic_command = config.TRAFFIC_COMMAND.replace(
            '{{b}}', pic_slot).replace('{{a}}', fpc_slot)

        token = get_token(config.USERNAME, config.PASSWORD, logger)
        if token is None:
            return False

        job_id = run_command(token, ip_address, get_traffic_command, logger)
        if job_id is None:
            return False

        await asyncio.sleep(12)

        for _ in range(10):
            try:
                output, state = get_command(token, job_id, logger)
                # Check result
                if state == 'SUCCESS' and output is not None:
                    break
            except:
                state, output = 'FAIL', None
            await asyncio.sleep(3)

        if state == 'SUCCESS' and output is not None:
            ioRegex = re.compile(
                r"Input rate\s*:\s*(\d+)(.|\r\n)*Output rate\s*:\s*(\d+)")
            try:
                match_ioRegex = ioRegex.search(output[2])
                inputRate = match_ioRegex.group(1)
                outputRate = match_ioRegex.group(3)
                if int(inputRate) < 50 * 10**6 or int(outputRate) < 50 * 10**6:
                    return True
                else:
                    return False
            except Exception as err:
                logger.error(
                    "Error uptime_picup_check in traffic_check_by_hour(): {}".format(str(err)))
                return False
    else:
        return True
