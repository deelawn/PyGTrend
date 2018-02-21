# PyGTrend
An python API to pull data from Google Trends and calculate the correlation between two trends

See the trend test for a simple example of how to use this.  Also note the libraries that are referenced in  GTrend.  I did not include
these so you'll have to verify that you have them installed.  Also install PhantomJS. Check GTrend for how to specify specific date ranges.
Check google trends if you want to use category values, country codes, or search types.

It works but it's a bit slow due to having to wait for the JS to be parsed.  No real documentation at them moment other that what I've
written here due to the many improvements I'll be making.  One should also note that Google's robots.txt file prohibits access to the
trends domain, so use at your own risk.

A demo is available here:  
http://deelawn.ninja/gtrend/

An explanation of how to use the demo is available here:  
https://steemit.com/data/@deelawn/google-trends-analysis-determining-correlation-of-two-search-terms
