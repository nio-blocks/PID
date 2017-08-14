from nio.block.base import Block
from nio.properties import VersionProperty, Property, FloatProperty
from nio.signal.base import Signal
import datetime


class PID(Block):

    version = VersionProperty('0.1.0')
    Kp = FloatProperty(title="Proportional Gain", default=0)
    Ki = FloatProperty(title="Integral Gain", default=0)
    Kd = FloatProperty(title="Derivative Gain", default=0)
    Integrator_max = FloatProperty(title="Integrator_max", default=500, visible=False)
    Integrator_min = FloatProperty(title="Integrator_min", default=-500, visible=False)
    current_value = Property(title='Process Variable', default=0)
    set_point = FloatProperty(title='Set Point', default=0)


    def __init__(self):
        super().__init__()
        self.Derivator = 0
        self.Integrator = 0
        self.Integrator_max = self.Integrator_max()
        self.Integrator_min = self.Integrator_min()
        self.error = 0.0
        self.last_time = None

    def start(self):
        super().start()
        self.last_time = datetime.datetime.utcnow()

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            value = self._update(self.current_value(signal))
            new_signals.append(Signal({'value' : value}))
        self.notify_signals(new_signals)


    def _update(self, current_value, current_time=datetime.datetime.utcnow()):
        """Calculate PID output value for given reference input and feedback"""
        dt = (current_time - self.last_time).total_seconds()
        self.error = self.set_point() - current_value
        self.P_value = self.Kp() * self.error
        self.D_value = self.Kd() * (self.error - self.Derivator) / dt

        self.Derivator = self.error
        self.Integrator = self.Integrator + self.error * dt
        self.last_time = datetime.datetime.utcnow()
        if self.Integrator > self.Integrator_max():
            self.Integrator = self.Integrator_max()
        elif self.Integrator < self.Integrator_min():
            self.Integrator = self.Integrator_min()

        self.I_value = self.Integrator * self.Ki()

        PID = self.P_value + self.I_value + self.D_value

        return PID
