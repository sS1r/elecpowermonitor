import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime, timedelta

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

def plot_elecprice(data):

	now = datetime.now()
	nowstr = now.strftime("%d.%m.%Y klo %H:%M")
	for t in data.time:
		if t.replace(tzinfo=None) > now:
			i_nearest = data.time.index(t) - 1
			t_nearest = data.time[i_nearest].replace(tzinfo=None)
			t_next = t
			break
	pricenow = data.prices[i_nearest]
	notestr = "Hinta {}:\n{:.3f} EUR/kWh".format(nowstr, pricenow)

	#import pdb; pdb.set_trace()

	fig, ax = plt.subplots()
	plt.plot(data.time, data.prices, label="Sähkön hinta")
	plt.axvline(x=now,      color='r', linestyle='--', label="Nyt")
	plt.axhline(y=pricenow, color='b', linestyle='--', label="Nykyinen hinta")
	plt.axvspan(t_nearest, t_next, color='green', alpha=0.2, label='Nykyhinta voimassa')

	#plt.plot([now], [pricenow], 'kx', markersize=12, label=None)
	#import pdb; pdb.set_trace()

	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
	ax.text(now + timedelta(minutes=60), pricenow * 1.1, notestr, fontsize=12)

	plt.legend(loc='upper right')
	plt.title("Pörssisähkön hinta", fontsize=20)
	plt.xlabel("Aika", fontsize=14)
	plt.ylabel("Hinta (EUR/kWh)", fontsize=14)
	plt.grid(True)
	plt.show()
