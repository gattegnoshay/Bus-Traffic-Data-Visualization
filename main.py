# Press the green button in the gutter to run the script.
def loadData():
    return  pd.concat([pd.read_csv("./Data/busdata2022.csv"), pd.read_csv("./Data/busdata2023.csv"),
                    pd.read_csv("./Data/busdata2024.csv")])
def load2324Data():
    return  pd.concat([ pd.read_csv("./Data/busdata2023.csv"),
                    pd.read_csv("./Data/busdata2024.csv")])
def replace_agency_name(name):
    if name not in ['אגד', 'מטרופולין']:
        return get_display('אחר')
    else:
        return get_display(name)


def getDescriptiveStatistics(df):
    print(df.describe())
    df.describe().to_csv("descriptive statistics.csv")
    #print(df['Saturday - 19:00-23:59'].mean())
    #print(df['Saturday - 19:00-23:59'].std())

def createBarChart(df):
    #droping zeros
    #df = df[df['AVGPassengersPerWeek'] != 0]

    df['AgencyName'] = df['AgencyName'].apply(get_display)
    average_passengers = df.groupby('AgencyName')['WeeklyPassengers'].count().sort_values(ascending=False)
    print(average_passengers)
    top_10_agencies = average_passengers.nlargest(15)

    fig, ax = plt.subplots()
    ax.barh(top_10_agencies.index, top_10_agencies.values, align='center')
    ax.set_yticks(top_10_agencies.index, labels=top_10_agencies.index)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Bus line count')
    ax.set_title('Eged Has the Most bus lines in the country ')
    plt.show()

def createZerosChart(df):
    df = df[df['WeeklyPassengers'] == 0]
    df['AgencyName'] = df['AgencyName'].apply(get_display)
    average_passengers = df.groupby('AgencyName')['WeeklyPassengers'].count().sort_values(ascending=False)

    plt.xticks(rotation=20, ha='right', fontsize=10)
    plt.bar(average_passengers.index, average_passengers.values)
    plt.xlabel(get_display('שם חברה'), fontname='Arial', fontsize=12)
    plt.ylabel(get_display('מספר הקווים הריקים'), fontsize=12)
    plt.title(get_display('נתיבי אקספרסס מנצחת במס הקווים הריקים'))
    plt.show()


def createTreeMap(df):
    df["AVGCostPerWeek"] = df['OperatingCostPerPassenger'] * df['WeeklyPassengers']
    locationCounter = df.groupby(['Metropolin', 'ClusterName'], group_keys=True).agg({'NumOfAlternatives':'sum','RouteID':'count'}).reset_index()

    print(locationCounter)
    fig = px.treemap(locationCounter, path=['Metropolin', 'ClusterName'], values='RouteID',color='NumOfAlternatives', title='Treemap with Two Clusters')
    fig.show()

def createStackedBarChart(df):
    df["NonUniqueStations"] = df['StationsInRoute'] - df['UniqueStations']
    df['UniqueStations'] = df['StationsInRoute']
    df['NonUniqueStations'] = df['NonUniqueStations']


    AVGPASS = df.groupby(['year', 'Q'], group_keys=True).agg(
        {'NonUniqueStations': 'sum', 'UniqueStations': 'sum'}).reset_index()

    AVGPASS['NonUniqueDifference'] = AVGPASS['NonUniqueStations'].diff()
    AVGPASS['UniqueDifference'] = AVGPASS['UniqueStations'].diff()

    print(AVGPASS)

    AVGPASS['Year-Quarter'] = AVGPASS['year'].astype(str) + ' - ' +"Q"+ AVGPASS['Q'].astype(str)


    fig, ax = plt.subplots()
    bars1 = ax.bar(AVGPASS['Year-Quarter'], AVGPASS['NonUniqueDifference'], label='NonUniqueDifference')
    bars2 = ax.bar(AVGPASS['Year-Quarter'], AVGPASS['UniqueDifference'], bottom=AVGPASS['NonUniqueDifference'], label='UniqueDifference')

    bars1[1].set_color('green')
    bars1[2].set_color('green')
    bars1[3].set_color('red')
    bars2[1].set_color('#5fe85a')
    bars2[2].set_color('#5fe85a')
    bars2[3].set_color('#f0655d')



    # Adding labels and title
    ax.set_xlabel('Year-Quarter')
    ax.set_ylabel('Values')
    ax.set_title('Stcked Bar Chart')
    #ax.set_ylim(175000,200000)

    ax.legend()

    plt.show()

def getColorsdf():
    data = {
        'AgencyName': ['סופרבוס', 'מטרופולין', 'נתיב אקספרס', 'אגד', 'קווים', 'אגד תעבורה','אלקטרה אפיקים', 'דן','ש.א.מ','גלים','בית שמש אקספרס','דן באר שבע','דן בדרום','תנופה','נסיעות ותיירות','מועצה אזורית גולן','גי.בי.טורס','מועצה אזורית אילות'],
        'Color':      ["#024DB2","#F99D20",'#66676B','#00A65E' ,"#03296A","#00A65E",'#0C87CB','#0257A8','#4C5416','white','#EC410F','#0257A8','#FFF200','#0257A8','#A349A4','#C9181F','#DCC96B','#BDBBBC']
    }

    return pd.DataFrame(data)

