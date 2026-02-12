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
            slider = ttk.Scale(slider_frame,orient="vertical",from_=-100,to=100)
            slider.set(self.rcmds.robot.get_curjpos()[i-1])
            slider.grid(row=0,column=i,padx=10)
            self.sliders_widget[f'slider{i}'] = slider
        self.loop_active = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(self.root,text="Цикл",variable=self.loop_active,command=self.activate)
        self.checkbox.place(x=330,y=50)
        self.stopbutton = tk.Button(root,text='STOP',command=self.stopcycle)
        self.stopbutton.pack(pady=50)

    def activate(self):
        if self.loop_active.get():
            self.returnslider()
            self.stopbutton.config(bg="white")
    def stopcycle(self):
        self.loop_active.set(False)
        if not self.loop_active.get():
            self.stopbutton.config(bg="red")        

    def returnslider(self):
        if not self.loop_active.get():
            return
        robot_velocity = [float(F"{self.sliders_widget[f"slider{i}"].get():.2f}") for i in range(1,7)]
        try:
            self.rcmds.Moving(robot_velocity)
        except Exception:
            self.stopcycle()
        print(robot_velocity)
        self.root.after(100,self.returnslider)



if __name__ == "__main__":
    root = tk.Tk()
    app = RoboGUI(root)
    root.mainloop()