import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def to_kebab_case(string):
    return '-'.join(
        string.replace(",", "").replace(".", "").split()
    ).lower()


np.random.seed(2)


def prepare_input_dataframes(ball_by_ball, matches_result):
    ball_by_ball = ball_by_ball.rename(columns={
        'ID': 'match_id',
        'ballnumber': 'ball_number',
        'non-striker': 'non_striker',
        'BattingTeam': 'batting_team',
    }).loc[:, [
        'match_id',
        'innings',
        'batting_team',
        'overs',
        'ball_number',
        'batter',
        'bowler',
        'total_run',
    ]]

    matches_result = matches_result.rename(columns={
        'ID': 'match_id',
        'Team1': 'team_1',
        'Team2': 'team_2',
        'Venue': 'venue',
    }).loc[:, [
        'match_id',
        'team_1',
        'team_2',
        'venue',
    ]]

    return ball_by_ball, matches_result


# In[5]:


venue_mapping_normal = {
    "Arun Jaitley Stadium": "Arun Jaitley Stadium",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium",
    "Feroz Shah Kotla": "Arun Jaitley Stadium",
    "Barsapara Cricket Stadium": "Barsapara Cricket Stadium",
    "Barsapara Cricket Stadium, Guwahati": "Barsapara Cricket Stadium",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "Eden Gardens": "Eden Gardens",
    "Eden Gardens, Kolkata": "Eden Gardens",
    "Himachal Pradesh Cricket Association Stadium": "Himachal Pradesh Cricket Association Stadium",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala": "Himachal Pradesh Cricket Association Stadium",
    "M Chinnaswamy Stadium": "M Chinnaswamy Stadium",
    "M Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium",
    "M Chinnaswamy Stadium, Bangalore": "M Chinnaswamy Stadium",
    "M.Chinnaswamy Stadium": "M Chinnaswamy Stadium",
    "M.Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium",
    "M.Chinnaswamy Stadium, Bangalore": "M Chinnaswamy Stadium",
    "MA Chidambaram Stadium": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chennai": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium",
    "Narendra Modi Stadium": "Narendra Modi Stadium",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium",
    "Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Rajiv Gandhi International Stadium": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Hyderabad": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium",
    "Sawai Mansingh Stadium": "Sawai Mansingh Stadium",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium",
    "Wankhede Stadium": "Wankhede Stadium",
    "Wankhede Stadium, Mumbai": "Wankhede Stadium"
}


# In[6]:


venue_mapping_kebab = {
    "arun-jaitley-stadium": "Arun Jaitley Stadium",
    "arun-jaitley-stadium-delhi": "Arun Jaitley Stadium",
    "feroz-shah-kotla": "Arun Jaitley Stadium",
    "barsapara-cricket-stadium": "Barsapara Cricket Stadium",
    "barsapara-cricket-stadium-guwahati": "Barsapara Cricket Stadium",
    "bharat-ratna-shri-atal-bihari-vajpayee-ekana-cricket-stadium": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "bharat-ratna-shri-atal-bihari-vajpayee-ekana-cricket-stadium-lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "eden-gardens": "Eden Gardens",
    "eden-gardens-kolkata": "Eden Gardens",
    "himachal-pradesh-cricket-association-stadium": "Himachal Pradesh Cricket Association Stadium",
    "himachal-pradesh-cricket-association-stadium-dharamsala": "Himachal Pradesh Cricket Association Stadium",
    "m-chinnaswamy-stadium": "M Chinnaswamy Stadium",
    "m-chinnaswamy-stadium-bengaluru": "M Chinnaswamy Stadium",
    "m-chinnaswamy-stadium-bangalore": "M Chinnaswamy Stadium",
    "mchinnaswamy-stadium": "M Chinnaswamy Stadium",
    "mchinnaswamy-stadium-bengaluru": "M Chinnaswamy Stadium",
    "mchinnaswamy-stadium-bangalore": "M Chinnaswamy Stadium",
    "ma-chidambaram-stadium": "MA Chidambaram Stadium",
    "ma-chidambaram-stadium-chennai": "MA Chidambaram Stadium",
    "ma-chidambaram-stadium-chepauk": "MA Chidambaram Stadium",
    "ma-chidambaram-stadium-chepauk-chennai": "MA Chidambaram Stadium",
    "narendra-modi-stadium": "Narendra Modi Stadium",
    "narendra-modi-stadium-ahmedabad": "Narendra Modi Stadium",
    "punjab-cricket-association-is-bindra-stadium": "Punjab Cricket Association IS Bindra Stadium",
    "punjab-cricket-association-is-bindra-stadium-mohali": "Punjab Cricket Association IS Bindra Stadium",
    "punjab-cricket-association-stadium-mohali": "Punjab Cricket Association IS Bindra Stadium",
    "rajiv-gandhi-international-stadium": "Rajiv Gandhi International Stadium",
    "rajiv-gandhi-international-stadium-hyderabad": "Rajiv Gandhi International Stadium",
    "rajiv-gandhi-international-stadium-uppal": "Rajiv Gandhi International Stadium",
    "sawai-mansingh-stadium": "Sawai Mansingh Stadium",
    "sawai-mansingh-stadium-jaipur": "Sawai Mansingh Stadium",
    "wankhede-stadium": "Wankhede Stadium",
    "wankhede-stadium-mumbai": "Wankhede Stadium"
}


