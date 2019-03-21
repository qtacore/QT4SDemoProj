# -*- coding: utf-8 -*-
'''http demo testcase
'''

from testbase.testcase import TestCase
from qt4s.channel.http import HttpChannel


class HttpDemoTest(TestCase):
    '''http demo testcase
    '''
    timeout = 5
    owner = 'foo'
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        self.start_step('构造一个通道')
        chan = HttpChannel(host="www.qq.com")

        self.start_step('发送请求并获取回包')
        rsp = chan.get("/")

        self.start_step('检查回包内容')
        self.assert_("返回码错误", rsp.status_code == 200)
        self.assert_("reason错误", rsp.reason == "OK")


if __name__ == "__main__":
    HttpDemoTest().debug_run()
