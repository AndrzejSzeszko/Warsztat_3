from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.db.utils import IntegrityError
from rooms_reservation.models import Room
from rooms_reservation.models import Reservation
from datetime import datetime


class RoomNew(View):

    def get(self, request):
        return render(request, 'rooms_reservation/new.html', {})

    def post(self, request):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = True if request.POST.get('projector') == 'True' else False

        Room.objects.create(name=name,
                            capacity=capacity,
                            projector=projector,
                            )

        message = f'Room named {name} (capacity: {capacity}, projector: {projector}) successfully saved to database.'

        return render(request, 'rooms_reservation/new.html', {'message': message})


class RoomModify(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id) # todo czy tu nie powinno byc self.room?
        name = room.name
        capacity = room.capacity
        projector = room.projector
        return render(request, 'rooms_reservation/modify.html', {'id': id,
                                                                 'name': name,
                                                                 'capacity': capacity,
                                                                 'projector': projector,
                                                                 }
                      )

    def post(self, request, id):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = True if request.POST.get('projector') == 'True' else False
        Room.objects.filter(pk=id).update(name=name,
                                          capacity=capacity,
                                          projector=projector,
                                          )

        return redirect(reverse('room', kwargs={'id': id}))


class RoomDelete(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        name = room.name
        capacity = room.capacity
        projector = room.projector
        room.delete()
        message = f"""Room named {name} (capacity: {capacity}, projector: {projector}, ID: {id}) successfully deleted 
        from database."""

        return render(request, 'rooms_reservation/delete.html', {'message': message})


class RoomShow(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        name = room.name
        capacity = room.capacity
        projector = room.projector
        reservations = room.reservation_set.filter(date__gte=datetime.now().date()).order_by('date')

        return render(request, 'rooms_reservation/show.html', {'id': id,
                                                               'name': name,
                                                               'capacity': capacity,
                                                               'projector': projector,
                                                               'reservations': reservations,
                                                               }
                      )


class RoomsAll(View):

    def get(self, request):
        rooms = Room.objects.all().order_by('pk')
        today = datetime.now().date()
        return render(request, 'rooms_reservation/all.html', {'rooms': rooms,
                                                              'today': today
                                                              }
                      )


class RoomReserve(View):

    def get(self, request, id):
        min_date = datetime.now().date().strftime('%Y-%m-%d')
        room = Room.objects.get(pk=id)
        name = room.name
        capacity = room.capacity
        projector = room.projector
        reservations = room.reservation_set.filter(date__gte=datetime.now().date()).order_by('date')

        return render(request, 'rooms_reservation/reserve.html', {'id': id,
                                                                  'min_date': min_date,
                                                                  'name': name,
                                                                  'capacity': capacity,
                                                                  'projector': projector,
                                                                  'reservations': reservations,
                                                                  }
                      )

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        today = datetime.now().date()

        reservations = room.reservation_set.filter(date__gte=today).order_by('date')
        name = room.name
        capacity = room.capacity
        projector = room.projector
        commentary = request.POST.get('commentary')
        date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()

        try:
            assert date >= today
            Reservation.objects.create(room=room,
                                       date=date,
                                       commentary=commentary if commentary else None
                                       )

            message = f"""Room named {name} (capacity: {capacity}, projector: {projector}) successfully reserved for 
            {date}."""
        except IntegrityError:
            message = f'The room has been already reserved for {date}. Try another date or room.'
        except AssertionError:
            message = f'You cannot reserve room for past date.'

        return render(request, 'rooms_reservation/reserve.html', {'message': message,
                                                                  'id': id,
                                                                  'name': name,
                                                                  'capacity': capacity,
                                                                  'projector': projector,
                                                                  'reservations': reservations,
                                                                  }
                      )


class RoomSearch(View):

    def get(self, request):
        search_name = request.GET.get('search_name')
        search_capacity = request.GET.get('search_capacity')
        search_date = request.GET.get('search_date')
        search_projector = request.GET.get('search_projector')

        if search_projector == 'Yes':
            search_projector = True
        elif search_projector == 'No':
            search_projector = False
        else:
            search_projector = None

        rooms = Room.objects.search(name=search_name,
                                    capacity=search_capacity,
                                    projector=search_projector,
                                    date=search_date,
                                    )

        return render(request, 'rooms_reservation/search.html', {'rooms': rooms})
