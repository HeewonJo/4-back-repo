from django.shortcuts import render
from .models import Profile
from rest_framework import generics, status, viewsets
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, editPostSerialzier, UserClubSerializer, applyClubSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from news.permissions import IsManagerOrReadOnly
from news.models import News
from recruit.models import ClubRecruit, RecruitApply
from itertools import chain
from operator import attrgetter

# 회원가입 뷰
class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer

# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"message":"로그인 성공", "token":token.key}, status=status.HTTP_200_OK)

# 로그아웃 뷰
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

# 프로필 
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'student_id'

    def get_object(self):
        student_id = self.kwargs.get('student_id')
        return get_object_or_404(Profile, student_id=student_id)

# 수정 가능 게시글 조회
class editPostViewset(viewsets.ModelViewSet):
    permission_classes = [IsManagerOrReadOnly]
    serializer_class = editPostSerialzier
    lookup_field = 'student_id'

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        user = get_object_or_404(Profile, student_id=student_id)

        news = News.objects.filter(author=user)
        recruits = ClubRecruit.objects.filter(author=user)
        if not news.exists() and not recruits.exists():
            return Response(
            {"error": "관련 게시글이 존재하지 않습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
        combined_queryset = sorted(
            chain(news, recruits),
            key=attrgetter('created_at'),
            reverse=True  # 내림차순 정렬
        )
        return combined_queryset

    def list(self, request, student_id=None):
        queryset = self.get_queryset()
        if not queryset:
            return Response(
                {"error": "관련 게시글이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "수정 가능 게시글 조회에 성공하였습니다.", "result": serializer.data},
            status=status.HTTP_200_OK
        )

            
# 내가 속한 동아리
class UserClubsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserClubSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'student_id'

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response({"message": "소속 동아리 조회에 성공했습니다.", "result": serializer.data}, status=status.HTTP_200_OK)

# 지원 동아리 조회
class ApplyClubsView(generics.ListAPIView):
    serializer_class = applyClubSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'student_id'

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response({"message": "지원 동아리 조회에 성공했습니다.", "result": serializer.data}, status=status.HTTP_200_OK)