import re
import pandas as pd
# import numpy as np
import wikipediaapi
# from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from wikidata.client import Client


def dateFromString(a):
    s = re.sub(r'[^\w]', ' ', a)
    try:
        return parse(s, fuzzy_with_tokens=True)[0].date()
    except:
        return None


def findBirthDate(pageName):
    wiki_wiki = wikipediaapi.Wikipedia('en')
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


def getWikiDataParam(ID, p):
    client = Client()
    param = "#N/A"
    try:
        entity = client.get(ID, load=True)
    except:
        return param
    try:
        a = ["politician", "MEP", "diplomat", "servant", "legislative", "election", "candidate", "European",
             "Parliament",
             "minister", "politic", "syndicalist", "political", "economist", "council", "senator", "activist", "peer"]
        if any(x.lower() in entity.description.texts["en"].lower() for x in a) or "Politiker" in \
                entity.description.texts["de"].lower():
            prop = client.get(p)
            param = entity[prop]
            if p == 'P21':
                if param.id == "Q6581097":
                    param = "male"
                elif param.id == "Q6581072":
                    param = "female"
        return param
    except:
        return param


voteDate = dateFromString("26 March 2019")

data = pd.read_csv("Mepnames.csv")
data['Gender'] = data['Gender'].astype(str)
pdToList = list(data['Full Name'])

# print(data.head())


def main():
    for i in range(len(pdToList)):
        code = data.at[i, 'Wikidata code']
        if data.at[i, 'Gender'] == "#N/A" or data.at[i, 'Age'] == 0:
            data.at[i, 'Gender'] = getWikiDataParam(code, "P21")
            dob = getWikiDataParam(code, "P569")
            print(dob)
            if (type(dob) == str):
                dob = dateFromString(dob)
            data.at[i, 'DoB'] = dob
            difference_in_years = relativedelta(voteDate, dob).years
            data.at[i, 'Age'] = difference_in_years
        print(i)
        if i % 10 == 0:
            outputToCsv("Mepnames", data)
    outputToCsv("Mepnames", data)


if __name__ == '__main__':
    main()
