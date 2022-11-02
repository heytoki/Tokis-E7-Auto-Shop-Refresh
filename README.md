# Tokis E7 Auto Shop Refresh
 EmaOlay previously made one using pictures but that requires different pictures
 for different video settings.
 
 This one only requires to change a single line in the code to match the emulator
 of your choice.
 
 It doesn't work 100% of the time, maybe missing a bookmark or two once in a while.
 
 Go ahead and change everything to your liking. If you improved it, I hope you share
 it with everyone. :)
 
*Written in Python 3.9.6 in case it doesn't work in future versions*

Steps for Setting up!!!
-
Install Python!
https://www.python.org/downloads/release/python-396/

Install tesseract ocr!
https://github.com/UB-Mannheim/tesseract/wiki

Download my python code!
1. Go to main.py
2. Open it raw
3. Save as anywhere you would like to access it from

Once Python is installed, use the Windows Search Bar and run CMD as administrator then run the following:

`pip install opencv-python`

`pip install pyautogui`

`pip install pywin32`

`pip install pypiwin32`

`pip install Pillow`

How to use my macro!
-
Once everything is installed, run IDLE (Python 3.9)

`File > Open > Find and open main.py`

Inside main.py, change the Application variable to whatever emulator you are using.
(To know the emulator's name, open it and hover over it in the taskbar.)

Check C:\Program Files\Tesseract-OCR in File Explorer and see if it exists. If it does not, check other drives 
and program files and look for Tesseract-OCR.

Once you find it, copy the file directory and paste it with an additional " \ " with tesseract.exe added to the end (ex.
C:\\Program Files\\Tesseract-OCR\\tesseract.exe) in main.py 

`pytesseract.tesseract_cmd = C:\\Program Files\\Tesseract-OCR\\tesseract.exe`

If you have your emulator secret shop open, go to 

`Run > Run Module`

**The emulator HAS to be on your main monitor!**

**If you want to stop the macro, drag your mouse to the TOP LEFT corner of your monitor!**

*Warning!!!*
-

If you want to change stuff other than Application, feel free. I am too lazy and didn't leave any comments on what does
what. The easiest thing to change is `time.sleep(seconds)`, but lowering the sleep time MIGHT make the macro make more 
mistakes. Change at your own risk!