from django.db import IntegrityError
from .models import Category, SubCategory


def save_categories(categories):
    results = []

    for category in categories:
        category_name, url_path = category
        try:
            vendor_id = extract_vendor_id(url_path)

            category, _ = Category.objects.get_or_create(
                name=category_name, vendor_url=url_path, vendor_id=vendor_id
            )

            results.append(category)
        except Exception as error:
            print(f"Category {category_name} could not be saved. Error: {error}")

    return results


def save_sub_categories(sub_categories):
    results = []

    for sub_category in sub_categories:
        sub_category_name, url_path, category = sub_category

        try:
            vendor_id = extract_vendor_id(url_path)
            sub_category, _ = SubCategory.objects.get_or_create(
                name=sub_category_name,
                vendor_url=url_path,
                vendor_id=vendor_id,
                category=category,
            )

            results.append(sub_category)
        except Exception as error:
            print(f"SubCategory {sub_category_name} could not be saved. Error: {error}")

    return results


def extract_vendor_id(url_path):
    return url_path.split("/")[-1]
