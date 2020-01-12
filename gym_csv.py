import csv

def read_from_data(dic):
    with open('data.csv','r') as f:

        reader = csv.DictReader(f)

        for each in reader:

            dic.setdefault(each['Exercise'], {'Weight':each['Weight'], 'Sets':each['Sets'],
                                              'Reps':each['Reps'],'AMRAP':each['AMRAP']})

def write_to_data(dic):
    with open('data.csv','w') as f:

        field = ['Exercise', 'Weight', 'Sets', 'Reps', 'AMRAP']

        writer = csv.DictWriter(f, fieldnames=field)

        writer.writeheader()

        for a,b in dic.items():
            writer.writerow({field[0]:a, field[1]:b[field[1]], field[2]:b[field[2]],
                             field[3]:b[field[3]], field[4]:b[field[4]]})

if __name__ == '__main__':
    pass
