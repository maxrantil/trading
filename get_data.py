import os
import csv
import requests

# URLs and file paths
btc_url = "https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv"
input_file = "btc.csv"
output_file = "data.csv"

# Function to download the btc.csv file
def download_btc_csv():
    response = requests.get(btc_url)
    with open(input_file, 'wb') as file:
        file.write(response.content)

# Function to extract relevant data from a row
def extract_data(row):
    return [
        row["time"],          # Date and Time
        row["PriceUSD"],      # BTC Price in USD
        row["HashRate"],      # Network HashRate
        row["TxCnt"],         # Transaction Count
        row["TxTfrCnt"],      # Transfer Transaction Count
        row["TxTfrValAdjNtv"],# Adjusted Native Value of Transfers
        row["TxTfrValAdjUSD"],# Adjusted USD Value of Transfers
        row["RevUSD"],        # Revenue in USD
        row["SplyCur"],       # Current Supply
        row["ROI1yr"],        # 1-Year ROI
        row["VtyDayRet30d"]   # Volatility (30-Day)
    ]

# Data point explanations
data_explanations = {
    "time": "Date and Time",
    "PriceUSD": "BTC Price in USD",
    "HashRate": "Network HashRate",
    "TxCnt": "Transaction Count",
    "TxTfrCnt": "Transfer Transaction Count",
    "TxTfrValAdjNtv": "Adjusted Native Value of Transfers",
    "TxTfrValAdjUSD": "Adjusted USD Value of Transfers",
    "RevUSD": "Revenue in USD",
    "SplyCur": "Current Supply",
    "ROI1yr": "1-Year ROI",
    "VtyDayRet30d": "Volatility (30-Day)"
}

def get_last_date_from_output():
    # Check if the file exists
    if not os.path.exists(output_file):
        return None

    with open(output_file, 'r') as csv_output:
        csv_reader = csv.reader(csv_output)
        last_row = None
        for last_row in csv_reader:
            pass
        if last_row:
            return last_row[0]
    return None

# Download the btc.csv file
download_btc_csv()

last_date_in_output = get_last_date_from_output()

# Read the input CSV file and append to the output CSV file
with open(input_file, 'r') as csv_input, open(output_file, 'a', newline='') as csv_output:
    csv_reader = csv.DictReader(csv_input)
    csv_writer = csv.writer(csv_output)

    # If output.csv is empty, write headers
    if not last_date_in_output:
        csv_writer.writerow(["Column Name", "Explanation"])
        for column, explanation in data_explanations.items():
            csv_writer.writerow([column, explanation])
        csv_writer.writerow(["Date"] + list(data_explanations.keys()))

    for row in csv_reader:
        # Check if 'time' key exists in the row
        if "time" not in row:
            print("Warning: 'time' key not found in a row. Skipping...")
            continue

        # If we have a last date and the current row's date is less than or equal to it, skip
        if last_date_in_output and row["time"] <= last_date_in_output:
            continue

        # Extract selected data points
        extracted_data = extract_data(row)

        # Write the extracted data to the output file
        csv_writer.writerow(extracted_data)

print("Starting downloading 10mb of data")
print("Data extraction completed. Output saved to", output_file)

file_to_remove = input_file
if os.path.exists(file_to_remove):
    os.remove(file_to_remove)
else:
    print(f"The file {file_to_remove} does not exist.")
