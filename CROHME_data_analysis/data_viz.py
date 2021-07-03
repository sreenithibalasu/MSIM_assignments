import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import numpy as np
import random
import os
import math

with open('config.json') as f:
    config = json.load(f)

# Plot 1 - Random labels

print("\nGenerating Plot with Random Labels....")
number_of_samples = config["number_of_samples"]
cols_numb = config["number_of_columns"]
save_dir = config["save_dir"]

rows_numb = math.ceil(number_of_samples / cols_numb)

figure, axis_arr = plt.subplots(rows_numb, cols_numb, figsize=(20, 4))
figure.patch.set_facecolor((0.91, 0.91, 0.91))

sample_id = 0
for row in range(rows_numb):
    for col in range(cols_numb):

        if sample_id < number_of_samples:
            label_choice = random.choice(os.listdir(save_dir + '/extracted_images'))
            image_choice = random.choice(os.listdir(save_dir + '/extracted_images/' + label_choice))

            img = mpimg.imread(save_dir + '/extracted_images/' + label_choice + '/' + image_choice)
            axis_arr[row, col].imshow(img, cmap='gray')
            axis_arr[row, col].set_title('Class: \"' + label_choice + '\"', size=13, y=2)

        axis_arr[row, col].axis('off')
        sample_id += 1

figure.subplots_adjust(hspace=2, wspace=10)
figure.savefig(save_dir + '/random_labels.jpeg')

print("\nPlot saved as random_labels.jpeg in ", save_dir)


# Plot 2 - Data Distribution
print("Generating Label Distribution plot ....")
label_counts = {}
for label in os.listdir(save_dir + '/extracted_images'):

    c = 0

    label_path = save_dir + '/extracted_images/' + label
    label_path.encode('UTF-8')

    for png in os.listdir(label_path):
        c += 1

    label_counts[label] = c

sorted_label_counts = {k: v for k, v in sorted(label_counts.items(), key=lambda item: item[1], reverse=True)}
y_pos = np.arange(len(sorted_label_counts.keys()))

fig, ax = plt.subplots(figsize=(50, 50))


ax.barh(y_pos, sorted_label_counts.values())
ax.set_yticks(y_pos)
ax.set_yticklabels(sorted_label_counts.keys())
ax.autoscale()
plt.title('LABEL DISTRIBUTIONS')
plt.xlabel('COUNT')
plt.ylabel('LABELS')

for i, v in enumerate(sorted_label_counts.values()):
    ax.text(v + 3, i + .25, str(v), fontweight='bold')

fig.savefig(save_dir + "/label_distribution.jpeg")

print("\nPlot saved as label_distribution.jpeg in " ,save_dir)
