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

def plot_elecprice(api, hide=False, fname=None):

	data = api.get_data()
	now = datetime.now()
	nowstr = now.strftime("%d.%m.%Y klo %H:%M")
	nearest_available = False
	for t in data.data.index:
		if t.replace(tzinfo=None) > now:
			i_nearest = data.data.index.get_loc(t) - 1
			t_nearest = data.data.index[i_nearest].replace(tzinfo=None)
			t_next = t
			nearest_available = True
			break

	if nearest_available:
		pricenow = data.data["price"][i_nearest]
		notestr = "Hinta {}:\n{:.3f} EUR/kWh".format(nowstr, pricenow)

	fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100.0)


	plt.minorticks_on()
	plt.stairs(data.data["price"], data.data.index.to_list() + [data.data.index[-1]], label="Sähkön hinta", linewidth=2)
	plt.axvline(x=now,             color='r', linestyle='--', label="Nyt")

	if nearest_available:
		plt.axhline(y=pricenow,        color='b', linestyle='--', label="Nykyinen hinta")
		plt.axvspan(t_nearest, t_next, color='g', alpha=0.2,      label='Nykyhinta voimassa')
		ax.text(now + timedelta(minutes=60), pricenow * 1.1, notestr, fontsize=12)

	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
	ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(6))

	plt.legend(loc='upper right')
	plt.title("Pörssisähkön hinta (ALV {:.1f}%)".format(api.vat), fontsize=20)
	plt.xlabel("Aika", fontsize=14)
	plt.ylabel("Hinta (EUR/kWh)", fontsize=14)
	plt.grid(True, which="both")

	if fname:
		plt.savefig(fname)

	if not hide:
		plt.show()
