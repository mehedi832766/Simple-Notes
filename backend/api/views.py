from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, filters
from . serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from .models import Note

# Create your views here.

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

class CreateNewUser(generics.CreateAPIView):
    #getting all the data to ensure not creating copy  user
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]

# class NoteListView(generics.ListAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title']

class SearchTitle(generics.ListAPIView):
    serializer_class = NoteSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        titleName = self.request.query_params.get('title')
        queryset = Note.objects.filter(author=user)
        queryset = queryset.filter(title = titleName)
        # if titleName is not None:

        return queryset