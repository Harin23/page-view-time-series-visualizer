import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")
# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(14, 9))
  plt.plot(df.index, df.values)
  plt.ylabel("Page Views")
  plt.xlabel("Date")
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  # Save image and return fig
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy().reset_index()
  df_bar["year"] = pd.DatetimeIndex(df_bar.date).year
  df_bar["Months"] = pd.DatetimeIndex(df_bar.date).month
  df_bar = df_bar.groupby(["year", "Months"]).value.mean().unstack()
  # Draw bar plot
  ax = df_bar.plot.bar(figsize=(14,10))
  ax.set_ylabel("Average Page Views")
  ax.set_xlabel("Years")
  ax.legend(title="Months", labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
  fig = ax.get_figure()
  # Save image and return fig
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
  # Prepare data for box plots 
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]
  print(df_box.head())
  # Draw box plots
  fig, ax = plt.subplots(figsize=(10, 15), nrows=1, ncols=2)

  ax0 = sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
  ax0.set_xlabel("Year")
  ax0.set_ylabel("Page Views")
  ax0.set_title("Year-wise Box Plot (Trend)")

  ax1 = sns.boxplot(x="month", y="value", order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], data=df_box, ax=ax[1])
  ax1.set_xlabel("Month")
  ax1.set_ylabel("Page Views")
  ax1.set_title("Month-wise Box Plot (Seasonality)")

  # Save image and return fig
  fig.savefig('box_plot.png')
  return fig
