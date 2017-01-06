# FBIThemePreviewer
The shady stopgap solution to all of your FBI theming needs.
Built on Python 3 and tkinter, FBITP is a currently completely user-unfriendly program, 
with 4 buttons that do literally nothing. The exe file is literally for the dunces that
don't have python already installed on their computers, so that can see what the program
does.

To actually use the previewer, you need to have the files in the romfs/ folder (or if you
are using the .py script, you can set it...Configurations => theme_folder). There is no 
user friendly checks that make sure the program doesn't break when unexpected things happen.
So if you are missing a file, or have a typo, fix it.

Features:
- Main menu preview
- Meta info preview
- Progress bar preview
- Rotating wifi icon (disconnected, wifi0, wifi1, wifi2, wifi3)
- Rotating battery icon (charging, battery0, etc.)
- Rotating progress bar (0%, 25%, 50%, 75%, 100%)
- A working clock
- At least 5 buttons to press (4 of which do nothing)
- Poorly written internals
- Randomly picked font family

Things to do:
- Add a screen that has two buttons (iunno, copy FBI updates screen)
- Add a screen that has one button (install finished)
- Add derp generators for titleID, media type, version, product code, region, and size.
- Read/Write to textcolor.cfg
- Color picker text colors
- Translation support