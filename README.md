# MiniPOV Designer

Create [MiniPOV](https://www.adafruit.com/product/1776) designs without messing with Processing, paint, gimp, etc!

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