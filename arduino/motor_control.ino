// Phase 1-4 Arduino Motor Controller
// Receives serial commands like: L120 R120
// L = left motor speed, R = right motor speed
// Range: -255 to 255

const int ENA = 10;
const int IN1 = 9;
const int IN2 = 8;

const int ENB = 5;
const int IN3 = 7;
const int IN4 = 6;

String inputString = "";

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();
  Serial.println("Arduino motor controller ready");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      processCommand(inputString);
      inputString = "";
    } else {
      inputString += c;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();

  int lIndex = cmd.indexOf('L');
  int rIndex = cmd.indexOf('R');

  if (lIndex == -1 || rIndex == -1) {
    Serial.println("Invalid command");
    return;
  }

  int leftSpeed = cmd.substring(lIndex + 1, rIndex).toInt();
  int rightSpeed = cmd.substring(rIndex + 1).toInt();

  leftSpeed = constrain(leftSpeed, -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  setMotor(ENA, IN1, IN2, leftSpeed);
  setMotor(ENB, IN3, IN4, rightSpeed);

  Serial.print("OK L");
  Serial.print(leftSpeed);
  Serial.print(" R");
  Serial.println(rightSpeed);
}

void setMotor(int enPin, int inA, int inB, int speedVal) {
  if (speedVal > 0) {
    digitalWrite(inA, HIGH);
    digitalWrite(inB, LOW);
    analogWrite(enPin, speedVal);
  } else if (speedVal < 0) {
    digitalWrite(inA, LOW);
    digitalWrite(inB, HIGH);
    analogWrite(enPin, abs(speedVal));
  } else {
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
    analogWrite(enPin, 0);
  }
}

void stopMotors() {
  setMotor(ENA, IN1, IN2, 0);
  setMotor(ENB, IN3, IN4, 0);
}
