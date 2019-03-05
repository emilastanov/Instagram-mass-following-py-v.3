from InstagramAPI import InstagramAPI
from db import Database
from re import search, DOTALL
from datetime import datetime as time
from time import sleep
from json import loads


def writelog(msg):
    print('{} IMF >> {}'.format(
        time.now(),
        msg
    ))

class IMF:
    def __init__(self, username, password, delay=60):
        print('\n\t\tInstagram-mass-following-py-v.3\n')
        self.username = username
        self.delay = delay

        self.api = InstagramAPI(username, password)
        self.api.login()

        self.db = Database('IMF.db')

        self.db.create_table(
            username,
            id='INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
            users='varchar(100) NOT NULL UNIQUE'
        )

    def get_user_id_by_username(self,user_name):
        url_info = "https://www.instagram.com/%s/" % (user_name)
        info = self.api.s.get(url_info)

        json_info = loads(
            search(
                "window._sharedData = (.*?);</script>", info.text, DOTALL
            ).group(1)
        )

        id_user = json_info["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

        return id_user

    def get_real_followers_by_user_id(self, id):
        self.api.getUserFollowers(id)
        for user in self.api.LastJson['users']:
            print(user['pk'])
            break

    def isRealUser(self,id):
        dictinary = [
            'тренер',
            'маникюр',
            'стилист',
            'учитель',
            'магазин',
            'группа',
            'преколы',
            'мемы',
            'анекдоты',
            'коуч',
            'маркет',
            'trainer',
            'teacher',
            'shop',
            'market'
            'coach'
            'jokes',
        ]

        self.api.getUsernameInfo(id)
        info = self.api.LastJson['user']
        description = info['biography'].lower()

        for word in dictinary:
            if description.find(word) > 0:
                return False

        if int(info['media_count']) < 4:
            return False

        if int(info['following_count']) < 300:
            return True

        return False

    def unfollow_everybody(self):
        self.api.getSelfUsersFollowing()
        followings = self.api.LastJson['users']

        for following in followings:
            self.api.unfollow(following['pk'])
            writelog(
                'unfollowed to {}.'.format(following['username'])
            )
            sleep(self.delay)

    def follow_to_follower_of_user_by_id(self,id, count=500):
        following = 0
        next_token = ''

        while following < count:
            self.api.getUserFollowers(id, maxid=next_token)
            users = self.api.LastJson['users']
            next_token = self.api.LastJson['next_max_id']

            for user in users:
                if self.isRealUser(user['pk']):
                    self.api.follow(user['pk'])
                    writelog(
                        'followed to {}.'.format(user['username'])
                    )
                    following += 1
                    self.db.insert(
                        self.username,
                        users=user['pk']
                    )
                    sleep(self.delay)
                if following > count:
                    break

    def unfollow_to_users_from_database(self):
        users = self.db.select(
            self.username,
            'users'
        )
        if len(users) > 0:
            for user in users:
                self.api.unfollow(user[0])
                writelog(
                    'unfollowed to {}.'.format(user[0])
                )
                sleep(self.delay)
                self.db.delete(
                    self.username,
                    where='users=\'{}\''.format(user[0])
                )
        else:
            writelog('ERROR: Database is empty!')