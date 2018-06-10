import csv


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    with open("arm_groups_descriptions1.sql", "w+") as file:
        file.write("set autocommit=0;\n")
        for row in reader:
            sql = 'INSERT INTO arm_groups_description VALUES("'
            sql += '","'.join([value.replace('"', '\\"') for value in row]) + '");'
            file.write(sql + "\n")
        file.write("commit;")


if __name__ == "__main__":
    csv_path = "arm_groups_descriptions1.csv"
    with open(csv_path, "rb") as f_obj:
        csv_reader(f_obj)
