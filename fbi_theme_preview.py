#!/usr/bin/python

from tkinter import *
from tkinter import font, messagebox, colorchooser
from PIL import Image, ImageTk
from io import BytesIO
import sys, datetime, random, string, time, base64, re

class Translations:
    def __init__(self):
        self.program_title = "FBI Theme Previewer"

class Configuration:
    def __init__(self):
        self.cfg = {
            'theme_folder':  "romfs/",
            'theme_title':   "FBI Theme Previewer",
            'theme_desc':    "A Shit Tier Stop-gap Solution",
            'theme_author':  "Jurassicplayer",
            'theme_version': "2.4.6",
            'screen_gap':    "0", #68
            'language':      "en",
            'text':          "#000000",
            'nand':          "#0000FF",
            'sd':            "#00FF00",
            'gamecard':      "#FF0000",
            'dstitle':       "#82004B",
            'file':          "#000000",
            'directory':     "#0000FF",
            'enabled':       "#00FF00",
            'disabled':      "#0000FF",
            'installed':     "#00FF00",
            'notinstalled':  "#0000FF",
            'ticketinuse':   "#00FF00",
            'ticketnotinuse':"#0000FF"
            }
        self.load_cfg_from_file("config")
        self.load_cfg_from_file(self.cfg['theme_folder']+"textcolor.cfg")
    def load_cfg_from_file(self, filename):
        argbstring = re.compile(r'[a-fA-F0-9]{8}$')
        try:
            with open(filename) as f:
                config_content = [line.rstrip('\n') for line in f]
        except:
            if "textcolor.cfg" in filename:
                messagebox.showwarning("Open file", "Cannot open this file\n(%s)" % filename)
            elif "config" in filename: pass
            return
        for option in self.cfg:
            for line in config_content:
                if option == line.split("=")[0]:
                    if "textcolor.cfg" in filename:
                        if argbstring.match(line.split("=")[1]):
                            self.cfg.update({option : "#"+line.split("=")[1][2:8]})
                        else:
                            print("Malformed color: {}".format(line))
                    elif "config" in filename:
                        self.cfg.update({option : line.split("=")[1]})
    def save_cfg_to_file(self):
        print("Not implemented")

