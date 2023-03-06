import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import pytz
from django.views import View
from conference_rooms_booking.models import ConferenceRoom, BookingDetails
from django.db import models

# Create your views here.
from django.shortcuts import render
from .models import ConferenceRoom, BookingDetails


def search(request):
    query = request.GET.get('q')

    rooms = ConferenceRoom.objects.filter(
        models.Q(name__icontains=query) |
        models.Q(capacity__icontains=query) |
        models.Q(projector_availability__icontains=query)
    )

    bookings = BookingDetails.objects.filter(
        models.Q(comment__icontains=query) |
        models.Q(room_id__name__icontains=query)
    )

    context = {
        'rooms': rooms,
        'bookings': bookings,
    }

    return render(request, 'Main Page.html', context)


class AllRoomsView(View):

    def get(self, request):
        rooms = ConferenceRoom.objects.all().order_by('id')
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.bookingdetails_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        ctx = {"rooms": rooms}
        return render(request, "Main Page.html", ctx)



class RoomDetails(View):

    def get(self, request, id):

        room = get_object_or_404(ConferenceRoom, id=id)
        yes = 'Yes' if room.projector_availability else 'No'
        reservations = room.bookingdetails_set.filter(date__gte=datetime.date.today()).order_by('date')
        ctx = {'room': room, 'yes': yes, "reservations": reservations}
        return render(request, 'Room Details.html', ctx)


class NewRoom(View):

    def get(self, request):
        return render(request, "Add Room.html")

    def post(self, request):
        name = request.POST.get("name")
        capacity = int(request.POST.get("capacity"))
        projector = request.POST.get("projector") == "on"
        if int(capacity) <= 0:
            ctx = {"message": "Capacity can't be smaller than 1!"}
            return render(request, "Add Room.html", ctx)
        elif ConferenceRoom.objects.filter(name=name).exists():
            ctx = {"message": "This name already exists!"}
            return render(request, "Add Room.html", ctx)
        elif not name:
            ctx = {"message": "Room name can't be empty"}
            return render(request, "Add Room.html", ctx)
        else:

            ConferenceRoom.objects.create(
                name=name,
                capacity=capacity,
                projector_availability=projector
            )

            return redirect("/all-rooms")


class DeleteRoom(View):

    def get(self, request, id):

        delete_room = get_object_or_404(ConferenceRoom, pk=id)
        delete_room.delete()

        return redirect('/all-rooms')


class EditRoom(View):

    def get(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        ctx = {'rooms': room}
        return render(request, "Edit Room.html", ctx)

    def post(self, request, id):
        def post(self, request):
            name = request.POST.get("name")
            capacity = int(request.POST.get("capacity"))
            projector = request.POST.get("projector") == "on"
            if int(capacity) <= 0:
                ctx = {"message": "Capacity can't be smaller than 1!"}
                return render(request, "Add Room.html", ctx)
            elif ConferenceRoom.objects.filter(name=name).exists():
                ctx = {"message": "This name already exists!"}
                return render(request, "Add Room.html", ctx)
            elif not name:
                ctx = {"message": "Room name can't be empty"}
                return render(request, "Add Room.html", ctx)
            else:

                ConferenceRoom.name = name
                ConferenceRoom.capacity = capacity
                ConferenceRoom.projector_availability = projector
                ConferenceRoom.save()
                return redirect("/all-rooms")


class BookRoom(View):

    def get(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        reservations = room.bookingdetails_set.filter(date__gte=datetime.date.today()).order_by('date')
        ctx = {'room': room, "reservations": reservations}
        return render(request, "Book Room.html", ctx)

    def post(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        date = request.POST.get("date")
        comment = request.POST.get("comment")

        if BookingDetails.objects.filter(room_id=room, date=date):
            ctx = {"rooms": room, "message": "This room is already booked!"}
            return render(request, "Book Room.html", ctx)
        elif date < str(datetime.date.today()):
            ctx = {"rooms": room, "message": "Date cannot be from the past!"}
            return render(request, "Book Room.html", ctx)

        else:
            BookingDetails.objects.create(room_id=room, date=date, comment=comment)
            return redirect("/all-rooms")


