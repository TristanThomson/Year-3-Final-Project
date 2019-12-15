import pandas as pd

def outputToCsv(outputName, df):
	fileName = "output/" + outputName + ".csv"
	df.to_csv(fileName, index=False, encoding="utf-8-sig")

def filterCountryRow(df,input):
	return df[df.Country == input]

def filterEUGroupRow(df,input):
	return df[df.Political_Group == input]

def filterNatGroupRow(df,input):
	return df[df.National_Political_Group == input]

def listEUGroups(data):
	p_groups={}
	for index, row in data.iterrows():
		curGroup = row["Political_Group"]
		if curGroup not in p_groups.keys():
			p_groups[curGroup] = 1
		else:
			p_groups[curGroup] +=1
	return p_groups

def toPercentage(data, vote):
	a = data[vote].value_counts().to_frame()
	vote1 = a.to_dict()[vote]
	voteCount = 0
	for key, value in vote1.items():
		voteCount+= value
	for key, value in vote1.items():
		vote1[key] = "{0:.2f}".format((value/voteCount)*100)
	return vote1

def queryDataAgainst(data):
	d = data[data._26_March_2019_Final_Vote == ("AGAINST - CORRECTED" and "AGAINST")]
	return d
def queryDataFor(data):
	d = data[data._26_March_2019_Final_Vote == ("FOR - CORRECTED" and "FOR")]
	return d

def dispC(data,c):
	# for key in current_dict.keys():
	# if key == key_to_find:
	a = c.get('FOR - CORRECTED')
	b = c.get('AGAINST - CORRECTED')
	if a is not None:
			c['FOR'] = float(c.get('FOR'))+float(a)
	if b is not None:
			c['AGAINST'] = float(c.get('AGAINST'))+float(b)
	c['NOT VOTING'] = float(c.get('NOT PRESENT'))+float(c.get('ABSTAINED'))
	c.pop('FOR - CORRECTED',None)
	c.pop('AGAINST - CORRECTED',None)
	c.pop('NOT PRESENT',None)
	c.pop('ABSTAINED',None)
	print(c)


def findRebels(data,c):
	# print(c)
	a,b,d,e = 0,0,0,0

	if('FOR' in data.index):
		a = float(c["FOR"])
	if('FOR - CORRECTED' in data.index):
		b = float(c["FOR - CORRECTED"])
	if('AGAINST' in data.index):
		d = float(c["AGAINST"])
	if('AGAINST - CORRECTED' in data.index):
		e = float(c["AGAINST - CORRECTED"])

	if(a+b > d+e):
		if(d+e)<20.0 and (d+e) > 0.0:
			print(queryDataAgainst(data))
		else:
			print("no keyRebels in selected data")
	else:
		if(a+b)<20.0 and (a+b) > 0.0:
			print(queryDataFor(data))
		else:
			print("no keyRebels in selected data")



# take input from user on all criteria (A = Country, B = EU political group, C = National Political Group)
# keep track of all user filter wishes
# return probability of YES vote & csv file


def main():
	cols_to_use = [0,1,2,4,5,13]
	data = pd.read_csv("dataset.csv", usecols= cols_to_use, encoding='utf-8-sig')

	outputStr = ""
	euGroupInput = input("What EU Group to filter by? Type 'no' if no filter. ")
	countryInput = input("What country to filter by? Type 'no' if no filter. ")
	natGroupInput = input("What National Group to filter by? Type 'no' if no filter. ")
	print("\n")

	if(euGroupInput != "no" and type(euGroupInput) == str):
		outputStr += euGroupInput+"_"
		data = filterEUGroupRow(data,euGroupInput)
	if(countryInput != "no" and type(countryInput) == str):
		outputStr += countryInput+"_"
		data = filterCountryRow(data,countryInput)
	if(natGroupInput != "no" and type(natGroupInput) == str):
		outputStr += natGroupInput
		data = filterNatGroupRow(data,natGroupInput)

	# find rebels (condition if they voted against?)
	percentages = toPercentage(data, '_26_March_2019_Final_Vote')
	# print(percentages,"\n")
	findRebels(data,percentages)
	dispC(data,percentages);

	outputToCsv(outputStr,data)


if __name__ == '__main__':
    main()