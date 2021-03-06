import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'total_vaccinations_per_hundred'],
    parse_dates=['date'])

countries = ['United States', 'Germany', 'United Kingdom', 'Brazil', 'Argentina', 'Chile', 'Uruguay']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='total_vaccinations_per_hundred',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                   # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )


# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45, fontsize=12)
#plt.ylim(0,100)

## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Total de doses administradas por 100 pessoas', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Vacina????es COVID-19', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_vac")


# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'people_vaccinated'],
    parse_dates=['date'])

countries = ['United States', 'Germany', 'United Kingdom', 'Brazil', 'Argentina', 'Chile', 'Uruguay']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='people_vaccinated',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                    # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )
    vacs_br = pivot['Brazil']

def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000:
        val = round(tick_val/1000000, 1)
        new_tick_format = '{:}'.format(val)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]

    return new_tick_format


# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
ax.yaxis.set_major_formatter(mtick.ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)
ax.yaxis.get_major_formatter().set_useOffset(False)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(reformat_large_tick_values))

## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Total de vacina????es por milh??o de habitante', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Vacina????es COVID-19', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_vactot")

def percentage(value, total, multiply=True):
	try:
		percent = (value / float(total))
		if multiply:
			percent = percent * 100
		return percent
	except ZeroDivisionError:
		return None


df = pd.DataFrame(vacs_br)
vacs = df.iloc[-1]['Brazil']

percent = round(percentage(vacs,212000000),3)

df = pd.read_csv('all_dead.csv')
df.at[1,"Mortos"] = percent
df.at[2,"Mortos"] = vacs
df.to_csv('all_dead.csv', index=False)


def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000:
        val = round(tick_val/1000, 1)
        new_tick_format = '{:}'.format(val)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]

    return new_tick_format


# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'new_cases_smoothed'],
    parse_dates=['date'])

countries = ['Brazil','India']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='new_cases_smoothed',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                   # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )


# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=2))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45, fontsize=12)
ax.yaxis.set_major_formatter(mtick.ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)
ax.yaxis.get_major_formatter().set_useOffset(False)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(reformat_large_tick_values))
#plt.ylim(0,100)

## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Novos casos di??rios por milhar', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Novos casos confirmados de COVID-19 no Brasil e na India', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_ind_cases")

#Gr??fico de Novas Mortes

# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'new_deaths_smoothed'],
    parse_dates=['date'])

countries = ['Brazil','India']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='new_deaths_smoothed',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                    # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )
    #vacs_br = pivot['new_deaths_smoothed']



# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=2))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45, fontsize=12)


## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Mortes di??rias', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Mortes em 24h por COVID-19 no Brasil e na India', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_ind_deaths")

#Gr??fico de mortes total

# Step 1: Load the data
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'total_deaths'],
    parse_dates=['date'])

countries = ['Brazil','India']
df = df[df['location'].isin(countries)]



# Step 2: Summarize the data
pivot = pd.pivot_table(
    data=df,                                    # What dataframe to use
    index='date',                               # The "rows" of your dataframe
    columns='location',                         # What values to show as columns
    values='total_deaths',    # What values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

pivot = pivot.fillna(method='ffill')


# Step 3: Set up key variables for the visualization
main_country = 'Brazil'
colors = {country:('black' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.5 if country!= main_country else 1.0) for country in countries}


# Step 4: Plot all countries
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # What to use as your x-values
        pivot[country],           # What to use as your y-values
        color=colors[country],    # How to color your line
        alpha=alphas[country]     # What transparency to use for your line
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
        y = pivot[country].max(),                   # How high to position your text
        color = colors[country],
        fontsize=13,                    # What color to give your text
        s = country,                                # What to write
        alpha=alphas[country]                       # What transparency to use
    )
    #vacs_br = pivot['new_deaths_smoothed']



# Step 5: Configures axes
## A) Format what shows up on axes and how it's displayed
date_form = DateFormatter("%d-%m-%Y")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=2))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45, fontsize=12)


## B) Customizing axes and adding a grid
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=1)

## C) Adding a title and axis labels
plt.ylabel('Total de Mortes', fontsize=18, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('Total de Mortes por COVID-19 no Brasil e na India', fontsize=18, weight='bold', alpha=0.9)

# D) Celebrate!
plt.savefig("covid_ind_totdeaths")
