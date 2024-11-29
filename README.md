# Ball Tracking Robot Car
## Bill of Materials:
- Raspberry Pi and breadboard
- 3V-6V DC 1:120 Gear Motor TT Motor (2x)
- L298n Dual H-Bridge Motor Driver
- 3Pcs Infrared Obstacle Avoidance Sensor (2x)
- RPI 8MP Camera Board
- Batteries
- Wires
## Goal
The overall goal of this project was to develop a car that would be able to follow a ball and stop whenever it got close enough. The robot would use a camera attached to its front to constantly take images. AFter determining the location of the ball in each one of these images, the robot would decide whether to left, right, or forward depending on the location of the ball. Finally, if the robot ever detected an obstacle in the way using the sensors, it would stop.
## How I Did This
I began this project by assembling the main chassis of the car. Once the main chassis was done, I moved onto dealing with the electricals. I first made a connection between the motors and the motor driver. In the Dual H-Bridge motor driver, there are two motor connectors, the motor A connector and the motor B connector, which connect directly to the motors. I made a connection between the 2 DC TT motors and Motor A and Motor B connectors on the Dual H-Bridge motor driver. There are also power connectors on the H-Bridge motor driver. There is one port for ground, and one port for power supply input, which will be connected with the batteries. Finally, there are 4 motor controller pins on the motor driver, and these pins will be connected with the GPIO pins. Each pair of pins affects one motor, and in each pair, one pin makes the motor spin clockwise while the other makes it spin counterclockwise. This is what will be used to make the robot car move.

Next, I attached the infrared sensors to the car. The Infrared Obstacle Avoidance Sensors has 3 pins, one for 5 volt, one for ground, and the last one for output. These pins will be used to connect the sensors to the Raspberry Pi GPIO pins. The infrared sensor has two LED’s, one transmitter and one receiver. The transmitter LED shoots out an infrared ray, and if there is an object in the way, the ray is reflected back and is received by the receiver LED and the output is made high. This is how the sensors are able to alert whether there is some object in front of them.

Finally, I connected the camera to the raspberry pi. The camera was going to be able to take photos that would be used by the program to detect where the ball is. 


