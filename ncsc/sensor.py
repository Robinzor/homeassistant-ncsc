import logging
import feedparser
import re
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

URL = "https://advisories.ncsc.nl/rss/advisories"
SCAN_INTERVAL = timedelta(minutes=1)
RISK_PATTERN = re.compile(r"(/)")

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([NCSCSensor()], True)

class NCSCSensor(SensorEntity):
    def __init__(self):
        self._state = "None"
        self._advisories = []
        self._attr_name = "NCSC Advisories"
        self._attr_icon = "mdi:alert"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {"advisories": self._advisories}

    def update(self):
        try:
            feed = feedparser.parse(URL)
            advisories = []

            for entry in feed.entries:
                title = entry.title
                timestamp = entry.published
                
                if RISK_PATTERN.search(title):
                    advisories.append({"title": title, "timestamp": timestamp})
                
                if len(advisories) >= 10:
                    break

            self._advisories = advisories
            self._state = advisories[0]["title"] if advisories else "None"
            _LOGGER.info("NCSC sensor updated: %d advisories found", len(advisories))

        except Exception as e:
            _LOGGER.error("Error fetching NCSC RSS feed: %s", e)
            self._state = "None"
