from django.core.management.base import BaseCommand, CommandError
from store.api import OpenFoodFactsApi
from store.models import Category
from django.db import IntegrityError
import logging

logger = logging.getLogger('Pur Beurre')


class Command(BaseCommand):
    ''' Command executed by Command in 'init_products'. '''
    help = 'Initialize database from Open Food Facts API.'

    def handle(self, *args, **options):
        ''' Method that call method init_categories and return str. '''
        self.init_category()
        return 'done'

    def init_category(self):
        ''' Method that retrieve data from API and fill table Category. '''
        api = OpenFoodFactsApi()
        category_list = []
        # Retrieve categories from API
        for json_category in api.fetch_categories_data_api()[:2000]:
            try:
                category = Category.from_api(json_category)
                category.save()
                category_list.append(category.name)
            except IntegrityError as error:
                logger.warn(error)
        return category_list
