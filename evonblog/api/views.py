from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
import asyncio

from evonblog.models import User, Post, Comment

from .serializers import SaveUserSerializer, GetUserSerializer, CommentSerializer, PostSerializer
from .error_to_array import convertErrorToArray

jwt_secret_token = "evonblog_tokens"


@api_view(["GET"])
@csrf_exempt
def getPosts(request):
    posts = Post.objects.all()
    print(posts)

    serialized_posts = PostSerializer(posts, many=True)

    print(serialized_posts.data)

    return Response(serialized_posts.data)


@api_view(["POST"])
@csrf_exempt
def createPost(request):
    if request.method == "POST":
        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        userInfo = User.objects.get(id=decoded_token["id"])

        if not userInfo: 
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # END AUTHENTICATION 
        post = JSONParser().parse(request)
        post["author_id"] = userInfo.id
        post["author_username"] = userInfo.username
    
        # userInfo = User.objects.get(id=post["author_id"])

        # if userInfo is not None and userInfo.username == post["author_username"]:
        serialized_post = PostSerializer(data=post)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)

        serializer_error = serialized_post.errors
        error_array = convertErrorToArray(serializer_error)
        return Response({"error": error_array}, status=status.HTTP_400_BAD_REQUEST)

        # return Response("Forbidden User", status=status.HTTP_403_FORBIDDEN)

    return Response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
def editPost(request, pk):
    if request.method == "PUT":
        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')
        post_data = JSONParser().parse(request)

        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try: 
            userInfo = User.objects.get(id=decoded_token["id"])
        except User.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist: 
            return Response({"error": "This post no longer exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if userInfo.id != post.author_id:
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

        # UPDATE POST
        post_data["id"] = pk
        post_data["author_id"] = userInfo.id
        post_data["author_username"] = userInfo.username
        post_data["created_at"] = post.created_at
        post_data["comments"] = []

        serialized_post = PostSerializer(post, data=post_data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response({"message": "Updated post successfully"})
        
        errors = convertErrorToArray(serialized_post.errors)
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        
    return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["DELETE"])
def deletePost(request, pk):
    if request.method == "DELETE":
        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try: 
            userInfo = User.objects.get(id=decoded_token["id"])
        except User.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist: 
            return Response({"error": "This post no longer exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if userInfo.id != post.author_id:
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "Deleted post successfully"})
        

        
    return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
# @csrf_exempt
def getComments(request, pk):
    comments = Comment.objects.filter(Q(post_id = pk))
    serialized_comments = CommentSerializer(comments, many=True)
    print(serialized_comments.data)

    return Response(serialized_comments.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
def createComment(request):
    if request.method == "POST":

        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        userInfo = User.objects.get(id=decoded_token["id"])

        if not userInfo: 
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # END AUTHENTICATION 

        comment = JSONParser().parse(request)
        comment["author_username"] = userInfo.username
        comment["author_id"] = userInfo.id

        post = Post.objects.get(id=comment["post_id"])
      
        if (post is not None):
            serialized_comment = CommentSerializer(data=comment)
            if serialized_comment.is_valid():
                serialized_comment.save()
                return Response("Comment added successfully")       
        
            errors = convertErrorToArray(serialized_comment.errors)
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Post does not exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return Response({"message": "failed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
def editComment(request, pk):
    if request.method == "PUT":
        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')
        comment_data = JSONParser().parse(request)

        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try: 
            userInfo = User.objects.get(id=decoded_token["id"])
        except User.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist: 
            return Response({"error": "This comment no longer exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if userInfo.id != comment.author_id:
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)


        # UPDATE COMMENT
        comment_data["author_id"] = userInfo.id
        comment_data["author_username"] = userInfo.username
        comment_data["created"] = comment.created

        serialized_comment = CommentSerializer(comment, data=comment_data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response({"message": "Updated comment successfully"})
        
        errors = convertErrorToArray(serialized_comment.errors)
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        
    return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
def deleteComment(request, pk):
    if request.method == "DELETE":
        # AUTHENTICATION 
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        token = authorization_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        except ExpiredSignatureError:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try: 
            userInfo = User.objects.get(id=decoded_token["id"])
        except User.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist: 
            return Response({"error": "This comment no longer exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if userInfo.id != comment.author_id:
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)


        comment.delete()
        return Response({"message": "Deleted comment successfully"})
        
    return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@csrf_exempt
def getUsers(request):
    users = User.objects.all()
    user_serializer = GetUserSerializer(users, many=True)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
def createUser(request):
    if request.method == "POST":
        user_data = JSONParser().parse(request)
     
        if user_data["password"] is not None:
            hashed_password = make_password(user_data["password"])
            user_data["password"] = hashed_password
            
            serialized_user_data = SaveUserSerializer(data=user_data)
          

            if serialized_user_data.is_valid():
                serialized_user_data.save()

                # print(saved_data)
                return JsonResponse("User created successfully", safe=False)
        
        return JsonResponse("Invalid data provided", safe=False)
    
@api_view(["POST"])
def loginUser(request):    
    if request.method == "POST":
        request_body = JSONParser().parse(request)
        username = request_body["username"]
        password = request_body["password"]
        user = User.objects.get(username=username)
    
        if user is not None:
            is_password_okay = check_password(password, user.password)
            
            if is_password_okay:
               
                serialized_user = GetUserSerializer(user)
                data = {**serialized_user.data}

                now = datetime.utcnow()
                expires_at = now + timedelta(hours=1)
                payload = {
                    'id': data["id"],
                    'username': data["username"],
                    'exp': expires_at
                }
                jwt_token = jwt.encode(payload, jwt_secret_token, algorithm='HS256')

                print(jwt_token)
                data["token"] = jwt_token
                return Response(data, status=status.HTTP_200_OK)
        
            return Response({"error": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST)
          
            
        Response({"errorr":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
 
    return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
