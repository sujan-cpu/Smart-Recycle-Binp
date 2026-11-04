#include <Servo.h>
Servo chute;
Servo gate;

const int PLASTIC_ANGLE = 30;
const int PAPER_ANGLE = 90;
const int METAL_ANGLE = 150;

void setup() {
  Serial.begin(9600);
  chute.attach(9);
  gate.attach(10);
  chute.write(PAPER_ANGLE);
  gate.write(0);
  Serial.println("READY: send P=Plastic, A=Paper, M=Metal");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    int angle = -1;

    if (command == 'P' || command == 'p') angle = PLASTIC_ANGLE;
    else if (command == 'A' || command == 'a') angle = PAPER_ANGLE;
    else if (command == 'M' || command == 'm') angle = METAL_ANGLE;

    if (angle >= 0) {
      gate.write(0);
      delay(300);
      chute.write(angle);
      delay(1000);
      gate.write(90);
      delay(1200);
      gate.write(0);
      Serial.println("SORTING COMPLETE");
    }
  }
}
