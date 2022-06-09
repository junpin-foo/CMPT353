import pandas as pd

def lowest(totals):
    print("City with lowest total precipitation:")
    Aftersum = pd.DataFrame.sum(totals, axis = 1)
    print(Aftersum.idxmin())

def averageMonth(totals,counts):
    print("Average precipitation in each month:")
    print(totals.mean(axis = 0) / counts.mean(axis = 0))

def averageCity(totals,counts):
    print("Average precipitation in each city:")
    print(totals.sum(axis = 1) / counts.sum(axis = 1))

def main():
    totals = pd.read_csv('totals.csv').set_index(keys=['name'])
    counts = pd.read_csv('counts.csv').set_index(keys=['name'])
    lowest(totals)
    averageMonth(totals, counts)
    averageCity(totals,counts)

if __name__ == '__main__':
    main()

