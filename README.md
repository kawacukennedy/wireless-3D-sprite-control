# 3D Embedded Game Controller

Control a 3D character in a simple game using an Arduino with joystick, MPU6050 IMU, and HC-05 Bluetooth module.

## Hardware Requirements

- Arduino board (e.g., Uno)
- MPU6050 IMU sensor
- HC-05 Bluetooth module
- Connecting wires

## Wiring

- MPU6050 SDA: A4
- MPU6050 SCL: A5
- HC-05 RX: Pin 10
- HC-05 TX: Pin 11

## Software Setup

### Arduino

1. Install Arduino IDE.
2. Install MPU6050_tockn library via Library Manager.
3. Open `3D_Controller.ino` and upload to Arduino.

### Python Game

1. Ensure Python 3 is installed.
2. Run `./install_deps.sh` to create virtual environment and install dependencies (pyserial, vpython).
3. Activate venv: `source venv/bin/activate`
4. Update `COM3` in `3D_Character_Controller.py` to your Bluetooth serial port (e.g., `/dev/tty.HC-05` on Mac/Linux).
5. Run: `python3 3D_Character_Controller.py`

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

- **MPU6050 Accel**: Move character position.
- **MPU6050 Gyro**: Rotate character.

## Game Mechanics

- Collect green spheres to increase score.
- Avoid red spheres (obstacles) to prevent losing lives.
- 3 lives; game over when lives reach 0.
- High score saved to `high_score.txt`.
- Game resets automatically on game over.

## Troubleshooting

- Ensure Bluetooth is paired and port is correct.
- Check sensor calibrations if movements are off.
- Vpython may require graphics drivers for 3D rendering.