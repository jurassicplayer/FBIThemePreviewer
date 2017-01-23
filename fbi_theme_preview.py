#!/usr/bin/python

#tkinter bindings
import tkinter as tk
from tkinter import font, filedialog, messagebox, colorchooser, StringVar
#watchdog bindings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#pillow bindings
from PIL import Image, ImageTk, ImageDraw, ImageGrab, ImageFont
from io import BytesIO
import base64
#File name/path manipulation
import os
#RNG for generated values
import random
#clock
import datetime
#Checking if string is valid ARGB
import re
#Pretty print dicts during debug
from pprint import pprint as p

class AppWindow(tk.Tk):
    def __init__(self, root=None):
        print("Started Execution")
        tk.Tk.__init__(self, root)
        self.setupApp()
        self.setupVariables()
        self.loadConfig(self.app_config, 'config')
        self.loadFont(self.app_config['font_path'])
        self.setupWidget()
        if self.app_config['meta_icon']:
            self.loadCustomMetaIcon(self.app_config['meta_icon'])
        self.loadTheme(self.app_config['theme_folder'])
        self.rebuildCache()
        self.updateCanvas()
        self.updateAnimationLoop(loop=True)
    
    def setupApp(self):
        print("Setting up main window...")
        self.icon_base64 = {
            'app' : """iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAp0lEQVRo3u3aoQ0CURBF0fsJ0A0VUMM2gFmFRBAIBr2GQBBI1BoaoAYqoBsQgyCIZR2CZJL75ORn/jt+SkQEiTMEKKWkLB8RbwBAPZ0AcFg+AVgdR53Hj3nDYr/htN71Fl3q6qcCs/bam33+GJ+3nfl3r/Z2B2BA8ggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAEC/pkSEZH+2CPzxc0LSCMmWnbVMHAAAAAASUVORK5CYII=""",
            'fbi' : """iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAlElEQVRYw+2YSw6AIAxEqeH+Vx5XJvhBVCyIebMitcpLRwoaAkJobFnugiQ1gzDLcsTCje5wpTrE2gdUVq6YM339HQQQQABHB4x3ko/6lqRdfOmduXw3wLMJ0riZBUkr0KcN/18Wb23bVs1je3S1mFVca30aW8auq/iKvW8f1dhJAAQQwN6NusW38WPAhj8XEEKol2b2bkM1u6bHlAAAAABJRU5ErkJggg==""",
            'textcolor' : """iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAABIklEQVRYw+2YUQ7CMAiGYfFi3kRvUr2IL72Hnozfh6Vba7p2sZDwUBJCzLb084cNWgZAnm0h5zYBJ+AEnIDGdundwMymX3IA3Fy/1UmY2bzPcAdyacDtP6JtLNaqSFz17XIkwDDS6ocsfUBjyL8Bc8gzfqDMGW9mcum8YamOe16vMSJG7D/bHPlaCp71pKDIHpM6ImNrqAHmcHltIToBtFKQNUZ+ZobIzwd2rW4WIRppRmq9+Mll1OyFajUYsMeU4gAnNZjDadag6rhVS/NwyjUVpIAtbl0iwEeKczi3NWihoFoNhgeK6G5P8nqX0R3g/brCpfgL7kLBHDIHd7PtrKXZjYJHdvsMDiJaB5iV/bPOpKR5wppvH9X++DwCnoATsG1fA0G6TzK0GV0AAAAASUVORK5CYII=""",
            'screenshot' : """iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAr0lEQVRYw+2XOw7AIAxDCcr9r5wuVEKolJAPYvBbWGgxJnFpKQAAAK6GVhNERMIXJSLtXFa+MEzc7n5rxrG8IvrRehCcUjfN8XFMFRhRihah9fYuhkAITIofCe/iyABvuSiaLwp7xFmjZ+dZd1D3JoyLjgZZNsRZ9fblksV1jir8lcPWcrg+ZvhUtKQL/GuGmbBjTWJ1IeQGZFxYvEGtvfqTo7Zc9lDkfwQAAAAw5QFkJVklKZGd2AAAAABJRU5ErkJggg==""",
            'opendir' : """iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAbElEQVRYw+2WMQ4AIAjEwPj/L+Pk7JGAOrQzwYoXgxkAAHyNK0UREVIzd78uuOVOZ+87VEtOcTJ2GqJS0yaYoToO0hNXRysTh5ltWhL8RBzG798MgggiiCCCCCL4Fnmbadjm6wQ7NmUAAIA7LC2EJS/bJR+TAAAAAElFTkSuQmCC""",
            'save' : """iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAk0lEQVRYw+2XzQ4AEQyEjXj/V+6eSCN76BYldr6TIEzG+EuJEELI0cDaUURkeDIASwRWcY7x9RgukWaBAFJv4ludrtftXdksMkdlqQr+GpccGXgtcqvACfupUVY6MkNoOcmt7Rm8UqBriT0HtjcKJSJ7IzfQnUtsdecXxwwdpIO7HQx7UXtf1qF/kpG/CSGEEOLjAb/NVySMpPXIAAAAAElFTkSuQmCC""",
            }
        self.icon = {
            'app'        : Image.open(BytesIO(base64.b64decode(self.icon_base64['app']))),
            'fbi'        : tk.PhotoImage(data=self.icon_base64['fbi']),
            'textcolor'  : tk.PhotoImage(data=self.icon_base64['textcolor']),
            'screenshot' : tk.PhotoImage(data=self.icon_base64['screenshot']),
            'opendir'    : tk.PhotoImage(data=self.icon_base64['opendir']),
            'save'       : tk.PhotoImage(data=self.icon_base64['save']),
            }
        app_icon = ImageTk.PhotoImage(self.icon['app'])
        self.call('wm', 'iconphoto', self._w, app_icon)
        self.resizable(width=False, height=False)
        self.title('FBI Theme Previewer')
    def setupVariables(self):
        print("Setting up program variables...")
        self.observer = Observer()
        self.observer.start()
        self.app_config = {
            'theme_folder'  : "romfs/",
            'theme_title'   : "FBI Theme Previewer",
            'theme_desc'    : "A Shit Tier Stop-gap Solution",
            'theme_author'  : "Jurassicplayer",
            'theme_version' : "2.4.7",
            'font_path'     : "font/RodinBokutoh_DB.otf",
            'meta_icon'     : '',
            'screen_gap'    : 0, #68
            'anim_duration' : 1, #In seconds
            'overwrite'     : 'never', #never/preview/textcolor/always
            }
        self.text_config = {
            'text':           (0,0,0,255),
            'nand':           (0,0,0,255),
            'sd':             (0,0,0,255),
            'gamecard':       (0,0,0,255),
            'dstitle':        (0,0,0,255),
            'file':           (0,0,0,255),
            'directory':      (0,0,0,255),
            'enabled':        (0,0,0,255),
            'disabled':       (0,0,0,255),
            'installed':      (0,0,0,255),
            'notinstalled':   (0,0,0,255),
            'ticketinuse':    (0,0,0,255),
            'ticketnotinuse': (0,0,0,255),
            }
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
        self.v = {
            'current_screen'     : 'main_screen',
            'previous_screen'    : 'main_screen',
            'selection_position' : 0,
            'sd_ex'              : 64.1,
            'ctrnand_ex'         : 328.7,
            'twlnand_ex'         : 128.8,
            'twlphoto_ex'        : 32.4,
            'top_screen'         : '',
            'bottom_screen'      : '',
            'canvas_image'       : '',
            'd_top_screen'       : '',
            'd_bottom_screen'    : '',
            'font_normal'        : '',
            'font_mini'          : '',
            }
        self.v.update({
            'top_screen'         : Image.new('RGBA', (400,240), (255,255,255,0)),
            'bottom_screen'      : Image.new('RGBA', (320,240), (255,255,255,0)),
            'canvas_image'       : Image.new('RGBA', (400,self.app_config['screen_gap']+480), (255,255,255,0)),
            })
        self.v.update({
            'd_top_screen'       : ImageDraw.Draw(self.v['top_screen']),
            'd_bottom_screen'    : ImageDraw.Draw(self.v['bottom_screen']),
            })
        self.c = {
                'textcolor_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'main_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'sd_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'nand_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'options_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'titles_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'ticket_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'titledb_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'remote_install_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
                'success_screen' : {
                        'top_screen' : '',
                        'bottom_screen' : '',
                    },
            }
    def setupWidget(self):
        print("Setting up main widget...")
        self.frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame, width=400, height=480+int(self.app_config['screen_gap']), 
        borderwidth=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", lambda event: self.cursorEvent(event, 'B1'))
        self.canvas.bind("<B1-Motion>", lambda event: self.cursorEvent(event, 'B1'))
        self.canvas.bind("<Button-3>", lambda event: self.cursorEvent(event, 'B3'))
        self.canvas.pack()
        self.active = StringVar()
        self.active.set("main_screen")
        radio_size = 38
        button_size = 40
        
        self.fbipreview_button = tk.Radiobutton(self, width=radio_size, height=radio_size, borderwidth=0, highlightthickness=0, indicatoron=0, offrelief='flat', overrelief='flat', value="main_screen", variable=self.active, image=self.icon['fbi'], command=lambda: self.changeScreen(self.v['previous_screen']))
        self.textcolor_button = tk.Radiobutton(self, width=radio_size, height=radio_size, borderwidth=0, highlightthickness=0, indicatoron=0, offrelief='flat', overrelief='flat', value="textcolor_screen", variable=self.active, image=self.icon['textcolor'], command=lambda: self.changeScreen("textcolor_screen"))
        self.screenshot_button = tk.Button(self, width=button_size, height=button_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['screenshot'], command=self.savePreview)
        self.opendir_button = tk.Button(self, width=button_size, height=button_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['opendir'], command=self.openTheme)
        self.save_button = tk.Button(self, width=button_size, height=button_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['save'], command=lambda: self.saveConfig("textcolor"))
        
        #Slider bars 
        config_array = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
        self.sliders = {}
        for i in range(len(config_array)):
            color_key = config_array[i]
            slider_var = tk.IntVar()
            label = tk.Label(self.frame,font=("Arial", 7), borderwidth=0, highlightthickness=0, padx=0, pady=0, textvariable=slider_var)
            label.place(x=40+180, y=i*15+2+20+240+self.app_config['screen_gap'])
            scale = tk.Scale(self.frame, orient='horizontal', length=100, width=11, sliderlength=8, from_=0, to=255, showvalue=0, borderwidth=0, variable=slider_var, highlightthickness=0, relief='flat')
            self.sliders.update({color_key: [scale, label]})
        for key in ["<ButtonRelease-1>", "<ButtonRelease-3>"]:
            self.sliders['text'][0].bind(key, lambda e: self.updateAlpha('text'))
            self.sliders['nand'][0].bind(key, lambda e: self.updateAlpha('nand'))
            self.sliders['sd'][0].bind(key, lambda e: self.updateAlpha('sd'))
            self.sliders['gamecard'][0].bind(key, lambda e: self.updateAlpha('gamecard'))
            self.sliders['dstitle'][0].bind(key, lambda e: self.updateAlpha('dstitle'))
            self.sliders['file'][0].bind(key, lambda e: self.updateAlpha('file'))
            self.sliders['directory'][0].bind(key, lambda e: self.updateAlpha('directory'))
            self.sliders['enabled'][0].bind(key, lambda e: self.updateAlpha('enabled'))
            self.sliders['disabled'][0].bind(key, lambda e: self.updateAlpha('disabled'))
            self.sliders['installed'][0].bind(key, lambda e: self.updateAlpha('installed'))
            self.sliders['notinstalled'][0].bind(key, lambda e: self.updateAlpha('notinstalled'))
            self.sliders['ticketinuse'][0].bind(key, lambda e: self.updateAlpha('ticketinuse'))
            self.sliders['ticketnotinuse'][0].bind(key, lambda e: self.updateAlpha('ticketnotinuse'))
        self.frame.pack()
    def updateAlpha(self, color_key):
        value = self.sliders[color_key][0].get()
        print('Updating cache with new text alpha {}...'.format(value))
        r,g,b,a = self.text_config[color_key]
        self.text_config[color_key] = (r,g,b,int(value))
        cache_array =['textcolor_screen']
        screen_refresh = 'bottom'
        if color_key == 'text':
            cache_array += ['main_screen', 'sd_screen', 'nand_screen', 'options_screen', 'titles_screen', 'titledb_screen', 'ticket_screen', 'remote_install_screen', 'success_screen']
            screen_refresh='topbottom'
        elif color_key in ['nand', 'sd', 'gamecard', 'dstitle']:
            cache_array += ['titles_screen']
        elif color_key in ['file', 'directory']:
            cache_array += ['sd_screen', 'nand_screen', 'options_screen', 'titles_screen', 'titledb_screen', 'ticket_screen', 'remote_install_screen', 'success_screen']
        elif color_key in ['enabled', 'disabled']:
            cache_array += ['options_screen']
        elif color_key in ['installed', 'notinstalled']:
            cache_array += ['titledb_screen']
        elif color_key in ['ticketinuse', 'ticketnotinuse']:
            cache_array += ['ticket_screen']
        for screen_name in cache_array:
            self.drawCanvasCache(screen_name, screen=screen_refresh)
            self.updateCanvas()
    def loadFont(self, filepath):
        if os.path.isfile(filepath):
            self.v['font_normal'] = ImageFont.truetype(filepath, 12)
            self.v['font_mini'] = ImageFont.truetype(filepath, 9)
        else:
            try:
                self.v['font_normal'] = ImageFont.truetype("arialbd.ttf", 12)
                self.v['font_mini'] = ImageFont.truetype("arialbd.ttf", 9)
            except:
                self.v['font_normal'] = ImageFont.load_default()
                self.v['font_mini'] = ImageFont.load_default()
    def loadConfig(self, config_dict, filename, argb_check=False):
        print("Loading config: {}".format(filename))
        if os.path.isfile(filename):
            with open(filename) as f:
                config_content = [line.rstrip('\n') for line in f]
            malformed_color = []
            for key in config_dict:
                for line in config_content:
                    value = line.split("=")[1]
                    if key == line.split("=")[0]:
                        if argb_check:
                            argbstring = re.compile(r'[a-fA-F0-9]{8}$')
                            if argbstring.match(value):
                                a, b, g, r = tuple([value[i:i+2] for i in range(0, len(value), 2)])
                                config_dict.update({key : (int(r, 16), int(g, 16), int(b, 16), int(a, 16)) })
                                self.sliders[key][0].set(int(a, 16))
                            else:
                                malformed_color.append(line)
                        else:
                            if key == "screen_gap" or key == "anim_duration":
                                try:
                                    value = int(value)
                                except:
                                    value = config_dict[key]
                            config_dict.update({key : value})
            if malformed_color:
                malformed_color.sort()
                messagebox.showwarning("Error", "Malformed text color (ABGR):\n{}".format('\n'.join(malformed_color)))
    def loadTheme(self, folderpath):
        print("Loading theme: {}".format(folderpath))
        self.observer.unschedule_all()
        if os.path.isdir(folderpath):
            self.app_config['theme_folder'] = folderpath
            self.loadConfig(self.text_config, os.path.join(folderpath,'textcolor.cfg'), argb_check=True)
            failed_to_load = []
            for key in self.i:
                failed_filename = self.loadImage(folderpath, key)
                if failed_filename:
                    failed_to_load.append("{}.png".format(failed_filename))
            if failed_to_load:
                failed_to_load.sort()
                messagebox.showwarning("Error", 'Failed to load {}/{} image(s):\n{}'.format(len(failed_to_load), len(self.i)-3, "\n".join(failed_to_load)))
            self.observer.schedule(FSEventHandler(self), folderpath, recursive=False)
            self.rebuildCache()
        else:
            messagebox.showwarning("Error", 'Theme path not found:\n{}'.format(folderpath))
    def loadImage(self, folderpath, filename):
        print("Loading image: {}".format(os.path.join(folderpath, "{}.png".format(filename))))
        try:
            filepath = os.path.join(folderpath, "{}.png".format(filename))
            self.i[filename] = Image.open(filepath).convert('RGBA')
            if filename == 'selection_overlay':
                self.i[filename] = self.i[filename].resize((320, 15), Image.ANTIALIAS)
                self.i[filename] = ImageTk.PhotoImage(self.i[filename])
        except Exception as e:
            return filename
    def openTheme(self):
        print("Opening ask directory dialog...")
        new_dir = tk.filedialog.askdirectory(initialdir='.', mustexist=True)
        if new_dir:
            new_dir = os.path.relpath(new_dir)
            self.loadTheme(new_dir)
            self.updateCanvas()
    def openCustomMetaIcon(self):
        print("Opening ask open file dialog...")
        new_icon = tk.filedialog.askopenfilename(initialdir='.', filetypes=[('image files', '.png')])
        if new_icon:
            new_icon = os.path.relpath(new_icon)
            self.loadCustomMetaIcon(new_icon)
            self.updateCanvas()
    def loadCustomMetaIcon(self, filepath):
        print("Loading custom meta icon: {}".format(filepath))
        if os.path.isfile(filepath):
            self.icon['app'] = Image.open(filepath).convert('RGBA')
            for screen in ['textcolor_screen', 'titles_screen', 'titledb_screen']:
                self.drawCanvasCache(screen, screen='top')
    def loadCustomColor(self):
        color_index = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
        if self.v['selection_position'] < len(color_index):
            r,g,b,a = self.text_config[color_index[self.v['selection_position']]]
            new_color = colorchooser.askcolor(initialcolor =(r,g,b))[0]
            if new_color:
                r,g,b = new_color
                self.text_config[color_index[self.v['selection_position']]] = (int(r),int(g),int(b),a)
                self.rebuildCache()
                self.updateCanvas()
    def changeScreen(self, screen):
        print("Changing screens: {} => {}".format(self.v['current_screen'], screen))
        if screen == "textcolor_screen" and not self.v['current_screen'] == "textcolor_screen":
            self.v['previous_screen'] = self.v['current_screen']
        elif not screen == "textcolor_screen" and not self.v['current_screen'] == "textcolor_screen":
            self.v['previous_screen'] = screen
        self.v['current_screen'] = screen
        self.updateCanvas()
    def saveConfig(self, config_type):
        print("Saving config: {}".format(config_type))
        if config_type == "config":
            filepath = "config"
            config_dict = self.app_config
            ordered = ['theme_folder', 'theme_title', 'theme_desc', 'theme_author', 'theme_version', 'meta_icon', 'screen_gap', 'anim_duration', 'overwrite', 'language']
        elif config_type == "textcolor":
            theme_folder = self.app_config['theme_folder']
            os.makedirs(theme_folder, exist_ok=True)
            filepath = os.path.join(theme_folder,'textcolor.cfg')
            config_dict={}
            for key in self.text_config:
                r,g,b,a = self.text_config[key]
                value = "{:02x}{:02x}{:02x}{:02x}".format(a,b,g,r).upper()
                config_dict.update({key: value})
            ordered = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
            if os.path.isfile(filepath) and not self.app_config['overwrite'] in ['always', 'textcolor']:
                if not messagebox.askyesno("Warning", "A textcolor.cfg already exists, do you want to overwrite?", icon='warning'):
                    return
        with open(filepath, 'w') as f:
            for key in ordered:
                f.write("{}={}\n".format(key, config_dict[key]))
            f.truncate(f.tell() - len(os.linesep))
    def savePreview(self):
        print("Generating preview image...")
        x1 = self.winfo_rootx()+self.canvas.winfo_x()
        y1 = self.winfo_rooty()+self.canvas.winfo_y()
        x2 = x1+self.canvas.winfo_width()
        y2 = y1+self.canvas.winfo_height()
        coords = [x1, y1, x2, y2]
        if os.path.isfile("preview.png") and not self.app_config['overwrite'] in ['always', 'preview']:
            if not messagebox.askyesno("Warning", "Preview image already exists, do you want to overwrite?", icon='warning'):
                return
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
        self.canvas.delete('toolbar')
        self.canvas.update_idletasks()
        ImageGrab.grab().crop((x1,y1,x2,y2)).save("preview.png")
        #self.v['canvas_image'].save("preview.png")
        self.updateCanvas()
    def cursorEvent(self, event, button):
        #print("Handling cursor event: {}".format(button))
        #Top screen handling
        if event.x >= 48 and event.x <= 96 and event.y >= 46 and event.y <= 94:
            if self.v['current_screen'] in ["textcolor_screen", "titles_screen", "titledb_screen"] and button == "B3":
                self.openCustomMetaIcon()
        #Bottom screen handling
        y_pos_offset = 20+240+int(self.app_config['screen_gap']) #20px bottom_screen_top_bar, 240px top screen, self.app_config['screen_gap']
        if event.x >= 40 and event.x <= 360 and event.y >= y_pos_offset and event.y <= 194+y_pos_offset:
            y_pos_fixed = event.y-y_pos_offset
            self.v['selection_position'] = y_pos_binned = int(y_pos_fixed/15)
            self.canvas.coords(self.selection_overlay, (40, y_pos_binned*15+y_pos_offset))
            if self.v['current_screen'] == "textcolor_screen" and button == "B3":
                self.loadCustomColor()
            if self.v['current_screen'] in ["sd_screen", "nand_screen", "options_screen", "titles_screen", "ticket_screen", "titledb_screen", "remote_install_screen", "success_screen"] and button == "B3":
                self.changeScreen("main_screen")
            elif self.v['current_screen'] == "main_screen" and button == "B3":
                if y_pos_binned == 0:
                    self.changeScreen("sd_screen")
                if y_pos_binned == 1:
                    self.changeScreen("nand_screen")
                if y_pos_binned == 2:
                    print('TWL NAND')
                    #self.changeScreen("nand_screen")
                if y_pos_binned == 3:
                    self.changeScreen("options_screen")
                if y_pos_binned == 4:
                    print('TWL Sound')
                    #self.changeScreen("options_screen")
                if y_pos_binned == 5:
                    self.changeScreen("success_screen")
                if y_pos_binned == 6:
                    self.changeScreen("titles_screen")
                if y_pos_binned == 7:
                    print('Pending Titles')
                if y_pos_binned == 8:
                    self.changeScreen("ticket_screen")
                if y_pos_binned == 9:
                    print('Ext Save Data')
                if y_pos_binned == 10:
                    print('System Save Data')
                if y_pos_binned == 11:
                   self.changeScreen("titledb_screen")
                if y_pos_binned == 12:
                    self.changeScreen("remote_install_screen")
                if y_pos_binned == 13:
                    print('Updates')
    def updateCanvas(self):
        #print("Refreshing canvas variables")
        #Delete all current canvas elements
        for color_key in self.text_config:
            try:
                self.sliders[color_key][1].lower()
            except:
                pass
        self.canvas.delete("all")
        #Bottom screen offsets
        x_offset = 40
        y_offset = self.app_config['screen_gap']+240
        self.v['canvas_image'].paste(self.c[self.v['current_screen']]['top_screen'], (0,0))
        self.v['canvas_image'].paste(self.c[self.v['current_screen']]['bottom_screen'], (x_offset,y_offset))
        self.image_preview = ImageTk.PhotoImage(self.v['canvas_image'])
        self.canvas.create_image(0,0, anchor=tk.NW, image=self.image_preview)
        if self.v['current_screen'] in ['textcolor_screen', 'main_screen', 'sd_screen', 'titles_screen', 'titledb_screen', 'ticket_screen', 'options_screen']:
            selection_image = self.i['selection_overlay']
        else:
            selection_image = ''
        self.selection_overlay = self.canvas.create_image(x_offset, self.v['selection_position']*15+y_offset+20, anchor=tk.NW, image=selection_image)
        #Layer topmost (toolbar buttons)
        self.canvas.create_window(0, y_offset, anchor=tk.NW, tags='toolbar', window=self.fbipreview_button)
        self.canvas.create_window(0, 40+y_offset, anchor=tk.NW, tags='toolbar', window=self.textcolor_button)
        self.canvas.create_window(x_offset+320, y_offset, anchor=tk.NW, tags='toolbar', window=self.opendir_button)
        self.canvas.create_window(x_offset+320, 40+y_offset, anchor=tk.NW, tags='toolbar', window=self.save_button)
        self.canvas.create_window(x_offset+320, 80+y_offset, anchor=tk.NW, tags='toolbar', window=self.screenshot_button)
        
        #Layer Textcolor Sliders
        if self.v['current_screen'] == 'textcolor_screen':
            config_array = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
            for i in range(len(config_array)):
                color_key = config_array[i]
                self.sliders[color_key][1].lift()
                self.canvas.create_window(x_offset+208, i*15+22+y_offset, anchor=tk.NW, tags='slider', window=self.sliders[color_key][0])
    def rebuildCache(self):
        for key in self.c:
            self.drawCanvasCache(key)
    def drawFontCache(self, screen_name, screen='topbottom', type='mainbar'):
        text = {
                'top_screen_main': [],
                'top_screen_bar' : [],
                'bottom_screen_main': [],
                'bottom_screen_bar' : [],
            }
        #Top screen
        if 'top' in screen:
            text['top_screen_bar'] = [
                    {'coord': (2,10), 'color': self.text_config['text'], 'text': 'Ver. 2.4.7', 'font_type': self.v['font_normal'], 'anchor':'W', 'alignment': 'left'},
                    {'coord': (200,10), 'color': self.text_config['text'], 'text': "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()), 'font_type': self.v['font_normal'], 'anchor':'', 'alignment': 'center'},
                    {'coord': (2,230), 'color': self.text_config['text'], 'text': "SD: {} GiB, CTR NAND: {} MiB, TWL NAND: {} MiB, TWL Photo: {} MiB".format(self.v['sd_ex'], self.v['ctrnand_ex'], self.v['twlnand_ex'], self.v['twlphoto_ex']), 'font_type': self.v['font_mini'], 'anchor':'W', 'alignment': 'left'},
                ]
            if screen_name in ['textcolor_screen', 'titles_screen', 'titledb_screen']:
                text['top_screen_bar'] += [
                    {'coord': (102,48), 'color': self.text_config['text'], 'text': '{}\n{}\n{}'.format(self.app_config['theme_title'], self.app_config['theme_desc'], self.app_config['theme_author']), 'font_type': self.v['font_normal'], 'anchor':'NW', 'alignment': 'left'},
                    {'coord': (200, 111), 'color': self.text_config['text'], 'text': 'Title ID: 0004000000FBIP00\nMedia Type: SD\nVersion: 0\nProduct Code: CTR-P-FBIP\nRegion: North America\nSize: 1.56 GiB', 'font_type': self.v['font_normal'], 'anchor':'N', 'alignment': 'center'},
                ]
        if 'bottom' in screen:
            row_text =[]
            if screen_name in ['textcolor_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Textcolor.cfg', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': "Don't forget to save!", 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['text',           self.text_config['text']],
                        ['nand',           self.text_config['nand']],
                        ['sd',             self.text_config['sd']],
                        ['gamecard',       self.text_config['gamecard']],
                        ['dstitle',        self.text_config['dstitle']],
                        ['file',           self.text_config['file']],
                        ['directory',      self.text_config['directory']],
                        ['enabled',        self.text_config['enabled']],
                        ['disabled',       self.text_config['disabled']],
                        ['installed',      self.text_config['installed']],
                        ['notinstalled',   self.text_config['notinstalled']],
                        ['ticketinuse',    self.text_config['ticketinuse']],
                        ['ticketnotinuse', self.text_config['ticketnotinuse']],
                    ]
            if screen_name in ['main_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Main Menu', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Select, START: Exit', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['SD',               self.text_config['text']],
                        ['CTR NAND',         self.text_config['text']],
                        ['TWL NAND',         self.text_config['text']],
                        ['TWL Photo',        self.text_config['text']],
                        ['TWL Sound',        self.text_config['text']],
                        ['Dump NAND',        self.text_config['text']],
                        ['Titles',           self.text_config['text']],
                        ['Pending Titles',   self.text_config['text']],
                        ['Tickets',          self.text_config['text']],
                        ['Ext Save Data',    self.text_config['text']],
                        ['System Save Data', self.text_config['text']],
                        ['TitleDB',          self.text_config['text']],
                        ['Remote Install',   self.text_config['text']],
                        ['Update',           self.text_config['text']],
                    ]
            if screen_name in ['sd_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Files', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Select, B: Back, X: Refresh, Select: Options', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['<current directory>', self.text_config['directory']],
                        ['3ds',                 self.text_config['directory']],
                        ['CIAs',                self.text_config['directory']],
                        ['fbi',                 self.text_config['directory']],
                        ['hblauncherloader',    self.text_config['directory']],
                        ['JKSV',                self.text_config['directory']],
                        ['luma',                self.text_config['directory']],
                        ['Nintendo3DS',         self.text_config['directory']],
                        ['arm9loaderhax.bin',   self.text_config['file']],
                        ['boot.3dsx',           self.text_config['file']],
                    ]
            if screen_name in ['nand_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Confirmation', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,87), 'color': self.text_config['text'], 'text': 'Modifying the NAND is dangerous and can render\nthe system inoperable.\nMake sure you know what you are doing.\n\nProceed?', 'anchor':'', 'alignment': 'center'},
                        {'coord': (10+72,155+30), 'color': self.text_config['text'], 'text': 'Yes (A)', 'anchor':'', 'alignment': 'center'},
                        {'coord': (10+72+155,155+30), 'color': self.text_config['text'], 'text': 'No (B)', 'anchor':'', 'alignment': 'center'},
                    ]
            if screen_name in ['options_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Options', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Toggle, B: Return', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['Show hidden',      self.text_config['disabled']],
                        ['Show directories', self.text_config['enabled']],
                        ['Show files',       self.text_config['enabled']],
                        ['Show CIAs',        self.text_config['enabled']],
                        ['Show tickets',     self.text_config['enabled']],
                    ]
            if screen_name in ['titles_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Titles', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Select, B: Return, X: Refresh, Select: Options', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['FBI',                    self.text_config['sd']],
                        ['Super ftpd II Turbo',    self.text_config['sd']],
                        ['hblauncher_loader v1.2', self.text_config['sd']],
                        ["JK's Save Manager",      self.text_config['sd']],
                        ['NEW ラブプラス+',           self.text_config['sd']],
                        ['Theme',                  self.text_config['sd']],
                        ['Friend List',            self.text_config['nand']],
                        ['Internet Browser',       self.text_config['nand']],
                        ['Notifications',          self.text_config['nand']],
                        ['System Settings',        self.text_config['nand']],
                        ['Hoshigami Remix',        self.text_config['gamecard']],
                        ['Cave Story',             self.text_config['dstitle']],
                        ['DS Download Play',       self.text_config['dstitle']],
                    ]
            if screen_name in ['ticket_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Tickets', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Select, B: Return, X: Refresh', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['000400000F800100', self.text_config['ticketinuse']],
                        ['000400000BEEF500', self.text_config['ticketinuse']],
                        ['000400000D921E00', self.text_config['ticketinuse']],
                        ['0004000002C23200', self.text_config['ticketinuse']],
                        ['00040000000F4E00', self.text_config['ticketnotinuse']],
                        ['0004008C00008F00', self.text_config['ticketnotinuse']],
                        ['0004003000009602', self.text_config['ticketinuse']],
                        ['0004003000009402', self.text_config['ticketinuse']],
                        ['0004003000009702', self.text_config['ticketinuse']],
                        ['0004001000021000', self.text_config['ticketinuse']],
                        ['000400000F12EE00', self.text_config['ticketnotinuse']],
                        ['000400000009B300', self.text_config['ticketinuse']],
                        ['00048005484E4441', self.text_config['ticketinuse']],
                    ]
            if screen_name in ['titledb_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'TitleDB.com', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'A: Select, B: Return, X: Refresh', 'anchor':'', 'alignment': 'center'},
                    ]
                row_text = [
                        ['Boot NTR Selector',      self.text_config['notinstalled']],
                        ['CTRXplorer',             self.text_config['installed']],
                        ['FBI',                    self.text_config['installed']],
                        ['GYTB',                   self.text_config['notinstalled']],
                        ['hblauncher_loader v1.2', self.text_config['installed']],
                        ["JK's Save Manager",      self.text_config['installed']],
                        ['Luma3DS Updater',        self.text_config['notinstalled']],
                        ['MultiUpdater',           self.text_config['notinstalled']],
                        ['Non-Stop Nyan Cat',      self.text_config['notinstalled']],
                        ['OpenSyobon3DS',          self.text_config['notinstalled']],
                        ['PKSM',                   self.text_config['notinstalled']],
                        ['Super ftpd II Turbo',    self.text_config['installed']],
                        ['TWLoader',               self.text_config['notinstalled']],
                    ]
            if screen_name in ['remote_install_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Installing from URL(s)', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,230), 'color': self.text_config['text'], 'text': 'Press B to cancel.', 'anchor':'', 'alignment': 'center'},
                    ]
            if screen_name in ['success_screen']:
                text['bottom_screen_bar'] = [
                        {'coord': (160,10), 'color': self.text_config['text'], 'text': 'Success', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,155+30), 'color': self.text_config['text'], 'text': 'Okay (Any Button)', 'anchor':'', 'alignment': 'center'},
                        {'coord': (160,87), 'color': self.text_config['text'], 'text': 'NAND dumped.', 'anchor':'', 'alignment': 'center'},
                    ]
            if row_text:
                for i in range(len(row_text)):
                    text['bottom_screen_main'].append({'coord': (2, 15*(i)+21), 'color': row_text[i][1], 'text': row_text[i][0], 'anchor':'NW', 'alignment': 'left'})
        for key in text:
            if 'top_screen' in key:
                for i in range(len(text[key])):
                    text[key][i].update({'screen': self.v['d_top_screen']})
            if 'bottom_screen' in key:
                for i in range(len(text[key])):
                    text[key][i].update({'screen': self.v['d_bottom_screen'], 'font_type': self.v['font_normal']})
        for key in text:
            if key.rsplit('_', 1)[1] in type:
                if len(text[key]):
                    for i in range(len(text[key])):
                        d = text[key][i]
                        r,g,b,a = d['color']
                        fade = 0.4
                        r = (255 - r) * fade + r
                        g = (255 - g) * fade + g
                        b = (255 - b) * fade + b
                        tmp_image = Image.new('RGBA', (400, 240), (int(r),int(g),int(b),0))
                        d_tmp_image = ImageDraw.Draw(tmp_image)
                        self.drawText(d_tmp_image, d['font_type'], d['color'], d['text'], d['coord'], d['anchor'], d['alignment'])
                        self.drawImage(self.v[key.rsplit('_', 1)[0]], (0,0), tmp_image)
    def drawCanvasCache(self, screen_name, screen='topbottom'):
        screen_top = []
        screen_bottom = []
        if 'top' in screen:
            screen_top = [
                    {'priority': 5},
                    {'priority': 10},
                    {'priority': 1, 'coord': (0,0), 'data': self.i['top_screen_bg']},
                    {'priority': 7, 'coord': (0,0), 'data': self.i['top_screen_top_bar']},
                    {'priority': 7, 'coord': (0,20), 'data': self.i['top_screen_top_bar_shadow']},
                    {'priority': 7, 'coord': (0,220), 'data': self.i['top_screen_bottom_bar']},
                    {'priority': 7, 'coord': (0,204), 'data': self.i['top_screen_bottom_bar_shadow']},
                ]
            #Meta Info Box
            if screen_name in ['textcolor_screen', 'titles_screen', 'titledb_screen']:
                meta_info_box = [
                        {'priority': 4, 'coord': (int(72-(self.icon['app'].size[0]/2)), int(70-(self.icon['app'].size[1]/2))), 'data': self.icon['app']},
                        {'priority': 3, 'coord': (40, 38), 'data': self.i['meta_info_box']},
                        {'priority': 2, 'coord': (24, 22), 'data': self.i['meta_info_box_shadow']},
                    ]
                screen_top += meta_info_box
            #Logo
            if screen_name in ['main_screen']:
                logo = [
                        {'priority': 2, 'coord': (136, 56), 'data': self.i['logo']},
                    ]
                screen_top += logo
            for i in range(len(screen_top)):
                screen_top[i].update({'screen': self.v['top_screen']})
        if 'bottom' in screen:
            screen_bottom = [
                    {'priority': 5},
                    {'priority': 10},
                    {'priority': 1, 'coord': (0,0), 'data': self.i['bottom_screen_bg']},
                    {'priority': 7, 'coord': (0,0), 'data': self.i['bottom_screen_top_bar']},
                    {'priority': 7, 'coord': (0,20), 'data': self.i['bottom_screen_top_bar_shadow']},
                    {'priority': 7, 'coord': (0,220), 'data': self.i['bottom_screen_bottom_bar']},
                    {'priority': 7, 'coord': (0,204), 'data': self.i['bottom_screen_bottom_bar_shadow']},
                ]
            #Scrollbar
            if screen_name in ['textcolor_screen', 'main_screen', 'sd_screen', 'titles_screen', 'options_screen', 'ticket_screen', 'titledb_screen']:
                scroll_bar = [
                        {'priority': 6, 'coord': (310,20), 'data': self.i['scroll_bar']},
                    ]
                screen_bottom += scroll_bar
            #Progress Bar
            if screen_name in ['remote_install_screen']:
                progress_bar = [
                        {'priority': 3, 'coord': (10, 95), 'data': self.i['progress_bar_bg']},
                    ]
                screen_bottom += progress_bar
            #Button Small
            if screen_name in ['nand_screen']:
                button_small = [
                        {'priority': 3, 'coord': (10, 155), 'data': self.i['button_small']},
                        {'priority': 3, 'coord': (165, 155), 'data': self.i['button_small']},
                    ]
                screen_bottom += button_small
            #Button Large
            if screen_name in ['success_screen']:
                button_large = [
                        {'priority': 3, 'coord': (10, 155), 'data': self.i['button_large']},
                    ]
                screen_bottom += button_large
            for i in range(len(screen_bottom)):
                screen_bottom[i].update({'screen': self.v['bottom_screen']})
        screen_base = screen_top + screen_bottom
        screen_base = sorted(screen_base, key=lambda k: k['priority'])
        for i in range(len(screen_base)):
            sc = screen_base[i]
            if sc['priority'] == 5:
                self.drawFontCache(screen_name, screen=screen, type='main')
            elif sc['priority'] == 10:
                self.drawFontCache(screen_name, screen=screen, type='bar')
            else:
                self.drawImage(sc['screen'], sc['coord'], sc['data'])
        if 'top' in screen:
            self.c[screen_name]['top_screen'] = self.v['top_screen'].copy()
        if 'bottom' in screen:
            self.c[screen_name]['bottom_screen'] = self.v['bottom_screen'].copy()
    def drawText(self, draw_handle, font_type, color, text, coord, anchor, alignment):
        fnt_w, fnt_h = draw_handle.multiline_textsize(text, font=font_type)
        x_coord, y_coord = coord
        x_offset = -int(fnt_w/2)
        y_offset = -int(fnt_h/2)
        if 'N' in anchor:
            y_offset = 0
        if 'W' in anchor:
            x_offset = 0
        if 'E' in anchor:
            x_offset = -fnt_w
        if 'S' in anchor:
            y_offset = -fnt_h
        draw_handle.text((x_coord+x_offset, y_coord+y_offset+1), text, font=font_type, fill=color, align=alignment)
    def drawImage(self, screen, coord, data):
        try:
            r,g,b,a = data.split()
            fg = Image.merge("RGB", (r, g, b))
            mask = Image.merge("L", (a,))
            screen.paste(fg, coord, mask)
        except: pass
    def updateAnimationLoop(self, loop=False):
        #print("Repopulating canvas animations...")
        self.drawCanvasCache(self.v['current_screen'], screen='top')
        self.updateCanvas()
        """
        #Bottom screen offsets
        x_offset = 40
        y_offset = self.app_config['screen_gap']+240
        #Map all changed screen element bindings (images, colors, text, etc.)
        animated = {
            'wifi' : [self.i['wifi_disconnected'], self.i['wifi0'], self.i['wifi1'], self.i['wifi2'], self.i['wifi3']],
            'battery' : [self.i['battery_charging'], self.i['battery0'], self.i['battery1'], self.i['battery2'], self.i['battery3'], self.i['battery4'], self.i['battery5']],
            'progress' : ["", self.i['progress_bar_content_25'], self.i['progress_bar_content_50'], self.i['progress_bar_content_75'], self.i['progress_bar_content']],
            }
        #Divide by zero defense
        if self.app_config['anim_duration']:
            anim_duration = self.app_config['anim_duration']
        else:
            anim_duration = 1
        #Process what image frame to use based on seconds
        frames = {}
        for element in animated:
            imageFrame = int(int("{:%S}".format(datetime.datetime.now()))/anim_duration)%len(animated[element])
            frames.update({element: imageFrame})
        self.canvas.create_text(200, 10, font=self.font_normal, tags='animate', fill=self.text_config['text']['rgb'], text = "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()))
        self.canvas.create_image(347, 2, anchor = tk.NW, tags='animate', image=animated['wifi'][frames['wifi']])
        self.canvas.create_image(371, 2, anchor = tk.NW, tags='animate', image=animated['battery'][frames['battery']])
        if self.v['current_screen'] == "remote_install_screen":
            self.progress_bar_content = self.canvas.create_image(20+x_offset, 105+y_offset, anchor = tk.NW, tags='animate', image=animated['progress'][frames['progress']])
        """
        if loop:
            self.canvas.after(1000, lambda: self.updateAnimationLoop(loop=True))
    def cleanupWatchdog(self):
        print("Cleaning up watchdog...")
        self.observer.stop()
        self.observer.join()
#Watchdog Event Handler
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
        print("Handling filesystem event: {} {}".format(event.event_type, event.src_path))
        if not 'textcolor' in event.src_path:
            self.appwindow.loadImage(os.path.split(event.src_path)[0], os.path.splitext(os.path.basename(event.src_path))[0])
            self.appwindow.updateCanvas()
    def on_created(self, event):
        self.process(event)
    def on_modified(self, event):
        self.process(event)

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
    app.cleanupWatchdog()