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
        elif file_name == "part_rubric":
            part_rubric = Rubric(title="Participation Rubric", tally_category=TallyCategory.objects.get(acronym="P"))
            part_rubric.save()
        elif file_name == "reso_rubric":
            reso_rubric = Rubric(title="Resolution Rubric", tally_category=TallyCategory.objects.get(acronym="R"))
            reso_rubric.save()
        for row in csv_reader:
            if line_count != 0:
                if file_name == "categories":
                    read_categories(row)
                elif file_name == "modes":
                    read_modes(row)
                elif file_name == "motions":
                    read_motions(row)
                elif file_name == "pp_rubric":
                    read_rubric(row, header_row, "Position Paper Rubric")
                elif file_name == "part_rubric":
                    read_rubric(row, header_row, "Participation Rubric")
                elif file_name == "reso_rubric":
                    read_rubric(row, header_row, "Resolution Rubric")
            else:
                header_row = row
            line_count += 1


def read_categories(row):
    category = TallyCategory(name=row[0], acronym=row[1], weight=row[2], scaled=row[3])
    category.save()


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

