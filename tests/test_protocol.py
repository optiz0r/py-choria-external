import unittest

from choria_external.exceptions import InvalidRPCData
from choria_external.protocol import ProtocolMessage


class TestProtocolMessage(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_valid_protocol(self):
        ProtocolMessage._protocols['foo'] = 'protocol object'
        self.assertEqual('protocol object', ProtocolMessage.get_protocol('foo'))

    def test_get_invalid_protocol(self):
        with self.assertRaises(InvalidRPCData) as cm:
            ProtocolMessage.get_protocol('improper_protocol')

        exc = cm.exception
        self.assertEqual('Unsupported message protocol improper_protocol', exc.args[0])

    def test_create_reply_for_base_class(self):
        with self.assertRaises(InvalidRPCData) as cm:
            ProtocolMessage.create_reply()

        exc = cm.exception
        self.assertEqual('Method should only be called for a ProtocolMessage subclass', exc.args[0])

    def test_register_protocol(self):
        protocol_name = 'choria:mcorpc:test:1'
        self.assertNotIn(protocol_name, ProtocolMessage._protocols)

        class TestProtocol(ProtocolMessage):
            _protocol = protocol_name

        ProtocolMessage.register_protocol()(TestProtocol)

        self.assertIn(protocol_name, ProtocolMessage._protocols)
