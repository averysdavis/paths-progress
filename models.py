import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

os.makedirs("figures", exist_ok=True)

BLUE, MUTED, INK = "#2a78d6", "#52514e", "#0b0b0b"
plt.rcParams.update({
    "font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": "#e4e3df", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "axes.axisbelow": True,
})

df = pd.read_csv("country_changes_1990_2019.csv", index_col="Code")

#fit models with more and more predictors
formulas = {
    "Model 1": "dLE ~ dGDP",
    "Model 2": "dLE ~ dGDP + dSchool",
    "Model 3": "dLE ~ dGDP + dSchool + GDP1990_k",
    "Model 3b": "dLE ~ dSchool + GDP1990_k",
}
models = {name: smf.ols(f, data=df).fit() for name, f in formulas.items()}

#full regression output (save for appendix)
with open("regression_output.txt", "w") as f:
    for name, m in models.items():
        f.write(f"===== {name}: {formulas[name]} =====\n")
        f.write(str(m.summary()) + "\n\n")

#compare in table
rows = []
for name, m in models.items():
    row = {"Model": name, "R2": m.rsquared, "Adj R2": m.rsquared_adj, "n": int(m.nobs)}
    for p in ["dGDP", "dSchool", "GDP1990_k"]:
        if p in m.params:
            row[p] = f"{m.params[p]:.3f} (p={m.pvalues[p]:.3f})"
        else:
            row[p] = ""
    rows.append(row)
table = pd.DataFrame(rows).set_index("Model")
print(table.round(3).to_string())

#overlap between predictors
print("\nCorrelation between predictors:")
print(df[["dGDP", "dSchool", "GDP1990_k"]].corr().round(2))

# residuals for full model and refined model
for name in ["Model 3", "Model 3b"]:
    m = models[name]
    df["fitted"] = m.fittedvalues
    df["resid"] = m.resid

    slug = name.replace(" ", "").lower()

    # residuals v fitted
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["fitted"], df["resid"], s=30, color=BLUE, alpha=0.8,
               edgecolor="white", linewidth=0.8)
    ax.axhline(0, color=MUTED, linewidth=1)
    for code, r in df.loc[df["resid"].abs().nlargest(6).index].iterrows():
        ax.annotate(r["Entity"], (r["fitted"], r["resid"]), xytext=(5, 2),
                    textcoords="offset points", fontsize=9, color=MUTED)
    ax.set_xlabel("Fitted value (predicted change in life expectancy)")
    ax.set_ylabel("Residual (years)")
    ax.set_title("Residuals vs fitted", loc="left")
    fig.tight_layout()
    fig.savefig(f"figures/resid_{slug}_vs_fitted.png")

    # residual histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["resid"], bins=20, color=BLUE, edgecolor="white")
    ax.set_xlabel("Residual (years)")
    ax.set_ylabel("Number of countries")
    ax.set_title("Distribution of residuals", loc="left")
    fig.tight_layout()
    fig.savefig(f"figures/resid_{slug}_hist.png")

    print(f"\n{name}: residual SD = {df['resid'].std():.2f} years")
    print("Largest residuals:")
    print(df.loc[df["resid"].abs().nlargest(8).index, ["Entity", "dLE", "fitted", "resid"]].round(1).to_string())
    print("Mean residual by region:")
    print(df.groupby("Region")["resid"].agg(["mean", "count"]).round(2).to_string())

# chart the final model (3b): each predictor's line, holding the other at its average
ORANGE = "#eb6834"
m = models["Model 3b"]
panels = [("GDP1990_k", "dSchool", "GDP per capita in 1990 (thousands of $)",
           "start_income", "starting income", "schooling change"),
          ("dSchool", "GDP1990_k", "Change in schooling, 1990–2019 (years)",
           "schooling", "schooling change", "starting income")]

for x, other, label, slug, short, other_short in panels:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter(df[x], df["dLE"], s=30, color=BLUE, alpha=0.8,
               edgecolor="white", linewidth=0.8)
    grid = pd.DataFrame({x: pd.Series(range(101)) / 100 * (df[x].max() - df[x].min()) + df[x].min()})
    grid[other] = df[other].mean()
    pred = m.get_prediction(grid).summary_frame(alpha=0.05)
    ax.fill_between(grid[x], pred["mean_ci_lower"], pred["mean_ci_upper"],
                    color=ORANGE, alpha=0.15, linewidth=0)
    ax.plot(grid[x], pred["mean"], color=ORANGE, linewidth=2)
    ax.axhline(0, color=MUTED, linewidth=1)
    # Uganda and Niger sit close together, so push their labels apart
    label_shift = {"Uganda": 8, "Niger": -6}
    for code, r in df.loc[m.resid.abs().nlargest(6).index].iterrows():
        ax.annotate(r["Entity"], (r[x], r["dLE"]),
                    xytext=(5, 2 + label_shift.get(r["Entity"], 0)),
                    textcoords="offset points", fontsize=9, color=MUTED)
    ax.set_xlabel(label)
    r = df[x].corr(df["dLE"])
    ax.set_ylabel("Change in life expectancy (years)")
    fig.suptitle(f"Change in life expectancy vs {short}", x=0.01, ha="left")
    ax.set_title(f"slope = {m.params[x]:.3f} per unit, r = {r:.2f}, r² = {r**2:.2f}, p = {m.pvalues[x]:.3f}\n"
                 f"{other_short} held at its average; band = 95% CI",
                 loc="left", fontsize=10, color=MUTED)
    fig.tight_layout()
    fig.savefig(f"figures/model3b_fit_{slug}.png")

# actual vs predicted: points on the diagonal = perfect prediction
df["fitted"] = m.fittedvalues
fig, ax = plt.subplots(figsize=(6.5, 6))
ax.scatter(df["fitted"], df["dLE"], s=25, color=BLUE, alpha=0.8,
           edgecolor="white", linewidth=0.6)
lims = [df[["fitted", "dLE"]].min().min() - 1, df[["fitted", "dLE"]].max().max() + 1]
ax.plot(lims, lims, color=ORANGE, linewidth=2, label="Perfect prediction")
for n in ["Liberia", "Malawi", "Lesotho", "Eswatini", "China", "United States"]:
    r = df[df["Entity"] == n].iloc[0]
    ax.annotate(n, (r["fitted"], r["dLE"]), xytext=(5, 2),
                textcoords="offset points", fontsize=9, color=MUTED)
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_xlabel("Predicted change in life expectancy (years)")
ax.set_ylabel("Actual change in life expectancy (years)")
ax.set_title(f"Actual vs predicted (R² = {m.rsquared:.3f})", loc="left")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("figures/model3b_actual_vs_predicted.png")
