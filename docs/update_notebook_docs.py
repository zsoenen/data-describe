import re
import os
import shutil
import glob
import pathlib


examples_template = """.. _x-tutorial:

.. note::

    This tutorial is intended to be run in an IPython notebook.


.. include:: ../_notebooks/x.rst"""


def load_notebooks():
    """Load notebooks from the /example directory."""
    notebooks = glob.glob("../examples/*.ipynb")

    outputs = []
    for notebook in notebooks:
        notebook_name = os.path.splitext(os.path.split(notebook)[1])[0]
        output_name = notebook_name.lower().replace(" ", "_")
        if output_name != "tutorial":
            outputs.append(output_name)
            print("Updating {}...".format(notebook_name))

            pathlib.Path("source/examples").mkdir(exist_ok=True)

            shutil.copyfile(notebook, "source/examples/" + output_name + ".ipynb")

    # Insert links to the examples ToC
    print("Finalizing examples Page")
    text = open("source/examples/index.rst", "r").read()
    text = re.sub(
        r"(:maxdepth: 1).*(\.\.\s_)",
        r"\1\n\n"
        + "\n".join(["   ../examples/" + name for name in outputs])
        + r"\n\2",
        text,
        flags=re.S,
    )
    open("source/examples/index.rst", "w").write(text)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    load_notebooks()