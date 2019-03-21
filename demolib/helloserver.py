# -*- coding: utf-8 -*-
'''server
'''

import socket
import select
import struct
import traceback

from SocketServer import TCPServer, ThreadingTCPServer, StreamRequestHandler
from qt4s.message.definition import String, Uint32, Field
from qt4s.message.serializers.binary import BinarySerializer
from qt4s.channel.sock import RequestBase, ResponseBase


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


class HelloRequestHandler(StreamRequestHandler):
    '''定义连接内部的处理过程
    '''

    def handle(self):
        recvbuf = ""
        buflen = 0
        try:
            while(1):
                fd_read, _, _ = select.select([self.connection, ], [], [], 1)
                if self.connection in fd_read:
                    buf = self.connection.recv(1000)
                    if not buf:
                        break
                    recvbuf += buf
                    buflen = len(recvbuf)
                    if buflen >= 4:
                        reqlen = struct.unpack("!I", recvbuf[0:4])[0]
                        if buflen >= reqlen:
                            body = recvbuf[:reqlen]
                            recvbuf = recvbuf[reqlen:]
                            req = HelloRequest()
                            req.loads(body)
                            self.on_request(req)
                            # print "receive from %s@%s: %s" % (self.client_address[0],self.client_address[1],recvbuf)
        except socket.error, e:
            if e.errno == 10054:
                self.connection.close()
        except:
            print ("%s" % traceback.format_exc())
        # print "End handling with client %s:%s" % (self.client_address[0],self.client_address[1])

    def on_request(self, req):
        rsp = HelloResponse()
        rsp.result = "Hello, %s!" % req.username
        rsp.seq = req.seq
        rsp.len = 8 + len(rsp.result)
        rspbuf = rsp.dumps(BinarySerializer())
        sent_size = 0
        while sent_size < rsp.len:
            sent_size += self.connection.send(rspbuf[sent_size:])


class HelloServer(ThreadingTCPServer):
    '''HelloServer implement
    '''

    def __init__(self):
        server_address = ('localhost', 0)
        TCPServer.__init__(self, server_address, HelloRequestHandler)


if __name__ == "__main__":
    server = HelloServer()
    server.serve_forever(1)

