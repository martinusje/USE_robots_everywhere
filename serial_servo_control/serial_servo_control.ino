
/*
 Stepper Motor Control - one revolution

 This program drives a unipolar or bipolar stepper motor.
 The motor is attached to digital pins 8 - 11 of the Arduino.

 The motor should revolve one revolution in one direction, then
 one revolution in the other direction.


 Created 11 Mar. 2007
 Modified 30 Nov. 2009
 by Tom Igoe

 */

#include <Servo.h>

Servo pitch;  // create servo object to control a servo
Servo yaw;
// twelve servo objects can be created on most boards

int pos = 0;
int pos_yaw = 90;    // variable to store the servo position
int pos_pitch = 0;

int increment = 8;

String readString;

void setup() {
  pitch.attach(10);
  yaw.attach(9);

  pitch.write(0);
  delay(500);
  yaw.write(90);
  
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  // step one revolution  in one direction:
  while (Serial.available()) {
    delay(3);  
    char c = Serial.read();
    readString += c; 
  }
  if (readString.length() >0) {
    if (readString == "left" && pos_yaw < 180){
      for (pos = pos_yaw; pos <= pos_yaw+increment; pos += 1) { // goes from 0 degrees to 180 degrees
        yaw.write(pos);              // tell servo to go to position in variable 'pos'
        delay(increment);                       // waits incrementms for the servo to reach the position
      }
      pos_yaw += increment;
    }
    if (readString == "right" && pos_yaw > 0){
      for (pos = pos_yaw; pos >= pos_yaw-increment; pos -= 1) { // goes from 0 degrees to 180 degrees
        yaw.write(pos);              // tell servo to go to position in variable 'pos'
        delay(increment);                       // waits incrementms for the servo to reach the position
      }
      pos_yaw -= increment;
    }
    if (readString == "up" && pos_pitch < 180){
      for (pos = pos_pitch; pos <= pos_pitch+increment; pos += 1) { // goes from 0 degrees to 180 degrees
        pitch.write(pos);              // tell servo to go to position in variable 'pos'
        delay(increment);                       // waits incrementms for the servo to reach the position
      }
      pos_pitch += increment;
    }
    if (readString == "down" && pos_pitch > 0){
      for (pos = pos_pitch; pos >= pos_pitch-increment; pos -= 1) { // goes from 0 degrees to 180 degrees
        pitch.write(pos);              // tell servo to go to position in variable 'pos'
        delay(increment);                       // waits incrementms for the servo to reach the position
      }
      pos_pitch -= increment;
    }
    readString="";
  } 
}

