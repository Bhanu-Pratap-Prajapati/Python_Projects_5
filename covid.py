import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

DATA_FILE = "covid_data.csv"

# Initialize or load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=['Date'])
    else:
        return pd.DataFrame(columns=['Date', 'City', 'Cases', 'Recoveries', 'Deaths'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add daily data
    date = input("Date (YYYY-MM-DD): ")
    city = input("City: ")
    cases = int(input("New Cases: "))
    recoveries = int(input("Recoveries: "))
    deaths = int(input("Deaths: "))

    new_entry = pd.DataFrame([{
        'Date': pd.to_datetime(date),
        'City': city,
        'Cases': cases,
        'Recoveries': recoveries,
        'Deaths': deaths
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    print("Data added successfully.\n")
    return df

# Analyze risk zones
def analyze_risk_zones(df):
    latest = df.groupby('City').last()
    print("\n--- Risk Zones ---")
    for city, row in latest.iterrows():
        active = row['Cases'] - row['Recoveries'] - row['Deaths']
        if active > 1000:
            risk = '🔴 High Risk'
        elif active > 100:
            risk = '🟠 Medium Risk'
        else:
            risk = '🟢 Low Risk'
        print(f"{city}: {risk} (Active: {active})")
    print()

# Generate summary and trends
def show_summary(df):
    print("\n--- COVID Summary ---")
    summary = df.groupby('City')[['Cases', 'Recoveries', 'Deaths']].sum()
    print(summary)

# Plot trends
def plot_trends(df):
    city = input("Enter city for trend visualization: ")
    city_data = df[df['City'].str.lower() == city.lower()].sort_values('Date')
    if city_data.empty:
        print("No data for this city.")
        return
    
    plt.figure(figsize=(10,6))
    plt.plot(city_data['Date'], city_data['Cases'], label='Cases')
    plt.plot(city_data['Date'], city_data['Recoveries'], label='Recoveries')
    plt.plot(city_data['Date'], city_data['Deaths'], label='Deaths')
    plt.title(f"COVID-19 Trends in {city.title()}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Predict hotspots (rapid case rise)
def predict_hotspots(df):
    print("\n--- Hotspot Prediction ---")
    recent = df[df['Date'] > datetime.now() - pd.Timedelta(days=7)]
    trends = recent.groupby('City')['Cases'].sum()
    hotspots = trends[trends > 500]  # Threshold can be adjusted
    if hotspots.empty:
        print("No hotspots predicted.")
    else:
        for city, cases in hotspots.items():
            print(f"🔥 {city}: {cases} cases in the last 7 days")
    print()

# Import from CSV
def import_csv():
    file = input("Enter CSV file path to import: ")
    if not os.path.exists(file):
        print("File not found.")
        return pd.DataFrame()
    imported_df = pd.read_csv(file, parse_dates=['Date'])
    print(f"Imported {len(imported_df)} rows.")
    return imported_df

# Main menu
def menu():
    df = load_data()
    while True:
        print("""
COVID Data Dashboard
1. Add Daily Data
2. Analyze Risk Zones
3. Show Summary
4. Plot City Trends
5. Predict Hotspots
6. Import from CSV
7. Exit
""")
        choice = input("Enter choice: ")
        if choice == '1':
            df = save_data(df)
        elif choice == '2':
            analyze_risk_zones(df)
        elif choice == '3':
            show_summary(df)
        elif choice == '4':
            plot_trends(df)
        elif choice == '5':
            predict_hotspots(df)
        elif choice == '6':
            new_df = import_csv()
            if not new_df.empty:
                df = pd.concat([df, new_df], ignore_index=True)
                save_data(df)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == '__main__':
    menu()