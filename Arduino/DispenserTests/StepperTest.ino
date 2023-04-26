#include <Stepper.h>

// Define number of steps per revolution
const int stepsPerRevolution = 2038;

// Create a new instance of the Stepper class
Stepper myStepper(stepsPerRevolution, 28, 30, 29, 31);

void setup() {
  // Set the speed of the motor (in RPM)
  myStepper.setSpeed(10);
}

void loop() {
  // Rotate forward for 3 seconds
  myStepper.step(2.8*stepsPerRevolution);
  delay(3000);

  // Rotate back for 3 seconds
  myStepper.step(-stepsPerRevolution * 2.8);
  delay(3000);
}
