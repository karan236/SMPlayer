import socket
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import MediaInfo
import vlc

class client:
    def __init__(self):
        self.client=socket.socket()
        self.filename=""
        self.player = ""
        self.state = ""
        self.opening_page()

    def opening_page(self):
        root = Tk()
        root.title("Social Player")
        root.geometry("725x275")
        root.resizable(False, False)

        img = PhotoImage(file="imge.png")

        welcome_image = Label(root, image=img)
        welcome_image.pack()

        about_button = Button(root, text="About", width=10, command=lambda: self.about(root))
        about_button.pack(side="left", padx=2)

        login_button = Button(root, text="Login", width=10, command=lambda: self.login(root))
        login_button.pack(side="right", padx=2)

        continue_without_login_button = Button(root, text="Continue Without Login", width=30,
                                               command=lambda: self.continue_without_login_action(root))
        continue_without_login_button.pack(side="right", padx=2)

        root.mainloop()

    def connect(self):
        host = 'localhost'
        port = 9999
        self.client.connect((host, port))

    def open_file(self):
        self.filename = askopenfilename()

    def play(self):
        if self.state=="pause":
            self.player.play()
            self.state="playing"
            return
        if self.state=="playing":
            return

        if self.filename=="":
            messagebox.showerror("No Video Found","Choose a video file to play")

        else:
            isvideo=False

            extensions=[
'.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
'.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
'.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
'.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
'.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
'.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
'.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
'.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
'.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
'.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
'.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
'.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
'.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
'.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
'.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
'.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
'.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
'.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
'.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
'.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
'.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
'.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
'.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
'.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg','.vem', '.vep', '.vf', '.vft',
'.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
'.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
'.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
'.zm1', '.zm2', '.zm3', '.zmv']

            for extension in extensions:
                if extension in self.filename:
                    isvideo=True

            if isvideo:
                self.player=vlc.MediaPlayer(self.filename)
                self.player.play()
                self.state="playing"

            else:
                messagebox.showerror("Not a Video File","Please Choose a Video File to play.")



    def pause(self):
        if self.state=="playing":
            self.player.pause()
            self.state="pause"

    def stop(self):
        if self.state!="":
            self.player.stop()
            self.state=""

    def progressbar(self):
        pass


    def about(self,root):
        pass

    def login(self,root):
        root.destroy()

    def continue_without_login_action(self,root):
        root.destroy()
        player_window=Tk()

        player_window.geometry("700x100")
        player_window.resizable(False,False)

        video_slider=Scale(player_window,orient=HORIZONTAL,sliderlength=10, width=5,showvalue=0,length=690,state="disabled")
        video_slider.pack(pady=10)

        video_timer=Label(text="Label")
        video_timer.pack()

        stop_button=Button(player_window,text="Stop",width=7,command=lambda: self.stop())
        stop_button.pack(side="right",padx=5)

        pause_button=Button(player_window,text="Pause",width=8,command=lambda: self.pause())
        pause_button.pack(side="right",padx=5)

        openvideo_button = Button(player_window, text="Open Video", width=10, command=lambda: self.open_file())
        openvideo_button.pack(side="left", padx=10)

        play_button=Button(player_window,text="Play",width=7,command=lambda : self.play())
        play_button.pack(side="right",padx=5)



        player_window.mainloop()

client()