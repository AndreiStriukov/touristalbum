from django.db.models import Q


def q_search(query):
    keywords = [word for word in query.split(' ') if len(word) > 2]
    q_objects = Q()
    for token in keywords:
        q_objects |= Q(j_place__icontains=query)

    return q_objects


def album_filters(self):
    years = self.request.GET.getlist('year', None)
    participants = self.request.GET.getlist('participants')
    types = self.request.GET.getlist('type')
    place = self.request.GET.get('place')

    filters = Q(a_is_active=True)
    if years:
        filters &= Q(j_year__in=years)
    if participants:
        filters &= Q(travel_participants__in=participants)
    if types:
        filters &= Q(j_type__in=types)
    if place:
        filters &= q_search(place)

    return filters
