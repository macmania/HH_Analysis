from nltk.corpus import wordnet as wn
import os
import httplib2
import atom
import io
from django.utils.encoding import smart_str, smart_unicode
import re

ID = 0
FROM_ID = 1
NAME = 2
GROUP_NAME = 4
MESSAGE = 5

def parse_csv():
    num_of_inconsistent = 0
    data = {}
    worksheet = open('HH_Data.csv')
    keys = worksheet.readline().split(',')

    data_inconsistent = {}

    #initializing what the keys look like
    #    data[key] = []

    for item in worksheet:
        data_str = item.split(',')

        if len(data_str) != len(keys):
            #print 'data', data_str
            #print len(data_str)
            data_str_inconsistent = data_str
            num_of_inconsistent += 1
            if len(data_str_inconsistent) < len(keys):
                for i in range(len(data_str_inconsistent)):
                    item_inconsistent = data_str_inconsistent[i]
                    #print item_inconsistent
                    key = keys[i]
                    if key in data_inconsistent.keys() and len(item_inconsistent) != 0:
                        data_inconsistent[key].append(item_inconsistent)
                    elif len(item_inconsistent) != 0:
                        data_inconsistent[key] = [item_inconsistent]
            elif len(data_str_inconsistent) > len(keys):
                for i in range(len(keys)):
                    key = keys[i]
                    item_inconsistent = data_str_inconsistent[i]
                    if key in data_inconsistent.keys() and len(item_inconsistent) != 0:
                        data_inconsistent[key].append(item_inconsistent)
                    elif len(item_inconsistent) != 0:
                        data_inconsistent[key] = [item_inconsistent]
        if len(data_str) == len(keys):
            for l in range(len(data_str)):
                item = data_str[l]
                key = keys[l]
                #print len(item)
                if key in data and len(item) != 0:
                    data[key].append(item)
                elif len(item) != 0:
                    data[key] = [item]

    output = open('output', 'w')
    #for key in data.keys():
        #print key, ': ', data[key][0]
        #print key, ': ', data[key]
        #output.write(key)
        #output.write(data[key])
    print num_of_inconsistent
    output.close()
    worksheet.close()
    all_data = {
        '# of inconsistent items': num_of_inconsistent,
        'good data': data,
        'shit data': data_inconsistent,
    }
    return all_data

'''
returns 2 dictionaries.
all_users_comments = {
        'user1': [all comments] ...
        'user2': [all comments] ...
    }
users_comments_by_group = {
    'user' :
        {
            'HH group 1': [ ... comments ... ]
        }
}
'''
def get_user_dict():
    all_users_data = {}
    user_comments_by_group = {}

    spreadsheet = open('HH_Data.csv')
    keys = spreadsheet.readline().split(',')

    for item in spreadsheet:
        data_str = item.split(',')

        if len(data_str) != len(keys) and len(data_str) >= 6:
            data_inconsistent = data_str
            name = data_inconsistent[NAME]
            message = data_inconsistent[MESSAGE]
            group = data_inconsistent[GROUP_NAME]
            if not has_numbers(name) and len(name.split(' ')) > 1 and len(message) > 1:
                if name in all_users_data.keys():
                    if (is_group(group)):
                        if group in user_comments_by_group[name].keys():
                            user_comments_by_group[name][group].append(message)
                        else:
                            user_comments_by_group[name][group] = [message]
                    all_users_data[name].append(message)
                else:
                    all_users_data[name] = [message]
                    if(is_group(group)):
                        user_comments_by_group[name] = {group:[message]}
                    else:
                        user_comments_by_group[name] = {}
        elif len(data_str) == len(keys):
            name = data_str[NAME]
            message = data_str[MESSAGE]
            group = data_str[GROUP_NAME]
            if len(message) > 1:
                if name in all_users_data.keys():
                    if (is_group(group)):
                        if group in user_comments_by_group[name].keys():
                            user_comments_by_group[name][group].append(message)
                        else:
                            user_comments_by_group[name][group] = [message]
                    all_users_data[name].append(message)
                else:
                    all_users_data[name] = [message]
                    if(is_group(group)):
                        user_comments_by_group[name] = {group:[message]}
                    else:
                        user_comments_by_group[name] = {}

    users_dictionary = {
        'user comments': all_users_data,
        'user comments by group': user_comments_by_group
    }

    spreadsheet.close()
    return users_dictionary

def is_group(input_string):
    return bool('Hackathon Hackers' in input_string or 'HH' in input_string)


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def main():
	#worksheet = open('HH_Data.csv')
    parse_csv()

if __name__ == '__main__':
	main()
