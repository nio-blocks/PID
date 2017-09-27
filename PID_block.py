import datetime

from nio.block.base import Block
from nio.properties import VersionProperty, Property, FloatProperty, \
                           PropertyHolder, ObjectProperty
from nio.signal.base import Signal


class ProcessConfig(PropertyHolder):
    current_value = FloatProperty(title="Process Variable", default=0.0)
    set_point = FloatProperty(title="Set Point", default=0.0)


class GainConfig(PropertyHolder):
    kp = FloatProperty(title="Proportional Gain", default=0.0)
    ki = FloatProperty(title="Integral Gain", default=0.0)
    kd = FloatProperty(title="Derivative Gain", default=0.0)
    integrator_max = Property(title="Maximum Integrator",
                              default=None, allow_none=True)
    integrator_min = Property(title="Minimum Integrator",
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
        self.derivator = 0
        self.d_value = 0
        self.integrator = 0
        self.i_value = 0
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
            self.p_value = self.gain_config().kp(signal) * self.error

            # First signal has dt==0 so:
            if self.last_time:
                # Find time for Integral and Derivator error Calculations
                dt = (
                    datetime.datetime.utcnow()-self.last_time).total_seconds()
                self.logger.debug('dt {}'.format(dt))

                # Calculation for Derivative Gain, Derivator==Previous Error
                self.d_value = self.gain_config().kd(signal) * \
                    (self.error - self.derivator) / dt
                self.logger.debug('d_value{}'.format(self.d_value))
                self.derivator = self.error
                self.logger.debug('Derivator {}'.format(self.derivator))

                # Calcualation for Integral Gain, Integrator==Sum of all Errors
                self.integrator = self.integrator + self.error * dt

                # Max and Min Integrator to Prevent Integral Windup
                config_max = self.gain_config().integrator_max(signal)
                config_min = self.gain_config().integrator_min(signal)
                if config_max:
                    self.integrator = min(self.integrator, float(config_max))
                if config_min:
                    self.integrator = max(self.integrator, float(config_min))
                self.logger.debug('Integrator {}'.format(self.integrator))
                self.i_value = self.integrator * self.gain_config().ki(signal)
                self.logger.debug('i_value{}'.format(self.i_value))

            # Need for dt calculation
            self.last_time = datetime.datetime.utcnow()
            self.logger.debug('last_time {}'.format(self.last_time))
            # Final Math: Addition of all terms
            pid = self.p_value + self.i_value + self.d_value
            new_signals.append(Signal({'value': pid}))
        self.notify_signals(new_signals)
