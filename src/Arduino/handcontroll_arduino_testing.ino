#include "SerialTransfer.h"
#include "Servo.h"


// Servo Class

class ServoControl {

  Servo servo1;
  
  public:

    ServoControl(){
      servo1.attach(9);
      servo1.write(20);
    };

    virtual ~ServoControl(){
      servo1.detach();
    };

    bool SetPosition(const uint32_t positions[]) {
      
      servo1.write(mapPos(positions[0]));
      return true;
    };

      
    uint32_t mapPos(const uint32_t &pos){
      return map(pos,0,100,0,180);
    };

};

// Defining Globals

SerialTransfer Transfer;

ServoControl* Control;

uint32_t marray[5];

// Defining Callbacks

void servo_do(){

  Transfer.rxObj(marray);

  Control->SetPosition(marray);

  Transfer.sendDatum(marray);
    
}

//functionpointer array; needed for SerialTransfer
const functionPtr callbackArr[] = {servo_do};


//Setup and Loop

void setup()
{

    Control = new ServoControl;

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