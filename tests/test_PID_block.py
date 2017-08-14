from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import MagicMock, ANY
from PID_block import PID


class TestPID(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        value = {'clear' : ANY}

        blk = PID()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal(value)])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            {'value' : ANY},
            self.last_notified[DEFAULT_TERMINAL][0].to_dict())
