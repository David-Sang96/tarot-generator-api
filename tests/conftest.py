import os

# Tests always use the bundled deck. Remove any TAROT_DATA_PATH from the shell
# before app.core.config creates its settings.
os.environ.pop("TAROT_DATA_PATH", None)
