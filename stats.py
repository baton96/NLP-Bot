import plotly.graph_objects as go
from functools import wraps
import pandas as pd

translation = {
    'year': 'Rok',
    'month': 'Miesiąc',
    'weekday': 'Dzień tygodnia',
    'date2': 'Dzień',
    'hour': 'Godzina',
    'minute': 'Minuta',
    'month2': 'EXP',
}

def sent(tmp_df):
    return tmp_df[tmp_df.sender]

def received(tmp_df):
    return tmp_df[~tmp_df.sender]

def no_groups(tmp_df):
    return tmp_df[~tmp_df.isGroup]

def only_groups(tmp_df):
    return tmp_df[tmp_df.isGroup]

def show_or_return(graph_func):
    @wraps(graph_func)
    def wrapper(*args, **kwargs):
        fig, graph = graph_func(*args, **kwargs)
        if kwargs.get('show', True):
            fig.show()
        else:
            return graph
    return wrapper

def measure_by(tmp_df, by=None, metric='count', top=0):
    if by == 'year':
        tmp_df['year'] = pd.Categorical(tmp_df.timestamp.dt.year)
    elif by == 'month':
        monthsEng = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthsPl = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        tmp_df['month'] = pd.Categorical(
            tmp_df.timestamp.dt.strftime("%b"),
            categories=monthsEng).rename_categories(
                {eng: pl for eng, pl in zip(monthsEng, monthsPl)})
    elif by == 'weekday':
        weekdaysEng = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekdaysPl = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        tmp_df['weekday'] = pd.Categorical(
            tmp_df.timestamp.dt.strftime("%a"),
            categories=weekdaysEng).rename_categories(
                {eng: pl for eng, pl in zip(weekdaysEng, weekdaysPl)})
    elif by == 'hour':
        tmp_df['hour'] = pd.Categorical(tmp_df.timestamp.dt.strftime('%H:00'))
    elif by == 'minute':
        tmp_df['minute'] = pd.Categorical(tmp_df.timestamp.dt.strftime('%H:%M'))
    elif by == 'date2':
        tmp_df['date2'] = pd.Series(tmp_df.timestamp.dt.date)
    elif by == 'month2':
        tmp_df['month2'] = pd.Series(tmp_df.timestamp.dt.strftime("%b"))

    tmp_df = tmp_df.groupby(by or tmp_df.index).size().reset_index(name='metric')

    if metric == 'count':
        pass
        #tmp_df = tmp_df.size().reset_index(name='metric')
    elif metric == 'mean':
        tmp_df = tmp_df.mean().reset_index(name='metric')
    elif metric == 'max':
        max_row = tmp_df[tmp_df['metric'] == tmp_df['metric'].max()].iloc[0]
        print('Most talkative day: ', max_row[by], ', messages exchanged: ', max_row.metric)

    #if top > 0:
    #    tmp_df = tmp_df.nlargest(top, 'metric')

    return tmp_df


@show_or_return
def plot(by = 'title', kind="pie", top=10, no_groups_arg=False, only_groups_arg=False, received_arg=False, sent_arg=False):
    tmp_df = df.copy()
    if no_groups_arg:
        tmp_df = no_groups(tmp_df)
    if only_groups_arg:
        tmp_df = only_groups(tmp_df)
    if received_arg:
        tmp_df = received(tmp_df)
    if sent_arg:
        tmp_df = sent(tmp_df)

    # tmp_df = measure_by(tmp_df, by)
    tmp_df = measure_by(tmp_df, by, top=top)
    if kind == "pie":
        graph = go.Pie(labels=tmp_df[by], values=tmp_df.metric
        #, title=f"{top} największych czatów pod względem łącznej ilości wiadomości"
        )
        fig = go.Figure(graph)
    elif kind == "bar":
        graph = go.Bar(x=tmp_df[by], y=tmp_df.metric)
        fig = go.Figure(graph)
        fig.update_layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text=translation[by])),
                          yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Liczba wiadomości")))
    elif kind == "scatter":
        graph = go.Scatter(x=tmp_df[by], y=tmp_df.metric, mode="lines")
        fig = go.Figure(graph)
        fig.update_layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text=translation[by])),
                          yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Liczba wiadomości")))
    #fig.update_layout(title_text=f"Top {top} largest chats", xaxis={'type': 'category'})
    return fig, graph

dtypes = {'isGroup': bool, 'sender': bool, 'type': bool, 'sticker': bool, 'photos': bool, 'videos': bool}
df = pd.read_csv('all.csv',
                 parse_dates=['timestamp'],
                 dtype=dtypes,
                 index_col='title',
                 infer_datetime_format=True)

# measure_by(no_groups(df), by='date2', metric='max')
#print(df.sender.head(5))
plot(by='month2', kind="scatter")
#by='year', kind="bar"
#kind="bar"
#only_groups_arg=True
#no_groups_arg=True