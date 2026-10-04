import pandas as pd

# shorten names
le = pd.read_csv("life-expectancy-hmd-unwpp/life-expectancy-hmd-unwpp.csv")
school = pd.read_csv("mean-years-of-schooling-long-run/mean-years-of-schooling-long-run.csv")
gdp = pd.read_csv("gdp-per-capita-worldbank/gdp-per-capita-worldbank.csv")

le.columns = ["Entity", "Code", "Year", "LE"]
school.columns = ["Entity", "Code", "Year", "School"]
gdp.columns = ["Entity", "Code", "Year", "GDP", "Region"]

# only real countries (ISO codes)
def countries_only(df):
    return df[df["Code"].notna() & (df["Code"].str.len() == 3)]

le = countries_only(le)
school = countries_only(school)
gdp = countries_only(gdp)

#years I need
def value_in(df, column, year):
    return df[df["Year"] == year].set_index("Code")[column]

le_1990 = value_in(le, "LE", 1990)
le_2019 = value_in(le, "LE", 2019)
gdp_1990 = value_in(gdp, "GDP", 1990)
gdp_2019 = value_in(gdp, "GDP", 2019)
school_1990 = value_in(school, "School", 1990)
school_2015 = value_in(school, "School", 2015)
school_2020 = value_in(school, "School", 2020)

#estimate school in 2019
school_2019 = school_2015 + 0.8 * (school_2020 - school_2015)

#combine into table
names = gdp.drop_duplicates("Code").set_index("Code")[["Entity", "Region"]]

df = pd.DataFrame({
    "LE_1990": le_1990, "LE_2019": le_2019,
    "GDP_1990": gdp_1990, "GDP_2019": gdp_2019,
    "School_1990": school_1990, "School_2019": school_2019,
}).join(names)

# variables:
# response
df["dLE"] = df["LE_2019"] - df["LE_1990"]
# change in income, $1,000s
df["dGDP"] = (df["GDP_2019"] - df["GDP_1990"]) / 1000
# change in education, years
df["dSchool"] = df["School_2019"] - df["School_1990"]
# starting income, $1,000s
df["GDP1990_k"] = df["GDP_1990"] / 1000

#drop countries w/o labels
print("Before:", len(df))
df = df.dropna()
print("After:", len(df))

#country trajectory (decline, stag, rise)
def classify(change):
    if change < 0:
        return "Decline"
    elif change <= 3:
        return "Stagnation"
    else:
        return "Rise"

df["Trajectory"] = df["dLE"].apply(classify)
print(df["Trajectory"].value_counts())

df.to_csv("country_changes_1990_2019.csv")