#coding=utf-8

import requests


def run(target):
    "检测svn、git 信息泄露"
    results = []
    dirs = [
        "/.svn/",
        "/.git/"
    ]

    for d in dirs:
        url = "http://" + target + d
        try:
            r = requests.get(url, timeout=5)
        except Exception:
            pass
        else:
            r.close()
            if (r.status_code == 200 or r.status_code == 403) and d in r.url:
                results.append(url)

    return results
