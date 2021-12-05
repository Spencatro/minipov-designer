# MiniPOV Designer

Create [MiniPOV](https://www.adafruit.com/product/1776) designs without messing with Processing, paint, gimp, etc!

![MiniPOV Designer Example](https://media2.giphy.com/media/XQT6bnA5Y7nvUxj8oN/giphy.gif?cid=790b7611fcea938aa6253463b65f4ab09ce1c4260b4f9565&rid=giphy.gif&ct=g)

## Setup

This program is built with PyQt5. You may be able to just `pip install -r requirements.txt` depending on
your platform. On an m1 mac, I had to `brew install pyqt@5` .

## Running

```
python3.9 main.py
```

## Flashing .bin files

Once you've generated a .bin file (e.g. `design.bin`), use avrdude to flash to your MiniPOV:

```
avrdude -cusbtiny -pm328p -s -D -Ueeprom:w:design.bin:r
```