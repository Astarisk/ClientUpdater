from GUI import GUI
import wx

if __name__ == "__main__":
    app = wx.App(False)
    g = GUI(None, -1, 'Updater')
    g.Show()
    app.MainLoop()
