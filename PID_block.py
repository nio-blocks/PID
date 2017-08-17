from nio.block.base import Block
from nio.properties import VersionProperty, Property, FloatProperty, \
                           PropertyHolder, ObjectProperty
from nio.signal.base import Signal
import datetime


class ProcessConfig(PropertyHolder):
    current_value = FloatProperty(title="Process Variable", default=0)
    set_point = FloatProperty(title="Set Point", default=0)


class GainConfig(PropertyHolder):
    Kp = FloatProperty(title="Proportional Gain", default=0)
    Ki = FloatProperty(title="Integral Gain", default=0)
    Kd = FloatProperty(title="Derivative Gain", default=0)
    Integrator_max = Property(title="Maximum Integrator",
                                   default=None, allow_none=True)
    Integrator_min = Property(title="Minimum Integrator",
                                   default=None, allow_none=True)


class PID(Block):

    version = VersionProperty('0.1.0')
    process_config = ObjectProperty(
        ProcessConfig, title="Process Variable Setup", default=ProcessConfig())
    gain_config = ObjectProperty(
        GainConfig, title="Gain Values", default=GainConfig())

    def __init__(self):
        super().__init__()
        self.error = 0
        self.Derivator = 0
        self.D_value = 0
        self.Integrator = 0
        self.I_value = 0
        self.last_time = None

    def start(self):
        super().start()

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:

            # Calculation for Proportional Gain, Error==SP-ProcessVariable
            self.error = self.process_config().set_point(signal) - \
                         self.process_config().current_value(signal)
            self.logger.debug('error {}'.format(self.error))
            self.P_value = self.gain_config().Kp(signal) * self.error

            # First signal has dt==0 so:
            if self.last_time:
                # Find time for Integral and Derivator error Calculations
                dt = (datetime.datetime.utcnow()-self.last_time).total_seconds()
                self.logger.debug('dt {}'.format(dt))

                # Calculation for Derivative Gain, Derivator==Previous Error
                self.D_value = self.gain_config().Kd(signal) * \
                    (self.error - self.Derivator) / dt
                self.Derivator = self.error
                self.logger.debug('Derivator {}'.format(self.Derivator))

                # Calcualation for Integral Gain, Integrator==Sum of all Errors
                self.Integrator = self.Integrator + self.error * dt

                # Max and Min Integrator to Prevent Integral Windup
                if self.gain_config().Integrator_max(signal):
                    self.Integrator = min(self.Integrator,
                                     float( self.gain_config().Integrator_max(signal)))
                if self.gain_config().Integrator_min(signal):
                    self.Integrator = max(self.Integrator,
                                     float(self.gain_config().Integrator_min(signal)))

                self.logger.debug('Integrator {}'.format(self.Integrator))
                self.I_value = self.Integrator * self.gain_config().Ki(signal)
                self.logger.debug('LastTime {}'.format(self.last_time))
            
            self.last_time = datetime.datetime.utcnow()

            # Final Math: Addition of all terms
            PID = self.P_value + self.I_value + self.D_value
            new_signals.append(Signal({'value': PID}))
        self.notify_signals(new_signals)
