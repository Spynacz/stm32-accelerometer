import threading
import serial 
import matplotlib.patches as patches 
from matplotlib.figure import Figure
from tkinter import * 
from tkinter import ttk 
import serial.tools.list_ports 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
 
ser = serial.Serial() 

axis = [[] for y in range(3)] 

def plot():
    global looping
    while (looping):
        fig.clear()
        line = ser.readline().decode("UTF-8") 
        nums = line.split(' ') 
        axis[0].append(int(nums[0])) 
        axis[1].append(int(nums[1])) 
        axis[2].append(int(nums[2])) 
            
        ax = fig.add_subplot(111)
        ax.plot(axis[0], color='blue', label="X") 
        ax.plot(axis[1], color='green', label="Y") 
        ax.plot(axis[2], color='red', label="Z") 

        ax.legend(loc='lower left')
        ax.set_ylabel("acceleration")

        canvas.get_tk_widget().pack()
        canvas.draw()
        root.loadtk()


def start(): 
    if (not ser.is_open):
        ser.baudrate = 115200 
        ser.port = combo.get()
        ser.open() 
        ser.write('1'.encode('UTF-8')) 
        global looping 
        looping = True 
        th = threading.Thread(target=plot)
        th.start()

 
def stop(): 
    ser.write('0'.encode('UTF-8')) 
    global looping 
    looping = False 
    ser.close() 


looping = False 
 
root = Tk()
root.title('STM32 accelerator')
fig = Figure(figsize=(5,5))
canvas = FigureCanvasTkAgg(fig, master=root)
butt1 = ttk.Button(root, text="Start", command=start) 
butt1.pack(side=BOTTOM) 
butt2 = ttk.Button(root, text="Stop", command=stop) 
butt2.pack(side=BOTTOM)
combo = ttk.Combobox(root)
combo.pack(side=BOTTOM)

ports=[] 
for port in serial.tools.list_ports.comports(): 
   ports.append(port.name) 
combo['values'] = ports 

root.mainloop()
