from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Comment
from .serializers import CommentDetailSerializer


class FeedComment(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, kapt_name, pk):
        comment = get_object_or_404(
            Comment.objects.select_related("user"),
            feed__house__kapt_name=kapt_name,
            pk=pk,
        )
        return comment

    # 특정 댓글 조회
    def get(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글에 대한 대댓글 추가
    def post(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)

        # 대댓글에는 댓글을 허용하지 않음
        # if comment.parent_comment:
        #    raise MethodNotAllowed(request.method)

        serializer = CommentDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400
        serializer.save(
            user=request.user,
            feed=comment.feed,
            parent_comment=comment,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 댓글 수정
    def put(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        if comment.user != request.user:
            raise PermissionDenied  # 403
        serializer = CommentDetailSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  # 400
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 삭제
    def delete(self, request, kapt_name, pk):
        comment = self.get_object(kapt_name, pk)
        if comment.user != request.user:
            raise PermissionDenied  # 403
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
