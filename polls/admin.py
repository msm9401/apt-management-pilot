from django.contrib import admin

from .models import Question, Choice


class ChoiceAdminInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "end_date",
        "status",
        "house",
    )

    list_filter = ("status", "created_at")

    search_fields = ["title"]

    search_help_text = "투표(설문조사) 제목 검색"

    autocomplete_fields = ["house"]

    inlines = [ChoiceAdminInline]

    def get_queryset(self, request):
        """
        관리자 아파트의 투표만 get.
        superuser(웹마스터)는 아파트에 관계없이 모든 투표 get.
        """
        if not request.user.is_superuser:
            return (
                super()
                .get_queryset(request)
                .filter(house=request.user.my_houses.first())
            )
        return super().get_queryset(request)

    def get_changeform_initial_data(self, request):
        # 투표 추가시 아파트의 default값으로 관리자의 아파트로 설정
        return {"house": request.user.my_houses.first()}

    def save_model(self, request, obj, form, change):
        """
        관리자가 default로 설정된 아파트 값을 바꿔서 추가해도 관리자 아파트로 저장.
        superuser(웹마스터)는 그대로 아파트에 관계없이 저장 가능.
        """
        if not request.user.is_superuser:
            obj.house = request.user.my_houses.first()
            return super().save_model(request, obj, form, change)

        return super().save_model(request, obj, form, change)
