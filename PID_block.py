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

            dt = (datetime.datetime.utcnow() - self.last_time).total_seconds()
            print('dt {}'.format(dt))
            self.logger.debug('dt {}'.format(dt))

            #Calculation for Proportional Gain, Error==SP-ProcessVariable
            self.error = self.process_config().set_point(signal) - \
                         self.process_config().current_value(signal)
            self.logger.debug('error {}'.format(self.error))
            print('error {}'.format(self.error))
            self.P_value = self.gain_config().Kp(signal) * self.error

            #Calculation for Derivative Gain, Derivator==Previous Error
            self.D_value = \
                    self.gain_config().Kd(signal) * \
                    (self.error - self.Derivator) / dt
            self.Derivator = self.error
            self.logger.debug('Derivator {}'.format(self.Derivator))
            print('Derivator {}'.format(self.Derivator))
            print('D {}'.format(self.D_value))
            #Calcualation for Integral Gain, Integrator==Sum of all Errors
            self.Integrator = self.Integrator + self.error * dt
            self.logger.debug('Integrator {}'.format(self.Integrator))
            print('Integrator {}'.format(self.Integrator))
            self.last_time = datetime.datetime.utcnow()
            self.I_value = self.Integrator * self.gain_config().Ki(signal)
            print('I {}'.format(self.I_value))
            #Final Math Addition of all terms
            PID = self.P_value + self.I_value + self.D_value
            new_signals.append(Signal({'value' : PID}))
        self.notify_signals(new_signals)
