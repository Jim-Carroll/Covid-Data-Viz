#!/usr/bin/env python

import http.client
import json
import datetime
import plotly.graph_objects as go

class SFCovidDataSet:
    _URL: str = "data.sfgov.org"
    
    def __init__(self, resource: str):
        conn = http.client.HTTPSConnection(self._URL);
        conn.request("GET", resource)
        resp = conn.getresponse()
        self.json_data = json.loads(resp.read())


def convdate(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')

    
def gen_xy_tuples(data, x, y, pred=lambda _x: True):
    return [(convdate(entry[x]), int(entry[y]))
            for entry in data if pred(entry)]

if __name__ == "__main__":
    deaths_over_time_resource = "/resource/g2di-xufg.json"
    cases_over_time_resource = "/resource/gyr2-k29z.json"
    hospitalizations_over_time_resource = "/resource/nxjg-bhem.json"

    dot = SFCovidDataSet(deaths_over_time_resource)
    cot = SFCovidDataSet(cases_over_time_resource)
    hot = SFCovidDataSet(hospitalizations_over_time_resource)

    dot_xy = gen_xy_tuples(dot.json_data, x="date_of_death", y='new_deaths')
    cot_xy = gen_xy_tuples(cot.json_data, x="specimen_collection_date", y="new_cases")
    hot_xy = gen_xy_tuples(hot.json_data, x="reportdate", y="patientcount", pred=lambda e: e['covidstatus'] == 'COVID+')
    
    fig = go.Figure(layout_title_text='Covid-19 Cases, Hospitalizations & Deaths in San Francisco vs. Time')
    
    fig.add_trace(go.Scatter(x=[e[0] for e in cot_xy],
                             y=[e[1] for e in cot_xy],
                             mode='lines+markers',
                             name='Cases'))
    fig.add_trace(go.Scatter(x=[e[0] for e in hot_xy],
                             y=[e[1] for e in hot_xy],
                             mode='lines+markers',
                             name='Hospitalized'))
    fig.add_trace(go.Scatter(x=[e[0] for e in dot_xy],
                             y=[e[1] for e in dot_xy],
                             mode='lines+markers',
                             name='Deaths'))
#    fig.update_yaxes(type='log', range=[0, 3])
    fig.show()
