from .models import CompanyInfo


def company_info(request):
    try:
        company_info = (
            CompanyInfo.objects.first()
        )  # اولین رکورد را دریافت می‌کنیم (فرض اینکه یک رکورد داریم)
    except CompanyInfo.DoesNotExist:
        company_info = None
    return {"company_info": company_info}
