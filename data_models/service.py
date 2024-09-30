from django.db import IntegrityError
from .models import Category, Ingredient, Product, SubCategory
import re

def save_categories(categories):
    results = []

    for category in categories:
        category_name, url_path = category
        try:
            vendor_id = extract_vendor_id(url_path)

            category, _ = Category.objects.update_or_create(
                vendor_id=vendor_id,
                defaults={
                    "name": category_name,
                    "vendor_url": url_path,
                },
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
            sub_category, _ = SubCategory.objects.update_or_create(
                vendor_id=vendor_id,
                defaults={
                    "name": sub_category_name,
                    "vendor_url": url_path,
                    "category": category,
                },
            )

            results.append(sub_category)
        except Exception as error:
            print(f"SubCategory {sub_category_name} could not be saved. Error: {error}")

    return results


def save_products(product_details):
    for detail in product_details:

        ingredients = extract_ingredients(detail["ingredients_text"])

        product, _ = Product.objects.update_or_create(
            vendor_id=detail["vendor_id"],
            defaults={
                "name": detail["name"],
                "brand": detail["brand"],
                "product_description": detail["product_description"],
                "vendor_id": detail["vendor_id"],
                "ingredients_text": detail["ingredients_text"],
            },
        )

        product.category.add(detail["category"])

        product.sub_category.add(detail["sub_category"])

        for ingredient_name in ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            product.ingredients.add(ingredient)

        product.save()


def extract_ingredients(ingredients_text):
    ingredients = ingredients_text.strip().lower()

    ingredients = ingredients.replace(".", "")

    ingredients = re.split(r"[(),]", ingredients)

    ingredients = [ingredient.strip() for ingredient in ingredients]

    ingredients = [i for i in ingredients if "may contain" not in i]

    return ingredients


def extract_vendor_id(url_path):
    return url_path.split("/")[-1]
