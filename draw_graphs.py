import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import Decimal

# configuration data: which results to show on graph
cw_min = 15
cw_max = 1023
N = 10  # number of contending stations
retry_limit = True

if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'
final_results = pd.read_csv(
    f'results/final_results_{cw_min}_{cw_max}_{retry}.csv')

# p_coll graph
# calculation of MSE
MSE_model = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_model'])).mean()
MSE_matlab = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_matlab'])).mean()
MSE_ns3 = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_ns3'])).mean()

plt.figure()
plt.plot(
    final_results['N'],
    final_results['p_coll_simulation'],
    'bo--',
    final_results['N'],
    final_results['p_coll_model'],
    'ro--',
    final_results['N'],
    final_results['p_coll_matlab'],
    'yo--',
    final_results['N'],
    final_results['p_coll_ns3'],
    'co--'
)

plt.title(
    f"Mean probability of collision for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('Number of contending stations')
plt.ylabel('Probability of collision')
plt.legend(['DCF-NumPy', 'Analytical model', 'Matlab simulation', 'ns-3'])
plt.figtext(0.55, 0.3, 'MSE:')
plt.figtext(0.55, 0.25, '* Analytical model: %.4E' % Decimal(MSE_model))
plt.figtext(0.55, 0.2, '* Matlab: %.4E' % Decimal(MSE_matlab))
plt.figtext(0.55, 0.15, '* Ns-3: %.4E' % Decimal(MSE_ns3))
plt.savefig(f'results/graphs/p_coll_result_{cw_min}_{cw_max}_{retry}.png')

# throughput graph

MSE_ns3_thr = np.square(np.subtract(
    final_results['throughput_simulation'], final_results['thr_ns3'])).mean()

thr_sim = final_results['throughput_simulation']
thr_conf = final_results['thr_conf_intervals']
n = final_results['N']
thr_ns3 = final_results['thr_ns3']

fig = plt.figure()
plt.errorbar(x=n, y=thr_sim, yerr=thr_conf, capsize=6, marker='s',
             markersize=5, linestyle='dashed', color='b', mfc='b', mec='b')
plt.errorbar(x=n, y=thr_ns3,yerr=thr_conf, capsize=6, marker='s',
             markersize=5, linestyle='dashed', color='g', mfc='g', mec='g')
plt.title(
    f"Throughput per station for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('Number of contending stations')
plt.ylabel('Throughput [Mb/s]')
legend = plt.legend(['DCF-NumPy', 'ns-3'])

plt.text(0.7, 6, 'MSE: %.4E' % Decimal(MSE_ns3_thr))
plt.ylim(ymin=0, ymax=32)
plt.tight_layout()

plt.savefig(f'results/graphs/throughput_result_{cw_min}_{cw_max}_{retry}.png')
