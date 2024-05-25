import csv

# Define the input and output file paths
input_file_path = "DBMS_unfilter.csv"
output_file_path = "DBMS.csv"

# Open input file for reading and output file for writing
with open(input_file_path, 'r', encoding="utf8") as input_file, open(output_file_path, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    
    # Iterate through the rows in the input file
    for row in reader:

        # Check if the row has less than 10 letters in the "review" column (e.g., column index 1)
      try:
        print(row)
        print(len(row[0]))
        if len(row[0]) >= 10:
              # Write the row to the output file
          writer.writerow(row)
      except:
        pass

print(f"Filtered data has been saved to {output_file_path}.")