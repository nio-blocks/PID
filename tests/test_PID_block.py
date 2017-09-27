from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import MagicMock, ANY
from ..PID_block import PID


class TestPID(NIOBlockTestCase):

    def test_onesignal_ponly(self):
        blk = PID()
        self.configure_block(
            blk,
            {
                'process_config': {'set_point': 9, 'current_value': 5},
                'gain_config': {'kp': 1, 'ki': 2, 'kd': 3}
            }
        )
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            {'value': 4},
            self.last_notified[DEFAULT_TERMINAL][0].to_dict())

    def test_config_signal(self):

        blk = PID()
        pv = 1000000
        setp = 10
        kp = 1
        ki = 2
        kd = 3
        imax = -150
        imin = None
        self.configure_block(
            blk,
            {
                'process_config': {'set_point': '{{$sp}}',
                                   'current_value': '{{$value}}'},
                'gain_config': {'kp': '{{$kp}}',
                                'ki': '{{$ki}}',
                                'kd': '{{$kd}}',
                                'integrator_max': '{{$imax}}',
                                'integrator_min': '{{$imin}}'}
            }
        )
        blk.start()
        blk.process_signals([Signal({'value': pv,
                                     'sp': setp,
                                     'kp': kp,
                                     'ki': ki,
                                     'kd': kd,
                                     'imax': imax,
                                     'imin': imin
                                     }),
                             Signal({'value': pv,
                                     'sp': setp,
                                     'kp': kp,
                                     'ki': ki,
                                     'kd': kd,
                                     'imax': imax,
                                     'imin': imin
                                     })])

        blk.stop()
        self.assert_num_signals_notified(2)
        print([n.to_dict() for n in self.last_notified[DEFAULT_TERMINAL]])
        self.assertFalse(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict() ==
            self.last_notified[DEFAULT_TERMINAL][1].to_dict())
