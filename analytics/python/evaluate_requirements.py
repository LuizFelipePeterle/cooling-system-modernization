from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'data'/'generated'
E=ROOT/'engineering'
R=ROOT/'results'
R.mkdir(exist_ok=True)
kpi=pd.read_csv(D/'python_kpi_crosscheck.csv').set_index('period')
req=pd.read_csv(E/'requirements_traceability.csv')
cap=pd.read_csv(D/'cooling_capacity_state.csv')
mon=pd.read_csv(D/'monitoring_completeness_daily.csv')
rows=[]
for _,q in req.iterrows():
    rid=q.requirement_id
    status='NOT EVALUATED'; measured=''; criterion=q.acceptance_criterion; evidence=''
    if rid=='SYS-CAP-001':
        measured=float(kpi.loc['post','cooling_service_availability_pct']); status='PASS' if measured>=99.95 else 'FAIL'; evidence='python_kpi_crosscheck.csv'
    elif rid=='SYS-RED-001':
        post=cap[cap.period=='post']; ok=post[['redundancy_state','capacity_margin_kw']].notna().all().all(); measured=f"{len(post)} / {len(post)} 15-min intervals populated" if ok else 'missing intervals/fields'; status='PASS' if ok else 'FAIL'; evidence='cooling_capacity_state.csv'
    elif rid=='SYS-MNT-001':
        measured=float(kpi.loc['post','pm_compliance_pct']); status='PASS' if measured>=95 else 'FAIL'; evidence='python_kpi_crosscheck.csv'
    elif rid=='SYS-ENE-001':
        measured=float(kpi.loc['post','weighted_cop']); status='PASS' if measured>=3.30 else 'FAIL'; evidence='python_kpi_crosscheck.csv (paired observations)'
    elif rid=='SYS-PUE-001':
        measured=float(kpi.loc['post','pue']); status='PASS' if measured<=1.50 else 'FAIL'; evidence='python_kpi_crosscheck.csv'
    elif rid=='SYS-MON-001':
        post=mon[mon.period=='post']; measured=float(post.completeness_pct.min()); status='PASS' if measured>=95 else 'FAIL'; evidence='monitoring_completeness_daily.csv (minimum daily completeness)'
    elif rid=='SYS-SEC-001':
        f=E/'security_architecture_review.md'; ok=f.exists() and 'ACCEPTED' in f.read_text(); measured='Accepted simulated design review' if ok else 'No accepted review artifact'; status='PASS' if ok else 'FAIL'; evidence='engineering/security_architecture_review.md'
    rows.append({'requirement_id':rid,'target_kpi':q.target_kpi,'acceptance_criterion':criterion,'measured_result':measured,'status':status,'evidence_source':evidence})
out=pd.DataFrame(rows)
out.to_csv(R/'verification_results.csv',index=False)
print(out[['requirement_id','status','measured_result']].to_string(index=False))
if (out.status=='FAIL').any():
    raise SystemExit('Requirement verification contains FAIL results. See results/verification_results.csv')
print('Requirement verification completed: all mapped v6 requirements PASS.')
