from reading_scraper import fetch_daily_readings

if __name__ == "__main__":
    readings = fetch_daily_readings()
    print(readings)
    for section, content in readings.items():
        print(f"== {section} ==\n")
        if content:
            print(content)
        else:
            print("Section not found or not available for this date.")
        print("\n" + "-"*40 + "\n")