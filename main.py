# !/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from os import remove
import logging
from datetime import datetime

import config
from processes.get_kibana_log import get_kibana
from processes.get_opsview_log import get_opsview
from processes.tool_aopt import reboot_pic, shutdown_pic, check_online
from processes.database import insert_data_to_history, insert_data_to_error_devices
from processes.history_check import history_check, get_card_reboot, shutdown_check
from processes.uptime_picup_check import uptime_check, picup_traffic_check, traffic_check_by_hour
from processes.run_jsnap import pre_jsnap, post_jsnap, compare_jsnap
from processes.auto_ticket import auto_ticket


def main(config):
    """Main process."""
    # Setup Log
    logger = logging_setup(config)
    # log kibana
    print('# B1-2-3: Get data from kibana and opsview')
    log_kibana = get_kibana(config.KibanaConfig, logger)
    # log opsview
    log_opsview = get_opsview(config.OpsviewConfig)
    # Total log
    log_1 = log_kibana['data'] + log_opsview['data']
    print(log_1)

    # Get cards reboot after 10'
    print("# B11: Get card reboot after 10'")
    log_2 = get_card_reboot(config, logger)
    print(log_2)

    # Add tasks
    tasks = [process_1(i, config, logger) for i in log_1] +\
            [process_2(i, config, logger) for i in log_2]

    if len(tasks) > 0:
        # Create event loop
        loop = asyncio.get_event_loop()
        # Run event loop
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

    # If file_log null remove file_log
    with open(config.LOG_PATH, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            remove(config.LOG_PATH)
    print('End.')


def logging_setup(config):
    """Logging setup."""
    config_log = {'filename': config.LOG_PATH,
                  'level': logging.ERROR,
                  'format': "%(levelname)s %(asctime)s - %(message)s",
                  'filemode': 'a'}
    logging.basicConfig(**config_log)
    return logging.getLogger()


async def process_1(pic, config, logger):
    """Process 1."""
    print('Running process 1...')
    if 'below the bandwidth threshold' in pic['log_message']:
        print('# B3.2: check traffic in 0h-6h')
        check_time_0_6 = await traffic_check_by_hour(
            config.AoptConfig,
            pic['device_ip'], pic['pic_slot'], pic['fpc_slot'], logger)

        print(check_time_0_6)
        if check_time_0_6 is False:
            print('End process 1')
            return
    print('# B4: check uptime')

    uptime = await uptime_check(
        config.AoptConfig,
        pic['device_ip'], pic['pic_slot'], pic['fpc_slot'], logger)

    print(uptime)
    # uptime == True => pic co uptime > 15'
    if uptime is True:
        print('B4: Store date in error_devices database')

        insert_data_to_error_devices(
            config, pic['device_name'], pic['device_ip'],
            pic['fpc_slot'], pic['pic_slot'], pic['card'],
            pic['log_message'], pic['time_stamp'], logger)

        print('# B5: check history')

        history = history_check(
            config, pic['device_name'], pic['card'], pic['time_stamp'], logger)

        print(history)
        # Check result history_check
        if history is None:
            return
        elif history is False:
            print('# B8: chay Pre JSNAP')

            result = pre_jsnap(
                config,
                pic['device_ip'], pic['device_name'], pic['card'])['result']

            print(result)
            # Check result pre jsnap
            if result is True:
                # B9: reboot PIC
                print('# B9: reboot PIC')

                result = await reboot_pic(config=config.AoptConfig,
                                          ip_address=pic['device_ip'],
                                          pic_slot=pic['pic_slot'],
                                          fpc_slot=pic['fpc_slot'],
                                          logger=logger)

                print(result)
                status = "Reboot"
                time_stamp = datetime.strftime(datetime.now(),
                                               "%Y-%m-%d %H:%M:%S")
                msg_aopt = "Rebooted by AOPT"
                reason = pic['log_message']
        else:
            print('# B6: shutdown PIC')
            print('# check card on or off')
            state = await check_online(config=config.AoptConfig,
                                       ip_address=pic['device_ip'],
                                       pic_slot=pic['pic_slot'],
                                       fpc_slot=pic['fpc_slot'],
                                       logger=logger)
            print(state)
            if state is False:
                return
            elif state is None:
                print('# B14: Tao SC cho NOC')
                auto_ticket(config.AutoTicket, logger)
                return
            result = await shutdown_pic(config=config.AoptConfig,
                                        ip_address=pic['device_ip'],
                                        pic_slot=pic['pic_slot'],
                                        fpc_slot=pic['fpc_slot'],
                                        logger=logger)

            print(result)
            status = "Shutdown"
            time_stamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            msg_aopt = "Shutdown by AOPT"
            reason = "Da reboot/shutdown >= 2 lan trong 120 phut"
        # Check result shutdown/reboot pic
        if result is True:
            print('# B7 B10: luu history thong tin shudown/reboot pic')

            insert_data_to_history(
                config, pic['device_name'], pic['device_ip'],
                pic['fpc_slot'], pic['pic_slot'], pic['card'],
                status, msg_aopt, reason, time_stamp, logger)

        else:
            print('# B14: Tao SC cho NOC')
            auto_ticket(config.AutoTicket, logger)
    print('End process 1')


async def process_2(pic, config, logger):
    """Process 2."""
    print('Running process 2...')
    print('# check card on or off')
    state = await check_online(config=config.AoptConfig,
                               ip_address=pic['device_ip'],
                               pic_slot=pic['pic_slot'],
                               fpc_slot=pic['fpc_slot'],
                               logger=logger)
    print(state)
    if state is False:
        return
    elif state is None:
        print('# B14: Tao SC cho NOC')
        auto_ticket(config.AutoTicket, logger)
        return
    print('# B11: Check PIC up va traffic')
    result = await picup_traffic_check(
        config.AoptConfig, pic['device_ip'], pic['pic_slot'],
        pic['fpc_slot'], logger)

    print(result)
    if result is True:
        print('# B12: Run POST JSNAP')

        result = post_jsnap(
            config, pic['device_ip'], pic['device_name'],
            pic['card'])['result']

        print(result)
        if result is True:
            print('# B13: Run COMPARE JSNAP')

            result = compare_jsnap(config, pic['device_ip'],
                                   pic['device_name'],
                                   pic['card'])['result']

            print(result)
        if result is False:
            print('# B14: Tao SC cho NOC')
            auto_ticket(config.AutoTicket, logger)

    elif result is None:
        print('# B14: Tao SC cho NOC')
        auto_ticket(config.AutoTicket, logger)

    elif result is False:
        print('# B6: shutdown PIC')

        result = await shutdown_pic(config=config.AoptConfig,
                                    ip_address=pic['device_ip'],
                                    pic_slot=pic['pic_slot'],
                                    fpc_slot=pic['fpc_slot'],
                                    logger=logger)

        if result is True:
            status = "Shutdown"
            time_stamp = datetime.strftime(
                datetime.now(), "%Y-%m-%d %H:%M:%S")
            msg_aopt = "Shutdown by AOPT"
            reason = "Da reboot/shutdown >= 2 lan trong 120 phut"
            print('# B7: luu history thong tin shudown pic')

            insert_data_to_history(
                config, pic['device_name'],
                pic['device_ip'], pic['fpc_slot'],
                pic['pic_slot'], pic['card'], status,
                msg_aopt, reason, time_stamp, logger)

        else:
            print('# B14: Tao SC cho NOC')
            auto_ticket(config.AutoTicket, logger)
    print('End process 2')


if __name__ == '__main__':
    main(config)
    # logger = logging_setup(config)
    # config.KibanaConfig.QUERY_TIME = 60 * 60 * 24 * 30
    # print(get_kibana(config.KibanaConfig, logger))
    # task_1 = check_online(config.AoptConfig,
    #                       ip_address='118.70.0.137',
    #                       pic_slot='0',
    #                       fpc_slot='11',
    #                       logger=logger)
    # # task_1 = picup_traffic_check(
    # #         config.AoptConfig, pic['device_ip'], pic['pic_slot'],
    # #         pic['fpc_slot'], logger)
    # # task_2 = shutdown_pic(config.AoptConfig,
    # #                       ip_address='118.70.0.137',
    # #                       pic_slot='0',
    # #                       fpc_slot='11',
    # #                       logger=logger)

    # tasks = [task_1]

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(*tasks))
    # loop.close()
