import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Analyzer:
    def __init__(self, target=180, overs=20):
        self.target = target
        self.total_balls = overs * 6
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        self.run_history = []

    def overs(self):
        return f"{self.balls//6}.{self.balls%6}"

    def run_rate(self):
        o = self.balls/6
        return self.runs/o if o>0 else 0

    def req_rr(self):
        balls_left = self.total_balls - self.balls
        runs_left = self.target - self.runs
        return (runs_left/balls_left)*6 if balls_left>0 else 0

    def win_prob(self):
        balls_left = self.total_balls - self.balls
        runs_left = self.target - self.runs
        if balls_left<=0:
            return 100 if self.runs>=self.target else 0
        req = (runs_left/balls_left)*6
        pressure = req - self.run_rate()
        return max(0,min(100,50-pressure*7))

    def update(self, val):
        if val=="W":
            self.wickets+=1
            self.balls+=1
        elif val=="wd" or val=="nb":
            self.runs+=1
        else:
            self.runs+=int(val)
            self.balls+=1

        self.run_history.append(self.run_rate())


class App:
    def __init__(self, root):
        self.root=root
        self.root.title("Real-Time Cricket Analyzer")

        self.an=Analyzer()

        self.info=tk.Label(root,font=("Arial",16))
        self.info.pack(pady=10)

        btn_frame=tk.Frame(root)
        btn_frame.pack()

        buttons=["0","1","2","3","4","6","W","wd","nb"]
        for i,b in enumerate(buttons):
            tk.Button(btn_frame,text=b,width=5,height=2,
                      command=lambda x=b:self.play(x)).grid(row=i//5,column=i%5,padx=5,pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.update_display()

    def play(self,val):
        self.an.update(val)
        self.update_display()
        self.update_graph()

    def update_display(self):
        txt = f"Score: {self.an.runs}/{self.an.wickets}   Overs: {self.an.overs()}\n"
        txt+=f"Run Rate: {self.an.run_rate():.2f}   Required RR: {self.an.req_rr():.2f}\n"
        txt+=f"Win Probability: {self.an.win_prob():.2f}%"
        self.info.config(text=txt)

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.an.run_history)
        self.ax.set_title("Run Rate Progression")
        self.ax.set_xlabel("Balls")
        self.ax.set_ylabel("Run Rate")
        self.canvas.draw()


root=tk.Tk()
app=App(root)
root.mainloop()
