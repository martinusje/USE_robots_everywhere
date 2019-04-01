
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

int increment = 0;
int totalSize = 180*2;
int rotation = 0;

String inString = "";

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
  increment = Serial.parseInt();
  Serial.println(increment);
  if(increment!=0)
  {
    if(increment < totalSize/2)
    {
      //Left/right
      rotation = increment;
      yaw.write(rotation);
    }
    if(increment > totalSize/2)
    {
      //Left/right
      rotation = increment - totalSize/2;
      pitch.write(rotation);
    }
  }
}

