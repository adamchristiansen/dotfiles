By default, Fush functions go in this directory. For example, `fisher` will
install functions defined in plugins into this directory.

This kind of muddles things up with managed functions, so instead, the managed
functions go in the `exact_dotfunctions/` directory. This has the benefit that
legacy functions are automatically removed from the system when removed from
this repository.
