import collections
import heapq
import os

import pandas as pd
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


class dataAnalysis:

    def group_state_mep_count(self,group,state):
        if state == "minority":  # updates
            count = len(list(min_df.loc[min_df['Political_Group'] == group]["Twitter"].dropna()))  # used for avg
        else:
            max_df = pd.concat([min_df, all_df]).drop_duplicates(keep=False)
            count = len(list(max_df.loc[max_df['Political_Group'] == group]["Twitter"].dropna()))
        return count

    def csv_parser(self,path,column):
        cur_file = pd.read_csv(path, encoding='utf-8-sig')
        output_list = list(map(str.lower, filter((str(cur_file["Target"][0])).__ne__, cur_file[column].tolist())))
        return output_list

    # def connection_counter(self,connection_list,mep_count):
    #     count_dict = {k: v for k, v in sorted(dict(Counter(connection_list)).items(), key=lambda item: item[1], reverse=True)}
    #     avg_count_dict = count_dict.copy()
    #     avg_count_dict.update((x, y / mep_count) for x, y in count_dict.items())
    #
    #     return count_dict,avg_count_dict

    def connection_counter(self,connection_list):
        return {k: v for k, v in sorted(dict(Counter(connection_list)).items(), key=lambda item: item[1], reverse=True)}

    def most_connected_meps(self,num,group,state):

        directory = Path("../Twitter_scraping/" + group + "/" + state)

        file_names = (os.path.join(path, name) for path, _, filenames in os.walk(directory)
                      for name in filenames)

        big_files = list(heapq.nlargest(num, file_names, key=os.path.getsize))
        # print(list(directory.glob('**/*.csv')))
        paths = []
        [paths.append(Path(i)) for i in big_files]

        self.most_contacted_sum_meps(group,state,directory,paths)
        self.most_contacted_sum_others(group,state,directory,paths)

    def mainfunc(self,group,state):
        print("-----"+group.upper()+" "+state.upper()+"-----")
        dir_path = Path("../Twitter_scraping/" + group + "/" + state)
        # Analyser.most_contacted_outwards(group,state,dir_path)
        # Analyser.most_contacted_inwards(group,state,dir_path)
        # Analyser.most_contacted_sum_others(group,state,dir_path)
        # Analyser.most_contacted_sum_meps(group,state,dir_path)
        # Analyser.most_contacted_mirror(group,state,dir_path)
        # Analyser.MEP_to_other_ratio(group,state,dir_path)
        # Analyser.symmetric_ratio(group,state,dir_path)
        # Analyser.most_connected_meps(5, group, state)

    def most_contacted_inwards(self,group,state,p):
        group_source_list = []
        pathlist = p.glob('**/*.csv')
        num_group_meps = self.group_state_mep_count(group, state)

        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            group_source_list.extend(source_list)

        count_dict, avg_count_dict = self.connection_counter(group_source_list,num_group_meps)

        n = 15
        print("\n" + str(n), "accounts following", group, state,"the most")
        for x in list(count_dict)[0:n]:
            print("\t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))

    def most_contacted_outwards(self,group,state,p):
        group_target_list = []
        pathlist = p.glob('**/*.csv')
        num_group_meps = self.group_state_mep_count(group, state)

        for path in pathlist:
            target_list = self.csv_parser(path, "Target")
            group_target_list.extend(target_list)

        count_dict, avg_count_dict = self.connection_counter(group_target_list,num_group_meps)

        n = 15
        print("\n"+str(n), "most followed accounts by", group, state)
        for x in list(count_dict)[0:n]:
            print("\t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))

    def most_contacted_sum(self,group,state,p):
        group_connection_list = []
        num_group_meps = self.group_state_mep_count(group, state)
        pathlist = p.glob('**/*.csv')
        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            target_list = self.csv_parser(path, "Target")
            group_connection_list.extend(source_list)
            group_connection_list.extend(target_list)

        count_dict, avg_count_dict = self.connection_counter(group_connection_list,num_group_meps)
        n = 15
        print("\n"+str(n),"most connected accounts to",group,state)
        for x in list(count_dict)[0:n]:
            print("\t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))

    def most_contacted_sum_meps(self,group,state,p,user=None):
        group_connection_list = []
        pathlist = p.glob('**/*.csv')
        if user is not None:
            pathlist = user
        num_group_meps = self.group_state_mep_count(group,state)

        for path in pathlist:
            source_list = set(self.csv_parser(path,"Source")).intersection(list(map(str.lower,mep_handles)))
            target_list = set(self.csv_parser(path,"Target")).intersection(list(map(str.lower,mep_handles)))
            group_connection_list.extend(source_list)
            group_connection_list.extend(target_list)

        count_dict, avg_count_dict = self.connection_counter(group_connection_list,num_group_meps)

        n = 20
        if user is not None:
            print(" "+str(n), "most connected MEP accounts to", group,state,len(user), "most connected MEPs")
        else:
            print(" \t\t"+str(n),"most connected MEP accounts to",group,state)
        for x in list(count_dict)[0:n]:
            g = all_df.loc[all_df['Twitter'] == x]['Political_Group'].iloc[0]
            s = "majority"
            if x in min_df['Twitter']:
                s = "minority"
            print(" \t {} ({} {}) : tot. {} connections\t (avg. {})".format(x, g, s, count_dict[x],avg_count_dict[x]))

    def most_contacted_sum_others(self,group,state,p,user=None):
        group_connection_list = []
        pathlist = p.glob('**/*.csv')
        if user is not None:
            pathlist = user
        num_group_meps = self.group_state_mep_count(group,state)

        for path in pathlist:
            source_list = set(self.csv_parser(path,"Source")).difference(list(map(str.lower,mep_handles)))
            target_list = set(self.csv_parser(path,"Target")).difference(list(map(str.lower,mep_handles)))
            group_connection_list.extend(source_list)
            group_connection_list.extend(target_list)

        count_dict, avg_count_dict = self.connection_counter(group_connection_list,num_group_meps)

        n = 20
        if user is not None:
            print(" "+str(n), "most connected non-MEP accounts to", group,state,len(user), "most connected MEPs")
            for x in list(count_dict)[0:n]:
                print(" \t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))
        else :
            print(" \t\t"+str(n),"most connected non-MEP accounts to",group,state)
            for x in list(count_dict)[0:n]:
                print(" \t\t\t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))

    def most_contacted_mirror(self,group,state,p):
        group_connection_list = []
        pathlist = p.glob('**/*.csv')
        num_group_meps = self.group_state_mep_count(group,state)
        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            target_list = self.csv_parser(path, "Target")
            a = set(source_list).intersection(target_list)
            group_connection_list.extend(a)

        count_dict, avg_count_dict = self.connection_counter(group_connection_list,num_group_meps)

        n = 15
        print("\n" + str(n), "most symmetricly connected accounts with", group, state)
        for x in list(count_dict)[0:n]:
            print("\t {} : tot. {} connections\t (avg. {})".format(x, count_dict[x], avg_count_dict[x]))

    def MEP_to_other_ratio(self,group,state,p):
        group_connection_list = []
        pathlist = p.glob('**/*.csv')
        num_group_meps = self.group_state_mep_count(group,state)
        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            target_list = self.csv_parser(path, "Target")
            group_connection_list.extend(source_list + target_list)

        a = set(group_connection_list).intersection(mep_handles)
        b = set(group_connection_list).difference(mep_handles)

        print("\n",group,state+"'s MEP to third-party comparison")
        print("\t",len(a),"connections with MEPs (avg.",len(a)/num_group_meps,")")
        self.group_to_other_ratio(group,p)
        print("\t",len(b),"connections with non-MEPs (avg.",len(b)/num_group_meps,")")
        self.most_contacted_sum_others(group, state,p)

    def group_to_other_ratio(self,group,p):
        group_df = all_df.loc[all_df['Political_Group'] == group]
        group_handles = list(group_df["Twitter"].dropna())
        non_group_handles = set(mep_handles).difference(group_handles)
        pathlist = p.glob('**/*.csv')
        group_connection_list = []
        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            target_list = self.csv_parser(path, "Target")
            group_connection_list.extend(list(source_list) + list(target_list))

        a = set(group_connection_list).intersection(group_handles) #same-group connections
        groups = []

        for i in set(group_connection_list).intersection(non_group_handles): #other-group connections:
            user_df = all_df.loc[all_df['Twitter'] == i]
            s = user_df['Political_Group'].iloc[0]
            if i in list(map(str.lower,list(min_df['Twitter'].dropna()))):
                s += " minority"
            else:
                s += " majority"
            groups.append(s)
        b = {k: v for k, v in sorted(dict(Counter(groups)).items(), key=lambda item: item[1], reverse=True)}

        print("\t\t", len(a), "connections with", group)
        print("\t\t",sum(b.values()),"connections with other groups : ", b)

    def symmetric_ratio(self,group,state,p):
        pathlist = p.glob('**/*.csv')
        num_group_meps = self.group_state_mep_count(group,state)
        mirror_count = 0
        total_count = 0
        for path in pathlist:
            source_list = self.csv_parser(path, "Source")
            target_list = self.csv_parser(path, "Target")
            a = set(source_list).intersection(target_list)
            total_count += len(source_list) + len(target_list)
            mirror_count += len(a)

        print("\n Symmetricly connected accounts with", group, state)
        print("\t tot. {} symmetric connections\t (avg. {})".format(mirror_count, mirror_count/num_group_meps))
        print("\t tot. {} total connections\t (avg. {})".format(total_count, total_count/num_group_meps))



    # Opinion-based analyses
    def avg_out_degrees_opinions(self, pos, neg):
        out_degrees = []
        for i in range(len(pos)):
            tmp = [0, 0]  # for against
            for j, k in enumerate([pos[i], neg[i]]):
                num_meps = self.group_state_mep_count(k[0], k[1])
                pathlist = Path("../Twitter_scraping/" + k[0] + "/" + k[1]).glob('**/*.csv')
                for path in pathlist:
                    target_list = set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))
                    tmp[j] += len(target_list)
                tmp[j] = tmp[j] / num_meps
            out_degrees.append(tmp)

        self.mpl_two_barh("Average MEP out-degree by opinion", "", ep_groups, [round(item[0], 1) for item in out_degrees],
                          [round(item[1], 1) for item in out_degrees], " YES", " NO", True)
        return out_degrees
    # EP-wide OPINION-BASED comparison
        # to what accounts they are the most connected to based on opinion
        # stuff that differs from the intersection on both sides (out-degree)
    def opinion_based_helper(self, s, ep):
        opinion_target_list = []
        for i in s:
            pathlist = Path("../Twitter_scraping/" + i[0] + "/" + i[1]).glob('**/*.csv')
            for path in pathlist:
                if ep:
                    target_list = set(self.csv_parser(path, "Target")).intersection(
                        list(map(str.lower, mep_handles)))
                else:
                    target_list = (set(self.csv_parser(path, "Target")).difference(
                        list(map(str.lower, mep_handles)))).difference(filter_by)
                opinion_target_list.extend(target_list)
        return opinion_target_list
    def opinion_based(self, pos,neg,ep = False):
        # just out-degree now-+
        pos_list = self.opinion_based_helper(pos,ep)
        neg_list = self.opinion_based_helper(neg,ep)
        pos_count_dict = self.connection_counter(pos_list)
        neg_count_dict = self.connection_counter(neg_list)
        pos_dif = set(pos_list).difference(set(neg_list))
        neg_dif = set(neg_list).difference(set(pos_list))
        pos_out, neg_out = {}, {}
        for elem in pos_dif:
            try:
                pos_out[elem] = pos_count_dict.get(elem)
            except:
                pass
        for elem in neg_dif:
            try:
                neg_out[elem] = neg_count_dict.get(elem)
            except:
                pass


        test_pos = {k: v for k, v in sorted(pos_out.items(), key=lambda item: item[1], reverse=True)}
        test_neg = {k: v for k, v in sorted(neg_out.items(), key=lambda item: item[1], reverse=True)}
        n=15
        self.mpl_one_barh("Top "+str(n)+" outwards connections of the YES vote", "YES", "", list(test_pos.keys())[0:n], test_pos)
        self.mpl_one_barh("Top "+str(n)+" outwards connections of the NO vote", "NO", "", list(test_neg.keys())[0:n], test_neg)


    # IN-PARTY state network graph comparison
        # out-degree vis for Parties defending the press should be more connected to media & journalist accounts
    def party_outdegree(self,group):
        # ep = False
        conn_list = []
        for i,state in enumerate(["majority","minority"]): # remove i if not used
            group_target_list = []
            pathlist = Path("../Twitter_scraping/" + group + "/" + state).glob('**/*.csv')
            for path in pathlist:
                target_list = (set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))).difference(filter_by)
                group_target_list.extend(target_list)
            conn_list.append(group_target_list)

        maj_count = self.connection_counter(conn_list[0])
        min_count = self.connection_counter(conn_list[1])
        maj_dif = set(conn_list[0]).difference(set(conn_list[1]))
        min_dif = set(conn_list[1]).difference(set(conn_list[0]))
        intersect = set(conn_list[0]).intersection(set(conn_list[1]))
        maj_out, min_out, intsct, maj_int, min_int = {}, {}, {}, {}, {}
        for elem in maj_dif:
            try:
                maj_out[elem] = maj_count.get(elem)
            except:
                pass
        for elem in min_dif:
            try:
                min_out[elem] = min_count.get(elem)
            except:
                pass
        num_meps = [self.group_state_mep_count(group, "majority"),self.group_state_mep_count(group, "minority")]
        for elem in intersect:
            try:
                maj_int[elem] = maj_count.get(elem)/num_meps[0]
                min_int[elem] = min_count.get(elem)/num_meps[1]
                intsct[elem] = maj_count.get(elem) + min_count.get(elem)
            except:
                pass

        test_maj = {k: v for k, v in sorted(maj_out.items(), key=lambda item: item[1], reverse=True)}
        test_min = {k: v for k, v in sorted(min_out.items(), key=lambda item: item[1], reverse=True)}
        test_intsct = {k: v for k, v in sorted(intsct.items(), key=lambda item: item[1], reverse=True)}
        test_maj_i = {k: v for k, v in sorted(maj_int.items(), key=lambda item: item[1], reverse=True)}
        test_min_i = {k: v for k, v in sorted(min_int.items(), key=lambda item: item[1], reverse=True)}
        n = 15
        self.mpl_two_barh("Average highest-degree extra-EP follows from "+group,group,list(test_intsct.keys())[0:n], test_maj_i, test_min_i)


        self.mpl_one_barh("Highest-degree extra-EP follows only from "+group+" majority",group,"majority",list(test_maj.keys())[0:n], test_maj)
        self.mpl_one_barh("Highest-degree extra-EP follows only from "+group+" minority",group,"minority",list(test_min.keys())[0:n], test_min)

    # State-based analyses

        # PARTY-STATE average out-degrees (& to non-EP)
        # check if minorities are more connected on average
        # ie minorities think for themselves instead of "mindlessly" following the group (less ostensible)
    def avg_out_degrees(self, groups):
        out_degrees = []
        for i, j in enumerate(groups):
            tmp = [0, 0]
            for k, l in enumerate(["majority", "minority"]):
                num_meps = self.group_state_mep_count(j, l)
                pathlist = Path("../Twitter_scraping/" + j + "/" + l).glob('**/*.csv')
                for path in pathlist:
                    target_list = set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))
                    tmp[k] += len(target_list)
                tmp[k] = tmp[k] / num_meps
            out_degrees.append(tmp)
        self.mpl_two_barh("Average MEP out-degree", "", ep_groups, [round(item[0], 1) for item in out_degrees],
                         [round(item[1], 1) for item in out_degrees])
        return out_degrees

        # EP-wide state comparison
        # to what accounts they are the most connected to based on state
    def state_based_helper(self,groups,state):
        state_target_list = []
        for i in groups:
            pathlist = Path("../Twitter_scraping/" + i + "/" + state).glob('**/*.csv')
            for path in pathlist:
                target_list = (set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))).difference(filter_by)
                state_target_list.extend(target_list)
        return state_target_list
    def state_based(self,groups):
        # just out-degree now-+
        minority_list = self.state_based_helper(groups,"minority")
        majority_list = self.state_based_helper(groups,"majority")
        min_count = self.connection_counter(minority_list)
        maj_count = self.connection_counter(majority_list)
        min_dif = set(minority_list).difference(set(majority_list))
        maj_dif = set(majority_list).difference(set(minority_list))
        intersect = set(minority_list).intersection(set(majority_list))
        min_out, maj_out, inter_out = {}, {}, {}
        for elem in min_dif:
            try:
                min_out[elem] = min_count.get(elem)
            except:
                pass
        for elem in maj_dif:
            try:
                maj_out[elem] = maj_count.get(elem)
            except:
                pass
        for elem in intersect:
            try:
                inter_out[elem] = min_count.get(elem)+maj_count.get(elem)
            except:
                pass


        test_min = {k: v for k, v in sorted(min_out.items(), key=lambda item: item[1], reverse=True)}
        test_maj = {k: v for k, v in sorted(maj_out.items(), key=lambda item: item[1], reverse=True)}
        test_int = {k: v for k, v in sorted(inter_out.items(), key=lambda item: item[1], reverse=True)}
        n=15
        self.mpl_one_barh("Top "+str(n)+" outwards connections of 'rebel' MEPs", "minority", "", list(test_min.keys())[0:n], test_min)
        self.mpl_one_barh("Top "+str(n)+" outwards connections of 'loyal' MEPs", "majority", "", list(test_maj.keys())[0:n], test_maj)

    # Take top 25 EP connections and see how each Party-state is connected to them.
    def ep_most_followed(self,groups,n):
        # don't include the eu institution and eu official accounts because following them has no concrete meaning
        ep_out_connections = []
        for i in groups:
            for j in ["majority","minority"]:
                pathlist = Path("../Twitter_scraping/" + i + "/" + j).glob('**/*.csv')
                for path in pathlist:
                    ep_out_connections.extend((set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))).difference(filter_by))
        ep_count = self.connection_counter(ep_out_connections)
        return list(ep_count)[0:n]
    def most_followed_per_group(self,group):
        out_degrees = []
        n = 15
        most_followed = self.ep_most_followed(ep_groups,n)
        for state in ["majority","minority"]:
            out_connections = []
            pathlist = Path("../Twitter_scraping/" + group + "/" + state).glob('**/*.csv')
            for path in pathlist:
                out_connections.extend((set(self.csv_parser(path, "Target")).difference(list(map(str.lower, mep_handles)))).intersection(most_followed))
            out_degrees.append(self.connection_counter(out_connections))
        print(out_degrees)
        maj_counts, min_counts = {}, {}
        for elem in most_followed:
            maj_counts[elem] = out_degrees[0].get(elem)/self.group_state_mep_count(group, "majority")
            try:
                min_counts[elem] = out_degrees[1].get(elem)/self.group_state_mep_count(group, "minority")
            except:
                if out_degrees[1].get(elem) == None:
                    min_counts[elem] = 0.0

        print(maj_counts)
        print(min_counts)

        self.mpl_two_barh("Average number of connections from "+group+"to accounts most followed by entire EP", group,most_followed, maj_counts, min_counts)




    def mpl_two_barh(self,title,group,usernames,sb1,sb2,lab1=' majority',lab2=' minority', v = False):
        val1, val2 = [], []
        try:
            for i in usernames:
                val1.append(sb1.get(i))
                val2.append(sb2.get(i))
        except:
            val1 = sb1
            val2 = sb2

        plt.rcdefaults()
        fig, ax = plt.subplots()

        x = np.arange(len(usernames))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        if v:
            rects1 = ax.barh(x - width / 2, val1, width, label=group+lab1,color="#00CB07")
            rects2 = ax.barh(x + width / 2, val2, width, label=group+lab2,color="#FF1900")
        else:
            rects1 = ax.barh(x - width / 2, val1, width, label=group+lab1)
            rects2 = ax.barh(x + width / 2, val2, width, label=group+lab2)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Connections')
        ax.set_title(title)
        ax.set_yticks(x)
        ax.set_yticklabels(usernames)
        ax.invert_yaxis()
        ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                x_val = rect.get_width()
                y_val = rect.get_y() + rect.get_height() / 2
                space = 5
                ha = 'left'
                label = "{:.1f}".format(x_val)
                ax.annotate(
                    label,
                    (x_val,y_val),
                    xytext=(space, 0),
                    textcoords="offset points",
                    va='center',
                    ha=ha)

        autolabel(rects1)
        autolabel(rects2)
        # fig.set_size_inches(18.5, 10.5)
        fig.set_size_inches(10.5, 5.95)
        plt.savefig(title + "out.png")
        plt.show()

    def mpl_one_barh(self,title,group,state,usernames,sb1):
        val1 = []
        usernames.reverse()
        for i in usernames:
            val1.append(sb1.get(i))

        x = np.arange(len(usernames))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.barh(x - width / 2, val1, width, label=group+" "+state)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Connections')
        ax.set_title(title)
        ax.set_yticks(x)
        ax.set_yticklabels(usernames)
        ax.legend()

        for rect in rects1:
            x_val = rect.get_width()
            y_val = rect.get_y() + rect.get_height() / 2
            space = 5
            ha = 'left'
            label = "{:.1f}".format(x_val)
            ax.annotate(
                label,
                (x_val, y_val),
                xytext=(space, 0),
                textcoords="offset points",
                va='center',
                ha=ha)

        # fig.set_size_inches(18.5, 10.5)
        fig.set_size_inches(10.5, 5.95)
        plt.savefig(title + "out.png")
        plt.show()






