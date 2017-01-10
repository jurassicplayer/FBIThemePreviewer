#!/usr/bin/python

from tkinter import *
from tkinter import font, messagebox, colorchooser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk, ImageGrab
from io import BytesIO
import os, sys, datetime, random, string, time, base64, re

class Translations:
    def __init__(self):
        self.program_title = "FBI Theme Previewer"

class Configuration:
    def __init__(self):
        self.cfg = {
            'theme_folder':   "romfs/",
            'theme_title':    "FBI Theme Previewer",
            'theme_desc':     "A Shit Tier Stop-gap Solution",
            'theme_author':   "Jurassicplayer",
            'theme_version':  "2.4.6",
            'screen_gap':     "0", #68
            'language':       "en",
            'text':           {'rgb': "#000000", 'alpha': "FF"},
            'nand':           {'rgb': "#FF0000", 'alpha': "FF"},
            'sd':             {'rgb': "#00FF00", 'alpha': "FF"},
            'gamecard':       {'rgb': "#0000FF", 'alpha': "FF"},
            'dstitle':        {'rgb': "#4B0082", 'alpha': "FF"},
            'file':           {'rgb': "#000000", 'alpha': "FF"},
            'directory':      {'rgb': "#FF0000", 'alpha': "FF"},
            'enabled':        {'rgb': "#00FF00", 'alpha': "FF"},
            'disabled':       {'rgb': "#FF0000", 'alpha': "FF"},
            'installed':      {'rgb': "#00FF00", 'alpha': "FF"},
            'notinstalled':   {'rgb': "#FF0000", 'alpha': "FF"},
            'ticketinuse':    {'rgb': "#00FF00", 'alpha': "FF"},
            'ticketnotinuse': {'rgb': "#FF0000", 'alpha': "FF"},
            }
        self.config_index = ['theme_folder', 'theme_title', 'theme_desc', 'theme_author', 'theme_version', 'screen_gap', 'language']
        self.color_index = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
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
                        option_value = line.split("=")[1]
                        if argbstring.match(option_value):
                            A = option_value[:2]
                            RGB = swapRGBBGR(option_value[2:])
                            self.cfg.update({option : {'rgb' : RGB, 'alpha' : A} })
                        else:
                            print("Malformed color: {}".format(line))
                    elif "config" in filename:
                        self.cfg.update({option : line.split("=")[1]})
    def save_cfg_to_file(self, type):
        if type == "textcolor":
            filename = self.cfg['theme_folder']+'textcolor.cfg'
            with open(filename, 'w') as f:
                for i in range (0, len(self.color_index)):
                    f.write("{}={}{}\n".format(self.color_index[i], self.cfg[self.color_index[i]]['alpha'], swapRGBBGR(self.cfg[self.color_index[i]]['rgb'])[1:]))
        elif type == "config":
            filename = 'config'
            with open(filename, 'w') as f:
                for i in range (0, len(self.config_index)):
                    f.write("{}={}\n".format(self.config_index[i], self.cfg[self.config_index[i]]))

class FSEventHandler(FileSystemEventHandler):
    def __init__(self, appwindow):
        self.appwindow = appwindow
    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        self.appwindow.loadDynamicResources(os.path.splitext(os.path.basename(event.src_path))[0])
        self.appwindow.updateCanvas()
    def on_created(self, event):
        self.process(event)
    def on_modified(self, event):
        self.process(event)
        
