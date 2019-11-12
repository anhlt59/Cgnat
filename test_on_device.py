"""Unittest for Main."""
# !/usr/bin/python
# -*- coding: utf-8 -*-
from unittest.mock import patch, DEFAULT

import config
import main
import config_test


@patch.multiple('main',
                get_kibana=DEFAULT,
                get_opsview=DEFAULT,
                get_card_reboot=DEFAULT,
                uptime_check=DEFAULT,
                history_check=DEFAULT,
                insert_data_to_error_devices=DEFAULT,
                insert_data_to_history=DEFAULT,
                auto_ticket=DEFAULT
                )
def test(get_kibana,
         get_opsview,
         get_card_reboot,
         uptime_check,
         history_check,
         insert_data_to_error_devices,
         insert_data_to_history,
         auto_ticket
         ):
    """Process 1-Test case 1."""
    # get data
    get_kibana.return_value = config_test.KIBANA
    get_opsview.return_value = []
    get_card_reboot.return_value = []
    # uptime_check = True
    uptime_check.return_value = config_test.uptime_check(False)
    insert_data_to_error_devices.return_value = None
    # history check = False
    history_check.return_value = False
    insert_data_to_history.return_value = None
    auto_ticket.return_value = 2222
    # run
    main.main(config)


if __name__ == '__main__':
    test()
