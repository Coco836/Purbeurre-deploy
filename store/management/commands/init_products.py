from django.core.management.base import BaseCommand, CommandError
from store.api import OpenFoodFactsApi
from store.models import Product, Category, Shop
from store.management.commands.init_categories import Command as Cat_command
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger('Pur Beurre')


class Command(BaseCommand):
    ''' Command to execute in order to fill all tables from store app. '''
    help = 'Initialize database from Open Food Facts API.'

    def handle(self, *args, **options):
        ''' Method that retrieve data from API and fill tables. '''
        api = OpenFoodFactsApi()
        category = Cat_command()
        # Call command that retrieve categories from API
        category_list = category.init_category()
        for category in category_list:
            # Retrieve products of all categories in database from API
            for json_product in api.fetch_products_data_api(category):
                try:
                    product = Product.from_api(json_product)
                    product.save()
                # Do not save a product if it already exists
                except (IntegrityError, KeyError) as error:
                    logger.warn(error)
                # Link a product to all the categories it belongs to 
                # if the category exists in database
                else:
                    if 'categories' in json_product:
                        list_of_product_categories = (
                                        json_product['categories'].split(',')
                        )
                        for product_category in list_of_product_categories:
                            try:
                                category_in_db = (
                                            Category.objects.get(
                                                name=product_category.strip()
                                            )
                                )
                                product.categories.add(category_in_db)
                            except ObjectDoesNotExist:
                                last_id_inserted = Category.objects.get(
                                                            name=category
                                                    )
                                product.categories.add(last_id_inserted)

                    # Link a product to all the stores it can be found in 
                    # and save these shops in database
                    if 'stores' in json_product:
                        list_of_product_shops = (
                                        json_product['stores'].split(',')
                        )
                        for product_shop in list_of_product_shops:
                            try:
                                shop = Shop.objects.get_or_create(
                                                    name=product_shop.strip()
                                        )
                            except ValueError as error:
                                logger.warn(error)
                            else:
                                product.shops.add(shop[0])
