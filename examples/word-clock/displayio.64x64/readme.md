# "Word-Clocks" for Hub75 display matrix with 64x64 LEDs
This code is for Adafruit's [MatrixPortal S3](https://circuitpython.org/board/adafruit_matrixportal_s3/). The code is using _DisplayIO_ for rendering graphics.

## English words
This [clock](https://adafruit-playground.com/u/VPTechOps/pages/rgb-matrix-word-clocks) has been published on the _Adafruit Playground_ by Frederick M. Meyer.
I've refactored his code by putting the word generation into a separate file (word_en_format.py) and using the UTC to local time converter (tzinfo.py).

## German words
The main code for the German version is very similar to the English version. However, I'm using a different word generator (word_de_format.py).