# In[7]:


venue_mapping_tags = {
    "delhi": "Arun Jaitley Stadium",
    "arun jaitley": "Arun Jaitley Stadium",
    "guwahati": "Barsapara Cricket Stadium",
    "barsapara": "Barsapara Cricket Stadium",
    "bhupen hazarika": "Barsapara Cricket Stadium",
    "assam cricket association stadium": "Barsapara Cricket Stadium",
    "lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "ekana": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "atal bihari": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "kolkata": "Eden Gardens",
    "eden gardens": "Eden Gardens",
    "dharamsala": "Himachal Pradesh Cricket Association Stadium",
    "himachal pradesh": "Himachal Pradesh Cricket Association Stadium",
    "bengaluru": "M Chinnaswamy Stadium",
    "bengalore": "M Chinnaswamy Stadium",
    "chinnaswamy": "M Chinnaswamy Stadium",
    "chennai": "MA Chidambaram Stadium",
    "chepauk": "MA Chidambaram Stadium",
    "chidambaram": "MA Chidambaram Stadium",
    "ahmedabad": "Narendra Modi Stadium",
    "narendra modi": "Narendra Modi Stadium",
    "mohali": "Punjab Cricket Association IS Bindra Stadium",
    "punjab cricket association": "Punjab Cricket Association IS Bindra Stadium",
    "is bindra": "Punjab Cricket Association IS Bindra Stadium",
    "hyderabad": "Rajiv Gandhi International Stadium",
    "rajiv gandhi": "Rajiv Gandhi International Stadium",
    "jaipur": "Sawai Mansingh Stadium",
    "sawai mansingh": "Sawai Mansingh Stadium",
    "mumbai": "Wankhede Stadium",
    "wankhede": "Wankhede Stadium"
}


# In[8]:


team_mapping = {  # 10 teams
    'Rajasthan Royals': 'Rajasthan Royals',
    'Gujarat Titans': 'Gujarat Titans',
    'Royal Challengers Bangalore': 'Royal Challengers Bangalore',
    'Lucknow Super Giants': 'Lucknow Super Giants',
    'Sunrisers Hyderabad': 'Sunrisers Hyderabad',
    'Mumbai Indians': 'Mumbai Indians',
    'Chennai Super Kings': 'Chennai Super Kings',
    'Kolkata Knight Riders': 'Kolkata Knight Riders',

    'Kings XI Punjab': 'Punjab Kings',
    'Punjab Kings': 'Punjab Kings',

    'Delhi Daredevils': 'Delhi Capitals',
    'Delhi Capitals': 'Delhi Capitals',
}


# In[9]:


def do_mapping(ball_by_ball, matches_result):
    matches_result.venue = matches_result.venue.map(
        venue_mapping_normal).fillna('Other')

    matches_result.team_1 = matches_result.team_1.map(
        team_mapping).fillna('Other')
    matches_result.team_2 = matches_result.team_2.map(
        team_mapping).fillna('Other')

    ball_by_ball.batting_team = ball_by_ball.batting_team.map(
        team_mapping).fillna('Other')
    return ball_by_ball, matches_result


# In[10]:


def select_innings_and_overs(ball_by_ball):
    ball_by_ball = ball_by_ball.loc[(
        ball_by_ball.overs <= 5) & (ball_by_ball.innings <= 2)]

    ball_by_ball.loc[ball_by_ball.innings == 1, 'innings'] = 0
    ball_by_ball.loc[ball_by_ball.innings == 2, 'innings'] = 1
    # ball_by_ball.innings = ball_by_ball.innings.replace({1: 0, 2: 1})
    # ball_by_ball.innings.replace({1: 0, 2: 1}, inplace=True)
    return ball_by_ball


# In[11]:


