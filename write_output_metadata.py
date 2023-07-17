###############################################################################
# Create metadata file
# Originally taken from the CITYCAT project:
#  https://github.com/OpenCLIM/citycat-dafni
#
# Robin Wardle
# May 2022
###############################################################################
import os
import pathlib
import datetime

##############################################################################
# Constants
###############################################################################
METADATA_FILENAME = "metadata.json"

##############################################################################
# Paths
###############################################################################
# Setup base path
platform = os.getenv("READ_PREPARE_DATA_ENV")
if platform=="docker":
    data_path = os.getenv("DATA_PATH", "/data")
else:
    data_path = os.getenv("DATA_PATH", "./data")

# INPUT paths
in_path = data_path / pathlib.Path("inputs")

# OUTPUT paths
out_path = data_path / pathlib.Path("outputs")
os.makedirs(metadata_path, exist_ok=True)


###############################################################################
# Metadata definition
###############################################################################
app_title = "pyramid-prepare-data"
app_description = "Prepare all rainfall data"
metadata = f"""{{
  "@context": ["metadata-v1"],
  "@type": "dcat:Dataset",
  "dct:title": "{app_title}",
  "dct:description": "{app_description}",
  "dct:identifier":[],
  "dct:subject": "Environment",
  "dcat:theme":[],
  "dct:language": "en",
  "dcat:keyword": ["PYRAMID"],
  "dct:conformsTo": {{
    "@id": null,
    "@type": "dct:Standard",
    "label": null
  }},
  "dct:spatial": {{
    "@id": null,
    "@type": "dct:Location",
    "rdfs:label": null
  }},
  "geojson": {{}},
  "dct:PeriodOfTime": {{
    "type": "dct:PeriodOfTime",
    "time:hasBeginning": null,
    "time:hasEnd": null
  }},
  "dct:accrualPeriodicity": null,
  "dct:creator": [
    {{
      "@type": "foaf:Organization",
      "@id": "http://www.ncl.ac.uk/",
      "foaf:name": "Newcastle University",
      "internalID": null
    }}
  ],
  "dct:created": "{datetime.datetime.now().isoformat()}Z",
  "dct:publisher":{{
    "@id": null,
    "@type": "foaf:Organization",
    "foaf:name": null,
    "internalID": null
  }},
  "dcat:contactPoint": {{
    "@type": "vcard:Organization",
    "vcard:fn": "DAFNI",
    "vcard:hasEmail": "support@dafni.ac.uk"
  }},
  "dct:license": {{
    "@type": "LicenseDocument",
    "@id": "https://creativecommons.org/licences/by/4.0/",
    "rdfs:label": null
  }},
  "dct:rights": null,
  "dafni_version_note": "created"
}}
"""

###############################################################################
# Write metadata file
###############################################################################
with open(metadata_path / pathlib.Path(METADATA_FILENAME), 'w') as f:
    f.write(metadata)

