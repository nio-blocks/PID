from nio.block.base import Block
from nio.properties import VersionProperty, Property, FloatProperty, \
                           PropertyHolder, ObjectProperty
from nio.signal.base import Signal
import datetime


class ProcessConfig(PropertyHolder):
    current_value = Property(title="Process Variable", default=0)
    set_point = FloatProperty(title="Set Point", default=0)


class GainConfig(PropertyHolder):
    Kp = FloatProperty(title="Proportional Gain", default=0)
    Ki = FloatProperty(title="Integral Gain", default=0)
    Kd = FloatProperty(title="Derivative Gain", default=0)

class PID(Block):

    version = VersionProperty('0.1.0')
    process_config = ObjectProperty(
        ProcessConfig, title="Process Variable Setup", default=ProcessConfig())
    gain_config = ObjectProperty(
        GainConfig, title="Gain Values", default=GainConfig())

    def __init__(self):
        super().__init__()
        self.Derivator = 0
        self.Integrator = 0
        self.error = 0.0
        self.last_time = None

    def start(self):
        super().start()
        self.last_time = datetime.datetime.utcnow()

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            value = self._update(self.process_config().current_value(signal))
            new_signals.append(Signal({'value' : value}))
        self.notify_signals(new_signals)


    def _update(self, current_value, current_time=datetime.datetime.utcnow()):
        """Calculate PID output for process variable at timestamp"""
        dt = (current_time - self.last_time).total_seconds()
        self.error = self.process_config().set_point() - current_value
        self.P_value = self.gain_config().Kp() * self.error
        self.D_value = \
                self.gain_config().Kd() * (self.error - self.Derivator) / dt
        self.Derivator = self.error
        self.Integrator = self.Integrator + self.error * dt
        self.last_time = datetime.datetime.utcnow()
        self.I_value = self.Integrator * self.gain_config().Ki()

        PID = self.P_value + self.I_value + self.D_value

        return PID
