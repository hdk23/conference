from .models import *
import csv


def read_file(file_name):
    with open(f'dartmun/inputs/dartmun/{file_name}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if file_name == "groups":
                    read_groups(row)
                elif file_name == "categories":
                    read_categories(row)
                elif file_name == "modes":
                    read_modes(row)
                elif file_name == "motions":
                    read_motions(row)
            line_count += 1


def read_groups(row):
    TallyGroup(name=row[0], acronym=row[1]).save()


def read_categories(row):
    group = TallyGroup.objects.get(acronym=row[0])
    category = TallyCategory(name=row[1], acronym=row[2], weight=row[3], scaled=row[4])
    category.save()
    group.categories.add(category)
    group.save()


def read_modes(row):
    DebateMode(mode=row[0], acronym=row[1], speeches=row[2], yielding=row[3], duration=row[4], speaking_time=row[5]).save()


def read_motions(row):
    Motion(motion=row[0], vote_type=row[1], speeches=row[2], duration=row[3], speaking_time=row[4], topic=row[5], purpose=row[6]).save()
