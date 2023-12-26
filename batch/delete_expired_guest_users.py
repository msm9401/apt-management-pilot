from celery import shared_task

from django.core.management import call_command


@shared_task
def delete_expired_guest_users():
    """
    - 만료된 게스트 유저 삭제
    - python manage.py delete_expired_users
    """
    call_command("delete_expired_users")
