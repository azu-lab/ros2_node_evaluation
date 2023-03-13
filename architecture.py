from caret_analyze import Architecture, check_procedure, Application, Lttng
# from caret_analyze.plot import message_flow
# from bokeh.plotting import output_notebook, figure, show, output_file
# from bokeh.io import export_svgs

def generate_architecture(select_tracedatapath, datepath):
	architecturepath = datepath + '/' + select_tracedatapath.rsplit('/', 1)[1] + '.yaml'
	arch = Architecture('lttng', select_tracedatapath)
	arch.export(architecturepath)
