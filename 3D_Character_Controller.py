import serial
import time
import random
import argparse
from vpython import *

parser = argparse.ArgumentParser(description='3D Character Controller Game')
parser.add_argument('--port', default='COM3', help='Serial port for Bluetooth connection (e.g., COM3, /dev/tty.HC-05)')
args = parser.parse_args()

try:
    ser = serial.Serial(args.port, 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port {args.port}: {e}")
    exit(1)

scene = canvas(title='3D Character Game')

character = box(pos=vector(0, 0, 0), size=vector(1, 2, 1), color=color.blue)

# Targets to collect
targets = []
for i in range(5):
    targets.append(sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.3, color=color.green))

# Obstacles to avoid
obstacles = []
for i in range(3):
    obstacles.append(sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.4, color=color.red))

# Labels
acc_label = label(pos=vector(-7, 6, 0), text='Accel: 0, 0, 0', height=10, color=color.white)
gyro_label = label(pos=vector(-7, 5, 0), text='Gyro: 0, 0, 0', height=10, color=color.white)
joy_label = label(pos=vector(-7, 4, 0), text='Joy: 0, 0', height=10, color=color.white)
score_label = label(pos=vector(-7, 3, 0), text='Score: 0', height=10, color=color.yellow)
lives_label = label(pos=vector(-7, 2, 0), text='Lives: 3', height=10, color=color.red)
game_over_label = label(pos=vector(0, 0, 2), text='', height=20, color=color.red, visible=False)

score = 0
lives = 3
high_score = 0
try:
    with open('high_score.txt', 'r') as f:
        high_score = int(f.read())
except:
    pass

last_button = 0
game_over = False

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            data = line.split(',')
            if len(data) == 8:
                try:
                    accX = float(data[0])
                    accY = float(data[1])
                    accZ = float(data[2])
                    gyroX = float(data[3])
                    gyroY = float(data[4])
                    gyroZ = float(data[5])
                    joyX = int(data[6])
                    joyY = int(data[7])
                except ValueError:
                    print("Invalid data received, skipping...")
                    continue

                if not game_over:
                    # Update labels
                    acc_label.text = f'Acc: {accX:.2f}, {accY:.2f}, {accZ:.2f}'
                    gyro_label.text = f'Gyro: {gyroX:.2f}, {gyroY:.2f}, {gyroZ:.2f}'
                    joy_label.text = f'Joy: {joyX}, {joyY}'
                    score_label.text = f'Score: {score}'
                    lives_label.text = f'Lives: {lives}'

                    # Map accelerometer to character position
                    x_pos = accX * 2
                    y_pos = accY * 2
                    z_pos = (joyY - 512) / 512.0 * 5  # Map joystick Y to Z position (-5 to 5)
                    character.pos = vector(x_pos, y_pos, z_pos)

                    # Map gyroscope to character rotation
                    character.rotate(angle=gyroX * 0.01, axis=vector(1, 0, 0))
                    character.rotate(angle=gyroY * 0.01, axis=vector(0, 1, 0))
                    character.rotate(angle=gyroZ * 0.01, axis=vector(0, 0, 1))

                    # Check for collisions with targets
                    for target in targets[:]:
                        if mag(character.pos - target.pos) < 1.5:
                            targets.remove(target)
                            target.visible = False
                            score += 1
                            # Add new target
                            targets.append(sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0), radius=0.3, color=color.green))

                    # Check for collisions with obstacles
                    for obstacle in obstacles[:]:
                        if mag(character.pos - obstacle.pos) < 1.5:
                            lives -= 1
                            if lives <= 0:
                                game_over = True
                                game_over_label.text = f'Game Over! Score: {score}\nHigh Score: {max(score, high_score)}'
                                game_over_label.visible = True
                                with open('high_score.txt', 'w') as f:
                                    f.write(str(max(score, high_score)))
                            else:
                                # Reset position
                                character.pos = vector(0, 0, 0)
                                break

    except Exception as e:
        print(f"Error: {e}")
        break

    time.sleep(0.1)