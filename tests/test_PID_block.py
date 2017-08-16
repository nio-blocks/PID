from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import MagicMock, ANY
from PID_block import PID


class TestPID(NIOBlockTestCase):

    def test_hardcoded(self):
        blk = PID()
        self.configure_block(blk, {'process_config' :
                                        {'set_point' : 10, 'current_value' : 5},
                                   'gain_config' :
                                        {'Kp' : 1, 'Ki' : 0, 'Kd' : 0}})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            {'value' : 5},
            self.last_notified[DEFAULT_TERMINAL][0].to_dict())

    def test_config_signal(self):

        blk = PID()
        # blk.method = MagicMock()
        # blk.method.assert_called_with()
        self.configure_block(blk, {'process_config' :
                                        {'set_point' : '{{$sp}}',
                                         'current_value' : '{{$value}}'},
                                   'gain_config' :
                                        {'Kp' : '{{$Kp}}',
                                         'Ki' : '{{$Ki}}',
                                         'Kd' : '{{$Kd}}'
        } })
        blk.start()
        blk.process_signals([Signal({'value' : 5,
                                     'sp' : 10,
                                     'Kp' : 1,
                                     'Ki' : 0,
                                     'Kd' : 0
        })])
        # block.process_signals([Signal({'test_count': 1})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            {'value' : 5},
            self.last_notified[DEFAULT_TERMINAL][0].to_dict())
