#!/home/tcast/Documents/Final_project/Year-3-Final-Project/venv/bin/ python3.6
import operator
import os
import sys
from pathlib import Path
import pandas as pd
import twint as tw
# for copied code
import requests
import re


# from datetime import datetime
# from datetime import timedelta


class TwintScraper:
    testvar = 5

    def dftocsv(self, outputName, df):
        fileName = outputName + ".csv"
        df.to_csv(fileName, index=False, encoding="utf-8-sig")

    def user_info(self, username):
        c = tw.Config()
        c.Username = username
        c.Format = "Username {username} | Bio {bio} | Private {private} | Followers {followers} | Friends {following}"
        c.Pandas = True
        tw.run.Lookup(c)

    # def accountExists(self, username):
    #     print(username, " being checked")
    #     if username == "nan":
    #         return False
    #     tw.output.users_list = []
    #     c = tw.Config()
    #     c.Username = username
    #     c.Store_object = True
    #     c.Format = "{username}"
    #     tw.run.Lookup(c)
    #     user = tw.output.users_list
    #     print(tw.output.users_list)
    #     return True if (len(user) > 0) else False

    def accountExists(self, username):
        if username == "nan":
            return False
        r = requests.get('https://twitter.com/' + username)
        text = r.text
        x = re.findall('Sorry, that page doesn’t exist!', text)
        return False if len(x) > 0 else True

    def track_errors(self):
        rootdir = os.getcwd()  # path to parent folder of current file
        tracker = []
        for path in Path(rootdir).rglob('*.csv'):
            if not os.path.isfile(str(path.parent) + "/followers.csv") or not os.path.isfile(
                    str(path.parent) + "/following.csv"):
                tracker.append(path.parent.name)
        print(tracker)

    def hashtag_helper(self, search, mep):  # gets twint to work while iterating through meps
        tweets = []
        # print(mep)
        c = tw.Config()
        c.Username = str(mep)
        c.Search = search
        c.Limit = 250
        c.Store_csv = False
        c.Hide_output = True
        c.Format = "{hashtags}"
        c.Since = "2019-02-13"
        c.Until = "2019-04-01"
        c.Store_object = True
        c.Store_object_tweets_list = tweets
        tw.run.Search(c)
        return tweets

    def get_hashtags(self, meps, search):
        counts = dict()
        for mep in meps:
            if not self.accountExists(mep):
                continue
            tweets = self.hashtag_helper(search, mep)
            for i in tweets:
                print(i.link)
                print(i.hashtags)
                for j in i.hashtags:
                    if j in counts:
                        counts[j] += 1
                    else:
                        counts[j] = 1
        for i in source_tags:
            if "#" + i in counts:
                del counts["#" + i]
        print(dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True)))

    def get_followings(self, username):
        # tw.storage.panda.clean
        print(tw.storage.panda.Follow_df)
        c = tw.Config()
        c.Username = username
        c.Pandas = True
        c.Hide_output = True
        c.Pandas_clean = True
        tw.run.Following(c)
        list_of_followings = tw.storage.panda.Follow_df
        print("collected following")
        out = list_of_followings['following'][username]
        return out

    def get_followers(self, username):
        print(tw.storage.panda.Follow_df)
        d = tw.Config()
        d.Username = username
        d.Pandas = True
        d.Hide_output = True
        d.Pandas_clean = True
        tw.run.Followers(d)
        print("collected followers")
        list_of_followers = tw.storage.panda.Follow_df
        out = list_of_followers['followers'][username]
        return out

    def user_followers(self, username, party, state):
        if not os.path.exists(party + "/" + state + "/" + username):
            os.makedirs(party + "/" + state + "/" + username)
        if os.path.isfile(party + "/" + state + "/" + username + "/followers.csv"):
            return
        test = self.get_followers(username)
        if test is None:
            sys.exit("Test unassigned")
        df = pd.DataFrame({'username': test})

        self.dftocsv(party + "/" + state + "/" + username + "/followers", df)

    def user_following(self, username, party, state):
        if not os.path.exists(party + "/" + state + "/" + username):
            os.makedirs(party + "/" + state + "/" + username)
        if os.path.isfile(party + "/" + state + "/" + username + "/following.csv"):
            return
        test = self.get_followings(username)
        if test is None:
            sys.exit("Test unassigned")
        df = pd.DataFrame({'username': test})
        self.dftocsv(party + "/" + state + "/" + username + "/following", df)

    def search_criteria(self, keywords):
        search = ""
        for i in keywords:
            search = search + i
            if keywords.index(i) != len(keywords) - 1:
                search = search + " OR "
        # print(search)
        return search

    def tweets_collector(self, u, search):
        tweets = []
        c = tw.Config()
        c.Username = u
        c.Search = search  # search for tweets containing any of the keywords
        c.Since = "2019-02-13"  # search during defined time period.
        c.Until = "2019-04-01"
        c.Store_object = True
        c.Store_object_tweets_list = tweets
        tw.run.Search(c)
        return tweets

    def get_retweeters_list(self, username, tweet_id):
        """
        Sourced from @x00x78's reply to https://github.com/twintproject/twint/issues/142
        """
        # get the data of retweets
        r = requests.get('https://twitter.com/i/activity/retweeted_popup?id=' + tweet_id)
        # use the grep in order to get the retweeters
        text = r.text
        x = re.findall(
            'div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"',
            text)
        return x

    def get_likers_list(self, username, tweet_id):
        """
        https://books.google.co.uk/books?id=dI1xDwAAQBAJ&pg=PA456&lpg=PA456&dq=https://twitter.com/i/activity/retweeted_popup?id%3D&source=bl&ots=uBkXREvol7&sig=ACfU3U3935syEn4PintKOzP8HnmZbpvBLA&hl=en&sa=X&ved=2ahUKEwjuwMGX6IPpAhXBrHEKHSI4C00Q6AEwAHoECAoQAQ#v=onepage&q=https%3A%2F%2Ftwitter.com%2Fi%2Factivity%2Fretweeted_popup%3Fid%3D&f=false
        """
        # get the data of retweets
        r = requests.get('https://twitter.com/i/activity/favorited_popup?id=' + tweet_id)
        # use the grep in order to get the retweeters
        text = r.text
        x = re.findall(
            'div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"',
            text)
        return x

    # def get_repliers_list(self, since, username,c_id):
    #     until = str(datetime.strptime(since, '%Y-%m-%d').date() + timedelta(days=2))
    #     c = tw.Config()
    #     c.Since = since
    #     c.Until = until
    #     c.Pandas = True
    #     c.To = "@"+username
    #     c.Hide_output = True
    #     tw.run.Search(c)
    #     df = tw.storage.panda.Tweets_df
    #
    #     repliers=[]
    #     for index, row in df.iterrows():
    #         if str(row['conversation_id']) == str(c_id):
    #             repliers.append(row['username'])
    #     return repliers

    def tweet_info(self, search, obj, connections):
        u_rt, u_like, u_ment = [],[],[]
        tweets = self.tweets_collector(obj[0], search)  # tweets in time period with keywords from source to target
        if len(tweets) > 0:
            retweeters, likers, mentions = [],[],[]
            for i in tweets:
                if int(i.retweets_count) > 0:
                    retweeters = self.get_retweeters_list(i.username, str(i.id))
                    r = list(retweeters)
                    for user in r:
                        if user.lower() not in connections:
                            retweeters.remove(user)
                if int(i.likes_count) > 0:
                    likers = self.get_likers_list(i.username, str(i.id))
                    l = list(likers)
                    for user in l:
                        if user.lower() not in connections:
                            likers.remove(user)

                mentions = i.mentions
                if len(mentions) > 0:
                    m = list(mentions)
                    for user in m:
                        if user.lower() not in connections:
                            mentions.remove(user)
                u_rt.extend(retweeters)
                u_like.extend(likers)
                u_ment.extend(mentions)
        return u_rt, u_like, u_ment

    def connection_to_list(self, df, source_user):
        connect_list = list(dict.fromkeys(list(df['Source']) + list(df['Target'])))
        connect_list.remove(source_user)
        return connect_list

    def tweet_info_storage(self, df, data, user, col1, col2):
        try:
            for u in data:  # problem here is for others_Tweets call, MEP appears on every row.
                indices = df.index[df['Source'] == u.lower()].tolist()
                indices.extend(df.index[df['Target'] == u.lower()].tolist())
                for i in indices:
                    if df.loc[i, "Source"] == user:
                        df.loc[i, col1] = int(df.loc[i, col1]) + 1
                    elif df.loc[i, "Target"] == user:
                        df.loc[i, col2] = int(df.loc[i, col2]) + 1
        except:
            pass
        return df

    def mep_tweets(self, search, obj):  # HOW OTHER USERS INTERACT WITH CONTENT PUBLISHED BY THE MEP
        # 1 - Tweets OUTWARD from MEP
        #       1.1 - to followers & friends
        #           a - liked by connections
        #           a - retweeted by connections
        #           a - that mention connections
        #       1.2 - to all others
        mep_connections = pd.read_csv(
            "/home/tcast/Documents/Final_project/Year-3-Final-Project/Twitter_scraping/" + obj[1] + "/" + obj[2] + "/" +
            obj[0] + ".csv", encoding='utf-8-sig')
        for idx, item in enumerate(["S_likes_T", "S_mentions_T", "S_rt_T", "T_likes_S", "T_mentions_S", "T_rt_S"]):
            try:
                mep_connections.insert(4 + idx, item, 0)
            except:
                print(item, "already exists")
        connect_list = self.connection_to_list(mep_connections, obj[0])
        u_rt, u_like, u_ment = self.tweet_info(search, obj, connect_list)
        print("retweets: ", u_rt)
        print("likers: ", u_like)
        print("mentions: ", u_ment)
        if len(u_rt) > 0 or len(u_like) > 0 or len(u_ment) > 0:
            mep_connections = self.tweet_info_storage(mep_connections, u_rt, obj[0], "T_rt_S", "S_rt_T")
            mep_connections = self.tweet_info_storage(mep_connections, u_like, obj[0], "T_likes_S", "S_likes_T")
            mep_connections = self.tweet_info_storage(mep_connections, u_ment, obj[0], "S_mentions_T", "T_mentions_S")
            self.dftocsv(
                "/home/tcast/Documents/Final_project/Year-3-Final-Project/Twitter_scraping/" + obj[1] + "/" + obj[
                    2] + "/" +
                obj[0], mep_connections)
        print("***")

    def others_tweets(self, search, obj):  # HOW THE MEP INTERACTS WITH CONTENT PUBLISHED BY OTHER USERS
        mep_connections = pd.read_csv(
            "/home/tcast/Documents/Final_project/Year-3-Final-Project/Twitter_scraping/" + obj[1] + "/" + obj[2] + "/" +
            obj[0] + ".csv", encoding='utf-8-sig')
        connect_list = self.connection_to_list(mep_connections, obj[0])
        for user in connect_list:
            if self.accountExists(user):
                print(user)
                u_rt, u_like, u_ment = self.tweet_info(search, [user], [obj[0]])
                print("retweets: ", u_rt)
                print("likers: ", u_like)
                print("mentions: ", u_ment)
                if len(u_rt) > 0 or len(u_like) > 0 or len(u_ment) > 0:
                    mep_connections = self.tweet_info_storage(mep_connections, u_rt, user, "T_rt_S", "S_rt_T")
                    mep_connections = self.tweet_info_storage(mep_connections, u_like, user, "T_likes_S", "S_likes_T")
                    mep_connections = self.tweet_info_storage(mep_connections, u_ment, user, "S_mentions_T",
                                                              "T_mentions_S")
                    self.dftocsv(
                        "/home/tcast/Documents/Final_project/Year-3-Final-Project/Twitter_scraping/" + obj[1] + "/" +
                        obj[
                            2] + "/" + obj[0], mep_connections)

        # tweets during time period
        # that contain keywords
        # that mention / are liked by / are retweeted by MEP
        # print("retweet: ", i.retweet)
        # - is this a retweet of a connection's tweet?
        # - reply to connection? (row["reply_to"])
        # 2 - Tweets INWARD to MEP
        #       1.1 - from followers & friends
        #           a - liked by MEP
        #           a - retweeted by MEP
        #           a - that mention MEP
        #       1.2 - from all others


