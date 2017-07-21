import glob
import pandas

def get_col_labels(labels):
    col_labels = []

    for i in range(len(labels)-1):
        #  print(labels[0:i+1])
        #  col_labels.append(labels[0:i+1])
        col_labels.extend(labels[0:i+1])

    return col_labels

def get_row_labels(labels):
    row_labels = []

    for i,label in enumerate(labels):
        for _ in range(i):
            row_labels.append(label)
    return row_labels

def clean_list(input_list):

    new_list = []
    for item in input_list:
        item = item.strip("()")
        new_list.append(float(item))

    return new_list

def process_file(file_path):

    data_file = open(file_path, "r")
    data_lines = []
    dn_over_ds = []
    dn = []
    ds = []
    labels = []

    for i, line in enumerate(data_file):
        if line.strip() == "Nei & Gojobori 1986. dN/dS (dN, dS)":
            data_lines = list(range(i+4, i+8))

        if i in data_lines:
            line = line.split()
            label = line[0]
            labels.append(label)
            line = line[1:]

            # Convert the list of strings to a list of ints
            # this requires removing any parentheses in the strings
            line = clean_list(line)

            #The first value on the line is dn/ds
            # every third value after that is dn/ds
            for j in range(0, len(line), 3):
                dn_over_ds.append(line[j])

            #The second value on the line is dn
            # every third value after that is also dn
            for j in range(1, len(line), 3):
                dn.append(line[j])

            for j in range(2, len(line), 3):
                ds.append(line[j])

    row_labels = get_row_labels(labels)
    col_labels = get_col_labels(labels)
    data_file.close()
    data_dict = {"dn":dn, "ds":ds, "dn/ds":dn_over_ds,
             "row_label":row_labels, "col_label":col_labels}
    dn_ds_data = pandas.DataFrame(data_dict)
    return dn_ds_data

file_list = glob.glob("intermediatefiles/*/*.model2")
data_frames = []

for filename in file_list:
    try:
        data_frames.append(process_file(filename))
    except:
        print("There's something wrong with", filename)

print(pandas.concat(data_frames))