def prepare_final_training_dataframe(ball_by_ball, matches_result):
    ball_by_ball_gb = ball_by_ball.groupby(
        ['match_id', 'innings', 'batting_team'])

    total_runs = ball_by_ball_gb['total_run'].sum()
    batsmen = ball_by_ball_gb['batter'].unique()
    bowlers = ball_by_ball_gb['bowler'].unique()

    total_runs = total_runs.to_frame(name='total_runs').reset_index()
    batsmen = batsmen.to_frame(name='batsmen').reset_index()
    bowlers = bowlers.to_frame(name='bowlers').reset_index()

    data = total_runs.merge(batsmen, how='right', on=[
                            'match_id', 'innings', 'batting_team'])
    data = data.merge(bowlers, how='right', on=[
                      'match_id', 'innings', 'batting_team'])
    data = data.merge(matches_result, on=['match_id'])

    mask = data['batting_team'] == data['team_1']
    data.loc[mask, 'bowling_team'] = data['team_2']
    data.loc[~mask, 'bowling_team'] = data['team_1']

    # match_id == 829763, data for one innings is missing
    # match_id == 829813, total_runs for one innings is 2 (probably a mistake in data entry)
    data = data.drop(data[(data['match_id'] == 829763) |
                     (data['match_id'] == 829813)].index)

    # get count of batsmen & bowlers for each innings
    data['count_batsmen'] = [len(x) for x in data['batsmen']]
    data['count_bowlers'] = [len(x) for x in data['bowlers']]

    data = data[
        ['venue', 'innings', 'batting_team', 'bowling_team',
            'count_batsmen', 'count_bowlers', 'total_runs']
    ]

    return data


# In[12]:


def prepare_training_data(input_dataframes):
    ball_by_ball, matches_result = input_dataframes
    ball_by_ball, matches_result = prepare_input_dataframes(
        ball_by_ball, matches_result)
    ball_by_ball, matches_result = do_mapping(ball_by_ball, matches_result)
    ball_by_ball = select_innings_and_overs(ball_by_ball)
    return prepare_final_training_dataframe(ball_by_ball, matches_result)


# In[13]:


class MyModel:
    def __init__(self):
        pass


# In[14]:


def train_model(X_train, y_train):
    #     from sklearn.linear_model import LinearRegression
    #     return LinearRegression().fit(X_train, y_train)
    from sklearn.linear_model import Ridge
    return Ridge(alpha=1.0).fit(X_train, y_train)


# In[15]:

class ConstantRegressor:
    def __init__(self, n):
        self.n = n

    def predict(self, X):
        return np.repeat(self.n, X.shape[0])


def MyModel__fit(self, input_dataframes):
    try:
        # raise Exception("Test Exception: MyModel__fit")

        data = prepare_training_data(input_dataframes)

        X = data.iloc[:, :-1]
        y = data["total_runs"]

        self.preprocessor = ColumnTransformer([
            ("onehot", OneHotEncoder(handle_unknown='ignore', sparse_output=False), [
                "venue", "batting_team", "bowling_team"]),
            ("scaler", StandardScaler(), ["count_batsmen", "count_bowlers"])
        ], remainder='passthrough')

        X_preprocessed = self.preprocessor.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_preprocessed, y, test_size=0.2)
        self.model = train_model(X_train, y_train)
    except Exception as e:
        self.model = ConstantRegressor(46)


# In[16]:


def MyModel__predict(self, X_IPL23):
    try:
        # raise Exception("Test Exception: MyModel__predict")

        X_IPL23.innings = X_IPL23.innings.replace({1: 0, 2: 1})

        # get count of batsmen & bowlers for each innings
        X_IPL23['count_batsmen'] = [len(x.split(","))
                                    for x in X_IPL23['batsmen']]
        X_IPL23['count_bowlers'] = [len(x.split(","))
                                    for x in X_IPL23['bowlers']]
        X_IPL23 = X_IPL23.drop(columns=['batsmen', 'bowlers'])[
            ['venue', 'innings', 'batting_team', 'bowling_team',
                'count_batsmen', 'count_bowlers']
        ]

        ambiguous_venues = np.setdiff1d(
            X_IPL23.venue.unique(), list(venue_mapping_normal.keys()))
        ambiguous_venues_mapping = {}
        for venue in ambiguous_venues:
            venue_kebab_case = to_kebab_case(venue)
            if venue_kebab_case in venue_mapping_kebab:
                ambiguous_venues_mapping[venue] = venue_mapping_kebab[venue_kebab_case]
            else:
                venue_lower = venue.lower()
                for tag in venue_mapping_tags:
                    if tag in venue_lower:
                        ambiguous_venues_mapping[venue] = venue_mapping_tags[tag]

        venue_mapping_final = {
            **venue_mapping_normal, **ambiguous_venues_mapping}

        X_IPL23.venue = X_IPL23.venue.map(venue_mapping_final).fillna('Other').replace({
            'Barsapara Cricket Stadium': 'Other',
            'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium': 'Other'
        })

        X_IPL23_preprocessed = self.preprocessor.transform(X_IPL23)

        return np.round(
            self.model.predict(X_IPL23_preprocessed)
        ).astype(int)
    except Exception as e:
        return [46, 46]


# In[17]:


MyModel.fit = MyModel__fit
MyModel.predict = MyModel__predict
