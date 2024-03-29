# Pico W LED Demo

## Introduction
The contents of this folder install a webserver application on a WiFi-enabled board running MicroPython. The server is a simple web page offering the ability to turn LED's on or off. The page is served by a small web server library called [microdot](https://github.com/miguelgrinberg/microdot), which was written for [MicroPython](https://www.micropython.org), running on a Pico W. This demo is intended to serve as a simple, **iterative** example as to how to develop a user-facing webpage running on the Pico W.
## Updated:
**Mar 2024:** Reorganized the site to be more hierarchical, adding folder for specific categories. The build files now reside in the *mpbuild* folder and they have been updated for the both the *http* (*/http*)  and *web socket* (/websockets) versions of the webserver.

**Jan 2024:** Using new 2.0 version of [microdot web server](https://github.com/miguelgrinberg/microdot). This changes how microdot is copied to the board, instead of standalone files, it looks like a package:

```bash
...files
/microdot/
         106 __init__.py
       51363 microdot.py
        2543 utemplate.py
...files
```

All mpbuild files *files_vN.txt* have been tested and load properly. I've added `async def` to all web functions in the 7th version *light_leds_v7* per the documentation. The recommendation stated it could increase performance. It does appear to do so, though I haven't done explicit timing.

## Versions and Installation
If you already have files on your Pico W, you will need to "*wipe*" your Pico W file system (reformat it) to reduce possible program conflicts. **Be sure you have saved any program files on your PC, before doing so!** See *"Tool to Erase...* below for more information.

There are different versions, *_v1*, *_v2*, *_v3* etc. of the web server software. Each one expands on the capabilities of the previous version.

Run these two commands to install the first version of files on the board.
```
mpremote littlefs_rp2 # this command will erase ALL program files on Pico!!
mpbuild.py files_v1.txt
``` 

To move to the next version with *n* as the desired build version. 
```
mpremote littlefs_rp2 # this command will erase ALL program files on Pico!!
mpbuild files_vn.txt 
```
### HTTP Versions
These programs use *HTTP* protocol to communicate with the Pico. The advantage of this protocol, is that it is relatively easy to understand and code. It does require a reload every communication, which makes it cumbersome as a user-interface.

#### Version 1
Very simple page which will provide the capability to turn the built-in LED ON/OFF. Introduces the HTTP POST method to pass a single value.

#### Version 2
Moves from the built-in LED to four LEDs of different colors. Expands on HTTP POST method for using several values.

#### Version 3
Fixes the user experience to allow for any number of the four LED's to be switched ON/OFF simultaneously. Adds the use of variables to be passed via the concept of a template, making the user experience more dynamic.

#### Version 4 
Adds information to the four LED's by providing labels for each pin. This adds using a template file with variables, expanding on the user experience. 

#### Version 5
Provides the capability for the user to set both the label for the color and the pin number being used. Similar to version 4, however, adds another form for the user to setup the breadboard. This allows the user to change pins or to provide a different set of labels such as *Error*, *Warning*, *Success*, or *Informational*, instead of *Red*, *Yellow*, *Green*, or *Blue*.

#### Version 6
Replaces *marx.css* with [*mvp.css*](https://andybrewer.github.io/mvp/#docs), which I prefer. The goal of *mvp* is to immediately provide a *minimum-viable-product* web page which looks *clean*. I believe it is closer to what I was looking to achieve than what I found in *marx*. A [tutorial on mvp.css](https://calmcode.io/shorts/mvp.css.html). It is also half the size of *marx.css*.

I also replaced the four lists, (*labels, pins, gpio, states*) with the class, *Led*. It does simplify the setup and provides better slighly better self-documentation led_0.label instead of label[0]. Added GPIO numbers into table as well, for confirming programming.

#### Version 7
Used the combination of templates and variables to refactor the server program and webpages to be far more simple. The *microdot* *POST* can return an array of values, as compared to each value labeled separately. (*I missed this early on.*) Therefore, I'm able to use an array on getting the values and printing the values, simplifying the code.

Simplifying the code makes a signficant difference in three areas, easier to maintain, 20% smaller in size and much easier to expand. This is the value in performing that "*one more iteration in factoring the code*".

### Web socket Versions
These programs use the *web socket* protocol to communicate with the Pico. The advantage of this protocol, is that it is almost instantaneous as an user-interface. It can be more complicated to program and requires *Javascript*.

#### Version 1ws - Web Socket version
Very simple page which will provide the capability to turn the built-in LED ON/OFF. Uses Web Sockets, instead of a method to pass a single value. The example builds on the *echo* example in the [Microdot documentation](https://microdot.readthedocs.io/en/latest/extensions.html#websocket-support).

#### Version 2ws - Web Socket version
Adds to version 1 with images for computer, and on/off leds. Very simple page which will provide the capability to turn the built-in LED ON/OFF. Uses Web Sockets, instead of a method to pass a single value. Clicking on an image will turn the built-in led on/off. There is styling via css which hides the radio buttons, and provides a square around the selected state. The advantage of this version (or any Web Socket page), is that the page isn't reloaded, the javascript on the page will immediately advise the MicroPython application of the desired state.

#### Version 3ws - Web Socket version
Continues on the theme of using Web Sockets, instead of a page reload. In this case, the page uses a hidden checkbox, with the word "Click" as an indicator of action required. When clicked, the image changes to represent the state of the led, *on* or *off*. The desktop Python program, *"set_pico_3ws"* provides the ability to automate testing of this version, run it on your desktop instead of using a browser.

#### Version 4ws - Web Socket version 
Similar to Version 4, it uses 4 LED's, however uses Web Sockets to connect. This version can be refactored a bit more using templates to reduce the redundent code in index_v4ws.html. The desktop Python program, *"set_pico_4ws"* provides the ability to automate testing of this version, run it on your desktop instead of using a browser.

#### Version 5 Time Test
I wanted to explore response times in greater detail, so I created a set of files which end in *"_v5tt"* (time_test):
* files_v5tt.txt - the mpbuild manifest for creating the application on a Pico
* light_leds_v5tt.py - main Pico MicroPython program which measures and reports the time between a start and stop click
* indext_v5tt.html - index.html which handles the start/stop and time reporting
* set_pico_v5tt.py - desktop Python program to test response rates

This set of programs is an interim step in measuring response. It demonstrates how to measure time between clicks, whether the clicks are from a browser or automated via *set_pico_v5tt*. The next step will be to allow for running the program for tens or hundreds of iterations and examine variance between response times vs. time between clicks.

##### Usage
1. Install the \_v5tt application using `mpremote littlefs_rp2` and `mpbuild files_v5tt.txt`.
2. Reset the Pi Pico to start the webserver and note the IP address
3. Edit the *set_pico_v5tt.py* file and enter the correct IP address
4. Run `python set_pico_v5tt.py` and observe the response times.

You can change the value of the variable *interval* in *set_pico_v5tt*, to determine the impact of the interval between clicks on the response time of the webserver.

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
1. Browse to IP address:5000 (not 0.0.0.0 as stated)

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
Starting sync server on 0.0.0.0:5000...
```
It is also critical the device (phone or PC) which are using to connect with the Pico is on the same network as well. **Be sure you are connected to the same SSID.**

The address you enter in your browser is a combination of the addresses supplied above. Use the **IP Address** combined with the *port number* following the *0.0.0.0* as in *:5000*. Using the above data, you would need to go to this address:
```
http://10.0.1.12:5000
```

If the wireless connection can not be made, the LED will blink at a faster rate and a error will be printed via the serial port as in:
```
Connection failed: LINK_BADAUTH
Starting sync server on 0.0.0.0:5000...
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
Starting sync server on 0.0.0.0:5000...
```
## Serial Programs
I develop on a Mac and use [CoolTerm](https://freeware.the-meiers.org). It is quite robust and is able to connect to everything I've attempted. Another amazing aspect is that it can be automated using AppleScript. I'll provide a link to demonstrate this at a later date.

My second favorite "connect to everything" serial program is a paid program ($40) Serial [https://www.decisivetactics.com/products/serial/). I've found it is easy to configure AND it is robust enough to connect to everything I'v attempted as well.

Two other programs to consider are [*tio*](https://github.com/tio/tio) and [*miniterm*](https://pyserial.readthedocs.io/en/latest/tools.html).

I've found several programs on the Mac which won't work with a Pico (*when it is re-booted...*):
* *cu* - a common, simple program which crashes when the Pico is rebooted
* *screen* - a ubiquitous, powerful screen program which doesn't seem to connect to the Pico after re-boot
* *minicom* - crashes when the Pico is rebooted
* *Thonny IDE* - loses serial connection when the Pico is rebooted

## Resetting the Pico
The *Pico W* doesn't have a reset button, which means there are two alternatives. First, power cycle the Pico by removing the USB cable or second, add a reset button. I find the second method preferable and have described the process [here](https://wellys.com/posts/rp2040_micropython_1/#reset).

## Program Size
This program hasn't been optimized for size as its a capability demo, not a production program. I have switched from bulma css framework (200K) to [*mvp.css*](https://andybrewer.github.io/mvp/#docs) (10k).

## Automation to Copy Project to Board
The program *mpbuild.py* provides automation to copy the appropriate files to the Pico board. The program *mpbuild.py* has been removed from this repository and now exists in the [CoolTerm_pip repository](https://github.com/lkoepsel/CoolTerm_pip). This repository continues to be the best example as to **how to use** *mpbuild*.
```bash
mpbuild --help
Usage: mpbuild [OPTIONS] BUILD

  Builds an MicroPython application on a board. Uses a text file containing
  names of folders and files to copy files and create folders, approriately to
  a board running MicroPython. Requires -p port for serial port: as in -p
  /dev/cu.usb... or -p COM3 Board storage must be empty or program exits.

  Detailed example: https://github.com/lkoepsel/microserver

  * Requires a text file containing the following:
  * Filenames can NOT have blanks in their names.
  * lines starting with '\n *' are comments and ignored
  * lines starting with '/' are directories and are created
  * lines starting with '!' are files to be copied and renamed,
  + 2 fields are required, separated by a ', ', localname, piconame
  * 1 line starting with '+' will be copied to main.py
  * directory lines must be prior to the files in the directories
  * all other lines are valid files in the current directory
  * -p port required to set to board serial port

Options:
  --version        Show the version and exit.
  -p, --port TEXT  Port address (e.g., /dev/cu.usbmodem3101, COM3).
                   [required]
  -n, --dry-run    Show commands w/o execution & print file format.
  -v, --verbose    Print lines in build file prior to execution.
  --help           Show this message and exit.
```

## Tool to Erase Pico LittleFS filesystem
Based on a [file by @jimmo](https://github.com/jimmo/dotfiles/blob/master/common/home/.config/mpremote/config.py), I am using his recommended method of erasing all of the files on a Pico. It is in my [config file](https://wellys.com/posts/rp2040_mpremote/#config) or you can use this command:

```bash
mpremote exec --no-follow  "import os, machine, rp2; os.umount('/'); bdev = rp2.Flash(); os.VfsLfs2.mkfs(bdev, progsize=256); vfs = os.VfsLfs2(bdev, progsize=256); os.mount(vfs, '/'); machine.reset()"
```
**IT WILL ERASE ALL OF YOUR PROGRAM FILES ON YOUR PICO!!** It will not delete the MicroPython uf2 file.

### Config file
Store this file in ~/.config/mpremote/config.py

```python
commands = {
    "A": "connect id:e6614864d3323634",
    "fl": "fs ls",
    "littlefs_rp2": [
        "exec",
        "--no-follow",
        "import os, machine, rp2; os.umount('/'); bdev = rp2.Flash();\
                os.VfsLfs2.mkfs(bdev, progsize=256); \
                vfs = os.VfsLfs2(bdev, progsize=256); \
                os.mount(vfs, '/'); machine.reset()",
    ],
    "test": ["mount", ".", "exec", "import test"],
    "info": ["mount", ".", "run", "fs_info.py"],
    "blink": ["mount", ".", "exec",
              "from blink import Blink; Blink()"]
}
```


## Error Codes
When using the REPL, frequently you might see an error code. Here is a list of known MicroPython error codes and explanations from *CPython*:
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


## Viewing JSON Responses in Browser
It helps to view the web socket responses in your browser to further understand them. I use Arc, which is Chrome-based as Chrome has very good developer tools. In a Chrome-based browser:
1. Click on Developer Tools to show the window
2. Click on Network tab at the top
3. Ensure All is clicked whowing all data (second line from top)
4. Do a refresh of the browser to display all activity, you will now see all of the files sent under Name
5. Click on ws for web socket, which will display Headers Messages Initiator Timing in the adjacent window, click on Messages to show the JSON data being exchanged.
6. Click on a specific line if you wish to see more details