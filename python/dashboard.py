import pygame
import serial
import math
import re
import sys
import time
from collections import deque

# ================= CONFIG =================

PORT = "COM3"  # CHANGE TO YOUR ARDUINO COM PORT
BAUD = 115200

WIDTH = 1200
HEIGHT = 760
FPS = 60

# ================= INITIALIZE =================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SmartLight V2 | Motion Dashboard")

clock = pygame.time.Clock()

font_title = pygame.font.SysFont("consolas", 32, bold=True)
font_large = pygame.font.SysFont("consolas", 26, bold=True)
font_medium = pygame.font.SysFont("consolas", 20)
font_small = pygame.font.SysFont("consolas", 15)

# ================= COLORS =================

BG = (12, 17, 28)
PANEL = (22, 30, 45)
BORDER = (55, 73, 95)

WHITE = (235, 242, 250)
MUTED = (135, 155, 175)

CYAN = (0, 220, 255)
GREEN = (0, 255, 145)
YELLOW = (255, 205, 65)
RED = (255, 80, 100)
BLUE = (80, 130, 255)

# ================= SENSOR DATA =================

pitch = 0.0
roll = 0.0
gyro_z = 0.0
accel = 1.0

brightness = 50
active_leds = 1

mode = "NORMAL"
lights_enabled = True

gesture = "NONE"
gesture_time = 0

# Graph history (180 samples)
pitch_history = deque([0.0] * 180, maxlen=180)
roll_history = deque([0.0] * 180, maxlen=180)

# Smooth visualization
smooth_pitch = 0.0
smooth_roll = 0.0

# ================= SERIAL =================

try:
    arduino = serial.Serial(PORT, BAUD, timeout=0)
    time.sleep(2)
    arduino.reset_input_buffer()
    connected = True

    print(f"Connected to Arduino on {PORT}")

except serial.SerialException as error:
    print(f"Connection failed: {error}")
    arduino = None
    connected = False

# ================= TEXT =================

def text(value, x, y, color=WHITE, font=font_medium):
    image = font.render(str(value), True, color)
    screen.blit(image, (x, y))


# ================= PANEL =================

def panel(x, y, w, h, title):
    pygame.draw.rect(
        screen, PANEL, (x, y, w, h), border_radius=12
    )

    pygame.draw.rect(
        screen, BORDER, (x, y, w, h), 2, border_radius=12
    )

    text(title, x + 20, y + 16, CYAN)


# ================= 3D ROTATION =================

def rotate_point(x, y, z, pitch_deg, roll_deg):
    p = math.radians(pitch_deg)
    r = math.radians(roll_deg)

    y2 = y * math.cos(p) - z * math.sin(p)
    z2 = y * math.sin(p) + z * math.cos(p)

    x3 = x * math.cos(r) + z2 * math.sin(r)
    z3 = -x * math.sin(r) + z2 * math.cos(r)

    return x3, y2, z3


def draw_motion_cube(cx, cy, pitch_angle, roll_angle):

    vertices = [
        (-1.5, -0.7, -0.25),
        (1.5, -0.7, -0.25),
        (1.5, 0.7, -0.25),
        (-1.5, 0.7, -0.25),

        (-1.5, -0.7, 0.25),
        (1.5, -0.7, 0.25),
        (1.5, 0.7, 0.25),
        (-1.5, 0.7, 0.25)
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    projected = []

    for vertex in vertices:
        x, y, z = rotate_point(
            *vertex, pitch_angle, roll_angle
        )

        scale = 95 / (4 + z)

        px = cx + x * scale * 3
        py = cy + y * scale * 3

        projected.append((int(px), int(py)))

    # Draw frame
    for start, end in edges:
        pygame.draw.line(
            screen,
            CYAN,
            projected[start],
            projected[end],
            3
        )

    # Front edge
    pygame.draw.line(
        screen,
        YELLOW,
        projected[0],
        projected[1],
        5
    )

    # Orientation marker
    pygame.draw.circle(
        screen,
        RED,
        projected[0],
        8
    )


# ================= LED DISPLAY =================

def draw_leds():
    panel(610, 100, 550, 180, "LED CONTROL")

    colors = [RED, YELLOW, GREEN, BLUE]

    for i in range(4):
        x = 690 + i * 125
        y = 190

        active = lights_enabled and i < active_leds

        color = colors[i] if active else (55, 65, 80)

        pygame.draw.circle(
            screen, color, (x, y), 30
        )

        pygame.draw.circle(
            screen,
            WHITE if active else BORDER,
            (x, y),
            34,
            2
        )

        text(
            f"LED {i + 1}",
            x - 28,
            y + 48,
            MUTED,
            font_small
        )


# ================= BRIGHTNESS =================

def draw_brightness():
    panel(610, 300, 550, 140, "BRIGHTNESS")

    bar_x = 640
    bar_y = 370
    bar_w = 470

    pygame.draw.rect(
        screen,
        (50, 60, 75),
        (bar_x, bar_y, bar_w, 25),
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            bar_x,
            bar_y,
            int(bar_w * brightness / 100),
            25
        ),
        border_radius=8
    )

    text(
        f"{brightness}%",
        1050,
        330,
        WHITE,
        font_large
    )


