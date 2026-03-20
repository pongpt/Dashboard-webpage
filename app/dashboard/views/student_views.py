import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from django.shortcuts import render
from django.conf import settings

# ──────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────

FILE_NAME = 'cleaned_survey_satisfaction_656667_full'

CAMPUSES = ['ศ.ท่าพระจันทร์', 'ศ.รังสิต', 'ศ.ลำปาง', 'ศ.พัทยา', 'มธ.ภาพรวม']
LEVELS   = ['ระดับ1', 'ระดับ2', 'ระดับ3', 'ระดับ4', 'ระดับ5']
COLORS   = {
    'ศ.ท่าพระจันทร์': '#8B0000',
    'ศ.รังสิต'      : '#DAA520',
    'ศ.ลำปาง'       : '#1a5276',
    'ศ.พัทยา'       : '#1e8449',
    'มธ.ภาพรวม'     : '#6c3483',
}


# ──────────────────────────────────────────
#  Data Loader
# ──────────────────────────────────────────

def load_student_data():
    data_dir = os.path.join(settings.BASE_DIR, 'data')
    for ext in ['.csv', '.xlsx', '.xls']:
        path = os.path.join(data_dir, FILE_NAME + ext)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path) if ext == '.csv' else pd.read_excel(path)
                return clean_numeric_columns(df)
            except Exception:
                return None
    return None


def clean_numeric_columns(df):
    """แปลง column ที่ควรเป็นตัวเลขทั้งหมดให้เป็น numeric"""
    for campus in CAMPUSES:
        # แปลง _จำนวน
        col_total = f'{campus}_จำนวน'
        if col_total in df.columns:
            df[col_total] = pd.to_numeric(df[col_total], errors='coerce').fillna(0)

        # แปลง _ระดับ1–5 และ _%ระดับ1–5
        for lvl in LEVELS:
            for prefix in ['', '%']:
                col = f'{campus}_{prefix}{lvl}' if prefix else f'{campus}_{lvl}'
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


# ───────────────────────────���──────────────
#  Data Transformers
# ──────────────────────────────────────────

def calc_avg_score(df, campus):
    """คำนวณคะแนนเฉลี่ย weighted ของวิทยาเขต"""
    total_col = f'{campus}_จำนวน'
    if total_col not in df.columns:
        return 0, 0
    total     = df[total_col].sum()
    score_sum = sum(
        df[f'{campus}_{lvl}'].sum() * (i + 1)
        for i, lvl in enumerate(LEVELS)
        if f'{campus}_{lvl}' in df.columns
    )
    return (round(score_sum / total, 3), int(total)) if total > 0 else (0, 0)


def get_avg_by_campus(df):
    rows = []
    for campus in CAMPUSES:
        avg, total = calc_avg_score(df, campus)
        rows.append({'วิทยาเขต': campus, 'คะแนนเฉลี่ย': avg, 'จำนวนผู้ตอบ': total})
    return pd.DataFrame(rows)


def get_level_distribution(df, campus='มธ.ภาพรวม'):
    rows = []
    for i, lvl in enumerate(LEVELS, start=1):
        col = f'{campus}_{lvl}'
        if col in df.columns:
            rows.append({'ระดับ': f'ระดับ {i}', 'จำนวน': int(df[col].sum())})
    return pd.DataFrame(rows)


def get_trend_by_year(df, campus='มธ.ภาพรวม'):
    rows = []
    for year in sorted(df['ปีการศึกษา'].unique()):
        year_df = df[df['ปีการศึกษา'] == year]
        avg, _  = calc_avg_score(year_df, campus)
        rows.append({'ปีการศึกษา': str(year), 'คะแนนเฉลี่ย': avg})
    return pd.DataFrame(rows)


def get_category_avg(df, campus='มธ.ภาพรวม'):
    rows = []
    for cat, group in df.groupby('หมวดหมู่'):
        avg, _ = calc_avg_score(group, campus)
        rows.append({'หมวดหมู่': cat, 'คะแนนเฉลี่ย': avg})
    return pd.DataFrame(rows)


def get_radar_data(df):
    categories = df['หมวดหมู่'].unique().tolist()
    result     = {'หมวดหมู่': categories}
    for campus in CAMPUSES[:-1]:
        scores = []
        for cat in categories:
            avg, _ = calc_avg_score(df[df['หมวดหมู่'] == cat], campus)
            scores.append(avg)
        result[campus] = scores
    return pd.DataFrame(result)


