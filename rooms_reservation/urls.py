#!/usr/bin/python3.7

from django.urls import path
from .views import RoomShow
from .views import RoomsAll
from .views import RoomDelete
from .views import RoomModify
from .views import RoomNew
from .views import RoomReserve
from .views import RoomSearch


urlpatterns = [
    path('room/new/', RoomNew.as_view(), name='new'),
    path('room/modify/<int:id>/', RoomModify.as_view(), name='modify'),
    path('room/delete/<int:id>/', RoomDelete.as_view(), name='delete'),
    path('room/<int:id>/', RoomShow.as_view(), name='room'),
    path('roomsall/', RoomsAll.as_view(), name='all'),
    path('reservation/<int:id>', RoomReserve.as_view(), name='reserve'),
    path('search/', RoomSearch.as_view(), name='search'),
]