# ================= LIVE GRAPH =================

def draw_graph():
    panel(40, 470, 1120, 245, "LIVE MOTION GRAPH")

    graph_x = 70
    graph_y = 530
    graph_w = 1060
    graph_h = 155

    center_y = graph_y + graph_h // 2

    # Center line
    pygame.draw.line(
        screen,
        BORDER,
        (graph_x, center_y),
        (graph_x + graph_w, center_y)
    )

    # Grid
    for i in range(1, 5):
        y = graph_y + i * graph_h // 5

        pygame.draw.line(
            screen,
            (35, 45, 60),
            (graph_x, y),
            (graph_x + graph_w, y)
        )

    # Motion histories
    for history, color in [
        (pitch_history, CYAN),
        (roll_history, YELLOW)
    ]:

        points = []

        for i, value in enumerate(history):

            x = graph_x + i * graph_w / (len(history) - 1)

            # Increased sensitivity
            y = center_y - value * 1.5

            y = max(
                graph_y,
                min(graph_y + graph_h, y)
            )

            points.append(
                (int(x), int(y))
            )

        if len(points) > 1:
            pygame.draw.lines(
                screen,
                color,
                False,
                points,
                2
            )

    text("PITCH", 900, 490, CYAN, font_small)
    text("ROLL", 1010, 490, YELLOW, font_small)


# ================= SERIAL READER =================

pattern = re.compile(
    r"Pitch:\s*([-\d.]+)"
    r"\s*\|\s*Roll:\s*([-\d.]+)"
    r"\s*\|\s*Gyro Z:\s*([-\d.]+)"
    r"\s*\|\s*Accel:\s*([-\d.]+)g"
    r"\s*\|\s*Brightness:\s*(\d+)%"
    r"\s*\|\s*LEDs:\s*(\d+)/4"
    r"\s*\|\s*Mode:\s*(\w+)"
)


def read_serial():
    global pitch, roll, gyro_z, accel
    global brightness, active_leds, mode
    global gesture, gesture_time, lights_enabled

    if not connected:
        return

    # Read a limited number of messages per frame
    for _ in range(100):

        if not arduino.in_waiting:
            break

        try:
            line = arduino.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

        except serial.SerialException:
            return

        if line.startswith("GESTURE:"):
            gesture = line.replace(
                "GESTURE:", ""
            ).strip()

            gesture_time = time.time()

            if gesture == "LIGHTS OFF":
                lights_enabled = False

            elif gesture == "LIGHTS ON":
                lights_enabled = True

            continue

        match = pattern.search(line)

        if match:
            pitch = float(match.group(1))
            roll = float(match.group(2))
            gyro_z = float(match.group(3))
            accel = float(match.group(4))

            brightness = int(match.group(5))
            active_leds = int(match.group(6))

            mode = match.group(7)


# ================= MAIN LOOP =================

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    read_serial()

    # Smooth cube animation
    smooth_pitch += (pitch - smooth_pitch) * 0.30
    smooth_roll += (roll - smooth_roll) * 0.30

    # Scroll graph continuously at 60 FPS
    pitch_history.append(pitch)
    roll_history.append(roll)

    screen.fill(BG)

    # HEADER
    text(
        "SMARTLIGHT V2",
        40, 28, CYAN, font_title
    )

    text(
        "ADVANCED GESTURE CONTROL SYSTEM",
        380, 38, MUTED
    )

    text(
        "CONNECTED" if connected else "DISCONNECTED",
        980, 38,
        GREEN if connected else RED,
        font_small
    )

    # 3D MOTION PANEL
    panel(
        40, 100, 540, 340,
        "3D MOTION TRACKER"
    )

    draw_motion_cube(
        300,
        270,
        smooth_pitch,
        smooth_roll
    )

    text(
        f"PITCH: {pitch:.1f}°",
        70,
        385,
        CYAN
    )

    text(
        f"ROLL: {roll:.1f}°",
        320,
        385,
        YELLOW
    )

    # LED PANEL
    draw_leds()

    # BRIGHTNESS PANEL
    draw_brightness()

    # STATUS
    text(
        f"MODE: {mode}",
        640,
        455,
        GREEN,
        font_small
    )

    text(
        f"GYRO Z: {gyro_z:.1f} deg/s",
        870,
        455,
        MUTED,
        font_small
    )

    # GESTURE
    if time.time() - gesture_time < 2:
        text(
            f"GESTURE: {gesture}",
            380,
            75,
            YELLOW
        )

    # GRAPH
    draw_graph()

    pygame.display.flip()

# ================= CLEANUP =================

if arduino:
    arduino.close()

pygame.quit()
sys.exit()