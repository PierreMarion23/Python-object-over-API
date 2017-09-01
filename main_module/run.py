import os
from main_module import app, logging

logging.info(app.config)
app.run(port=5044)
