# OpenAPI
from enum import Enum


OPENAPI_TITLE = '3D&T Victory Character Creator API'
OPENAPI_SUMMARY = 'An API for creating/storing 3D&T characters'
OPENAPI_DESCRIPTION = '''
## Features
- A
- B
- C
'''
OPENAPI_VERSION = '0.0.1'
OPENAPI_TERMS_OF_SERVICE = 'http://example.com/terms/'
OPENAPI_CONTACT = {
        "name": "Luis Yamada",
        "url": "https://www.linkedin.com/in/luis-yamada/",
        "email": "luishm.yamada@gmail.com",
    }
OPENAPI_LICENSE_INFO = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }


# Expertises (Habilidades)
class Expertises(Enum):
    ANIMALS = 1
    ARTS = 2
    SPORTS = 3
    INFLUENCE = 4
    FIGHT = 5
    TRICKERY = 6
    MACHINES = 7
    MEDICINE = 8
    MYSTIC = 9
    PERCEPTION = 10
    KNOWLEDGE = 11

    def to_list():
        return [member.name for member in Expertises]