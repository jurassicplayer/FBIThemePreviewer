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
- A subsampled and then zoomed selection overlay bar (I can't fix this, FBI's theme image is 
    320x20, but on the 3DS it shows up as 320x15 through some voodoo that I can't replicate
    with tkinter)
- Rotating wifi icon (disconnected, wifi0, wifi1, wifi2, wifi3)
- Rotating battery icon (charging, battery0, etc.)
- A working clock
- At least 5 buttons to press (4 of which do nothing)
- Poorly written internals

Things to do:
- Add progress bar screen (and no, it's not going to move)
- Add a screen that has two buttons (iunno, copy FBI updates screen)
- Add a screen that has one button (install finished)
- Add a screen that has item metadata (Titles)
    - Add derp generators for titleID, media type, version, product code, region, and size.
- Add a preview text colors screen (something that shows all the colors)
- Read/Write to textcolor.cfg
- Color picker text colors
- Translation support