from collections import defaultdict

from constants.common import ERRORS

TELEGRAM = "TELEGRAM"
SLACK = "SLACK"

NOTIFICATIONS_CHANNELS_TO_URL_PATH = defaultdict(
    None,
    {k.upper(): v for k, v in {
        ERRORS: "B08GJ5A7NMS/KHZMMCr85NPM4AYP35FKq6Rc",
    }.items()}
)