def on_scroll(event):
    if event.button == 'up':
        factor = 1.1  # zoom in
    elif event.button == 'down':
        factor = 0.9  # zoom out
    else:
        return

    xdata, ydata = event.xdata, event.ydata
    ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    new_xlim = (xlim[0] - xdata) * factor + xdata, (xlim[1] - xdata) * factor + xdata
    new_ylim = (ylim[0] - ydata) * factor + ydata, (ylim[1] - ydata) * factor + ydata

    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    plt.draw()
def createGeoMapChart(df):
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import mplcursors
    cities = pd.read_csv("./Data/IsraelCities.csv",encoding = "Windows-1255")
    cities['hebrew_name'] = cities['hebrew_name'].apply( lambda x: get_display(str(x)))
    #merge = pd.merge(df, cities, left_on='OriginCityName', right_on='hebrew_name', how='left')
    #print(merge)
    group = df.groupby(['OriginCityName','AgencyName']).agg({'WeeklyPassengers': 'sum'}).reset_index()
    sorted_group = group.sort_values(by='WeeklyPassengers', ascending=False)
    filtered_group = sorted_group.drop_duplicates(subset='OriginCityName')
    print(filtered_group)

    filtered_group['OriginCityName'] =     filtered_group['OriginCityName'].apply(lambda x: get_display(str(x)))
    cities['hebrew_name'] = cities['hebrew_name'].apply(lambda x: str(x))


    merge = pd.merge(filtered_group, cities, left_on='OriginCityName', right_on='hebrew_name', how='left')

    colors = getColorsdf()
    colors['AgencyName'] = colors['AgencyName'].apply(lambda x: get_display(str(x)))
    merge['AgencyName'] = merge['AgencyName'].apply(lambda x: get_display(str(x)))
    merge = pd.merge(merge, colors, on='AgencyName', how='left')
    print(merge)
    merge = merge.dropna()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    israel = world[world['name'] == 'Israel']
    israel.plot(color='lightgrey')

    scatter = plt.scatter(merge['lng'], merge['lat'], color=merge['Color'], marker='.')
    #for index, row in cities.iterrows():
     #   plt.annotate(row['hebrew_name'], (row['lng'], row['lat']), textcoords="offset points", xytext=(0, 10),
    #                 ha='center')
    mplcursors.cursor(scatter, hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(merge['OriginCityName'].iloc[sel.target.index]))

    #Legend
    legend_elements = []
    for color, name in zip(colors['Color'], colors['AgencyName']):
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', label=name, markerfacecolor=color, markersize=10))
    plt.legend(handles=legend_elements, title='City Names',bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.connect('scroll_event', on_scroll)



    plt.ylim(30, None)
    plt.show()



def createNetworkGraph(df):

    import networkx as nx
    df["OriginCityName"].apply(lambda x:get_display(x))
    df["DestinationCityName"].apply(lambda x: get_display(x))
    group = df.groupby(['OriginCityName', 'DestinationCityName']).agg({'WeeklyPassengers': 'sum'}).reset_index()
    group["OriginCityName"] = group["OriginCityName"].apply(lambda x: get_display(x.replace(" ","\n")))
    group["DestinationCityName"] = group["DestinationCityName"].apply(lambda x: get_display(x.replace(" ","\n")))
    nodes = pd.Index(group['OriginCityName'].append(group['DestinationCityName']).unique())
    group = group[group["OriginCityName"]!= group["DestinationCityName"]]
    group = group.sort_values(by='WeeklyPassengers', ascending=False).head(30)

    G = nx.from_pandas_edgelist(group, 'OriginCityName', 'DestinationCityName', edge_attr='WeeklyPassengers')

    # Draw the graph
    pos = nx.kamada_kawai_layout(G)  # positions for all nodes

    nx.draw_networkx(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=9,font_family ="sans-serif")

    edge_widths = [data['WeeklyPassengers'] / 50000 for _, _, data in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='black')

    plt.title("Network Graph with Edge Weights")
    plt.show()

if __name__ == '__main__':
    from bidi.algorithm import get_display # pip install python-bidi
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.express as px
    import geopandas # pip install geopandas
    import plotly.graph_objects as go

    df = loadData()

    #getDescriptiveStatistics(df)
    #createBarChart(df)
    #createZerosChart(df)
    #createStackedBarChart(df)
    #createGeoMapChart(df)
    createNetworkGraph(df)
    #df = load2324Data()
    #createTreeMap(df)



"""
    empty_df = pd.DataFrame(columns=["CityName1","CityName2","WeeklyPassengers"])
    print(empty_df)
    for index, row in group.iterrows():
        for index1, row1 in group.iterrows():
            if row["OriginCityName"] == row1["CityName2"] and row["DestinationCityName"] == lastrow["CityName1"]:
                empty_df[row["OriginCityName"] == empty_df["CityName2"]]["WeeklyPassengers"] += row["WeeklyPassengers"]
            else:
                empty_df.append(row, ignore_index=True)

    print(empty_df)
"""