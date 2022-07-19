from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import numpy as np
import string, random, os
import uuid
import os.path as op
import time
from random import randint as ri

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def search():
	results = []
	legend = []

	forbidden = ["True", "False", "true", "false"]

	try:
		inp = request.form["nm"]

		
		if inp in forbidden:
			return render_template("search.html")
		else:
			pass


		with app.open_resource('new_data_2406.csv') as file:
			for i in range(3548):
				line = file.readline()
				memory = str(line).split("|")
		
				for item in memory:
					if inp in item:
						indexes = [0, 2, 16, 17, 19]
						for index in sorted(indexes, reverse=True):
						    del memory[index]

						name = memory[-2]
						memory.insert(0, name)
						memory.pop(-2)

						name = memory[-1]
						name = name.replace("\n", "")
						memory.insert(3, name)
						memory.pop(-1)

						# return str(memory)

						results.append(memory)
					else:
						try:
							if inp.capitalize() in item:
								indexes = [0, 2, 16, 17, 19]
								for index in sorted(indexes, reverse=True):
								    del memory[index]

								name = memory[-2]
								memory.insert(0, name)
								memory.pop(-2)

								name = memory[-1]
								name = name.replace("\n", "")
								memory.insert(3, name)
								memory.pop(-1)

								# return str(memory)

								results.append(memory)
						except:
							pass

						try:
							if inp.lower() in item:
								indexes = [0, 2, 16, 17, 19]
								for index in sorted(indexes, reverse=True):
								    del memory[index]

								name = memory[-2]
								memory.insert(0, name)
								memory.pop(-2)

								name = memory[-1]
								name = name.replace("\n", "")
								memory.insert(3, name)
								memory.pop(-1)

								# return str(memory)

								results.append(memory)
						except:
							pass

		#return str(results)

		with app.open_resource('new_data_2406.csv') as file:
			for i in range(1):
				line = file.readline()
				legend = str(line).split("|")

			indexes = [0, 2, 16, 17, 19]
			for index in sorted(indexes, reverse=True):
			    del legend[index]

			name = legend[-2]
			legend.insert(0, name)
			legend.pop(-2)

			name = legend[-1]
			name = name.replace("\n", "")
			legend.insert(3, name)
			legend.pop(-1)
			

		if len(results) == 0:
			return render_template("error.html")

		for biglist in results:
			for index, val in enumerate(biglist):
				try:
					if index == 1:
						pass
					elif index == 2:
						pass
					elif index == 3:
						pass
					else:
						try:
							biglist[index] = int(val)
						except:
							biglist[index] = float(val)
							biglist[index] = int(val)
				except:
					pass

		results.insert(0, legend)
		
		for item in results:
			item[3] = item[3][:-5]
		
		data = tuple(map(tuple, results))

		#return str(ri(1, 100))
		return render_template("main.html", variable=data, legend=legend, leg=legend)
	except:
		return render_template("search.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

if __name__ == "__main__":
	app.run(debug=True)
