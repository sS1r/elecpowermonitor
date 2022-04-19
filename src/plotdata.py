import matplotlib.pyplot as plt


PLOT_OVERALL = ['consumption','production','import']
PLOT_IMPORT =  ['import_russia', 'import_estonia', 'import_sweden', 'import_sweden_mid', 'import_sweden_aland', 'import_norway']

def plot_overall(data):
	for name in PLOT_OVERALL:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend(loc='upper right')
	plt.title("Yleiskatsaus", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	# ax.xaxis.labelpad=-5
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)

def plot_import(data):
	for name in PLOT_IMPORT:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend(loc='upper right')
	plt.title("Tuonnin erittely", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)

def plot_data(data):

	plt.figure()

	ax = plt.subplot(2,1,1)
	plot_overall(data)

	plt.subplot(2,1,2)
	plot_import(data)

	# Adds space between the subplots
	plt.tight_layout(h_pad=-2.0)
	
	plt.show()