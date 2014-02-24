#coding=utf-8

import requests


def run(target):
    "Discuz Config Backup"
    results = []
    bak_file_list = [
        "/config/config_global.php.bak",
        "/config/config_ucenter.php.bak"
    ]

    for bak_file in bak_file_list:
        url = "http://" + target + bak_file
        try:
            r = requests.get(url, timeout=5)
        except Exception:
            pass
        else:
            r.close()
            if r.status_code == 200 and bak_file in url and "<?php" in r.text:
                results.append(url)

    return results