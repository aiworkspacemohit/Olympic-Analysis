import streamlit as st 
import pandas as pd 
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)



# st.sidebar.title("Olympics Analysis")
# st.sidebar.title("🏅 Olympic Insights Hub")
st.sidebar.markdown("""
<h2 style="
    color: inherit;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.0;
">
OLYMPIC<br>ANALYSIS
</h2>
<hr>
""", unsafe_allow_html=True)

st.sidebar.image('flag-Olympic-Games.png')

user_menu = st.sidebar.radio(
    'Select an option', 
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis' , 'Athlete wise Analysis')
)


# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")

    if selected_year!= 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "Overall Performance")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + "Olympics")

    st.dataframe(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top statistics : ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3: 
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.title("Participating Nations Over the Years")
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.plotly_chart(fig)

    st.title("Events Over the Years")
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    st.title("Athletes Over the Years")
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sports)")
    fig, ax = plt.subplots(figsize=(20,20))
    x= df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int), annot=True )
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport =st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)


    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y = 'Medal')
    st.title(selected_country + " Medal tally over the years")
    st.plotly_chart(fig)


    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize = (20, 20))
    ax = sns.heatmap(pt, annot = True  )
    st.pyplot(fig)

    st.title("Top 10 athletes")
    top10_df = helper.most_successful_athlete(df, selected_country)
    st.table(top10_df)



if user_menu == 'Athlete wise Analysis':

    #Distribution of Age 
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']== 'Silver']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist = False, show_rug = False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    #Distribution of Age with respect to Sports (Gold Medalists)
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                 'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                 'Tennis', 'Golf', 'Softball', 'Archery',
                 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                 'Rhythmic Gymnastics', 'Rugby Sevens',
                 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    x = [] 
    name = [] 
    for Sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']== Sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(Sport)

    fig = ff.create_distplot(x, name, show_hist= False, show_rug = False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution of Age with respect to Sports (Gold Medalists)")
    st.plotly_chart(fig)


    #Height vs Weight
    st.title("Height Vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'], y = temp_df['Height'], hue = temp_df['Medal'], style = temp_df['Sex'], s = 60)
    
    st.pyplot(fig)

     
    #Men vs Womwn Chart 
    st.title("Men vs Women Participations over the Year")
    final= helper.men_vs_women(df)
    fig = px.line(final, x = 'Year', y = ['Male', 'Female'], color_discrete_map={'Male': 'red','Female': 'green'})
    st.plotly_chart(fig)


    



