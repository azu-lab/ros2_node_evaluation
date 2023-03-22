from caret_analyze import Architecture, check_procedure, Application, Lttng
from caret_analyze.plot import Plot
from caret_analyze import Application, Architecture, Lttng
from bokeh.plotting import output_notebook, figure, show
from caret_analyze.plot import message_flow
from caret_analyze.plot import chain_latency
from bokeh.plotting import save
from bokeh.resources import CDN
import sys
import os



def visualize(message_flow_bln, chain_latency_bln, response_time_bln, app, datepath, now):

    if message_flow_bln:
        # export_path = os.getenv('LD_PRELOAD')
        path = app.get_path('target_path')
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        figure = message_flow(path, granularity='node', lstrip_s=1, rstrip_s=1)
        figure_path = datepath + '/message_flow_' + now
        figure_html = figure_path + '.html'
        print(figure_html)
        save(figure, figure_html, resources=CDN)
        # os.environ['LD_PRELOAD'] = export_path
        # figure_path = datepath + '/message_flow_' + now
        # figure_html = figure_path + '.html'
        # plot.save(figure_html)
        # fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)

    if chain_latency_bln:
        # export_path = os.getenv('LD_PRELOAD')
        path = app.get_path('target_path')
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        chain_latency(path, granularity='node', lstrip_s=1, rstrip_s=1)
        # os.environ['LD_PRELOAD'] = export_path
        # figure_path = datepath + '/chain_latency_' + now
        # figure_html = figure_path + '.html'
        # plot.save(figure_html)
        # fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)


    if response_time_bln:
        # export_path = os.getenv('LD_PRELOAD')
        path = app.get_path('target_path')
        # plot best-to-worst case
        plot = Plot.create_response_time_histogram_plot(path)
        figure = plot.show()
        figure_path = datepath + '/response_time_' + now
        figure_html = figure_path + '.html'
        save(figure, figure_html, resources=CDN)
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        # plot.show()
        # os.environ['LD_PRELOAD'] = export_path
        # figure_path = datepath + '/response_time_' + now
        # figure_html = figure_path + '.html'
        # plot.save(figure_html)
        # fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)




