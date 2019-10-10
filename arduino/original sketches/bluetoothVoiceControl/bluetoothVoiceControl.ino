
#include <SoftwareSerial.h> 

String command;
int incomingByte = 0;  


int enA = 10;//robot's right motor 
int in1 = 9;
int in2 = 8;

int enB = 5;//robot's left motor
int in3 = 7;
int in4 = 6;

      
int bluepin=A1;//RGB LED pins      
int redpin=A2;    
int greenpin=A3;   
   

void stop()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void forward()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  
  analogWrite(enA, 150);//change speeds here 0-255

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enB, 150);//change speeds here 0-255

  delay(500);//change delay value here to go more forward or less forward
  stop();
}


void backward()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
 
  analogWrite(enA, 150);//change speeds here 0-255

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(enB,150);//change speeds here 0-255

  delay(500);
  stop();
}

void right()
{

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  analogWrite(enA, 230);//change speeds here 0-255

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  analogWrite(enB, 230);//change speeds here 0-255
  delay(1000);
  stop();
}

void RGB (int R, int G, int B){

    analogWrite(redpin,R);
    analogWrite(greenpin,G);
    analogWrite(bluepin,B);
}

void setup() {
  RGB(0,0,255); //blue
  Serial.begin(9600);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT); 
}

void loop() {
  while (Serial.available()){ 
  delay(10); 
  char instruction = Serial.read(); 
  if (instruction == '#') {
    break;
    } 
  command = command + instruction; 
  } 

  
  if (command.length() > 0) {
    Serial.println(command);
       if (command == "*forward") {
              forward();
        }  else if (command == "*backward"){
          backward();
          } else if (command == "*turn"){
            right();
          } else if (command == "*red"){
          RGB(255,0,0);
          } else if (command == "*green"){
            RGB(0,255,0);
          } else if (command == "*blue"){
            RGB(0,0,255);
          } 

          

command ="";  
  }

} 
