#include <Servo.h>
Servo chute;
Servo gate;

const int CHUTE_PIN = 9;
const int GATE_PIN = 10;

// Calibrate these angles for your actual chute.
const int PLASTIC_ANGLE = 30;
const int PAPER_ANGLE = 90;
const int METAL_ANGLE = 150;

const int CHUTE_SETTLE_MS = 900;
const int RELEASE_MS = 1200;

void setup() {
  Serial.begin(9600);
  chute.attach(CHUTE_PIN);
  gate.attach(GATE_PIN);
  gate.write(0);  // release gate closed
  chute.write(PAPER_ANGLE);
  delay(500);
  Serial.println("READY");
}

void sortItem(int targetAngle, const char *category) {
  gate.write(0);
  delay(250);
  chute.write(targetAngle);
  delay(CHUTE_SETTLE_MS);
  gate.write(90);  // release item
  delay(RELEASE_MS);
  gate.write(0);
  delay(300);
  Serial.print("DONE:");
  Serial.println(category);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'P' || command == 'p') {
      sortItem(PLASTIC_ANGLE, "PLASTIC");
    } else if (command == 'A' || command == 'a') {
      sortItem(PAPER_ANGLE, "PAPER");
    } else if (command == 'M' || command == 'm') {
      sortItem(METAL_ANGLE, "METAL");
    } else if (command == 'X' || command == 'x') {
      gate.write(0);
      Serial.println("CANCELLED");
    }
  }
}
