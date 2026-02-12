import asyncio
import robot
import tkinter as tk
from tkinter import ttk
import threading

class RoboGUI:
    def __init__(self,root):
        self.root = root
        self.root.title("RoboGUI")
        self.root.geometry("1000x500")
        self.rcmds = robot.Motion()
        self.central_panel()


    def central_panel(self):
        slider_frame = ttk.Frame(self.root)
        slider_frame.place(x=50,y=50,width=300,height=200)
        self.sliders_widget = {}
        for i in range(1,7):
            slider = ttk.Scale(slider_frame,orient="vertical",from_=100,to=-100)
            slider.set(self.rcmds.robot.get_curjpos()[i-1])
            slider.grid(row=0,column=i,padx=10)
            self.sliders_widget[f'slider{i}'] = slider
        self.loop_active = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(self.root,text="Cycle",variable=self.loop_active,command=self.activate)
        self.checkbox.place(x=330,y=50)
        self.gripper_statue = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(self.root,text="Gripper",variable=self.gripper_statue,command=self.grip)
        self.checkbox.place(x=330,y=70)
        self.stopbutton = tk.Button(root,text='STOP',command=self.stopcycle)
        self.stopbutton.pack(pady=50)
        self.box = ttk.Combobox(values = ["joint","pose"],state="readonly")
        self.box.current(0)
        self.box.place(x=330,y=90)
        
        self.frame = ttk.Frame(self.root)
        self.frame.place(x=50,y=200)
        self.coords = {}
        for i in range(1,7):
            label = ttk.Label(self.frame,text=i)
            label.grid(row=0,column=i+1,padx=20)
            label2 = ttk.Label(self.frame,text=self.rcmds.robot.get_curjpos()[i-1])
            self.coords[f'coords{i}'] = label2
            label2.grid(row=1,column=i+1)

    def grip(self):
        self.rcmds.turn_gripper(self.gripper_statue.get())

    def activate(self):
        if self.loop_active.get():
            self.returnslider()
            self.stopbutton.config(bg="white",text="STOP")
    def stopcycle(self):
        self.loop_active.set(False)
        self.stopbutton.config(bg="red",text="STOPPED")        

    def returnslider(self):
        if not self.loop_active.get():
            return
        try:
            if self.box.get() == "pose":
                robot_velocity = [float(F"{self.sliders_widget[f"slider{i}"].get() * 5:.2f}") for i in range(1,7)]
            elif self.box.get() == "joint":
                robot_velocity = [float(F"{self.sliders_widget[f"slider{i}"].get():.2f}") for i in range(1,7)]
            self.rcmds.Moving(robot_velocity,self.box.get())
            for i in range(1,7):
                self.coords[f'coords{i}']["text"] = robot_velocity[i-1]
            self.root.after(100,self.returnslider)
        except Exception as e:
            print(f"ошибка - {e}")
            self.stopcycle()

        



if __name__ == "__main__":
    root = tk.Tk()
    app = RoboGUI(root)
    root.mainloop()