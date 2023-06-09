# Pico W LED Demo
The contents of this folder enable a simple web page offering the ability to turn LED's on or off. The page is served by a small web server called [microdot](https://github.com/miguelgrinberg/microdot), which was written for [MicroPython](), running on a Pico W. This demo is intended to serve as a simple iterative example as to how to develop a user-facing webpage running on the Pico W.
## Versions and Installation
If you already have files on your Pico W, it might help to "*wipe*" your Pico W file system (reformat it) to reduce possible program conflicts. **Be sure you have saved any program files on your PC, before doing so!** See *"Tool to Erase...* below for more information.

There are different versions, *_v1*, *_v2*, *_v3* etc. of the web server software. Each one expands on the capabilities of the previous version.

Run this command to install the first version of files on the board.
```
mpbuild.py files_v1.txt
``` 

To move to the next version with *n* as the desired build version. 
```
mpr littlefs_rp2
mpbuild files_vn.txt 
```
### Version 1
Very simple page which will provide the capability to turn the built-in LED ON/OFF. Introduces the HTTP POST method to pass a single value.

### Version 2
Moves from the built-in LED to four LEDs of different colors. Expands on HTTP POST method for using several values.

### Version 3
Fixes the user experience to allow for any number of the four LED's to be switched ON/OFF simultaneously. Adds the use of variables to be passed via the concept of a template, making the user experience more dynamic.

### Version 4 
Adds information to the four LED's by providing documentation as to the color/pin combination expected. This adds using a template file with variables, expanding on the user experience.

### Version 5
Provides the capability for the user to set both the label for the color and the pin number being used. Similar to version 4, however, adds another form for the user to setup the breadboard. This allows the user to change pins or to provide a different set of labels such as *Error*, *Warning*, *Success*, or *Informational*, instead of *Red*, *Yellow*, *Green*, or *Blue*.

### Version 6
Replaces *marx.css* with [*mvp.css*](https://andybrewer.github.io/mvp/#docs), which I believe I prefer. The goal of *mvp* is to immediately provide a *minimum-viable-product* web page which looks *clean*. I believe it is closer to what I was looking to achieve than what I found in *marx*. A [tutorial on mvp.css](https://calmcode.io/shorts/mvp.css.html).

I also replaced the four lists, (*labels, pins, gpio, states*) with the class, *Led*. It does simplify the setup and provides better slighly better self-documentation led_0.label instead of label[0]. Added GPIO numbers into table as well, for confirming programming.

### Version 7
Used the combination of templates and variables to refactor the server program and webpages to be far more simple. The *microdot* *POST* can return an array of values, as compared to each value labeled separately. (*I missed this early on.*) Therefore, I'm able to use an array on getting the values and printing the values, simplifying the code.

## Additional Files Required
### secrets.py
This file contains the SSID and password of your desired wireless LAN connection:
```python
ssid = 'Demo'
password = 'mpc1234!'
```
A simple text file called *secrets.py* with the above format and the correct SSID and password is required. It sits at the root folder along with the other files such as wlan.py.
## Installation
* Copy the folder to your PC

To run on a Pico W:

1. Ensure secrets.py has the desired SSID and password for your WiFi
1. Build the desired version, using instructions above
1. Start a serial program (see Note below)
1. Press Reset or cycle power on your Pico W
1. Use the IP address provided via the serial port
1. Browse to IP address:5001 to play game (not 0.0.0.0 as stated)

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

## Resolving Program Errors
Sometimes, a program error will prevent any output from the Pico. This makes it difficult to debug the problem. The solution is to:
1. Start your serial program
2. Press *Ctrl-C* to enter the REPL
then enter `from main import *`. Then the startup error will more than likely print.
Here is an example:
```python
>>> from main import *
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "main.py", line 6, in <module>
ImportError: no module named 'pins.py'
```
In this error, I attempted to import a module with the full name, I needed to drop the ".py". If you continue to have problems, you can start the program by entering "web_server()" as in this example:
```python
>>> from main import *
>>> web_server()
IP Address: 10.0.1.10
MAC Address: 28:cd:c1:08:a9:7c
Channel: 1
SSID: Demo
TX Power: 31
Starting sync server on 0.0.0.0:5001...
```
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
This program hasn't been optimized for size as its a capability demo, not a production program. I have switched from bulma css framework (200K) to [marx css framework](https://mblode.github.io/marx/) (10k). *See note on Version 6 regarding mvp.css.*

## Automation to Copy Project to Board
The program *mpbuild.py* provides automation to copy the appropriate files to the Pico board.
```bash
usage: mpbuild.py [-h] [-n] [-v] build

Reads names of files from build file in current folder. Copies files to attached MicroPython board. Use --dry-run or -n to print commands, instead of execution. Filenames can NOT have blanks in their names.

positional arguments:
  build          file to use for building Pico

options:
  -h, --help     show this help message and exit
  -n, --dry-run  required to copy the files to the board
  -v, --verbose  print lines in build file prior to execution
```
The program uses pyboard.py from mpremote (installed via pip), which means the PYBOARD_DEVICE environmental variable must be set. See [here](https://docs.micropython.org/en/latest/reference/pyboard.py.html#running-a-command-on-the-device).

## Tool to Erase Pico LittleFS filesystem
Based on a [file by @jimmo](https://github.com/jimmo/dotfiles/blob/master/common/home/.config/mpremote/config.py), I am using his recommended method of erasing all of the files on a Pico. It is in my [config file](https://wellys.com/posts/rp2040_mpremote/#config) or you can use this command:
```py
mpremote exec --no-follow  "import os, machine, rp2; os.umount('/'); bdev = rp2.Flash(); os.VfsLfs2.mkfs(bdev, progsize=256); vfs = os.VfsLfs2(bdev, progsize=256); os.mount(vfs, '/'); machine.reset()"
```
**IT WILL ERASE ALL OF YOUR PROGRAM FILES ON YOUR PICO!!** It will not delete the MicroPython uf2 file.

## Error Codes
When using Thonny or the REPL, frequently you might see an error code. Here is a list of known MicroPython error codes and explanations from *CPython*:
```bash
1 EPERM Operation not permitted
2 ENOENT No such file or directory
5 EIO Input/output error
9 EBADF Bad file descriptor
11 EDEADLK Resource deadlock avoided
12 ENOMEM Cannot allocate memory
13 EACCES Permission denied
17 EEXIST File exists
19 ENODEV Operation not supported by device
21 EISDIR Is a directory
22 EINVAL Invalid argument
95 EMULTIHOP EMULTIHOP (Reserved)
98 ENOSR No STREAM resources
103 ENOPOLICY Policy not found
104 ENOTRECOVERABLE State not recoverable
105 EOWNERDEAD Previous owner died
```

## Minimal Shell Using upysh
In this folder is a program called *upysh.py*. It has a minimal set of shell commands which can be quite useful. I've found I'm able to use these commands instead of spinning up Thonny, when I need to see something on the board. Use the MicroPython REPL and follow below:
```python
upysh is intended to be imported using:
from upysh import *

To see this help text again, type "man".

upysh commands:
clear, ls, ls(...), head(...), cat(...), newfile(...)
cp('src', 'dest'), mv('old', 'new'), rm(...)
pwd, cd(...), mkdir(...), rmdir(...), tree(...), du(...)
```
The last two commands came from [here](https://forum.micropython.org/viewtopic.php?t=7550) and can be quite useful!
