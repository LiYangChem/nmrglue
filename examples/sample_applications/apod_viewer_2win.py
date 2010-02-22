#!/usr/bin/env python
"""
An example of using wxPython to build a GUI application using nmrglue
This application displays the NMRPipe apodization windows
"""

import numpy as np
import nmrglue as ng
import matplotlib

# uncomment the following to use wx rather than wxagg
#matplotlib.use('WX')
#from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

# comment out the following to use wx rather than wxagg
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx

apod_list = ["SP","EM","GM","GMB","TM","TRI","JMOD"]

class ParameterFrame(wx.Frame):
    
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,-1,"Parameters",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.parent = parent

        self.qName1 = wx.StaticText(self,-1,"Type:")
        self.qName2 = wx.Choice(self,-1,choices=apod_list)
        self.Bind(wx.EVT_CHOICE,self.ApodChoose,self.qName2)
        
        self.q1_1 = wx.StaticText(self,-1,"q1:")
        self.q1_2 = wx.TextCtrl(self,-1,"0.0")

        self.q2_1 = wx.StaticText(self,-1,"q2:")
        self.q2_2 = wx.TextCtrl(self,-1,"1.0")
        
        self.q3_1 = wx.StaticText(self,-1,"q3:")
        self.q3_2 = wx.TextCtrl(self,-1,"1.0")

        self.c1 = wx.StaticText(self,-1,"c")
        self.c2 = wx.TextCtrl(self,-1,"1.0")

        self.start_1 = wx.StaticText(self,-1,"Start")
        self.start_2 = wx.TextCtrl(self,-1,"1.0")

        self.size_1 = wx.StaticText(self,-1,"Size")
        self.size_1.Enable(False)
        self.size_2 = wx.TextCtrl(self,-1,"1.0")
        self.size_2.Enable(False)

        self.inv = wx.CheckBox(self,-1,"Invert")

        self.use_size = wx.CheckBox(self,-1,"Custom Size")
        self.Bind(wx.EVT_CHECKBOX,self.OnLimitCheck,self.use_size)

        self.points_1 = wx.StaticText(self,-1,"Number of Points:")
        self.points_2 = wx.TextCtrl(self,-1,"1000")

        self.sw_1 = wx.StaticText(self,-1,"Spectral Width:")
        self.sw_2 = wx.TextCtrl(self,-1,"50000.")


        self.b1 = wx.Button(self,10,"Draw")
        self.Bind(wx.EVT_BUTTON,self.OnDraw,self.b1)
        self.b1.SetDefault()

        self.b2 = wx.Button(self,20,"Clear")
        self.Bind(wx.EVT_BUTTON,self.OnClear,self.b2)
        self.b2.SetDefault()

        self.InitApod("SP")

        # layout
        apod_grid = wx.GridSizer(8,2)

        apod_grid.AddMany([self.qName1, self.qName2,
                   self.q1_1, self.q1_2,
                   self.q2_1, self.q2_2,
                   self.q3_1, self.q3_2, 
                   self.c1,self.c2,
                   self.start_1,self.start_2,
                   self.size_1,self.size_2,
                   self.inv,self.use_size])
        
        data_grid = wx.GridSizer(2,2)
        data_grid.AddMany([self.points_1,self.points_2,
                self.sw_1,self.sw_2])


        apod_box = wx.StaticBoxSizer(wx.StaticBox(self,-1,
            "Apodization Parameters"))
        apod_box.Add(apod_grid)

        data_box = wx.StaticBoxSizer(wx.StaticBox(self,-1,
            "Data Parameters"))
        data_box.Add(data_grid)

        button_box = wx.GridSizer(1,2)
        button_box.AddMany([self.b1,self.b2])

        mainbox = wx.BoxSizer(wx.VERTICAL)
        mainbox.Add(apod_box)
        mainbox.Add(data_box)
        mainbox.Add(button_box)
        self.SetSizer(mainbox)

        self.Fit()
        self.SetMinSize(self.GetSize())

    def OnLimitCheck(self,event):
        k= event.IsChecked()
        self.size_1.Enable(k)
        self.size_2.Enable(k)
        points = float(self.points_2.GetValue())
        self.size_2.SetValue(str(points))

    def ApodChoose(self,event):
        self.InitApod(apod_list[self.qName2.GetCurrentSelection()])

    def InitApod(self,qName):
        
        if qName == "SP":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("off")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("end")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("1.0")

            self.q3_1.Enable(True)
            self.q3_1.SetLabel("pow")
            self.q3_2.Enable(True)
            self.q3_2.SetValue("1.0")

        elif qName == "EM":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("lb (Hz)")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(False)
            self.q2_2.Enable(False)

            self.q3_1.Enable(False)
            self.q3_2.Enable(False)

        elif qName == "GM":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("g1 (Hz)")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("g2 (Hz)")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("0.0")

            self.q3_1.Enable(True)
            self.q3_1.SetLabel("g3")
            self.q3_2.Enable(True)
            self.q3_2.SetValue("0.0")

        elif qName == "GMB":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("lb")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("gb")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("0.0")

            self.q3_1.Enable(False)
            self.q3_2.Enable(False)

        elif qName == "TM":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("t1")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("t2")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("0.0")

            self.q3_1.Enable(False)
            self.q3_2.Enable(False)

        elif qName == "TRI":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("loc")
            self.q1_2.Enable(True)
            points = points = float(self.points_2.GetValue())
            self.q1_2.SetValue(str(points/2.))

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("lHi")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("0.0")

            self.q3_1.Enable(True)
            self.q3_1.SetLabel("rHi")
            self.q3_2.Enable(True)
            self.q3_2.SetValue("0.0")

        elif qName == "JMOD":
            self.q1_1.Enable(True)
            self.q1_1.SetLabel("off")
            self.q1_2.Enable(True)
            self.q1_2.SetValue("0.0")

            self.q2_1.Enable(True)
            self.q2_1.SetLabel("j (Hz)")
            self.q2_2.Enable(True)
            self.q2_2.SetValue("0.0")

            self.q3_1.Enable(True)
            self.q3_1.SetLabel("lb (Hz)")
            self.q3_2.Enable(True)
            self.q3_2.SetValue("0.0")

    def OnDraw(self,event):
        qName = apod_list[self.qName2.GetCurrentSelection()]
        q1 = float(self.q1_2.GetValue())
        q2 = float(self.q2_2.GetValue())
        q3 = float(self.q3_2.GetValue())
        c = float(self.c2.GetValue())
        start = float(self.start_2.GetValue())
        size = float(self.size_2.GetValue())
        
        inv = self.inv.GetValue()
        use_size = self.use_size.GetValue()

        points = float(self.points_2.GetValue())
        sw = float(self.sw_2.GetValue())

        self.parent.ApplyApod(qName,q1,q2,q3,c,start,size,inv,use_size,
        points,sw)
        
    def OnClear(self,event):
        self.parent.ClearFigure()

class CanvasFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Apodization Viewer')

        self.SetBackgroundColour(wx.NamedColor("WHITE"))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        
        # open Parameter Dialog
        win = ParameterFrame(self,-1)
        win.Show(True)

        # layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

    def OnPaint(self, event):
        self.canvas.draw()

    def ClearFigure(self):
        self.axes.cla()
        self.OnPaint(-1)

    def ApplyApod(self,qName,q1,q2,q3,c,start,size,inv,use_size,points,sw):
       
        """
        print "DEBUGGING INFOMATION"
        print "ApplyApod Recieved:"
        print "qName:",qName
        print "q1:",q1
        print "q2:",q2
        print "q3:",q3
        print "c:",c
        print "start:",start
        print "size:",size
        print "inv:",inv
        print "use_size:",use_size
        print "points:",points
        print "sw:",sw
        """

        # create the dictionary
        dic = ng.fileiobase.create_blank_udic(1)
        dic[0]["sw"] = sw
        dic[0]["size"] = points

        # create the data
        data = np.ones(points,dtype="complex")

        # convert to NMRPipe format
        C = ng.convert.converter()
        C.from_universal(dic,data)
        pdic,pdata = C.to_pipe()


        if use_size == True:
            tsize = size
        else:
            tsize = 'default'
        null,apod_data = ng.pipe_proc.apod(pdic,pdata,qName=qName,
        q1=q1,q2=q2,q3=q3,c=c,inv=inv,size=tsize,start=start)

        # draw the window
        #self.axes.cla()
        self.axes.plot(apod_data)
        self.OnPaint(-1)

class App(wx.App):
    def OnInit(self):
        frame = CanvasFrame()
        frame.Show(True)
        return True

app = App(0)
app.MainLoop()
