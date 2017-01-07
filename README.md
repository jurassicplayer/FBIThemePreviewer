# FBIThemePreviewer
The shady stopgap solution to all of your FBI theming needs.
Built on Python 3 and tkinter, FBITP is a currently completely user-unfriendly program, 
with 2 buttons that do literally nothing. The exe file is literally for the dunces that
don't have python already installed on their computers, so that can see what the program
does.

To actually use the previewer, you need to have the files in the romfs/ folder or set a 
folder with the config file (theme_folder). There is no user friendly checks that make 
sure the program doesn't break when unexpected things happen. So if you are missing a 
file, or have a typo, fix it.

Features:
- Main menu preview
- Meta info preview
- Progress bar preview
- Rotating wifi icon (disconnected, wifi0, wifi1, wifi2, wifi3)
- Rotating battery icon (charging, battery0, etc.)
- Rotating progress bar (0%, 25%, 50%, 75%, 100%)
- A working clock
- At least 5 buttons to press (2 of which does nothing)
- Following selection overlay on left mouse press
- Poorly written internals
- Randomly picked font family
- Reading from textcolor.cfg
- Instant write to textcolor.cfg on color change
- Colorpicker for text colors (right click relevant text line in Meta Info screen)

Things to do:
- Add a screen that has two buttons (iunno, copy FBI updates screen)
- Add a screen that has one button (install finished)
- Add derp generators for titleID, media type, version, product code, region, and size.
- Translation support

Things to note:
- This is a stop-gap solution, make no mistakes with anything, because there is no safety
net to stop you from ruining your carefully picked colors with a simple misclick. Since
currently this program writes to textcolor.cfg right after you change a color, it is very
easy to lose the previous color you had, unless you have good memory.
- If you are missing files, this program will probably crash.