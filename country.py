import uuid
from datetime import datetime
class Country:
    def __init__(self, countryName):
        self.countryId = uuid.uuid4()
        self.countryName = countryName
        self.timeStampCreated = datetime.utcnow()
    def getInitCountryJson(self):
        return {
            "countryId": str(self.countryId),
            "countryName": self.countryName,
            "timeStampCreated": str(self.timeStampCreated),
            "fileIds": {}
        }
