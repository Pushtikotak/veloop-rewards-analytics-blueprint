"""
VELOOP Rewards - Product Analytics Platform
Module: UI Components & Plotly Visualizations
Author: Pushti Kotak
Description: Commercial SaaS-grade Plotly chart builders, custom KPI card renderers,
and interactive export utilities.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Commercial SaaS Color Palette
PALETTE = {
    "navy": "#0A2540",
    "indigo": "#635BFF",
    "cyan": "#00D4B2",
    "sky": "#0EA5E9",
    "emerald": "#10B981",
    "amber": "#F59E0B",
    "rose": "#EF4444",
    "slate": "#64748B",
    "light_bg": "#F8FAFC",
    "card_bg": "#FFFFFF",
    "border": "#E2E8F0"
}

def apply_chart_theme(fig, title: str = ""):
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "font": {"size": 16, "family": "Inter, sans-serif", "color": PALETTE["navy"]},
            "x": 0.02,
            "y": 0.95
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": PALETTE["slate"], "size": 12},
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        hoverlabel={"bgcolor": PALETTE["navy"], "font_size": 13, "font_family": "Inter, sans-serif"},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5}
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#EDF2F7", zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#EDF2F7", zeroline=False)
    return fig

def render_kpi_card(title: str, value: str, delta: str = None, delta_type: str = "positive", tooltip: str = None):
    badge_bg = "#ECFDF5" if delta_type == "positive" else ("#FEF2F2" if delta_type == "negative" else "#EFF6FF")
    badge_color = "#047857" if delta_type == "positive" else ("#B91C1C" if delta_type == "negative" else "#1D4ED8")
    delta_icon = "↑" if delta_type == "positive" else ("↓" if delta_type == "negative" else "•")
    
    delta_html = f"""
    <div style="background-color: {badge_bg}; color: {badge_color}; padding: 3px 8px; border-radius: 9999px; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; margin-top: 6px;">
        <span>{delta_icon} {delta}</span>
    </div>
    """ if delta else ""
    
    tooltip_html = f'title="{tooltip}"' if tooltip else ""
    
    html = f"""
    <div {tooltip_html} style="background: {PALETTE['card_bg']}; border: 1px solid {PALETTE['border']}; border-radius: 12px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 600; color: {PALETTE['slate']}; text-transform: uppercase; letter-spacing: 0.5px;">{title}</div>
        <div style="font-size: 26px; font-weight: 800; color: {PALETTE['navy']}; margin-top: 4px; font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';">{value}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_business_insight(title: str, takeaway: str, action: str):
    html = f"""
    <div style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border-left: 4px solid {PALETTE['indigo']}; border-radius: 8px; padding: 16px 20px; margin: 16px 0 24px 0;">
        <div style="font-size: 14px; font-weight: 700; color: {PALETTE['navy']}; margin-bottom: 4px;">
            💡 Business Insight: {title}
        </div>
        <div style="font-size: 13px; color: #1E293B; line-height: 1.5; margin-bottom: 6px;">
            <b>Takeaway:</b> {takeaway}
        </div>
        <div style="font-size: 12px; color: {PALETTE['indigo']}; font-weight: 600;">
            🚀 Recommended Action: {action}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def plot_dual_axis_trend(df: pd.DataFrame, x_col: str, bar_col: str, line_col: str, title: str, bar_name: str, line_name: str):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[x_col],
        y=df[bar_col],
        name=bar_name,
        marker_color=PALETTE["indigo"],
        opacity=0.85,
        yaxis="y"
    ))
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[line_col],
        name=line_name,
        mode="lines+markers",
        marker=dict(color=PALETTE["cyan"], size=6),
        line=dict(color=PALETTE["cyan"], width=3),
        yaxis="y2"
    ))
    fig.update_layout(
        yaxis=dict(title=dict(text=bar_name, font=dict(color=PALETTE["indigo"]))),
        yaxis2=dict(title=dict(text=line_name, font=dict(color=PALETTE["cyan"])), overlaying="y", side="right")
    )
    return apply_chart_theme(fig, title)

def plot_funnel(stages: list, values: list, title: str):
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent previous+percent initial",
        marker={"color": [PALETTE["navy"], PALETTE["indigo"], PALETTE["cyan"], PALETTE["emerald"]]}
    ))
    return apply_chart_theme(fig, title)

def plot_donut(labels: list, values: list, title: str, hole: float = 0.6):
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(colors=[PALETTE["indigo"], PALETTE["cyan"], PALETTE["sky"], PALETTE["amber"], PALETTE["rose"]]),
        textinfo="percent+label"
    )])
    return apply_chart_theme(fig, title)

def plot_stacked_bar(df: pd.DataFrame, x_col: str, y_col: str, color_col: str, title: str):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        color_discrete_sequence=[PALETTE["indigo"], PALETTE["cyan"], PALETTE["sky"], PALETTE["amber"]],
        barmode="stack"
    )
    return apply_chart_theme(fig, title)

def plot_waterfall(categories: list, values: list, title: str):
    fig = go.Figure(go.Waterfall(
        name="Balance Delta",
        orientation="v",
        measure=["relative"] * (len(categories) - 1) + ["total"],
        x=categories,
        textposition="outside",
        text=[f"{v:+,.0f}" for v in values[:-1]] + [f"{values[-1]:,.0f}"],
        y=values,
        connector={"line": {"color": PALETTE["slate"]}},
        increasing={"marker": {"color": PALETTE["emerald"]}},
        decreasing={"marker": {"color": PALETTE["rose"]}},
        totals={"marker": {"color": PALETTE["navy"]}}
    ))
    return apply_chart_theme(fig, title)

def plot_heatmap(z_matrix: list, x_labels: list, y_labels: list, title: str):
    fig = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=x_labels,
        y=y_labels,
        colorscale=[[0, "#F8FAFC"], [0.5, "#A5B4FC"], [1.0, PALETTE["indigo"]]],
        hoverongaps=False
    ))
    return apply_chart_theme(fig, title)

def export_dataframe_button(df: pd.DataFrame, filename: str, label: str = "📥 Download CSV Report"):
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv_bytes,
        file_name=filename,
        mime="text/csv"
    )
