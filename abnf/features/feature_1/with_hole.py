"""
Collected rules from RFC 2616.
https://www.rfc-editor.org/rfc/rfc2616.html

Though RFC 2616 is largely obsolete, some later RFCs, not obsolete, 
still incorporate grammar from RFC 2616; in particular, RFC 6265.
Here we collect grammar from RFC 2616 as needed for use with other RFC grammars.
"""


from src.abnf1.parser import Rule as _Rule

from .misc import load_grammar


@load_grammar()
class Rule(_Rule):
    """Rule objects generated from ABNF in RFC 2616.
    Note that token rule is implemented from prose value in RFC 2616, and | was 
    replaced by / as expected by RFC 5234."""

    grammar = r'''
HTTP-date    = rfc1123-date / rfc850-date / asctime-date
rfc1123-date = wkday "," SP date1 SP time SP "GMT"
rfc850-date  = weekday "," SP date2 SP time SP "GMT"
asctime-date = wkday SP date3 SP time SP 4DIGIT
date1        = 2DIGIT SP month SP 4DIGIT
                ; day month year (e.g., 02 Jun 1982)
date2        = 2DIGIT "-" month "-" 2DIGIT
                ; day-month-year (e.g., 02-Jun-82)
date3        = month SP ( 2DIGIT / ( SP 1DIGIT ))
                ; month day (e.g., Jun  2)
time         = 2DIGIT ":" 2DIGIT ":" 2DIGIT
                ; 00:00:00 - 23:59:59
wkday        = "Mon" / "Tue" / "Wed"
            / "Thu" / "Fri" / "Sat" / "Sun"
weekday      = "Monday" / "Tuesday" / "Wednesday"
            / "Thursday" / "Friday" / "Saturday" / "Sunday"
month        = "Jan" / "Feb" / "Mar" / "Apr"
            / "May" / "Jun" / "Jul" / "Aug"
            / "Sep" / "Oct" / "Nov" / "Dec"

"""
  Defines a `token` using ABNF (Augmented Backus-Naur Form) syntax.

    The token is composed of one or more characters from the following set:
    - `!` (U+0021)
    - `#` to `'` (U+0023 to U+0027): `#`, `$`, `%`, `&`, `'`
    - `*` to `+` (U+002A to U+002B): `*`, `+`
    - `-` to `.` (U+002D to U+002E): `-`, `.`
    - `0` to `9` (U+0030 to U+0039)
    - `A` to `Z` (U+0041 to U+005A)
    - `^` to `z` (U+005E to U+007A): `^`, `_`, `` ` ``, `a` to `z`
    - `|` (U+007C)
"""
$PlaceHolder$
'''

