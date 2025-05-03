from tkinter import *
from collections import namedtuple
import heapq

# Define Food item using a namedtuple (for structured knowledge representation)
Food = namedtuple('Food', ['name', 'category', 'calories'])

# Knowledge base: Example food database
food_db = [
    Food('Yogurt(1 cup)', 'protein', 150),
    Food('Cooked meat(3 Oz)', 'protein', 210),
    Food('Cooked fish(4 Oz)', 'protein', 180),
    Food('1 whole egg + 4 egg whites', 'protein', 150),
    Food('Tofu(5 Oz)', 'protein', 130),
    Food('Apple', 'fruit', 95),
    Food('Orange', 'fruit', 80),
    Food('Banana', 'fruit', 110),
    Food('Dried Fruits(Handful)', 'fruit', 120),
    Food('Fruit Juice(125ml)', 'fruit', 100),
    Food('Vegetables(80g)', 'vegetable', 35),
    Food('Whole Grain Bread(1 slice)', 'grain', 90),
    Food('Oats(250g)', 'grain', 150),
    Food('Corn tortillas (2)', 'grain', 120),
    Food('Soy nuts(1 Oz)', 'ps', 140),
    Food('Cottage cheese (125g)', 'ps', 160),
    Food('Olive oil (2 tsp)', 'taste_en', 80),
    Food('Jam (1 tbsp)', 'taste_en', 50),
]

# Heuristic search: Best-first based on closest calorie match
def plan_meal(calorie_target):
    selected = []
    heap = []
    total_cal = 0

    # Heuristic: absolute difference from target
    for food in food_db:
        diff = abs(calorie_target - food.calories)
        heapq.heappush(heap, (diff, food))

    while heap and total_cal < calorie_target:
        _, food = heapq.heappop(heap)
        selected.append(food)
        total_cal += food.calories

    return selected

# Tkinter UI setup
app = Tk()
app.title("AI Dietician - BMR Meal Planner")

Label(app, text='Gender').grid(row=0, column=0)
Label(app, text='Weight (kg)').grid(row=1, column=0)
Label(app, text='Height (cm)').grid(row=2, column=0)
Label(app, text='Age').grid(row=3, column=0)
Label(app, text='Activity').grid(row=4, column=0)

v3 = StringVar()
v4 = StringVar()
v5 = StringVar()
Entry(app, textvariable=v3).grid(row=1, column=1)
Entry(app, textvariable=v4).grid(row=2, column=1)
Entry(app, textvariable=v5).grid(row=3, column=1)

Lb2 = Listbox(app, height=2)
Lb2.insert(1, 'Male')
Lb2.insert(2, 'Female')
Lb2.grid(row=0, column=1)

Lb = Listbox(app, height=5)
Lb.insert(1, 'Sedentary (little or no exercise)')
Lb.insert(2, 'Lightly active (1-3 days/week)')
Lb.insert(3, 'Moderately active (3-5 days/week)')
Lb.insert(4, 'Very active (6-7 days/week)')
Lb.insert(5, 'Super active (twice/day)')
Lb.grid(row=4, column=1)

def calculate_bmr():
    weight = float(v3.get())
    height = float(v4.get())
    age = int(v5.get())
    gender = Lb2.get(ACTIVE)
    activity = Lb.get(ACTIVE)

    if gender == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_factor = {
        'Sedentary (little or no exercise)': 1.2,
        'Lightly active (1-3 days/week)': 1.375,
        'Moderately active (3-5 days/week)': 1.55,
        'Very active (6-7 days/week)': 1.725,
        'Super active (twice/day)': 1.9
    }
    total_cal = bmr * activity_factor[activity]

    result = plan_meal(total_cal)
    display_meal(result, total_cal)

def display_meal(meals, total):
    Label(app, text=f"Target Calories: {int(total)}").grid(row=6, column=0, columnspan=2)
    for idx, food in enumerate(meals):
        Label(app, text=f"{food.category}: {food.name} ({food.calories} cal)").grid(row=7+idx, column=0, columnspan=2)

Button(app, text='Generate Meal Plan', command=calculate_bmr).grid(row=5, column=1)
app.mainloop()
