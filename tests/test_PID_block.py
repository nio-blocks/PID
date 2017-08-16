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
        pv = 9
        setp = 10
        kp = 1
        ki = 1
        kd = 1
        self.configure_block(blk, {'process_config' :
                                        {'set_point' : '{{$sp}}',
                                         'current_value' : '{{$value}}'},
                                   'gain_config' :
                                        {'Kp' : '{{$Kp}}',
                                         'Ki' : '{{$Ki}}',
                                         'Kd' : '{{$Kd}}'
        } })
        blk.start()
        blk.process_signals([Signal({'value' : pv,
                                     'sp' : setp,
                                     'Kp' : kp,
                                     'Ki' : ki,
                                     'Kd' : kd}),
                             Signal({'value' : pv,
                                     'sp' : setp,
                                     'Kp' : kp,
                                     'Ki' : ki,
                                     'Kd' : kd
        })] )
        # block.process_signals([Signal({'test_count': 1})])
        blk.stop()
        self.assert_num_signals_notified(2)
        print([n.to_dict() for n in self.last_notified[DEFAULT_TERMINAL]])
        self.assertFalse(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict()==\
            self.last_notified[DEFAULT_TERMINAL][1].to_dict())
        # self.assertDictEqual(
            # {'value' : ANY},
            # self.last_notified[DEFAULT_TERMINAL][0].to_dict())
