# Press the green button in the gutter to run the script.
def loadData():
    return  pd.concat([pd.read_csv("./Data/busdata2022.csv"), pd.read_csv("./Data/busdata2023.csv"),
                    pd.read_csv("./Data/busdata2024.csv")])

def replace_agency_name(name):
    if name not in ['אגד', 'מטרופולין']:
        return get_display('אחר')
    else:
        return get_display(name)


def getDescriptiveStatistics(df):
    print(df.describe())
    df.describe().transpose().to_csv("descriptive statistics.csv")
    print(df.corr().to_csv("corr.csv"))

def createBarChart(df):

    df = df[df['year'] == 2024]
    df = df[df['OperatingCostPerPassenger']!=0]
    #filtered_df = df.drop_duplicates(subset=['RouteID'])
    df['AgencyName'] = df['AgencyName'].apply(get_display)
    average_passengers = df.groupby('AgencyName')['OperatingCostPerPassenger'].mean().sort_values(ascending=False)

    top_10_agencies = average_passengers.nlargest(10)

    fig, ax = plt.subplots()
    ax.barh(top_10_agencies.index, top_10_agencies.values, align='center',color=["#00A65E"])

    ax.set_yticks(top_10_agencies.index, labels=top_10_agencies.index)
    ax.invert_yaxis()
    plt.grid(True, linestyle='--', color='gray', linewidth=0.5,alpha=0.4)
    ax.set_xlabel(get_display('עלויות תפעולית ממוצעות לנוסע בש"ח'))
    plt.title(get_display('חברות קטנות, עלויות גדולות'), fontsize=16)
    #plt.title(get_display('עלות תפעולית ממוצעת לנוסע לפי חברת האוטובוסים'), fontsize=10)
    ################
    plt.subplots_adjust(top=0.88, bottom=0.11, left=0.260, right=0.9, hspace=0.2, wspace=0.2)

    ################


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
    df = df[df['year'] == 2024]
    df["AVGOperationalCost"] = df['OperatingCostPerPassenger'] * df['WeeklyPassengers']
    df["Metropolin"] = df["Metropolin"].apply(lambda x: "י-ם" if x == "מזרח ירושלים" else x)

    df= df[df["Metropolin"] != "הדרום"]
    df= df[df["Metropolin"] != "גולן גליל ועמקים" ]
    df= df[df["Metropolin"] != "בין מחוזי"]
    df = df[df["Metropolin"] != "מרכז"]


    df["OriginCityName"] = df["OriginCityName"].apply(lambda x: x.replace(" ","<br>"))
    locationCounter = df.groupby(['Metropolin','OriginCityName'], group_keys=True).agg({"AVGOperationalCost":'mean','WeeklyPassengers':'sum',"OperatingCostPerPassenger":"sum"}).reset_index()
    locationCounter = locationCounter.nlargest(15,'WeeklyPassengers')
    #locationCounter = locationCounter[locationCounter["WeeklyPassengers"]>locationCounter["WeeklyPassengers"].mean()]
    locationCounter["AVGOperationalCost"] = locationCounter["AVGOperationalCost"].apply(lambda x: x/10000)
    print(locationCounter)
    fig = px.treemap(locationCounter, path=['Metropolin','OriginCityName'], values='WeeklyPassengers',color='AVGOperationalCost',
                     title='עלות התפעול בבת ים וקרית מוצקין: כפול מכל השאר',color_continuous_scale='rdbu_r',width=1000,height=700)
    fig.update_layout(coloraxis_colorbar=dict(
          title='עלות תפעול שבועית ממוצעת <br> בעשרות אלפי שקלים'  # Change the colorbar label here
    ))
    fig.update_traces(marker=dict(cornerradius=5))
    fig.update_layout(
        title_font_size=20,  # Adjust subtitle font size as needed
        title_y=0.95,  # Adjust subtitle vertical position as needed
        title_pad_t=10,  # Adjust subtitle padding as needed
        title_pad_l=510,
        title_text= 'עלות התפעול בבת ים וקרית מוצקין: כפול מכל השאר'
    )
    fig.add_annotation(
        text="חמישה עשר הערים עם עלויות התפעול הגבוהות ביותר מחולקות לפי מטרופולין. הגדלים מייצגים את ממוצע הנוסעים השבועי בעיר",
        xref="paper", yref="paper",
        x=1.27, y=1.05,  # Adjust position of subtitle
        showarrow=False,
        font=dict(size=16, color="black"),
    )
    fig.show()

