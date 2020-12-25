import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import PIL
import io

data = pd.read_csv("time_series_covid19_confirmed_global.csv")

# group the data by the country
data_grouped_by_country = data.groupby("Country/Region").sum()

# Drop LAt and Lon Columns
data_dropped_columns = data_grouped_by_country.drop(columns=["Lat", "Long"])

# create a transpose of the df

# Read in the wolrd map shapefile
world = gpd.read_file(r"res/World_Countries.shp")

country_name_mapping = {
    "Myanmar": "Burma",
    "Cape Verde": "Cabo Verde",
    "Democratic Republic of the Congo": "Congo(Kinshasa)",
    "Congo": "Congo(Brazzaville)",
    "Ivory Coast": "Cote d'Ivoire",
    "Czech Republic": "Czechia",
    "Swaziland": "Eswatini",
    "South Korea": "Korea, South",
    "Macedonia": "North Macedonia",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Taiwan": "Taiwan*",
    "East Timor": "Timor-Leste",
    "United States": "US",
    "Palestine": "West Bank and Gaza",
    "St. Lucia": "Saint Lucia",
}

for original_name, modified_name in country_name_mapping.items():
    world.replace(original_name, modified_name, inplace=True)

# merging the data with "world" geopandas geodatafram
merge = world.join(data_dropped_columns, on="COUNTRY", how="right")

image_frames = []
dates_list_from_jan_to_april = merge.columns.to_list()[2:87]

for dates in dates_list_from_jan_to_april:
    # plot
    ax = merge.plot(
        column=dates,
        cmap="OrRd",
        figsize=(14, 14),
        legend=True,
        scheme="user_defined",
        classification_kwds={"bins": [10, 20, 50, 100, 500, 1000, 5000, 10000, 500000]},
        edgecolor="black",
        linewidth=0.4,
    )

    # add a title to the map
    ax.set_title(
        "Total Confirmed Coronavirus Cases" + dates, fontdict={"fontsize": 20}, pad=12.5
    )

    # removing the axes
    ax.set_axis_off()

    # move to the legend
    ax.get_legend().set_bbox_to_anchor((0.20, 0.5))

    img = ax.get_figure()

    f = io.BytesIO()
    img.savefig(f, format="png", bbox_inches="tight")
    image_frames.append(PIL.Image.open(f))
    f.seek(0)


# create a gif animation
image_frames[0].save(
    "covid19map.gif",
    format="GIF",
    append_images=image_frames[1:],
    save_all=True,
    duration=300,
    loop=0,
)
f.close()
