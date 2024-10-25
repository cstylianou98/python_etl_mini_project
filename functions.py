import matplotlib.pyplot as plt



def plot_temp_graphs(date ,temp_tuple, folder_path, file_names, legend_names):
    for temp_i in range(len(temp_tuple)):
        plt.figure(figsize=(12,6))
        plt.plot(date, temp_tuple[temp_i], label = f'{legend_names[temp_i]} Temperature')
        plt.xlabel('Date')
        plt.ylabel('Daily Temperature (°C)')
        plt.title(f'Daily {legend_names[temp_i]} Temperature Over Year 1998-1999')
        plt.legend(loc='lower right')
        plt.xticks(rotation=45)  # Rotate dates for better readability
        plt.tight_layout()
        plt.savefig(f'{folder_path}/{file_names[temp_i]}.png')
        plt.close()


