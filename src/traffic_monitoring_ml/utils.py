import pickle
import json
import matplotlib.pyplot as plt

from pathlib import Path

def save_pickle(path: Path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_pickle(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)

def save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f)

def load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)

def get_day_period_from_time(time: str):
    hour = int(time.split(':')[0])
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

def plot_target_dist(x, y):
    fig, ax = plt.subplots(figsize=(6, 4))

    colors = ['#2ecc71', '#e67e22', '#e74c3c']
    bars = ax.bar(
        x,
        y,
        color=colors,
        width=0.5
    )

    ax.set_title('Distribución de severidad de víctimas')
    ax.set_xlabel('Severidad')
    ax.set_ylabel('Porcentaje (%)')

    for bar in bars:
        ax.annotate(f'{bar.get_height():.1f}%',
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha='center', va='bottom', fontsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()