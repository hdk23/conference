from .models import *
import csv


def read_file(file_name):
    with open(f'dartmun/inputs/dartmun/{file_name}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = []
        line_count = 0
        if file_name == "pp_rubric":
            pp_rubric = Rubric(title="Position Paper Rubric", tally_category=TallyCategory.objects.get(acronym="PP"))
            pp_rubric.save()
        elif file_name == "wp_part_rubric":
            part_rubric = Rubric(title="Working Paper Participation Rubric", tally_category=TallyCategory.objects.get(acronym="WP"))
            part_rubric.save()
        elif file_name == "wp_rubric":
            wp_rubric = Rubric(title="Working Paper Rubric", tally_category=TallyCategory.objects.get(acronym="R"))
            wp_rubric.save()
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
                elif file_name == "pp_rubric":
                    read_rubric(row, header_row, "Position Paper Rubric")
                elif file_name == "wp_part_rubric":
                    read_rubric(row, header_row, "Working Paper Participation Rubric")
                elif file_name == "wp_rubric":
                    read_rubric(row, header_row, "Working Paper Rubric")
            else:
                header_row = row
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


def read_rubric(row, header_row, title):
    criterion = Criterion(criterion=row[0], weight=int(header_row[1]))
    criterion.save()
    rubric = Rubric.objects.get(title=title)
    rubric.max_possible += criterion.weight
    rubric.save()
    for num in range(1, len(row)):
        descriptor = Descriptor(descriptor=row[num], points=header_row[num])
        descriptor.save()
        criterion.possible_scores.add(descriptor)
        criterion.save()
        rubric.criteria.add(criterion)
        rubric.save()

