from __future__ import annotations
from pathlib import Path
import json, math
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'data'/'generated'; OUT.mkdir(parents=True,exist_ok=True)
CFG=json.loads((Path(__file__).parent/'data_generation_config.json').read_text())
SEED=CFG['seed']
# independent streams reduce accidental coupling
ss=np.random.SeedSequence(SEED); streams=iter(ss.spawn(20))
def rng(): return np.random.default_rng(next(streams))
R_LOAD,R_COP,R_FAIL,R_REPAIR,R_PM,R_ALARM,R_COST,R_IMP=[rng() for _ in range(8)]
ASSETS=pd.DataFrame([
 ('CH-01','Chiller',400,'HIGH'),('CH-02','Chiller',400,'HIGH'),('CH-03','Chiller',400,'HIGH'),
 ('P-01','Pump',75,'MEDIUM'),('P-02','Pump',75,'MEDIUM'),('P-03','Pump',75,'MEDIUM'),
 ('P-04','Pump',75,'MEDIUM'),('P-05','Pump',75,'MEDIUM'),('P-06','Pump',75,'MEDIUM')],
 columns=['asset_code','asset_type','rated_capacity_kw','criticality'])

def period_index(label,freq='15min'):
 c=CFG['periods'][label]; return pd.date_range(c['start'],pd.Timestamp(c['end'])+pd.Timedelta(days=1),freq=freq,inclusive='left')

def it_load(idx):
 p=CFG['it_load_model']; doy=idx.dayofyear.to_numpy(); hour=(idx.hour+idx.minute/60).to_numpy()
 x=p['base_kw']+p['seasonal_amplitude_kw']*np.sin(2*np.pi*(doy-20)/365.25)+p['daily_amplitude_kw']*np.sin(2*np.pi*(hour-8)/24)+R_LOAD.normal(0,p['noise_sigma_kw'],len(idx))
 return np.clip(x,p['min_kw'],p['max_kw'])

def gen_failures(label):
 idx=period_index(label,'D'); annual=CFG['failure_model'][f'{label}_annual_rate']; lam=annual/len(idx)
 rows=[]; seq=1; eligible=ASSETS.asset_code.to_numpy(); weights=np.array([.20,.20,.20,.0667,.0667,.0667,.0667,.0666,.0666]); weights/=weights.sum()
 for d in idx:
  for _ in range(R_FAIL.poisson(lam)):
   asset=R_FAIL.choice(eligible,p=weights); med=CFG['failure_model']['downtime_lognormal_median_hours'][label]
   down=float(R_REPAIR.lognormal(np.log(med),CFG['failure_model']['downtime_sigma'])); repair=max(.5,down*R_REPAIR.uniform(.60,.92))
   start=d+pd.Timedelta(minutes=int(R_FAIL.integers(0,1440)))
   rows.append({'period':label,'failure_id':f'{label[0].upper()}F{seq:04d}','asset_code':asset,'start_timestamp':start,'end_timestamp':start+pd.Timedelta(hours=down),'downtime_hours':round(down,2),'repair_hours':round(repair,2),'failure_mode':R_FAIL.choice(['bearing','control','sensor','electrical','flow'])}); seq+=1
 return pd.DataFrame(rows)

def capacity_state(label,perf,fail):
 idx=perf.timestamp; state=pd.DataFrame({'period':label,'timestamp':idx})
 state['available_chillers']=3
 if len(fail):
  for _,f in fail[fail.asset_code.str.startswith('CH')].iterrows():
   m=(state.timestamp>=f.start_timestamp)&(state.timestamp<f.end_timestamp); state.loc[m,'available_chillers']-=1
 state['available_chillers']=state.available_chillers.clip(lower=0)
 state['available_cooling_capacity_kw']=state.available_chillers*CFG['assets']['chiller_capacity_kw']
 state['required_cooling_capacity_kw']=perf.cooling_demand_kw.to_numpy()+CFG['thermal_model']['capacity_margin_kw']
 state['capacity_margin_kw']=state.available_cooling_capacity_kw-state.required_cooling_capacity_kw
 state['service_available']=state.capacity_margin_kw>=0
 state['redundancy_state']=np.where(state['capacity_margin_kw']<0,'capacity deficit',np.where(state['available_chillers']>=3,'N+1','N / degraded'))
 return state

