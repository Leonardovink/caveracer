import tkinter as tk
import smbus

bus = smbus.SMBus(1)
# bus = 1
arduino_addresses = [0, 1, 2, 3, 4]

current_speed = 0
current_direction = "Stop"
selected_arduinos = [True] * 5 

def send_command(byte_value):
    for slave in arduino_addresses:
        if selected_arduinos[slave]:
            print(slave, byte_value)
            bus.write_byte(slave, byte_value)

# def update_values(list, value):
#     for slave in arduino_addresses:
#         if selected_arduinos[slave]:
#             list


# Function to handle speed button presses
def set_speed(speed):
    global current_speed
    current_speed = speed

    speed_to_byte = {
        0: 14,
        25: 15,
        50: 16,
        75: 17,
        100: 18
    }

    send_command(speed_to_byte[speed])
    speed_label.config(text=f"Speed: {current_speed}%")

def set_servo_position(position):
    global current_servo_position
    current_servo_position = position

    servo_pos_to_byte = {
        0: 0,
        45: 1,
        90: 2,
        135: 3,
        180: 4
    }

    send_command(servo_pos_to_byte[position])


# Function to handle keyboard inputs for driving
def key_press(event):
    global current_direction
    key = event.keysym.upper()

    if key == "W":
        current_direction = "Forward"
        send_command(10)
    elif key == "A":
        current_direction = "Left"
        send_command(13)
    elif key == "S":
        current_direction = "Backward"
        send_command(11)
    elif key == "D":
        current_direction = "Right"
        send_command(12)
    else:
        current_direction = "Stop"

    direction_label.config(text=f"Direction: {current_direction}")

# Function to toggle button selection
def toggle_button(index):
    selected_arduinos[index] = not selected_arduinos[index]  # Toggle state
    button = button_list[index]
    if selected_arduinos[index]:
        button.config(bg="green")
    else:
        button.config(bg="lightgray")

    # Optionally print the selected values
    print(f"Selected buttons: {selected_arduinos}")

# Create the main application window
root = tk.Tk()
root.title("Motor Control GUI")
root.geometry("400x300")

# Create a label for speed
speed_label = tk.Label(root, text="Speed: 0%", font=("Arial", 14))
speed_label.pack(pady=10)

# Create buttons for speed control
speed_frame = tk.Frame(root)
speed_frame.pack(pady=10)

speed_values = [0, 25, 50, 75, 100]

for value in speed_values:
    button = tk.Button(
        speed_frame,
        text=f"{value}%",
        width=5,
        command=lambda v=value: set_speed(v)  # Pass the speed value to the function
    )
    button.pack(side="left", padx=5)

# Create a label for direction display
direction_label = tk.Label(root, text="Direction: Stop", font=("Arial", 14))
direction_label.pack(pady=10)

servo_frame = tk.Frame(root)
servo_frame.pack(pady=10)

servo_positions = [0, 45, 90, 135, 180]
for position in servo_positions:
    button = tk.Button(
        servo_frame,
        text=f"{position}°",
        width=5,
        command=lambda p=position: set_servo_position(p)  # Pass the position value to the function
    )
    button.pack(side="left", padx=5)

# Create the selection buttons (0 to 5)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button_list = []
for i in range(6):
    button = tk.Button(
        button_frame,
        text=str(i),
        width=5,
        bg="green",
        command=lambda i=i: toggle_button(i)
    )
    button.pack(side="left", padx=5)
    button_list.append(button)

# Bind keyboard events
root.bind("<KeyPress>", key_press)

# Run the tkinter event loop
root.mainloop()
