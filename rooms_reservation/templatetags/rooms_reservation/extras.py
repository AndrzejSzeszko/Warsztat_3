#!/usr/bin/python3.7

from django import template
from datetime import datetime

register = template.Library()


def reservation_status_for_today(room):
    today = datetime.now().date()
    return 'reserved' if room.reservation_set.filter(date=today).first() else 'available'


register.filter('reservation_status_for_today', reservation_status_for_today)