if __name__ == "__main__":
    Analyser = dataAnalysis()
    ep_groups = ["ALDE", "ECR", "EFDD", "ENF", "EPP", "Greens-EFA", "GUE-NGL", "S&D"]
    in_favour = [["ALDE","majority"],["ECR","minority"], ["EFDD","minority"], ["ENF","majority"], ["EPP","majority"],
                 ["Greens-EFA","minority"],["GUE-NGL", "minority"],["S&D", "majority"]]
    not_in_favour = [["ALDE","minority"],["ECR","majority"], ["EFDD","majority"], ["ENF","minority"],
                     ["EPP","minority"], ["Greens-EFA","majority"],["GUE-NGL", "majority"],["S&D", "minority"]]
    filter_by = ["jduch", "mac_europa", "alexstubb", "paulruebig", "coe","lgbtiintergroup","cjbxl","lelylada","equo","efsse_","iueuropa","gdelboscorfield","ajbxl","agnesevren","ylvajohansson","tomastobe","richardgcorbett","pe_france","desarnez","euerasmusplus","andrewduffeu","ansip_eu","aldeparty","giannipittella", "eu_eurostat", "euombudsman", "verajourova", "corinacretueu", "euinmyregion",
                 "vestager", "pes_pse", "europarl_photo", "marossefcovic", "philhoganeu", "mariannethyssen",
                 "europarlav", "martinselmayr", "jhahneu", "pierremoscovici", "ep_thinktank", "goettingereu",
                 "michelbarnier", "jyrkikatainen", "reneweurope", "eu_commission", "junckereu", "europarl_en",
                 "eucopresident", "eucouncil", "timmermanseu", "ep_president", "malmstromeu", "martinschulz",
                 "europarlpress", "eucouncilpress", "federicamog", "parlimag", "eu_eeas", "europarl_video",
                 "ep_presschulz", "eppgroup", "epp", "theprogressives", "josephdaul", "gabrielmariya", "jmdbarroso",
                 "vdombrovskis", "moedas", "donaldtusk", "greensefa", "foodreveu", "erikmarquardt","gruene_europa", "monicafrassoni", "ruthreichstein", "europeangreens", "jeanlambertldn", "jensmestereu","epculture", "fracapoluongo", "greens_climate", "fyeg","avramopoulos", "vonderleyen", "tnavracsicseu", "euenvironment", "mepassistants","eu_ttip_team"]
    min_df = pd.read_csv("../20191110 - Key Rebels/output/minorities.csv", encoding='utf-8-sig')
    all_df = pd.read_csv("../20191110 - Key Rebels/data/dataset.csv", encoding='utf-8-sig')
    mep_handles = list(all_df["Twitter"].dropna())

    # Analyser.avg_out_degrees_opinions(in_favour,not_in_favour)
    # Analyser.opinion_based(in_favour,not_in_favour,False)
    # Analyser.party_outdegree("EPP")
    # Analyser.party_outdegree("Greens-EFA")
        # first one needs averages
    # Analyser.most_followed_per_group("EPP")
    # Analyser.most_followed_per_group("Greens-EFA")
    # print(Analyser.avg_out_degrees(ep_groups))
    # Analyser.state_based(ep_groups)

        # needs averages
