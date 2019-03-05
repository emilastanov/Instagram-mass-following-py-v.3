from IMF import IMF

user = IMF(
    "USERNAME",  # Input your instagram username
    "PASSWORD",  # Input your password
    delay=60     # Delay between of actions
)

while True:
    user.follow_to_follower_of_user_by_id(
        user.get_user_id_by_username(
            "USERNAME"  # Input your donor username. For example 'sayonaraboy'
        ),
        count=500       # Count of subs
    )

    user.unfollow_to_users_from_database()