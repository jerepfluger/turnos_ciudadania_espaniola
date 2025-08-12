from collections import defaultdict

from constants.common import INSTAGRAM, PRENOTAMI, CITA_PREVIA, DGT, ERRORS

TELEGRAM = "TELEGRAM"
SLACK = "SLACK"

NOTIFICATIONS_CHANNELS_TO_URL_PATH = defaultdict(
    None,
    {k.upper(): v for k, v in {
        CITA_PREVIA: "B08DA3Y8A65/y2ReheoWjT7HvMUDcU7fxBdw",
        DGT: "B08H7JS613M/qvFRIZmcaHuochVUTB76Lw9V",
        ERRORS: "B08GJ5A7NMS/KHZMMCr85NPM4AYP35FKq6Rc",
        INSTAGRAM: "B08DA2PQR4Z/bgGLzigzHHuc4jmyQEGGelfa",
        PRENOTAMI: "B08CX703PNX/6iCEeJhyYiBrxvNE3zfL37tA",
    }.items()}
)
