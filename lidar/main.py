import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar
import tkinter as tk
from tkinter import ttk
import asyncio
import car_controller as cc  # Import car controller module

# Global variables
PORT_NAME = 'COM4'  # Update with your actual LiDAR port
SAFE_DISTANCE = 1000  # Initial safe distance in millimeters
ANGLE_RANGE = 20  # Initial angle range for obstacle detection (±20° ahead)
latest_scan = []  # To store the latest scan data
running = False  # Flag to control start/stop state
direction = "forward"

async def find_clear_path():
    """Find the most open direction when an obstacle is ahead."""
    global latest_scan, direction
    left_distances = []
    right_distances = []

    # Group distances based on angle (left or right of the car's forward direction)
    for quality, angle, distance in latest_scan:
        if 20 < angle < 90:  # Right side
            right_distances.append(distance)
        elif 270 < angle < 340:  # Left side
            left_distances.append(distance)

    avg_left = np.mean(left_distances) if left_distances else 0
    avg_right = np.mean(right_distances) if right_distances else 0

    if avg_left > avg_right:
        await cc.left_async()
        direction = "left"
    else:
        await cc.right_async()
        direction = "right"

def visualize_scan():
    """Visualize the scan data and the obstacle zone."""
    global direction, latest_scan
    plt.clf()
    angles = np.radians([meas[1] for meas in latest_scan])
    distances = [meas[2] for meas in latest_scan]
    
    # add the direction of the car in the legend
    plt.text(0, 0, f"Direction: {direction}", fontsize=12, ha='center')

    # Plot scan data
    plt.polar(angles, distances, 'go', markersize=2, label="Obstacles")

    forward_angles = np.radians([-ANGLE_RANGE, ANGLE_RANGE])
    plt.fill_between(forward_angles, 0, SAFE_DISTANCE, color='red', alpha=0.3, label="Obstacle Zone")
    plt.title("Lidar Scan with Obstacle Avoidance")
    plt.legend(loc="upper right")
    plt.pause(0.01)

async def lidar_scan_loop():
    """Continuously scan with LiDAR and update the latest scan data."""
    global running, lidar, latest_scan
    try:
        lidar = RPLidar(PORT_NAME)
        for scan in lidar.iter_scans():
            if not running:
                break
            latest_scan = scan  # Update the global scan data for other tasks
            visualize_scan()
            await asyncio.sleep(0.05)  # Short delay to prevent overload
    finally:
        lidar.stop()
        lidar.disconnect()

async def movement_control():
    """Separate movement control task that decides turns based on latest scan."""
    global running, direction
    while running:
        # Check if obstacle detected within the forward range
        forward_obstacle = any(
            (-ANGLE_RANGE < angle < ANGLE_RANGE) and (distance < SAFE_DISTANCE)
            for _, angle, distance in latest_scan
        )

        if forward_obstacle:
            print("Obstacle detected! Finding a clear path...")
            await find_clear_path()  # Perform left or right turn based on clearance
        else:
            print("Path is clear. Moving forward.")
            await cc.forward_async()
            direction = "forward"

        await asyncio.sleep(0.1)  # Adjust delay as needed

async def main_tasks():
    """Gather all async tasks."""
    await asyncio.gather(lidar_scan_loop(), movement_control())

def start():
    """Start both lidar scanning and movement control tasks."""
    global running
    running = True
    asyncio.run(main_tasks())  # Run main_tasks coroutine

def stop():
    """Stop all tasks and reset car."""
    global running
    running = False
    asyncio.run(cc.reset_async())

def update_safe_distance(val):
    """Update the SAFE_DISTANCE based on GUI slider."""
    global SAFE_DISTANCE
    SAFE_DISTANCE = int(val)

def update_angle_range(val):
    """Update the ANGLE_RANGE based on GUI slider."""
    global ANGLE_RANGE
    ANGLE_RANGE = int(val)

# GUI Setup
root = tk.Tk()
root.title("Obstacle Avoidance Control Panel")

# Safe distance slider
ttk.Label(root, text="Safe Distance (mm)").grid(row=0, column=0, padx=10, pady=5)
safe_distance_slider = tk.Scale(root, from_=500, to=2000, orient='horizontal', command=update_safe_distance)
safe_distance_slider.set(SAFE_DISTANCE)
safe_distance_slider.grid(row=0, column=1, padx=10, pady=5)

# Angle range slider
ttk.Label(root, text="Angle Range (degrees)").grid(row=1, column=0, padx=10, pady=5)
angle_range_slider = tk.Scale(root, from_=10, to=90, orient='horizontal', command=update_angle_range)
angle_range_slider.set(ANGLE_RANGE)
angle_range_slider.grid(row=1, column=1, padx=10, pady=5)

# Start and Stop buttons
start_button = ttk.Button(root, text="Start", command=start)
start_button.grid(row=2, column=0, padx=10, pady=5)
stop_button = ttk.Button(root, text="Stop", command=stop)
stop_button.grid(row=2, column=1, padx=10, pady=5)

root.mainloop()
