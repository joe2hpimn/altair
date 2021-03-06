'''
US Population Pyramid Over Time
===============================
A population pyramid shows the distribution of age groups within a population.
It uses a slider widget that is bound to the year to visualize the age
distribution over time.
'''
# category: case studies
import altair as alt
from vega_datasets import data

pop = data.population.url

slider = alt.binding_range(min=1850, max=2000, step=10)
select_year = alt.selection_single(name='year', fields=['year'], bind=slider)

base = alt.Chart(pop).add_selection(
    select_year
).transform_filter(
    select_year
).transform_calculate(
    gender=alt.expr.if_(alt.datum.sex == 1, 'Male', 'Female')
)

title = alt.Axis(title='population')
color_scale = alt.Scale(domain=['Male', 'Female'],
                        range=['#1f77b4', '#e377c2'])

left = base.transform_filter(
    alt.datum.gender == 'Female'
).encode(
    y=alt.X('age:O', axis=None),
    x=alt.X('sum(people):Q', axis=title, sort=alt.SortOrder('descending')),
    color=alt.Color('gender:N', scale=color_scale, legend=None)
).mark_bar().properties(title='Female')

middle = base.encode(
    y=alt.X('age:O', axis=None),
    text=alt.Text('age:Q'),
).mark_text().properties(width=20)

right = base.transform_filter(
    alt.datum.gender == 'Male'
).encode(
    y=alt.X('age:O', axis=None),
    x=alt.X('sum(people):Q', axis=title),
    color=alt.Color('gender:N', scale=color_scale, legend=None)
).mark_bar().properties(title='Male')

left | middle | right
