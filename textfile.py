import pandas as pd

# this is the one the will changed the merged csv file into a text file with the proper annotation merged_dataset/image1.png "label"
df = pd.read_csv('merged_file.csv', header=None)
df = df[[0,1]]
df.columns = ['image_path', 'label']
df['image_path'] = df['image_path'].apply(lambda x: 'merged_dataset/' + x.split('/')[-1])

with open('formatted_dataset.txt', 'w') as file:
    for index, row in df.iterrows():
        file.write(f"{row['image_path']} {row['label']}\n")

print("textfile has been created")

# this is the code to change the enye data set into merged_dataset/image1.png "label"

with open('image_labels.txt', 'r', encoding='utf-8') as infile, open('second_textfile.txt','w',encoding='utf-8') as outfile:
    for line in infile:
        parts = line.strip().split()
        image_path = 'merged_dataset/' + parts[0]
        label = parts[1]
        outfile.write(f"{image_path} {label}\n")

with open('formatted_dataset.txt','r',encoding='utf-8') as file1, \
     open('second_textfile.txt','r', encoding='utf-8') as file2, \
     open('merged_dataset.txt','w', encoding='utf-8') as outfile:
    
    outfile.writelines(file1.readlines())
    outfile.writelines(file2.readlines())
