import re

import pandas as pd
import numpy as np
import wikipediaapi
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


def dateFromString(input):
    s = re.sub(r'[^\w]', ' ', input)
    try:
        return parse(s, fuzzy_with_tokens=True)[0]
    except:
        return voteDate


def findBirthDate(pageName):
    try:
        page_py = wiki_wiki.page(pageName)
        summary = page_py.summary
    except:
        return ""
    result = dateFromString(summary[0:100])
    if "politician" in summary or "Member of the European" in summary:
        return result
    return voteDate


def outputToCsv(outputName, df):
    fileName = outputName + ".csv"
    df.to_csv(fileName, index=False, encoding="utf-8-sig")


voteDate = dateFromString("26 March 2019")

data = pd.read_csv("Mepnames2.csv")
pdToList = list(data['Full Name'])

print(data.head())

wiki_wiki = wikipediaapi.Wikipedia('en')
counter = 0
for i in pdToList:
    bDate = findBirthDate(i)
    difference_in_years = relativedelta(voteDate, bDate).years
    data.at[counter, 'Age'] = difference_in_years
    counter = counter + 1

print(data.head())
outputToCsv("withAge", data)

# print(ages)
