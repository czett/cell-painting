from flask import (
    Flask,
    url_for,
    render_template,
    request,
    send_from_directory,
)
import os
import os.path as op
import time
import uuid

app = Flask(__name__)


def del_old_files(base_dir, days=2):
    """Delete files older than `days` from `base_dir`."""
    now = time.time()
    for f in os.listdir(base_dir):
        full_path = op.join(base_dir, f)
        print(full_path)
        if op.isfile(full_path) and full_path.endswith(".txt"):
            if os.stat(full_path).st_mtime < (now - days * 86400):
                os.remove(full_path)


def write_data(data, fname):
    """Write data to file.
    `data` is a tuple of tuples."""
    with open(fname, "w") as f:
        for row in data:
            f.write("|".join(map(str, row)) + "\n")


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

        with app.open_resource("new_data_2406.csv") as file:
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

        # return str(results)

        with app.open_resource("new_data_2406.csv") as file:
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

        # return str(ri(1, 100))

        app_dir = op.dirname(__file__)

        uuid_str = str(uuid.uuid4()).split("-")[0]
        tmpfile = f"cluster_biosims_{uuid_str}.txt"

        write_data(data, op.join(app_dir, "tmp", tmpfile))

        tmpfile_url = url_for("download", fname=tmpfile)

        return render_template(
            "main.html",
            variable=data,
            legend=legend,
            leg=legend,
            tmpfile_url=tmpfile_url,
        )
        # Clean up old files:
        tmp_dir = op.join(app_dir, "tmp")
        del_old_files(tmp_dir, days=2)
    except:
        return render_template("search.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/download/<path:fname>")
def download(fname):
    return send_from_directory("tmp", fname, as_attachment=True)


if __name__ == "__main__":
    app.run()
