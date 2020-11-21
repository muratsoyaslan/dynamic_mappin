import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt
import PIL
import io 

data=pd.read_csv("time_series_covid19_confirmed_global.csv")

#group the data by the country 
data=data.groupby("Country/Region").sum()

#Drop LAt and Lon Columns
data= data.drop(columns = ["Lat","Long"])

#create a transpose of the df

data_transposed = data.T 
data_transposed.plot( y =[ "Australia","China","US","Italy"], use_index = True , figsize=(10,10))

#Read in the wolrd map shapefile
world = gpd.read_file(r'C:\Users\SOYASLAN\Desktop\MDSoyaslan\dynamic_mappin\res\World_Countries.shp')

world.replace("Myanmar","Burma" ,inplace=True)
world.replace("Cape Verde","Cabo Verde",inplace=True)
world.replace("Democratic Republic of the Congo","Congo(Kinshasa)", inplace=True)
world.replace("Congo","Congo(Brazzaville)",inplace=True)
world.replace("Ivory Coast","Cote d'Ivoire",inplace=True)
world.replace("Czech Republic","Czechia",inplace=True)
world.replace("Swaziland","Eswatini",inplace=True)
world.replace("South Korea","Korea, South",inplace=True)
world.replace("Macedonia","North Macedonia",inplace=True)
world.replace("St. Kitts and Nevis","Saint Kitts and Nevis",inplace=True)
world.replace("St. Vincent and the Grenadines","Saint Vincent and the Grenadines",inplace=True)
world.replace("Taiwan","Taiwan*",inplace=True)
world.replace("East Timor","Timor-Leste",inplace=True)
world.replace("United States","US",inplace=True)
world.replace("Palestine","West Bank and Gaza",inplace=True)
world.replace("St. Lucia","Saint Lucia",inplace=True)

#merging the data with "world" geopandas geodatafram
merge=world.join(data, on= "COUNTRY" ,how="right")

image_frames=[]
for dates in merge.columns.to_list()[2:87]:

   #plot
   ax=merge.plot(column= dates,
   cmap="OrRd",
   figsize=(14,14),
   legend=True,
   scheme="user_defined",
   classification_kwds={"bins":[10,20,50,100,500,1000,5000,10000,500000]},
   edgecolor="black",
   linewidth=0.4)


   #add a title to the map
   ax.set_title("Total Confirmed Coronavirus Cases"+dates ,fontdict={"fontsize":20},pad=12.5)

   #removing the axes
   ax.set_axis_off()

   #move to the legend
   ax.get_legend().set_bbox_to_anchor((0.20,0.5))


   img=ax.get_figure()

   f=io.BytesIO()
   img.savefig(f,format="png",bbox_inches="tight")
   f.seek(0)
   image_frames.append(PIL.Image.open(f))



#create a gif animation

image_frames[0].save("covid19map.gif",format="GIF"
,append_images=image_frames[1:],save_all=True,duration=600,loop=0)   
f.close()