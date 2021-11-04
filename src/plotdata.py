import matplotlib.pyplot as plt


PLOT_OVERALL = ['consumption','production','import']
PLOT_IMPORT =  ['import_russia', 'import_estonia', 'import_sweden', 'import_sweden_mid', 'import_sweden_aland', 'import_norway']

def plot_data(data):

	plt.figure()
	
	plt.subplot(2,1,1)
	for name in PLOT_OVERALL:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend()
	plt.title("Yleiskatsaus", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)
	
	plt.subplot(2,1,2)
	for name in PLOT_IMPORT:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend()
	plt.title("Tuonnin erittely", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)
	
	plt.show()