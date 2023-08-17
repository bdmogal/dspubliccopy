#!/usr/bin/env python
# coding: utf-8

import requests
import xml.etree.ElementTree as ET
import csv
import json
#from dominodatalab import DominoClient

# Make a request to the API
## TODO: Make size configurable
response = requests.get("https://clinicaltrials.gov/api/query/full_studies?expr=&min_rnk=1&max_rnk=100&fmt=xml")

# Parse the XML response
root = ET.fromstring(response.content)

# Parse the XML string
#xml_string = """<FullStudyList><FullStudy Rank="1"><Struct Name="Study"><Struct Name="ProtocolSection"><Struct Name="IdentificationModule"><Field Name="NCTId">NCT05831969</Field></Struct></Struct></Struct></FullStudy><FullStudy Rank="2"><Struct Name="Study"><Struct Name="ProtocolSection"><Struct Name="IdentificationModule"><Field Name="NCTId">NCT05831970</Field></Struct></Struct></Struct></FullStudy></FullStudyList>"""
#root1 = ET.fromstring(xml_string)

# TODO: Make configurable
fields_to_fetch = ['NCTId', 'BriefTitle', 'OfficialTitle', 'OrgFullName', 'LeadSponsorName', 'IsFDARegulatedDrug', 'IsFDARegulatedDevice', 'Keyword', 'StudyType', 'PrimaryOutcomeDescription', 'SecondaryOutcomeDescription', 'Gender', 'MinimumAge', 'MaximumAge', 'Phase', 'DesignPrimaryPurpose', 'Condition', 'InterventionName', 'BriefSummary', 'DetailedDescription']

nct_ids = []
for full_study in root.findall('.//FullStudy'):
    study = {}
    for child in full_study.iter('Field'):
        name = child.attrib['Name']
        if name in fields_to_fetch:
            study[name] = child.text
    nct_ids.append(study)

with open("clinical_trials.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields_to_fetch)
    writer.writeheader()
    for row in nct_ids:
        #print('writing row' + json.dumps(row))
        writer.writerow(row)
#print(nct_ids)

