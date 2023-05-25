import serial
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

mpl.use('tkagg')

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/pts/5'
ser.open()
# ser.readline()
axis = [[] for y in range(3)]

fig, ax = plt.subplots(1, 1, num="STM32 Accelerometer")
ax.set_title("Accelerometer readout")

blue_patch = patches.Patch(color='blue', label='X')
green_patch = patches.Patch(color='green', label='Y')
red_patch = patches.Patch(color='red', label='Z')
plt.legend(handles=[blue_patch, green_patch, red_patch], loc='center left', bbox_to_anchor=(1, 0.5))

plt.subplots_adjust(bottom=0.2, right=0.8)

looping = False


def start(event):
    ser.write('1'.encode('UTF-8'))
    global looping
    looping = True
    plt.ion()
    while looping:
        line = ser.readline().decode("UTF-8")
        nums = line.split(' ')
        axis[0].append(int(nums[0]))
        axis[1].append(int(nums[1]))
        axis[2].append(int(nums[2]))
        ax.plot(axis[0], color='blue', label="X")
        ax.plot(axis[1], color='green', label="Y")
        ax.plot(axis[2], color='red', label="Z")
        plt.draw()
        plt.pause(0.1)


def stop(event):
    ser.write('0'.encode('UTF-8'))
    global looping
    looping = False


axstart = plt.axes([0.4, 0.05, 0.1, 0.075])
bstart = Button(axstart, "Start")
bstart.on_clicked(start)

axstop = plt.axes([0.5, 0.05, 0.1, 0.075])
bstop = Button(axstop, "Stop")
bstop.on_clicked(stop)

plt.show()
