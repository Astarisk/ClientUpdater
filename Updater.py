import wx
from GUI import GUI

if __name__ == "__main__":
    app = wx.App(False)
    g = GUI(None, -1, 'Updater')
    g.Show()
    app.MainLoop()
