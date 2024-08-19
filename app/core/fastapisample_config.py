import logging

# Setting Logger
LOGGER = logging.getLogger(__name__)

# MAC_MATCH_PATTERN: MAC-XX-XX-XX-XX-XX-XX
MAC_MATCH_PATTERN = r"^MAC-([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})$"
# MAC_MATCH_PATTERN: MAC-XX-XX-XX-XX-XX-XX or ""
MAC_NULL_MATCH_PATTERN = r"^(MAC-([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})|)$"

FILE_SAVED_FOLDER = "images/"
