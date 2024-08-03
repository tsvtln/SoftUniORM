import os
import django
from django.db import models
from django.db.models import Q, F, Max, Count, Subquery, Sum, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission


# from dummy_data import populate_model_with_data
# populate_model_with_data(Spacecraft, 20)
# Create queries within functions

def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    search_string = search_string.strip()

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)

    tp = []
    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts.exists():
        return ''

    for jingibi in astronauts:
        tp.append(
            f"Astronaut: {jingibi.name}, phone number: {jingibi.phone_number}, status: "
            f"{f'Active' if jingibi.is_active else 'Inactive'}")

    return '\n'.join(tp)


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().filter(missions_count__gt=0).first()

    if astronaut is None:
        return 'No data.'

    return f'Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions.'


def get_top_commander():
    # Subquery to count the number of missions commanded by each astronaut
    commanded_missions_subquery = Mission.objects.filter(
        commander_id=models.OuterRef('pk')
    ).values('commander_id').annotate(
        commanded_missions_count=Count('id')
    ).values('commanded_missions_count')

    # Annotate astronauts with the number of commanded missions
    astronauts = Astronaut.objects.annotate(
        commanded_missions_count=Subquery(commanded_missions_subquery, output_field=models.IntegerField())
    ).order_by('-commanded_missions_count', 'phone_number')

    # Get the top astronaut
    top_commander = astronauts.first()

    if top_commander and top_commander.commanded_missions_count is not None and top_commander.commanded_missions_count > 0:
        return f"Top Commander: {top_commander.name} with {top_commander.commanded_missions_count} commanded missions."
    else:
        return "No data."


def get_last_completed_mission():
    # last_mission = Mission.objects.all().order_by('launch_date').filter(status='COMPLETE').first()
    # if not last_mission:
    #     return 'No data.'
    # return f"The last completed mission is: {last_mission.name}. Commander:
    # {last_mission.commander__name if not last_mission.commander__name == 'null' else 'TBA'}."
    # Retrieve the last completed mission (latest launch date)
    last_completed_mission = Mission.objects.filter(
        status=Mission.Statuses.COMPLETED
    ).order_by('-launch_date').first()

    if not last_completed_mission:
        return "No data."

    commander_name = last_completed_mission.commander.name if last_completed_mission.commander else 'TBA'

    astronauts = last_completed_mission.astronauts.all().order_by('name')
    astronaut_names = ', '.join([astronaut.name for astronaut in astronauts])

    spacecraft_name = last_completed_mission.spacecraft.name

    total_spacewalks = astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks'] or 0

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. "
            f"Spacecraft: {spacecraft_name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecrafts = Spacecraft.objects.annotate(
        num_missions=Count('mission')
    ).order_by('-num_missions', 'name')
    most_used_spacecraft = spacecrafts.first()

    if not most_used_spacecraft:
        return "No data."
    unique_astronauts_count = Astronaut.objects.filter(
        missions__spacecraft=most_used_spacecraft
    ).distinct().count()

    return (f"The most used spacecraft is: {most_used_spacecraft.name}, "
            f"manufactured by {most_used_spacecraft.manufacturer}, "
            f"used in {most_used_spacecraft.num_missions} missions, "
            f"astronauts on missions: {unique_astronauts_count}.")

#
# def decrease_spacecrafts_weight() -> str:
#     # ships_to_update = Spacecraft.objects.prefetch_related('missions').filter(
#     #     spacecraft_missions__status=Mission.Statuses.PLANNED, weight__gte=200.0).distinct()
#
#     planned_missions = Mission.objects.filter(status=Mission.Statuses.PLANNED)
#     ships_to_update = Spacecraft.objects.filter(mission__in=planned_missions, weight__gte=200.0).distinct()
#     if not ships_to_update.exists():
#         return 'No changes in weight.'
#
#     affected_ships = ships_to_update.count()
#
#     ships_to_update.update(weight=F('weight') - 200.0)
#     avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
#
#     return (
#         f'The weight of the {affected_ships} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f} kg.')

#
def decrease_spacecrafts_weight():
    planned_missions = Mission.objects.filter(status=Mission.Statuses.PLANNED)
    # spacecrafts_to_update = Spacecraft.objects.filter(mission__in=planned_missions).distinct().filter(weight__gte=200.0)
    spacecrafts_to_update = Spacecraft.objects.prefetch_related('missions').filter(
        spacecraft_missions__status=Mission.Statuses.PLANNED, weight__gte=200.0).distinct()
    num_of_spacecrafts_affected = spacecrafts_to_update.count()

    if num_of_spacecrafts_affected == 0:
        return "No changes in weight."

    spacecrafts_to_update.update(weight=F('weight') - 200.0)

    Spacecraft.objects.filter(weight__lt=0.0).update(weight=0.0)

    average_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    # if average_weight:
    # average_weight = round(average_weight, 1)

    return (f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {average_weight:.1f}kg.")

# def decrease_spacecrafts_weight():
#     spacecrafts_to_update = Spacecraft.objects.prefetch_related('missions').filter(
#         mission__in='Planned').distinct().filter(weight__gte=200.0)
#
#     spacecrafts_affected = spacecrafts_to_update.count()
#
#     if spacecrafts_affected == 0:
#         return 'No changes in weight.'
#
#     spacecrafts_to_update.update(weight=F('weight') - 200.0)
#
#     avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
#
#     return (f"The weight of {spacecrafts_affected} spacecrafts has been decreased. "
#             f"The new average weight of all spacecrafts is {avg_weight:.1f}kg.")



# print(get_astronauts('cecko'))
# print(get_top_astronaut())
# print(get_top_commander())
# print(decrease_spacecrafts_weight())
