import pygame
import csv
import itertools
import datetime
import random

# Initialize pygame
pygame.init()

# Set up display
width, height = 1400, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Value Comparison")



# Read the CSV file and store the data
data = []
input_file_name = "values_list.csv"
with open('values_list.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# Generate all cartesian combinations of pairs of values, disregarding the order
pairs = list(itertools.combinations(data, 2))
random.seed(10)
random.shuffle(pairs)

print(len(pairs))

# Function to display text on the screen
def display_text(text, font, colour, x, y):
    text_surface = font.render(text, True, colour)
    window.blit(text_surface, (x, y))

# Function to display a pair of values and their examples
def display_pair(pair, selected = None, remaining = None):
    window.fill((0, 0, 0))
    value1, value2 = pair[0], pair[1]
    
    # Set up font
    font1 = pygame.font.Font(None, 25)
    colour1 = (255,255,255)
    
    font2 = pygame.font.Font(None, 25)
    colour2 = (0,150,255)
    
    display_text(f"Value 1: {value1[1]}", font1, colour1, 25, 50)
    display_text(f"Description: {value1[2]}", font1, colour1, 25, 75)
    display_text(f"Positive:{value1[3]}", font1, colour1, 25, 100)
    display_text(f"Negative:{value1[4]}", font1, colour1, 25, 125)
    
    display_text(f"Value 2: {value2[1]}", font2, colour2, 25, 350)
    display_text(f"Description: {value2[2]}", font2, colour2, 25, 375)
    display_text(f"Positive:{value2[3]}", font2, colour2, 25, 400)
    display_text(f"Negative:{value2[4]}", font2, colour2, 25, 425)
    
    display_text(f"{selected} / {remaining}", font1, colour1, width - 150, 50)
    
    pygame.display.flip()

# Prompt the user to select the starting comparison number
max_index = len(pairs)
start_index = 0
input_active = True
user_input = ""
fontA = pygame.font.Font(None, 30)
colourA = (255,255,255)

while input_active:
    window.fill((0, 0, 0))
    display_text(f"Select the comparison number (from 1 to {max_index}): {user_input}", fontA, colourA, 50, 50)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            input_active = False
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.isdigit() and 1 <= int(user_input) <= max_index:
                    start_index = int(user_input) - 1
                    input_active = False
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

# Main loop
running = True
pair_index = start_index
output_data = []

while running and pair_index < len(pairs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                output_data.append([pairs[pair_index][0][1], pairs[pair_index][1][1], "1"])
                pair_index += 1
            elif event.key == pygame.K_2:
                output_data.append([pairs[pair_index][0][1], pairs[pair_index][1][1], "2"])
                pair_index += 1
    
    if pair_index < len(pairs):
        selected = pair_index
        remaining = len(pairs) - pair_index
        display_pair(pairs[pair_index], selected, remaining)

# Get the current date and time
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Write the output data to a text file with a timestamp in the file name
output_filename = f'output_{current_time}.csv'
with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["First Value", "Last Value", "Favourite Value"])
    writer.writerows(output_data)

# Quit pygame
pygame.quit()