import numpy as np
import csv
from colorama import Fore, Style, init
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Initialize Colorama
init()

# Loads the Iris dataset from a CSV file
csv_file_path = r"C:\CODSOFT INTERN\CSV FILES CODSOFT\IRIS.csv"  # Make sure this is the right path to your file

X = []  # This will hold the flower measurements
y = []  # This will hold the flower species names

# Reads the data from the CSV file
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        X.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])  # Measurements
        y.append(row[4].strip())  # Species

# Converts lists to NumPy arrays
X = np.array(X)
y = np.array(y)

# Mapps species names to numbers
species_map = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
species_reverse_map = {v: k for k, v in species_map.items()}
y = np.array([species_map[label] for label in y])

# Splits the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creates the k-NN model
k = 3
knn = KNeighborsClassifier(n_neighbors=k)

# Trains the model
knn.fit(X_train, y_train)

# Makes predictions on the test set
y_pred = knn.predict(X_test)

# Evaluates the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print(Fore.GREEN + f'Accuracy of the model: {accuracy * 100:.2f}%' + Style.RESET_ALL)

# Gets user input for flower measurements
try:
    sepal_length = float(input(Fore.YELLOW + "Enter sepal length: " + Style.RESET_ALL))
    sepal_width = float(input(Fore.YELLOW + "Enter sepal width: " + Style.RESET_ALL))
    petal_length = float(input(Fore.YELLOW + "Enter petal length: " + Style.RESET_ALL))
    petal_width = float(input(Fore.YELLOW + "Enter petal width: " + Style.RESET_ALL))

    # Puts user input into an array
    user_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    # Predicts the species for the user's flower measurements
    predicted_label = knn.predict(user_input)[0]
    species_name = species_reverse_map[predicted_label]  # Convert the number back to a species name
    print(Fore.GREEN + f'The predicted species is: {species_name}' + Style.RESET_ALL)

except ValueError:
    print(Fore.RED + "Oops! Please enter valid numbers for the measurements." + Style.RESET_ALL)
    
