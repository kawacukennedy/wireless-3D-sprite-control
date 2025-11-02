# 3D Embedded Game Controller

Control a 3D character in a simple game using an Arduino with joystick, MPU6050 IMU, and HC-05 Bluetooth module.

## Hardware Requirements

- Arduino board (e.g., Uno)
- MPU6050 IMU sensor
- HC-05 Bluetooth module
- Analog Joystick
- Connecting wires

## Wiring

- MPU6050 SDA: A4
- MPU6050 SCL: A5
- HC-05 RX: Pin 10
- HC-05 TX: Pin 11
- Joystick X: A0
- Joystick Y: A1
- Joystick VCC: 5V
- Joystick GND: GND

## Software Setup

### Arduino

1. Install Arduino IDE.
2. Install MPU6050_tockn library via Library Manager.
3. Open `3D_Controller.ino` and upload to Arduino.

### Python Game

1. Ensure Python 3 is installed.
2. Run `./install_deps.sh` to create virtual environment and install dependencies (pyserial, vpython).
3. Activate venv: `source venv/bin/activate`
4. Run: `python3 3D_Character_Controller.py --port YOUR_PORT` (replace YOUR_PORT with your Bluetooth serial port, e.g., `/dev/tty.HC-05` on Mac/Linux or COM3 on Windows).

## Device Connections

### Hardware Connections

Connect components to Arduino as follows:

- **MPU6050**:
  - VCC to 5V
  - GND to GND
  - SDA to A4
  - SCL to A5

- **HC-05**:
  - VCC to 5V
  - GND to GND
  - RX to Pin 10 (via voltage divider if needed, 5V to 3.3V)
  - TX to Pin 11
  - KEY/EN to Pin 9

Power Arduino via USB or external power.

### Bluetooth Connection

1. Upload Arduino code; HC-05 enters AT configuration mode on startup.
2. Open Serial Monitor at 9600 baud.
3. Send AT commands to configure HC-05 (e.g., AT+NAME=YourName, AT+PSWD=1234, AT+UART=9600,0,0).
4. Send "EXIT" to exit AT mode and start data transmission.
5. HC-05 should blink fast (data mode).
6. On receiving device, enable Bluetooth and search for devices.
7. Pair with configured name (password as set).
8. Once paired, it appears as a serial port (e.g., COM3 on Windows, /dev/tty.YourName on Mac).
9. Update the port in `3D_Character_Controller.py`.

## Game Controls

- **MPU6050 Accel**: Move character X/Y position.
- **MPU6050 Gyro**: Rotate character.
- **Joystick Y**: Control character Z position.

## Game Mechanics

- Collect green spheres to increase score.
- Avoid red spheres (obstacles) to prevent losing lives.
- 3 lives; game over when lives reach 0.
- High score saved to `high_score.txt`.
- Game resets automatically on game over.

## Architecture

The system consists of two main components:

- **Arduino (3D_Controller.ino)**: Reads sensor data from MPU6050 IMU and sends it via Bluetooth using HC-05 module.
- **Python Game (3D_Character_Controller.py)**: Receives sensor data over serial (Bluetooth) and updates a 3D scene using VPython.

Data flow: MPU6050 -> Arduino -> HC-05 Bluetooth -> Serial Port -> Python -> VPython 3D Rendering.

## Code Explanation

### Arduino Code

- Initializes HC-05 in AT mode for configuration.
- After exiting AT mode, reads MPU6050 accelerometer and gyroscope data, and joystick X/Y every 100ms.
- Sends comma-separated values: accX,accY,accZ,gyroX,gyroY,gyroZ,joyX,joyY over Bluetooth.

### Python Code

- Connects to serial port (Bluetooth).
- Parses incoming data and maps accelerometer to character X/Y position, gyroscope to rotation, joystick Y to Z position.
- Handles game logic: collecting targets, avoiding obstacles, scoring, lives.

## Troubleshooting

- **Serial Port Issues**: Ensure Bluetooth is paired and the port is correct. On Windows, check Device Manager; on Mac/Linux, use `ls /dev/tty.*` or similar.
- **No Data Received**: Verify HC-05 is in data mode (fast blinking). Check wiring and power.
- **Sensor Calibration**: If movements are off, recalibrate MPU6050 by resetting Arduino.
- **VPython Rendering**: May require graphics drivers. On some systems, run with `python3 -m vpython` or install additional packages.
- **Game Not Starting**: Ensure virtual environment is activated and dependencies are installed.
- **High Score Not Saving**: Check write permissions for `high_score.txt`.