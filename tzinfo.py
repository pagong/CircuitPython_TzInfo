# tz.py  –  POSIX TZ string parser and UTC→local converter for CircuitPython
# No `re` module required.  Works on both hemispheres.
#
# POSIX TZ string format (the subset used here):
#   std offset [dst [offset] [,start[/time],end[/time]]]
#
# Offset sign convention (POSIX): positive = WEST of UTC  (e.g. EST5 = UTC-5)
# Examples:
#   "EST5EDT,M3.2.0,M11.1.0"          – US Eastern
#   "CET-1CEST,M3.5.0,M10.5.0/3"     – Central Europe
#   "AEST-10AEDT,M10.1.0,M4.1.0/3"   – Australia Eastern (southern hemisphere)
#   "NZST-12NZDT,M9.5.0,M4.1.0/3"    – New Zealand
#   "IST-5:30"                         – India (no DST)
#   "UTC0"                             – UTC

import time

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_hms(s):
    """Parse [+|-]h[:mm[:ss]] → total seconds.  POSIX sign: + means WEST."""
    s = s.strip()
    sign = 1
    if s.startswith('-'):
        sign = -1
        s = s[1:]
    elif s.startswith('+'):
        s = s[1:]
    parts = s.split(':')
    h = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 0
    sc = int(parts[2]) if len(parts) > 2 else 0
    return sign * (h * 3600 + m * 60 + sc)


def _split_name_offset(s):
    """
    Split a run like 'EST5' or 'CET-1' or 'AEST-10' into (name, offset_str).
    Name is everything up to the first digit, '+', or '-' that follows a letter.
    Returns (name, rest_of_string) where rest_of_string starts at the offset.
    """
    i = 0
    # Name: quoted (<...>) or plain letters (3+ chars by POSIX, but we're lenient)
    if s.startswith('<'):
        end = s.index('>')
        name = s[1:end]
        i = end + 1
    else:
        while i < len(s) and (s[i].isalpha()):
            i += 1
        name = s[:i]
    # Offset: remainder up to next alphabetic run (the DST name) or end
    j = i
    while j < len(s) and (s[j].isdigit() or s[j] in '+-:'):
        j += 1
    return name, s[i:j], s[j:]


def _is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


_DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _days_in_month(month, year):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _day_of_year_to_month_day(yday, year):
    """1-based yday → (month, day)."""
    rem = yday
    for m in range(1, 13):
        dm = _days_in_month(m, year)
        if rem <= dm:
            return m, rem
        rem -= dm
    return 12, 31


