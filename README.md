# FBIThemePreviewer
The shady stopgap solution to all of your FBI theming needs.
Built on Python 3 and tkinter, FBITP is a currently completely user-unfriendly program. 
The exe file is literally for the dunces that don't have python already installed on 
their computers or are too lazy to deal with dependecies (Pillow and Watchdog), so that
they can see what the program does.

To actually use the previewer, you need to have the files in the romfs/ folder or set a 
folder with the config file (theme_folder). There are some user friendly checks that try
to keep the program from breaking when unexpected things happen. So if you are missing a 
file, or have a typo, fix it.

Features:
- FBI simulator preview (right click bottom screen entries)
- Meta info preview
- Reading from textcolor.cfg
- Instant write to textcolor.cfg on color change
- Colorpicker for text colors (right click entry in Text Cfg)
- Auto-load correctly named created/modified image
- Cycling wifi, battery, progress bar images
- Configurable screen gap height
- A working clock
- At least 2 buttons to press
- Following selection overlay (left mouse press)
- Poorly written internals
- Randomly picked font family

Things to do:
- Add derp generators for titleID, media type, version, product code, region, and size.
- Translation support

Things to note:
- This is a stop-gap solution, make no mistakes with anything, because there is no safety
net to stop you from ruining your carefully picked colors with a simple misclick. Since
currently this program writes to textcolor.cfg right after you change a color, it is very
easy to lose the previous color you had, unless you have good memory.
- If you are missing files, this program might not crash.