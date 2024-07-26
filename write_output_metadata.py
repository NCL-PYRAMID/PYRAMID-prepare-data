# Creates DAFNI dataset metadata for model: PYRAMID-prepare-data
# Copyright (C) 2022  Robin Wardle & Newcastle University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
metadata_path = out_path
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

