#!/usr/bin/python

from tkinter import *
from tkinter import font
import sys, datetime, random, time, threading

class Translations:
    def __init__(self):
        self.program_title = "FBI Theme Previewer"

class Configuration:
    def __init__(self):
        self.theme_folder = "romfs/"
        self.y_screen_distance = 0 #68
        self.language = "en"
        self.text="#000000"
        self.nand="#0000FF"
        self.sd="#00FF00"
        self.gamecard="#FF0000"
        self.dstitle="#82004B"
        self.file="#000000"
        self.directory="#0000FF"
        self.enabled="#00FF00"
        self.disabled="#0000FF"
        self.installed="#00FF00"
        self.notinstalled="#0000FF"
        self.ticketinuse="#00FF00"
        self.ticketnotinuse="#0000FF"
    def load_ini(self):
        print("Not implemented")
    def save_ini(self):
        print("Not implemented")

class AppWindow(Tk):
    def __init__(self, root=None):
        Tk.__init__(self, root)
        icon_base64 ="""R0lGODlhIAAgAOfYAKYAAKcAAKgAAKUBAakAAKoAAKsAAKgBAawAAK0AAK4AAKwBAa0BAa4BAa0C\nAq4DA64EBK4FBa8ICKwMDLALC60MDLEQD7IRELETE7IUFLMUFLIWFrMWFrMYF7QYGLQZGbUZGbYb\nG7UcHLYeHbYfH7YhILciIrUlJbYlJbcnJrgoJ7krKrksK7otLbouLbsxMbsyMbo0NLk1NL05OL47\nOlZXV748O1dYV7o+PcBCQbtEQ71EQ75EQ79EQ8BEQ8BERMFGRcJKSWJkY8JKSmNkZL5MS8NNTMNO\nTcRPTsRQT8RRUMVUU8VVVMdaWchdXMVfXshfXsViYcZiYcdiYchiYcliYcZjYsdjYcdjYshjYslj\nYcljYspjYcpjYspkY8tpZ8tracxsa8xubc1ubcl2ds51c891c892ddB5d8+BgNCBgNGBgNKBgNKC\ngNaBgdSGhdSJh9SJiNOLitWLitSMi9WMitWMi9aMi9ONjdWNi9aNi9eNi9eOi9mOi9iQjtiUktiW\nlNmYltmamNmbmdqcmq6urNyjodimpbGxrtmnp9iop9mop9qop9uoqN2optqpqNqpqdupqNupqdyp\nqNypqduqqdyqqdyqqt2qqd6qqN2rqd6rqd6rqt+rqd+rqt6sqd6sqt+squCsqt+tqeCtqt2urLq6\nuOCwrru7ueCysNO3ttS4uOG1stO5udW5uNW5uda5uNa6uNa6ude6uNe6ucPAv9e7udi7ueK5ttm8\nueK6t9e9usXCwNq9uePCweXDwebGxObHxNnPzdrPzOnQzufS0erU0erW0+vZ1uza1+3f3O7i4O7j\n4O/k4e/n5PDn5PHr6PHt6vHu6/Lv7PLw7fLw7vLx7vPy7///////////////////////////////\n////////////////////////////////////////////////////////////////////////////\n/////////////////////////////////////////////////////yH5BAEKAP8ALAAAAAAgACAA\nAAj+AP8JHEiwoMGDBlH98sOHD508dujs2WOnDh07dvrokaMH4508evD4MjUQERoFCRIoICCAgIEE\nCGIiMFAAAcyZBmQiIECmkEBjCxpAYbNGTRo1bdi0abOmKdKlS5u2UfNkwIFiAi8hMHKtq9evzaqU\ncALtq9kiAioJZGSgi9mvyl6kTGDj2NuuUQhEWksgy91r1jZ1mJugRbC31qToXVsAy19kySzMlZBA\nBbO3UwgsEjipr7W7y541mTsiRIIgn79mfiSQUl9qfzNFIJzSgzSzUwQoEhipQBbYbw09MDH3iyNi\n094q3vwvEQEsyd8SQuAmpYrUd/Pu/ffJN3CzzCD+gEhp5i9eAKAEdkrg9u+SuWHMX5uCIP0/Twm2\n/E11YS4L7G9RkQAnAnGiQHtmVQMDbYOYpxiB/4iCAIJm/ZJBAgwk4MAP35mlhQGhCBRKfuaVgUAc\nW8nHRQIh/kMJAvr9BQgEznBQhXwfYiJQIwBYYV4gIlwDhBfyZbZdJAI49tcZK1wDRg7yKQZJa32Z\nB4UL18xBQTQOEmAJZ8+Zx8QM1+iCADBdSsJZkuYpkcQ10WhgiHlGCiRJAD7+hcQYXUEBh3lUGKCJ\nQKOw+dcRb3T1hxiAGkCKQKQIcIV5PwTSFStD0InAo/+UEoAMt701DQmCdIXLBwB6JU0MCJwi0DBs\nExRwAg898ODDrT3QgMAGO/CQAgI46NArD8T2gEIBFQgjEBGHYFBAAQQEIIABOSVgAEsFUEsAAAR0\nSwC0BWDAiBAD3cDLLr3kosoqrrxiyy2zzOKKK7fkAksssdAiyyuyyNJKLTUgJPDABwUEADs="""
        img = PhotoImage(data=icon_base64)
        self.call('wm', 'iconphoto', self._w, img)
        self.screen = ""
        self.loadStaticResources()
        self.loadDynamicResources()
        self.createWidgets()
        self.drawCanvas()
        self.screen = "main_menu"
        self.wifi_counter = 0
        self.battery_counter = 0
        self.updateCanvas()
    
    def loadStaticResources(self):
        #Load translations
        tl = getattr(sys.modules[__name__], "Translations")()
        self.title(tl.program_title)
        #Load configurations
        config = getattr(sys.modules[__name__], "Configuration")()
        self.dir = config.theme_folder
        self.screen_gap = config.y_screen_distance
        #Shits and giggles number generator
        sd_size = random.choice((2.0,4.0,8.0,16.0,32.0,64.0,128.0,256.0,512.0))
        ctrnand_size = random.choice((943.0, 1240.0))
        self.sd_ex = sd_size - random.randrange(0.0, sd_size) - (random.randrange(0,9)/10)
        self.ctrnand_ex = ctrnand_size - random.randrange(0.0, ctrnand_size) - (random.randrange(0,9)/10)
        self.twlnand_ex = 128.0 - (random.randrange(0,9)/10)
        self.twlphoto_ex = 32.0 - (random.randrange(0,9)/10)
        
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
        self.i_progress_bar_content = PhotoImage(file=self.dir+"progress_bar_content.png")
        self.i_scroll_bar = PhotoImage(file=self.dir+"scroll_bar.png")
        tmp = PhotoImage(file=self.dir+"selection_overlay.png")
        self.i_selection_overlay = tmp.subsample(1,20).zoom(1,15)
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
        self.canvas = Canvas(self.frame, width=400, height=480+self.screen_gap, bd=0, highlightthickness=0)
        self.toolbar = Frame(self.frame)
        self.main_button = Button(self.toolbar, text="Main Menu", command=lambda: self.callButton("main_menu"))
        self.item_button = Button(self.toolbar, text="Item Metadata", command=lambda: self.callButton("item_metadata"))
        self.progress_button = Button(self.toolbar, text="Progress Bar", command=lambda: self.callButton("progress_bar"))
        self.little_buttons = Button(self.toolbar, text="Little Buttons", command=lambda: self.callButton("little_buttons"))
        self.big_button = Button(self.toolbar, text="Big Button", command=lambda: self.callButton("big_button"))
        self.main_button.pack(side=LEFT, fill=X)
        self.item_button.pack(side=LEFT, fill=X)
        self.progress_button.pack(side=LEFT, fill=X)
        self.little_buttons.pack(side=RIGHT, fill=X)
        self.big_button.pack(side=RIGHT, fill=X)
        self.toolbar.pack(side=TOP)
        self.canvas.pack()
        self.frame.pack()
    
    def callButton(self, screen):
        self.screen = screen
        self.updateCanvas()
    
    def drawCanvas(self):
        self.font_normal = font.Font(family='Arial', size=-12, weight="bold")
        self.font_mini = font.Font(family='Arial', size=7, weight="bold")
        x_offset = 40
        y_offset = 240+self.screen_gap
        #Top screen alignment
        self.top_screen_bg = self.canvas.create_image(0, 0, anchor = NW, image=self.i_top_screen_bg)
        self.top_screen_top_bar = self.canvas.create_image(0, 0, anchor = NW, image=self.i_top_screen_top_bar)
        self.top_screen_bottom_bar = self.canvas.create_image(0, 220, anchor = NW, image=self.i_top_screen_bottom_bar)
        self.top_screen_top_bar_shadow = self.canvas.create_image(0, 20, anchor = NW, image=self.i_top_screen_top_bar_shadow)
        self.top_screen_bottom_bar_shadow = self.canvas.create_image(0, 204, anchor = NW, image=self.i_top_screen_bottom_bar_shadow)
        self.wifi = self.canvas.create_image(347, 2, anchor = NW, image = self.i_wifi3)
        self.battery = self.canvas.create_image(371, 2, anchor = NW, image=self.i_battery_charging)
    
        #Bottom screen alignment
        self.bottom_screen_bg = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image=self.i_bottom_screen_bg)
        self.bottom_screen_top_bar = self.canvas.create_image(0+x_offset, 0+y_offset, anchor = NW, image=self.i_bottom_screen_top_bar)
        self.bottom_screen_bottom_bar = self.canvas.create_image(0+x_offset, 220+y_offset, anchor = NW, image=self.i_bottom_screen_bottom_bar)
        self.bottom_screen_top_bar_shadow = self.canvas.create_image(0+x_offset, 20+y_offset, anchor = NW, image=self.i_bottom_screen_top_bar_shadow)
        self.bottom_screen_bottom_bar_shadow = self.canvas.create_image(0+x_offset, 204+y_offset, anchor = NW, image=self.i_bottom_screen_bottom_bar_shadow)
    
        #Text alignment
        self.canvas.create_text(2, 10, anchor = W, font=self.font_normal, text = "Ver. 2.4.6") #FBI Version Number
        self.date_time = self.canvas.create_text(200, 10, font=self.font_normal, text = "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()))
        self.canvas.create_text(2, 230, anchor = W, font=self.font_mini, text = "SD: {} GiB, CTR NAND: {} MiB, TWL NAND: {} MiB, TWL Photo: {} MiB".format(self.sd_ex, self.ctrnand_ex, self.twlnand_ex, self.twlphoto_ex)) #Example Unit Stats
        
        #Main Menu Screen
        self.logo = self.canvas.create_image(200, 120, image="")
        self.bottom_screen_top_bar_text = self.canvas.create_text(200, 10+y_offset, font=self.font_normal, text = "")
        self.bottom_screen_listing = self.canvas.create_text(2+x_offset, 20+y_offset, anchor = NW, font=self.font_normal, text = "")
        self.bottom_screen_bottom_bar_text = self.canvas.create_text(200, 230+y_offset, font=self.font_normal, text = "")
        self.select_overlay = self.canvas.create_image(0+x_offset, 20+y_offset, anchor = NW, image="")
        self.scroll_bar = self.canvas.create_image(0+320+x_offset, 20+y_offset, anchor = NE, image="")

    def updateCanvas(self):
        config = getattr(sys.modules[__name__], "Configuration")()
        self.loadDynamicResources()
        #Top screen update
        self.canvas.itemconfig(self.top_screen_bg, image=self.i_top_screen_bg)
        self.canvas.itemconfig(self.top_screen_top_bar, image=self.i_top_screen_top_bar)
        self.canvas.itemconfig(self.top_screen_bottom_bar, image=self.i_top_screen_bottom_bar)
        self.canvas.itemconfig(self.top_screen_top_bar_shadow, image=self.i_top_screen_top_bar_shadow)
        self.canvas.itemconfig(self.top_screen_bottom_bar_shadow, image=self.i_top_screen_bottom_bar_shadow)
        
        #Wifi Charging
        wifi_icon = [self.i_wifi_disconnected, self.i_wifi0, self.i_wifi1, self.i_wifi2, self.i_wifi3]
        battery_icon = [self.i_battery_charging, self.i_battery0, self.i_battery1, self.i_battery2, self.i_battery3, self.i_battery4, self.i_battery5]
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
        self.canvas.itemconfig(self.date_time, fill=config.text, text = "{:%a %b %d %H:%M:%S %Y}".format(datetime.datetime.now()))
        
        if self.screen == "main_menu":
            self.canvas.itemconfig(self.logo, image=self.i_logo)
            self.canvas.itemconfig(self.select_overlay, image=self.i_selection_overlay)
            self.canvas.itemconfig(self.scroll_bar, image=self.i_scroll_bar)
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, fill=config.text, text = "Main Menu")
            self.canvas.itemconfig(self.bottom_screen_listing, fill=config.text, text = """SD\nCTR NAND\nTWL NAND\nTWL Photo\nTWL Sound\nDump NAND\nTitles\nPending Titles\nTickets\nExt Save Data\nSystem Save Data\nTitleDB\nRemote Install""")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, fill=config.text, text = "A: Select, START: Exit")
        else:
            self.canvas.itemconfig(self.bottom_screen_top_bar_text, text = "")
            self.canvas.itemconfig(self.bottom_screen_listing, text = "")
            self.canvas.itemconfig(self.bottom_screen_bottom_bar_text, text = "")
        self.canvas.after(1000, self.updateCanvas)
    
tl = Translations()
config = Configuration()
app = AppWindow()
app.mainloop()