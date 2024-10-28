import argparse
import os
from collections import defaultdict, Counter
import csv
from dataclasses import dataclass
import datetime

# Activity done in a circuit
@dataclass
class Exercise:
    title: str
    start_time: str
    end_time: str
    description: str
    exercise_title: str
    superset_id: str
    exercise_notes: str
    set_index: int
    set_type: str
    weight_lbs: int
    reps: int
    distance_miles: int
    duration_seconds: int	
    rpe: str

def reader(filepath):
    """
    Takes in a workouts CSV file and returns a list of exercises completed
    """
    exercises = []
    with open(filepath, 'r', encoding="utf8") as csvfile:
        workout_reader = csv.reader(csvfile)
        # skip header
        next(workout_reader, None)
 
        for row in workout_reader:
            exercises.append(Exercise(
                title=row[0], 
                start_time=datetime.datetime.strptime(row[1], "%d %b %Y, %H:%M"),
                end_time=datetime.datetime.strptime(row[2], "%d %b %Y, %H:%M"),
                description=row[3], 
                exercise_title=row[4],
                superset_id=row[5], 
                exercise_notes=row[6], 
                set_index=row[7], 
                set_type=row[8], 
                weight_lbs=int(row[9]) if row[9] else None, 
                reps=int(row[10]) if row[10] else None, 
                distance_miles=int(row[11]) if row[11] else None, 
                duration_seconds=int(row[12]) if row[12] else None,
                rpe=row[13])
            )
            
    return exercises

def get_daily_workouts(exercises):
    """
    Takes in an exercise list and groups together the exercises by day
    """
    workouts = defaultdict(list)
    for exercise in exercises:
        workouts[exercise.start_time.date()].append(exercise)

    return workouts

def get_average_workout_time(workouts):
    average_workout_time = 0
    for workout in workouts:
        earliest_time = min([exercise.start_time for exercise in workouts[workout]])
        latest_time = max([exercise.end_time for exercise in workouts[workout]])
        current_workout_time = (latest_time - earliest_time).seconds
        average_workout_time += current_workout_time
    average_workout_time = average_workout_time / len(workouts)
    return average_workout_time

def get_pounds_lifted(workouts):
    pounds_lifted = 0
    for workout in workouts:
        for exercise in workouts[workout]:
            if exercise.weight_lbs:
                pounds_lifted += int(exercise.weight_lbs) * int(exercise.reps)
    return pounds_lifted


def main():
    parser = argparse.ArgumentParser(prog="weighty", description="Hevy App workout stats")
    parser.add_argument('filepath')
    args = parser.parse_args()
    filepath = args.filepath

    if not os.path.exists(filepath):
        print("Error: CSV filepath must exist")
        exit(1)
    
    exercises = reader(filepath)
    workouts = get_daily_workouts(exercises)
    average_workout_time = get_average_workout_time(workouts)
    exercise_title_counts = Counter(exercise.exercise_title for exercise in exercises)
    exercise_title_counts_freq = exercise_title_counts.most_common()
    pounds_lifted = get_pounds_lifted(workouts)

    print("Hevy Workout Stats: ")
    print("Total Daily Workout Count 💪:", len(workouts))
    print("Total Individual Exercise Count 🏃:", len(exercises))
    print("Total Weight Lifted 🏋️:", pounds_lifted, "lbs")
    print("Average Workout Time ⏰:", average_workout_time / 60, "minutes")
    print("Favorite Exercise(s) 😄:", exercise_title_counts_freq[:3])
    print("Least Favorite Exercise 😢", exercise_title_counts_freq[-1])


if __name__ == '__main__':
    main()