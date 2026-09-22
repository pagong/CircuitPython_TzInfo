# 'TzInfo' module 

'TzInfo' is a module for _CircuitPython_ to map UTC time to local time.
A POSIX TZ string is used to specify time zone and daylight saving times.

## Examples
Put the correct POSIX_TX variable for your location into the _settings.toml_ file of the CIRCUITPY drive.
- Central Europe: POSIX_TZ = "CET-1CEST,M3.5.0,M10.5.0/3"
- USA East: POSIX_TZ = "EST5EDT,M3.2.0,M11.1.0"
- UTC: POSIX_TX = "UTC0"

## Usage

```python
POSIX_TZ = os.getenv('POSIX_TZ')

# initialize TZinfo cache
our_tz = tzinfo.TZInfo(POSIX_TZ)

# let the onboard RTC run on UTC !
utc = time.time()

# convert UTC to local time
lt = our_tz.utc_to_local(utc)

hour   = lt.tm_hour
minute = lt.tm_min
second = lt.tm_sec
```

See the "Berlin-Uhr" and "Word-Clock" directories in the examples directory for working code.

