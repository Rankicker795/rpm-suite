import json
import sys
from datetime import date

import pandas as pd
from bokeh.models import ColumnDataSource, Range1d, Span
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, savek


def db_json_parse(json_file: str) -> dict:
    """
    Parse the JSON data into a dict
    :param json_file: JSON file containing the Gantt Database
    :return: Dict representation of JSON file
    """
    with open(json_file, "r") as jh:
        data = json.load(jh)
    return data


def dict2df(db_dict: dict) -> pd.DataFrame:
    """
    Convert the JSON to a Pandas DataFrame
    :param db_dict: Database Dict
    :return: Dataframe version of db
    """
    df = pd.DataFrame(columns=["Name", "Start-Date", "End-Date",
                               "Resources", "Color"])
    tasks = db_dict.values()
    for t in tasks:
        df = df.append(t, ignore_index=True, sort=False)
    return df


def prepare_df(db_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the Dataframe for Bokeh
    :param db_df: Database Dataframe
    :return: Altered Database Dataframe
    """
    db_df[['Start_DT', 'End_DT']] = db_df[['Start', 'End']].apply(
        pd.to_datetime)
    db_df = db_df.sort_values(by="Start_DT", ascending=False,
                              ignore_index=True)
    db_df['ID'] = db_df.index + 0.25
    db_df['ID1'] = db_df.index + 0.75
    return db_df


def make_gantt(df: pd.DataFrame, gantt_html: str) -> None:
    """
    Make the Gantt Bokeh HTML
    :param df: Database Dataframe
    :param gantt_html: Name of the save Gantt HTML
    :return: None
    """
    current_dt = date.today()
    TOOLS = "save,pan,box_zoom,reset,wheel_zoom,tap"

    gantt = figure(title='Project Schedule', x_axis_type='datetime', width=800,
               height=400, y_range=df.Name,
               x_range=Range1d(df.Start_DT.min(), df.End_DT.max()),
               tools=TOOLS)

    hover = HoverTool(tooltips="Task: @Name<br>\
    Start: @Start<br>\
    End: @End")
    gantt.add_tools(hover)

    CDS = ColumnDataSource(df)
    gantt.quad(left='Start_DT', right='End_DT', bottom='ID', top='ID1',
               source=CDS, color="Color", legend_group="Resources")
    current_date = Span(location=current_dt,
                        dimension='height', line_color='purple',
                        line_dash='dashed', line_width=3)
    gantt.add_layout(current_date)
    gantt.legend.title = "Resources"
    save(gantt, gantt_html)


def main(json_file: str, gantt_html: str) -> None:
    db_dict = db_json_parse(json_file)
    db_dataframe = dict2df(db_dict)
    prepared_dataframe = prepare_df(db_dataframe)
    make_gantt(prepared_dataframe, gantt_html)


if __name__ == "__main__":
    database_json = sys.argv[1]
    gantt_name = "test.html"
    main(database_json, gantt_name)
