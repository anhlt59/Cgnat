"""Unittest for Main."""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from unittest.mock import patch, DEFAULT

import config
import main
import config_test


@patch.multiple('main',
                # get_kibana=DEFAULT,
                # get_opsview=DEFAULT,
                # get_card_reboot=DEFAULT,
                # picup_traffic_check=DEFAULT,
                # post_jsnap=DEFAULT,
                # compare_jsnap=DEFAULT,
                auto_ticket=DEFAULT,
                # insert_data_to_history=DEFAULT,
                # shutdown_pic=DEFAULT,
                # uptime_check=DEFAULT,
                # traffic_check_by_hour=DEFAULT,
                # history_check=DEFAULT,
                # insert_data_to_error_devices=DEFAULT,
                # pre_jsnap=DEFAULT,
                # reboot_pic=DEFAULT
                )
def test(
    # get_kibana,
    # get_opsview,
    # get_card_reboot,
    # picup_traffic_check,
    # post_jsnap,
    # compare_jsnap,
    auto_ticket,
    # traffic_check_by_hour,
    # insert_data_to_history,
    # shutdown_pic,
    # uptime_check,
    # history_check,
    # insert_data_to_error_devices,
    # pre_jsnap,
    # reboot_pic
):
    """Process 1+2-Test case 1."""
    # get data
    # get_kibana.return_value = config_test.KIBANA
    # get_opsview.return_value = []
    # get_card_reboot.return_value = [{'log_message': 'SPD_CONN_OPEN_FAILURE', 'card': '11/0/0', 'device_name': 'HNI-MX960-LAB',
    #                                  'fpc_slot': '11', 'device_ip': '118.70.0.137', 'time_stamp': '2018-12-26 8:50:00', 'pic_slot': '0'}]
    # traffic_check_by_hour.return_value = config_test.traffic_check_by_hour(
    #     True)
    # uptime_check.return_value = config_test.uptime_check(True)

    # insert_data_to_error_devices.return_value = None
    # # history check = Falsel
    # history_check.return_value = False
    # # pre jsnap = False
    # pre_jsnap.return_value = {'result': True}
    # # shutdown pic = True
    # shutdown_pic.return_value = config_test.shutdown_pic(True)
    # # reboot pic = True
    # reboot_pic.return_value = config_test.reboot_pic(True)
    # insert_data_to_history.return_value = None
    auto_ticket.return_value = 2222
    # # picup_traffic_check = True
    # picup_traffic_check.return_value = config_test.picup_traffic_check(True)
    # # post_jsnap = True
    # post_jsnap.return_value = {'result': True}
    # # compare_jsnap = True
    # compare_jsnap.return_value = {'result': True}
    # run
    main.main(config)


if __name__ == '__main__':
    test()
