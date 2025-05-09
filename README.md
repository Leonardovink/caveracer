
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

# **ORB SLAM3 Installation/Operation Guide**
The 3D mapping from a 2D image came from https://github.com/UZ-SLAMLab/ORB_SLAM3. If you want to install the software from skratch I recommend that you use a virtual environment of ubuntu. When installing I also recommend that you follow this guide on youtube: https://www.youtube.com/watch?v=HWm5KMOL2PY , since the installation is pure hell if you do not know what you are doing. It is also possible to install on other versions of ubuntu and without a virtual environment. The installation that I did was on ubuntu 22.04 without virtual environment, but for me that caused a lot of problems with package dependencies.

For the operation there is a run.txt which includes commands to run the software it is important to run the files in the ORB-SLAM3 folder in the cmd. The commands are in a certain order, the things that you need to run the program are Opencv2 folder, the pangolin folder and the boost folder. Then when you want to execute the software on your own footage it is important that you have a dataset folder in which you have a folder with all the images and the rgb.txt, I don't know why but the rgb.txt file is not the rgb values but it is set up as {timestamp_foto} {name_image.jpg}.
- 

---

Let me know if you'd like further customization!
