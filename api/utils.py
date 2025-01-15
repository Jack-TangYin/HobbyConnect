def get_similar_users(user):
    return CustomUser.objects.annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__in=user.hobbies.all()))
    ).exclude(id=user.id).order_by('-common_hobbies')

def paginate_users(request, user, users):
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

def filter_users_by_age(user, min_age, max_age):
    today = date.today()
    min_birth_date = today - relativedelta(years=min_age)
    max_birth_date = today - relativedelta(years=max_age)

    return CustomUser.objects.filter(
        hobbies__in=user.hobbies.all(),
        date_of_birth__range=(max_birth_date, min_birth_date)
    ).exclude(id=user.id).distinct()

def get_filtered_and_sorted_users(user, min_age, max_age):
    filtered_users = filter_users_by_age(user, min_age, max_age)
    return filtered_users.annotate(
        common_hobbies=Count('hobbies', filter=Q(hobbies__in=user.hobbies.all()))
    ).order_by('-common_hobbies')

