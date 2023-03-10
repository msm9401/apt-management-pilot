from django.core.management.base import BaseCommand
from houses.models import Apartment
from houses.api import apt_list


class Command(BaseCommand):

    help = "This command saves Apartment"

    """
    대구:27[0], 인천:28[0], 광주:29[0], 대전:30[0], 울산:31[0], 경기:41[1], 강원:42[0]
    충북:43[0], 충남:44[0], 전북:45[0], 전남:46[0], 경북:47[0], 경남:48[0], 제주:50[1]  
    apt_list()에 필요한 지역 코드 대입

    서비스 지역 확장시 추가하는식으로?...

    [1] : 저장함
    [0] : 저장안함

    실행 : python manage.py get_houses
    """

    def handle(self, *args, **options):
        apt_data = apt_list(41)
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
