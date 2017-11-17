import wx
from wx.lib.buttons import GenButton
from wx import Button
from wx import BitmapFromImage
from wx import TextCtrl
from wx import adv
from Downloader import Downloader
import threading
import Config
import subprocess
import wx.media


class GUI(wx.Frame):
    ID_MAID = 1
    ID_RUN = 2
    ID_UPDATE = 3
    ID_HEAP = 4
    ID_COMBO = 5
    ID_MUTE = 6
    ID_USERNAME = 7

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize((550, 647))
        self.SetSizeHints(550, 647, 550, 647)

        # Worker thread for updating
        self.worker = None
        self.pw = Config.getpassword()
        self.username = Config.getusername()
        Downloader.initialize()

        self.InitUI()
        self.bindEvents()

    def bindEvents(self):
        self.Bind(wx.EVT_BUTTON, self.onUpdatePress, id=self.ID_UPDATE)
        self.Bind(wx.EVT_BUTTON, self.onRunPress, id=self.ID_RUN)
        self.Bind(wx.EVT_COMBOBOX, self.onComboBox, id=self.ID_COMBO)
        self.Bind(wx.EVT_TEXT, self.OnKeyTypedPass)
        self.Bind(wx.EVT_CHECKBOX, self.onMute)

    def InitUI(self):
        # Turn this into a download off the website
        image = wx.Image('res\\'+ 'background.jpg', wx.BITMAP_TYPE_ANY)
        imagepanel = wx.StaticBitmap(self, -1, wx.Bitmap(image))

        self.updatebtn = Button(imagepanel, self.ID_UPDATE, 'Update')
        self.runbtn = Button(imagepanel, self.ID_RUN, 'Run')

        self.heapText = wx.StaticText(imagepanel, label="Heap Size: ")

        self.sizes = ['-Xmx1024m -Xms512m', '-Xmx2048m -Xms1024m', '-Xmx512m -Xms256m']
        self.comboBox = wx.ComboBox(imagepanel, self.ID_COMBO, choices=self.sizes, style=wx.CB_READONLY)
        self.comboBox.SetSelection(int(Config.getheap()))

        # A running gif that plays when updating.... Will save this for another day.
        #self.rungif = adv.AnimationCtrl(imagepanel, -1)
        #self.rungif.LoadFile(Config.updaterdir + 'loading.gif')
        #self.rungif.Hide()

        # Plays music... Will also save this for another day.
        #self.music = wx.media.MediaCtrl(self)
        #self.music.Load(Config.updaterdir + 'bgmusic.mp3')
        #self.mutemusic = wx.CheckBox(imagepanel, self.ID_MUTE)
        #self.mutemusic.SetValue(Config.getMute())

        gsizer = wx.GridSizer(rows=20, cols=4, hgap=0, vgap=0)
        # Empty cells are used to create blank spaces in the grid
        empty_cell = (0, 0)
        #gsizer.Add(self.mutemusic)

        if Config.authenticationRequired:
            self.pwtxtfield = TextCtrl(imagepanel, value=Config.password, style=wx.TE_PASSWORD)
            self.usertxtfeild = TextCtrl(imagepanel, value=Config.username)
            self.userText = wx.StaticText(imagepanel, label="Username")
            self.pwText = wx.StaticText(imagepanel, label="Password")

            gsizer.Add(self.userText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER)
            gsizer.Add(self.usertxtfeild, flag=wx.EXPAND)
            gsizer.Add(self.pwText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER)
            gsizer.Add(self.pwtxtfield, flag=wx.EXPAND)
            for x in range(0, 68):
                gsizer.Add(empty_cell)
        else:
            for x in range(0, 72):
                gsizer.Add(empty_cell)

        gsizer.Add(self.heapText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER)
        gsizer.Add(self.comboBox, flag=wx.EXPAND)
        gsizer.Add(self.updatebtn, flag=wx.EXPAND)
        gsizer.Add(self.runbtn, flag=wx.EXPAND)

        imagepanel.SetSizer(gsizer)
        self.SetSizer(gsizer)
        self.Fit()

    def onUpdatePress(self, e):
        print("Updating...")
        # Not quite sure why I need to use this callback instead of just using checkForUpdater as target

        # Save the username + password, If these authorization boolean is enabled
        if Config.authenticationRequired:
            Config.saveusername(Config.username)
            Config.savepassword(Config.password)
            Downloader.authenticate(Config.username, Config.password)

        def callback():
            Downloader.checkForUpdate()
            self.worker = None
            #wx.CallAfter(self.stopGif)
        if not self.worker:
            print("Starting...")
            #self.playGif()
            self.worker = threading.Thread(target=callback)
            self.worker.start()
        else:
            print("Already started")

    def onRunPress(self, e):
        print("Run")
        heap = self.sizes[self.comboBox.GetSelection()].split()

        def callback():
            file = open(Config.clientdir + "errorlog.txt", "w+")
            # The subprocess runs the java jar provided
            # Currently doesn't pop up a cmd prompt, got to read the errorlog for the output.
            subprocess.Popen(['java', heap[0], heap[1], '-jar', Config.clientdir + 'SimpleDemo.jar'], stdout=file,
                             stderr=file, cwd=Config.clientdir)

        t = threading.Thread(target=callback)
        t.start()
        #if not self.mutemusic.GetValue():
        #    self.music.Play()

    def onMaidPress(self, e):
        heap = self.sizes[self.comboBox.GetSelection()].split()
        file = open(Config.clientdir + "errorlog.txt", "w+")
        def callback():
            file = open(Config.clientdir + "errorlog.txt", "w+")
            subprocess.call(['java', heap[0], heap[1], '-jar', Config.clientdir + 'maid.jar', '-U', 'http://game.havenandhearth.com/hres/',
                             'game.havenandhearth.com'], stdout=file, stderr=file, cwd=Config.clientdir)

        t = threading.Thread(target=callback)
        t.start()
        if not self.mutemusic.GetValue():
            self.music.Play()

    def OnKeyTypedPass(self, e):
        Config.password = e.GetString()

    def OnKeyTypedUser(self, e):
        Config.username = e.GetString()

    def onComboBox(self, e):
        Config.saveheap(self.sizes.index(e.GetString()))

    def onMute(self,e):
        Config.saveMute(e.GetEventObject().Value)
        if e.GetEventObject().Value:
            self.music.Stop()

    def playGif(self):
        self.rungif.Show()
        self.rungif.Play()

    def stopGif(self):
        self.rungif.Hide()
        self.rungif.Stop()
