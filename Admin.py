from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from threading import *
import pickle
import time
import vlc
import socket
import StartingPage

class admin_window:
    def __init__(self):
        self.room_id_password=self.receive_object(StartingPage.server)

        #self.room_id_password=StartingPage.server.recv(5120)
        #pickle.loads(self.room_id_password[20:])
        self.ex=True
        self.video_title=""
        self.filename = ""
        self.player = ""
        self.state = ""
        self.running=True
        self.length="00:00"
        self.show_more=False
        self.player_window = Tk()
        self.player_window.geometry("700x155")
        self.player_window.resizable(False, False)

        #self.room_id_password_label=Label(self.player_window,text="Room Id: "+self.room_id_password[0]+"     Password: "+self.room_id_password[1],font=10)
        self.room_id_password_label = Label(self.player_window,text="Please choose a video file ", font=10)
        self.room_id_password_label.pack(pady=5)

        self.player_frame=Frame(self.player_window,bg='red')
        self.player_frame.pack()

        self.video_slider = Scale(self.player_frame, orient=HORIZONTAL, sliderlength=10, width=5, showvalue=0, length=690,
                             state="disabled",command=self.video_slider_change)
        self.video_slider.pack(pady=10)
        self.Video_Progress = Thread(target=self.Video_progress)
        self.Video_Progress.start()
        self.video_timer = Label(self.player_frame,text="00:00/00:00")
        self.video_timer.pack()
        video_timer=Thread(target=self.timer)
        video_timer.start()
        self.stop_button = Button(self.player_frame, text="Stop", width=7, command=lambda: self.stop())
        self.stop_button.pack(side="right", padx=5)

        self.pause_button = Button(self.player_frame, text="Pause", width=8, command=lambda: self.pause())
        self.pause_button.pack(side="right", padx=5)

        self.openvideo_button = Button(self.player_frame, text="Choose Video", width=12,height=1,command=lambda: self.open_file())
        self.openvideo_button.pack(side="left", padx=10)

        self.play_button = Button(self.player_frame, text="Play", width=7, command=lambda: self.play())
        self.play_button.pack(side="right", padx=5)

        self.volume=Scale(self.player_frame,from_=0,to=100,orient=HORIZONTAL,sliderlength=15,width=7,showvalue=0,label="Volume",command=self.check_volume)
        self.volume.set(80)
        self.volume.pack(side="left")



        self.show_more_less_button=Button(self.player_window,text="Show More",command=self.show_more_less_action)
        self.show_more_less_button.pack(pady=5)



        self.chat_frame=Frame(self.player_window,bg='green')
        self.chat_frame.pack(side='left')

        self.chat_label=Label(self.chat_frame,text="Chat:-")
        self.chat_label.pack(pady=10)

        self.chatbox=Text(self.chat_frame,width=50,height=10)
        self.chatbox.pack()

        self.members_frame=Frame(self.player_window,bg='blue')
        self.members_frame.pack(side='right')

        self.member_label=Label(self.members_frame,text="Memebers:-")
        self.member_label.pack(pady=10)

        #self.scrollbar=Scrollbar(self.members_frame)

        self.member_list=Listbox(self.members_frame,width=30,font=('Courier',10))
        self.member_list.pack()

        #self.member_list.config(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.member_list.yview)

        for i in range(50):
            self.member_list.insert(END,'item',i)


        self.player_window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.player_window.mainloop()



    def show_more_less_action(self):
        if self.show_more:
            self.show_more_less_button.config(text="Show More")
            self.show_more=False
            self.player_window.geometry("700x155")
        else:
            self.show_more_less_button.config(text="Show Less")
            self.show_more=True
            self.player_window.geometry("700x350")



    def open_file(self):
        self.filename = askopenfilename()
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
            if extension in self.filename:
                isvideo = True

        if isvideo:
            if self.state=="playing":
                self.stop()

            self.video_title=self.filename.split('/')[-1]

            self.room_id_password_label.config(text="Room Id: " + self.room_id_password[0] + "     Password: " +
                                                     self.room_id_password[1])

            self.player = vlc.MediaPlayer(self.filename)
            self.player.play()
            #time.sleep(0.0250)
            while(self.player.get_length()==0):
                pass
            self.video_slider.config(state="active",from_=0, to=self.player.get_length())

            StartingPage.server.send(bytes(f"{len('new file'):<20}" + 'new file', 'utf-8'))

            message = pickle.dumps([self.video_title,self.player.get_length()])
            message = bytes(f"{len(message):<20}", 'utf-8') + message
            StartingPage.server.send(message)

            self.length=self.player.get_length()
            self.player.audio_set_volume(self.volume.get())
            self.player.stop()

            length_second=self.length//1000
            length_minute=length_second//60
            length_second=length_second%60

            length_minute=str(length_minute)
            if len(length_minute)==1:
                length_minute='0'+length_minute

            length_second=str(length_second)
            if len(length_second)==1:
                length_second='0'+length_second
            self.length=length_minute+':'+length_second
            sync_thread=Thread(target=self.sync_thread)
            sync_thread.start()
            self.video_timer.config(text="00:00/"+self.length)
            self.openvideo_button.config(state="disable")

        else:
            if self.filename!="":
                messagebox.showerror("Not a Video File", "Please Choose a Video File to play.")
                self.filename=""


    def video_slider_change(self,event):
        if self.video_slider.get()-self.player.get_time() and self.ex:
            self.pause()
            self.player.set_time(self.video_slider.get())

            #time.sleep(0.001)

    def stop(self):
        if self.state!="":
            self.player.stop()
            self.state=""

    def pause(self):
        if self.state=="playing":
            self.player.pause()
            self.state="pause"
            if not self.running:
                return
            StartingPage.server.send(bytes(f"{len('pause'):<20}" + 'pause', 'utf-8'))

    def play(self):
        if not self.running:
            return
        StartingPage.server.send(bytes(f"{len('play'):<20}" + 'play', 'utf-8'))
        if not self.running:
            return
        time = str(self.video_slider.get())
        if not self.running:
            return
        StartingPage.server.send(bytes(f"{len(time):<20}" + time, 'utf-8'))
        if not self.running:
            return
        if self.state=="pause":
            if not self.running:
                return
            self.player.play()
            self.state="playing"


        elif self.state=="playing":
            return

        elif self.filename=="":
            messagebox.showerror("No Video Found","Choose a video file to play")
        else:
            if not self.running:
                return
            self.player.play()
            self.state="playing"
            #self.player.set_fullscreen(True)


    def check_volume(self,event):
        if self.state=="playing":
            self.player.audio_set_volume(self.volume.get())

    def Video_progress(self):
        while(self.running):
            if self.state=="playing":
                self.video_slider.set(self.player.get_time())
            elif self.state=="":
                self.video_slider.set(0)
            time.sleep(0.0001)

            #if self.player_window.state()!="normal":
            #    break

    def timer(self):
        while(self.running):
            current_time=self.video_slider.get()
            time.sleep(0.0001)
            if not self.running:
                break

            second=current_time//1000
            minute=second//60
            second=second%60

            minute=str(minute)
            if len(minute)==1:
                minute='0'+minute

            second=str(second)
            if len(second)==1:
                second='0'+second

            self.video_timer.config(text=minute+':'+second+'/'+self.length)

            time.sleep(0.0001)

            if not self.running:
                break
            #time.sleep(0.0001)

    def receive_object(self,server):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            print("before recieve")
            msg = server.recv(64)
            print()
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                print('here')
                return pickle.loads(full_msg[20:])

    def receive_data(self,server):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            try:
                msg = server.recv(64)
            except:
                print("recieve error handled")
                return
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                return full_msg[20:].decode()


    def sync_thread(self):
        while(self.running):
            action=self.receive_data(StartingPage.server)
            print("sync thread: ", action)
            time.sleep(1.5)
            if not self.running:
                break
            if action=='sync':
                if self.state=="":
                    StartingPage.server.send(bytes(f"{len('empty'):<20}" + 'empty', 'utf-8'))
                elif self.state == "playing":
                    #time.sleep(1.5)
                    self.play()
                elif self.state== "pause":
                    StartingPage.server.send(bytes(f"{len('empty'):<20}" + 'empty', 'utf-8'))
                    if not self.running:
                        break

            if not self.running:
                break

    def close_window(self):
        self.running=False
        StartingPage.server.send(bytes(f"{len('stop'):<20}" + 'stop', 'utf-8'))
        StartingPage.server.shutdown(socket.SHUT_RDWR)
        StartingPage.server.close()
        time.sleep(0.0001)
        self.player_window.destroy()