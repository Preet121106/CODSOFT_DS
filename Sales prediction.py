import numpy as np
import matplotlib.pyplot as plt
import csv

#CSV filep path
csv_file_path = r"C:\CODSOFT INTERN\CSV FILES CODSOFT\advertising.csv"

# Initializes lists to store data for each advertising medium and sales
tv_ad_spend = []
radio_ad_spend = []
newspaper_ad_spend = []
sales_figures = []

# Reads data from the CSV file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        tv_ad_spend.append(float(row[0]))          # TV ad spending
        radio_ad_spend.append(float(row[1]))       # Radio ad spending
        newspaper_ad_spend.append(float(row[2]))   # Newspaper ad spending
        sales_figures.append(float(row[3]))        # Sales figures

# Converts lists into NumPy arrays for easier calculations
tv_ad_spend = np.array(tv_ad_spend)
radio_ad_spend = np.array(radio_ad_spend)
newspaper_ad_spend = np.array(newspaper_ad_spend)
sales_figures = np.array(sales_figures)

# Normalizes the data (scale to 0 to 1)
tv_ad_spend /= np.max(tv_ad_spend)
radio_ad_spend /= np.max(radio_ad_spend)
newspaper_ad_spend /= np.max(newspaper_ad_spend)
sales_figures /= np.max(sales_figures)

# Calculates growth rates (percentage change)
tv_growth_rate = np.diff(tv_ad_spend) / np.where(tv_ad_spend[:-1] != 0, tv_ad_spend[:-1], 1) * 100
radio_growth_rate = np.diff(radio_ad_spend) / np.where(radio_ad_spend[:-1] != 0, radio_ad_spend[:-1], 1) * 100
newspaper_growth_rate = np.diff(newspaper_ad_spend) / np.where(newspaper_ad_spend[:-1] != 0, newspaper_ad_spend[:-1], 1) * 100
sales_growth_rate = np.diff(sales_figures) / np.where(sales_figures[:-1] != 0, sales_figures[:-1], 1) * 100

# Creates subplots to visualize growth trends
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Graph 1: Growth trends for each advertising medium
axes[0].plot(tv_growth_rate, label='TV Growth', color='blue')
axes[0].plot(radio_growth_rate, label='Radio Growth', color='green')
axes[0].plot(newspaper_growth_rate, label='Newspaper Growth', color='orange')
axes[0].plot(sales_growth_rate, label='Sales Growth', color='red')
axes[0].axhline(0, color='black', linewidth=0.5)  # Horizontal line at zero for reference
axes[0].set_title('Growth Rate Trends')
axes[0].set_xlabel('Data Points')
axes[0].set_ylabel('Growth Rate (%)')
axes[0].legend()

# Prepares data for linear regression model
X = np.c_[np.ones(tv_ad_spend.shape[0]), tv_ad_spend, radio_ad_spend, newspaper_ad_spend]
y = sales_figures

# Calculates linear regression parameters (coefficients)
theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

# Makes predictions based on the regression model
predicted_sales = X.dot(theta)

# Graph 2: Actual sales vs predicted sales
axes[1].scatter(np.arange(len(sales_figures)), sales_figures, color='blue', label='Actual Sales')
axes[1].plot(np.arange(len(predicted_sales)), predicted_sales, color='red', label='Predicted Sales')
axes[1].set_title('Actual vs Predicted Sales')
axes[1].set_xlabel('Data Points')
axes[1].set_ylabel('Normalized Sales')
axes[1].legend()

# Displays both graphs side by side
plt.tight_layout()
plt.show()

# Evaluates the model using Mean Squared Error (MSE)
mse = np.mean((predicted_sales - y) ** 2)
print(f'Mean Squared Error: {mse:.2f}')

# Analyzes potential reasons behind the growth trends
print("Analysis of growth trends:")
print("- Increases in TV or radio spending likely indicate higher advertising budgets.")
print("- A decline in newspaper growth may suggest a shift towards digital advertising.")
print("- Sales growth generally mirrors trends in TV and radio advertising, indicating their impact on consumer behavior.")
print("- Spikes or drops in data could be influenced by economic factors or seasonal marketing strategies.")
