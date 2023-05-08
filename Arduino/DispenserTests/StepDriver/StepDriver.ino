// Include the Stepper library
#include <Stepper.h>

//Negative is in, and positive is out
// Define the number of steps per revolution for the 28BYJ-48 stepper motor
const int steps_Per_Revolution = 2038;
const int steps_per_Dispense = -70 * 100;
const int step_Speed = 15;

int combination_List[] = {0,4,5,6,10,14,15,16,20,24,25,26,30,34,35,36};
int combination_List_Size = 16;
int dispensing_Time_S = 20;
int last_Motor_Num = 1;
int motor_Num;
int digits[2];

// Define the number of stepper motors
const int num_Stepper_Motors = 6;

//Motor 1: {22, 26, 24, 28} - D1 - S
//Motor 2: {30, 34, 32, 36} - D1 - S
//Motor 3: {38, 42, 40, 44} - D1 - S
//Motor 4: {23, 27, 25, 29} - D2 - L
//Motor 5: {31, 35, 33, 37} - D2 - L
//Motor 6: {39, 43, 41, 45} - D2 - L

// Define the pins for each stepper motor
int motorPins[num_Stepper_Motors][4] = {
  {22, 26, 24, 28},
  {30, 34, 32, 36},
  {38, 42, 40, 44},
  {23, 27, 25, 29},
  {31, 35, 33, 37},
  {39, 43, 41, 45}
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
    int temp_Num = motor_Num;

    // Split the number into digits and store them in the array
    for (int i = 0; i < 2; i++) {
      digits[i] = motor_Num % 10;
      motor_Num /= 10;
    }

    if (Is_Valid_Input(temp_Num)) {
      Stepper_Drive(digits[1], digits[0]);
      Serial.println("Process complete!");
    }
    else {
      Serial.println("Invalid input");
    }
  }
}

void Stepper_Drive(int motor_Num1, int motor_Num2){

    Serial.print(motor_Num1);
    Serial.print(motor_Num2);

  if (motor_Num1 > 0 && motor_Num2 > 0){
    stepperMotors[motor_Num1 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num2 - 1].setSpeed(step_Speed);
    for (int i = 0; i < (-steps_per_Dispense); i++) {
      stepperMotors[motor_Num1 - 1].step(-1);
      stepperMotors[motor_Num2 - 1].step(-1);
      delay(1);  
    }
    for (int i = 0; i < (-steps_per_Dispense); i++) {
      stepperMotors[motor_Num1 - 1].step(1);
      stepperMotors[motor_Num2 - 1].step(1);
      delay(1);  
    } 
  }
  else if (motor_Num1 > 0) {
    stepperMotors[motor_Num1 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num1 - 1].step(steps_per_Dispense);
    delay(10); 
    stepperMotors[motor_Num1 - 1].step(-steps_per_Dispense);
  }
  else {
    stepperMotors[motor_Num2 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num2 - 1].step(steps_per_Dispense);
    delay(10); 
    stepperMotors[motor_Num2 - 1].step(-steps_per_Dispense);
  }

    // Turn off the activated motor pins
    for (int i = 0; i < 4; i++) {
      digitalWrite(motorPins[motor_Num1 - 1][i], LOW);
      digitalWrite(motorPins[motor_Num2 - 1][i], LOW);
    }


}
   

bool Is_Valid_Input(int numb){
  for (int i = 0; i < combination_List_Size; i++) {
    if (numb == combination_List[i]) {
      return true; // Return true if the number is found in the list
    }
  }
  return false; // Return false if the number is not found in the list
}