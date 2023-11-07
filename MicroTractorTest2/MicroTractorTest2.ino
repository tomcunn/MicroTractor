/*************************************************
//
//  MicroTractor v2.0
//
//  Cunningham 03/09/2023
//
**************************************************/
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Adafruit_PWMServoDriver.h>
#include <Wire.h>
#include <Servo.h>

#define PIN           D3
#define SDA           D2
#define SCL           D1

#define MOTOR_ENABLE  D4

#define MOTOR_A_POS   D5
#define MOTOR_A_NEG   D6
#define MOTOR_A_PWM   8

#define MOTOR_B_POS   D7
#define MOTOR_B_NEG   D8
#define MOTOR_B_PWM   9

#define SERVO_1       0
#define SERVO_2       1
#define SERVO_3       2
#define SERVO_4       3
#define SERVO_5       4
#define SERVO_6       5
#define SERVO_7       6
#define SERVO_8       7


#define MIN_PULSE_WIDTH       450
#define MAX_PULSE_WIDTH       2450
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             200

//Configure the PWM chip for the tractor
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x52);

void setup() 
{ 
  //Setup the i2c bus
  Wire.begin(SDA, SCL);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);

  //Drive motor
  pinMode(MOTOR_A_POS,  OUTPUT);
  pinMode(MOTOR_A_NEG,  OUTPUT);
  pinMode(MOTOR_ENABLE, OUTPUT);
  pinMode(MOTOR_B_POS,  OUTPUT);
  pinMode(MOTOR_B_NEG,  OUTPUT);
  

  //Turn on external LED
  pinMode(D0, OUTPUT);
  digitalWrite(D0, HIGH);
  
  //short delay to get things kicked off
  delay(100);

}

void loop() 
{
   digitalWrite(D0, HIGH);
   digitalWrite(MOTOR_ENABLE, HIGH);

   Forward();
   delay(100);
   Turn();
   delay(50);
   Forward();
   delay(200);
   Turn();
   delay(50);
   Reverse();
   delay(200);
   Turn();
   delay(50);
}

int pulseWidth(int angle, int servo_ID)
{
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  pwm.setPWM(servo_ID, 0, analog_value);
  return analog_value;
}


void Forward()
{
  digitalWrite(MOTOR_A_NEG, LOW);
  digitalWrite(MOTOR_A_POS, HIGH);

  digitalWrite(MOTOR_B_POS, LOW);
  digitalWrite(MOTOR_B_NEG, HIGH);
  
  pwm.setPWM(MOTOR_A_PWM, 0, 2450);
  pwm.setPWM(MOTOR_B_PWM, 0, 2450);
}

void Turn()
{
  digitalWrite(MOTOR_A_NEG, HIGH);
  digitalWrite(MOTOR_A_POS, LOW);

  digitalWrite(MOTOR_B_POS, LOW);
  digitalWrite(MOTOR_B_NEG, HIGH);
  
  pwm.setPWM(MOTOR_A_PWM, 0, 2450);
  pwm.setPWM(MOTOR_B_PWM, 0, 2450);
}

void Reverse()
{  
  digitalWrite(MOTOR_A_NEG, HIGH);
  digitalWrite(MOTOR_A_POS, LOW);

  digitalWrite(MOTOR_B_POS, HIGH);
  digitalWrite(MOTOR_B_NEG, LOW);
  
  pwm.setPWM(MOTOR_A_PWM, 0, 2450);
  pwm.setPWM(MOTOR_B_PWM, 0, 2450);
}