def CreateStackedBarChart(df):
    df = df[df["year"] == 2024]

    # Encode the operation periods into separate columns
    df['לפני 1 חודשים'] = df["OperationSince"] == 'לפני 1 חודשים'
    df['לפני 2 חודשים'] = df["OperationSince"] == 'לפני 2 חודשים'
    df['לפני 3 חודשים'] = df["OperationSince"] == 'לפני 3 חודשים'
    df['לפני 4 חודשים'] = df["OperationSince"] == 'לפני 4 חודשים'
    df['לפני 5 חודשים'] = df["OperationSince"] == 'לפני 5 חודשים'
    df['לפני 6 חודשים'] = df["OperationSince"] == 'לפני 6 חודשים'


    # Group by 'AgencyName' and sum the counts of different operation periods
    AVGPASS = df.groupby(['AgencyName']).agg({
        'RouteName': 'count',
        'לפני 1 חודשים': 'sum',
        'לפני 2 חודשים': 'sum',
        'לפני 3 חודשים': 'sum',
        'לפני 4 חודשים': 'sum',
        'לפני 5 חודשים': 'sum',
        'לפני 6 חודשים': 'sum'
    }).reset_index()
    print(AVGPASS)
    # Filter out rows with all zeros
    AVGPASS_filtered = AVGPASS[
        (AVGPASS[['לפני 1 חודשים', 'לפני 2 חודשים', 'לפני 3 חודשים', 'לפני 4 חודשים', 'לפני 5 חודשים', 'לפני 6 חודשים']] != 0).any(axis=1)]

    # Calculate the sum of the counts for the first 6 periods
    AVGPASS_filtered['Sum'] = AVGPASS_filtered[
        ['לפני 1 חודשים', 'לפני 2 חודשים', 'לפני 3 חודשים', 'לפני 4 חודשים', 'לפני 5 חודשים', 'לפני 6 חודשים']].sum(
        axis=1)

    # Sort the DataFrame by the sum
    #AVGPASS_sorted = AVGPASS_filtered.sort_values(by='Sum', ascending=False)

    AVGPASS_filtered = AVGPASS_filtered[AVGPASS_filtered['AgencyName'] != "נתיב אקספרס"]
    AVGPASS_filtered = AVGPASS_filtered.nlargest(5 ,"Sum")


    x = AVGPASS_filtered['AgencyName'].apply(lambda x: get_display(x.replace(" ","\n")))
    y1 = AVGPASS_filtered['לפני 1 חודשים']
    y2 = AVGPASS_filtered['לפני 2 חודשים']
    y3 = AVGPASS_filtered['לפני 3 חודשים']
    y4 = AVGPASS_filtered['לפני 4 חודשים']
    y5 = AVGPASS_filtered['לפני 5 חודשים']

    # Create the figure and axis
    fig, ax = plt.subplots()

    # Plot the bars
    bars1 = ax.bar(x, y1, label=get_display('לפני חודש'), color='#E0A346')
    bars2 = ax.bar(x, y2, bottom=y1, label=get_display('לפני חודשיים'), color="#90B5DA")
    bars3 = ax.bar(x, y3, bottom=y1 + y2, label=get_display('לפני 3 חודשים'), color="#B3987F")
    bars4 = ax.bar(x, y4, bottom=y1 + y2 + y3, label=get_display('לפני 4 חודשים'), color="#F5D963")
    bars5 = ax.bar(x, y5, bottom=y1 + y2 + y3 + y4, label=get_display('לפני 5 חודשים'), color="#407DB0")


    # Add labels, title, and legend
    ax.set_xlabel(get_display('חברת אוטובוסים'), fontsize=10,labelpad=0)
    ax.set_ylabel(get_display('מספר\nקווים\nחדשים'), fontsize=10,rotation=0,labelpad=15)
    ax.set_title(get_display('חמשת החברות המובילות במספר הקוים החדשים שהוקמו'), fontsize=10)
    plt.suptitle(get_display('התחדשות! חברות האוטובוסים ממשיכות להשיק קווים'))
    ax.legend()
    plt.grid(alpha=0.2)
    # Show the plot
    plt.show()

