# import numpy as np
import pandas as pd

from IPython.display import display


def proc_revenues(num_f):
    tags_set = set(num_f['tag'])
    tags_w_rev = [i for i in tags_set if 'revenue' in i.lower() or 'sales' in i.lower()]
    # print('len(tags_w_rev)',len(tags_w_rev))
    revs = num_f[num_f['tag'].isin(tags_w_rev)]
    revs_piv = revs.pivot_table(columns='tag',index='adsh',values='value')

    final_revenue_flds = ['RevenueFromContractWithCustomerExcludingAssessedTax','Revenue',
            'RevenueFromContractsWithCustomers',
            'Revenues', 'NetRevenues1','GrossRevenue','TotalRevenuesFromReportableSegments',
            'BusinessAcquisitionsProFormaRevenue','GrossOperatingAndOtherRevenue',
            'RevenueFromContractWithCustomerIncludingAssessedTax',
            'TotalRevenue','ConsolidatedRevenues','RevenueNet','GrossSales',
            'NetSales',]
    final_revenue_flds_pres = [i for i in final_revenue_flds if i in list(revs_piv.columns)]
    revs_piv['MAX_COL'] = revs_piv[final_revenue_flds_pres].idxmax(axis=1)
    revs_piv['Revenues_FINAL'] = revs_piv[final_revenue_flds_pres].max(axis=1)

    return revs_piv


def proc_income(num_f):
    inc_prelim = num_f[( num_f['tag'] == 'NetIncomeLoss') &
                        (num_f['coreg'].isna()) &
                        (num_f['uom'] == 'USD')]
    incomes = inc_prelim.pivot_table(columns='tag',index='adsh',values='value')
    
    return incomes


def load_and_proc_sub(year_qtr_key):
    sub = pd.read_csv(f'data/{year_qtr_key}/sub.txt', delimiter='	')
    sub_proc = sub[['adsh','name','instance']]
    sub_proc['ticker'] = sub_proc['instance'].str.split('-').str[0].str.upper()
    sub_proc = sub_proc.drop('instance',axis=1)

    return sub_proc


def proc_rev_inc_names(rev_inc, sub_proc, num_f):
    rev_inc_names = rev_inc.join(sub_proc.set_index('adsh'))
    for col in ['Revenues_FINAL', 'NetIncomeLoss']:
        rev_inc_names[col] = rev_inc_names[col] / 1e9

    rev_inc_names['ddate'] = num_f['ddate'].iloc[0]
    rev_inc_names['ddate_dt'] = pd.to_datetime(rev_inc_names['ddate'],  
                                                format='%Y%m%d')

    return rev_inc_names