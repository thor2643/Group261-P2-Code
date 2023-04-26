// Include the Stepper library
#include <Stepper.h>

// Define the number of steps per revolution for the 28BYJ-48 stepper motor
const int steps_Per_Revolution = 2038;
const int steps_per_Dispense = 4038;
const int step_Speed = 30;

int dispensing_Time_S = 20;
int last_Motor_Num = 1;
int motor_Num;
int digits[2];

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

    // Check if the input is valid
    if (motor_Num < 11 || motor_Num > 64) {
      Serial.println("Invalid input");
      return;
    }

    // Split the number into digits and store them in the array
    for (int i = 0; i < 2; i++) {
      digits[i] = motor_Num % 10;
      motor_Num /= 10;
    }

    // Access the individual digits using the array index
    int motor_Num1 = digits[0];
    int motor_Num2 = digits[1];

    if (motor_Num1 > 0 && motor_Num2 < 7 && motor_Num2 > 0 && motor_Num2 < 7) {
      Stepper_Drive(motor_Num1, motor_Num2);
    }
    else {
      Serial.println("Invalid input");
    }
  }
}



void Stepper_Drive(int motor_Num1, int motor_Num2){
  if (motor_Num2 != 0){
    stepperMotors[motor_Num1 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num2 - 1].setSpeed(step_Speed);
    for (int i = 0; i < steps_per_Dispense; i++) {
      stepperMotors[motor_Num1 - 1].step(1);
      stepperMotors[motor_Num2 - 1].step(1);
      delay(10);  
    }
    for (int i = 0; i < steps_per_Dispense; i++) {
      stepperMotors[motor_Num1 - 1].step(-1);
      stepperMotors[motor_Num2 - 1].step(-1);
      delay(10);  
    } 
  }
  else {
    stepperMotors[motor_Num1 - 1].setSpeed(10);
    stepperMotors[motor_Num1 - 1].step(steps_per_Dispense);
    delay(10); 
    stepperMotors[motor_Num1 - 1].step(steps_per_Dispense);
  }
}
   