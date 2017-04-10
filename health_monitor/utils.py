from django.utils import timezone


def init_dict(d, k):
    """Initializes k: {} entry in dict, d if not present."""
    if k not in d.keys():
        d[k] = {'score': None, 'updated': timezone.now()}
    return d
