from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from PID_block import PID


class TestPID(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = PID()
        self.configure_block(blk, {
                                   'kp' : "{{ $kp }}",
                                   'ki' : "{{ $ki }}",
                                   'kd' : "{{ $kd }}",
                                   'setpoint' : "{{ $setpoint }}",
                                   'current_value' : "{{ $current_value }}"
        })
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            {"PID": 2},
            self.last_notified[DEFAULT_TERMINAL][0].to_dict())
