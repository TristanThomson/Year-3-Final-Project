import pandas as pd
# import random as rdm
import twint as tw
import os
from Twitter_scraping.tscraper import TwintScraper

min_df = pd.read_csv("../20191110 - Key Rebels/output/minorities.csv", encoding='utf-8-sig')
all_df = pd.read_csv("../20191110 - Key Rebels/data/dataset.csv", encoding='utf-8-sig')



# def draw_MEP(self, meps_df=min_df):
#     index = rdm.randrange(0, len(meps_df))
#     rand_mep = meps_df.loc[index, "Twitter"]
#     return rand_mep
#
# def randomMEPs(self, num_select):
#     output = [None] * num_select
#     for i in range(num_select):
#         rand_mep = self.draw_MEP()
#         while rand_mep not in output:
#             rand_mep = self.draw_MEP()
#             output[i] = rand_mep
#         while type(rand_mep) != str or not self.accountExists(rand_mep):
#             rand_mep = self.draw_MEP()
#             while rand_mep not in output:
#                 rand_mep = self.draw_MEP()
#                 output[i] = rand_mep
#
#     return output

def collect_connections(ts, rndm):
    for index, row in all_df.iterrows():  # traverses all MEPs in all_df
        mep = str(row["Twitter"]).lower()  # assigns and lowercases the handle of the MEP in current row
        group = row["Political_Group"]  # assigns the political group of the MEP in current row
        state = "majority"  # assigns default "state" of their vote
        if mep.lower() in map(lambda x: x.lower(), rndm.min_df["Twitter"].dropna()):
            state = "minority"  # assigns minority state if the handle is contained in min_df
        try:
            if os.path.isfile(group + "/" + state + "/" + mep + "/following.csv"):
                continue  # skips to next MEP if current MEP's data has already been collected
            # print("------handle:------")
            if rndm.accountExists(mep):
                if not os.path.isfile(group + "/" + state + "/" + mep + "/followers.csv"):
                    ts.user_followers(mep, group, state)  # begin scraping followers if the file doesn't exist
                tw.storage.panda.clean
                if not os.path.isfile(group + "/" + state + "/" + mep + "/following.csv"):
                    ts.user_following(mep, group, state)  # begin scraping followings if the file doesn't exist
            # else:
            #     print("no handle")
        except Exception as e:  # acts as a log
            ts.user_info(mep)
            pass

def csvfilesize(filename):
    with open(filename) as f:
        return sum(1 for line in f)

def converter_helper(f,user,fname,df):
    hello = fname
    for i, line in enumerate(f):
        if i == 0:
            continue
        is_mep = False
        if str(line[:-1]).lower() in map(lambda x: x.lower(), all_df["Twitter"].dropna()):
            is_mep = True
        if fname == "followers.csv":
            df = df.append({'Source': line[:-1], 'Target': user, 'S_is_MEP': is_mep, 'T_is_MEP': True}, ignore_index=True)
        elif fname == "following.csv":
            df = df.append({'Source': user, 'Target': line[:-1], 'S_is_MEP': True, 'T_is_MEP': is_mep}, ignore_index=True)
    return df

def converter(Scraper):
    print("this is converter")
    for index, row in all_df.iterrows():  # traverses all MEPs in all_df
        # if str(row["Twitter"]).lower() == username:
        df = pd.DataFrame(columns=['Source', 'Target', 'S_is_MEP', 'T_is_MEP'])
        username = str(row["Twitter"]).lower()  # assigns and lowercases the handle of the MEP in current row
        group = row["Political_Group"]  # assigns the political group of the MEP in current row
        state = "majority"  # assigns default "state" of their vote
        if username.lower() in map(lambda x: x.lower(), min_df["Twitter"].dropna()):
            state = "minority"
        if Scraper.accountExists(username) and not os.path.isfile(group + "/" + state + "/" + username + ".csv"):
            file_size = 0
            for file in ["followers.csv","following.csv"]:
                try:
                    with open(group + "/" + state + "/" + username + "/" + file) as f:
                        df = converter_helper(f,str(row["Twitter"]).lower(),file,df)
                    file_size += csvfilesize(group + "/" + state + "/" + username + "/" + file)
                except:
                    print("hey")
            if len(df.index) == file_size-2:
                print(len(df.index), file_size-2)
                print("file written to " + group + "/" + state + "/" + username + ".csv")
                Scraper.dftocsv(group + "/" + state + "/" + username, df)
    #takes mep as input
    #finds mep group in dataset
    #finds both files of mep
    #makes new df with columns :source, target, source_mep, target_mep
    #if file followers.csv, source is row, target is mep
    #if file following.csv, source is mep, target is mep




def main():
    # initialise both necessary classes
    Scraper = TwintScraper()
    # collect_connections(Scraper)
    converter(Scraper)

if __name__ == "__main__":
    main()
