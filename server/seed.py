from app import app
from models import db, Workout, Exercise, WorkoutExercise
from datetime import date

with app.app_context():

    print("Clearing database...")

    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()

    print("Seeding data...")

    w1 = Workout(name="Leg Day", date=date.today(), duration_minutes=60, notes="Leg day")
    e1 = Exercise(name="Push Up", category="strength", equipment_needed=False)

    db.session.add_all([w1, e1])
    db.session.commit()

    we = WorkoutExercise(
        workout_id=w1.id,
        exercise_id=e1.id,
        sets=3,
        reps=10
    )

    we.validate_reps_duration()

    db.session.add(we)
    db.session.commit()

    print("Done seeding!")