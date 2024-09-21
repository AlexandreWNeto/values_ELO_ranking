import csv

# Function to read CSV file and return the data as a list of lists
def read_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

# Function to write data to CSV file
def write_csv(file_name, data):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Function to calculate the expected score
def expected_score(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

# Function to update ELO scores
def update_elo(elo_a, elo_b, result, k=32):
    expected_a = expected_score(elo_a, elo_b)
    expected_b = expected_score(elo_b, elo_a)
    
    new_elo_a = elo_a + k * (result - expected_a)
    new_elo_b = elo_b + k * ((1 - result) - expected_b)
    
    return new_elo_a, new_elo_b

# Read the personal values and comparisons from CSV files
values_list = read_csv('values_list.csv')
comparisons = read_csv('comparisons.csv')

# Initialize ELO scores for each personal value
elo_scores = {value[1]: 1000 for value in values_list[0:]}
print(elo_scores)

# Perform 50 rounds of comparisons
rounds = 50
output_data = [['Personal Value'] + [f'Round {i+1}' for i in range(rounds)]]

for value in values_list[1:]:
    output_data.append([value[1]])

for round_num in range(rounds):
    for comparison in comparisons[1:]:
        value1, value2, result = comparison[0], comparison[1], int(comparison[2])
        print(value1,value2)
        if result == 1:
            elo_scores[value1], elo_scores[value2] = update_elo(elo_scores[value1], elo_scores[value2], 1)
        else:
            elo_scores[value1], elo_scores[value2] = update_elo(elo_scores[value1], elo_scores[value2], 0)
    
    for row in output_data[1:]:
        row.append(round(elo_scores[row[0]],2))

# Write the output data to output.csv
write_csv('output.csv', output_data)

print("ELO scores have been calculated and saved to output.csv.")