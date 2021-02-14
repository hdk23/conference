from .models import *
import csv


def read_file(file_name):
    with open(f'./inputs/{file_name}.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1


def read_groups(row):
    TallyGroup(name=row[0], acronym=row[1]).save()


def read_categories(row):
    group = TallyGroup.objects.get(acronym=row[0])
    category = TallyCategory(name=row[1], acronym=row[2], weight=row[3], scaled=row[4])
    category.save()
    group.categories.add(category)
    group.save()

