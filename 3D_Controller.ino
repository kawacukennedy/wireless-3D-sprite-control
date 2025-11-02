#include <SoftwareSerial.h>
#include <Wire.h>
#include <MPU6050_tockn.h>

// Pin definitions
#define BT_KEY 9
#define BT_RX 10
#define BT_TX 11
#define JOY_X A0
#define JOY_Y A1

SoftwareSerial BTSerial(BT_RX, BT_TX); // Arduino ↔ HC-05/06
MPU6050 mpu(Wire);

void setup() {
  Serial.begin(9600);      // Serial Monitor for AT commands
  pinMode(BT_KEY, OUTPUT);
  
  // Enter AT mode for configuration
  digitalWrite(BT_KEY, HIGH);
  BTSerial.begin(38400); // AT mode baud rate
  delay(1000);
  
  Serial.println("HC-05 in AT mode. Send AT commands via Serial Monitor.");
  Serial.println("Example: AT+NAME=YourName");
  Serial.println("To exit AT mode, send 'EXIT' or reset Arduino.");
}

void loop() {
  static bool atMode = true;
  static String command = "";

  // --- Forward Serial Monitor commands to BT module ---
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      command.trim();
      if (command == "EXIT") {
        // Exit AT mode
        digitalWrite(BT_KEY, LOW);
        delay(1000);
        BTSerial.begin(9600); // Data mode baud rate
        Wire.begin();
        mpu.begin();
        mpu.calcGyroOffsets(true);
        Serial.println("Exited AT mode. Ready for data transmission.");
        atMode = false;
      } else {
        BTSerial.println(command); // send command to Bluetooth
      }
      command = "";
    } else {
      command += c;
      BTSerial.write(c); // send character to Bluetooth
    }
  }

  // --- Forward BT module responses to Serial Monitor ---
  if (BTSerial.available()) {
    char c = BTSerial.read();
    Serial.write(c); // show module response
  }

  // --- Read MPU6050 sensor and send to BT every 100ms (only in data mode) ---
  if (!atMode) {
    static unsigned long lastTime = 0;
    if (millis() - lastTime >= 100) {
      lastTime = millis();

      mpu.update();
      float accX = mpu.getAccX();
      float accY = mpu.getAccY();
      float accZ = mpu.getAccZ();
      float gyroX = mpu.getGyroX();
      float gyroY = mpu.getGyroY();
      float gyroZ = mpu.getGyroZ();

       // Send sensor data to BT module
       BTSerial.print(accX);
       BTSerial.print(",");
       BTSerial.print(accY);
       BTSerial.print(",");
       BTSerial.print(accZ);
       BTSerial.print(",");
       BTSerial.print(gyroX);
       BTSerial.print(",");
       BTSerial.print(gyroY);
       BTSerial.print(",");
       BTSerial.print(gyroZ);
       BTSerial.print(",");
       BTSerial.print(analogRead(JOY_X));
       BTSerial.print(",");
       BTSerial.println(analogRead(JOY_Y));
    }
  }
}
