from datetime import datetime

import plotly.graph_objects as go
import pytz

import streamlit as st
from src.dagster_app.defs.noaa.models import ThreeDayForecast


class AuroraForecastTable:
    def __init__(self, forecast_data: ThreeDayForecast):
        self.data = forecast_data


def convert_time_periods_to_local(time_periods: list[str], target_timezone: str = "UTC"):
    """
    Convert UTC time periods to local timezone

    Args:
        time_periods: List of time period strings like "00-03", "03-06", etc.
        target_timezone: Target timezone string (default: Eastern Time)

    Returns:
        List of converted time period strings
    """
    try:
        utc = pytz.UTC
        local_tz = pytz.timezone(target_timezone)

        converted_periods = []
        for period in time_periods:
            if "-" in period:
                start_hour, end_hour = period.split("-")
                start_hour = int(start_hour)
                end_hour = int(end_hour)

                # Use a reference date to calculate timezone offset
                reference_date = datetime(2025, 1, 15, start_hour, 0, tzinfo=utc)
                local_time = reference_date.astimezone(local_tz)

                # Calculate local start and end hours
                local_start = local_time.hour
                local_end = (local_start + 3) % 24

                start_str = f"{local_start:02d}"
                end_str = f"{local_end:02d}"
                converted_periods.append(f"{start_str}-{end_str}")
            else:
                converted_periods.append(period)

        return converted_periods
    except Exception:
        return time_periods


def get_user_timezone():
    """Get user's timezone with a selectbox"""
    common_timezones = [
        ("UTC", "UTC"),
        ("America/New_York", "EST/EDT"),
        ("America/Chicago", "CST/CDT"),
        ("America/Denver", "MST/MDT"),
        ("America/Los_Angeles", "PST/PDT"),
        ("Europe/London", "GMT/BST"),
        ("Europe/Paris", "CET/CEST"),
        ("Europe/Berlin", "CET/CEST"),
        ("Asia/Tokyo", "JST"),
        ("Asia/Shanghai", "CST"),
        ("Australia/Sydney", "AEST/AEDT"),
    ]

    display_options = [f"{short_name}" for _, short_name in common_timezones]

    selected_index = st.selectbox(
        "Timezone:",
        options=range(len(display_options)),
        format_func=lambda x: display_options[x],
        index=0,
        key="timezone_selector",
    )

    return common_timezones[selected_index]


def get_kp_color(val):
    """Get color for Kp value"""
    try:
        numeric_val = float(val)
        if numeric_val < 4:
            return "rgba(0,0,0,0)"
        elif 4 <= numeric_val < 5:
            return "#90EE90"
        elif 5 <= numeric_val < 7:
            return "#FFFF99"
        elif 7 <= numeric_val <= 8.5:
            return "#FFA500"
        else:  # > 8.5
            return "#FF6B6B"
    except (ValueError, TypeError):
        return "#FFFFFF"


