Git basics
**Must navigate to root directory (contains cleopatra folder) before any of these commands**

Copy repository to current (root) directory
git clone https://github.com/dylancrispen/cleopatra.git





Steps for installing dependencies:
- Opencv: 
expand file system
Sudo pip3 install opencv-python
Sudo pip3 install opencv-contrib-python
- Install imutils: (note: Pizero can’t use imutils.resize)
pip3 install imutils
- Reinstall numpy
cd /home/pi/.local/lib/python3.5/site-packages/
rm -r numpy
rm -r numpy(tab)
pip3 install numpy==1.12.1
- Install packages:
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
sudo apt-get install libv4l-dev
sudo apt-get install libhdf5-dev
sudo pip3 install Adafruit_PCA9685 OR sudo apt-get install pigpio
- Enable:
Camera, I2C, SSH

- Make sure to run:
sudo pigpiod (if using pigpio)
sudo modprobe bcm2835-v4l2 (note it's V4L2 not V412)


Turn off xinit (Desktop GUI) for better quality