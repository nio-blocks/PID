from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty
from nio.signal.base import Signal



class PID(Block):

    version = VersionProperty('0.1.0')
    kp = IntProperty(title = "Proportional Gain", default = 0)
    # ki = IntProperty(title = "Integral Gain", default = 0)
    # kd = IntProperty(title = "Derivative Gain", default = 0)
    setpoint = IntProperty(title = "Setpoint", default = 0)
    current_value = IntProperty(title = 'Attribute to Control', default = 0)
    # integral_error = 0
    # derivative_error = 0
    # previous_error = 0

    def process_signals(self, signals):
        for signal in signals:
            self.error = self.setpoint() - self.current_value()
            #self.integral_error =+ self.error
            #self.derivative_error = self.error - self.previous_error
            PID = self.kp * self.error
            #self.previous_error = self.error

            self.notify_signals([ Signal( {"PID" : PID} )])