class AppWindow(Tk):
    def __init__(self, root=None):
        Tk.__init__(self, root)
        self.icon_base64 ="""R0lGODlhIAAgAOfYAKYAAKcAAKgAAKUBAakAAKoAAKsAAKgBAawAAK0AAK4AAKwBAa0BAa4BAa0C\nAq4DA64EBK4FBa8ICKwMDLALC60MDLEQD7IRELETE7IUFLMUFLIWFrMWFrMYF7QYGLQZGbUZGbYb\nG7UcHLYeHbYfH7YhILciIrUlJbYlJbcnJrgoJ7krKrksK7otLbouLbsxMbsyMbo0NLk1NL05OL47\nOlZXV748O1dYV7o+PcBCQbtEQ71EQ75EQ79EQ8BEQ8BERMFGRcJKSWJkY8JKSmNkZL5MS8NNTMNO\nTcRPTsRQT8RRUMVUU8VVVMdaWchdXMVfXshfXsViYcZiYcdiYchiYcliYcZjYsdjYcdjYshjYslj\nYcljYspjYcpjYspkY8tpZ8tracxsa8xubc1ubcl2ds51c891c892ddB5d8+BgNCBgNGBgNKBgNKC\ngNaBgdSGhdSJh9SJiNOLitWLitSMi9WMitWMi9aMi9ONjdWNi9aNi9eNi9eOi9mOi9iQjtiUktiW\nlNmYltmamNmbmdqcmq6urNyjodimpbGxrtmnp9iop9mop9qop9uoqN2optqpqNqpqdupqNupqdyp\nqNypqduqqdyqqdyqqt2qqd6qqN2rqd6rqd6rqt+rqd+rqt6sqd6sqt+squCsqt+tqeCtqt2urLq6\nuOCwrru7ueCysNO3ttS4uOG1stO5udW5uNW5uda5uNa6uNa6ude6uNe6ucPAv9e7udi7ueK5ttm8\nueK6t9e9usXCwNq9uePCweXDwebGxObHxNnPzdrPzOnQzufS0erU0erW0+vZ1uza1+3f3O7i4O7j\n4O/k4e/n5PDn5PHr6PHt6vHu6/Lv7PLw7fLw7vLx7vPy7///////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n/////////////////////////////////////////////////////yH5BAEKAP8ALAAAAAAgACAA\nAAj+AP8JHEiwoMGDBlH98sOHD508dujs2WOnDh07dvrokaMH4508evD4MjUQERoFCRIoICCAgIEE\nCGIiMFAAAcyZBmQiIECmkEBjCxpAYbNGTRo1bdi0abOmKdKlS5u2UfNkwIFiAi8hMHKtq9evzaqU\ncALtq9kiAioJZGSgi9mvyl6kTGDj2NuuUQhEWksgy91r1jZ1mJugRbC31qToXVsAy19kySzMlZBA\nBbO3UwgsEjipr7W7y541mTsiRIIgn79mfiSQUl9qfzNFIJzSgzSzUwQoEhipQBbYbw09MDH3iyNi\n094q3vwvEQEsyd8SQuAmpYrUd/Pu/ffJN3CzzCD+gEhp5i9eAKAEdkrg9u+SuWHMX5uCIP0/Twm2\n/E11YS4L7G9RkQAnAnGiQHtmVQMDbYOYpxiB/4iCAIJm/ZJBAgwk4MAP35mlhQGhCBRKfuaVgUAc\nW8nHRQIh/kMJAvr9BQgEznBQhXwfYiJQIwBYYV4gIlwDhBfyZbZdJAI49tcZK1wDRg7yKQZJa32Z\nB4UL18xBQTQOEmAJZ8+Zx8QM1+iCADBdSsJZkuYpkcQ10WhgiHlGCiRJAD7+hcQYXUEBh3lUGKCJ\nQKOw+dcRb3T1hxiAGkCKQKQIcIV5PwTSFStD0InAo/+UEoAMt701DQmCdIXLBwB6JU0MCJwi0DBs\nExRwAg898ODDrT3QgMAGO/CQAgI46NArD8T2gEIBFQgjEBGHYFBAAQQEIIABOSVgAEsFUEsAAAR0\nSwC0BWDAiBAD3cDLLr3kosoqrrxiyy2zzOKKK7fkAksssdAiyyuyyNJKLTUgJPDABwUEADs="""
        img = PhotoImage(data=self.icon_base64)
        self.call('wm', 'iconphoto', self._w, img)
        self.resizable(width=False, height=False)
        self.screen = ""
        self.loadStaticResources()        
        self.createWidgets()
        self.createCanvas()
        observer = Observer()
        observer.schedule(FSEventHandler(self), self.dir, recursive=False)
        observer.start()
        self.wifi_counter = 0
        self.battery_counter = 0
        self.updateCanvas(auto_loop=True)
    
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
        self.screen = "main_screen"
        self.i = {
            'battery_charging': '',
            'battery0': '',
            'battery1': '',
            'battery2': '',
            'battery3': '',
            'battery4': '',
            'battery5': '',
            'bottom_screen_bg': '',
            'bottom_screen_bottom_bar': '',
            'bottom_screen_bottom_bar_shadow': '',
            'bottom_screen_top_bar': '',
            'bottom_screen_top_bar_shadow': '',
            'button_large': '',
            'button_small': '',
            'logo': '',
            'meta_info_box': '',
            'meta_info_box_shadow': '',
            'progress_bar_bg': '',
            'progress_bar_content': '',
            'progress_bar_content_25': '',
            'progress_bar_content_50': '',
            'progress_bar_content_75': '',
            'scroll_bar': '',
            'selection_overlay': '',
            'top_screen_bg': '',
            'top_screen_bottom_bar': '',
            'top_screen_bottom_bar_shadow': '',
            'top_screen_top_bar': '',
            'top_screen_top_bar_shadow': '',
            'wifi_disconnected': '',
            'wifi0': '',
            'wifi1': '',
            'wifi2': '',
            'wifi3': ''
            }
        failed_to_load = []
        for key in self.i:
            failed_filename = self.loadDynamicResources(key)
            if failed_filename:
                failed_to_load.append("{}.png".format(failed_filename))
        if failed_to_load:
            failed_to_load.sort()
            messagebox.showwarning("Error", 'Failed to load {}/{} image(s):\n{}'.format(len(failed_to_load), len(self.i)-3, "\n".join(failed_to_load)))
        
    def loadDynamicResources(self, filename):
        try:
            if filename in ['progress_bar_content_25', 'progress_bar_content_50', 'progress_bar_content_75']: return
            elif filename == 'progress_bar_content' or filename == 'selection_overlay':
                tmp_image = Image.open("{}{}.png".format(self.dir, filename))
                if filename == 'selection_overlay':
                    tmp_image = tmp_image.resize((320, 15), Image.ANTIALIAS)
                if filename == 'progress_bar_content':
                    self.i['{}_25'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.25), 30)))
                    self.i['{}_50'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.50), 30)))
                    self.i['{}_75'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.75), 30)))
                self.i[filename] = ImageTk.PhotoImage(tmp_image)
            else:
                self.i[filename] = PhotoImage(file="{}{}.png".format(self.dir, filename))
        except Exception as e:
            return filename
        
    def createWidgets(self):
        self.frame = Frame(self)
        self.canvas = Canvas(self.frame, width=400, height=480+int(self.c['screen_gap']), bd=0, highlightthickness=0)
        self.toolbar = Frame(self.frame)
        self.main_button = Button(self.toolbar, text="Preview", command=lambda: self.changeScreen("main_screen"))
        self.item_button = Button(self.toolbar, text="Text Cfg", command=lambda: self.changeScreen("meta_screen"))
        self.screenshot_button = Button(self.toolbar, text="Screenshot", command=self.createPreview)
        self.main_button.pack(side=LEFT, fill=X)
        self.item_button.pack(side=LEFT, fill=X)
        self.screenshot_button.pack(side=LEFT, fill=X)
        self.toolbar.pack(side=TOP)
        self.canvas.bind("<Button-1>", lambda event: self.cursorMove(event, 'B1'))
        self.canvas.bind("<B1-Motion>", lambda event: self.cursorMove(event, 'B1'))
        self.canvas.bind("<Button-3>", lambda event: self.cursorMove(event, 'B3'))
        self.canvas.pack()
        self.frame.pack()
    def createPreview(self):
        x1 = self.winfo_rootx()+self.canvas.winfo_x()
        y1 = self.winfo_rooty()+self.canvas.winfo_y()
        x2 = x1+self.canvas.winfo_width()
        y2 = y1+self.canvas.winfo_height()
        coords = [x1, y1, x2, y2]
        if os.path.isfile("preview.png"):
            if not messagebox.askyesno("Warning", "Preview image already exists, do you want to overwrite?", icon='warning'):
                return
        ImageGrab.grab().crop((x1,y1,x2,y2)).save("preview.png")    
                
    def changeScreen(self, screen):
        self.screen = screen
        self.clearCanvas()
        self.updateCanvas()
        
    def cursorMove(self, event, button):
        if event.x >= 40 and event.x <= 360 and event.y >= 20+240+int(self.c['screen_gap']) and event.y <= 220+240+int(self.c['screen_gap']):
            y_pos_offset = 20+240+int(self.c['screen_gap']) #20px bottom_screen_top_bar, 240px top screen, screen_gap
            y_pos_fixed = event.y-y_pos_offset
            y_pos_binned = int(y_pos_fixed/15)
            self.canvas.coords(self.selection_overlay, (40, y_pos_binned*15+y_pos_offset))
            if self.screen == "meta_screen" and button == "B3":
                if y_pos_binned < len(self.config.color_index):
                    new_color = colorchooser.askcolor(initialcolor = self.c[self.config.color_index[y_pos_binned]]['rgb'])[1]
                    if new_color:
                        self.c[self.config.color_index[y_pos_binned]]['rgb'] = new_color
                        self.config.save_cfg_to_file("textcolor")
                        self.updateCanvas()
            if self.screen in ["sd_screen", "nand_screen", "remote_install_screen", "update_screen"] and button == "B3":
                self.changeScreen("main_screen")
            elif self.screen == "main_screen" and button == "B3":
                if y_pos_binned == 0:
                    self.changeScreen("sd_screen")
                if y_pos_binned == 1:
                    self.changeScreen("nand_screen")
                if y_pos_binned == 2:
                    self.changeScreen("nand_screen")
                if y_pos_binned == 3:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: TWL Photo')
                if y_pos_binned == 4:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: TWL Sound')
                if y_pos_binned == 5:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: Dump NAND')
                if y_pos_binned == 6:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: Titles')
                if y_pos_binned == 7:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: Pending Titles')
                if y_pos_binned == 8:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: Tickets')
                if y_pos_binned == 9:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: Ext Save Data')
                if y_pos_binned == 10:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: System Save Data')
                if y_pos_binned == 11:
                    messagebox.showwarning('Not Implemented Yet', 'Preview not implemented yet: TitleDB')
                if y_pos_binned == 12:
                    self.changeScreen("remote_install_screen")
                if y_pos_binned == 13:
                    self.changeScreen("update_screen")
                    
    def createCanvas(self):
        self.font_normal = font.Font(family='Arial', size=-12, weight="bold")
        self.font_mini = font.Font(family='Arial', size=7, weight="bold")
        x_offset = 40
        y_offset = 240+int(self.c['screen_gap'])
                
        #Layer 0 (Background images)
        self.top_screen_bg = self.canvas.create_image(0, 0, anchor = NW, image="")
        self.bottom_screen_bg = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image="")
        
        #Layer 1 (Main information)
        ###Main Menu Screen
        self.logo = self.canvas.create_image(200, 120, image="")
        line_height = 15
        line_offset = 20
        self.bottom_screen_justified_text = self.canvas.create_text(160+x_offset, 100+line_offset+y_offset, justify='center', font=self.font_normal, text = "")
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
        ###Button Screen
        self.button_large = self.canvas.create_image(10+x_offset, 155+y_offset, anchor = NW, image="")
        self.button_small_yes = self.canvas.create_image(10+x_offset, 155+y_offset, anchor = NW, image="")
        self.button_small_no = self.canvas.create_image(165+x_offset, 155+y_offset, anchor = NW, image="")
        self.button_text = self.canvas.create_text(200, 184+y_offset, text="")
        
        #Layer 2 (Top bars)
        self.top_screen_top_bar = self.canvas.create_image(0, 0, anchor = NW, image="")
        self.top_screen_bottom_bar = self.canvas.create_image(0, 220, anchor = NW, image="")
        self.top_screen_top_bar_shadow = self.canvas.create_image(0, 20, anchor = NW, image="")
        self.top_screen_bottom_bar_shadow = self.canvas.create_image(0, 204, anchor = NW, image="")
        #Layer 2 (Bottom bars)
        self.bottom_screen_top_bar = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image="")
        self.bottom_screen_bottom_bar = self.canvas.create_image(0+x_offset, 220+y_offset, anchor = NW, image="")
        self.bottom_screen_top_bar_shadow = self.canvas.create_image(0+x_offset, 20+y_offset, anchor = NW, image="")
        self.bottom_screen_bottom_bar_shadow = self.canvas.create_image(0+x_offset, 204+y_offset, anchor = NW, image="")
        
        #Layer 3 (Top bar overlays)
        self.wifi = self.canvas.create_image(347, 2, anchor = NW, image="")
        self.battery = self.canvas.create_image(371, 2, anchor = NW, image="")
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
        self.canvas.itemconfig(self.bottom_screen_justified_text, text = "")
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
        #remote_install_screen
        self.canvas.itemconfig(self.progress_bar_bg, image="")
        self.canvas.itemconfig(self.progress_bar_content, image="")
        #button screen
        self.canvas.itemconfig(self.button_large, image="")
        self.canvas.itemconfig(self.button_small_yes, image="")
        self.canvas.itemconfig(self.button_small_no, image="")
        self.canvas.itemconfig(self.button_text, text = "")
        
    def updateCanvas(self, auto_loop=False):
        #Top screen update
        self.canvas.itemconfig(self.top_screen_bg, image=self.i['top_screen_bg'])
        self.canvas.itemconfig(self.top_screen_top_bar, image=self.i['top_screen_top_bar'])
        self.canvas.itemconfig(self.top_screen_bottom_bar, image=self.i['top_screen_bottom_bar'])
        self.canvas.itemconfig(self.top_screen_top_bar_shadow, image=self.i['top_screen_top_bar_shadow'])
        self.canvas.itemconfig(self.top_screen_bottom_bar_shadow, image=self.i['top_screen_bottom_bar_shadow'])
        
        #Bottom screen update
        self.canvas.itemconfig(self.bottom_screen_bg, image=self.i['bottom_screen_bg'])
        self.canvas.itemconfig(self.bottom_screen_top_bar, image=self.i['bottom_screen_top_bar'])
        self.canvas.itemconfig(self.bottom_screen_bottom_bar, image=self.i['bottom_screen_bottom_bar'])
        self.canvas.itemconfig(self.bottom_screen_top_bar_shadow, image=self.i['bottom_screen_top_bar_shadow'])
        self.canvas.itemconfig(self.bottom_screen_bottom_bar_shadow, image=self.i['bottom_screen_bottom_bar_shadow'])
        
        #Text update
        self.canvas.itemconfig(self.version_number, fill=self.c['text']['rgb'], text = "Ver. {}".format(self.c['theme_version']))
        self.canvas.itemconfig(self.system_info, fill=self.c['text']['rgb'], text = "SD: {} GiB, CTR NAND: {} MiB, TWL NAND: {} MiB, TWL Photo: {} MiB".format(self.sd_ex, self.ctrnand_ex, self.twlnand_ex, self.twlphoto_ex))
        
        #Reload screen specific text and images
        if self.screen == "main_screen":
            self.canvas.itemconfig(self.logo, image=self.i['logo'])
            self.canvas.itemconfig(self.selection_overlay, image=self.i['selection_overlay'])
            self.canvas.itemconfig(self.scroll_bar, image=self.i['scroll_bar'])
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text']['rgb'], text = "Main Menu")
            self.canvas.itemconfig(self.bottom_screen_listing01, fill=self.c['text']['rgb'], text = "SD")
            self.canvas.itemconfig(self.bottom_screen_listing02, fill=self.c['text']['rgb'], text = "CTR NAND")
            self.canvas.itemconfig(self.bottom_screen_listing03, fill=self.c['text']['rgb'], text = "TWL NAND")
            self.canvas.itemconfig(self.bottom_screen_listing04, fill=self.c['text']['rgb'], text = "TWL Photo")
            self.canvas.itemconfig(self.bottom_screen_listing05, fill=self.c['text']['rgb'], text = "TWL Sound")
            self.canvas.itemconfig(self.bottom_screen_listing06, fill=self.c['text']['rgb'], text = "Dump NAND")
            self.canvas.itemconfig(self.bottom_screen_listing07, fill=self.c['text']['rgb'], text = "Titles")
            self.canvas.itemconfig(self.bottom_screen_listing08, fill=self.c['text']['rgb'], text = "Pending Titles")
            self.canvas.itemconfig(self.bottom_screen_listing09, fill=self.c['text']['rgb'], text = "Tickets")
            self.canvas.itemconfig(self.bottom_screen_listing10, fill=self.c['text']['rgb'], text = "Ext Save Data")
            self.canvas.itemconfig(self.bottom_screen_listing11, fill=self.c['text']['rgb'], text = "System Save Data")
            self.canvas.itemconfig(self.bottom_screen_listing12, fill=self.c['text']['rgb'], text = "TitleDB")
            self.canvas.itemconfig(self.bottom_screen_listing13, fill=self.c['text']['rgb'], text = "Remote Install")
            self.canvas.itemconfig(self.bottom_screen_listing14, fill=self.c['text']['rgb'], text = "Update")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text']['rgb'], text = "A: Select, START: Exit")
        if self.screen == "sd_screen":
            self.canvas.itemconfig(self.selection_overlay, image=self.i['selection_overlay'])
            self.canvas.itemconfig(self.scroll_bar, image=self.i['scroll_bar'])
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text']['rgb'], text = "Files")
            self.canvas.itemconfig(self.bottom_screen_listing01, fill=self.c['directory']['rgb'], text = "<current directory>")
            self.canvas.itemconfig(self.bottom_screen_listing02, fill=self.c['directory']['rgb'], text = "3ds")
            self.canvas.itemconfig(self.bottom_screen_listing03, fill=self.c['directory']['rgb'], text = "CIAs")
            self.canvas.itemconfig(self.bottom_screen_listing04, fill=self.c['directory']['rgb'], text = "fbi")
            self.canvas.itemconfig(self.bottom_screen_listing05, fill=self.c['directory']['rgb'], text = "hblauncherloader")
            self.canvas.itemconfig(self.bottom_screen_listing06, fill=self.c['directory']['rgb'], text = "JKSV")
            self.canvas.itemconfig(self.bottom_screen_listing07, fill=self.c['directory']['rgb'], text = "luma")
            self.canvas.itemconfig(self.bottom_screen_listing08, fill=self.c['directory']['rgb'], text = "Nintendo3DS")
            self.canvas.itemconfig(self.bottom_screen_listing09, fill=self.c['file']['rgb'], text = "arm9loaderhax.bin")
            self.canvas.itemconfig(self.bottom_screen_listing10, fill=self.c['file']['rgb'], text = "boot.3dsx")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text']['rgb'], text = "A: Select, B: Back, X: Refresh, Select: Options")
        if self.screen == "nand_screen":
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text']['rgb'], text = "Confirmation")
            self.canvas.itemconfig(self.bottom_screen_justified_text, fill=self.c['text']['rgb'], text = "Modifying the NAND is dangerous and can render\nthe system inoperable.\nMake sure you know what you are doing.\n\nProceed?")
            self.canvas.itemconfig(self.button_small_yes, image=self.i['button_small'])
            self.canvas.itemconfig(self.button_small_no, image=self.i['button_small'])
            self.canvas.itemconfig(self.button_text, fill=self.c['text']['rgb'], text = "Yes (A)                                        No (B)")
        if self.screen == "remote_install_screen":
            self.canvas.itemconfig(self.progress_bar_bg, image=self.i['progress_bar_bg'])
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text']['rgb'], text = "Installing From URL(s)")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text']['rgb'], text = "Press B to cancel.")
        if self.screen == "update_screen":
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=self.c['text']['rgb'], text = "Success")
            self.canvas.itemconfig(self.bottom_screen_justified_text, fill=self.c['text']['rgb'], text = "No updates available.")
            self.canvas.itemconfig(self.button_large, image=self.i['button_large'])
            self.canvas.itemconfig(self.button_text, fill=self.c['text']['rgb'], text = "Okay (Any Button)")
        if self.screen == "meta_screen":
            self.canvas.itemconfig(self.meta_info_box, image=self.i['meta_info_box'])
            self.canvas.itemconfig(self.meta_info_box_shadow, image=self.i['meta_info_box_shadow'])
            self.canvas.itemconfig(self.meta_info_icon, image=self.i_meta_info_icon)
            self.canvas.itemconfig(self.meta_info_box_info, fill=self.c['text']['rgb'], text = "{}\n{}\n{}".format(self.c['theme_title'], self.c['theme_desc'], self.c['theme_author']))
            self.canvas.itemconfig(self.meta_info_info, fill=self.c['text']['rgb'], text = "Title ID: 0004000000FBIP00\nMedia Type: SD\nVersion: 0\nProduct Code: CTR-P-FBIP\nRegion: North America\nSize: 1.56 GiB")
            self.canvas.itemconfig(self.selection_overlay, image=self.i['selection_overlay'])
            self.canvas.itemconfig(self.scroll_bar, image=self.i['scroll_bar'])
            self.canvas.itemconfig(self.bottom_screen_top_bar_text,    fill=self.c['text']['rgb'],           text = "Textcolor.cfg (#BGR)")
            self.canvas.itemconfig(self.bottom_screen_listing01,       fill=self.c['text']['rgb'],           text = "{}{}".format("Default".ljust(43),           swapRGBBGR(self.c['text']['rgb']).rjust(42))  )
            self.canvas.itemconfig(self.bottom_screen_listing02,       fill=self.c['nand']['rgb'],           text = "{}{}".format("NAND".ljust(43),              swapRGBBGR(self.c['nand']['rgb']).rjust(42))  )
            self.canvas.itemconfig(self.bottom_screen_listing03,       fill=self.c['sd']['rgb'],             text = "{}{}".format("SD".ljust(45),                swapRGBBGR(self.c['sd']['rgb']).rjust(44))  )
            self.canvas.itemconfig(self.bottom_screen_listing04,       fill=self.c['gamecard']['rgb'],       text = "{}{}".format("Gamecard".ljust(40),          swapRGBBGR(self.c['gamecard']['rgb']).rjust(40))  )
            self.canvas.itemconfig(self.bottom_screen_listing05,       fill=self.c['dstitle']['rgb'],        text = "{}{}".format("DS Title".ljust(43),          swapRGBBGR(self.c['dstitle']['rgb']).rjust(42))  )
            self.canvas.itemconfig(self.bottom_screen_listing06,       fill=self.c['file']['rgb'],           text = "{}{}".format("File".ljust(45),              swapRGBBGR(self.c['file']['rgb']).rjust(44))  )
            self.canvas.itemconfig(self.bottom_screen_listing07,       fill=self.c['directory']['rgb'],      text = "{}{}".format("Directory".ljust(42),         swapRGBBGR(self.c['directory']['rgb']).rjust(41))  )
            self.canvas.itemconfig(self.bottom_screen_listing08,       fill=self.c['enabled']['rgb'],        text = "{}{}".format("Enabled".ljust(42),           swapRGBBGR(self.c['enabled']['rgb']).rjust(41))  )
            self.canvas.itemconfig(self.bottom_screen_listing09,       fill=self.c['disabled']['rgb'],       text = "{}{}".format("Disabled".ljust(42),          swapRGBBGR(self.c['disabled']['rgb']).rjust(41))  )
            self.canvas.itemconfig(self.bottom_screen_listing10,       fill=self.c['installed']['rgb'],      text = "{}{}".format("Installed".ljust(42),         swapRGBBGR(self.c['installed']['rgb']).rjust(42))  )
            self.canvas.itemconfig(self.bottom_screen_listing11,       fill=self.c['notinstalled']['rgb'],   text = "{}{}".format("Not installed".ljust(41),     swapRGBBGR(self.c['notinstalled']['rgb']).rjust(40))  )
            self.canvas.itemconfig(self.bottom_screen_listing12,       fill=self.c['ticketinuse']['rgb'],    text = "{}{}".format("Ticket in use".ljust(40),     swapRGBBGR(self.c['ticketinuse']['rgb']).rjust(40))  )
            self.canvas.itemconfig(self.bottom_screen_listing13,       fill=self.c['ticketnotinuse']['rgb'], text = "{}{}".format("Ticket not in use".ljust(39), swapRGBBGR(self.c['ticketnotinuse']['rgb']).rjust(38))  )
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=self.c['text']['rgb'],           text = "A: Select, B: Return, X: Refresh")
        y_offset = 240+int(self.c['screen_gap'])
        self.canvas.coords(self.bottom_screen_justified_text, 160+40, (135/2)+20+y_offset)
        if auto_loop:
            self.updateAnim(auto_loop=True)

    def updateAnim(self, auto_loop=False):
        #Time Date
        self.canvas.itemconfig(self.date_time, fill=self.c['text']['rgb'], text = "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()))
        #Wifi Battery Progress bar
        wifi_icon = [self.i['wifi_disconnected'], self.i['wifi0'], self.i['wifi1'], self.i['wifi2'], self.i['wifi3']]
        battery_icon = [self.i['battery_charging'], self.i['battery0'], self.i['battery1'], self.i['battery2'], self.i['battery3'], self.i['battery4'], self.i['battery5']]
        progress_icon = ["", self.i['progress_bar_content_25'], self.i['progress_bar_content_50'], self.i['progress_bar_content_75'], self.i['progress_bar_content']]
        if self.wifi_counter >= 4:
            self.wifi_counter = 0
        else:
            self.wifi_counter += 1
        
        if self.battery_counter >= 6:
            self.battery_counter = 0
        else:
            self.battery_counter += 1
        self.canvas.itemconfig(self.wifi, image=wifi_icon[self.wifi_counter])
        self.canvas.itemconfig(self.battery, image=battery_icon[self.battery_counter])
        if self.screen == "remote_install_screen":
            self.canvas.itemconfig(self.progress_bar_content, image=progress_icon[self.wifi_counter])
        if auto_loop:
            self.canvas.after(1000, lambda: self.updateAnim(auto_loop=True))
            
def swapRGBBGR(color):
    if len(color) == 7:
        color = color[1:]
    color_list = [color[i:i+2] for i in range(0, len(color), 2)]
    color1 = color_list[0]
    color2 = color_list[1]
    color3 = color_list[2]
    return "#{}{}{}".format(color3,color2,color1).upper()

app = AppWindow()
app.mainloop()