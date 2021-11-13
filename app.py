import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

THEME = dbc.themes.SIMPLEX
pd.options.mode.chained_assignment = None   # mute SettingWithCopyWarning

app = dash.Dash(
    __name__,
    external_stylesheets = [THEME]
)
server = app.server

property_income = pd.read_csv("assets/data/property_full.csv")
industry = pd.read_csv("assets/data/industry.csv")
climate = pd.read_csv("assets/data/climate.csv")

app_colors = {
    'background':'#f5f5f5',
    'plot_title':'#666666',
    'subtitle':'#898989',
    'primary':'#e6bd26',
    'secondary':'#d7d7d4'
}

HEADER_STYLE = {
    'position': 'fixed',
    'padding': '2rem',
    'overflow': 'hidden',
    'top': 0,
    'width': '100%',
    'background-color': app_colors['background'],
    'z-index': '10'
}

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 150,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '1rem'
}

BODY_STYLE = {
    'margin': '0 0 5rem 20%',
    'width': '80%'
}

header = html.Header(
    [
        html.Div(
            [
                html.H1(
                    "The Truth About America’s Worst Place to Live",
                    style = {'color': app_colors["primary"]}
                ),
                html.H3(
                    "Red Lake County, MN",
                    style = {'color': app_colors["subtitle"]}
                ),
                html.H4(
                    "2013 - 2015",
                    style = {'color': app_colors["subtitle"]}
                )
            ]
        )
    ],
    style = HEADER_STYLE
)

year_filter = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Form(
                    [
                        html.Br(),
                        dbc.Label(
                            "Select Year",
                            html_for = 'select-year',
                            style = {
                                'padding-left':'1rem',
                                'font-weight':'bold',
                                'color': app_colors['plot_title']
                            }
                        ),
                        dcc.Slider(
                            id = 'select-year',
                            min = 2013,
                            max = 2015,
                            step = 1,
                            value = 2015,
                            marks = {
                                2013:'2013',
                                2014:'2014',
                                2015:'2015'
                            }
                        )
                    ]
                )
            ]
        )
    ]
)

sidebar = html.Div(
    [
        year_filter
    ],
    style=SIDEBAR_STYLE,
)

body = dbc.Container(
    [
        sidebar,
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            "What is Red Lake County good at?",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        html.H5(
                            "Agriculture is a key driver of the county's economy",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        dbc.Spinner(
                            dcc.Graph(id = "industry")
                        ),
                        html.P(
                            "* Industry RCA: Measures the industry's comparative advantage compared to other counties.",
                            style = {
                                'color': app_colors["plot_title"],
                                'margin-top': '1rem'
                            }
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.H4(
                            "How much does it cost to live here?",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        html.H5(
                            "Apparently, not as much as most places",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        dbc.Spinner(
                            dcc.Graph(id = "property-income")
                        ),
                        html.P(
                            "* Housing Affordability: Median household income / Median property value",
                            style = {
                                'color': app_colors["plot_title"],
                                'margin-top': '1rem'
                            }
                        )
                    ]
                )
            ],
            style = {'margin-top': '11rem'}
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Form(
                            [
                                dbc.Label(
                                    "Select Season",
                                    html_for = 'select-season',
                                    style = {
                                        'font-weight':'bold',
                                        'color': app_colors['plot_title']
                                    }
                                ),
                                dcc.RadioItems(
                                    id = 'select-season',
                                    value = 'winter',
                                    options=[
                                        {'label': 'Winter', 'value': 'winter'},
                                        {'label': 'Spring', 'value': 'spring'},
                                        {'label': 'Summer', 'value': 'summer'},
                                        {'label': 'Fall', 'value': 'fall'}
                                    ],
                                    labelStyle = {
                                        'display': 'inline-block',
                                        'color': app_colors["plot_title"],
                                        'font-size': '0.8rem',
                                        'margin-right': '1rem'
                                    },
                                    inputStyle = {
                                        'margin-right': '0.5rem',
                                        'vertical-align': 'middle'
                                    }
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                        id = 'season-img',
                                        src = app.get_asset_url("images/winter.jpg"),
                                        height = "160px"
                                    ),
                                    width = "auto",
                                    style = {'padding-right': '6px'}
                                ),
                                dbc.Col(
                                    [
                                        html.H5(
                                            "Red Lake County in the Winter",
                                            id = "rlc-season",
                                            style = {
                                                'color': app_colors["plot_title"],
                                                'font-size': '14px'
                                            }
                                        ),
                                        html.P(
                                            id = "what-to-do",
                                            style = {'color': app_colors["plot_title"]}
                                        ),
                                    ]
                                )
                            ],
                            align = 'center'
                        )
                    ],
                    width = 5,
                    align = 'center'
                ),
                dbc.Col(
                    [
                        html.H4(
                            "What it's like and what to do in Red Lake County",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        html.H5(
                            "The four seasons of Red Lake County",
                            style = {'color': app_colors["plot_title"]}
                        ),
                        dbc.Spinner(
                            dcc.Graph(id = "season-climate")
                        )
                    ],
                    width = 7
                )
            ]
        )
    ],
    style=BODY_STYLE
)

