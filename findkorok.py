import os
import sys
KOROK_COUNT = {
	"C": 89,
	"P": 18,
	"L": 92,
	"D": 59,
	"F": 58,
	"N": 66,
	"Z": 62,
	"E": 45,
	"K": 35,
	"A": 57,
	"X": 25,
	"T": 37,
	"G": 36,
	"W": 68,
	"H": 73,
	"R": 80,
}

def make_data():
    data = {}
    for region in KOROK_COUNT:
        data[region] = {}
        for i in range(KOROK_COUNT[region]+1):
            if i == 0:
                continue
            if i > 9:
                stri = str(i)
            else:
                stri = "0" + str(i)
            data[region][stri] = False
    return data

def search_file(file_path, data, duplicates):
    with open(file_path, "r") as f:
        for line in f:
            i = line.find("_Korok::")
            if i > 0:
                code = line[i+8:i+11]
                # print(code)
                region = code[0]
                if region not in data:
                    print(f"Error in {file_path}: {line}: invalid region {region}")
                    continue
                id = code[1:3]
                if id not in data[region]:
                    print(f"Error in {file_path}: {line}: invalid id {id}")
                    continue
                
                if data[region][str(id)]:
                    duplicates.append(code)
                data[region][str(id)] = True

def report(data, duplicates):
    if len(duplicates) > 0:
        print("Potentially duplicated koroks")
        for d in duplicates:
            print(d)
    else:
        print("Cannot seem to find any duplicate koroks")
    missing = []
    for region in data:
        for id in data[region]:
            if not data[region][id]:
                missing.append(region+id)
    if len(missing) > 0:
        print("Potentially missing koroks:")
        for d in missing:
            print(d)
    else:
        print("Cannot seem to find any missing koroks")

def search_path(file_path, data, duplicates):
    if os.path.isdir(file_path):
        for subpath in os.listdir(file_path):
            if subpath != "bundle.json":
                search_path(os.path.join(file_path, subpath), data, duplicates)
    elif os.path.isfile(file_path):
        print(f"Scanning {file_path}")
        search_file(file_path, data, duplicates)

def run(arg):
    data = make_data()
    # print(data)
    duplicates = []
    search_path(arg, data, duplicates)
    report(data, duplicates)

run(sys.argv[1])
