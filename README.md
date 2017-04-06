M/Monit Mattermost notification script
======================================

A script for [M/Monit](https://mmonit.com/) to enable notifications to a [Mattermost](http://www.mattermost.org/) server.

## Script Usage

Run `./mm-notify.py --help` for full usage information.

## Mattermost Configuration

Both M/Monit and Monit can quite easy be setup to send alerts to almost any online service. This is especially straightforward if the service sports a HTTP API. In this example we demonstrate how this can be done by sending notification to Mattermost.

On the Mattermost side you will first need to activate an integration and obtain a token integrations by adding an "Incoming WebHooks" integration. 

The solution is most the same as for Slack integration: https://mmonit.com/wiki/MMonit/SlackNotification

```
/usr/local/bin/mm-notify.py --url https://mattermost.server/hooks/<token> --notificationtype "$MONIT_ACTION"
```
