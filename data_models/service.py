from django.db import IntegrityError
from .models import Category


def save_categories(categories):
    for category in categories:
        category_name, url_path = category
        try:
            vendor_id = extract_vendor_id(url_path)
            category = Category(
                name=category_name, vendor_url=url_path, vendor_id=vendor_id
            )
            category.save()
        except IntegrityError:
            print(f"Category {category_name} already exists.")


def extract_vendor_id(url_path):
    return url_path.split("/")[-1]
