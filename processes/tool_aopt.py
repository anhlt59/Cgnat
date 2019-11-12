# !/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import re
from .API.api_aopt import get_token, run_command, get_command

""" ip_address  :   ip host
    pic_slot    :   pic slot
    fpc_slot    :   fpc slot
    command     :   command run on device
    pattern     :   regex to match output
"""


def tools(f):
    """Decorator for tools."""
    async def wrapper(config='', ip_address='', logger='', ** kwargs):
        # Get token
        token = get_token(config.USERNAME, config.PASSWORD, logger)
        if token is None:
            return

        # Run command
        command, pattern = f(config=config, ip_address=ip_address,
                             logger=logger, **kwargs)
        job_id = run_command(token, ip_address, command, logger)
        if job_id is None:
            return

        # Wait for AOPT
        await asyncio.sleep(12)
        # If Fail, retry get_command max 10 time, delay 3s
        for _ in range(10):
            try:
                output, state = get_command(token, job_id, logger)
                print('output', output, 'state', state)
                if state == 'SUCCESS' and output is not None:
                    break
            except:
                state, output = 'FAIL', None
                return
            await asyncio.sleep(3)
        if state == 'SUCCESS' and output is not None:
            # Check output by regex
            try:
                result = re.search(pattern, output[2], re.M | re.I | re.DOTALL)
                print(True if result else False)
                return True if result else False
            except Exception as err:
                logger.error("Error tool_aopt(): {}".format(str(err)))
        print('Tool thao tac Fail')
        return
    return wrapper


@tools
def reboot_pic(config='', ip_address='', pic_slot='', fpc_slot='', logger=''):
    """Reboot pic, Success if reboot_PIC() return True."""
    command = config.COMMAND_REBOOT.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    pattern = config.PATTERN_REBOOT.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    return command, pattern


@tools
def shutdown_pic(config='', ip_address='', pic_slot='',
                 fpc_slot='', logger=''):
    """Shutdown pic, Success if shutdown_PIC() return True."""
    command = config.COMMAND_SHUTDOWN.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    pattern = config.PATTERN_SHUTDOWN.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    return command, pattern


@tools
def check_online(config='', ip_address='', pic_slot='',
                 fpc_slot='', logger=''):
    """PIC offline if check_online() return True else False."""
    command = config.COMMAND_OFFLINE.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    pattern = config.PATTERN_OFFLINE.replace('{{b}}', pic_slot).\
        replace('{{a}}', fpc_slot)
    return command, pattern
