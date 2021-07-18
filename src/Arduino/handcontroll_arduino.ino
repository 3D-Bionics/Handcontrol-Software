#include <SerialTransfer.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


#define SERVOMIN  150
#define SERVOMAX  600

// ServoController Class

class ServoControl {
  private:
     Adafruit_PWMServoDriver Servos;
  public:

    ServoControl(){   // initilize Servocontrol
        Servos = Adafruit_PWMServoDriver();
        Servos.begin();
        Servos.setPWMFreq(60);
        delay(10);
    };

    virtual ~ServoControl(){
    };

    bool updatePos(const uint32_t positions[]) {
      
        setServo(0, mapPosToPWM( positions[4]) );         //Pinkie
        setServo(1, mapPosToPWM( positions[3]) );         //Ringfinger
        setServo(2, mapPosToPWM( positions[2]) );         //Middlefinger
        setServo(3, mapPosToPWMReverse( positions[1]) );  //Indexfinger
        setServo(4, mapPosToPWMReverse( positions[0]) );  //Thumb

      
    };

    // Define how the servo is set in motion
    void setServo(int servonum, int pwm ){
      Servos.setPWM(servonum, 0, pwm);
    }

    // How the Position maps to PWM
    uint32_t mapPosToPWM(uint32_t pos){
      return map(pos,0,100,SERVOMIN,SERVOMAX);

    }

    // How the Position maps to PWM in Reverse
    uint32_t mapPosToPWMReverse(uint32_t pos){
        return map(pos,0,100,SERVOMAX,SERVOMIN);
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