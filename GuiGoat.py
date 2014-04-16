#!/usr/bin/python
# -*- coding: utf-8 -*-
#Python 3.x
#Small GUI Framework based on Tkinter
from tkinter import *


class GoatCanvas(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent)

    def create_triangle(self, x,y, width, height, outlineColor,fillColor):
        points = [0+x, height+y,     int(width/2)+x, 0+y,     width+x,height+y ]
        self.create_polygon(points, outline=outlineColor, fill=fillColor, width=1)

    def create_square(self, x,y,width):
        self.create_rectangle(x,y,x+width,y+width)


class Window(Frame):
    """docstring for Window"""
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self,self.parent)

        # BASIC DEFAULT PARAMETERS
        self.color = "#21262C"
        self.title = "Window"
        self.width = 10
        self.height = 10
        self.update()




    def run(self):

        self.mainloop()



    def update(self):
        self.initUI()
        self.initMainFrame()
        self.initTitleBar()
        self.bindEvents()

    def bindEvents(self):
        self.titleBar.bind("<ButtonPress-1>", self.onMousePress)
        self.titleBar.bind("<ButtonRelease-1>", self.onMouseRelease)
        self.titleBar.bind("<B1-Motion>", self.onMouseMotion)



    def onMousePress(self, event):
        self.x = event.x
        self.y = event.y

    def onMouseRelease(self, event):
        self.x = None
        self.y = None

    def onMouseMotion(self, event):
        #Connaitre la difference parce que geometry additione a la position actuelle
        deltaX = event.x - self.x
        deltaY = event.y - self.y

        x = self.parent.winfo_x() + deltaX
        y = self.parent.winfo_y() + deltaY
        self.parent.geometry("+%s+%s" % (x, y))





    def quit(self):
        self.parent.destroy()


    def initTitleBar(self):
        #TITLE BAR
        titleBar_height = 10

        frameTitleBar = Frame(self, height=titleBar_height)
        frameTitleBar['background'] = self.color
        frameTitleBar.grid(row=0,column=0, sticky=N+W+E+S, columnspan=3,)
        self.titleBar = frameTitleBar

        labelTitre = Label(frameTitleBar, text=self.title, background=self.color, foreground="white")
        labelTitre.grid(row=0,column=0, sticky=N+W+E, columnspan=2 )

        btnClose = Button(self, text="x", command=self.quit, width=5)
        btnClose['background'] = "#c0392b" #RED
        btnClose['borderwidth'] = 0
        btnClose['foreground'] = "#ecf0f1" #WHITE
        btnClose.grid(row=0, column=2, sticky=E+N)

        spacer = Frame(self, height=5)
        spacer['background'] = self.color
        spacer.grid(row=1,column=0, sticky=N+W+E+S, columnspan=3 )


    def initMainFrame(self):
        self.mainFrame = Frame(self, height=self.height, width=self.width)
        self.mainFrame['background'] = "white"
        self.mainFrame.grid(row=2,column=0, sticky=N+W+E+S, columnspan=3 )

    def initUI(self):
        #Disable System title bar
        self.parent.wm_overrideredirect(True)

        self.parent.geometry("+50+50")
        self.parent.resizable(width=FALSE, height=FALSE)

        self.parent.configure(background=self.color)
        self.grid(column=0, row=0, sticky=(N, W, E, S), padx=5,pady=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



    def setTitle(self, title):
        self.title.set(title)
        self.title.get() #Weirdly: it only works wheit this line

    def getTitle(self):
        return self.title.get()




class GUI(object):
    def __init__(self):
        self.master = Window()
        self.master.mainFrame


        frame = Frame(self.master.mainFrame, width=500,height=500)
        frame['background'] = "red"
        frame.pack(fill=BOTH)



    def run(self):
        self.master.run()

def main():

    app = GUI()
    app.run()

if __name__ == '__main__':
    main()
