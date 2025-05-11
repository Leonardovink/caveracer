
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
### **Connecting the robot to wifi**
1. **Connect to uva network with the raspberry by filling in credentials**
2. **Delete password after being finished with the project, the previous group did not do this but it is unsafe to just leave your uva login in a shared space**
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
   ⚠️ **Look out!** When running `video.py`, it starts making screenshots of the footage at 15 FPS, which can fill up memory quickly. Consider commenting out the screenshot code before running it.

   
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

## ORB-SLAM3: 3D Mapping from a 2D Image

The 3D mapping from a 2D image comes from [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3).

If you want to install the software from scratch, I recommend using a **virtual environment of Ubuntu**. When installing, I also recommend to follow this guide on YouTube since the documentation on original github in my opinion was lacking:  
https://www.youtube.com/watch?v=HWm5KMOL2PY

> ⚠️ The installation is **pure hell**. If you do not know exactly what you are doing I recommend you to follow the youtube guide step by step.

It is possible to install ORB SLAM 3 on a lot of different versions of Ubuntu and without a virtual environment.+  
The type of installation I did was on **Ubuntu 22.04 without a virtual environment**, but I really recommend you not to do this because this caused a lot of problems with **package dependencies**, because ubuntu 22.04 was too new for some packages.

---

## **Operation**

For running the software, there is a `run.txt` file that includes commands to execute the system that you can copy into the cmd.  
It is important to run the commands from within the **`ORB_SLAM3/` folder**.

Ultimately, the necessary folders/files to run the program are:

- `Opencv2 version 4.7.0/` http://opencv.org. Required at least 3.0. Documentation was Tested with OpenCV 3.2.0 and 4.4.0.
- `Pangolin version 0_8/` https://github.com/stevenlovegrove/Pangolin
- `boost version 1_78_0/` Not Required, but the youtube video used it so I also used it.
- `eigen3/` Required by g2o. Download and install instructions can be found at: http://eigen.tuxfamily.org. Required at least 3.1.0. I don't remember the exact version I used, but it should be in the youtube video.


> ❗ Note: The `rgb.txt` file is **not** a list of RGB values and if it is incorrectly formatted in my experience it will not work!!.  
> It is formatted as:
> ```
> name_image is normally a 6 number name, so 000001.jpg etc etc
> {timestamp_foto} {name_image.jpg}

Another important file is the `camera.yaml` or in our case TUMMonoVO.yaml this is a settings file required for ORB-SLAM3 processing.

For a **monocular camera setup**, the settings are located at: ORB-SLAM3/Examples/Monocular/TUMMonoVO.yaml

This file includes:

- Extrinsic and intrinsic camera parameters
- Processing settings used by the software

To obtain the correct settings for your camera, a **calibration is needed**.  

## Camera Calibration Process Using a Checkerboard

Camera calibration is an essential step in the ORB-SLAM3 pipeline. It helps determine both the **intrinsic** and **extrinsic** parameters of the camera, which are crucial for accurate 3D mapping. The process also accounts for **lens distortion**, which must be corrected for the SLAM system to function optimally.

The process of camera calibration typically involves the following steps:

### 1. Prepare the Checkerboard Pattern
   
- A **checkerboard** pattern is used to perform the calibration.
- You can either print the checkerboard pattern on a sheet of paper or use physical checkerboard.
- The checkerboard should have a known grid size, for example:
  - 7x7 inner squares (this is the number of intersections in the grid, not the number of squares).
  - Each square might be 25mm x 25mm (but you can scale it to any size).

### 2. Capture Calibration Images

- Use the camera you're calibrating to take several **images** of the checkerboard.
- The images should cover a range of angles and distances from the camera to ensure accurate calibration.
- For best results:
  - Take pictures from **different distances**.
  - Vary the **angle** of the camera (e.g., front, side, and tilted).
  - Ensure that the checkerboard occupies a significant portion of the image but doesn't need to take up the whole frame.

> **Note:** It's recommended to capture around 10-20 images with different angles for better accuracy.

### 3. Extract the Corners of the Checkerboard

- Use a calibration tool (like OpenCV) to **detect the corners** of the checkerboard in each image code can be found online it is used a lot.
- This is done by identifying the **intersections** of the black-and-white squares.
- OpenCV’s `findChessboardCorners()` function can automatically detect these corners in the images if the checkerboard is visible.

> **Tip:** If the corners aren't detected correctly, try adjusting the lighting or focus on the checkerboard.

### 4. Calibrate the Camera Using OpenCV (optional you could use other ways)

After capturing the images and extracting the corners, you can proceed with camera calibration using OpenCV.

- OpenCV provides the function `cv2.calibrateCamera()` to calculate the intrinsic and extrinsic parameters of the camera.
  
#### 4.1 Input to `cv2.calibrateCamera()`
You need two sets of data for calibration:
- **Object points**: These are the known 3D coordinates of the checkerboard corners in the world. Since the checkerboard is flat, the Z-coordinate is typically set to 0.
  - For example, if the checkerboard squares are 25mm x 25mm, the object points will look like:
    ```
    (0, 0, 0), (25, 0, 0), (50, 0, 0), ..., (0, 25, 0), (25, 25, 0), ...
    ```
- **Image points**: These are the detected 2D coordinates of the checkerboard corners in the image space.
  - These points are extracted automatically by OpenCV.

#### 4.2 Output from `cv2.calibrateCamera()`
The calibration function outputs several parameters:
- **Camera Matrix (Intrinsic Parameters)**:
  - Focal length (`fx`, `fy`)
  - Optical center (`cx`, `cy`)
  - Skew factor (usually zero)

- **Distortion Coefficients**:
These coefficients are necessary to correct lens distortion. Common distortion parameters include:
- `k1`, `k2`: Radial distortion coefficients.
- `p1`, `p2`: Tangential distortion coefficients.
- `k3`: Higher-order radial distortion (optional).
---