def gen_period(label):
 idx=period_index(label); it=it_load(idx); cooling=it*CFG['thermal_model']['it_to_cooling_ratio']+CFG['thermal_model']['other_heat_kw']
 copc=CFG['cop_model']; mean=copc[f'{label}_mean']; cop=np.clip(mean-copc['load_penalty']*((cooling/cooling.mean())-1)+R_COP.normal(0,copc[f'{label}_sigma'],len(idx)),copc['min'],copc['max'])
 interval_h=CFG['telemetry']['performance_interval_minutes']/60
 cooling_kwh=cooling*interval_h; cooling_power=cooling/cop; it_kwh=it*interval_h
 other=CFG['facility_energy_model']['other_facility_kw']; ups_loss=it*CFG['facility_energy_model']['ups_loss_fraction']; facility_power=it+cooling_power+other+ups_loss
 facility_kwh=facility_power*interval_h; pue=facility_power/it
 perf=pd.DataFrame({'period':label,'timestamp':idx,'it_load_kw':it.round(2),'cooling_demand_kw':cooling.round(2),'cooling_energy_kwh':cooling_kwh.round(3),'cooling_electrical_power_kw':cooling_power.round(2),'cooling_electrical_energy_kwh':(cooling_power*interval_h).round(3),'cop':cop.round(4),'facility_power_kw':facility_power.round(2),'facility_energy_kwh':facility_kwh.round(3),'it_energy_kwh':it_kwh.round(3),'pue':pue.round(4)})
 fail=gen_failures(label); cap=capacity_state(label,perf,fail)
 # excursions tied partly to deficit/degraded conditions plus residual stochastic rate
 days=pd.date_range(idx.min().normalize(),idx.max().normalize(),freq='D'); annual=CFG['excursion_model'][f'{label}_annual_rate']; n=R_ALARM.poisson(annual); choices=R_ALARM.choice(days,size=n,replace=True) if n else []
 ex=pd.DataFrame([{'period':label,'event_id':f'{label[0].upper()}T{i+1:04d}','date':pd.Timestamp(d).date(),'peak_deviation_c':round(float(R_ALARM.lognormal(np.log(.8 if label=='baseline' else .55),.35)),2),'duration_min':round(float(R_ALARM.lognormal(np.log(40 if label=='baseline' else 22),.5)),1)} for i,d in enumerate(choices)])
 # PM
 months=pd.period_range(idx.min(),idx.max(),freq='M'); pm=[]; seq=1; eligible=ASSETS.asset_code.iloc[:6]
 for m in months:
  for a in eligible:
   planned=m.start_time+pd.Timedelta(days=int(R_PM.integers(0,20))); completed=bool(R_PM.random()<CFG['pm_model']['completion_probability'][label]); cd=planned+pd.Timedelta(days=int(R_PM.integers(0,8))) if completed else pd.NaT
   pm.append({'period':label,'work_order_id':f'{label[0].upper()}PM{seq:04d}','asset_code':a,'planned_date':planned.date(),'completed_date':'' if pd.isna(cd) else cd.date(),'completed':completed}); seq+=1
 pm=pd.DataFrame(pm)
 # alarms monthly Poisson-ish
 alarms=[]; aid=1
 for m in months:
  cnt=R_ALARM.poisson(CFG['alarm_model'][f'{label}_monthly_mean'])
  for _ in range(cnt):
   d=m.start_time+pd.Timedelta(days=int(R_ALARM.integers(0,m.days_in_month)),minutes=int(R_ALARM.integers(0,1440)))
   alarms.append({'period':label,'alarm_id':f'{label[0].upper()}A{aid:05d}','timestamp':d,'asset_code':R_ALARM.choice(ASSETS.asset_code),'priority':R_ALARM.choice(['HIGH','MEDIUM'],p=[.72,.28])}); aid+=1
 alarms=pd.DataFrame(alarms)
 # costs from energy + maintenance/failure events
 costs=[]; cc=CFG['cost_model']
 for m in months:
  op=perf[perf.timestamp.dt.to_period('M')==m]; fm=fail[pd.to_datetime(fail.start_timestamp).dt.to_period('M')==m] if len(fail) else fail; pm_m=pm[pd.to_datetime(pm.planned_date).dt.to_period('M')==m]
  energy=float(op.cooling_electrical_energy_kwh.sum()*cc['baseline_energy_eur_per_kwh']); labor=(float(pm_m.completed.sum())*cc['preventive_labor_hours_per_completed_order']+(float(fm.repair_hours.sum()) if len(fm) else 0))*cc['labor_eur_per_hour']; parts=emerg=0
  for _ in range(len(fm)):
   part=float(R_COST.lognormal(np.log(cc['parts_cost_lognormal_median_eur'][label]),cc['parts_cost_lognormal_sigma'])); parts+=part
   if R_COST.random()<cc['emergency_procurement_probability'][label]: emerg+=part*(cc['emergency_parts_markup']-1)
  svc=cc['planned_service_contract_monthly_eur']; total=energy+labor+parts+emerg+svc
  costs.append({'period':label,'month':str(m),'energy_cost_eur':round(energy,2),'labor_cost_eur':round(labor,2),'parts_cost_eur':round(parts,2),'emergency_parts_cost_eur':round(emerg,2),'service_contract_cost_eur':round(svc,2),'total_om_cost_eur':round(total,2)})
 return perf,fail,pm,alarms,ex,pd.DataFrame(costs),cap

