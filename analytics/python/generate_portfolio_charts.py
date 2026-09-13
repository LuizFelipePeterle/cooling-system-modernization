from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'data'/'generated'; O=ROOT/'results'/'charts'; O.mkdir(parents=True,exist_ok=True)
k=pd.read_csv(D/'python_kpi_crosscheck.csv').set_index('period')

def save_bar(metric,title,ylabel,name):
    fig,ax=plt.subplots(figsize=(7,4))
    vals=[k.loc['baseline',metric],k.loc['post',metric]]
    ax.bar(['Baseline','Post'],vals)
    ax.set_title(title); ax.set_ylabel(ylabel); ax.grid(axis='y',alpha=.2)
    fig.tight_layout(); fig.savefig(O/name,dpi=180); plt.close(fig)

save_bar('equipment_downtime_h','Equipment downtime - Before vs After','Hours','equipment_downtime.png')
save_bar('degraded_redundancy_h','Time outside intended N+1 state','Hours','redundancy_exposure.png')
save_bar('capacity_deficit_h','Cooling-capacity deficit exposure','Hours','capacity_deficit.png')
save_bar('om_cost_eur','Annual cooling O&M','EUR','om_cost.png')

perf=pd.read_csv(D/'performance_telemetry_raw.csv',parse_dates=['timestamp'])
perf=perf.sort_values(['period','timestamp']).drop_duplicates(['period','timestamp'])
perf['month']=perf.timestamp.dt.to_period('M').astype(str)
# Monthly COP uses the same paired-energy methodology as the official KPI.
rows=[]
for (period,month),g in perf.groupby(['period','month']):
    cp=g[['cooling_energy_kwh','cooling_electrical_energy_kwh']].dropna()
    pp=g[['facility_energy_kwh','it_energy_kwh']].dropna()
    rows.append({'period':period,'month':month,
                 'weighted_cop':cp.cooling_energy_kwh.sum()/cp.cooling_electrical_energy_kwh.sum(),
                 'weighted_pue':pp.facility_energy_kwh.sum()/pp.it_energy_kwh.sum()})
m=pd.DataFrame(rows)
for metric,ylabel,name in [('weighted_cop','Weighted COP','cop_monthly.png'),('weighted_pue','Weighted PUE','pue_monthly.png')]:
    fig,ax=plt.subplots(figsize=(9,4))
    for p,g in m.groupby('period'):
        g=g.sort_values('month')
        ax.plot(range(len(g)),g[metric],label=p.capitalize())
    ax.set_title(f'Monthly {ylabel}'); ax.set_ylabel(ylabel); ax.set_xlabel('Month within observation period')
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(O/name,dpi=180); plt.close(fig)

f=pd.read_csv(D/'failures.csv')
counts=f.groupby(['period','failure_mode']).size().unstack(fill_value=0).T
fig,ax=plt.subplots(figsize=(8,4)); counts.plot(kind='bar',ax=ax)
ax.set_title('Failure modes - Before vs After'); ax.set_ylabel('Events')
fig.tight_layout(); fig.savefig(O/'failure_modes.png',dpi=180); plt.close(fig)
print(f'Portfolio charts written to {O}')
