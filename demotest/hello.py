# -*- coding: utf-8 -*-
'''
示例测试用例
'''

import threading

from testbase.testcase import TestCase
from demolib.hellolib import HelloChannel, HelloService, HelloRequest
from demolib.helloserver import HelloServer


class HelloTestBase(TestCase):
    '''HelloTest基类
    '''

    def add_cleanup(self, callee, *args, **kwargs):
        self.clean_ups.append((callee, args, kwargs))

    def pre_test(self):
        self.clean_ups = []
        self.server = HelloServer()
        threading.Thread(target=self.server.serve_forever).start()

    def post_test(self):
        for clean_up in self.clean_ups:
            try:
                callee, args, kwargs = clean_up
                callee(*args, **kwargs)
            except:
                self.log_info("invoke %s with %s and %s failed" % (callee, str(args), str(kwargs)))

    def clean_test(self):
        super(HelloTestBase, self).clean_test()
        self.server.shutdown()


class HelloTest(HelloTestBase):
    '''示例测试用例，使用服务方式
    '''
    timeout = 5
    owner = 'foo'
    priority = HelloTestBase.EnumPriority.High
    status = HelloTestBase.EnumStatus.Ready

    def run_test(self):

        # --------------------------------------
        self.start_step('构造一个服务')
        host, port = self.server.server_address
        chan = HelloChannel(host=host, port=port)
        self.add_cleanup(chan.close)
        svc = HelloService(chan)

        # --------------------------------------
        self.start_step('调用服务接口并获取结果')
        req = HelloRequest()
        req.username = "foo"
        rsp = svc.hello(req)

        # --------------------------------------
        self.start_step('检查回包')
        self.assert_equal('检查回包是否正确', rsp.result, "Hello, %s!" % req.username)


class HelloTest2(HelloTestBase):
    '''示例测试用例，使用信道直接发送方式
    '''
    timeout = 5
    owner = 'foo'
    priority = HelloTestBase.EnumPriority.High
    status = HelloTestBase.EnumStatus.Ready

    def run_test(self):
        # --------------------------------------
        self.start_step('构造一个通道')
        host, port = self.server.server_address
        chan = HelloChannel(host=host, port=port)
        self.add_cleanup(chan.close)

        # --------------------------------------
        self.start_step('发送请求并获取回包')
        req = HelloRequest()
        req.username = "foo"
        rsp = chan.send(req)

        # --------------------------------------
        self.start_step('发送请求并检查回包')
        self.log_info("回包内容为: %s" % rsp)
        self.assert_equal('检查回包是否正确', rsp.result, "Hello, %s!" % req.username)


if __name__ == '__main__':
    HelloTest().debug_run()
#     HelloTest2().debug_run()
