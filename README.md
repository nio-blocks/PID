PID
===
A NIO Block that creates a discretized PID Controlled output from a list of incoming signals.

Properties
----------
- **Process Variable** : Signal to be controlled, compared with Set Point.
- **Set Point** : Value to compare with Process Variable.
- **Propertional Gain** : Float, Proprtional Gain of the Controller (kp)
- **Integral Gain** : Float, Integral Gain of the Controller (ki)
- **Derivative Gain** : Float, Derivative Gain of the Controller (kd)
- **Integrator Max** : Float, Maximum Integrator to be applied to prevent Integral Windup
- **Integrator Min** : Float, Minimum Integrator to be applied to prevent Integral Windup

Input
-------
- **default**: Any list of signals.

Output
---------
- **value**: Float, Calculated control output from the PID controller.

Dependencies
----------------
None

Commands
----------------
None