def plot_industry(df, year):
    df_year = df.sort_values(f'ACS Industry yg RCA ({year})', ascending = False, ignore_index = True)
    df_year = df_year.loc[:4,['Industry', f'ACS Industry yg RCA ({year})', f'Workforce by Industry and Gender ({year})']]

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x = df_year["Industry"],
            y = df_year[f'ACS Industry yg RCA ({year})'],
            width = 0.5,
            text = df_year[f'ACS Industry yg RCA ({year})'],
            hovertext = df_year[f'Workforce by Industry and Gender ({year})'],
            texttemplate = '%{text:.2f}',
            marker_color = [app_colors["primary"]] + [app_colors["secondary"]] * 4,
            hovertemplate =
                '<b>%{x}</b><br>'+
                '<b>RCA</b>: %{y}<br>'+
                '<b>Workforce</b>: %{hovertext}<extra></extra>'
        )
    )

    figure.update_layout(
        xaxis = go.layout.XAxis(
            tickmode = 'array',
            tickangle = 0,
            tickvals = [*range(len(df_year['Industry']))],
            tickfont_size = 8,
            ticktext = [f'{" ".join(i.split(" ")[:2])}<br>{" ".join(i.split(" ")[2:])}' for i in df_year['Industry']],
            showgrid = False
        ),
        yaxis = go.layout.YAxis(
            title = "<b>Industry RCA</b>",
            title_font_size = 10,
            tickfont_size = 10,
            showgrid = False,
            zeroline=False
        ),
        height = 400,
        width = 500,
        margin = dict(l = 10, r = 20, t = 0, b = 10),
        plot_bgcolor = app_colors['background'],
        paper_bgcolor = app_colors['background']
    )

    return figure

def plot_property_income(df, year):
    df_year = df.loc[df['Year'] == year]
    df_year['Affordability'] = df_year['Household Income by Race'] / df_year['Property Value']
    us_pos = df_year.loc[df_year["Geography"] == "United States", :]
    mn_pos = df_year.loc[df_year["Geography"] == "Minnesota", :]
    rlc_pos = df_year.loc[df_year["Geography"] == "Red Lake County, MN", :]
    df_year['is_rlc'] = df_year.apply(lambda x: x['Geography'] == "Red Lake County, MN", axis = 1)
    colors = {True: app_colors["primary"], False: app_colors["secondary"]}

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x = df_year['Property Value'],
            y = df_year['Affordability'],
            mode = 'markers',
            text = df_year["Geography"],
            hovertext = df_year['Household Income by Race'],
            marker_size = 12,
            marker_color = [colors[k] for k in df_year['is_rlc']],
            hovertemplate =
                '<b>%{text}</b><br>'+
                '<b>Property Value</b>: %{x}<br>'+
                '<b>Household Income</b>: %{hovertext}<extra></extra>'
        )
    )
    figure.update_layout(
        xaxis = go.layout.XAxis(
            title = "<b>Property Value</b>",
            title_font_size = 10,
            tickfont_size = 10,
            showgrid = False),
        yaxis = go.layout.YAxis(
            title = "<b>Housing Affordability</b>",
            title_font_size = 10,
            tickfont_size = 10,
            showgrid = False),
        autosize = True,
        height = 400,
        width = 450,
        margin = dict(l = 10, r = 20, t = 0, b = 10),
        plot_bgcolor = app_colors['background'],
        paper_bgcolor = app_colors['background']
    )

    figure.add_annotation(
        x = us_pos["Property Value"].values[0] + 20000,
        y = us_pos["Affordability"].values[0] - 0.01,
        xref = "x",
        yref = "y",
        text = "United States",
        showarrow = False
    )

    figure.add_annotation(
        x = mn_pos["Property Value"].values[0] + 20000,
        y = mn_pos["Affordability"].values[0] - 0.01,
        xref = "x",
        yref = "y",
        text = "Minnesota",
        showarrow = False
    )

    figure.add_annotation(
        x = rlc_pos["Property Value"].values[0] + 20000,
        y = rlc_pos["Affordability"].values[0] - 0.01,
        xref = "x",
        yref = "y",
        text = "Red Lake County",
        showarrow = False
    )

    return figure

