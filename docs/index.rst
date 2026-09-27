PaintByChar documentation
========================

Welcome to the PaintByChar documentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   examples

Quick start
-----------

.. code-block:: python

   import paintbychar as pbc

   grid = """A B
   C D
   """

   img = pbc.string_to_image(
       grid,
       value_colors={"A": (255, 0, 0), "B": (0, 255, 0), "C": (0, 0, 255), "D": (255, 255, 0)},
       cell_size=30,
       render_style=pbc.RenderStyle.COLORED_CELLS,
   )

   pbc.save_image(img, "example.png")
