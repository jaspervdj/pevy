import pevy.sources.facebook
import pevy.sources.twitter
import pevy.sources.slack
import pevy.sources.time

sources = {
    'facebook': facebook.Facebook,
    'twitter': twitter.Twitter,
    'slack': slack.Slack,
    'time': time.Time,
}
