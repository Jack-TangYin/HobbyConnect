from typing import List, Dict
from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Count, Q
from datetime import date

from api.models import CustomUser


def filter_users_by_age(user: CustomUser, min_age: int, max_age: int) -> QuerySet[CustomUser]:
    """
    Return all users (excluding current user) whose age is in [min_age, max_age].
    
    If min_age=10 and max_age=20, we want DOB between:
      [today - 20 years, today - 10 years].
    """
    today: date = date.today()

    # Earliest birthdate for a user to still be within max_age
    earliest_birthdate: date = today - relativedelta(years=max_age)

    # Latest birthdate for a user to still be within min_age
    latest_birthdate: date = today - relativedelta(years=min_age)

    return (
        CustomUser.objects
                  .filter(
                      date_of_birth__range=(earliest_birthdate, latest_birthdate),
                      hobbies__in=user.hobbies.all()
                  )
                  .exclude(id=user.id)
                  .distinct()
    )


def get_filtered_and_sorted_users(user: CustomUser, min_age: int, max_age: int) -> QuerySet[CustomUser]:
    """
    Filter users by [min_age, max_age], then annotate each user
    with the count of hobbies in common, sorting descending by that count.
    """
    filtered_users: QuerySet[CustomUser] = filter_users_by_age(user, min_age, max_age)
    return filtered_users.annotate(
        common_hobbies=Count(
            'hobbies',
            filter=Q(hobbies__in=user.hobbies.all()),
            distinct=True
        )
    ).order_by('-common_hobbies')


def flatten_errors(errors: Dict[str, List[str]]) -> str:
    """
    Convert a Django form errors dictionary into a single string.
    """
    messages: List[str] = []
    for field, error_list in errors.items():
        if isinstance(error_list, list):
            messages.extend(error_list)
        else:
            messages.append(str(error_list))
    return " ".join(messages)