if __name__ == "__main__":
    source_tags = ["copyright", "article13", "article17", "saveyourinternet", "article11", "uploadfilter",
                   "copyrightdirective", "artikel13", "yes2copyright", "art13", "fixcopyright", "mobgate",
                   "digitalsinglemarket", "artikel17", "article11", "artikel11", "savethelink", "urheberrecht"]

    # source_tags = ["copyright", "article13", "article17", "saveyourinternet", "article11", "uploadfilter",
    #                "copyrightdirective", "artikel13", "yes2copyright", "art13", "fixcopyright", "mobgate",
    #                "digitalsinglemarket", "artikel17", "article11", "artikel11", "savethelink", "urheberrecht",
    #                "urheberrechtsreform", "artikel13demo", "leistungsschutzrecht", "lsr", "savetheinternet",
    #                "art11", "gafa", "copyrightreform", "salvemosinternet", "berlingegen13", "wirsindkeinebots",
    #                "blackout21", "art13grafiken", "mob", "droitdauteur", "dirittodautore", "europeforcreators",
    #                "artikel15", "tekijänoikeusdirektiivi", "prawoautorskie", "creators", "dirittiautore",
    #                "deleteart13", "direttivacopyright", "directivedroitdauteur", "manifesto4copyright", "linktax",
    #                "artykul13", "artykuł13", "eplenary", "bots", "uploadfilters", "artigo13", "urheberechtsreform",
    #                "directivecopyright", "créateurs", "wirsindkeinebots", "artikla13", "freeinternet", "artikel12"]

    Scraper = TwintScraper()
    min_df = pd.read_csv(
        "/home/tcast/Documents/Final_project/Year-3-Final-Project" + "/20191110 - Key Rebels/output/minorities.csv",
        encoding='utf-8-sig')
    all_df = pd.read_csv(
        "/home/tcast/Documents/Final_project/Year-3-Final-Project" + "/20191110 - Key Rebels/data/dataset.csv",
        encoding='utf-8-sig')
    meps = all_df["Twitter"].dropna()
    keywords = Scraper.search_criteria(source_tags)

    # for index, row in min_df.loc[int(sys.argv[1]):int(sys.argv[2])].iterrows():
    # for index, row in min_df.iterrows():
    #     username = str(row["Twitter"]).lower()  # assigns and lowercases the handle of the MEP in current row
    #     group = row["Political_Group"]  # assigns the political group of the MEP in current row
    #     state = "minority"  # assigns default "state" of their vote
    #     if group == "ALDE":
    #         if Scraper.accountExists(username) and username in ["renateweber"]:
    #         # if group == "GUE-NGL" and username == "emmanuelmaurel":
    #             Scraper.mep_tweets(keywords, [username, group, state])
    #             #     # Scraper.mep_tweets(keywords, ["dantinicola", "S&D", "majority"])
    #             Scraper.others_tweets(keywords, [username, group, state])
    #         #     # Scraper.others_tweets(keywords, ["dantinicola", "S&D", "majority"])

    for index, row in all_df.iterrows():
        username = str(row["Twitter"]).lower()  # assigns and lowercases the handle of the MEP in current row
        group = row["Political_Group"]  # assigns the political group of the MEP in current row
        state = "majority"  # assigns default "state" of their vote
        if str(username).lower() in map(lambda x: x.lower(), min_df["Twitter"].dropna()):
            state = "minority"
        if group == "ALDE" and state == "majority":
            if Scraper.accountExists(username):
                Scraper.mep_tweets(keywords, [username, group, state])
                Scraper.others_tweets(keywords, [username, group, state])