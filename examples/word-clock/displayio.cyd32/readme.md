# "Word-Clocks" for Cheap Yellow Display with 3.2" LCD (ST7789)
This code is for the [Cheap Yellow Display](https://circuitpython.org/board/sunton_esp32_2432S032C/) with a 3.2 inch LCD display.
It is based on the _DisplayIO_ code of the "Matrix Portal S3" version.

## English words
The [original clock](https://adafruit-playground.com/u/VPTechOps/pages/rgb-matrix-word-clocks) has been published on the _Adafruit Playground_ by Frederick M. Meyer.
I've refactored his code by putting the word generation into a separate file (word_en_format.py) and using the UTC to local time converter (tzinfo.py).

## German words
The main code for the German version is very similar to the English version. However, I'm using a different word generator (word_de_format.py).