class AppWindow(Tk):
    def __init__(self, root=None):
        Tk.__init__(self, root)
        self.icon_base64 ="""R0lGODlhIAAgAOfYAKYAAKcAAKgAAKUBAakAAKoAAKsAAKgBAawAAK0AAK4AAKwBAa0BAa4BAa0C\nAq4DA64EBK4FBa8ICKwMDLALC60MDLEQD7IRELETE7IUFLMUFLIWFrMWFrMYF7QYGLQZGbUZGbYb\nG7UcHLYeHbYfH7YhILciIrUlJbYlJbcnJrgoJ7krKrksK7otLbouLbsxMbsyMbo0NLk1NL05OL47\nOlZXV748O1dYV7o+PcBCQbtEQ71EQ75EQ79EQ8BEQ8BERMFGRcJKSWJkY8JKSmNkZL5MS8NNTMNO\nTcRPTsRQT8RRUMVUU8VVVMdaWchdXMVfXshfXsViYcZiYcdiYchiYcliYcZjYsdjYcdjYshjYslj\nYcljYspjYcpjYspkY8tpZ8tracxsa8xubc1ubcl2ds51c891c892ddB5d8+BgNCBgNGBgNKBgNKC\ngNaBgdSGhdSJh9SJiNOLitWLitSMi9WMitWMi9aMi9ONjdWNi9aNi9eNi9eOi9mOi9iQjtiUktiW\nlNmYltmamNmbmdqcmq6urNyjodimpbGxrtmnp9iop9mop9qop9uoqN2optqpqNqpqdupqNupqdyp\nqNypqduqqdyqqdyqqt2qqd6qqN2rqd6rqd6rqt+rqd+rqt6sqd6sqt+squCsqt+tqeCtqt2urLq6\nuOCwrru7ueCysNO3ttS4uOG1stO5udW5uNW5uda5uNa6uNa6ude6uNe6ucPAv9e7udi7ueK5ttm8\nueK6t9e9usXCwNq9uePCweXDwebGxObHxNnPzdrPzOnQzufS0erU0erW0+vZ1uza1+3f3O7i4O7j\n4O/k4e/n5PDn5PHr6PHt6vHu6/Lv7PLw7fLw7vLx7vPy7///////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n/////////////////////////////////////////////////////yH5BAEKAP8ALAAAAAAgACAA\nAAj+AP8JHEiwoMGDBlH98sOHD508dujs2WOnDh07dvrokaMH4508evD4MjUQERoFCRIoICCAgIEE\nCGIiMFAAAcyZBmQiIECmkEBjCxpAYbNGTRo1bdi0abOmKdKlS5u2UfNkwIFiAi8hMHKtq9evzaqU\ncALtq9kiAioJZGSgi9mvyl6kTGDj2NuuUQhEWksgy91r1jZ1mJugRbC31qToXVsAy19kySzMlZBA\nBbO3UwgsEjipr7W7y541mTsiRIIgn79mfiSQUl9qfzNFIJzSgzSzUwQoEhipQBbYbw09MDH3iyNi\n094q3vwvEQEsyd8SQuAmpYrUd/Pu/ffJN3CzzCD+gEhp5i9eAKAEdkrg9u+SuWHMX5uCIP0/Twm2\n/E11YS4L7G9RkQAnAnGiQHtmVQMDbYOYpxiB/4iCAIJm/ZJBAgwk4MAP35mlhQGhCBRKfuaVgUAc\nW8nHRQIh/kMJAvr9BQgEznBQhXwfYiJQIwBYYV4gIlwDhBfyZbZdJAI49tcZK1wDRg7yKQZJa32Z\nB4UL18xBQTQOEmAJZ8+Zx8QM1+iCADBdSsJZkuYpkcQ10WhgiHlGCiRJAD7+hcQYXUEBh3lUGKCJ\nQKOw+dcRb3T1hxiAGkCKQKQIcIV5PwTSFStD0InAo/+UEoAMt701DQmCdIXLBwB6JU0MCJwi0DBs\nExRwAg898ODDrT3QgMAGO/CQAgI46NArD8T2gEIBFQgjEBGHYFBAAQQEIIABOSVgAEsFUEsAAAR0\nSwC0BWDAiBAD3cDLLr3kosoqrrxiyy2zzOKKK7fkAksssdAiyyuyyNJKLTUgJPDABwUEADs="""
        img = PhotoImage(data=self.icon_base64)
        self.call('wm', 'iconphoto', self._w, img)
        self.screen = ""
        self.loadStaticResources()
        self.loadDynamicResources()
        self.createWidgets()
        self.drawCanvas()
        self.screen = "main_screen"
        self.wifi_counter = 0
        self.battery_counter = 0
        self.updateCanvas()
    
    def loadStaticResources(self):
        #Load translations
        tl = getattr(sys.modules[__name__], "Translations")()
        self.title(tl.program_title)
        #Load configurations
        self.config = getattr(sys.modules[__name__], "Configuration")()
        self.c = self.config.cfg
        self.dir = self.c['theme_folder']
        #Shits and giggles number generator
        sd_size = random.choice((2.0,4.0,8.0,16.0,32.0,64.0,128.0,256.0,512.0))
        ctrnand_size = random.choice((943.0, 1240.0))
        self.sd_ex = sd_size - random.randrange(0.0, sd_size) + (random.randrange(0,9)/10)
        self.ctrnand_ex = ctrnand_size - random.randrange(0.0, ctrnand_size) + (random.randrange(0,9)/10)
        self.twlnand_ex = 128.0 + (random.randrange(0,9)/10)
        self.twlphoto_ex = 32.0 + (random.randrange(0,9)/10)
        self.i_meta_info_icon = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(self.icon_base64))).resize((48,48)))
        
    def loadDynamicResources(self):
        #Load all images
        self.i_battery_charging = PhotoImage(file=self.dir+"battery_charging.png")
        self.i_battery0 = PhotoImage(file=self.dir+"battery0.png")
        self.i_battery1 = PhotoImage(file=self.dir+"battery1.png")
        self.i_battery2 = PhotoImage(file=self.dir+"battery2.png")
        self.i_battery3 = PhotoImage(file=self.dir+"battery3.png")
        self.i_battery4 = PhotoImage(file=self.dir+"battery4.png")
        self.i_battery5 = PhotoImage(file=self.dir+"battery5.png")
        self.i_bottom_screen_bg = PhotoImage(file=self.dir+"bottom_screen_bg.png")
        self.i_bottom_screen_bottom_bar = PhotoImage(file=self.dir+"bottom_screen_bottom_bar.png")
        self.i_bottom_screen_bottom_bar_shadow = PhotoImage(file=self.dir+"bottom_screen_bottom_bar_shadow.png")
        self.i_bottom_screen_top_bar = PhotoImage(file=self.dir+"bottom_screen_top_bar.png")
        self.i_bottom_screen_top_bar_shadow = PhotoImage(file=self.dir+"bottom_screen_top_bar_shadow.png")
        self.i_button_large = PhotoImage(file=self.dir+"button_large.png")
        self.i_button_small = PhotoImage(file=self.dir+"button_small.png")
        self.i_logo = PhotoImage(file=self.dir+"logo.png")
        self.i_meta_info_box = PhotoImage(file=self.dir+"meta_info_box.png")
        self.i_meta_info_box_shadow = PhotoImage(file=self.dir+"meta_info_box_shadow.png")
        self.i_progress_bar_bg = PhotoImage(file=self.dir+"progress_bar_bg.png")
        tmp_image = Image.open(self.dir+"progress_bar_content.png")
        self.i_progress_bar_content = ImageTk.PhotoImage(tmp_image)
        self.i_progress_bar_0 = ImageTk.PhotoImage(tmp_image.crop((0, 0, 0, 30)))
        self.i_progress_bar_25 = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.25), 30)))
        self.i_progress_bar_50 = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.50), 30)))
        self.i_progress_bar_75 = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.75), 30)))
        self.i_scroll_bar = PhotoImage(file=self.dir+"scroll_bar.png")
        ##
        tmp_image = Image.open(self.dir+"selection_overlay.png").resize((320, 15), Image.ANTIALIAS)
        self.i_selection_overlay = ImageTk.PhotoImage(tmp_image)
        self.i_progress_bar_bg = PhotoImage(file=self.dir+"progress_bar_bg.png")
        self.i_top_screen_bg = PhotoImage(file=self.dir+"top_screen_bg.png")
        self.i_top_screen_bottom_bar = PhotoImage(file=self.dir+"top_screen_bottom_bar.png")
        self.i_top_screen_bottom_bar_shadow = PhotoImage(file=self.dir+"top_screen_bottom_bar_shadow.png")
        self.i_top_screen_top_bar = PhotoImage(file=self.dir+"top_screen_top_bar.png")
        self.i_top_screen_top_bar_shadow = PhotoImage(file=self.dir+"top_screen_top_bar_shadow.png")
        self.i_wifi_disconnected = PhotoImage(file=self.dir+"wifi_disconnected.png")
        self.i_wifi0 = PhotoImage(file=self.dir+"wifi0.png")
        self.i_wifi1 = PhotoImage(file=self.dir+"wifi1.png")
        self.i_wifi2 = PhotoImage(file=self.dir+"wifi2.png")
        self.i_wifi3 = PhotoImage(file=self.dir+"wifi3.png")
        
    def createWidgets(self):
        self.frame = Frame(self)
        self.canvas = Canvas(self.frame, width=400, height=480+int(self.c['screen_gap']), bd=0, highlightthickness=0)
        self.toolbar = Frame(self.frame)
        self.main_button = Button(self.toolbar, text="Main Menu", command=lambda: self.callButton("main_screen"))
        self.item_button = Button(self.toolbar, text="Meta Info", command=lambda: self.callButton("meta_screen"))
        self.progress_button = Button(self.toolbar, text="Progress Bar", command=lambda: self.callButton("progress_screen"))
        self.little_buttons = Button(self.toolbar, text="Little Btn", command=lambda: self.callButton("little_btn_screen"))
        self.big_button = Button(self.toolbar, text="Big Btn", command=lambda: self.callButton("big_btn_screen"))
        self.refresh_button = Button(self.toolbar, text="Refresh", command=self.loadDynamicResources)
        self.main_button.pack(side=LEFT, fill=X)
        self.item_button.pack(side=LEFT, fill=X)
        self.progress_button.pack(side=LEFT, fill=X)
        self.little_buttons.pack(side=LEFT, fill=X)
        self.big_button.pack(side=LEFT, fill=X)
        self.refresh_button.pack(side=LEFT, fill=X)
        self.toolbar.pack(side=TOP)
        self.canvas.bind("<Button-1>", lambda event: self.cursorMove(event, 'B1'))
        self.canvas.bind("<B1-Motion>", lambda event: self.cursorMove(event, 'B1'))
        self.canvas.bind("<Button-3>", lambda event: self.cursorMove(event, 'B3'))
        self.canvas.pack()
        self.frame.pack()
    
    def callButton(self, screen):
        self.screen = screen
        self.clearCanvas()
        self.updateCanvas(auto_loop=False)
        
    def cursorMove(self, event, button):
        if event.x >= 40 and event.x <= 360 and event.y >= 20+240+int(self.c['screen_gap']) and event.y <= 220+240+int(self.c['screen_gap']):
            y_pos_offset = 20+240+int(self.c['screen_gap']) #20px bottom_screen_top_bar, 240px top screen, screen_gap
            y_pos_fixed = event.y-y_pos_offset
            y_binned_index = int(y_pos_fixed/15)
            self.canvas.coords(self.selection_overlay, (40, y_binned_index*15+y_pos_offset))
            if self.screen == "meta_screen" and button == "B3":
                color_index = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
                if y_binned_index < len(color_index):
                    new_color = colorchooser.askcolor(initialcolor = self.c[color_index[y_binned_index]])[1]
                    if new_color:
                        self.c[color_index[y_binned_index]] = new_color
                        self.updateCanvas(auto_loop=False)
                    
    def drawCanvas(self):
        self.font_normal = font.Font(family='Arial', size=-12, weight="bold")
        self.font_mini = font.Font(family='Arial', size=7, weight="bold")
        x_offset = 40
        y_offset = 240+int(self.c['screen_gap'])
                
        #Layer 0 (Background images)
        self.top_screen_bg = self.canvas.create_image(0, 0, anchor = NW, image=self.i_top_screen_bg)
        self.bottom_screen_bg = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image=self.i_bottom_screen_bg)
        
        #Layer 1 (Main information)
        ###Main Menu Screen
        self.logo = self.canvas.create_image(200, 120, image="")
        line_height = 15
        line_offset = 20
        self.bottom_screen_listing01 = self.canvas.create_text(2+x_offset, line_height*0+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing02 = self.canvas.create_text(2+x_offset, line_height*1+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing03 = self.canvas.create_text(2+x_offset, line_height*2+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing04 = self.canvas.create_text(2+x_offset, line_height*3+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing05 = self.canvas.create_text(2+x_offset, line_height*4+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing06 = self.canvas.create_text(2+x_offset, line_height*5+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing07 = self.canvas.create_text(2+x_offset, line_height*6+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing08 = self.canvas.create_text(2+x_offset, line_height*7+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing09 = self.canvas.create_text(2+x_offset, line_height*8+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing10 = self.canvas.create_text(2+x_offset, line_height*9+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing11 = self.canvas.create_text(2+x_offset, line_height*10+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing12 = self.canvas.create_text(2+x_offset, line_height*11+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing13 = self.canvas.create_text(2+x_offset, line_height*12+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_listing14 = self.canvas.create_text(2+x_offset, line_height*13+line_offset+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.selection_overlay = self.canvas.create_image(0+x_offset, 20+y_offset, anchor = NW, image="")
        self.scroll_bar = self.canvas.create_image(0+320+x_offset, 20+y_offset, anchor = NE, image="")
        ###Item Metadata Screen
        self.meta_info_box_shadow = self.canvas.create_image(24, 22, anchor = NW, image="")
        self.meta_info_box = self.canvas.create_image(40, 38, anchor = NW, image="")
        self.meta_info_icon = self.canvas.create_image(48, 46, anchor = NW, image="")
        self.meta_info_box_info = self.canvas.create_text(102, 48, anchor = NW, text="")
        self.meta_info_info = self.canvas.create_text(200, 111, anchor = N, justify='center', text="")
        ###Progress Bar Screen
        self.progress_bar_bg = self.canvas.create_image(10+x_offset, 95+y_offset, anchor = NW, image="")
        self.progress_bar_content = self.canvas.create_image(20+x_offset, 105+y_offset, anchor = NW, image="")
        
        #Layer 2 (Top bars)
        self.top_screen_top_bar = self.canvas.create_image(0, 0, anchor = NW, image=self.i_top_screen_top_bar)
        self.top_screen_bottom_bar = self.canvas.create_image(0, 220, anchor = NW, image=self.i_top_screen_bottom_bar)
        self.top_screen_top_bar_shadow = self.canvas.create_image(0, 20, anchor = NW, image=self.i_top_screen_top_bar_shadow)
        self.top_screen_bottom_bar_shadow = self.canvas.create_image(0, 204, anchor = NW, image=self.i_top_screen_bottom_bar_shadow)
        #Layer 2 (Bottom bars)
        self.bottom_screen_top_bar = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image=self.i_bottom_screen_top_bar)
        self.bottom_screen_bottom_bar = self.canvas.create_image(0+x_offset, 220+y_offset, anchor = NW, image=self.i_bottom_screen_bottom_bar)
        self.bottom_screen_top_bar_shadow = self.canvas.create_image(0+x_offset, 20+y_offset, anchor = NW, image=self.i_bottom_screen_top_bar_shadow)
        self.bottom_screen_bottom_bar_shadow = self.canvas.create_image(0+x_offset, 204+y_offset, anchor = NW, image=self.i_bottom_screen_bottom_bar_shadow)
        
        #Layer 3 (Top bar overlays)
        self.wifi = self.canvas.create_image(347, 2, anchor = NW, image = self.i_wifi3)
        self.battery = self.canvas.create_image(371, 2, anchor = NW, image=self.i_battery_charging)
        self.version_number = self.canvas.create_text(2, 10, anchor = W, font=self.font_normal, text = "")
        self.date_time = self.canvas.create_text(200, 10, font=self.font_normal, text = "")
        self.system_info = self.canvas.create_text(2, 230, anchor = W, font=self.font_mini, text = "")
        #Layer 3 (Bottom bar overlays)
        self.bottom_screen_top_bar_text = self.canvas.create_text(200, 10+y_offset, font=self.font_normal, text = "")
        self.bottom_screen_bottom_bar_text = self.canvas.create_text(200, 230+y_offset, font=self.font_normal, text = "")
        
        

    def clearCanvas(self):
        #Remove all screen specific text and images
        self.canvas.itemconfig(self.bottom_screen_top_bar_text, text = "")
        self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing01, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing02, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing03, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing04, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing05, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing06, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing07, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing08, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing09, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing10, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing11, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing12, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing13, text = "")
        self.canvas.itemconfig(self.bottom_screen_listing14, text = "")
        #main_screen
        self.canvas.itemconfig(self.logo, image="")
        self.canvas.itemconfig(self.selection_overlay, image="")
        self.canvas.itemconfig(self.scroll_bar, image="")
        #meta_screen
        self.canvas.itemconfig(self.meta_info_box, image="")
        self.canvas.itemconfig(self.meta_info_box_shadow, image="")
        self.canvas.itemconfig(self.meta_info_icon, image="")
        self.canvas.itemconfig(self.meta_info_box_info, text = "")
        self.canvas.itemconfig(self.meta_info_info, text = "")
        #progress_screen
        self.canvas.itemconfig(self.progress_bar_bg, image="")
        self.canvas.itemconfig(self.progress_bar_content, image="")
        
    def updateCanvas(self, auto_loop=True):
        #self.loadDynamicResources()
        #Top screen update
        self.canvas.itemconfig(self.top_screen_bg, image=self.i_top_screen_bg)
        self.canvas.itemconfig(self.top_screen_top_bar, image=self.i_top_screen_top_bar)
        self.canvas.itemconfig(self.top_screen_bottom_bar, image=self.i_top_screen_bottom_bar)
        self.canvas.itemconfig(self.top_screen_top_bar_shadow, image=self.i_top_screen_top_bar_shadow)
        self.canvas.itemconfig(self.top_screen_bottom_bar_shadow, image=self.i_top_screen_bottom_bar_shadow)
        
        #Wifi Charging
        wifi_icon = [self.i_wifi_disconnected, self.i_wifi0, self.i_wifi1, self.i_wifi2, self.i_wifi3]
        battery_icon = [self.i_battery_charging, self.i_battery0, self.i_battery1, self.i_battery2, self.i_battery3, self.i_battery4, self.i_battery5]
        progress_icon = [self.i_progress_bar_0, self.i_progress_bar_25, self.i_progress_bar_50, self.i_progress_bar_75, self.i_progress_bar_content]
        if self.wifi_counter >= 4:
            self.wifi_counter = 0
        else:
            self.wifi_counter = self.wifi_counter + 1
        self.canvas.itemconfig(self.wifi, image=wifi_icon[self.wifi_counter])
        if self.battery_counter >= 6:
            self.battery_counter = 0
        else:
            self.battery_counter = self.battery_counter + 1
        self.canvas.itemconfig(self.battery, image=battery_icon[self.battery_counter])
        del wifi_icon
        del battery_icon
        
        #Bottom screen update
        self.canvas.itemconfig(self.bottom_screen_bg, image=self.i_bottom_screen_bg)
        self.canvas.itemconfig(self.bottom_screen_top_bar, image=self.i_bottom_screen_top_bar)
        self.canvas.itemconfig(self.bottom_screen_bottom_bar, image=self.i_bottom_screen_bottom_bar)
        self.canvas.itemconfig(self.bottom_screen_top_bar_shadow, image=self.i_bottom_screen_top_bar_shadow)
        self.canvas.itemconfig(self.bottom_screen_bottom_bar_shadow, image=self.i_bottom_screen_bottom_bar_shadow)
        
        #Text update
        self.canvas.itemconfig(self.version_number, fill=self.c['text'], text = "Ver. {}".format(self.c['theme_version']))
        self.canvas.itemconfig(self.date_time, fill=self.c['text'], text = "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()))
        self.canvas.itemconfig(self.system_info, fill=self.c['text'], text = "SD: {} GiB, CTR NAND: {} MiB, TWL NAND: {} MiB, TWL Photo: {} MiB".format(self.sd_ex, self.ctrnand_ex, self.twlnand_ex, self.twlphoto_ex))
        
        #Reload screen specific text and images
        if self.screen == "main_screen":
            self.canvas.itemconfig(self.logo, image=self.i_logo)
            self.canvas.itemconfig(self.selection_overlay, image=self.i_selection_overlay)
            self.canvas.itemconfig(self.scroll_bar, image=self.i_scroll_bar)
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text'], text = "Main Menu")
            self.canvas.itemconfig(self.bottom_screen_listing01, fill=self.c['text'], text = "SD")
            self.canvas.itemconfig(self.bottom_screen_listing02, fill=self.c['text'], text = "CTR NAND")
            self.canvas.itemconfig(self.bottom_screen_listing03, fill=self.c['text'], text = "TWL NAND")
            self.canvas.itemconfig(self.bottom_screen_listing04, fill=self.c['text'], text = "TWL Photo")
            self.canvas.itemconfig(self.bottom_screen_listing05, fill=self.c['text'], text = "TWL Sound")
            self.canvas.itemconfig(self.bottom_screen_listing06, fill=self.c['text'], text = "Dump NAND")
            self.canvas.itemconfig(self.bottom_screen_listing07, fill=self.c['text'], text = "Titles")
            self.canvas.itemconfig(self.bottom_screen_listing08, fill=self.c['text'], text = "Pending Titles")
            self.canvas.itemconfig(self.bottom_screen_listing09, fill=self.c['text'], text = "Tickets")
            self.canvas.itemconfig(self.bottom_screen_listing10, fill=self.c['text'], text = "Ext Save Data")
            self.canvas.itemconfig(self.bottom_screen_listing11, fill=self.c['text'], text = "System Save Data")
            self.canvas.itemconfig(self.bottom_screen_listing12, fill=self.c['text'], text = "TitleDB")
            self.canvas.itemconfig(self.bottom_screen_listing13, fill=self.c['text'], text = "Remote Install")
            self.canvas.itemconfig(self.bottom_screen_listing14, fill=self.c['text'], text = "Update")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text'], text = "A: Select, START: Exit")
        if self.screen == "meta_screen":
            self.canvas.itemconfig(self.meta_info_box, image=self.i_meta_info_box)
            self.canvas.itemconfig(self.meta_info_box_shadow, image=self.i_meta_info_box_shadow)
            self.canvas.itemconfig(self.meta_info_icon, image=self.i_meta_info_icon)
            self.canvas.itemconfig(self.meta_info_box_info, fill=self.c['text'], text = "{}\n{}\n{}".format(self.c['theme_title'], self.c['theme_desc'], self.c['theme_author']))
            self.canvas.itemconfig(self.meta_info_info, fill=self.c['text'], text = "Title ID: 0004000000FBIP00\nMedia Type: SD\nVersion: 0\nProduct Code: CTR-P-FBIP\nRegion: North America\nSize: 1.56 GiB")
            self.canvas.itemconfig(self.selection_overlay, image=self.i_selection_overlay)
            self.canvas.itemconfig(self.scroll_bar, image=self.i_scroll_bar)
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text'], text = "Textcolor.ini")
            self.canvas.itemconfig(self.bottom_screen_listing01, fill=self.c['text'], text = "Default {}".format(self.c['text']))
            self.canvas.itemconfig(self.bottom_screen_listing02, fill=self.c['nand'], text = "NAND {}".format(self.c['nand']))
            self.canvas.itemconfig(self.bottom_screen_listing03, fill=self.c['sd'], text = "SD {}".format(self.c['sd']))
            self.canvas.itemconfig(self.bottom_screen_listing04, fill=self.c['gamecard'], text = "Gamecard {}".format(self.c['gamecard']))
            self.canvas.itemconfig(self.bottom_screen_listing05, fill=self.c['dstitle'], text = "DS Title {}".format(self.c['dstitle']))
            self.canvas.itemconfig(self.bottom_screen_listing06, fill=self.c['file'], text = "File {}".format(self.c['file']))
            self.canvas.itemconfig(self.bottom_screen_listing07, fill=self.c['directory'], text = "Directory {}".format(self.c['directory']))
            self.canvas.itemconfig(self.bottom_screen_listing08, fill=self.c['enabled'], text = "Enabled {}".format(self.c['enabled']))
            self.canvas.itemconfig(self.bottom_screen_listing09, fill=self.c['disabled'], text = "Disabled {}".format(self.c['disabled']))
            self.canvas.itemconfig(self.bottom_screen_listing10, fill=self.c['installed'], text = "Installed {}".format(self.c['installed']))
            self.canvas.itemconfig(self.bottom_screen_listing11, fill=self.c['notinstalled'], text = "Not installed {}".format(self.c['notinstalled']))
            self.canvas.itemconfig(self.bottom_screen_listing12, fill=self.c['ticketinuse'], text = "Ticket in use {}".format(self.c['ticketinuse']))
            self.canvas.itemconfig(self.bottom_screen_listing13, fill=self.c['ticketnotinuse'], text = "Unused Ticket {}".format(self.c['ticketnotinuse']))
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text'], text = "A: Select, B: Return, X: Refresh")
        if self.screen == "progress_screen":
            self.canvas.itemconfig(self.progress_bar_bg, image=self.i_progress_bar_bg)
            self.canvas.itemconfig(self.progress_bar_content, image=progress_icon[self.wifi_counter])
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text'], text = "Installing From URL(s)")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text'], text = "Press B to cancel.")
        
        if auto_loop:
            self.canvas.after(1000, self.updateCanvas)

    
app = AppWindow()
app.mainloop()