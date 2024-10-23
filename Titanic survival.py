import csv
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the Titanic data from CSV
file_path = r"C:\CODSOFT INTERN\CSV FILES CODSOFT\Titanic-Dataset.csv" # <-- Replace with your actual path
data = []

with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Data processing
X = []
y = []

for row in data:
    # Features: Pclass, Sex (convert to numeric), Age, SibSp, Parch, Fare
    if row['Age'] == '':
        row['Age'] = '0'
    if row['Fare'] == '':
        row['Fare'] = '0'

    sex = 1 if row['Sex'] == 'male' else 0
    features = [int(row['Pclass']), sex, float(row['Age']), int(row['SibSp']), int(row['Parch']), float(row['Fare'])]
    X.append(features)
    y.append(int(row['Survived']))

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the logistic regression model and train it
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Predict survival on the test data
y_pred = model.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(Fore.CYAN + f"Model Accuracy: {accuracy * 100:.2f}%" + Style.RESET_ALL)

# Separate survivors and non-survivors for display
survived = defaultdict(list)
not_survived = defaultdict(list)

for row in data:
    if row['Survived'] == '1':
        for key in row.keys():
            survived[key].append(row[key])
    else:
        for key in row.keys():
            not_survived[key].append(row[key])

# Function to print table with borders
def print_table(data_dict, color):
    headers = list(data_dict.keys())
    
    # Print the header
    print(color + "+-" + "-+-".join(['-' * len(header) for header in headers]) + "-+")
    print(color + "| " + " | ".join(headers) + " |")
    print(color + "+-" + "-+-".join(['-' * len(header) for header in headers]) + "-+")

    # Print the data rows
    for i in range(len(data_dict[headers[0]])):
        row = [data_dict[header][i] for header in headers]
        print(color + "| " + " | ".join(row) + " |")
        print(color + "+-" + "-+-".join(['-' * len(header) for header in headers]) + "-+")

# Display details for passengers who survived (in green)
print(Fore.GREEN + "\n--- Passengers Who Survived ---" + Style.RESET_ALL)
print_table(survived, Fore.GREEN)

# Display details for passengers who did not survive (in red)
print(Fore.RED + "\n--- Passengers Who Did Not Survive ---" + Style.RESET_ALL)
print_table(not_survived, Fore.RED)
