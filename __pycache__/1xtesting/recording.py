import time
import openpyxl
from selenium import webdriver

# Create a new Chrome instance
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://1xbet.com")

# Wait for the page to load
time.sleep(10)

# Close the cookies dialog box
driver.find_element_by_css_selector("button.css-1s0s0u8").click()

# Open the Live section
driver.find_element_by_css_selector("a.css-1t35v4t").click()

# Wait for the Live section to load
time.sleep(10)

# Open an Excel workbook
workbook = openpyxl.Workbook()

# Create a new worksheet
worksheet = workbook.active

# Set the headers for the worksheet
worksheet["A1"] = "Event"
worksheet["B1"] = "Time"
worksheet["C1"] = "Outcome"

# Start a loop that runs indefinitely
while True:
    # Get all the live events on the page
    events = driver.find_elements_by_css_selector("div.css-12q3q1j")

    # Loop through each event
    for event in events:
        # Get the event name
        event_name = event.find_element_by_css_selector("div.css-xwaf0d").text

        # Get the time of the event
        event_time = event.find_element_by_css_selector("div.css-1hyzvmp").text

        # Get the available outcomes for the event
        outcomes = event.find_elements_by_css_selector("div.css-10bdpru")

        # Loop through each outcome
        for outcome in outcomes:
            # Get the name of the outcome
            outcome_name = outcome.find_element_by_css_selector("span.css-14rv2i0").text

            # Get the odds for the outcome
            outcome_odds = outcome.find_element_by_css_selector("span.css-15kwphj").text

            # Get the next available row in the worksheet
            row = worksheet.max_row + 1

            # Write the data to the worksheet
            worksheet["A{}".format(row)] = event_name
            worksheet["B{}".format(row)] = event_time
            worksheet["C{}".format(row)] = "{} ({})".format(outcome_name, outcome_odds)

            # Save the workbook
            workbook.save("1xbet_data.xlsx")

    # Wait for 10 seconds before getting the next data
    time.sleep(10)
