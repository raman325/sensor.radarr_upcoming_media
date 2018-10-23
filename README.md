# Radarr Upcoming Media Component

Component required to use the associated Lovelace card: [Upcoming_Media_Card](https://github.com/custom-cards/upcoming-media-card)</br>
This is just a modified version of home assistants default sonarr (not a typo, modified from sonarr not radarr) component.</br>
This component works with or without the default radarr component.</br></br>Unfortunately, there seems to be no reliable source for movie banner images and as such there is no banner view for this component.</br></br>
<link href="https://fonts.googleapis.com/css?family=Lato&subset=latin,latin-ext" rel="stylesheet"><a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/FgwNR2l"><img src="https://www.buymeacoffee.com/assets/img/BMC-btn-logo.svg" alt="Buy me a coffee"><span style="margin-left:5px">If you feel I deserve it, you can buy me a coffee</span></a></br>
</br>
<a href="https://www.themoviedb.org/"><img width="200" src="https://www.themoviedb.org/assets/1/v4/logos/408x161-powered-by-rectangle-green-bb4301c10ddc749b4e79463811a68afebeae66ef43d17bcfd8ff0e60ded7ce99.png">
</br>This product uses the TMDb API but is not endorsed or certified by TMDb.</a>

## Installation:

1. Install this component by copying to your `/custom_components/sensor/` folder.
2. Add this to your `configuration.yaml` using the config options below example. 
3. **You will need to restart for the component to start working.**

```yaml
sensor:
- platform: radarr_upcoming_media
  api_key: YOUR_API_KEY
  host: 192.168.1.4
  port: 7878
  days: 120
  ssl: true
```

### Options

| key | default | required | description
| --- | --- | --- | ---
| api_key | | yes | Your Radarr API key
| host | localhost | no | The host Radarr is running on.
| port | 7878 | no | The port Radarr is running on.
| urlbase | / | no | The base URL Radarr is running under.
| days | 60 | no | How many days to look ahead for the upcoming sensor, 1 means today only.
| ssl | false | no | Whether or not to use SSL for Radarr. Set to `True` if you use SSL.
| theaters | true | no | Show or hide theater releases.

