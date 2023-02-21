from django.shortcuts import render
from django.views import View

from conference_rooms_booking.models import ConferenceRoom


# Create your views here.

class AllRoomsView(View):

    def get(self, request):
        room = ConferenceRoom.objects.all().order_by('id')
        ctx = {'rooms': room}
        return render(request, "Main Page.html", ctx)


class RoomDetails(View):

    def get(self, request):
        pass

