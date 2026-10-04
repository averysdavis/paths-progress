import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

# chart style
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, MUTED = "#0b0b0b", "#52514e"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": "#e4e3df", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150,
})

df = pd.read_csv("country_changes_1990_2019.csv", index_col="Code")

#figure 1: og data, not new
le = pd.read_csv("life-expectancy-hmd-unwpp/life-expectancy-hmd-unwpp.csv")
le.columns = ["Entity", "Code", "Year", "LE"]
le = le[(le["Year"] >= 1990) & (le["Year"] <= 2019)]

countries = {"Malawi": BLUE, "Lesotho": ORANGE, "United States": AQUA, "China": YELLOW}
# US and China end close together, so push their labels apart
label_shift = {"United States": 6, "China": -6}
fig, ax = plt.subplots(figsize=(8, 5))
for name, color in countries.items():
    c = le[le["Entity"] == name]
    ax.plot(c["Year"], c["LE"], color=color, linewidth=2, label=name)
    ax.annotate(name, (c["Year"].iloc[-1], c["LE"].iloc[-1]),
                xytext=(5, label_shift.get(name, 0)), textcoords="offset points",
                va="center", color=INK)
ax.set_xlim(1990, 2025)
ax.set_xlabel("Year")
ax.set_ylabel("Life expectancy at birth (years)")
ax.set_title("Figure 1. Contrasting life expectancy trajectories, 1990–2019", loc="left")
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig("figures/fig1_trajectories.png")

#figure 2: gains v starting income
def label_points(ax, x, y, names):
    for n in names:
        r = df[df["Entity"] == n].iloc[0]
        ax.annotate(n, (r[x], r[y]), xytext=(6, 2), textcoords="offset points",
                    fontsize=9, color=MUTED)

highlight = ["Malawi", "Lesotho", "Liberia", "United States", "China", "Eswatini"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["GDP1990_k"], df["dLE"], s=30, color=BLUE, alpha=0.8,
           edgecolor="white", linewidth=0.8)
ax.axhline(0, color=MUTED, linewidth=1)
label_points(ax, "GDP1990_k", "dLE", highlight)
ax.set_xlabel("GDP per capita in 1990 (thousands of 2021 int-$)")
ax.set_ylabel("Change in life expectancy, 1990–2019 (years)")
ax.set_title("Figure 2. Poorer countries gained the most life expectancy", loc="left")
fig.tight_layout()
fig.savefig("figures/fig2_gain_vs_start_income.png")

#figure 3: convergence
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["LE_1990"], df["dLE"], s=30, color=BLUE, alpha=0.8,
           edgecolor="white", linewidth=0.8)
ax.axhline(0, color=MUTED, linewidth=1)
label_points(ax, "LE_1990", "dLE", highlight)
ax.set_xlabel("Life expectancy in 1990 (years)")
ax.set_ylabel("Change in life expectancy, 1990–2019 (years)")
ax.set_title("Figure 3. Countries that started lower caught up (convergence)", loc="left")
fig.tight_layout()
fig.savefig("figures/fig3_convergence.png")

#figure 4: preston curve
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["GDP_1990"] / 1000, df["LE_1990"], s=30, color=BLUE, alpha=0.8,
           edgecolor="white", linewidth=0.8, label="1990")
ax.scatter(df["GDP_2019"] / 1000, df["LE_2019"], s=30, color=ORANGE, alpha=0.8,
           edgecolor="white", linewidth=0.8, label="2019")
ax.set_xlabel("GDP per capita (thousands of 2021 int-$)")
ax.set_ylabel("Life expectancy at birth (years)")
ax.set_title("Figure 4. Life expectancy vs income: steep, then flat", loc="left")
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig("figures/fig4_preston_curve.png")

#figure 5: response v each predictor
predictors = [("dGDP", "Change in GDP per capita\n(thousands of $)"),
              ("dSchool", "Change in schooling\n(years)"),
              ("GDP1990_k", "GDP per capita in 1990\n(thousands of $)")]
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
for ax, (col, label) in zip(axes, predictors):
    ax.scatter(df[col], df["dLE"], s=20, color=BLUE, alpha=0.8,
               edgecolor="white", linewidth=0.6)
    ax.axhline(0, color=MUTED, linewidth=1)
    ax.set_xlabel(label)
    r = df[col].corr(df["dLE"])
    ax.set_title(f"r = {r:.2f}", loc="left", fontsize=10, color=MUTED)
axes[0].set_ylabel("Change in life expectancy (years)")
fig.suptitle("Figure 5. Change in life expectancy vs each predictor", x=0.01, ha="left")
fig.tight_layout()
fig.savefig("figures/fig5_predictors.png")

print(df[["dLE", "dGDP", "dSchool", "GDP1990_k", "LE_1990"]].corr().round(2))