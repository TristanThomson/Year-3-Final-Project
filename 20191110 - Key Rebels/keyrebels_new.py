from collections import OrderedDict

import pandas as pd
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

EU_Groups = ["GUE-NGL", "ECR", "EPP", "S&D", "ALDE", "EFDD", "Greens-EFA", "Non-attached", "ENF"]
genders = ["male", "female"]
votes = ["FOR", "ABSTAINED", "NOT PRESENT", "AGAINST"]
all_countries = ["Estonia", "Latvia", "Lithuania", "Poland", "Czech Republic", "Slovakia", "Hungary", "Malta", "Cyprus",
                 "Slovenia", "Romania", "Bulgaria", "Croatia", "France", "Germany", "Italy", "Belgium", "Netherlands",
                 "Luxembourg", "United Kingdom", "Ireland",
                 "Denmark", "Greece", "Spain", "Portugal", "Austria", "Sweden", "Finland"]
country_groups = {
    'eu13': ["Estonia", "Latvia", "Lithuania", "Poland", "Czech Republic", "Slovakia", "Hungary", "Malta", "Cyprus",
             "Slovenia", "Romania", "Bulgaria", "Croatia"],
    'eu15': ["France", "Germany", "Italy", "Belgium", "Netherlands", "Luxembourg", "United Kingdom", "Ireland",
             "Denmark", "Greece", "Spain", "Portugal", "Austria", "Sweden", "Finland"]}


def outputToCsv(outputName, df):
    fileName = "output/" + outputName + ".csv"
    df.to_csv(fileName, index=False, encoding="utf-8-sig")


# function from https://matplotlib.org/
def survey(results, category_names, name):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1, dtype=float)
    category_colors = plt.get_cmap('RdYlGn_r')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        # print(starts)
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.2 else 'black'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(float(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plt.savefig(str(name) + "out.png")
    return fig, ax


# print(listEUGroups("Political_Group",df))
def listEUGroups(a, data):
    p_groups = {}
    for index, row in data.iterrows():
        curGroup = row[a]
        if curGroup not in p_groups.keys():
            p_groups[curGroup] = 1
        else:
            p_groups[curGroup] += 1
    return list(p_groups.keys())


def filterEUGroupRow(df, group):
    return df[df.Political_Group == group]


def filterCountryGroups(df, group):
    return df[df['Country'].isin(group)]


def filterGender(df, group):
    return df[df.Gender == group]


def filterAge(df, criteria, threshold):
    if criteria == "above":
        return df[df.Age >= threshold]
    elif criteria == "below":
        return df[df.Age <= threshold]


def combineVotes(dict):
    ordered = OrderedDict([('FOR', 0), ('ABSTAINED', 0), ('NOT PRESENT', 0), ('AGAINST', 0)])
    for i in votes:
        a = i + " - CORRECTED"
        if a in dict.keys() and i in dict.keys():
            dict[i] += dict.pop(a)
        if i in dict.keys():
            ordered[i] = dict[i]
    return ordered


def toPercentage(data, vote):
    voteCount = data[vote].value_counts().to_frame()
    voteDict = voteCount.to_dict()[vote]
    voteDict = combineVotes(voteDict)
    voteTot = len(data.index)
    for key, value in voteDict.items():
        voteDict[key] = float("{0:.2f}".format((value / voteTot) * 100))
    return voteDict


def main():
    cols_to_use = [0, 1, 2, 4, 5, 7, 8, 16]
    df = pd.read_csv("data/dataset.csv", usecols=cols_to_use, encoding='utf-8-sig')

    # results5 = {}
    # data1 = filterEUGroupRow(df, 'EPP')
    # data2 = filterCountryGroups(data1, country_groups['eu15'])
    # data3 = filterAge(data2, 'above', 55.48666667)
    # a = toPercentage(data3, '_26_March_2019_Final_Vote')
    # results5["EPP, eu15, above avg"] = list(a.values())

    # results6 = {}
    # data4 = filterEUGroupRow(df, 'Greens-EFA')
    # data5 = filterCountryGroups(data4, country_groups['eu13'])
    # data6 = filterAge(data5, 'below', 55.48666667)
    # a = toPercentage(data6, '_26_March_2019_Final_Vote')
    # results6["Greens-EFA, eu13, below avg"] = list(a.values())
    # outputToCsv('greens-eu13-below', data6)

    results7 = {}
    for i in country_groups:
        data7 = filterCountryGroups(df, country_groups[i])
        print(i)
        for j in genders:
            print(j)
            data8 = filterGender(data7, j)
            a = toPercentage(data8, '_26_March_2019_Final_Vote')
            results7[i + " " + j] = list(a.values())
    # outputToCsv('greens-eu13-below', data6)

    # voting for the passing but being in the party minority is more interesting

    # # is there a correlation in groups?
    # results = {}
    # for i in EU_Groups:
    #     data = filterEUGroupRow(df, i)
    #     a = toPercentage(data, '_26_March_2019_Final_Vote')
    #     results[i] = list(a.values())
    #
    # # is there a correlation in gender?
    # results2 = {}
    # for i in genders:
    #     data = filterGender(df, i)
    #     a = toPercentage(data, '_26_March_2019_Final_Vote')
    #     results2[i] = list(a.values())
    #
    # # is there a correlation in age?
    # results3 = {}
    # age_avg = 55.48666667
    # for i in ["above","below"]:
    #     age_filtered = filterAge(df, i, age_avg)
    #     a_vote_percent = toPercentage(age_filtered, '_26_March_2019_Final_Vote')
    #     results3[i] = list(a_vote_percent.values())
    #
    # # eu15/eu13 analyses?
    # results4 = {}
    # for j in country_groups:
    #     d = filterCountryGroups(df, country_groups[j])
    #     a = toPercentage(d, '_26_March_2019_Final_Vote')
    #     results4[j] = list(a.values())
    #
    # survey(results, votes,"groups")
    # survey(results2, votes,"gender")
    # survey(results3, votes,"age")
    # survey(results4, votes,"location")
    # survey(results5, votes,"")
    survey(results7, votes, "gender+location")
    plt.show()


if __name__ == '__main__':
    main()
