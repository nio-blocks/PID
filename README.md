Discretized PID Controller 

Properties
--------------
Measured Value : Signal to be controlled, compared with Set Point.

Set Point : Value that Measured Value should be.

Propertional Gain : Float, Proprtional Gain of the Controller (kp)

Integral Gain : Float, Integral Gain of the Controller (ki)

Derivative Gain : Float, Derivative Gain of the Controller (kd)


Dependencies
----------------
None

Commands
----------------
None

Input
-------
A list of signals containing a signal to be measured and controlled.

Output
---------
value : Calculated control from the PID controller.
