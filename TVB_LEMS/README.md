# TVB LEMS

**Original source of files: https://github.com/maedoc/tvb-lems**

## What

This project has a few modest goals:

- Neural mass models from TVB defined in LEMS format
- Use a LEMS model as a node model in TVB
- Run TVB mass model with jLEMS and/or PyLEMS

In time, TVB itself will use this project instead of its
own Python code.  Not everything is supported

- coupling functions
- annotations on parameters
- noise functions (gfuns, diffusion coefficients)

## Why

New applications of neural mass models outstrip the original
TVB library code base, so having the definitions in an independent
reusable form should enable new applications more easily:

- single sim within TVB
- high throughput parameter sweeps on GPUs
- gradient based inference techniques
- multiscale on single simulator (PyNN, NEST, Neuron, etc)

It could be interesting to build proofs of concepts

- LEMS to gufunc for generic parallel par sweep
- LEMS to Pyro or PyMC3 estimator

These would be simplistic but intended to demo reusability.