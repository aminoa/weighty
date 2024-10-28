import argparse
import os
import sys
import csv
from dataclasses import dataclass
import datetime

@dataclass
class Exercise:
    title: str
    start_time: datetime.date
    end_time: datetime.date
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
    with open(filepath, 'r', encoding="utf8") as csvfile:
        workout_reader = csv.reader(csvfile)
        for row in workout_reader:
            print(row)


def main():
    parser = argparse.ArgumentParser(prog="weighty", description="Hevy App workout stats")
    parser.add_argument('filepath')
    args = parser.parse_args()
    filepath = args.filepath

    if not os.path.exists(filepath):
        print("Error: CSV filepath must exist")
        exit(1)
    
    reader(filepath)

if __name__ == '__main__':
    main()