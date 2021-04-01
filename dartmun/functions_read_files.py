from .models import *
from datetime import datetime
import csv
conference_acronym = "DartMUN 2021"
conference = Conference.objects.get(acronym=conference_acronym)

rubrics = {
    "pp_rubric": "Position Paper Rubric", "part_rubric": "Participation Rubric", "reso_rubric": "Resolution Rubric"
}


def read_file(file_name):
    with open(f'dartmun/inputs/dartmun/{file_name}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = []
        line_count = 0
        if file_name in rubrics:
            if file_name == "pp_rubric":
                Rubric(title=rubrics[file_name], tally_category=TallyCategory.objects.get(acronym="PP")).save()
            elif file_name == "reso_rubric":
                Rubric(title=rubrics[file_name], tally_category=TallyCategory.objects.get(acronym="R")).save()
            elif file_name == "part_rubric":
                Rubric(title=rubrics[file_name], tally_category=TallyCategory.objects.get(acronym="P")).save()
        for row in csv_reader:
            if line_count != 0:
                if file_name in rubrics:
                    read_rubric(row, header_row, rubrics[file_name])
                else:
                    if file_name == "categories":
                        TallyCategory(name=row[0], acronym=row[1], weight=row[2], scaled=row[3]).save()
                    elif file_name == "committees":
                        read_committee(row)
                    elif file_name == "dais":
                        read_user(row, "chair")
                    elif file_name == "delegates":
                        read_user(row)
                    elif file_name == "secretariat":
                        read_user(row, "secretariat")
                    elif file_name == "modes":
                        DebateMode(mode=row[0], acronym=row[1], speeches=row[2], yielding=row[3], duration=row[4],
                                   speaking_time=row[5]).save()
                    elif file_name == "motions":
                        Motion(motion=row[0], vote_type=row[1], speeches=row[2], duration=row[3], speaking_time=row[4],
                               topic=row[5], purpose=row[6]).save()
                    elif file_name == "organs":
                        read_organ(row)
                    elif file_name == "schools":
                        School(name=row[0]).save()
                    elif file_name == "sessions":
                        read_session(row)
            else:
                header_row = row
            line_count += 1


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


def read_committee(row):
    organ = Organ.objects.get(acronym=row[0])
    committee = Committee(acronym=row[1], name=row[2])
    committee.save()
    topic1 = Topic(number=1, topic=row[3])
    topic1.save()
    committee.topics.add(topic1)
    if row[4]:
        topic2 = Topic(number=2, topic=row[4])
        topic2.save()
        committee.topics.add(topic2)
    if row[1] == "UNEP":
        committee.set_managers(double=True)
    else:
        committee.set_managers()
    committee.save()
    organ.committees.add(committee)
    organ.save()


def read_organ(row):
    organ = Organ(acronym=row[0], name=row[1])
    organ.save()
    conference.organs.add(organ)
    conference.save()


def read_session(row):
    session = Session(number=int(row[0]), start_time=row[1], end_time=row[2], counts=bool(row[3]))
    session.save()
    conference.sessions.add(session)
    conference.save()


def read_user(row, participant="delegate"):
    if participant != "secretariat":
        committee = Committee.objects.get(acronym=row[4])
        people_manager = committee.people

    if participant == "chair":
        user = people_manager.add_user(row[0], row[1], row[2], row[3], staff=True, superuser=False)
        people_manager.add_chair(user, row[5], row[6])
    elif participant == "secretariat":
        user = PeopleManager.add_user(row[0], row[1], row[2], row[3], staff=True, superuser=True)
        conference.add_secretariat(user, row[4], row[5], row[6])
    else:
        user = people_manager.add_user(row[0], row[1], row[2], row[3])
        delegate = people_manager.add_delegate(user, row[5], row[6], row[7])
        delegation = people_manager.delegations.get(delegates=delegate)
        try:
            score_manager = ScoreManager.objects.get(delegation=delegation)
        except:
            committee.initialize_delegation(delegation)
