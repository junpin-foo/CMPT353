
import sys
import pandas as pd
import numpy as np
from scipy import stats

filename1 = sys.argv[1]
data = pd.read_json(filename1, orient='records', lines=True) 

data.loc[data['uid'] % 2 == 0, 'odd/even'] = 'Even' 
data.loc[data['uid'] % 2 != 0, 'odd/even'] = 'Odd' #new UI
data.loc[data['search_count'] == 0, 'searched_never/at_least_once'] = 'Never'
data.loc[data['search_count'] != 0, 'searched_never/at_least_once'] = 'At_least_once'

contingency = pd.crosstab(data['searched_never/at_least_once'], data['odd/even'])
chi2, p, dof, expected = stats.chi2_contingency(contingency)

data_odd = data.loc[data['odd/even'] == 'Odd']
data_even = data.loc[data['odd/even'] == 'Even']

utest = (stats.mannwhitneyu(data_odd['search_count'], data_even['search_count'], alternative='two-sided').pvalue)

data_inst = data.loc[data['is_instructor'] == True]

contingency2 = pd.crosstab(data_inst['odd/even'], data_inst['searched_never/at_least_once'])
chi2, p2, dof, expected = stats.chi2_contingency(contingency2)

data_odd2 = data_inst.loc[data_inst['odd/even'] == 'Odd']
data_even2 = data_inst.loc[data_inst['odd/even'] == 'Even']
utest2 = (stats.mannwhitneyu(data_odd2['search_count'], data_even2['search_count'], alternative='two-sided').pvalue)



OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    # ...

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p= p,
        more_searches_p= utest,
        more_instr_p= p2,
        more_instr_searches_p= utest2,
    ))


if __name__ == '__main__':
    main()
