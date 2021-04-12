#region Imports
import json, pytz

from datetime import datetime
#endregion

def get_timestamp():
    timezone = pytz.timezone('America/New_York')
    return timezone.localize(datetime.now())