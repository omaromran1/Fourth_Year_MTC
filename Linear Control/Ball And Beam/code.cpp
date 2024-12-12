/* PID balance code with ping pong ball and distance sensor sharp 2y0a21
 *  by ELECTRONOOBS: https://www.youtube.com/channel/UCjiVhIvGmRZixSzupD0sS9Q
 *  Tutorial: http://electronoobs.com/eng_arduino_tut100.php
 *  Code: http://electronoobs.com/eng_arduino_tut100_code1.php
 *  Scheamtic: http://electronoobs.com/eng_arduino_tut100_sch1.php 
 *  3D parts: http://electronoobs.com/eng_arduino_tut100_stl1.php   
 */
#include <Wire.h>
#include <Servo.h>



///////////////////////Inputs/outputs///////////////////////
int Analog_in = A0;
Servo myservo;  // create servo object to control a servo, later attatched to D9
///////////////////////////////////////////////////////


////////////////////////Variables///////////////////////
int Read = 0;
float distance = 0.0;
float elapsedTime, time, timePrev;        //Variables for time control
float distance_previous_error, distance_error;
int period = 50;  //Refresh rate period of the loop is 50ms
///////////////////////////////////////////////////////


///////////////////PID constants///////////////////////
float kp=8; //Mine was 8
float ki=0.2; //Mine was 0.2
float kd=3100; //Mine was 3100
float distance_setpoint = 21;           //Should be the distance from sensor to the middle of the bar in mm
float PID_p, PID_i, PID_d, PID_total;
///////////////////////////////////////////////////////



void setup() {
  //analogReference(EXTERNAL);
  Serial.begin(9600);  
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(125); //Put the servco at angle 125, so the balance is in the middle
  pinMode(Analog_in,INPUT);  
  time = millis();
}

void loop() {
  if (millis() > time+period)
  {
    time = millis();    
    distance = get_dist(100);   
    distance_error = distance_setpoint - distance;   
    PID_p = kp * distance_error;
    float dist_diference = distance_error - distance_previous_error;     
    PID_d = kd*((distance_error - distance_previous_error)/period);
      
    if(-3 < distance_error && distance_error < 3)
    {
      PID_i = PID_i + (ki * distance_error);
    }
    else
    {
      PID_i = 0;
    }
  
    PID_total = PID_p + PID_i + PID_d;  
    PID_total = map(PID_total, -150, 150, 0, 150);
  
    if(PID_total < 20){PID_total = 20;}
    if(PID_total > 160) {PID_total = 160; } 
  
    myservo.write(PID_total+30);  
    distance_previous_error = distance_error;
  }
}




float get_dist(int n)
{
  long sum=0;
  for(int i=0;i<n;i++)
  {
    sum=sum+analogRead(Analog_in);
  }  
  float adc=sum/n;
  //float volts = analogRead(adc)*0.0048828125;  // value from sensor * (5/1024)
  //float volts = sum*0.003222656;  // value from sensor * (3.3/1024) EXTERNAL analog refference

  float distance_cm = 17569.7 * pow(adc, -1.2062);
  //float distance_cm = 13*pow(volts, -1); 
  return(distance_cm);
}