def _weekday_of_jan1(year):
    """Return weekday of Jan 1 of `year` (0=Mon … 6=Sun, Python convention)."""
    # Tomohiko Sakamoto / Zeller-lite
    y = year - 1
    return (y + y // 4 - y // 100 + y // 400 ) % 7  # 0=Mon


def _yday_of_mwd(month, week, wday, year):
    """
    POSIX Mm.w.d rule → 1-based day-of-year.
    month : 1-12
    week  : 1-5  (5 = last occurrence)
    wday  : 0-6  (0 = Sunday in POSIX)
    """
    # Convert POSIX Sunday-based wday to Python Monday-based
    py_wday = (wday - 1) % 7  # Sun(0)→6, Mon(1)→0 …

    # Find the first occurrence of py_wday in `month`
    # Jan 1 weekday (Python)
    jan1 = _weekday_of_jan1(year)
    # yday of 1st of month
    first_yday = 1
    for m in range(1, month):
        first_yday += _days_in_month(m, year)
    # weekday of the 1st of month
    first_wday = (jan1 + first_yday - 1) % 7
    # Days until target wday
    diff = (py_wday - first_wday) % 7
    yday_first = first_yday + diff          # 1st occurrence (1-based)

    days_in_m = _days_in_month(month, year)
    if week == 5:
        # Last occurrence
        candidate = yday_first
        while candidate + 7 <= first_yday + days_in_m - 1:
            candidate += 7
        return candidate
    else:
        return yday_first + (week - 1) * 7


def _parse_rule(rule):
    """
    Parse a POSIX transition rule (the part after the comma).
    Returns (month, week, wday, time_of_day_seconds) for Mm.w.d,
    or ('J', n, time) for Julian, or ('N', n, time) for 0-based Julian.
    Supported: Mm.w.d and Jn  (Nn rarely used but included).
    """
    # Split off optional /time
    if '/' in rule:
        date_part, time_part = rule.split('/', 1)
        tod = _parse_hms(time_part)
    else:
        date_part = rule
        tod = 2 * 3600   # default 02:00:00 wall clock

    if date_part.startswith('M'):
        parts = date_part[1:].split('.')
        return ('M', int(parts[0]), int(parts[1]), int(parts[2]), tod)
    elif date_part.startswith('J'):
        return ('J', int(date_part[1:]), tod)
    else:
        return ('N', int(date_part), tod)


def _rule_to_yday_and_tod(rule, year):
    """Return (yday_1based, time_of_day_seconds) for a parsed rule in `year`."""
    if rule[0] == 'M':
        _, month, week, wday, tod = rule
        return _yday_of_mwd(month, week, wday, year), tod
    elif rule[0] == 'J':
        _, n, tod = rule
        # Jn: 1-based, Feb 29 never counted
        return n, tod
    else:
        _, n, tod = rule
        # Nn: 0-based, Feb 29 counted on leap years
        return n + 1, tod


def _year_start_epoch(year):
    """Unix timestamp of Jan 1 00:00:00 UTC of `year`."""
    # Days from 1970-01-01 to year-01-01
    y = year - 1970
    leaps = 0
    for yr in range(1970, year):
        if _is_leap(yr):
            leaps += 1
    days = y * 365 + leaps
    return days * 86400


# ---------------------------------------------------------------------------
# TZInfo  –  parsed representation of a POSIX TZ string
# ---------------------------------------------------------------------------

class TZInfo:
    """
    Parsed POSIX TZ string.

    Attributes:
        std_name   : standard time abbreviation
        std_offset : standard offset from UTC in seconds (positive = east,
                     i.e. POSIX sign is inverted internally)
        has_dst    : True if DST rules are present
        dst_name   : DST abbreviation (or None)
        dst_offset : DST offset from UTC in seconds (or None)
        start_rule : parsed start-of-DST rule tuple (or None)
        end_rule   : parsed end-of-DST rule tuple (or None)
    """

    def __init__(self, tz_string):
        self._cache = {}   # year → (start_utc, end_utc)
        self._parse(tz_string)

    def _parse(self, s):
        # --- Standard name + offset ---
        std_name, std_off_str, rest = _split_name_offset(s)
        self.std_name = std_name
        # POSIX: positive offset = WEST; we store as seconds EAST
        self.std_offset = -_parse_hms(std_off_str) if std_off_str else 0

        if not rest:
            self.has_dst = False
            self.dst_name = None
            self.dst_offset = None
            self.start_rule = None
            self.end_rule = None
            return

        # --- DST name + optional offset ---
        dst_name, dst_off_str, rest = _split_name_offset(rest)
        self.dst_name = dst_name
        if dst_off_str:
            self.dst_offset = -_parse_hms(dst_off_str)
        else:
            # Default: std + 1 hour
            self.dst_offset = self.std_offset + 3600

        if not rest:
            # DST observed but no transition rules (unusual; treat as no DST)
            self.has_dst = False
            self.start_rule = None
            self.end_rule = None
            return

        self.has_dst = True
        # rest should be ",start,end" or ",start[/time],end[/time]"
        rules = rest.lstrip(',').split(',', 1)
        self.start_rule = _parse_rule(rules[0])
        self.end_rule   = _parse_rule(rules[1]) if len(rules) > 1 else None

    # -----------------------------------------------------------------------
    # DST transition cache
    # -----------------------------------------------------------------------

    def _transitions(self, year):
        """
        Return (dst_start_utc, dst_end_utc) for the given year,
        using a per-year cache.

        dst_start_utc : Unix timestamp when DST begins (wall-clock based)
        dst_end_utc   : Unix timestamp when DST ends
        """
        if year in self._cache:
            return self._cache[year]

        if not self.has_dst or self.start_rule is None or self.end_rule is None:
            self._cache[year] = (None, None)
            return (None, None)

        ys = _year_start_epoch(year)

        s_yday, s_tod = _rule_to_yday_and_tod(self.start_rule, year)
        e_yday, e_tod = _rule_to_yday_and_tod(self.end_rule, year)

        # Wall time at transition is expressed in *standard* time (POSIX spec)
        # DST starts: wall clock is still on std time
        dst_start = ys + (s_yday - 1) * 86400 + s_tod - self.std_offset
        # DST ends: wall clock is on DST time
        dst_end   = ys + (e_yday - 1) * 86400 + e_tod - self.dst_offset

        self._cache[year] = (dst_start, dst_end)
        return (dst_start, dst_end)

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def utc_to_local(self, utc_epoch):
        """
        Convert a UTC Unix timestamp (int or float) to a local-time tuple:
          (year, month, mday, hour, minute, second, weekday, yearday, is_dst)

        Compatible with CircuitPython's time.struct_time field order.
        weekday: 0=Monday … 6=Sunday
        is_dst : 0 or 1
        """
        utc_epoch = int(utc_epoch)

        # Determine which year this UTC timestamp falls in (approximate)
        # We check year-1 through year+1 to handle cross-year transitions.
        approx_year = 1970 + utc_epoch // 31557600  # 365.25 days
        offset, is_dst = self._offset_for(utc_epoch, approx_year)

        local = utc_epoch + offset
        #return _epoch_to_struct(local, is_dst)
        return time.struct_time( _epoch_to_struct(local, is_dst) )


    def _offset_for(self, utc_epoch, approx_year):
        """Return (offset_seconds_east, is_dst_int) for a UTC epoch."""
        if not self.has_dst:
            return self.std_offset, 0

        # Check the approximate year and neighbours to be safe near year edges
        for year in (approx_year - 1, approx_year, approx_year + 1):
            dst_start, dst_end = self._transitions(year)
            if dst_start is None:
                continue

            if dst_start < dst_end:
                # Northern hemisphere: DST is the middle segment
                # std … [dst_start] … DST … [dst_end] … std
                if dst_start <= utc_epoch < dst_end:
                    return self.dst_offset, 1
            else:
                # Southern hemisphere: DST wraps around the year boundary
                # DST … [dst_end] … std … [dst_start] … DST
                if utc_epoch >= dst_start or utc_epoch < dst_end:
                    return self.dst_offset, 1

        return self.std_offset, 0


# ---------------------------------------------------------------------------
# Epoch → broken-down time  (no datetime / time module needed)
# ---------------------------------------------------------------------------

def _epoch_to_struct(epoch, is_dst=0):
    """
    Convert a Unix epoch (seconds since 1970-01-01 00:00:00 UTC) to a tuple
    (year, month, mday, hour, minute, second, weekday, yearday, is_dst).
    weekday: 0=Monday … 6=Sunday  (same as Python / CircuitPython struct_time)
    """
    epoch = int(epoch)
    days  = epoch // 86400
    secs  = epoch % 86400

    hour   = secs // 3600
    minute = (secs % 3600) // 60
    second = secs % 60

    # Weekday: Jan 1 1970 was a Thursday = weekday 3
    weekday = (days + 3) % 7

    # Walk through years
    year = 1970
    while True:
        days_in_year = 366 if _is_leap(year) else 365
        if days < days_in_year:
            break
        days -= days_in_year
        year += 1

    yearday = days + 1  # 1-based
    month, mday = _day_of_year_to_month_day(yearday, year)

    return (year, month, mday, hour, minute, second, weekday, yearday, is_dst)


# ---------------------------------------------------------------------------
# Convenience: parse + convert in one call
# ---------------------------------------------------------------------------

def utc_to_local(utc_epoch, tz_string):
    """
    One-shot helper.  For repeated calls, prefer creating a TZInfo object.

    Returns (year, month, mday, hour, minute, second, weekday, yearday, is_dst).
    """
    return TZInfo(tz_string).utc_to_local(utc_epoch)

