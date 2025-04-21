import datetime
import time
import matplotlib.pyplot as plt

# Store weekly data
weekly_data = []

# Constants
WATER_GOAL = 2.5  # liters/day
STEP_GOAL = 10000
SLEEP_GOAL = 8  # hours
CALORIE_GOAL = 2000

# BMI Calculator
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

# Calorie Calculator (Mifflin-St Jeor formula estimate)
def calorie_needs(weight, age, gender):
    if gender.lower() == 'male':
        return int(10 * weight + 6.25 * 170 - 5 * age + 5)
    else:
        return int(10 * weight + 6.25 * 170 - 5 * age - 161)

# Hydration Reminder
def hydration_reminder():
    print("\n💧 Stay hydrated! Remember to drink water every 2 hours.")
    time.sleep(2)  # simulate a delay (for demonstration)

# Log daily data
def log_day():
    print("\nEnter today's health data:")
    date = datetime.date.today().strftime('%A %d-%b-%Y')
    steps = int(input("Steps taken: "))
    sleep = float(input("Hours of sleep: "))
    calories = int(input("Calories consumed: "))
    water = float(input("Water intake (L): "))

    day_data = {
        'date': date,
        'steps': steps,
        'sleep': sleep,
        'calories': calories,
        'water': water
    }
    weekly_data.append(day_data)

    print("\n📊 Daily Summary:")
    print(f"Date: {date}")
    print(f"Steps: {steps} / {STEP_GOAL}")
    print(f"Sleep: {sleep} hrs / {SLEEP_GOAL} hrs")
    print(f"Calories: {calories} / {CALORIE_GOAL}")
    print(f"Water: {water} L / {WATER_GOAL} L")
    hydration_reminder()

# Weekly Report & Graphs
def weekly_report():
    if not weekly_data:
        print("\nNo data available for report.")
        return

    print("\n📅 Weekly Health Report")
    for day in weekly_data:
        print(f"{day['date']} - Steps: {day['steps']}, Sleep: {day['sleep']}h, Calories: {day['calories']}kcal, Water: {day['water']}L")

    # Graphs
    dates = [day['date'].split()[0] for day in weekly_data]
    steps = [day['steps'] for day in weekly_data]
    sleep = [day['sleep'] for day in weekly_data]
    water = [day['water'] for day in weekly_data]

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.plot(dates, steps, marker='o')
    plt.title("Steps")
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 2)
    plt.plot(dates, sleep, marker='o', color='purple')
    plt.title("Sleep (hrs)")
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 3)
    plt.plot(dates, water, marker='o', color='blue')
    plt.title("Water Intake (L)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Main Program
def main():
    print("🏋️‍♀️ Welcome to the Health & Fitness Tracker!")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (m): "))
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ")

    bmi = calculate_bmi(weight, height)
    calorie_goal = calorie_needs(weight, age, gender)

    print(f"\n✅ Your BMI: {bmi}")
    print(f"🔥 Estimated daily calorie needs: {calorie_goal} kcal")

    while True:
        print("\nMenu:\n1. Log today's health data\n2. View weekly report\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            log_day()
        elif choice == '2':
            weekly_report()
        elif choice == '3':
            print("Goodbye! Stay healthy 🌿")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
