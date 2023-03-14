from caret_analyze import Architecture, check_procedure, Application, Lttng
from caret_analyze.plot import Plot
from caret_analyze import Application, Architecture, Lttng
from bokeh.plotting import output_notebook, figure, show
from bokeh.io import export_svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import sys
import os




def visualize(callbackname, latency_bln, frequency_bln, period_bln, app, datepath, now):


    if latency_bln:
        export_path = os.getenv('LD_PRELOAD')
        print(export_path)
        get_callback = []
        callbackname_list = callbackname.split(',')
        for re_callbackname_list in callbackname_list:
            callback = app.get_callback(re_callbackname_list)
            get_callback.append(callback)
        plot = Plot.create_latency_timeseries_plot(get_callback)
        # callback_df = plot.to_dataframe()
        # print(callback_df)
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        # plot.show()
        figure_path = datepath + '/latency_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html)
        fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)


        figure_path = datepath + '/latency_index_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html, xaxis_type = 'index')
        fig = plot.figure(xaxis_type='index')
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)

        
        # os.environ['LD_PRELOAD'] = export_path
        # export_pathcmd = '$(readlink -f ' + export_path + ')'
        # os.environ['LD_PRELOAD'] = export_pathcmd

        # export_path_cmd = 'export LD_PRELOAD=$(readlink -f ' + export_path + ')'
        # env_result = subprocess.run(export_path_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # export = os.getenv('LD_PRELOAD')
        # print(export_pathcmd)
        # print(export)

    if frequency_bln:
        export_path = os.getenv('LD_PRELOAD')
        get_callback = []
        callbackname_list = callbackname.split(',')
        for re_callbackname_list in callbackname_list:
            callback = app.get_callback(re_callbackname_list)
            get_callback.append(callback)
        plot = Plot.create_frequency_timeseries_plot(get_callback)
        # callback_df = plot.to_dataframe()
        # print(callback_df)
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        # plot.show()
        figure_path = datepath + '/frequency_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html)
        fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)


        figure_path = datepath + '/frequency_index_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html, xaxis_type = 'index')
        fig = plot.figure(xaxis_type='index')
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)

        os.environ['LD_PRELOAD'] = export_path

    if period_bln:
        export_path = os.getenv('LD_PRELOAD')
        get_callback = []
        callbackname_list = callbackname.split(',')
        for re_callbackname_list in callbackname_list:
            callback = app.get_callback(re_callbackname_list)
            get_callback.append(callback)
        plot = Plot.create_period_timeseries_plot(get_callback)
        # callback_df = plot.to_dataframe()
        # print(callback_df)
        # if os.getenv('LD_PRELOAD'):
        #     del os.environ['LD_PRELOAD']
        # plot.show()
        figure_path = datepath + '/period_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html)
        fig = plot.figure()
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)

        
        figure_path = datepath + '/period_index_' + now
        figure_html = figure_path + '.html'
        plot.save(figure_html, xaxis_type = 'index')
        fig = plot.figure(xaxis_type='index')
        # figure_svg = figure_path + '.svg'
        # export_svg(fig, filename = figure_svg)

        os.environ['LD_PRELOAD'] = export_path
