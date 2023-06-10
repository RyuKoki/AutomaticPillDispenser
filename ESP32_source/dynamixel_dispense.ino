#include <DynamixelUNO_Shield.h>
#include <SoftwareSerial.h>

SoftwareSerial esp32(23, 19);
SoftwareSerial SoftSerial(16, 17);

// initialize variables
int  degree_position    = 0;
int  degree             = 0;
char angle_str[10]; 
char Input_data; 
int  idx                = 0; 
int  state              = 0;
int  encoder_angle      = 0;
int  encoder_angle_data = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // pinMode(13, INPUT);
  // pinMode(12, OUTPUT);
  esp32.begin(9600);
  // :param => long baud_rate
  Dynamixel.begin(9600);
  // :params => (unsigned char ID, int Position)
  Dynamixel.move(2, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (esp32.available() > 0) {
    // String d = esp32.read('\n');
    // Serial.println(d);
    Input_data = esp32.read();
    if (Input_data == ':') {
      // check start angle number
      state = 1;
    } else if (Input_data == 0x0A) {
      // check ending angle number
      state = 2;
    }
    if (state == 1) {
      // the state for keeping some characters data
      angle_str[idx] = Input_data;
      idx++;
    } else if (state == 2) {
      // the state for converting angle
      String angle = angle_str;
      angle = angle.substring(1, idx);
      encoder_angle = angle.toInt();
      // reset state 
      state = 0;
      idx = 0;
      delay(200);
      // mapping for degree postion
      degree_position = map(encoder_angle, 0, 360, 4095, 0);
      // moving to goal position
      Dynamixel.move(2, degree_position);
      // Dynamixel.moveSpeed(2, degree_position, 1023);
      Serial.print("position degree = ");
      Serial.println(encoder_angle);
      delay(200);
    }
  }
}
