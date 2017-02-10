#!/usr/bin/env python3

import platform

import ev3dev.ev3 as ev3

from module.api import *

if platform.system() in ['Windows', 'Linux']:
    macAddress = "20:15:10:26:62:90"
else:
    macAddress = "/dev/tty.bitalino-DevB"
running_time = 5

batteryThreshold = 30
acqChannels = [4]
"""
    0 = EMG (Electromyography)
    1 = EDA (Electrodermal activity)
    2 = ECG (Electrocardiography)
    3 = ACC (Accelerometer)
    4 = LUX (https://en.wikipedia.org/wiki/Lux)
    5 = LED (Light-emitting diode)
"""
samplingRate = 100
nSamples = 1
#turn on LED light
digitalOutput = [0, 0, 1, 0]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
print(device.battery(batteryThreshold))

# Read BITalino version
device.version()

# Start Acquisition
device.start(samplingRate, acqChannels)

start = time.time()
end = time.time()
while (end - start) < running_time:
    # Read samples
    read = device.read(nSamples)
    print(read)
    end = time.time()

    # Lego Mindstorms EV3
    m = ev3.LargeMotor('outA')
    m.run_timed(samplingRate, read[0][-1])

# Turn BITalino led on
device.trigger(digitalOutput)

# Stop acquisition
device.stop()

# Close connection
device.close()