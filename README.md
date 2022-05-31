# Radarr Upcoming Media Component

Home Assistant component to feed [Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card) with
Radarr's upcoming added media.</br>
This component does not require, nor conflict with, the default Radarr component.</br></br>
### Issues
Read through these two resources before posting issues to GitHub or the forums.
* [troubleshooting guide](https://github.com/custom-cards/upcoming-media-card/blob/master/troubleshooting.md)
* [@thomasloven's lovelace guide](https://github.com/thomasloven/hass-config/wiki/Lovelace-Plugins).


## Supporting Development
- :coffee:&nbsp;&nbsp;[Buy me a coffee](https://www.buymeacoffee.com/FgwNR2l)
- :heart:&nbsp;&nbsp;[Sponsor me on GitHub](https://github.com/sponsors/raman325)

### If you're having issues, check out the [troubleshooting guide](https://github.com/custom-cards/upcoming-media-card/blob/master/troubleshooting.md) before posting an issue or asking for help on the forums.

## Installation:

1. Install this component by copying [these files](https://github.com/custom-components/sensor.radarr_upcoming_media/tree/master/custom_components/radarr_upcoming_media) to `/custom_components/radarr_upcoming_media/`.
2. Install the card: [Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card)
3. Add the code to your `configuration.yaml` using the config options below.
4. Add the code for the card to your `ui-lovelace.yaml`. 
5. **You will need to restart after installation for the component to start working.**

### Options

| key | default | required | description
| --- | --- | --- | ---
| api_key | | yes | Your Radarr API key
| host | localhost | no | The host Radarr is running on.
| port | 7878 | no | The port Radarr is running on.
| urlbase | / | no | The base URL Radarr is running under.
| days | 60 | no | How many days to look ahead for the upcoming sensor.
| ssl | false | no | Whether or not to use SSL for Radarr.
| theaters | true | no | Show or hide theater releases.
| max | 5 | no | Max number of items in sensor.

**Do not just copy examples, please use config options above to build your own!**
### Sample for configuration.yaml:

```
sensor:
  - platform: radarr_upcoming_media
    api_key: YOUR_API_KEY
    host: 127.0.0.1
    port: 7878
    days: 14
    ssl: false
    theaters: false
    max: 10
```

### Sample for ui-lovelace.yaml:

    - type: custom:upcoming-media-card
      entity: sensor.radarr_upcoming_media
      title: Upcoming Movies
      

### Card Content Defaults

| key | default | example |
| --- | --- | --- |
| title | $title | "Night of the Living Dead" |
| line1 | $release | "In Theaters Mon, 10/31" if it's a theater release or "Available digitally/physically Monday" if it's a physical or digital release.|
| line2 | $genres | "Action, Adventure, Comedy" |
| line3 | $rating - $runtime | "★ 9.8 - 01:30"
| line4 | $studio | "Laurel Group Inc."
| icon | mdi:arrow-down-bold | https://materialdesignicons.com/icon/arrow-down-bold

### Credits

This integration was originally written by @maykar. Since the original repository for this integration was archived, this fork is an attempt to keep it alive.
