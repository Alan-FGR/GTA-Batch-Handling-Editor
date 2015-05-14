# GTA-Batch-Handling-Editor
GTA Batch Handling Editor

UPDATE: Here is a link to a binary distribution (self extractor): https://drive.google.com/file/d/0B-imfIHFgQA5cGlpcUN6Ql9EU2M/view?usp=sharing
- It works with IV+EFLC (allows you to easily choose from different handling files)

When I used to play GTA IV, I liked modding the handling file to my tastes, however, I wanted to modify all the values of all vehicles (or some, e.g: bikes) at once, for example, multiplying the value of the engine power or top speed by some number; I couldn't find anything on the web to do that (for both IV and EFLC), so I decided to make my own.

This program should work with any GTA version (HD era) with only minor adjustments, so I'm waiting for the GTA V handling to be moddable in order to put it to the test and unlike the other editors, this one leaves the commented lines intact.

It's written in Python (2) and requires PyQt4 to work, in the future I'm going to build binaries with pyinstaller.

With this program you can easily select (and de-select) a vehicle category (sports cars, bikes, etc.) and add, multiply or set all the values of a variable. The categories are easily configured in the 'vehiclestypes' file.

Teh columns are configured in the 'cols' file. (formatting is like this: Header_Text Tooltip Width_Chars)

This isn't very nicely programmed because it was made originally only for personal usage, and personally, I don't care about some bad practices for my personal stuff as long as it works :).

Here's an old screenshot:
![image](https://fungamesreactor.files.wordpress.com/2015/05/sshot1.png)
