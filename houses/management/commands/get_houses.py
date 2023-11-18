from django.core.management.base import BaseCommand
from houses.models import Apartment
from houses.api import apt_list


class Command(BaseCommand):
    help = "This command saves Apartment"

    """
    대구:27, 인천:28, 광주:29, 대전:30, 울산:31, 경기:41, 강원:42
    충북:43, 충남:44, 전북:45, 전남:46, 경북:47, 경남:48, 제주:50  
    apt_list()에 필요한 지역 코드 대입

    실행 : python manage.py get_houses
    """

    def handle(self, *args, **options):
        # 임시로 경기도 아파트만 저장
        code = 41

        apt_data = apt_list(code)

        for a in apt_data:
            try:
                Apartment(
                    address_do=a["as1"],
                    address_si=a["as2"],
                    address_dong=a["as3"],
                    address_li=a["as4"],
                    bjd_code=a["bjdCode"],
                    kapt_code=a["kaptCode"],
                    kapt_name=a["kaptName"],
                ).save()
            except KeyError:
                Apartment(
                    address_do=a["as1"],
                    address_si=a["as2"],
                    address_dong=a["as3"],
                    bjd_code=a["bjdCode"],
                    kapt_code=a["kaptCode"],
                    kapt_name=a["kaptName"],
                ).save()

        self.stdout.write(self.style.SUCCESS("Houses Saved!"))
