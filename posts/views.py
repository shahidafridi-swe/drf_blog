from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly,IsAuthorUser,IsAdminUser

class PostList(APIView):
    permission_classes = [IsAuthenticated & IsAuthorUser | IsAdminUser]
    def get(self, request, format=None):
        print("inside get in posts")
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        print("inside post in posts")
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetail(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        print("inside get in post detail")
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request,pk, format=None):
        print("inside put in post detail")
        
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        print("inside delete in post detail")
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_200_OK)
        
        