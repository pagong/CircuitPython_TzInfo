# 'TzInfo' module 

'TzInfo' is a module for _CircuitPython_ to map UTC time to local time.
A POSIX TZ string is used to specify time zone and daylight saving times.

## Examples
Put the correct POSIX_TX variable for your location into the _settings.toml_ file of the CIRCUITPY drive.
- Central Europe: POSIX_TZ = "CET-1CEST,M3.5.0,M10.5.0/3"
- USA East: POSIX_TZ = "EST5EDT,M3.2.0,M11.1.0"
- UTC: POSIX_TX = "UTC0"

## Usage
See the "Berlin-Uhr" and "Word-Clock" directories in the examples directory.

