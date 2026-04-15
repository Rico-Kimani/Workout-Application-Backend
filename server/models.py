from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)


    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value

    workout_exercises = db.relationship(
        'WorkoutExercise',
        backref='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        viewonly=True
    )

    def __repr__(self):
        return f"<Workout {self.id}>"
    

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    muscle_group = db.Column(db.String(50))
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    @validates('category')
    def validate_category(self, key, value):
        allowed = ['strength', 'cardio', 'flexibility', 'balance']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return value

    workout_exercises = db.relationship(
        'WorkoutExercise',
        backref='exercise',
        cascade='all, delete-orphan'
    )

    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        viewonly=True
    )

    def __repr__(self):
        return f"<Exercise {self.name}>"
    
class WorkoutExercise(db.Model):
    """Represents the association between a Workout and an Exercise with specific details."""
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)


    @validates('sets')
    def validate_sets(self, key, value):
        if value <= 0:
            raise ValueError("Sets must be greater than 0")
        return value
    
    def validate_reps_duration(self):
        if self.reps is None and self.duration_seconds is None:
            raise ValueError("Must provide either reps or duration_seconds")

        if self.reps is not None and self.duration_seconds is not None:
            raise ValueError("Provide either reps OR duration_seconds, not both")

    __table_args__ = (
        UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
        CheckConstraint('sets > 0', name='check_sets_positive'),
         CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='check_duration_positive'),
        CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
        CheckConstraint('weight >= 0', name='check_weight_non_negative'),
    )

    def __repr__(self):
        return f"<WorkoutExercise Workout ID: {self.workout_id}, Exercise ID: {self.exercise_id}>"