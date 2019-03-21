# -*- coding: utf-8 -*-
'''
示例lib层
'''

from qt4s.channel.sock import SocketChannel, RequestBase, ResponseBase
from qt4s.message.definition import Field, String, Uint32
from qt4s.message.serializers.binary import BinarySerializer
from qt4s.service import Service, Method


class HelloResponse(ResponseBase):
    """hello response definition
    """
    _struct_ = [
        Field('len', Uint32),
        Field('seq', Uint32),
        Field('result', String, byte_size=0)
    ]
    _serializer_ = BinarySerializer()
    _length_field_ = "len"

    def get_sequence_id(self):
        return self.seq


class HelloRequest(RequestBase):
    """hello request definition
    """
    _struct_ = [
        Field('len', Uint32),
        Field('seq', Uint32),
        Field('username', String, byte_size=0)
    ]
    _serializer_ = BinarySerializer()
    _length_field_ = "len"
    response_class = HelloResponse

    def get_sequence_id(self):
        return self.seq

    def pre_process(self, chan):
        self.seq = chan.create_seq()


class HelloChannel(SocketChannel):
    '''hello channel
    '''
    request_class = HelloRequest

    def call_method(self, methodname, req, rsp_cls, timeout):
        if methodname == "hello":
            response = self.send(req)
            return response


class HelloService(Service):
    '''示例服务
    '''
    _methods_ = [
         Method("hello", HelloRequest, HelloResponse)
    ]


if __name__ == '__main__':
    pass
