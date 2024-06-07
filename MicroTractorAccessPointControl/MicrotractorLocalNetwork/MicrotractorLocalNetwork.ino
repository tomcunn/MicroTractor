#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>
#include <WiFiUdp.h>
#include "Arduino.h"
#include "Wire.h"
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

#define PIN D3
#define pwmSDA D2
#define pwmSCL D1

#define FRONT_HITCH 3

#define MIN_PULSE_WIDTH       200  //150
#define MAX_PULSE_WIDTH       500  //600
#define FREQUENCY             50

//Function Prototypes
void ProcessFrontHitchControl(byte desired_angle);


//******************************************************************

char replyPacket[] = "GreyTractor"; // a reply string to send back
const char *ssid = "ESP-2F050A";
const char *password = "********";

//********************************************************************

//IP address of the computer you are connecting to
IPAddress RaspberryIP(192,168,4,2);
IPAddress VehicleIP(192, 168, 4, 1);

//Configure the pwm driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x52);

//Create wifi parameters
WiFiUDP Udp;
WiFiClient client;
unsigned int localUdpPort = 5000; // local port to listen on



void setup_motors()
{
  //Set Frequency for PCA chip
  Wire.begin(pwmSDA, pwmSCL);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
  
  //Drive Motor Right
  pinMode(D6, OUTPUT);
  pinMode(D5, OUTPUT);
  digitalWrite(D6, LOW);
  digitalWrite(D5, LOW);
  pwm.setPWM(8, 0, 4096);

  //Drive Motor Left
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  digitalWrite(D7, LOW);
  digitalWrite(D8, LOW);
  pwm.setPWM(9, 0, 4096);

  //Setup the Hitch
  ProcessFrontHitchControl(90);
}

void setup() 
{
  Serial.begin(115200);
  delay(3000);

  Serial.println();
  Serial.println("Configuring access point...");

  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  // Initialize OTA
  ArduinoOTA.begin();
  setup_motors();
  delay(1000);
   
  Udp.begin(localUdpPort);
}

//*******************************************************
//
//  Function: Loop
//
//  Runs the main loop of the project
//
//*******************************************************
void loop() 
{
  static bool EnableDriveTrain = false;
  
  // Handle OTA updates
  ArduinoOTA.handle();
   
  //Check to see if a packet has come in the door
  int packetSize = Udp.parsePacket();
 
  //If the packet is present
  if (packetSize)
  { 
    //Create an array to hold the data
    char incoming_data[packetSize];
    int len = Udp.read(incoming_data, Udp.remotePort());
    
    Serial.println(incoming_data);

    //Check for enable/disable commands
    if(incoming_data[0] == 0x4D)
    {
      //Check for A Button to Enable
      if(incoming_data[4] == 1) 
      {
        EnableDriveTrain = true;
        Serial.println("Enabled");
      }
      //Check for Y-Button to Stop
      if(incoming_data[5] == 1)
      { 
        EnableDriveTrain = false;
        pwm.setPWM(9, 0, 4096);
        pwm.setPWM(8, 0, 4096);
        Serial.println("Disabled");
      }
    }

    if(EnableDriveTrain)
    {
      if(incoming_data[0] == 0x4D)
      {
        //Process travel direction
        Serial.println(incoming_data);
        ProcessMotionControl(incoming_data[1],incoming_data[2]);

        //Process the front hitch control
        if(incoming_data[3] != 0xFF)
        {
          ProcessFrontHitchControl(incoming_data[3]);
        } 
      }
    }
  }
}

//***************************************************************
//
//  Function: ProcessFrontHitchControl
//
//  Move the front hitch up and down
//
//  Defaults to 90, can move to 180 or 0
//
//**************************************************************
void ProcessFrontHitchControl(byte desired_angle)
{
  long degrees = (long)desired_angle;
  uint16_t pulselength;
  pulselength = map(degrees, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  pwm.setPWM(FRONT_HITCH,  0, pulselength);
}

//************************************************************
//
//  Function: ProcessMotionControl
//
//  Process the left and right drive commands to the wheel 
//  motors 
//  
//  Full Speed Forward = 250
//  Stop               = 125
//  Full Speed Reverse =   0
//
//************************************************************
void ProcessMotionControl(byte LeftCommand, byte RightCommand)
{
  //Take off the offset, the value should be between -100 and 100
  int LeftPercent = LeftCommand - 125;
  int RightPercent = RightCommand -125;
  int value = 0;
  
  //****************LEFT SIDE***************
  value = DeterminePercent(abs(LeftPercent));
  
  if(LeftPercent < 0)
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, HIGH);
    pwm.setPWM(8, 0, value);

  }
  else if(LeftPercent > 0)
  {
    digitalWrite(D5, LOW);
    digitalWrite(D6, HIGH);
    
    pwm.setPWM(8,  0, value);
  }
  else
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, LOW);
    pwm.setPWM(8, 0, 4096);
  }

  //****************RIGHT SIDE**************
  value = DeterminePercent(abs(RightPercent));
  
  //Reverse
  if(RightPercent < 0)
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, HIGH);
    pwm.setPWM(9, 0, value);
  }
  //Forward
  else if(RightPercent > 0)
  {
    digitalWrite(D8, LOW);
    digitalWrite(D7, HIGH);
    pwm.setPWM(9,  0, value);
  }
  //Stop
  else
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, LOW);
    pwm.setPWM(9, 0, 4096);
  }
}

int DeterminePercent(int percent)
{
  int value;

  value = (int16_t)(((int32_t)percent * 4095) / 125);
  return value;
}
