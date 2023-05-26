# Pico W LED Demo
The contents of this folder enable a simple web page offering the ability to turn LED's on or off. The page is served by a small server called [microdot](), which was written for [MicroPython](), running on a Pico W. It is intended to serve as a simple example as to how to develop a user-facing webpage running on the Pico W.

There are three different versions, *_v1*, *_v2* and *_v3*. With each version is:
* *webserver_vn.py* - contains the code which runs as main.py on the Pico.
* *index_vn.py* - contains the web page code and needs to be copied to *template/index.html* on the Pico.

To view each version:
1. Copy the desired *webserver_vn.py* to main.py, you can make this automatic by changing the value n in the file *files.txt* so that it copies the desired version.
2. Duplicate the matching version of *index_vn.html* to *index.html* and mpbuild will copy appropriately.
3. Run mpbuild.py to load the Pico. See "Automation..." below for more information.

## Additional Files Required
### secrets.py
This file contains the SSID and password of your desired wireless LAN connection:
```python
ssid = 'Demo'
password = 'mpc1234!'
```
A simple text file called *secrets.py* with the above format and the correct SSID and password is required. It sits at the root folder along with the other files such as wlan.py.
## Installation
1. Copy the folder to your PC
To run on a Pico W:
```bash
# ensure secrets.py has the desired SSID and password for your WiFi
# Apply the version instructions above then
mpbuild -e
# start a serial program (see Note below)
# press Reset or cycle power on your Pico W
# Use the IP address provided via the serial port
# Browse to IP address:5001 to play game (not 0.0.0.0 as stated)
```

## Resolving Connection Errors with Pico W
Sometimes it is difficult to connect to the Pico W, here is some background and hints how to resolve issues.

When the Pico W resets, it will attempt to connect to the SSID using the information in *secrets.py*. The built-in LED will blink slowly when this is in progress. If a wireless connection is made, the LED will turn off and the program will print the following information:
```
Name: Pico W B
IP Address: 10.0.1.12
MAC Address: 28:cd:c1:08:a9:7d
Channel: 1
SSID: Demo
TX Power: 31
Starting sync server on 0.0.0.0:5001...
```
It is also critical the device (phone or PC) which are using to connect with the Pico is on the same network as well. **Be sure you are connected to the same SSID.**

The address you enter in your browser is a combination of the addresses supplied above. Use the **IP Address** combined with the *port number* following the *0.0.0.0* as in *:5001*. Using the above data, you would need to go to this address:
```
http://10.0.1.12:5001
```

If the wireless connection can not be made, the LED will blink at a faster rate and a error will be printed via the serial port as in:
```
Connection failed: LINK_BADAUTH
Starting sync server on 0.0.0.0:5001...
```
In this case, the password was in-correct, resulting in a *BADAUTH* or *bad authorization* error. The following line *Starting sync...* is irelevant as there isn't an IP address to connect.

## Serial Programs
I develop on a Mac and use a paid program called [Serial](https://www.decisivetactics.com/products/serial/). It is quite robust and is able to connect to everything I've attempted. That said, you might not want to pay for Serial (or have a Mac).

My second favorite "connect to everything" serial program is the serial monitor in the Arduino [Legacy IDE (1.8.X)](https://www.arduino.cc/en/software). I've found it is easy to configure AND it seems robust enough to connect to everything I'v attempted as well.

I've found several programs on the Mac which won't work with a Pico (*when it is re-booted...*):
* *cu* - a common, simple program which crashes when the Pico is rebooted
* *screen* - a ubiquitous, powerful screen program which doesn't seem to connect to the Pico after re-boot
* *minicom* - crashes when the Pico is rebooted
* *Thonny IDE* - loses serial connection when the Pico is rebooted

## Resetting the Pico
The *Pico W* doesn't have a reset button, which means there are two alternatives. First, power cycle the Pico by removing the USB cable or second, add a reset button. I find the second method preferable and have described the process [here](https://wellys.com/posts/rp2040_micropython_1/#reset).

## Program Size
This program hasn't been optimized for size as its a capability demo, not a production program. I have switched from bulma css framework (200K) to marx css frame work (10k).

## Automation to Copy Project to Board
The program *mpbuild* will copy all required program files to the board. The program uses *files.txt* to identify which files to copy based on the first character in the line:
* '*#*' - comment line, line is ignored
* '*/*' - directory, a mkdir is executed. This line must be before any files which need to be copied into the directory.
* '*+*' - main program file, it will be copied into *main.py* to execute upon reset
* No special characters (just the file name), file copied over to board

The program uses pyboard.py from mpremote (installed via pip), which means the PYBOARD_DEVICE environmental variable must be set. See [here](https://docs.micropython.org/en/latest/reference/pyboard.py.html#running-a-command-on-the-device).

## Tool to Erase Pico LittleFS filesystem
Based on a [file by @jimmo](https://github.com/jimmo/dotfiles/blob/master/common/home/.config/mpremote/config.py), I am using his recommended method of erasing all of the files on a Pico. It is in my [config file](https://wellys.com/posts/rp2040_mpremote/#config) or you can use this command:
```py
mpremote exec --no-follow  "import os, machine, rp2; os.umount('/'); bdev = rp2.Flash(); os.VfsLfs2.mkfs(bdev, progsize=256); vfs = os.VfsLfs2(bdev, progsize=256); os.mount(vfs, '/'); machine.reset()"
```
**IT WILL ERASE ALL OF YOUR PROGRAM FILES ON YOUR PICO!!** It will not delete the MicroPython uf2 file.
