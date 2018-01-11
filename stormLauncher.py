#!/usr/bin/python

# Copyright 2012, Nathan Milford

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# This script requires:
# * PyUSB 1.0+, apt in Debian/Ubuntu installs 0.4.
# * The ImageTk library. On Debian/Ubuntu 'sudo apt-get install python-imaging-tk'
# Also, unless you want to toggle with udev rules, it needs to be run as root

# Use arrows to aim.  Sse the left enter to fire.

# BTW, Leeroy Jenkins Mode .wav is from: http://www.leeroyjenkins.net/soundbites/warcry.wav

import os
import sys
import hid

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from PIL import Image, ImageTk

wavFile  = "warcry.wav"
logoFile = "stormLauncher.png"

class launchControl(Frame):
    def __init__(self):
        hidraw = hid.device(0x2123, 0x1010)
        hidraw.open(0x2123, 0x1010)
        self.dev = hidraw
        if self.dev is None:
            raise ValueError('Launcher not found.')

        Frame.__init__(self)
        self.pack()
        self.master.title("Launch Control")
        self.master.geometry("400x90")

        self.logo = ImageTk.PhotoImage(Image.open(logoFile))

        self.panel1 = Label(self, image=self.logo)
        self.panel1.pack(side='top', fill='both', expand='yes')
        self.panel1.image = self.logo

        self.message1 = StringVar()
        self.line1 = Label(self, textvariable = self.message1)
        self.message1.set("Aim (arrow keys) & Fire (return)!")
        self.line1.pack()

        if os.path.isfile(wavFile):
            self.hasSound = IntVar()
            self.check1 = Checkbutton(self, text = "Leeroy Jenkins Mode?", variable = self.hasSound, onvalue = 1, offvalue = 0)
            self.check1.pack()

        self.master.bind("<KeyPress-Up>", self.turretUp)
        self.master.bind("<KeyRelease-Up>", self.turretStop)

        self.master.bind("<KeyPress-Down>", self.turretDown)
        self.master.bind("<KeyRelease-Down>", self.turretStop)

        self.master.bind("<KeyPress-Left>", self.turretLeft)
        self.master.bind("<KeyRelease-Left>", self.turretStop)

        self.master.bind("<KeyPress-Right>", self.turretRight)
        self.master.bind("<KeyRelease-Right>", self.turretStop)

        self.master.bind("<KeyPress-Return>", self.turretFire)

    def turretUp(self, event):
        self.message1.set("Turret Up.")
        self.dev.send_feature_report([0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00])

    def turretDown(self, event):
        self.message1.set("Turret Down.")
        self.dev.send_feature_report([0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])

    def turretLeft(self, event):
        self.message1.set("Turret Left.")
        self.dev.send_feature_report([0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])

    def turretRight(self, event):
        self.message1.set("Turret Right.")
        self.dev.send_feature_report([0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])

    def turretStop(self, event):
        self.dev.send_feature_report([0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])

    def turretFire(self, event):
        self.message1.set("FIRE!")
        self.dev.send_feature_report([0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])


if __name__ == '__main__':
    if not os.geteuid() == 0:
        sys.exit("Script must be run as root.")
    launchControl().mainloop()
