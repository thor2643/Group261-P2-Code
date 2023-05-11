// Include the Stepper library
#include <Stepper.h>

// Negative is in, and positive is out in regards to the dispenser
// constants that define the number of steps per revolution for the 28BYJ-48 stepper motor, the speed and how many steps there is per dispense
const int steps_Per_Revolution = 2038;
const int steps_per_Dispense = -7300;
const int step_Speed = 20;

// A list with the double digits that are allowed, and the size of the list
int combination_List[] = {0,4,5,6,10,14,15,16,20,24,25,26,30,34,35,36};
int combination_List_Size = 16;

// An int and an int array, which will hold the motor_num being used, and the digits in the double digit
int motor_Num;
int digits[2];

// Define the number of stepper motors
const int num_Stepper_Motors = 6;

//A list to show much motor is connected to which pins on the Arduino board, which digit group they are in and what lenght of cable they have
//Motor 1: {22, 26, 24, 28} - D1 - S
//Motor 2: {30, 34, 32, 36} - D1 - S
//Motor 3: {38, 42, 40, 44} - D1 - S
//Motor 4: {23, 27, 25, 29} - D2 - L
//Motor 5: {31, 35, 33, 37} - D2 - L
//Motor 6: {39, 43, 41, 45} - D2 - L

//Definition of the pins for each stepper motor
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

//Main loop
void loop() {
  // Wait for a doubledigit to be received over the serial port. It is made into an integer
  if (Serial.available()) {
    int motor_Num = Serial.parseInt();
    int temp_Num = motor_Num;

    // Split the number into digits and store them in the array. This is done using the modolus operator
    for (int i = 0; i < 2; i++) {
      digits[i] = motor_Num % 10;
      motor_Num /= 10;
    }

    // It is checked with the double digits is valid, meaning that is is contained within the combination list. If it is, 
    // then the digits will be passed on in the stepper function
    if (Is_Valid_Input(temp_Num)) {
      Stepper_Drive(digits[1], digits[0]);
    }
    else {
      //Serial.println("Invalid input");
    }
  }
}

// This function will use the split up double digit to drive the dispensing sequence by the requested stepper motors 
void Stepper_Drive(int motor_Num1, int motor_Num2){
  
  // Serial.print(motor_Num1);
  // Serial.print(motor_Num2);

  // First it is checked if both motor values are larger than 0. If they are, it means they both need to drive at the same time
  if (motor_Num1 > 0 && motor_Num2 > 0){
    // Firsly the speed is set for both the motors
    stepperMotors[motor_Num1 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num2 - 1].setSpeed(step_Speed);
    // A for-loop is then used to make them step forward. This is done, as threading is not possible and two stepper motors therefore cannot run at the same time
    // By incrementing the steps, they both appear to move as the same time, even though they do not.
    for (int i = 0; i < (-steps_per_Dispense); i++) {
      stepperMotors[motor_Num1 - 1].step(-1);
      stepperMotors[motor_Num2 - 1].step(-1);
      delay(1);  
    }
    // A print is made, which will be send trough the serial port, to let the python program know it can continue the operation
      Serial.write("Finished\n");
    //Then a for-loop is used to move them back to the starting position, so they can dispense again.
    for (int i = 0; i < (-steps_per_Dispense); i++) {
      stepperMotors[motor_Num1 - 1].step(1);
      stepperMotors[motor_Num2 - 1].step(1);
      delay(1);  
    } 
  } // If only one of the motor values are larger than 0, only one component is needed to be moved. In this case a for-loop is not used.
  else if (motor_Num1 > 0) {
    stepperMotors[motor_Num1 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num1 - 1].step(steps_per_Dispense);
    // A print is made, which will be send trough the serial port, to let the python program know it can continue the operation
      Serial.write("Finished\n");
    delay(10); 
    stepperMotors[motor_Num1 - 1].step(-steps_per_Dispense);
  } // The same happens here, but with the other motor.
  else {
    stepperMotors[motor_Num2 - 1].setSpeed(step_Speed);
    stepperMotors[motor_Num2 - 1].step(steps_per_Dispense);
    // A print is made, which will be send trough the serial port, to let the python program know it can continue the operation
      Serial.write("Finished\n");
    delay(10); 
    stepperMotors[motor_Num2 - 1].step(-steps_per_Dispense);
  }

    // Turn off the activated motor pins. This is done as they would keep pulling power, even though they were not in use.
    // If they were kept on, they could possible also overheat, as they receive 3 volts more, than is recommended.
    for (int i = 0; i < 4; i++) {
      digitalWrite(motorPins[motor_Num1 - 1][i], LOW);
      digitalWrite(motorPins[motor_Num2 - 1][i], LOW);
    }


}
   
// This boolean function checks if the double digits is valid, meaning contained within the array.
bool Is_Valid_Input(int numb){
  for (int i = 0; i < combination_List_Size; i++) {
    if (numb == combination_List[i]) {
      return true; // Return true if the number is found in the list
    }
  }
  return false; // Return false if the number is not found in the list
}