#coding=utf-8

import requests


def run(target):
    "Phpmyadmin"
    results = []
    paths = [
        "/phpmyadmin/",
        "/phpMyAdmin/"
        "/myadmin/",
    ]

    for path in paths:
        url = "http://" + target + path
        try:
            r = requests.get(url, timeout=5)
        except Exception:
            pass
        else:
            r.close()
            if r.status_code == 200 and "<title>phpMyAdmin" in r.text:
                results.append(url)
                break

    return results
