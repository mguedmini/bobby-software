#include <SoftwareSerial.h>
#include <Servo.h>
int enA = 10;//right motor (robot's right)
int in1 = 9;
int in2 = 8;

int enB = 5;//left motor (robot's left)
int in3 = 7;
int in4 = 6;


int bluepin = A1; //define RGB LED pins
int redpin = A2;
int greenpin = A3;

int forward_speed = 250; //change speed here, can range from 0 to 255.
int backward_speed = 150;

int ear_servo_min_position = 70;
int ear_servo_max_position = 105;

Servo servo1;
Servo servo2;

int incomingByte = '*';

void setup()
{
  RGB(255, 0, 255); //blue

  Serial.begin(9600); //Use serial monitor at 9600 for debugging and controlling from computer

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(11, OUTPUT);

  servo1.attach(A4);
  servo2.attach(A5);
}


void left()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);

  analogWrite(enA, forward_speed);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(enB, forward_speed);
}

void right()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  analogWrite(enA, forward_speed);

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enB, forward_speed);
}

void backward()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);

  analogWrite(enA, backward_speed);

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enB, backward_speed);
}

void forward()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  analogWrite(enA, forward_speed);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(enB, forward_speed);
}

void stop()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}


void wiggleears()
{
  for (int i = ear_servo_min_position; i <= ear_servo_max_position; i++) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
  for (int i = ear_servo_max_position; i >= ear_servo_min_position; i--) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
  for (int i = ear_servo_min_position; i <= ear_servo_max_position; i++) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
  for (int i = ear_servo_max_position; i >= ear_servo_min_position; i--) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
  for (int i = ear_servo_min_position; i <= ear_servo_max_position; i++) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
  for (int i = ear_servo_max_position; i >= ear_servo_min_position; i--) {
    servo1.write(i);
    servo2.write(i);
    delay(10);
  }
}

void RGB (int R, int G, int B) {
  analogWrite(redpin, R);
  analogWrite(greenpin, G);
  analogWrite(bluepin, B);
}

void loop()
{
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
  }

  switch (incomingByte)
  {
    case 'S':
      {
        stop();
        Serial.println("Stop\n");
        incomingByte = '*';
      }
      break;

    case 'F':
      {
        forward();
        Serial.println("Forward\n");
        incomingByte = '*';
      }
      break;

    case 'B':
      {
        backward();
        Serial.println("Backward\n");
        incomingByte = '*';
      }
      break;

    case 'R':
      {
        right();
        Serial.println("Rotate Right\n");
        incomingByte = '*';
      }
      break;

    case 'L':
      {
        left();
        Serial.println("Rotate Left\n");
        incomingByte = '*';
      }
      break;

    case 'W':
      {
        RGB(255, 0, 0); //red
        Serial.println("Red eyes");
        incomingByte = '*';
      }
      break;

    case 'V':
      {
        RGB(0, 255, 0); //green
        Serial.println("Green eyes");
        incomingByte = '*';
      }
      break;

    case 'Y':
      {
        wiggleears();
        Serial.println("Ear yoga");
        incomingByte = '*';
      }
      break;
  }
}
