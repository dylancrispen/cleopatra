***Dependencies***

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

***Git basics (Linux)***
Must navigate to root directory (contains cleopatra folder) before any of these commands

-copy repository to current (root) directory
git clone https://github.com/dylancrispen/cleopatra.git

-make changes
git add <file_name>
git commit -m "Always write a brief message explaining the commit."
git push

-pull changes from other branches into yours
git pull origin <pull_branch>

-view a log of commits on this branch
git log

-rollback changes
git reset --hard <commit_name> #get <commit_name> from calling git log



***Branching***
#Note: This was written by memory, for more (better) info check out the following:
#https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging

Helpful Commands
-create new branch
git branch <branch_name>

-start working on that branch
git checkout <branch_name>

-merge branch back into <develop>
git checkout <develop> #First have to switch to the branch you want to merge into
git merge <branch_name> #Then merge the branch

-pull changes from other branches into yours
git pull origin <develop>

-delete the branch when you're done with it
git push --delete <develop> <branch_name> #pushes all remaining changes to develop and deletes it remotely
git delete <branch_name> #deletes the local copy of the branch info


Branches Table

BRANCH_NAME	PURPOSE
master		Current official working build. The only branch that should commit to here is develop
develop		Current build in-progress. Make all changes/ branches off this branch.
readme		Changes to readme document only.
