
import pandas as  pd
import streamlit as st
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as  plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv(r'/Users/mohitsinghchandel/Olympic  data analysis/athlete_events.csv')
df_region=pd.read_csv(r'/Users/mohitsinghchandel/Olympic  data analysis/noc_regions.csv')

df= preprocessor.preprocess(df,df_region)

st.sidebar.title('Olympics Analysis')
user_menu=st.sidebar.radio('Select an option',('Medal Tally','Country_wise analysis','Athlete_wise analysis','Overall analysis'))

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    
    years,country= helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox('select Year',years)
    selected_country=st.sidebar.selectbox('select country',country)
    
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year!='Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year) + ' OLympics')
    if selected_year=='Overall' and selected_country != 'Overall':
        st.title(selected_country+' Overall Performance')
    if selected_year!='Overall' and selected_country != 'Overall':
        st.title(selected_country+' performance in '+ str(selected_year))
        
        
        
    st.table(medal_tally)
    
    
if user_menu == 'Overall analysis':
    Editions=df['Year'].unique().shape[0]-1
    Cities=df['City'].unique().shape[0]
    Sports=df['Sport'].unique().shape[0]
    Events=df['Event'].unique().shape[0]
    Athlets=df['Name'].unique().shape[0]
    Nations=df['region'].unique().shape[0]  
    
    st.title('Overall statistics')
    col1,col2,col3 =st.columns(3)
    with col1:
        st.header('Editions')
        st.title(Editions)
    with col2:
        st.header('Hosts')
        st.title(Cities)
    with col3:
        st.header('Sports')
        st.title(Sports)
        
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(Events)
    with col2:
        st.header('Athlets')
        st.title(Athlets)
    with col3:
        st.header(' Nations')
        st.title( Nations)
        
    nations_over_time= helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)
    
        
    events_over_time= helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title('Events over the years')
    st.plotly_chart(fig)
    
    athletes_over_time= helper.data_over_time(df,'Name')
    fig = px.line( athletes_over_time, x="Edition", y="Name")
    st.title('Athletes over the years')
    st.plotly_chart(fig)
    
    
    st.title('No. of Events over time(Every Sports)')
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    
    
    st.title('Most Successful Athlete')
    sport_list= df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    Selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,Selected_sport)
    st.table(x)
    
    
if user_menu=='Country_wise analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a Country',country_list)
    country_df=helper.yearwise_medal_tally(df,selected_country)
    
    fig= px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+'Medal Tally Over The Years')
    st.plotly_chart(fig)
    
    
    st.title(selected_country+' excel in the following sports')
    
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    
    ax=sns.heatmap(pt ,annot=True)
    st.pyplot(fig)
    
    
    st.title('Top 10 athletes of'+ selected_country)
    top_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top_df)
    
    
    
if user_menu=='Athlete_wise analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    
    st.title('Distribution of Age')
    
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronge Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
    
    
    x=[]
    name=[]
    famous_sports=['Ice Hockey','Table Tennis' ,'Tennis','Archery','Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics','Art Competitions','Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo','Cycling']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age with respect to Sports(Gold Medalist)')
    st.plotly_chart(fig)
    
    sport_list= df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    
    Selected_sport=st.selectbox('Select a Sport',sport_list)
    temp_df=helper.weight_v_height(df,Selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.title('Height vs Weight')
    st.pyplot(fig)
    
    st.title('Men vs Women Participation Over the Years')
    final=helper.men_vs_women(df)
    fig= px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)
        