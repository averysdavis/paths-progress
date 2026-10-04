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
ax.set_title("Contrasting life expectancy trajectories, 1990–2019", loc="left")
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
ax.set_title("Poorer countries gained the most life expectancy", loc="left")
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
ax.set_title("Countries that started lower caught up (convergence)", loc="left")
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
ax.set_title("Life expectancy vs income: steep, then flat", loc="left")
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig("figures/fig4_preston_curve.png")

#figure 5: response v each predictor
predictors = [("a", "dGDP", "Change in GDP per capita, 1990–2019 (thousands of $)", "change in GDP"),
              ("b", "dSchool", "Change in schooling, 1990–2019 (years)", "change in schooling"),
              ("c", "GDP1990_k", "GDP per capita in 1990 (thousands of $)", "starting income")]
for letter, col, label, short in predictors:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df[col], df["dLE"], s=30, color=BLUE, alpha=0.8,
               edgecolor="white", linewidth=0.8)
    ax.axhline(0, color=MUTED, linewidth=1)
    ax.set_xlabel(label)
    ax.set_ylabel("Change in life expectancy, 1990–2019 (years)")
    r = df[col].corr(df["dLE"])
    ax.set_title(f"Change in life expectancy vs {short} (r = {r:.2f})", loc="left")
    fig.tight_layout()
    fig.savefig(f"figures/fig5{letter}_{col}.png")

print(df[["dLE", "dGDP", "dSchool", "GDP1990_k", "LE_1990"]].corr().round(2))

#figure 6: trajectories by starting income (3 equal-size groups by 1990 GDP)
df["Income group"] = pd.qcut(df["GDP1990_k"], 3, labels=["Low", "Middle", "High"])
cutoffs = df.groupby("Income group", observed=True)["GDP1990_k"].agg(["min", "max", "count"])
print("\nStarting income groups ($1,000s):")
print(cutoffs.round(1))

traj = le[le["Code"].isin(df.index)].merge(df[["Income group"]], left_on="Code", right_index=True)
group_colors = {"Low": BLUE, "Middle": ORANGE, "High": AQUA}

fig, ax = plt.subplots(figsize=(8, 5))
for group, color in group_colors.items():
    g = traj[traj["Income group"] == group]
    # each country as a faint line
    for code, c in g.groupby("Code"):
        ax.plot(c["Year"], c["LE"], color=color, linewidth=0.6, alpha=0.2)
    # group average as a bold line
    avg = g.groupby("Year")["LE"].mean()
    lo, hi = cutoffs.loc[group, "min"], cutoffs.loc[group, "max"]
    ax.plot(avg.index, avg.values, color=color, linewidth=2.5,
            label=f"{group} (\\${lo:.1f}k–\\${hi:.1f}k)")
    ax.annotate(f"{group}: {avg.iloc[0]:.1f} → {avg.iloc[-1]:.1f}",
                (avg.index[-1], avg.iloc[-1]), xytext=(5, 0),
                textcoords="offset points", va="center", color=INK, fontsize=9)
ax.set_xlim(1990, 2027)
ax.set_xlabel("Year")
ax.set_ylabel("Life expectancy at birth (years)")
ax.set_title("Life expectancy by starting income group, 1990–2019", loc="left")
ax.legend(frameon=False, loc="lower right", title="1990 GDP per capita", fontsize=9)
fig.tight_layout()
fig.savefig("figures/fig6_trajectories_by_start_income.png")

print("\nGroup average life expectancy:")
print(traj.groupby(["Income group", "Year"], observed=True)["LE"].mean().unstack().loc[:, [1990, 2000, 2010, 2019]].round(1))


#figures 7-10: how GDP and schooling changed for the figure 1 countries
gdp = pd.read_csv("gdp-per-capita-worldbank/gdp-per-capita-worldbank.csv")
gdp.columns = ["Entity", "Code", "Year", "GDP", "Region"]
gdp = gdp[(gdp["Year"] >= 1990) & (gdp["Year"] <= 2019)]

