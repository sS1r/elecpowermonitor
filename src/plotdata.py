import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime, timedelta

PLOT_OVERALL = ['consumption','production','import']
PLOT_IMPORT =  ['import_russia', 'import_estonia', 'import_sweden', 'import_sweden_mid', 'import_sweden_aland', 'import_norway']

def plot_overall(data):
	for name in PLOT_OVERALL:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend(loc='upper left')
	plt.title("Yleiskatsaus", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	# ax.xaxis.labelpad=-5
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)

def plot_import(data):
	for name in PLOT_IMPORT:
		plt.plot(data[name]['time'], data[name]['values'], label=data[name]['name'])
	plt.legend(loc='upper left')
	plt.title("Tuonnin erittely", fontsize=20)
	plt.xlabel("Aika (h)", fontsize=14)
	plt.ylabel("Teho (MW)", fontsize=14)
	plt.grid(True)

def plot_data(data, hide=False, fname=None):

	plt.figure(figsize=(19.2, 10.8), dpi=100.0)

	ax = plt.subplot(2,1,1)
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
	plot_overall(data)

	ax = plt.subplot(2,1,2)
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
	plot_import(data)

	# Adds space between the subplots
	plt.tight_layout(h_pad=1.0)

	if fname:
		plt.savefig(fname)

	if not hide:
		plt.show()

def plot_elecprice(data, hide=False, fname=None):

	now = datetime.now()
	nowstr = now.strftime("%d.%m.%Y klo %H:%M")
	for t in data.data.index:
		if t.replace(tzinfo=None) > now:
			i_nearest = data.time.index(t) - 1
			t_nearest = data.time[i_nearest].replace(tzinfo=None)
			t_next = t
			break
	pricenow = data.data["price"][i_nearest]
	notestr = "Hinta {}:\n{:.3f} EUR/kWh".format(nowstr, pricenow)

	fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100.0)

	plt.plot(data.data.index, data.data["price"], label="Sähkön hinta")
	plt.axvline(x=now,      color='r', linestyle='--', label="Nyt")
	plt.axhline(y=pricenow, color='b', linestyle='--', label="Nykyinen hinta")
	plt.axvspan(t_nearest, t_next, color='green', alpha=0.2, label='Nykyhinta voimassa')

	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
	ax.text(now + timedelta(minutes=60), pricenow * 1.1, notestr, fontsize=12)

	plt.legend(loc='upper right')
	plt.title("Pörssisähkön hinta", fontsize=20)
	plt.xlabel("Aika", fontsize=14)
	plt.ylabel("Hinta (EUR/kWh)", fontsize=14)
	plt.grid(True)

	if fname:
		plt.savefig(fname)

	if not hide:
		plt.show()