def imperfect(df):
 out=df.copy(); imp=CFG['imperfections']; cols=['it_load_kw','cooling_demand_kw','cooling_electrical_energy_kwh','cop','pue']
 for c in cols:
  m=R_IMP.random(len(out))<imp['sensor_missing_rate']; out.loc[m,c]=np.nan
 dup=R_IMP.random(len(out))<imp['duplicate_rate']; return pd.concat([out,out.loc[dup]],ignore_index=True).sort_values('timestamp').reset_index(drop=True)

res={p:gen_period(p) for p in ('baseline','post')}
pd.concat([imperfect(res[p][0]) for p in res]).to_csv(OUT/'performance_telemetry_raw.csv',index=False)
pd.concat([res[p][1] for p in res]).to_csv(OUT/'failures.csv',index=False)
pd.concat([res[p][2] for p in res]).to_csv(OUT/'maintenance_orders.csv',index=False)
pd.concat([res[p][3] for p in res]).to_csv(OUT/'alarms.csv',index=False)
pd.concat([res[p][4] for p in res]).to_csv(OUT/'temperature_excursions.csv',index=False)
pd.concat([res[p][5] for p in res]).to_csv(OUT/'om_costs.csv',index=False)
pd.concat([res[p][6] for p in res]).to_csv(OUT/'cooling_capacity_state.csv',index=False)
# minute monitoring completeness dataset: compact daily summary instead of 1M raw rows
mon=[]
for p in ('baseline','post'):
 for d in period_index(p,'D'):
  expected=1440; observed=int(round(expected*(1-CFG['imperfections']['sensor_missing_rate'])+R_IMP.normal(0,2))); observed=max(0,min(expected,observed)); mon.append({'period':p,'date':pd.Timestamp(d).date(),'expected_1min_samples':expected,'observed_1min_samples':observed,'completeness_pct':round(100*observed/expected,4)})
pd.DataFrame(mon).to_csv(OUT/'monitoring_completeness_daily.csv',index=False)
ASSETS.to_csv(OUT/'assets.csv',index=False)
print('NDC-01 synthetic evidence generated.')
# Diagnostics are calculated from the persisted, imperfected evidence using the
# same paired-observation methodology as the official Python crosscheck.
from kpi_calculations import calculate_kpis
_diag=calculate_kpis(OUT)
for _,r in _diag.iterrows():
 print(r['period'], 'failures=',int(r['failures']),
       'equipment_downtime_h=',round(r['equipment_downtime_h'],1),
       'service_availability_pct=',round(r['cooling_service_availability_pct'],5),
       'degraded_h=',round(r['degraded_redundancy_h'],2),
       'paired_weighted_COP=',round(r['weighted_cop'],4),
       'paired_COP_obs=',int(r['paired_cop_observations']),
       'paired_COP_pct=',round(r['paired_cop_observation_pct'],3),
       'PUE=',round(r['pue'],4),
       'PM=',round(r['pm_compliance_pct'],2),
       'O&M=',round(r['om_cost_eur'],2))
