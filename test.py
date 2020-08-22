from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from threading import *
import time
import vlc

filename = ""
player = ""
global state
state = ""
running=True
#Check_Volume = Thread(target=check_volume)
#Check_Volume.start()
Video_Progress=Thread(target=Video_progress)


player_window = Tk()
Video_Progress.start()
player_window.geometry("700x100")
player_window.resizable(False, False)

video_slider = Scale(player_window, orient=HORIZONTAL, sliderlength=10, width=5, showvalue=0, length=690,
                     state="disabled")
video_slider.pack(pady=10)

video_timer = Label(text="Label")
video_timer.pack()

stop_button = Button(player_window, text="Stop", width=7, command=lambda: stop())
stop_button.pack(side="right", padx=5)

pause_button = Button(player_window, text="Pause", width=8, command=lambda: pause())
pause_button.pack(side="right", padx=5)

openvideo_button = Button(player_window, text="Open Video", width=10,height=1,command=lambda: open_file())
openvideo_button.pack(side="left", padx=10)

play_button = Button(player_window, text="Play", width=7, command=lambda: play())
play_button.pack(side="right", padx=5)

volume=Scale(player_window,from_=0,to=100,orient=HORIZONTAL,sliderlength=15,width=7,showvalue=0,label="Volume",command=check_volume)
volume.set(80)
volume.pack(side="left")

#player_window.protocol("WM_DELETE_WINDOW", close_window)

player_window.mainloop()

def open_file():
    filename = askopenfilename()
    isvideo = False

    extensions = [
        '.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec',
        '.aep', '.aepx',
        '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf',
        '.asx', '.avb',
        '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik',
        '.bin', '.bix',
        '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel',
        '.cine', '.cip',
        '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat',
        '.dav', '.dce',
        '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm',
        '.dmsm3d', '.dmss',
        '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms',
        '.dvx', '.dxr',
        '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp',
        '.fcproject',
        '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp',
        '.h264', '.hdmov',
        '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf',
        '.ivr', '.ivs',
        '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg',
        '.m1v', '.m21',
        '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv',
        '.mj2', '.mjp',
        '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov',
        '.movie', '.mp21',
        '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2',
        '.mpgindex', '.mpl',
        '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv',
        '.mvb', '.mvc',
        '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv',
        '.nvc', '.ogm',
        '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs',
        '.playlist', '.plproj',
        '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva',
        '.pvr', '.pxv',
        '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm',
        '.rmd', '.rmd',
        '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl',
        '.sbk', '.sbt',
        '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv',
        '.smi', '.smi',
        '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi',
        '.swf', '.swi',
        '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts',
        '.tsp', '.ttxt',
        '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep',
        '.vf', '.vft',
        '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6',
        '.vp7', '.vpj',
        '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx',
        '.wot', '.wp3',
        '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog',
        '.yuv', '.zeg',
        '.zm1', '.zm2', '.zm3', '.zmv']

    for extension in extensions:
        if extension in filename:
            isvideo = True

    if isvideo:
        if state=="playing":
            player.stop()
            state=""

        player = vlc.MediaPlayer(filename)
        player.play()
        time.sleep(0.030)
        video_slider.config(state="active",from_=0, to=player.get_length())
        print(player.get_length())
        player.audio_set_volume(volume.get())
        player.stop()

    else:
        if filename!="":
            messagebox.showerror("Not a Video File", "Please Choose a Video File to play.")
            filename=""


def stop():
    if state!="":
        player.stop()
        state=""

def pause():
    if state=="playing":
        player.pause()
        state="pause"

def play():
    if state=="pause":
        player.play()
        state="playing"

    elif state=="playing":
        return

    elif filename=="":
        messagebox.showerror("No Video Found","Choose a video file to play")
    else:
        player.play()
        state="playing"
        #player.set_fullscreen(True)


def check_volume(event):
    if state=="playing":
        player.audio_set_volume(volume.get())

def Video_progress():
    while(running):
        print(state,player_window.state())
        if state=="playing":
            video_slider.set(player.get_time())
        if player_window.state()!="normal":
            break
    print("BREAK")


def close_window():
    running=False
    player_window.destroy()