import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd
from bokeh.models import ColumnDataSource, Range1d, Span
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, save


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
                               "Resources", "Customer", "Color"])
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


def make_gantt(df: pd.DataFrame, gantt_html: str, html_height: int,
               html_width: int) -> \
        None:
    """
    Make the Gantt Bokeh HTML
    :param df: Database Dataframe
    :param gantt_html: Name of the save Gantt HTML
    :param html_height: HTML Height
    :param html_width: HTML Width
    :return: None
    """
    current_dt = date.today()
    TOOLS = "save,pan,box_zoom,reset,wheel_zoom,tap"

    gantt = figure(title='Project Schedule', x_axis_type='datetime',
                   width=html_width, height=html_height, y_range=df.Name,
                   x_range=Range1d(df.Start_DT.min(), df.End_DT.max()),
                   tools=TOOLS)

    hover = HoverTool(tooltips="Task: @Name<br>\
    Start: @Start<br>\
    End: @End<br>\
    Customer: @Customer")
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


def gantt_cli() -> argparse.Namespace:
    """
    Command Line Interface to gather command line args into a single Namespace
    :return Namespace of all the command line args
    """
    # Create the parser with a helpful description of its purpose and a
    # formatting class that prints the default values in the command argument
    # descriptions.
    gantt_parser = argparse.ArgumentParser(
        description='Parses arguments for the Gantt Chart generator.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Add the positional and optional arguments to the parser. Optionals are
    # indicated by the flag names ('--') and have been assigned default values.
    # Additional arguments can be added if need be.
    gantt_parser.add_argument(
        'json',
        help='JSON containing the information to be plotted'
    )
    gantt_parser.add_argument(
        '-d', '--dest_html',
        default=Path.cwd() / "index.html",
        type=Path,
        help='Destination HTML file to create'
    )
    gantt_parser.add_argument(
        '-hh', '--height',
        default=400,
        type=int,
        help='Destination HTML Height'
    )
    gantt_parser.add_argument(
        '-wh', '--width',
        default=800,
        type=int,
        help='Destination HTML Width'
    )
    # Returns a namespace of parsed command arguments. Since the age threshold
    # has a default of None, it needs to be converted to an integer outside the
    # parser.
    return gantt_parser.parse_args()


def main() -> None:
    gantt_args = gantt_cli()
    db_dict = db_json_parse(gantt_args.json)
    db_dataframe = dict2df(db_dict)
    prepared_dataframe = prepare_df(db_dataframe)
    make_gantt(prepared_dataframe, gantt_args.dest_html, gantt_args.height,
               gantt_args.width)


if __name__ == "__main__":
    main()
