import matplotlib.pyplot as plt

def plot_data(data):

	data_c = data["consumption"]
	x_data_c = data_c['time']
	y_data_c = data_c['values']
	
	data_p = data["production"]
	x_data_p = data_p['time']
	y_data_p = data_p['values']
	
	data_i = data["import"]
	x_data_i = data_i['time']
	y_data_i = data_i['values']
	
	plt.figure()
	
	plt.subplot(2,1,1)
	plt.plot(x_data_c, y_data_c, label="Kulutus")
	plt.plot(x_data_p, y_data_p, label="Tuotanto")
	plt.plot(x_data_i, y_data_i, label="Tuonti")
	plt.legend()
	plt.title("Yleiskatsaus", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)
	
	plt.subplot(2,1,2)
	plt.plot(data["import_russia"]['time'], data["import_russia"]['values'], label="Tuonti Venäjältä")
	plt.plot(data["import_estonia"]['time'], data["import_estonia"]['values'], label="Tuonti Virosta")
	plt.plot(data["import_sweden"]['time'], data["import_sweden"]['values'], label="Tuonti Ruotsista (pohjoinen)")
	plt.plot(data["import_sweden_mid"]['time'], data["import_sweden_mid"]['values'], label="Tuonti Ruotsista (keski)")
	plt.plot(data["import_sweden_aland"]['time'], data["import_sweden_aland"]['values'], label="Tuonti Ruotsista (Ahvenanmaa)")
	plt.plot(data["import_norway"]['time'], data["import_norway"]['values'], label="Tuonti Norjasta")
	plt.legend()
	plt.title("Tuonnin erittely", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)
	
	#import pdb; pdb.set_trace()
	
	plt.show()