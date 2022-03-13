# Aurora Forecast for Garmin inReach
Provides on-demand 3-day forecast of Kp index for Garmin InReach devices.

Know a chance of northern lights observation even in remote places.

![Aurora observed in Urho Kekkonen NP](img/aurora-ukk.jpg)

## How to use for free
From Garmin inReach device, send an email message with arbitrary text to `auroraforecast@seznam.cz` recipient.

Within 10 minutes, you will get message with Kp index forecast.
```
Kp for 3hr blocks UTC time.
12/03: 54312222
13/03: 21111134
14/03: 56444334
```

Service is provided for free, since it only uses free tier services and open data source.

Data is sourced from [NOAA Geomagnetic Activity Observation and Forecast](https://services.swpc.noaa.gov/text/3-day-forecast.txt).

As you can see in source report, each number represents forecast for 3-hour window, e.g. 00-03, 03-06, etc.
Time is in UTC, so you'll need to recalculate for your position.
For example Finland is 2 hours ahead of UTC, so first number represents 02-05 window.

If you want to save fees for outgoing message, you can add email above as a recipient of a preset message.
I usually need only 2 preset messages - to notify start and end of the hike, so third one can be reserved to get aurora forecast if weather conditions are favorable that night.
For incoming message, 1 text message is spent from your inReach credit.

## How it works
Message from inReach device is delivered to email with accompanying information about position and link to Garmin map, which allows reply to the message.

Email address mentioned above is periodically scanned for new incoming message.
Content of the message is ignored, but link to Garmin map is used to send a reply with current aurora forecast.

Every email is replied once, but you can request multiple forecasts per day.

## How to run own service
You may consider information provided in inReach message as sensitive.
It contains your location and provides link with reply form which can be misused for spamming - and spam delivered via satellite may be very expensive.

You can simply run your own service. Just send inReach message to your own email inbox and schedule provided `notify-aurora.py` script to check for inReach emails and reply to them.

Script can be deployed and scheduled for free with [Heroku](https://www.heroku.com).
As an email, you can use any free mail service providing IMAP access.
I recommend creating dedicated email and not using regular personal email for security reasons.

If using the script as-is, you'll need to provide following environment variables for email access:

- `IMAP_URL` - url of IMAP server of your email provider, e.g. `imap.gmail.com`
- `IMAP_LOGIN` - login for IMAP (usually your email address)
- `IMAP_PASSWORD` - password for IMAP (usually your email password)

## How to improve
Do you have any questions?

Do you have any ideas for improvement?

Feel free to [leave a comment](https://github.com/hajekr/aurora-forecast/issues/new) or open a pull request in [GitHub repo](https://github.com/hajekr/aurora-forecast).