// Include the Stepper library
#include <Stepper.h>

// Define the number of steps per revolution for the 28BYJ-48 stepper motor
const int stepsPerRevolution = 2038;

// Define the number of stepper motors
const int numStepperMotors = 6;

// Define the pins for each stepper motor
int motorPins[numStepperMotors][4] = {
  {8, 9, 10, 11},
  {12, 13, 14, 15},
  {16, 17, 18, 19},
  {20, 21, 22, 23},
  {24, 25, 26, 27},
  {28, 29, 30, 31}
};

// Define the stepper motor objects
Stepper stepperMotors[numStepperMotors] = {
  Stepper(stepsPerRevolution, motorPins[0][0], motorPins[0][1], motorPins[0][2], motorPins[0][3]),
  Stepper(stepsPerRevolution, motorPins[1][0], motorPins[1][1], motorPins[1][2], motorPins[1][3]),
  Stepper(stepsPerRevolution, motorPins[2][0], motorPins[2][1], motorPins[2][2], motorPins[2][3]),
  Stepper(stepsPerRevolution, motorPins[3][0], motorPins[3][1], motorPins[3][2], motorPins[3][3]),
  Stepper(stepsPerRevolution, motorPins[4][0], motorPins[4][1], motorPins[4][2], motorPins[4][3]),
  Stepper(stepsPerRevolution, motorPins[5][0], motorPins[5][1], motorPins[5][2], motorPins[5][3])
};

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {
  // Wait for a value from 1 to 6 to be received over the serial port
  while (Serial.available() == 0);
  int motorNum = Serial.parseInt();

  // Move the selected motor one revolution
  stepperMotors[motorNum - 1].setSpeed(5);
  stepperMotors[motorNum - 1].step(stepsPerRevolution);
  delay(1000);
}
