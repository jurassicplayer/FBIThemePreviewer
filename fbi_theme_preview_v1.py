#!/usr/bin/python

#tkinter bindings
import tkinter as tk
from tkinter import font, filedialog, messagebox, colorchooser, StringVar
#watchdog bindings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#pillow bindings
from PIL import Image, ImageTk, ImageGrab
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
        self.setupWidget()
        if self.app_config['meta_icon']:
            self.loadCustomMetaIcon(self.app_config['meta_icon'])
        self.loadTheme(self.app_config['theme_folder'])
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
            'app'        : tk.PhotoImage(data=self.icon_base64['app']),
            'fbi'        : tk.PhotoImage(data=self.icon_base64['fbi']),
            'textcolor'  : tk.PhotoImage(data=self.icon_base64['textcolor']),
            'screenshot' : tk.PhotoImage(data=self.icon_base64['screenshot']),
            'opendir'    : tk.PhotoImage(data=self.icon_base64['opendir']),
            'save'       : tk.PhotoImage(data=self.icon_base64['save']),
            }
        self.call('wm', 'iconphoto', self._w, self.icon['app'])
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
            'theme_version' : "2.4.6",
            'meta_icon'     : '',
            'screen_gap'    : 0, #68
            'anim_duration' : 1, #In seconds
            'overwrite'     : 'never', #never/preview/textcolor/always
            'language'      : "en",
            }
        self.text_config = {
            'text':           {'rgb': "#000000", 'alpha': "FF"},
            'nand':           {'rgb': "#000000", 'alpha': "FF"},
            'sd':             {'rgb': "#000000", 'alpha': "FF"},
            'gamecard':       {'rgb': "#000000", 'alpha': "FF"},
            'dstitle':        {'rgb': "#000000", 'alpha': "FF"},
            'file':           {'rgb': "#000000", 'alpha': "FF"},
            'directory':      {'rgb': "#000000", 'alpha': "FF"},
            'enabled':        {'rgb': "#000000", 'alpha': "FF"},
            'disabled':       {'rgb': "#000000", 'alpha': "FF"},
            'installed':      {'rgb': "#000000", 'alpha': "FF"},
            'notinstalled':   {'rgb': "#000000", 'alpha': "FF"},
            'ticketinuse':    {'rgb': "#000000", 'alpha': "FF"},
            'ticketnotinuse': {'rgb': "#000000", 'alpha': "FF"},
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
        self.v = {
            'current_screen'     : 'main_screen',
            'previous_screen'    : 'main_screen',
            'selection_position' : 0,
            'sd_ex'              : 64,
            'ctrnand_ex'         : 328,
            'twlnand_ex'         : 128,
            'twlphoto_ex'        : 32,
            }
        self.l = {
            'title'  : 'FBI Theme Previewer',
            'error'  : 'Error',
            'error1' : 'File not found (X).',            'warn'   : 'Warning',
            'warn1'  : 'Preview image already exists.\nDo you want to overwrite?',
            'bottom_screen_top_bar_text00' : 'Textcolor.cfg (#BGR)',
            'bottom_screen_top_bar_text01' : 'Main Menu',
            'bottom_screen_top_bar_text02' : 'Files',
            'bottom_screen_top_bar_text03' : 'Confirmation',
            'bottom_screen_top_bar_text04' : 'Titles',
            'bottom_screen_top_bar_text05' : 'Pending Titles',
            'bottom_screen_top_bar_text06' : 'Tickets',
            'bottom_screen_top_bar_text07' : 'Ext Save Data',
            'bottom_screen_top_bar_text08' : 'System Save Data',
            'bottom_screen_top_bar_text09' : 'TitleDB.com',
            'bottom_screen_top_bar_text10' : 'Installing From URL(s)',
            'bottom_screen_top_bar_text11' : 'Success',
            'bottom_screen_top_bar_text12' : 'Options',
            'bottom_screen_bottom_bar_text00' : "Don't forget to save!",
            'bottom_screen_bottom_bar_text01' : 'A: Select, START: Exit',
            'bottom_screen_bottom_bar_text02' : 'A: Select, B: Back, X: Refresh, Select: Options',
            'bottom_screen_bottom_bar_text03' : 'A: Select, B: Return, X: Refresh, Select: Options',
            'bottom_screen_bottom_bar_text04' : 'A: Select, B: Return, X: Refresh',
            'bottom_screen_bottom_bar_text05' : 'A: Select, B: Return',
            'bottom_screen_bottom_bar_text06' : 'Press B to cancel.'
            }
    def setupWidget(self):
        print("Setting up main widget...")
        self.frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame, width=400, height=480+int(self.app_config['screen_gap']), borderwidth=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", lambda event: self.cursorEvent(event, 'B1'))
        self.canvas.bind("<B1-Motion>", lambda event: self.cursorEvent(event, 'B1'))
        self.canvas.bind("<Button-3>", lambda event: self.cursorEvent(event, 'B3'))
        self.canvas.pack()
        self.active = StringVar()
        self.active.set("main_screen")
        radio_icon_size = 38
        button_icon_size = 40
        
        self.fbipreview_button = tk.Radiobutton(self, width=radio_icon_size, height=radio_icon_size, borderwidth=0, highlightthickness=0, indicatoron=0, offrelief='flat', overrelief='flat', value="main_screen", variable=self.active, image=self.icon['fbi'], command=lambda: self.changeScreen(self.v['previous_screen']))
        self.textcolor_button = tk.Radiobutton(self, width=radio_icon_size, height=radio_icon_size, borderwidth=0, highlightthickness=0, indicatoron=0, offrelief='flat', overrelief='flat', value="textcolor_screen", variable=self.active, image=self.icon['textcolor'], command=lambda: self.changeScreen("textcolor_screen"))
        self.screenshot_button = tk.Button(self, width=button_icon_size, height=button_icon_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['screenshot'], command=self.savePreview)
        self.opendir_button = tk.Button(self, width=button_icon_size, height=button_icon_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['opendir'], command=self.openTheme)
        self.save_button = tk.Button(self, width=button_icon_size, height=button_icon_size, borderwidth=0, highlightthickness=0, overrelief='flat', image=self.icon['save'], command=lambda: self.saveConfig("textcolor"))
        self.frame.pack()
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
                                A = value[:2]
                                RGB = swapRGBBGR(value[2:])
                                config_dict.update({key : {'rgb' : RGB, 'alpha' : A} })
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
        else:
            messagebox.showwarning("Error", 'Theme path not found:\n{}'.format(folderpath))
    def loadImage(self, folderpath, filename):
        print("Loading image: {}".format(os.path.join(folderpath, "{}.png".format(filename))))
        try:
            filepath = os.path.join(folderpath, "{}.png".format(filename))
            if filename in ['progress_bar_content_25', 'progress_bar_content_50', 'progress_bar_content_75']:    return
            elif filename == 'progress_bar_content' or filename == 'selection_overlay':
                tmp_image = Image.open(filepath)
                if filename == 'selection_overlay':
                    tmp_image = tmp_image.convert('RGBA').resize((320, 15), Image.ANTIALIAS)
                if filename == 'progress_bar_content':
                    self.i['{}_25'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.25), 30)))
                    self.i['{}_50'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.50), 30)))
                    self.i['{}_75'.format(filename)] = ImageTk.PhotoImage(tmp_image.crop((0, 0, int(280*0.75), 30)))
                self.i[filename] = ImageTk.PhotoImage(tmp_image)
            else:
                self.i[filename] = tk.PhotoImage(file=filepath)
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
            self.icon['app'] = tk.PhotoImage(file=filepath)
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
                value = "{}{}".format(self.text_config[key]['alpha'], swapRGBBGR(self.text_config[key]['rgb'])[1:])
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
        self.updateCanvas()
    def cursorEvent(self, event, button):
        #print("Handling cursor event: {}".format(button))
        #Top screen handling
        if event.x >= 48 and event.x <= 96 and event.y >= 46 and event.y <= 94:
            if self.v['current_screen'] in ["textcolor_screen", "titles_screen", "titledb_screen"] and button == "B3":
                self.openCustomMetaIcon()
        #Bottom screen handling
        y_pos_offset = 20+240+int(self.app_config['screen_gap']) #20px bottom_screen_top_bar, 240px top screen, self.app_config['screen_gap']
        if event.x >= 40 and event.x <= 360 and event.y >= y_pos_offset and event.y <= 200+y_pos_offset:
            y_pos_fixed = event.y-y_pos_offset
            self.v['selection_position'] = y_pos_binned = int(y_pos_fixed/15)
            self.canvas.coords(self.selection_overlay, (40, y_pos_binned*15+y_pos_offset))
            if self.v['current_screen'] == "textcolor_screen" and button == "B3":
                color_index = ['text', 'nand', 'sd', 'gamecard', 'dstitle', 'file', 'directory', 'enabled', 'disabled', 'installed', 'notinstalled', 'ticketinuse', 'ticketnotinuse']
                if y_pos_binned < len(color_index):
                    new_color = colorchooser.askcolor(initialcolor = self.text_config[color_index[y_pos_binned]]['rgb'])[1]
                    if new_color:
                        self.text_config[color_index[y_pos_binned]]['rgb'] = new_color
                        self.updateCanvas()
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
                    #self.changeScreen("success_screen")
    def updateCanvas(self):
        print("Refreshing canvas variables")
        #Delete all current canvas elements
        self.canvas.delete("all")
        #Map all changed screen element bindings (images, colors, text, etc.)
        screen = {
            'textcolor_screen': {
                #Text
                'meta_info_box_text': ["", self.text_config['text']['rgb']],
                'meta_info_text': ["", self.text_config['text']['rgb']],
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text00'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['{:<40}{:>50}'.format('text', swapRGBBGR(self.text_config['text']['rgb'])),self.text_config['text']['rgb']],
                'bottom_screen_listing02': ['{:<40}{:>48}'.format('nand', swapRGBBGR(self.text_config['nand']['rgb'])),self.text_config['nand']['rgb']],
                'bottom_screen_listing03': ['{:<40}{:>50}'.format('sd', swapRGBBGR(self.text_config['sd']['rgb'])),self.text_config['sd']['rgb']],
                'bottom_screen_listing04': ['{:<40}{:>41}'.format('gamecard', swapRGBBGR(self.text_config['gamecard']['rgb'])),self.text_config['gamecard']['rgb']],
                'bottom_screen_listing05': ['{:<40}{:>48}'.format('dstitle', swapRGBBGR(self.text_config['dstitle']['rgb'])),self.text_config['dstitle']['rgb']],
                'bottom_screen_listing06': ['{:<40}{:>51}'.format('file', swapRGBBGR(self.text_config['file']['rgb'])),self.text_config['file']['rgb']],
                'bottom_screen_listing07': ['{:<40}{:>45}'.format('directory', swapRGBBGR(self.text_config['directory']['rgb'])),self.text_config['directory']['rgb']],
                'bottom_screen_listing08': ['{:<40}{:>45}'.format('enabled', swapRGBBGR(self.text_config['enabled']['rgb'])),self.text_config['enabled']['rgb']],
                'bottom_screen_listing09': ['{:<40}{:>45}'.format('disabled', swapRGBBGR(self.text_config['disabled']['rgb'])),self.text_config['disabled']['rgb']],
                'bottom_screen_listing10': ['{:<40}{:>46}'.format('installed', swapRGBBGR(self.text_config['installed']['rgb'])),self.text_config['installed']['rgb']],
                'bottom_screen_listing11': ['{:<40}{:>43}'.format('notinstalled', swapRGBBGR(self.text_config['notinstalled']['rgb'])),self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing12': ['{:<40}{:>43}'.format('ticketinuse', swapRGBBGR(self.text_config['ticketinuse']['rgb'])),self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing13': ['{:<40}{:>40}'.format('ticketnotinuse', swapRGBBGR(self.text_config['ticketnotinuse']['rgb'])),self.text_config['ticketnotinuse']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text00'], self.text_config['text']['rgb']],
                #Image
                'meta_info_box': self.i['meta_info_box'],
                'meta_info_box_icon': self.icon['app'],
                'meta_info_box_shadow': self.i['meta_info_box_shadow'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'main_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text01'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['SD',self.text_config['text']['rgb']],
                'bottom_screen_listing02': ['CTR NAND',self.text_config['text']['rgb']],
                'bottom_screen_listing03': ['TWL NAND (WIP)',self.text_config['text']['rgb']],
                'bottom_screen_listing04': ['TWL Photo',self.text_config['text']['rgb']],
                'bottom_screen_listing05': ['TWL Sound (WIP)',self.text_config['text']['rgb']],
                'bottom_screen_listing06': ['Dump NAND',self.text_config['text']['rgb']],
                'bottom_screen_listing07': ['Titles',self.text_config['text']['rgb']],
                'bottom_screen_listing08': ['Pending Titles (WIP)',self.text_config['text']['rgb']],
                'bottom_screen_listing09': ['Tickets',self.text_config['text']['rgb']],
                'bottom_screen_listing10': ['Ext Save Data (WIP)',self.text_config['text']['rgb']],
                'bottom_screen_listing11': ['System Save Data (WIP)',self.text_config['text']['rgb']],
                'bottom_screen_listing12': ['TitleDB',self.text_config['text']['rgb']],
                'bottom_screen_listing13': ['Remote Install',self.text_config['text']['rgb']],
                'bottom_screen_listing14': ['Update',self.text_config['text']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text01'], self.text_config['text']['rgb']],
                'logo': self.i['logo'],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'sd_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text02'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['<current directory>',self.text_config['directory']['rgb']],
                'bottom_screen_listing02': ['3ds',self.text_config['directory']['rgb']],
                'bottom_screen_listing03': ['CIAs',self.text_config['directory']['rgb']],
                'bottom_screen_listing04': ['fbi',self.text_config['directory']['rgb']],
                'bottom_screen_listing05': ['hblauncherloader',self.text_config['directory']['rgb']],
                'bottom_screen_listing06': ['JKSV',self.text_config['directory']['rgb']],
                'bottom_screen_listing07': ['luma',self.text_config['directory']['rgb']],
                'bottom_screen_listing08': ['Nintendo3DS',self.text_config['directory']['rgb']],
                'bottom_screen_listing09': ['arm9loaderhax.bin',self.text_config['file']['rgb']],
                'bottom_screen_listing10': ['boot.3dsx',self.text_config['file']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text02'], self.text_config['text']['rgb']],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'nand_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text03'], self.text_config['text']['rgb']],
                'bottom_screen_justified_text': ["Modifying the NAND is dangerous and can render\nthe system inoperable.\nMake sure you know what you are doing.\n\nProceed?", self.text_config['text']['rgb']],
                'button_text' : ["Yes (A)                                        No (B)", self.text_config['text']['rgb']],
                'button_small': self.i['button_small'],
                },
            'titles_screen': {
                'meta_info_box_text': ["{}\n{}\n{}".format(self.app_config['theme_title'], self.app_config['theme_desc'], self.app_config['theme_author']), self.text_config['text']['rgb']],
                'meta_info_text': ["Title ID: 0004000000FBIP00\nMedia Type: SD\nVersion: 0\nProduct Code: CTR-P-FBIP\nRegion: North America\nSize: 1.56 GiB", self.text_config['text']['rgb']],
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text04'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['FBI',self.text_config['sd']['rgb']],
                'bottom_screen_listing02': ['Super ftpd II Turbo',self.text_config['sd']['rgb']],
                'bottom_screen_listing03': ['hblauncher_loader v1.2',self.text_config['sd']['rgb']],
                'bottom_screen_listing04': ["JK's Save Manager",self.text_config['sd']['rgb']],
                'bottom_screen_listing05': ['NEW ラブプラス+',self.text_config['sd']['rgb']],
                'bottom_screen_listing06': ['Theme',self.text_config['sd']['rgb']],
                'bottom_screen_listing07': ['Friend List',self.text_config['nand']['rgb']],
                'bottom_screen_listing08': ['Internet Browser',self.text_config['nand']['rgb']],
                'bottom_screen_listing09': ['Notifications',self.text_config['nand']['rgb']],
                'bottom_screen_listing10': ['System Settings',self.text_config['nand']['rgb']],
                'bottom_screen_listing11': ['Hoshigami Remix',self.text_config['gamecard']['rgb']],
                'bottom_screen_listing12': ['Cave Story',self.text_config['dstitle']['rgb']],
                'bottom_screen_listing13': ['DS Download Play',self.text_config['dstitle']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text03'], self.text_config['text']['rgb']],
                'meta_info_box': self.i['meta_info_box'],
                'meta_info_box_icon': self.icon['app'],
                'meta_info_box_shadow': self.i['meta_info_box_shadow'],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'options_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text12'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['Show hidden',self.text_config['disabled']['rgb']],
                'bottom_screen_listing02': ['Show directories',self.text_config['enabled']['rgb']],
                'bottom_screen_listing03': ['Show files',self.text_config['enabled']['rgb']],
                'bottom_screen_listing04': ['Show CIAs',self.text_config['enabled']['rgb']],
                'bottom_screen_listing05': ['Show tickets',self.text_config['enabled']['rgb']],
                'bottom_screen_bottom_bar_text': ['A: Toggle, B: Return', self.text_config['text']['rgb']],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'ticket_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text06'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['000400000F800100',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing02': ['000400000BEEF500',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing03': ['000400000D921E00',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing04': ['0004000002C23200',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing05': ['00040000000F4E00',self.text_config['ticketnotinuse']['rgb']],
                'bottom_screen_listing06': ['0004008C00008F00',self.text_config['ticketnotinuse']['rgb']],
                'bottom_screen_listing07': ['0004003000009602',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing08': ['0004003000009402',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing09': ['0004003000009702',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing10': ['0004001000021000',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing11': ['000400000F12EE00',self.text_config['ticketnotinuse']['rgb']],
                'bottom_screen_listing12': ['000400000009B300',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_listing13': ['00048005484E4441',self.text_config['ticketinuse']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text04'], self.text_config['text']['rgb']],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'titledb_screen': {
                'meta_info_box_text': ["{}\n{}\n{}".format(self.app_config['theme_title'], self.app_config['theme_desc'], self.app_config['theme_author']), self.text_config['text']['rgb']],
                'meta_info_text': ["Title ID: 0004000000FBIP00\nMedia Type: SD\nVersion: 0\nProduct Code: CTR-P-FBIP\nRegion: North America\nSize: 1.56 GiB", self.text_config['text']['rgb']],
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text09'], self.text_config['text']['rgb']],
                'bottom_screen_listing01': ['Boot NTR Selector',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing02': ['CTRXplorer',self.text_config['installed']['rgb']],
                'bottom_screen_listing03': ['FBI',self.text_config['installed']['rgb']],
                'bottom_screen_listing04': ['GYTB',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing05': ['hblauncher_loader v1.2',self.text_config['installed']['rgb']],
                'bottom_screen_listing06': ["JK's Save Manager",self.text_config['installed']['rgb']],
                'bottom_screen_listing07': ['Luma3DS Updater',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing08': ['MultiUpdater',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing09': ['Non-Stop Nyan Cat',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing10': ['OpenSyobon3DS',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing11': ['PKSM',self.text_config['notinstalled']['rgb']],
                'bottom_screen_listing12': ['Super ftpd II Turnbo',self.text_config['installed']['rgb']],
                'bottom_screen_listing13': ['TWLoader',self.text_config['installed']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text04'], self.text_config['text']['rgb']],
                'meta_info_box': self.i['meta_info_box'],
                'meta_info_box_icon': self.icon['app'],
                'meta_info_box_shadow': self.i['meta_info_box_shadow'],
                'scroll_bar': self.i['scroll_bar'],
                'selection_overlay': self.i['selection_overlay'],
                },
            'remote_install_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text10'], self.text_config['text']['rgb']],
                'bottom_screen_bottom_bar_text': [self.l['bottom_screen_bottom_bar_text06'], self.text_config['text']['rgb']],
                'progress_bar_bg': self.i['progress_bar_bg']
                },
            'success_screen': {
                'bottom_screen_top_bar_text': [self.l['bottom_screen_top_bar_text11'], self.text_config['text']['rgb']],
                'bottom_screen_justified_text': ["No updates available.", self.text_config['text']['rgb']],
                'button_large': self.i['button_large'],
                'button_text' : ["Okay (Any Button)", self.text_config['text']['rgb']]
                }
            }
        #Recreate all canvas elements
        self.createCanvas(screen[self.v['current_screen']])
    def createCanvas(self, screen_dict):
        print("Populating canvas elements...")
        d = {
            #Text
            'meta_info_box_text': ['',''],
            'meta_info_text': ['',''],
            'bottom_screen_top_bar_text': ['',''],
            'bottom_screen_listing01': ['',''],
            'bottom_screen_listing02': ['',''],
            'bottom_screen_listing03': ['',''],
            'bottom_screen_listing04': ['',''],
            'bottom_screen_listing05': ['',''],
            'bottom_screen_listing06': ['',''],
            'bottom_screen_listing07': ['',''],
            'bottom_screen_listing08': ['',''],
            'bottom_screen_listing09': ['',''],
            'bottom_screen_listing10': ['',''],
            'bottom_screen_listing11': ['',''],
            'bottom_screen_listing12': ['',''],
            'bottom_screen_listing13': ['',''],
            'bottom_screen_listing14': ['',''],
            'bottom_screen_justified_text': ['',''],
            'bottom_screen_bottom_bar_text': ['',''],
            'button_text': ['',''],
            #Image
            'button_large': "",
            'button_small': "",
            'logo': "",
            'meta_info_box': "",
            'meta_info_box_icon': "",
            'meta_info_box_shadow': "",
            'progress_bar_bg': "",
            'scroll_bar': "",
            'selection_overlay': "",
            }
        for key in d:
            try:
                d[key] = screen_dict[key]
            except: pass
        #Set text font
        self.font_normal = font.Font(family='Arial', size=-12, weight="bold")
        self.font_mini   = font.Font(family='Arial', size=7,   weight="bold")
        #Bottom screen offsets
        x_offset = 40
        y_offset = self.app_config['screen_gap']+240
        
        #Layer 0 (Background images)
        self.canvas.create_image(0, 0, anchor = tk.NW, image=self.i['top_screen_bg'])
        self.canvas.create_image(0+x_offset, 0+y_offset, anchor = tk.NW, image=self.i['bottom_screen_bg'])
        
        #Layer 1 (Screen Information)
        self.canvas.create_image(200, 120, image=d['logo'])
        line_height = 15
        line_offset = 20+y_offset #Height of top bar+y_offset
        self.canvas.create_image(24, 22, anchor = tk.NW, image=d['meta_info_box_shadow'])
        self.canvas.create_image(40, 38, anchor = tk.NW, image=d['meta_info_box'])
        self.canvas.create_image(72, 70, image=d['meta_info_box_icon'])
        self.canvas.create_text(102, 48, anchor = tk.NW, fill=d['meta_info_box_text'][1], text=d['meta_info_box_text'][0])
        self.canvas.create_text(200, 111, anchor = tk.N, justify='center', fill=d['meta_info_text'][1], text=d['meta_info_text'][0])
        for i in range(1, 15):
            self.canvas.create_text(2+x_offset, line_height*(i-1)+line_offset, anchor=tk.NW, font=self.font_normal, fill=d['bottom_screen_listing{0:02d}'.format(i)][1], text=d['bottom_screen_listing{0:02d}'.format(i)][0])
        self.canvas.create_image(0+320+x_offset, line_offset, anchor = tk.NE, image=d['scroll_bar'])
        self.selection_overlay = self.canvas.create_image(0+x_offset, self.v['selection_position']*15+line_offset, anchor = tk.NW, image=d['selection_overlay'])
        self.canvas.create_text(160+x_offset, 68+line_offset, justify='center', font=self.font_normal, fill=d['bottom_screen_justified_text'][1], text=d['bottom_screen_justified_text'][0])
        
        #Buttons
        self.canvas.create_image(10+x_offset, 155+y_offset, anchor = tk.NW, image=d['button_large'])
        self.canvas.create_image(10+x_offset, 155+y_offset, anchor = tk.NW, image=d['button_small'])
        self.canvas.create_image(165+x_offset, 155+y_offset, anchor = tk.NW, image=d['button_small'])
        self.canvas.create_text(200, 184+y_offset, fill=d['button_text'][1], text=d['button_text'][0])
        #Progress bar
        self.canvas.create_image(10+x_offset, 95+y_offset, anchor = tk.NW, image=d['progress_bar_bg'])
        #Layer 2 (Top bars)
        self.canvas.create_image(0, 0, anchor = tk.NW, image=self.i['top_screen_top_bar'])
        self.canvas.create_image(0, 220, anchor = tk.NW, image=self.i['top_screen_bottom_bar'])
        self.canvas.create_image(0, 20, anchor = tk.NW, image=self.i['top_screen_top_bar_shadow'])
        self.canvas.create_image(0, 204, anchor = tk.NW, image=self.i['top_screen_bottom_bar_shadow'])
        #Layer 2 (Bottom bars)
        self.canvas.create_image(0+x_offset, 0+y_offset, anchor = tk.NW, image=self.i['bottom_screen_top_bar'])
        self.canvas.create_image(0+x_offset, 220+y_offset, anchor = tk.NW, image=self.i['bottom_screen_bottom_bar'])
        self.canvas.create_image(0+x_offset, 20+y_offset, anchor = tk.NW, image=self.i['bottom_screen_top_bar_shadow'])
        self.canvas.create_image(0+x_offset, 220+y_offset, anchor = tk.SW, image=self.i['bottom_screen_bottom_bar_shadow'])
        
        #Layer 3 (Top bar overlays)
        self.canvas.create_text(2, 10, anchor = tk.W, font=self.font_normal, fill=self.text_config['text']['rgb'], text = "Ver. {}".format(self.app_config['theme_version']))
        self.canvas.create_text(2, 230, anchor = tk.W, font=self.font_mini, fill=self.text_config['text']['rgb'], text = "SD: {} GiB, CTR NAND: {} MiB, TWL NAND: {} MiB, TWL Photo: {} MiB".format(self.v['sd_ex'], self.v['ctrnand_ex'], self.v['twlnand_ex'], self.v['twlphoto_ex']))
        #Layer 3 (Bottom bar overlays)
        self.canvas.create_text(200, 10+y_offset, font=self.font_normal, fill=d['bottom_screen_top_bar_text'][1], text = d['bottom_screen_top_bar_text'][0])
        self.canvas.create_text(200, 230+y_offset, font=self.font_normal, fill=d['bottom_screen_bottom_bar_text'][1], text = d['bottom_screen_bottom_bar_text'][0])
        
        #Layer topmost (toolbar buttons)
        self.canvas.create_window(0, y_offset, anchor=tk.NW, tags='toolbar', window=self.fbipreview_button)
        self.canvas.create_window(0, 40+y_offset, anchor=tk.NW, tags='toolbar', window=self.textcolor_button)
        self.canvas.create_window(x_offset+320, y_offset, anchor=tk.NW, tags='toolbar', window=self.opendir_button)
        self.canvas.create_window(x_offset+320, 40+y_offset, anchor=tk.NW, tags='toolbar', window=self.save_button)
        self.canvas.create_window(x_offset+320, 80+y_offset, anchor=tk.NW, tags='toolbar', window=self.screenshot_button)
        self.updateAnimationLoop()
    def updateAnimationLoop(self, loop=False):
        #print("Repopulating canvas animations...")
        #Delete animated canvas elements
        self.canvas.delete("animate")
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
        self.appwindow.loadImage(os.path.split(event.src_path)[0], os.path.splitext(os.path.basename(event.src_path))[0])
        self.appwindow.updateCanvas()
    def on_created(self, event):
        self.process(event)
    def on_modified(self, event):
        self.process(event)
# Miscellaneous functions
def swapRGBBGR(color):
    if len(color) == 7:
        color = color[1:]
    color_list = [color[i:i+2] for i in range(0, len(color), 2)]
    color1 = color_list[0]
    color2 = color_list[1]
    color3 = color_list[2]
    return "#{}{}{}".format(color3,color2,color1).upper()

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
    app.cleanupWatchdog()