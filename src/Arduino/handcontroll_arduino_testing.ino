#include "SerialTransfer.h"
#include "Servo.h"

//Defining Globals

Servo servo1;

SerialTransfer Transfer;

uint32_t marray[5];

//Defining Callbacks

void servo_do(){

  Transfer.rxObj(marray);

  int pos = map(marray[0],0,100,0,180);

  servo1.write(marray[0]);

  Transfer.sendDatum(marray);
    
}

//functionpointer array; needed for SerialTransfer
const functionPtr callbackArr[] = {servo_do};


//Setup and Loop

void setup()
{
    servo1.attach(9);
    servo1.write(0);

    //Communicaion Stuff
    Serial.begin(115200);

    configST serial_config;
    serial_config.callbacks = callbackArr;
    serial_config.callbacksLen = sizeof(callbackArr) / sizeof(functionPtr);


    Transfer.begin(Serial, serial_config);

    Serial.println("READY");
}

void loop()
{
  //SerialTransfer Loop Function; Checks for new messages and calls specific function for specific package ID
  Transfer.tick();
}