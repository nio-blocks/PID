Discretized PID Controller 
==========================

Properties
--------------
Process Variable : Signal to be controlled, compared with Set Point.

Set Point : Value to compare with Process Variable.

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
A list of signals containing a Process Variable.

Output
---------
value : Float, Calculated control output from the PID controller.