school = pd.read_csv("mean-years-of-schooling-long-run/mean-years-of-schooling-long-run.csv")
school.columns = ["Entity", "Code", "Year", "School"]
school = school[(school["Year"] >= 1990) & (school["Year"] <= 2015)]
# add the interpolated 2019 value from build_dataset.py
school_2019 = df[["Entity", "School_2019"]].rename(columns={"School_2019": "School"}).reset_index()
school_2019["Year"] = 2019
school = pd.concat([school, school_2019]).sort_values(["Code", "Year"])


def end_labels(ax, data, xcol, ycol, shift):
    for name, color in countries.items():
        c = data[data["Entity"] == name]
        ax.annotate(name, (c[xcol].iloc[-1], c[ycol].iloc[-1]),
                    xytext=(5, shift.get(name, 0)), textcoords="offset points",
                    va="center", color=INK)


#figure 7: GDP per capita over time
fig, ax = plt.subplots(figsize=(8, 5))
for name, color in countries.items():
    c = gdp[gdp["Entity"] == name]
    ax.plot(c["Year"], c["GDP"] / 1000, color=color, linewidth=2, label=name)
end_labels(ax, gdp.assign(GDP_k=gdp["GDP"] / 1000), "Year", "GDP_k",
           {"Malawi": -6, "Lesotho": 6})
ax.set_xlim(1990, 2025)
ax.set_xlabel("Year")
ax.set_ylabel("GDP per capita (thousands of 2021 int-$)")
ax.set_title("GDP per capita, 1990–2019", loc="left")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("figures/fig7_gdp_trajectories.png")

#figure 8: schooling over time (5-year data + 2019 estimate)
fig, ax = plt.subplots(figsize=(8, 5))
for name, color in countries.items():
    c = school[school["Entity"] == name]
    ax.plot(c["Year"], c["School"], color=color, linewidth=2, marker="o",
            markersize=5, label=name)
end_labels(ax, school, "Year", "School", {})
ax.set_xlim(1990, 2025)
ax.set_xlabel("Year")
ax.set_ylabel("Average years of schooling (ages 15–64)")
ax.set_title("Average years of schooling, 1990–2019", loc="left")
ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, 0.85))
ax.annotate("Data every 5 years; 2019 estimated from 2015 and 2020",
            (0.99, 0.02), xycoords="axes fraction", ha="right", fontsize=9, color=MUTED)
fig.tight_layout()
fig.savefig("figures/fig8_schooling_trajectories.png")

#figures 9-10: each country's path, 1990 (circle) to 2019 (arrow)
def path_chart(data, xcol, xlabel, title, filename, xscale=1):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for name, color in countries.items():
        c = data[data["Entity"] == name].merge(le[["Code", "Year", "LE"]], on=["Code", "Year"])
        x = c[xcol] / xscale
        ax.plot(x, c["LE"], color=color, linewidth=2, label=name)
        ax.scatter(x.iloc[0], c["LE"].iloc[0], s=50, color=color,
                   edgecolor="white", linewidth=1.5, zorder=3)
        ax.annotate("", xy=(x.iloc[-1], c["LE"].iloc[-1]),
                    xytext=(x.iloc[-2], c["LE"].iloc[-2]),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
        ax.annotate(f"{name} 1990", (x.iloc[0], c["LE"].iloc[0]), xytext=(6, -10),
                    textcoords="offset points", fontsize=9, color=MUTED)
        ax.annotate(f"{name} 2019", (x.iloc[-1], c["LE"].iloc[-1]), xytext=(6, 4),
                    textcoords="offset points", fontsize=9, color=INK)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Life expectancy at birth (years)")
    ax.set_title(title, loc="left")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(filename)

path_chart(gdp, "GDP", "GDP per capita (thousands of 2021 int-$)",
           "Path of life expectancy vs income, 1990 → 2019",
           "figures/fig9_path_le_vs_gdp.png", xscale=1000)
path_chart(school, "School", "Average years of schooling (ages 15–64)",
           "Path of life expectancy vs schooling, 1990 → 2019",
           "figures/fig10_path_le_vs_schooling.png")
