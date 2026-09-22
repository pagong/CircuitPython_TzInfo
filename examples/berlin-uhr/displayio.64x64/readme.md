# "Berlin-Uhr" for Hub75 display matrix with 64x64 LEDs
I am using a "RGB Matrix Adapter Board (E)" by [Seengreat](https://seengreat.com/wiki/186/rgb-matrix-adapter-board-e) to drive a 64x64 RGB matrix display (Hub75).
This adapter is _somewhat_ compatible to Adafruit's "MatrixPortal S3".

I am using the adapter with a cheap ESP32-S3 board by [VCC-GND](https://circuitpython.org/board/yd_esp32_s3_n16r8/).
However, this ESP32-S3 board is **not** working properly with version **V1.x** of the Seengreat matrix adapter.
Due to a collision of IO pins the onboard PSRAM of the ESP32-S3 needs to be disabled.
That's why I'm using _CircuitPython_ for the Espressif [ESP32SR-DevKit-C1-N16](https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n16/) board instead.
Version **V2.x** of the Seengreat matrix adapter is using different IO pins and should not have this problem.

The main code of the Berlin-Uhr can be found in file berlin_hub75.py.
Adafruit's _DisplayIO_ module is used as graphics engine.
The details are located in the included library berlin_display_32.py.

