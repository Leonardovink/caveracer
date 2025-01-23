#include <Wire.h>
#include <Servo.h>

int motor1pin1 = 2;
int motor1pin2 = 3;

int motor2pin1 = 4;
int motor2pin2 = 7;

int enaPin = 6; // ENA for motor 1
int enbPin = 5; // ENB for motor 2

int servoPin = 10;

int slave_address = 0; // Slave address

const int ledPin = 13;
int currentAngle = 90;

Servo myServo;

void setup() {
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(enaPin, OUTPUT);
  pinMode(enbPin, OUTPUT);

  Wire.begin(slave_address);
  myServo.attach(servoPin);

  setServo(90);

  Wire.onReceive(receiveData);
  delay(2000);
}

// Function to set motor speeds
void setSpeed(int speed) {
  analogWrite(enaPin, speed);
  analogWrite(enbPin, speed);
}

// Function to drive forward
void driveForward() {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}

// Function to drive backward
void driveBackward() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

// Function to drive left (rotate in place)
void driveLeft() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}

// Function to drive right (rotate in place)
void driveRight() {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

void driveStop() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void setServo(int targetAngle) {
  if (targetAngle > currentAngle) {
    for (int angle = currentAngle; angle <= targetAngle; angle++) {
      myServo.write(angle);
      delay(15); // Adjust delay for slower or faster movement
    }
  } else {
    for (int angle = currentAngle; angle >= targetAngle; angle--) {
      myServo.write(angle);
      delay(15); // Adjust delay for slower or faster movement
    }
  }
  currentAngle = targetAngle; // Update the current angle
}
void loop() {

}

// Function to handle incoming data from the Raspberry Pi
void receiveData(int byteCount) {
  if (Wire.available()) {
    byte command = Wire.read();  // Read the command byte

    switch (command) {
      case 0:  // Set servo 0 degrees
        digitalWrite(ledPin, HIGH);
        setServo(0);
        break;
      
      case 1: // Set servo 45 degrees
        setServo(45);

      case 2:  // Set servo 90 degrees
        setServo(90);
        break;

      case 3: // Set servo 135 degrees
        setServo(135);
        break;

      case 4:  // Set servo 180 degrees
        setServo(180);
        break;

      case 9: // Stop
        driveStop();
        break;

      case 10:  // Drive forward
        driveForward();
        break;
      
      case 11: // Drive backward
        driveBackward();
        break;
      
      case 12: // Turn right
        driveRight();
        break;

      case 13: // Turn left
        driveLeft();
        break;

      case 14: //set speed 0%
        setSpeed(0);
        break;
      
      case 15: //set speed 25%
        setSpeed(64);
        break;
      
      case 16: //set speed 50%
        setSpeed(128);
        break;

      case 17: //set speed 75%
        setSpeed(192);
        break;

      case 18: //set speed 100%
        setSpeed(256);
        break;

      default:  // Handle unknown commands
        Serial.println("Unknown command received");
        break;
    }
  }
}