def season_selection(season):
    if season == "winter":
        selection_bounds = {'x0': -0.5, 'x1': 2.5, 'y0': 0, 'y1': 40}
    elif season == "spring":
        selection_bounds = {'x0': 2.5, 'x1': 5.5, 'y0': 0, 'y1': 72}
    elif season == "summer":
        selection_bounds = {'x0': 5.5, 'x1': 8.5, 'y0': 0, 'y1': 75}
    else:
        selection_bounds = {'x0': 8.5, 'x1': 11.5, 'y0': 0, 'y1': 50}
    
    return selection_bounds

def plot_climate(df, year, season):
    df_year = df.loc[df['YEAR'] == year]
    df_year['MONTH'] = pd.to_datetime(df_year['MONTH'], format='%m').dt.month_name().str.slice(stop=3)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            name = "Temperature",
            x = df_year["MONTH"],
            y = df_year['TAVG'],
            textposition = 'top center',
            mode = 'markers+lines+text',
            marker_size = 8,
            marker_color = app_colors["secondary"]
        )
    )

    figure.add_trace(
        go.Bar(
            name = "Precipitation",
            x = df_year["MONTH"],
            y = df_year['PRCP'],
            width = 0.5,
            marker_color = app_colors["primary"],
            yaxis = 'y2'
        )
    )

    figure.update_layout(
        xaxis = go.layout.XAxis(
            tickfont_size = 10,
            showgrid = False
        ),
        yaxis = go.layout.YAxis(
            title = "<b>Average Temperature (°F)</b>",
            title_font_size = 10,
            tickfont_size = 10,
            showgrid = False,
            zeroline = False,
            range = [0, 80]
        ),
        yaxis2 = go.layout.YAxis(
            title = "<b>Precipitation (in)</b>",
            title_font_size = 10,
            tickfont_size = 10,
            showgrid = False,
            zeroline = False,
            overlaying = 'y',
            side = 'right',
            range = [0, 8]
        ),
        height = 300,
        width = 540,
        margin = dict(l = 10, r = 20, t = 0, b = 10),
        plot_bgcolor = app_colors['background'],
        paper_bgcolor = app_colors['background'],
        legend = dict(
            xanchor = 'center',
            x = 0.5,
            orientation = 'h',
            font_size = 8
        ),
        hovermode='x unified'
    )

    figure.add_shape(
        dict({
                'type': 'rect',
                'line': {'width': 1, 'dash': 'dot', 'color': 'grey'}
            }, **season_selection(season)))

    return figure

@app.callback(
    [Output('industry', 'figure')],
    [Input('select-year', 'value')]
)
def update_industry(year):
    figure = plot_industry(industry, year)
    return [figure]

@app.callback(
    [Output('property-income', 'figure')],
    [Input('select-year', 'value')]
)
def update_property_income(year):
    figure = plot_property_income(property_income, year)
    return [figure]

@app.callback(
    [Output('season-climate', 'figure')],
    [Input('select-year', 'value'),
    Input('select-season', 'value')]
)
def update_climate(year, season):
    figure = plot_climate(climate, year, season)
    return [figure]

@app.callback(
    [Output('season-img', 'src'),
    Output('rlc-season', 'children'),
    Output('what-to-do', 'children')],
    [Input('select-season', 'value')]
)
def update_img(season):
    src = app.get_asset_url(f'images/{season}.jpg')
    rlc_season = f"Red Lake County in the {season.title()}"

    if season == "winter":
        season_activity = "Ski and skate across the surface of Red Lake River!"
    elif season == "spring":
        season_activity = "See the green trees bloom all around Red Lake County!"
    elif season == "summer":
        season_activity = "Fish in the Red Lake River for bass and walleye!"
    else:
        season_activity = "Kayak down Red Lake River and admire the green-gold landscape!"
    return [src, rlc_season, season_activity]

app.layout = html.Div(
    [
        header,
        html.Br(),
        body
    ]
)

if __name__ == '__main__':
    app.run_server(debug = False)
