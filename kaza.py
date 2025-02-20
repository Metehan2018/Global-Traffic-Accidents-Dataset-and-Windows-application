import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('global_traffic_accidents.csv')

# Check for missing values and fill them
data['Casualties'].fillna(data['Casualties'].mean(), inplace=True)

# Translate Turkish terms to English
weather_mapping = {
    'Açık': 'Clear', 'Yağmurlu': 'Rain', 'Karlı': 'Snow',
    'Sisli': 'Fog', 'Fırtınalı': 'Storm', 'Dolu': 'Hail'
}
road_mapping = {
    'Kuru': 'Dry', 'Islak': 'Wet', 'Buzlu': 'Icy',
    'Karlı': 'Snowy', 'Çakıllı': 'Gravel', 'Yapım Aşamasında': 'Under Construction'
}
cause_mapping = {
    'Tehlikeli Sürüş': 'Reckless Driving', 'Sarhoş Sürüş': 'Drunk Driving',
    'Hava Koşulları': 'Weather Conditions', 'Dikkatsiz Sürüş': 'Distracted Driving',
    'Mekanik Arıza': 'Mechanical Failure', 'Aşırı Hız': 'Speeding'
}

data['Weather Condition'] = data['Weather Condition'].map(weather_mapping)
data['Road Condition'] = data['Road Condition'].map(road_mapping)
data['Cause'] = data['Cause'].map(cause_mapping).fillna(data['Cause'])

# Translate country names to English
country_mapping = {
    'Hindistan': 'India', 'Brezilya': 'Brazil', 'Avustralya': 'Australia',
    'Japonya': 'Japan', 'Çin': 'China', 'Fransa': 'France',
    'İngiltere': 'UK', 'Kanada': 'Canada', 'Almanya': 'Germany',
    'ABD': 'USA'
}

data['Location'] = data['Location'].apply(lambda x: ', '.join(
    [country_mapping.get(part.strip(), part.strip()) for part in x.split(',')]
))

# Create main window
def main_gui():
    def show_graph():
        country_name = entry.get().strip()
        if not country_name:
            result_label.config(text="Please enter a valid country name.", fg="red")
            return
        
        # Filter data based on country name
        filtered_data = data[data['Location'].str.contains(country_name, case=False, na=False)]
        if filtered_data.empty:
            result_label.config(text=f"No accident information found for {country_name}.", fg="red")
            return
        
        # Clear previous graph
        for widget in graph_frame.winfo_children():
            widget.destroy()
        
        # Distribution of causes of accidents
        cause_distribution = filtered_data['Cause'].value_counts().reset_index()
        cause_distribution.columns = ['Cause', 'Number of Accidents']
        
        # Create graph with Matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.barh(cause_distribution['Cause'], cause_distribution['Number of Accidents'], color='skyblue')
        ax.set_title(f"Distribution of Causes of Accidents in {country_name}", fontsize=14)
        ax.set_xlabel("Number of Accidents", fontsize=12)
        ax.set_ylabel("Causes of Accidents", fontsize=12)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Write numbers on the bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, f'{int(width)}', ha='left', va='center', fontsize=10)
        
        # Add the graph to the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Update result message
        result_label.config(text=f"Graph successfully created for {country_name}.", fg="green")

    # Main window
    root = tk.Tk()
    root.title("Accident Information Application")
    root.geometry("1200x800")

    # Top frame (Country name entry and button)
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10, fill=tk.X)

    tk.Label(input_frame, text="Enter Country Name:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    entry.pack(side=tk.LEFT, padx=5)
    entry.bind("<Return>", lambda event: show_graph())  # Trigger when Enter key is pressed

    tk.Button(input_frame, text="Show", command=show_graph, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    # Result message
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack(pady=5)

    # Graph frame
    graph_frame = tk.Frame(root)
    graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()

# Start the program
if __name__ == "__main__":
    main_gui()
