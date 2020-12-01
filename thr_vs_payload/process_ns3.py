import pandas as pd
import sys
from helpers import conf_intervals

sys.path.append('helpers')

ns3_dt = pd.read_csv('thr_vs_payload/ns3_raw.csv')

# calculating confidance intervals
thr_yerr = conf_intervals.confidence_intervals(
    results=ns3_dt, field='thr_ns3', key='payload')
# grouping the runs with the same payload
ns3_dt = ns3_dt.groupby(
    'payload')['thr_ns3'].mean().reset_index(name='thr_ns3')
# adding conf intervals to results
ns3_dt = ns3_dt.merge(thr_yerr, on='payload', suffixes=('', '_conf'))

ns3_dt.to_csv('thr_vs_payload/ns3.csv')
