
# CaveRacer

CaveRacer is a snake-like robot designed for cave exploration. This robot can traverse rugged terrain and operate in environments where human access is limited. Follow the instructions below to control and monitor the robot.

---

## **Getting Started**

### **Connecting to the Robot**
1. **SSH into the Raspberry Pi:**
   Use the following command to connect to the Raspberry Pi controlling the robot:
   ```bash
   ssh -X username@<raspi_ip>
   ```
   Replace `<raspi_ip>` with the Raspberry Pi's IP address.  
   The default SSH password is:  
   ```
   CaveRacer
   ```

---

### **Running the Robot Software**
After logging in via SSH, follow these steps:

1. **Start the Robot's Control System:**
   Run the provided script:
   ```bash
   ./run.sh
   ```

2. **If the above doesn't work, start the individual components manually:**
   ```bash
   python3 gui.py &
   python3 video.py &
   ```

---

### **Viewing the Live Stream**
The robot provides a live video stream for monitoring its environment. To access the live stream:

1. Open a browser.
2. Navigate to:
   ```
   http://<raspi_ip>:8000
   ```
   Replace `<raspi_ip>` with the Raspberry Pi's IP address.

---

## **Troubleshooting**
- Ensure the Raspberry Pi is powered on and connected to the same network as your computer.
- If `./run.sh` doesn't execute, verify its permissions:
  ```bash
  chmod +x run.sh
  ```
- Confirm that Python 3 is installed on the Raspberry Pi.

---

## **License**
This project is licensed under [Your Preferred License]. See `LICENSE` for details.

---

Let me know if you'd like further customization!
