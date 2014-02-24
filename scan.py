#!/usr/bin/python
#coding=utf-8

"""Total Scan

Usage:
    scan.py plugins
    scan.py info <plugin>
    scan.py scan -n <thread_num> -t <target> -p <plugin>...
    scan.py scan -n <thread_num> -f <file> -p <plugin>...

Options:
    -h --help       Show help
    -v --version    Show version
"""

import os
import threading
from ConfigParser import ConfigParser
from docopt import docopt


class MyThread(threading.Thread):
    "多线程"
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class TotalScan(object):
    "核心类"
    def __init__(self):
        self.plugins = {}

        self.plugin_confs = self.get_plugins_conf()                     # 获取插件列表
        self.import_plugins()                                           # 导入所有插件

    def get_plugins_conf(self):
        "获取插件列表"
        confs = []
        conf_file = [f for f in os.listdir("plugins") if f.endswith(".conf")]
        cp = ConfigParser()

        for f in conf_file:
            cp.read("plugins/%s" % f)
            conf = {}
            for i in cp.items("Documentation"):
                conf[i[0]] = i[1]
            for i in cp.items("Core"):
                conf[i[0]] = i[1]
            confs.append(conf)

        return confs

    def import_plugins(self):
        "导入所有插件至self.plugins"
        for plugin_conf in self.plugin_confs:
            exec "from plugins import %s" % plugin_conf["module"].split(".")[0]
            exec 'self.plugins[\"%s\"]=%s' % (plugin_conf["name"], plugin_conf["module"].split(".")[0])

    def list_plugins(self):
        "显示所有插件"
        print "-" * 80
        print "| %-20s| %s" % ("Plugin", "Description")
        print "-" * 80
        for plugin in self.plugin_confs:
            print "| %-20s| %s" % (plugin["name"], plugin["description"])
            print "-" * 80

    def info_plugin(self, plugin):
        """
        显示单个插件详细信息
        @plugin, str: 插件名
        """
        print "-" * 80
        for p in self.plugin_confs:
            if p["name"] == plugin:
                print "Name: %s" % p["name"]
                print "Description: %s" % p["description"]
                print "Author: %s" % p["author"]
                print "Version: %s" % p["version"]
                print "Website: %s" % p["website"]
                print "License: %s" % p["license"]
                print "Module: %s" % p["module"]
        print "-" * 80

    def exec_plugin_single_thread(self, plugin, target):
        """
        单线程执行插件
        @plugin, str: 插件名，通过self.plugins[plugin]引用插件
        @target, str: 目标网站域名
        """
        results = self.plugins[plugin].run(target)

        if len(results):
            if self.lock.acquire():
                for result in results:
                    self.results[plugin].append(result)
                    print "%s: %s" % (plugin, result)
                    self.lock.release()

    def exec_plugin_threads(self, plugin, targets, thread_num):
        """
        多线程运行单个插件
        @plugin, str: 插件名
        @targets, list: 目标域名列表
        @thread_num, int: 线程数
        """
        threads = []

        for target in targets:
            threads.append(MyThread(self.exec_plugin_single_thread, (plugin, target)))
        while len(threads) > thread_num:
            for i in range(thread_num):
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
            for i in range(thread_num):
                threads.remove(threads[0])
        else:
            for i in threads:
                i.start()
            for i in threads:
                i.join()

    def exec_plugins(self, plugins, targets, thread_num):
        """
        批量运行插件
        @plugins, list: 要运行的插件列表，『all』表示所有插件
        @targets, list: 目标域名列表
        """
        self.results = {}
        self.lock = threading.Lock()

        if plugins == ["all"]:
            plugins = [plugin for plugin in self.plugins]
        for plugin in plugins:
            print "Loading Plugin <%s>..." % plugin
            if not plugin in self.results:
                self.results[plugin] = []
            self.exec_plugin_threads(plugin, targets, thread_num)

    def report(self):
        "输出结果"
        print "\n\n\n"
        print  "-" * 35 + "=" + " Report " + "=" + "-" * 35
        f = open("report.txt", "w")
        split = "+" + "-" * 79
        print split
        f.write(split + "\n")
        for plugin in self.results:
            print "| %-18s| %d" % (plugin, len(self.results[plugin]))
            print split
            f.write("| %-18s| %d" % (plugin, len(self.results[plugin])))
            f.write("\n" + split + "\n")
            for id, vul in zip(range(len(self.results[plugin])), self.results[plugin]):
                print "| %d. %s" % (id+1, vul)
                print split
                f.write("| %d. %s\n" % (id+1, vul))
                f.write(split + "\n")
        f.close()


def main():
    args = docopt(__doc__, version="2014/01/30")
    ts = TotalScan()

    if args["plugins"]:
        ts.list_plugins()
    elif args["info"]:
        plugin = args["<plugin>"][0]
        ts.info_plugin(plugin)
    elif args["scan"]:
        thread_num = int(args["<thread_num>"])
        if args["-t"]:
            targets = []
            targets.append(args["<target>"])
        elif args["-f"]:
            targets = [target.strip() for target in open(args["<file>"]) if not target.isspace()]
        plugins = args["<plugin>"]
        ts.exec_plugins(plugins, targets, thread_num)
        ts.report()

if __name__ == "__main__":
    main()
