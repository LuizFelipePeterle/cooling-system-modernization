
import numpy as np

rng = np.random.default_rng(20260912)
n = 20000

# Critical-path activity durations in weeks: triangular(min, mode, max)
activities = {
    "A": (2.5,3.0,3.8),
    "B": (2.5,3.0,4.0),
    "C": (2.2,3.0,4.2),
    "D": (2.3,3.0,4.0),
    "E": (6.5,8.0,11.0),
    "H": (3.0,4.0,5.5),
    "I": (2.0,3.0,4.5),
    "J": (2.0,3.0,4.0),
    "K": (1.5,2.0,3.0),
    "L": (0.7,1.0,1.5)
}

samples = np.zeros(n)
for low, mode, high in activities.values():
    samples += rng.triangular(low, mode, high, n)

for p in [50,80,90]:
    print(f"P{p}: {np.percentile(samples,p):.2f} weeks")
print(f"Mean: {samples.mean():.2f} weeks")
