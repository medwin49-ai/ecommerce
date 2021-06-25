from django.core.management.base import BaseCommand, CommandError
from main.models import Product, Potency
import argparse


class Command(BaseCommand):
    help = 'Populates the database with values specified in the file passed'

    def add_arguments(self, parser):
        parser.add_argument('--file_path', nargs='+', type=argparse.FileType('r'))
        parser.add_argument('--table', nargs='+')

    def handle(self, *args, **options):
        input_file = options['file_path'][0]
        table = options['table'][0]

        if table == 'product':
            self.handle_product_table(input_file)  
        elif table == 'potency':
            self.handle_potency_table(input_file)

    def handle_product_table(self, input_file):
        while True:
            line = input_file.readline()
            if len(line.strip()) == 0:
                break
            else:
                values = line.split(',')
                name = values[0]
                desc = values[1]
                p = Product(product_name=name, product_description=desc)
                p.save() 
                self.stdout.write(self.style.SUCCESS('Successfully added "%s"' % line))  

    def handle_potency_table(self, input_file):
        while True:
            line = input_file.readline()
            if len(line.strip()) == 0:
                break
            else:
                values = line.split(',')
                product_id = values[0]
                product = Product.objects.get(pk=product_id)
                potency_value = values[1]
                price = values[2]
                supply = values[3]
                print(line)
                p = Potency(product=product, potency_value=potency_value, price=price, supply=supply)
                p.save()   
                self.stdout.write(self.style.SUCCESS('Successfully added "%s"' % line))   