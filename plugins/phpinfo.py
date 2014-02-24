#coding=utf-8

import requests


def run(target):
    file_list = [
        "1.php",
        "test.php",
        "ceshi.php",
        "info.php",
        "phpinfo.php",
        "php_info.php",
        "php.php"
    ]
    results = []

    for f in file_list:
        url = "http://" + target + "/" + f

        try:
            r = requests.get(url, timeout=5)
        except Exception:
            pass
        else:
            r.close()
            if r.status_code == 200 and "<title>phpinfo()</title>" in r.text:
                results.append(url)
                break

    return results
