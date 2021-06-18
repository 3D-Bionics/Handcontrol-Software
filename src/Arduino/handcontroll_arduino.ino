#include "SerialTransfer.h"
#include "Servo.h"


#define SERVOMIN  150 // Needs modification
#define SERVOMAX  600

// ServoController Class

class ServoControl {
  
  public:

    ServoControl(){
        // initilize Servos
    };

    virtual ~ServoControl(){

        // Detach all Servos here

    };

    bool updatePos(const uint32_t positions[]) {
      
        setServo(0, mapPosToPWM( positions[0]) );
        setServo(1, mapPosToPWM( positions[1]) );
        setServo(2, mapPosToPWM( positions[2]) );
        setServo(3, mapPosToPWMReverse( positions[3]) );
        setServo(4, mapPosToPWMReverse( positions[4]) );

      
    };

    // Define how the servo is set in motion (possible envelope)
    void setServo(int servonum, int pwm ){
  
        
        // Something along the lines of "myServos.setPWM(servonum, 0, pwm);"

    }

    // How the Position maps to PWM
    uint32_t mapPosToPWM(uint32_t pos){

    }

    // How the Position maps to PWM in Reverse
    uint32_t mapPosToPWMReverse(uint32_t pos){
        
    }

};

// Defining Globals

SerialTransfer Transfer;

ServoControl* Control;

uint32_t marray[5];

// Defining Callbacks

void servo_do(){

  Transfer.rxObj(marray);

  Control->updatePos(marray);

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