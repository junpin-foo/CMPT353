import numpy as np

def RWLTP(totals):
    print("Row with lowest total precipitation:")
    print(np.argmin(np.sum(totals, axis = 1)))

def APIEM(totals, counts):
    print("Average precipitation in each month:")
    print(np.sum(totals, axis = 0) / np.sum(counts, axis = 0))

def APIEC(totals, counts):
    print("Average precipitation in each city:")
    print(np.sum(totals, axis = 1) / np.sum(counts, axis = 1))

def QPT(totals):
    print("Quarterly precipitation totals:")
    quaterly = np.reshape(totals, (36, 3))
    sumQuaterly = np.sum(quaterly, axis = 1)
    print(np.reshape(sumQuaterly, (9,4)))

def main():
    data = np.load('monthdata.npz')
    totals = data['totals']
    counts = data['counts']
    RWLTP(totals)
    APIEM(totals,counts)
    APIEC(totals,counts)
    QPT(totals)

if __name__ == '__main__':
    main()

