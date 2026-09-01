---
title: MaanSick
meta: Python, DIPY, scikit-learn, Flask, React
order: 2
summary: >-
  Classifies depression vulnerability from diffusion tensor imaging metrics in 3D neuroimaging
  data. The SVM reaches 90%+ accuracy, served through Flask for real-time inference.
---

## Approach

An SVM over DTI metrics, fractional anisotropy, mean diffusivity, axial and radial diffusivity,
extracted from 3D neuroimaging data.

The preprocessing pipeline uses DIPY to compute eigenvalues from diffusion tensors and pull scalar
features out of high-dimensional voxel-level data. Tuned with grid search and k-fold
cross-validation, deployed behind Flask with a React frontend.

## Caveats

TODO: important to state plainly. Dataset size, class balance, and why 90%+ accuracy on a small
clinical dataset is not a clinical claim. What this would need before anyone should trust it.

## What I learned

TODO: the gap between a model that scores well and a model that means something.