def getColorsdf():
    data = {
        'AgencyName': ['סופרבוס', 'מטרופולין', 'נתיב אקספרס', 'אגד', 'קווים', 'אגד תעבורה','אלקטרה אפיקים', 'דן','ש.א.מ','גלים','בית שמש אקספרס','דן באר שבע','דן בדרום','תנופה','נסיעות ותיירות','מועצה אזורית גולן','גי.בי.טורס','מועצה אזורית אילות'],
        'Color':      ["#FFDE27","#F99D20",'#66676B','#00A65E' ,"#8215F2","#00A65E",'#AAFFAE','#0257A8','#4C5416','white','#EC410F','#0257A8','#FFF200','#0257A8','#A349A4','#C9181F','#DCC96B','#BDBBBC']
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

    #Dealing With Business Data
    #AgencyName Union
    df['AgencyName'] = df['AgencyName'].apply(lambda x: "אגד" if x == "אגד תעבורה" else x)
    df['AgencyName'] = df['AgencyName'].apply(lambda x: "דן" if x == "דן באר שבע" else x)
    df['AgencyName'] = df['AgencyName'].apply(lambda x: "דן" if x == "דן בדרום" else x)
    group = df.groupby(['OriginCityName','AgencyName']).agg({'WeeklyPassengers': 'mean'}).reset_index()
    sorted_group = group.sort_values(by='WeeklyPassengers', ascending=False).drop_duplicates(subset='OriginCityName')
    sorted_group['OriginCityName'] = sorted_group['OriginCityName'].apply(lambda x: get_display(str(x)))

    #Dealing with geo data
    cities = pd.read_csv("./Data/IsraelCities.csv", encoding="Windows-1255")
    cities['hebrew_name'] = cities['hebrew_name'].apply(lambda x: get_display(str(x)))
    cities['hebrew_name'] = cities['hebrew_name'].apply(lambda x: str(x))
    merge = pd.merge(sorted_group, cities, left_on='OriginCityName', right_on='hebrew_name', how='left')

    #Dealing with colors
    colors = getColorsdf()
    colors['AgencyName'] = colors['AgencyName'].apply(lambda x: get_display(str(x)))
    merge['AgencyName'] = merge['AgencyName'].apply(lambda x: get_display(str(x)))
    merge = pd.merge(merge, colors, on='AgencyName', how='left')
    merge = merge.dropna()

    #Printing the Graph
    #Print Israel
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    israel = world[world['name'] == 'Israel']
    israel.plot(color='lightgrey')
    #drop unmatched color + heb_name
    merge = merge.dropna(subset=["hebrew_name", "Color"])
    merge = merge.nlargest(35, 'WeeklyPassengers')

    #Print Data
    scatter = plt.scatter(merge['lng'], merge['lat'], color=merge['Color'], marker='o',s=15)
    mplcursors.cursor(scatter, hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(merge['OriginCityName'].iloc[sel.target.index] +
                                              " : " + merge['AgencyName'].iloc[sel.target.index]))

    #Legend
    legend_elements = []
    merge['Combined'] = merge['Color'] + '_' + merge['AgencyName'].astype(str)
    unique_pairs = merge['Combined'].unique()


    unique_pairs_df = pd.DataFrame([x.split('_') for x in unique_pairs], columns=['Color', 'AgencyName'])
    print(unique_pairs_df)
    for color, name in zip(unique_pairs_df['Color'], unique_pairs_df['AgencyName']):
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', label=name, markerfacecolor=color, markersize=10))
    plt.legend(handles=legend_elements, title=get_display('שם חברה'),bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.connect('scroll_event', on_scroll)

    plt.suptitle(get_display('תוכנית החלוקה'),fontsize=16)
    plt.title(get_display('חברת האוטובוסים לה ממוצע הנוסעים הגבוה ביותר בכל עיר'),fontsize=10)
    plt.axis('off')
    plt.ylim(30.8,33.023)
    plt.show()



def createNetworkGraph(df):

    import networkx as nx

    df["OriginCityName"].apply(lambda x:get_display(x))
    df["DestinationCityName"].apply(lambda x: get_display(x))

    group = df.groupby(['OriginCityName', "DestinationCityName"]).agg({'WeeklyPassengers': 'sum', }).reset_index()
    group["OriginCityName"] = group["OriginCityName"].apply(lambda x: get_display(x.replace(" ","\n")))
    group["DestinationCityName"] = group["DestinationCityName"].apply(lambda x: get_display(x.replace(" ","\n")))

    nodes = pd.Index(group['OriginCityName'].append(group['DestinationCityName']).unique())
    group = group[group["OriginCityName"]!= group["DestinationCityName"]]
    group = group.sort_values(by='WeeklyPassengers', ascending=False).head(30)

    G = nx.from_pandas_edgelist(group, 'OriginCityName', 'DestinationCityName', edge_attr='WeeklyPassengers')
    pos = nx.fruchterman_reingold_layout(G,iterations = 10)
    nx.draw_networkx(G, pos, with_labels=True, node_size=1000, node_color="#B2DFE7",font_size=9,font_family ="sans-serif",edgecolors="Grey")

    edge_widths = [data['WeeklyPassengers'] / 50000 for _, _, data in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color='black')

    #plt.title(get_display(''), fontsize=10)
    plt.suptitle(get_display("תלויים במטרופולין"))
    plt.title(get_display("מספר הנוסעים הממוצע בין הערים השונות"))
    plt.subplots_adjust(top=0.88, bottom=0.11, left=0.125, right=0.9, hspace=0.2, wspace=0.2)

    plt.show()


def createViolinChart(df):
    from matplotlib.widgets import RangeSlider
    import seaborn as sns
    func= "sum"

    """
    #check n largest
    
    group = df.groupby(['OriginCityName']).agg(
        {'Friday - 15:00-18:59': func, 'Friday - 19:00-23:59': func, 'Saturday - 00:00-03:59': func,
         'Saturday - 04:00-05:59': func, 'Saturday - 06:00-08:59': func, 'Saturday - 09:00-11:59': func,
         'Saturday - 12:00-14:59': func, 'Saturday - 15:00-18:59': func}).reset_index()
    print(group.nlargest(5,'Saturday - 12:00-14:59'))
"""

    #prepare for violin
    sliced = df[['OriginCityName','Friday - 15:00-18:59','Friday - 19:00-23:59','Saturday - 00:00-03:59','Saturday - 04:00-05:59','Saturday - 06:00-08:59','Saturday - 09:00-11:59','Saturday - 12:00-14:59','Saturday - 15:00-18:59']]
    df = df[(df["OriginCityName"] == "ירושלים") | (df["OriginCityName"] == "חיפה") | (df["OriginCityName"] == "נצרת") | (df["OriginCityName"] == "מגאר")| (df["OriginCityName"] == "נוף הגליל")]

    #df = df[['OriginCityName', 'Saturday - 12:00-14:59']].dropna()
    df["OriginCityName"] = df["OriginCityName"].apply(get_display)
    # Display the plot
    fig, ax = plt.subplot_mosaic(
        [
            ['main', 'radio']
        ],
        width_ratios=[5, 1]
       # layout='constrained',
    )
    ax["main"] = sns.violinplot(x='OriginCityName', y='Friday - 15:00-18:59', data=df, linewidth=1.5, showextrema=True, ax=ax['main'])
    ax['main'].set_xlabel(get_display('שם עיר'), fontsize=16)
    ax['main'].tick_params(axis='x', labelsize=14)
    ax['main'].tick_params(axis='y', labelsize=14)
    ax['main'].set_ylabel(get_display('כמות נוסעים' + " \n" + ' ממוצעת לקו'), rotation=0, labelpad=40, fontsize=16)
    ax['main'].set_title(get_display('ירושלים בפסגה: התפלגות כמות הנוסעים הממוצעת לקו ביום שבת'), fontsize=24)
    ax['main'].set_ylim(0, 210)
    plt.draw()


    radio_button = RadioButtons(ax['radio'], ('Friday - 15:00-18:59','Friday - 19:00-23:59','Saturday - 06:00-08:59','Saturday - 09:00-11:59','Saturday - 12:00-14:59','Saturday - 15:00-18:59'))
    ax['radio'].set_title(get_display('התפלגות לפי תקופה'))
    def on_radio_button_clicked(label):
        ax['main'].cla()  # Clear current plot
        sns.violinplot(x='OriginCityName', y=label, data=df, linewidth=1.5, showextrema=True,ax=ax['main'],fontsize=14)
        ax['main'].set_xlabel(get_display('שם עיר'), fontsize=16)
        ax['main'].tick_params(axis='x', labelsize=14)
        ax['main'].tick_params(axis='y', labelsize=14)
        ax['main'].set_ylabel(get_display('כמות נוסעים' + " \n" + ' ממוצעת לקו'), rotation=0, labelpad=40, fontsize=16)
        ax['main'].set_title(get_display('ירושלים בפסגה: התפלגות כמות הנוסעים הממוצעת לקו ביום שבת'), fontsize=24)
        ax['main'].set_ylim(0, 210)
        plt.draw()
    radio_button.on_clicked(on_radio_button_clicked)

    #Slider
    ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = RangeSlider(ax_slider, get_display('כמות נוסעים ממוצעת לקו'), 0, 200, valinit=(0, 210))

    def update_range(val):
        lower, upper = slider.val
        ax['main'].set_ylim(lower, upper)
        fig.canvas.draw_idle()

    slider.on_changed(update_range)

    plt.show()

    plt.show()

if __name__ == '__main__':
    from bidi.algorithm import get_display # pip install python-bidi
    from matplotlib.widgets import RadioButtons
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.express as px
    import plotly.graph_objects as go
    import geopandas as gpd # pip install geopandas
    import mplcursors

    df = loadData()
    #getDescriptiveStatistics(df)
    #createGeoMapChart(df)
    #createTreeMap(df)
    #createBarChart(df)
    #createNetworkGraph(df)
    #createViolinChart(df)
    #CreateStackedBarChart(df)


    #BONUS: Busses with 0 passengers?
    #createZerosChart(df)
