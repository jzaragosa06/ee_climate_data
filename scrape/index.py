import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize(project='ee-zukozaragosa2003')

import pandas as pd
import datetime
import plotly.express as px