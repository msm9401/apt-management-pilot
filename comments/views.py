from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Comment
from .serializers import CommentDetailSerializer


class FeedComment(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    # 특정 댓글 조회
    def get(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        if comment.feed.house.kapt_name != kapt_name:
            raise ParseError("이 피드에 존재하지 않는 댓글입니다.")
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    # 댓글에 대한 대댓글 추가
    def post(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                feed=comment.feed,
                parent_comment=comment,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 수정
    def put(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        if comment.user != request.user:
            raise PermissionDenied
        serializer = CommentDetailSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        if comment.user != request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
