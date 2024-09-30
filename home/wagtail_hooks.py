from bs4 import BeautifulSoup
from wagtail import hooks
from wagtail.rich_text import expand_db_html


class CustomRichTextRenderer:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        # دریافت HTML از richtext
        html = expand_db_html(self.value.source)

        # ویرایش HTML با BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # اضافه کردن کلاس 'main-slider__text-two' به تمامی تگ‌های <p>
        for p in soup.find_all("p"):
            p["class"] = p.get("class", []) + ["main-slider__text-two"]

        return str(soup)


@hooks.register("register_rich_text_features")
def register_custom_richtext_renderer(features):
    # تعریف ویژگی سفارشی richtext
    features.default_features.append("custom_richtext")
