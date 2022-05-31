"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Radarr upcoming releases.

https://github.com/raman325/sensor.radarr_upcoming_media

https://github.com/custom-cards/upcoming-media-card

"""
from datetime import date, datetime, timedelta
import logging

from aiopyarr.exceptions import ArrException
from aiopyarr.models.host_configuration import PyArrHostConfiguration
from aiopyarr.radarr_client import RadarrCalendar, RadarrClient
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import voluptuous as vol


__version__ = "0.3.6"

_LOGGER = logging.getLogger(__name__)

CONF_DAYS = "days"
CONF_URLBASE = "urlbase"
CONF_THEATERS = "theaters"
CONF_MAX = "max"

FIRST_CARD = {
    "title_default": "$title",
    "line1_default": "$release",
    "line2_default": "$genres",
    "line3_default": "$rating - $runtime",
    "line4_default": "$studio",
    "icon": "mdi:arrow-down-bold",
}

RELEASE_TEXT_MAP = {
    "digitalRelease": "Available digitally on $day, $date",
    "physicalRelease": "Available physically on $day, $date",
    "inCinemas": "In theaters on $day, $date",
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_DAYS, default=60): vol.Coerce(int),
        vol.Optional(CONF_HOST, default="localhost"): cv.string,
        vol.Optional(CONF_PORT, default=7878): cv.port,
        vol.Optional(CONF_SSL, default=False): cv.boolean,
        vol.Optional(CONF_URLBASE): cv.string,
        vol.Optional(CONF_THEATERS, default=True): cv.boolean,
        vol.Optional(CONF_MAX, default=5): vol.Coerce(int),
    }
)


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([RadarrUpcomingMediaSensor(hass, config)], True)


class RadarrUpcomingMediaSensor(SensorEntity):
    def __init__(self, hass, conf):
        url_base = conf.get(CONF_URLBASE)
        if url_base:
            url_base = "{}/".format(url_base.strip("/"))
        self._host_config = PyArrHostConfiguration(
            api_token=conf[CONF_API_KEY],
            hostname=conf[CONF_HOST],
            port=conf[CONF_PORT],
            ssl=conf[CONF_SSL],
            base_api_path=url_base,
        )
        self.client = RadarrClient(
            self._host_config, session=async_get_clientsession(hass)
        )
        self.days = conf.get(CONF_DAYS)
        self.theaters = conf.get(CONF_THEATERS)
        self.max_items = conf.get(CONF_MAX)

        self._attr_available = True
        self._attr_name = "Radarr Upcoming Media"

    def _get_air_date_key(self, movie: RadarrCalendar):
        """Return air date key."""
        out_of_bounds_date = date.today() + timedelta(days=(self.days + 1))
        keys = ["digitalRelease", "physicalRelease"]
        if self.theaters:
            keys.append("inCinemas")
        for key in keys:
            try:
                release_date = datetime.date(getattr(movie, key))
            except AttributeError:
                release_date = out_of_bounds_date
            if release_date >= date.today() and release_date < out_of_bounds_date:
                return key
        return None

    def _get_rating(self, movie: RadarrCalendar):
        """Return rating."""
        for key in ("tmdb", "imdb", "rottenTomatoes", "metacritic"):
            try:
                return "\N{BLACK STAR} " + str(getattr(movie.ratings, key).value)
            except AttributeError:
                continue
        return ""

    async def async_update(self):
        start = datetime.combine(date.today(), datetime.min.time())
        end = start + timedelta(days=self.days)
        try:
            movies = await self.client.async_get_calendar(
                start_date=start, end_date=end
            )
        except ArrException as err:
            if self._attr_available:
                _LOGGER.warning(err)
            self._attr_available = False
            return
        else:
            self._attr_available = True

        movies = [movie for movie in movies if self._get_air_date_key(movie)][
            : self.max_items
        ]
        self._attr_native_value = len(movies)
        self._attr_extra_state_attributes = {"data": [FIRST_CARD]}
        for movie in movies:
            air_date_key = self._get_air_date_key(movie)
            movie_data = {
                "airdate": datetime.date(getattr(movie, air_date_key)).isoformat(),
                "release": RELEASE_TEXT_MAP[air_date_key],
                "rating": self._get_rating(movie),
                "flag": movie.hasFile,
                "title": movie.attributes.get("title", ""),
                "runtime": movie.attributes.get("runtime", ""),
                "studio": movie.attributes.get("studio", ""),
                "genres": ", ".join(movie.attributes.get("genres", [])),
            }

            movie_data["poster"] = next(
                (image.url for image in movie.images if image.coverType == "poster"),
                "",
            )
            movie_data["fanart"] = next(
                (image.url for image in movie.images if image.coverType == "fanart"),
                "",
            )
            self._attr_extra_state_attributes["data"].append(movie_data)
