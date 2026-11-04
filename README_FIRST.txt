SMART AI RECYCLING BIN - PLASTIC / PAPER / METAL
================================================

WHAT IT DOES
A laptop camera and a Teachable Machine image model classify an item as Plastic, Paper,
Metal, or No Object. Python sends P, A, or M over USB serial to Arduino. Arduino turns
a sorting chute and opens a release flap.

IMPORTANT: THE TRAINED AI MODEL IS NOT INCLUDED.
Train your own model at https://teachablemachine.withgoogle.com/
Choose Image Project and create FOUR classes:
  Plastic
  Paper
  Metal
  No Object

Export as TensorFlow -> Keras. Copy keras_model.h5 and labels.txt into the Model folder.
The labels.txt file should have one class per line. Example:
0 Plastic
1 Paper
2 Metal
3 No Object
The order may differ; the Python code reads the labels.

HARDWARE
- Arduino Uno or compatible board
- Two servo motors (SG90 for a lightweight prototype)
- Laptop with camera or USB webcam
- USB cable, three compartments, sorting chute and release flap

SERVO WIRING
Sorting chute servo: signal -> D9
Release gate servo: signal -> D10
Both servo red wires -> regulated external 5V
Both servo brown/black wires -> GND
External supply GND -> Arduino GND (common ground).

POWER SAFETY
Use a separate regulated 5V supply suitable for the servos. Do not connect the external
5V supply to the Arduino 5V pin. Test the mechanism without fingers near moving parts.
Small SG90 servos may not be strong enough for a heavy chute.

INSTALLATION
1. Install Python 3.
2. Open a terminal in this project folder.
3. Install dependencies:
     python -m pip install -r requirements.txt
4. Upload Arduino/Page3_Final_Arduino.ino to your Arduino.
5. Find the serial port:
   Windows: Device Manager -> Ports, e.g. COM3
   macOS: Terminal command `ls /dev/cu.*`, e.g. /dev/cu.usbmodemXXXX
   Linux: often /dev/ttyACM0 or /dev/ttyUSB0
6. Edit Python/Page6_Final_AI_Sorting.py and set SERIAL_PORT to your port.
7. Put keras_model.h5 and labels.txt in Model/.
8. Close Arduino Serial Monitor and run:
     python Python/Page6_Final_AI_Sorting.py

TEST ORDER
1. Upload Page1_Servo_Test.ino to test both servos.
2. Upload Page2_Sorting_Test.ino and send P, A, M in Serial Monitor.
3. Upload Page3_Final_Arduino.ino.
4. Run Python/Page4_Camera_Test.py.
5. Run Python/Page5_AI_Test.py.
6. Run Python/Page6_Final_AI_Sorting.py.

CALIBRATION
Default chute angles: Plastic 30°, Paper 90°, Metal 150°. Adjust these in Page3_Final_Arduino.ino
so the chute lines up with your actual compartments. The release gate uses 0° closed and
90° open; adjust if your mechanism needs different angles.

LIMITATIONS
The camera model estimates visual appearance; it cannot guarantee actual material composition.
Train with varied images and follow local recycling rules. An inductive proximity sensor can
be added to help verify metal. Dirty, coated, or mixed-material items may need to be rejected.
