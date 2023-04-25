// Include the Stepper library
#include <Stepper.h>

// Define the number of steps per revolution for the 28BYJ-48 stepper motor
const int steps_Per_Revolution = 2038;

int motor_Num;

// Define the number of stepper motors
const int num_Stepper_Motors = 6;

// Define the pins for each stepper motor
int motorPins[num_Stepper_Motors][4] = {
  {8, 10, 9, 11},
  {12, 14, 13, 15},
  {16, 18, 17, 19},
  {20, 22, 21, 23},
  {24, 26, 25, 27},
  {28, 30, 29, 31}
};

// Define the stepper motor objects
Stepper stepperMotors[num_Stepper_Motors] = {
  Stepper(steps_Per_Revolution, motorPins[0][0], motorPins[0][1], motorPins[0][2], motorPins[0][3]),
  Stepper(steps_Per_Revolution, motorPins[1][0], motorPins[1][1], motorPins[1][2], motorPins[1][3]),
  Stepper(steps_Per_Revolution, motorPins[2][0], motorPins[2][1], motorPins[2][2], motorPins[2][3]),
  Stepper(steps_Per_Revolution, motorPins[3][0], motorPins[3][1], motorPins[3][2], motorPins[3][3]),
  Stepper(steps_Per_Revolution, motorPins[4][0], motorPins[4][1], motorPins[4][2], motorPins[4][3]),
  Stepper(steps_Per_Revolution, motorPins[5][0], motorPins[5][1], motorPins[5][2], motorPins[5][3])
};

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {
  // Wait for a value from 1 to 6 to be received over the serial port
  if (Serial.available()) {
    int motor_Num = Serial.parseInt();
    if (motor_Num > 0 && motor_Num < 7) {
      stepperMotors[motor_Num - 1].setSpeed(15);
      stepperMotors[motor_Num - 1].step(steps_Per_Revolution*2 );
      delay(1000);  
      stepperMotors[motor_Num - 1].step(-steps_Per_Revolution * 2);
      delay(1000);  

    }
  }
}
