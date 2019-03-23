
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

#include <Stepper.h>

const int stepsPerRevolution = 4096 ;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 7, 8, 8, 10);

String readString;

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(7);
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
    if (readString == "right"){
      myStepper.step(stepsPerRevolution/30);
      delay(500);
    }
    if (readString == "left"){
      myStepper.step(-stepsPerRevolution/30);
      delay(500);
    }
    readString="";
  } 
}

