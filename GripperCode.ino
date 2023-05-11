#include <Servo.h>

Servo servoTop;  // create servo objects to control a servo
Servo servoBot;
Servo servoPCB;

#define servoSignal1 13 // blå - DO8 Tool_out_1
#define servoSignal2 12 // pink - DO9 Tool_out_0
 
bool new_state = false;

int pickupPosTop = 67;    // servo position when picking up object for the top cover
int releasePosTop = 110;   // servo position when releasing object for the top cover
int pickupPosBot = 100;    // servo position when picking up object for the bottom cover
int releasePosBot = 130;   // servo position when releasing object for the bottom cover
int pickupPosPCB = 9;    // servo position when picking up object for the PCB
int releasePosPCB = 50;   // servo position when releasing object for the PCB

int gripper_delay = 0;

int signalTop = 0;
int signalBot = 0;
int signalPCB = 0;

int pickupTopActive = 0;
int pickupBotActive = 0;
int pickupPCBActive = 0; 

int countTop = 0;
int countBot = 0;
int countPCB = 0;

unsigned long count = 0;
unsigned long prev_count = 0;

int signal1 = 0;       // signal1 and signal2 help initialising the pickup and release
int signal2 = 0;
int prev_signal1 = 0;
int prev_signal2 = 0;

void setup() {
  Serial.begin(9600);

  pinMode(servoSignal1, INPUT);
  pinMode(servoSignal2, INPUT);
  
  servoTop.attach(11);  // attaches the servo to pin 9, 10, and 11
  servoBot.attach(9);
  servoPCB.attach(10);

  servoTop.write(releasePosTop);
  servoBot.write(releasePosBot);
  servoPCB.write(releasePosPCB);
}

void loop() {
  readSignalValues();         // start each loop by reading for signals to initiate picking up object

  if (signalTop == 1 && new_state == true) {
    countTop++;
    if (pickupTopActive == 0 && countTop % 2 != 0) {
      Serial.println("Gør klar til at samle Top Cover op");
      servoTop.write(pickupPosTop);       // tell servo for top cover to go to pickup position
      pickupTopActive = 1;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    if (pickupTopActive == 1 && countTop % 2 == 0) {
      Serial.println("Gør klar til at slippe Top Cover");
      servoTop.write(releasePosTop);      // tell servo for top cover to go to release position
      pickupTopActive = 0;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    signalTop = 0;
    new_state = false;
  }
    
  if (signalBot == 1 && new_state == true) {
    countBot++;
    if (pickupBotActive == 0 && countBot % 2 != 0) {
      Serial.println("Gør klar til at samle Bottom Cover op");
      servoBot.write(pickupPosBot);       // tell servo for bottom cover to go to pickup position
      pickupBotActive = 1;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    if (pickupBotActive == 1 && countBot % 2 == 0){
      Serial.println("Gør klar til at slippe Bottom Cover");
      servoBot.write(releasePosBot);      // tell servo to go to release position
      pickupBotActive = 0;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    signalBot = 0;
    new_state = false;
  }

  if (signalPCB == 1 && new_state == true) {
    countPCB++;
    if (pickupPCBActive == 0 && countPCB % 2 != 0) {
      Serial.println("Gør klar til at samle PCB op");
      servoPCB.write(pickupPosPCB);       // tell servo to go to pickup position
      pickupPCBActive = 1;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    if (pickupPCBActive == 1 && countPCB % 2 == 0){
      Serial.println("Gør klar til at slippe PCB");
      servoPCB.write(releasePosPCB);      // tell servo to go to release position
      pickupPCBActive = 0;
      delay(gripper_delay);                       // waits 15ms for the servo to reach the position
    }
    signalPCB = 0;
    new_state = false;
  }

}

void readSignalValues() {
  signal1 = digitalRead(servoSignal1);
  signal2 = digitalRead(servoSignal2);

  //delay(10);
  
  Serial.println(signal1);
  Serial.println(signal2);
  
  if (signal1 != 1 || signal2 != 1) {
    if (signal1 != prev_signal1 || signal2 != prev_signal2) {
      if (signal1 == 0 && signal2 == 1) { // signal for picking up top cover
        signalTop = 1;
        new_state = true;
      }
      
      if (signal1 == 1 && signal2 == 0) { // signal for picking up bottom cover
        signalBot = 1; 
        new_state = true;
      }
      
      if (signal1 == 0 && signal2 == 0) { // signal for picking up PCB cover
        signalPCB = 1;
        new_state = true;
      }
    }
  }

  prev_signal1 = signal1;
  prev_signal2 = signal2;
  
  //delay(250);
 
}