# ──────────────────────────────────────────
#  Chart Builders
# ──────────────────────────────────────────

def make_bar_campus(df_avg):
    fig = px.bar(
        df_avg,
        x='วิทยาเขต', y='คะแนนเฉลี่ย',
        color='วิทยาเขต', text='คะแนนเฉลี่ย',
        title='คะแนนเฉลี่ยความพึงพอใจรายวิทยาเขต',
        color_discrete_map=COLORS,
        hover_data=['จำนวนผู้ตอบ'],
        template='plotly_white',
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(yaxis_range=[0, 5], showlegend=False,
                      yaxis_title='คะแนนเฉลี่ย (1–5)', title_font_size=18)
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def make_pie_level(df_dist):
    fig = px.pie(
        df_dist, names='ระดับ', values='จำนวน',
        title='สัดส่วนระดับความพึงพอใจ (มธ. ภาพรวม)',
        color_discrete_sequence=['#c0392b','#e67e22','#f1c40f','#2ecc71','#1a5276'],
        hole=0.38, template='plotly_white',
    )
    fig.update_layout(title_font_size=18)
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def make_line_trend(df_trend):
    fig = px.line(
        df_trend, x='ปีการศึกษา', y='คะแนนเฉลี่ย',
        title='แนวโน้มความพึงพอใจรายปีการศึกษา (มธ. ภาพรวม)',
        markers=True, color_discrete_sequence=['#8B0000'],
        template='plotly_white',
    )
    fig.update_traces(line_width=3, marker_size=10)
    fig.update_layout(yaxis_range=[0, 5], yaxis_title='คะแนนเฉลี่ย (1–5)',
                      title_font_size=18)
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def make_hbar_category(df_cat):
    df_cat = df_cat.sort_values('คะแนนเฉลี่ย')
    fig = px.bar(
        df_cat, x='คะแนนเฉลี่ย', y='หมวดหมู่',
        orientation='h', text='คะแนนเฉลี่ย',
        title='คะแนนเฉลี่ยความพึงพอใจรายหมวดหมู่',
        color='คะแนนเฉลี่ย', color_continuous_scale='RdYlGn',
        template='plotly_white',
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_range=[0, 5], xaxis_title='คะแนนเฉลี่ย (1–5)',
                      coloraxis_showscale=False, title_font_size=18)
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def make_radar_campus(df_radar):
    categories = df_radar['หมวดหมู่'].tolist()
    fig        = go.Figure()
    for campus in CAMPUSES[:-1]:
        if campus not in df_radar.columns:
            continue
        vals = df_radar[campus].tolist() + [df_radar[campus].tolist()[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=categories + [categories[0]],
            fill='toself', name=campus,
            line_color=COLORS.get(campus), opacity=0.65,
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        title='เปรียบเทียบความพึงพอใจรายวิทยาเขต',
        title_font_size=18, template='plotly_white',
        legend=dict(orientation='h', y=-0.25),
    )
    return json.dumps(fig, cls=PlotlyJSONEncoder)


# ──────────────────────────────────────────
#  View
# ──────────────────────────────────────────

def dashboard_student(request):
    df = load_student_data()

    if df is None:
        return render(request, 'dashboard/student_dashboard.html', {
            'active_tab': 'student',
            'charts'    : [],
            'error'     : f'ไม่พบไฟล์ {FILE_NAME}.csv/.xlsx ใน app/data/',
        })

    charts = [
        {'id': 'chart_bar_campus', 'json': make_bar_campus(get_avg_by_campus(df))},
        {'id': 'chart_pie_level',  'json': make_pie_level(get_level_distribution(df))},
        {'id': 'chart_line_trend', 'json': make_line_trend(get_trend_by_year(df))},
        {'id': 'chart_hbar_cat',   'json': make_hbar_category(get_category_avg(df))},
        {'id': 'chart_radar',      'json': make_radar_campus(get_radar_data(df))},
    ]

    return render(request, 'dashboard/student_dashboard.html', {
        'active_tab': 'student',
        'charts'    : charts,
        'row_count' : len(df),
        'error'     : None,
    })