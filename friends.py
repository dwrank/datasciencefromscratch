#!/usr/bin/env python

from __future__ import division
from pprint import pprint
from collections import Counter
from collections import defaultdict


users = [
    {'id': 0, 'name': 'Hero'},
    {'id': 1, 'name': 'Dunn'},
    {'id': 2, 'name': 'Sue'},
    {'id': 3, 'name': 'Chi'},
    {'id': 4, 'name': 'Thor'},
    {'id': 5, 'name': 'Clive'},
    {'id': 6, 'name': 'Hicks'},
    {'id': 7, 'name': 'Devin'},
    {'id': 8, 'name': 'Kate'},
    {'id': 9, 'name': 'Klein'}
]

friendships = [(0,1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# add a list of friends to the user
for user in users:
    user['friends'] = []

# populate the friends list
for (i, j) in friendships:
    users[i]['friends'].append(users[j])
    users[j]['friends'].append(users[i])

def number_of_friends(user):
    return len(user['friends'])

total_connections = sum(number_of_friends(user)
                        for user in users)
print('total_connections: %d' % total_connections)

num_users = len(users)
avg_connections = total_connections / num_users
print('avg_connections: %f' % avg_connections)

# create a list (user_id, number_of_friends)
num_friends_by_id = [(user['id'], number_of_friends(user))
                     for user in users]

num_friends_by_id = \
    sorted(num_friends_by_id,                               # sort
           key=lambda (user_id, num_friends): num_friends,  # by num_friends
           reverse=True)                                    # largest to smallest

print('num_friends_by_id:')
pprint(num_friends_by_id)

def friends_of_friends_ids_bad(user):
    '''returns foaf id list, but may contain duplicate ids'''
    return [foaf['id']
            for friend in user['friends']
            for foaf in friend['friends']]


def not_the_same(user, other_user):
    '''not the same if they have different ids'''
    return user['id'] != other_user['id']


def not_friends(user, other_user):
    '''other_user is not a friend of user if he's not in user's friends list'''
    return all(not_the_same(friend, other_user)
               for friend in user['friends'])

def friends_of_friends_ids(user):
    '''returns foaf id list'''
    return Counter(foaf['id']
                   for friend in user['friends']  # for each of user's friends
                   for foaf in friend['friends']  # count their friends
                   if not_the_same(user, foaf)    # who aren't user
                   and not_friends(user, foaf))   # and aren't user's friends


print('friends_of_friends_ids %s:' % str(users[3]['name']))
print(friends_of_friends_ids(users[3]))


interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]


def data_scientists_who_like(target_interest):
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]

# keys are interests, values are lists of user_ids with that interest
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# keys are user_ids, values are lists of interests for that user_id
interest_by_user_id = defaultdict(list)

for user_id, user_interest in interests:
    interest_by_user_id[user_id].append(user_interest)
    

def most_common_interests_with(user):
    Counter(interested_user_id
            for interest in interests_by_user_id[user['id']]  # for each of the user's interests
            for interested_user_id in user_ids_by_interest[interest]  # count user ids who share the interest
            if interested_user_id != user['id'])  # who is not the user


words_and_counts = Counter(word
                           for user_id, interest in interests
                           for word in interest.lower().split())

for word, count in words_and_counts.most_common():
    if count > 1:
        print word, count