def create_kp_legend():
    """Create a horizontal gradient legend bar"""
    fig = go.Figure()

    # Define the gradient segments with proper spacing
    segments = [
        {"range": "0-4", "label": "Quiet", "color": "rgba(0,0,0,0)", "x_start": 0, "x_end": 2},
        {"range": "4-5", "label": "Unsettled", "color": "#90EE90", "x_start": 2, "x_end": 4},
        {"range": "5-7", "label": "Active - Minor Storm", "color": "#FFFF99", "x_start": 4, "x_end": 6},
        {"range": "7-8.5", "label": "Strong Storm", "color": "#FFA500", "x_start": 6, "x_end": 8},
        {"range": "8.5+", "label": "Severe Storm", "color": "#FF6B6B", "x_start": 8, "x_end": 10},
    ]

    for segment in segments:
        fig.add_shape(
            type="rect",
            x0=segment["x_start"],
            y0=0,
            x1=segment["x_end"],
            y1=1,
            fillcolor=segment["color"],
            line=dict(color="black", width=1),
        )

        # Add text labels with appropriate font color
        mid_x = (segment["x_start"] + segment["x_end"]) / 2
        # Use white font for transparent background, black font for colored backgrounds
        font_color = "white" if segment["color"] == "rgba(0,0,0,0)" else "black"
        fig.add_annotation(
            x=mid_x,
            y=0.5,
            text=f"{segment['range']}<br>({segment['label']})",
            showarrow=False,
            font=dict(size=11, color=font_color),
            align="center",
        )

    fig.update_layout(
        xaxis=dict(range=[0, 10], showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(range=[0, 1], showticklabels=False, showgrid=False, zeroline=False),
        height=40,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_kp_table(data: ThreeDayForecast, use_local_time=False, timezone_info=("UTC", "UTC")):
    """Create a color-coded table for the Kp forecast data"""
    df = data.to_dataframe()

    timezone_str, timezone_short = timezone_info

    header_values = [
        f"Time Period ({timezone_short if use_local_time and timezone_str != 'UTC' else 'UTC'})"
    ] + list(df.columns)
    time_periods = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-00"]

    if use_local_time and timezone_str != "UTC":
        # Calculate timezone offset properly
        utc = pytz.UTC
        local_tz = pytz.timezone(timezone_str)

        # Use current time to get accurate offset (accounts for DST)
        reference_time = datetime.now(utc)
        utc_offset = reference_time.astimezone(local_tz).utcoffset().total_seconds() / 3600

        # Calculate how many 3-hour periods to shift, rounding to nearest whole period
        shift_periods = round(utc_offset / 3)

        # Flatten all data into a single list for easier indexing across days
        all_values = []
        for col in df.columns:
            all_values.extend(list(df[col]))

        num_total_periods = len(all_values)

        # Reconstruct the table column by column (day by day) based on the local time
        new_daily_values = []
        for day_idx in range(len(df.columns)):
            day_values = [""] * 8
            for period_idx in range(8):
                # This is the index of the cell in the destination (local time) table
                local_flat_idx = day_idx * 8 + period_idx

                # Find the corresponding index in the source (UTC) data
                # The formula is utc_time = local_time - offset, so utc_idx = local_idx - shift
                utc_flat_idx = local_flat_idx - shift_periods

                if 0 <= utc_flat_idx < num_total_periods:
                    day_values[period_idx] = all_values[utc_flat_idx]
                # If the source index is out of bounds, the value remains ""

            new_daily_values.append(day_values)

        cell_values = [time_periods] + new_daily_values

        # Generate colors based on the new, shifted values
        cell_colors = [["rgba(0,0,0,0)"] * 8]
        cell_font_colors = [["white"] * 8]

        for col_values in new_daily_values:
            col_colors_for_day = []
            col_font_colors_for_day = []
            for val in col_values:
                bg_color = get_kp_color(val) if val != "" else "rgba(0,0,0,0)"
                col_colors_for_day.append(bg_color)
                font_color = "white" if bg_color == "rgba(0,0,0,0)" else "black"
                col_font_colors_for_day.append(font_color)
            cell_colors.append(col_colors_for_day)
            cell_font_colors.append(col_font_colors_for_day)

    else:
        # UTC display - original logic
        time_periods_utc = list(df.index)
        cell_values = [time_periods_utc]
        cell_colors = [["rgba(0,0,0,0)"] * len(df.index)]
        cell_font_colors = [["white"] * len(df.index)]

        for col in df.columns:
            cell_values.append(list(df[col]))
            col_colors_for_day = []
            col_font_colors_for_day = []
            for val in df[col]:
                bg_color = get_kp_color(val)
                col_colors_for_day.append(bg_color)
                font_color = "white" if bg_color == "rgba(0,0,0,0)" else "black"
                col_font_colors_for_day.append(font_color)
            cell_colors.append(col_colors_for_day)
            cell_font_colors.append(col_font_colors_for_day)

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=header_values,
                    fill_color="rgba(70, 130, 180, 0.8)",
                    align="center",
                    font=dict(size=13, color="white"),
                    line=dict(color="rgba(255,255,255,0.2)", width=1),
                ),
                cells=dict(
                    values=cell_values,
                    fill_color=cell_colors,
                    align="center",
                    font=dict(size=12, color=cell_font_colors),
                    height=30,
                    line=dict(color="rgba(128,128,128,0.3)", width=0.5),
                ),
            )
        ]
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def display_kp_forecast(data: ThreeDayForecast):
    """Display the Kp forecast with legend and timezone controls"""
    if data:
        st.write("**Geomagnetic Activity Levels:**")
        legend_fig = create_kp_legend()
        st.plotly_chart(legend_fig, use_container_width=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("#### Planetary K Index (Kp) 3-Day Forecast")
        with col2:
            use_local_time = st.toggle("Local time", value=False, key="time_toggle")
            if use_local_time:
                selected_timezone_info = get_user_timezone()
            else:
                selected_timezone_info = ("UTC", "UTC")

        forecast_fig = create_kp_table(data, use_local_time, selected_timezone_info)
        st.plotly_chart(forecast_fig, use_container_width=True)
    else:
        st.write("No forecast data available.")
