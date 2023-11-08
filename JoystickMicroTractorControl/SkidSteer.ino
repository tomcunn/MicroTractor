#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Adafruit_PWMServoDriver.h>
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_NeoPixel.h>


#define PIN D3
#define pwmSDA D2
#define pwmSCL D1

#define MIN_PULSE_WIDTH       450
#define MAX_PULSE_WIDTH       2450
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             200

WiFiServer tractor_server(10010);
WiFiClient ComputerClientConnection;

//Configure the LEDS for the tractor
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(4, PIN);
//Configure the PWM chip for the tractor
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x52);

String data;
static int servo_position  = 30;
static int servo_direction = 0;
static int counter = 0;
static int turn = 0;
static int PreviousLightRequest = 0;

void setup() 
{ 
  //Start the LEDS
  pixels.begin();
  delay(100);
  
  //Setup the i2c bus
  Wire.begin(pwmSDA, pwmSCL);
  pwm.begin();
  pwm.setPWMFreq(200);

  //Drive Motor Right
  pinMode(D6, OUTPUT);
  pinMode(D5, OUTPUT);
  digitalWrite(D6, LOW);
  digitalWrite(D5, LOW);
  pwm.setPWM(8, 4096, 0);

  //Drive Motor Left
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  digitalWrite(D7, LOW);
  digitalWrite(D8, LOW);
  pwm.setPWM(9, 4096, 0);

  //Start the serial port to allow for debugging
  Serial.begin(115200);
  Serial.println();

  //Start the wifi access point
  Serial.print("Setting soft-AP ... ");
  boolean result = WiFi.softAP("microtractor");

  if(result == true)
  {
    Serial.println("Ready");
  }
  else
  {
    Serial.println("Failed!");
  }

  //Print the IP address of the network
  Serial.println(WiFi.softAPIP());

  //Start the server on port 10010
  tractor_server.begin();

  //Turn on external LED
  pinMode(D0, OUTPUT);
  digitalWrite(D0, HIGH);
  
  //short delay to get things kicked off
  delay(100);

}

void loop() 
{
   
   //Wait for the computer to connect
   ComputerClientConnection =  tractor_server.available();
   if(ComputerClientConnection)
   {
      Serial.println("Computer is connected on port 10010");

      byte incoming_data[4];
      int NumberOfBytesRX;

      //Set all of the incoming data to 0
      incoming_data[0] = 0;
      incoming_data[1] = 0;
      incoming_data[2] = 0;
      incoming_data[3] = 0;
      
      //Perform this loop as long as the computer is connected
      while(ComputerClientConnection.connected())
      {
         //Get data from the client connection
         //This line is currently setting the task rate
         NumberOfBytesRX = ComputerClientConnection.readBytesUntil( 0x68, incoming_data,4);

         //print line data
         Serial.println(NumberOfBytesRX);
         Serial.println("Incoming data: " + String(incoming_data[0]) + "," + String(incoming_data[1]) + "," + String(incoming_data[2]) + "," + String(incoming_data[3]));
         //Add a delay in here to service the watchdog
         delay(1);  
         //Process travel direction
         ProcessMotionControl(incoming_data[1],incoming_data[2]);
      }  
   }
}

int pulseWidth(int angle)
{
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return analog_value;
}


void ProcessMotionControl(byte LeftCommand, byte RightCommand)
{
  //****************LEFT SIDE***************
  if(LeftCommand < 125)
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, HIGH);
    pwm.setPWM(8, 1024, 3072);

  }
  else if(LeftCommand > 125)
  {
    digitalWrite(D5, LOW);
    digitalWrite(D6, HIGH);
    pwm.setPWM(8,  1024, 3072);
  }
  else
  {
    digitalWrite(D6, LOW);
    digitalWrite(D5, LOW);
    pwm.setPWM(8, 4096, 0);
  }

  //****************RIGHT SIDE**************
  //Reverse
  if(RightCommand < 125)
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, HIGH);
    pwm.setPWM(9, 1024, 3072);
  }
  //Forward
  else if(RightCommand > 125)
  {
    digitalWrite(D8, LOW);
    digitalWrite(D7, HIGH);
    pwm.setPWM(9,  1024, 3072);
  }
  //Stop
  else
  {
    digitalWrite(D7, LOW);
    digitalWrite(D8, LOW);
    pwm.setPWM(9, 4096, 0);
  }
}

