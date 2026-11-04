#include <Servo.h>
Servo chute;
Servo gate;

void setup() {
  chute.attach(9);
  gate.attach(10);
  chute.write(90);
  gate.write(0);
  delay(1000);
}

void loop() {
  chute.write(30);  delay(1500);
  chute.write(90);  delay(1500);
  chute.write(150); delay(1500);
  gate.write(90);   delay(1000);
  gate.write(0);    delay(1500);
}
