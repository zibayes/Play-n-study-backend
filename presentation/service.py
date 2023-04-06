from domain.User import User


def am_i_subscriber_of(sub_to: list[User], user: User) -> bool:
    am_i_sub = False
    for user_in_my_list in sub_to:
        if user_in_my_list.user_id == user.user_id:
            am_i_sub = True
    return am_i_sub
