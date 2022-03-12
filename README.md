Recently I received a letter from some company asking me to give them 50 bucks so they would recover some money due to me.

This definitely smelled like a scam, but after dismissing at first I decided to investigate anyway, and found out that indeed there was "unclaimed property" in my name. Apparently I overpaid for insurance or something and they were trying to refund me (i haven't changed my e-mail address or phone number though, ahem...)

After filing by mail (yes they have a web form, which is great... as it fills out some parts of the paper application I still needed to mail), I then got a letter back from the State telling me they would process my request in the next 180 days and to check on their website for a status update. How convenient!

And that's where this script comes in: it will just scrape the California State Controller's Unclaimed Property website and return the status for a given case:

```
python3 scraper.py 123456789
```

where 123456789 is the case number.
The script returns one thing only, the status text. In my case it's showing "Received by State Controller's Office" right now.

What you could do with this is write it to a file, then run it again and compare to what is in that file, and if it doesn't match, send a Pushover notification. You'd use this in a cron job so it runs regularly. If this is a personal machine, you could use your an anacron hourly / daily job. This way you'd get updated every time the status changes.

Something like this:


```
touch old_status
python3 scraper.py 123456789 > new_status
diff old_status new_status > /dev/null || pushover_notify --title  "New Unclaimed Property Status" --message "$(cat new_status)"
mv new_status old_status
```

Line 3 compares the old status with the new, discarding the output of diff in the process, which is useful if we use this in a cron job. If the status has changed, diff fails (non zero exit code) and pushover_notify gets triggered.
