---
title: "SecurePark: Vehicle Intrusion Detection System"
subtitle: Deep U. Nayak, Atharva P. Mohite, Pranav P. Nair, Pramod J. Bide
meta: IEEE, 2021
order: 4
summary: >-
  End-to-end license plate recognition and vehicle authorization that runs locally on an ordinary
  machine, so CCTV footage never leaves the premises.
---

## The problem

Unauthorized vehicle entry and illegal parking in residential societies, business complexes, toll
areas, and parking facilities. Design goals were affordability, local processing, ease of use, and
a workflow that runs end to end on hardware people already own.

## Why local processing

Privacy. Continuous CCTV footage never needs to be streamed to a third-party cloud for object
detection. This was my first paper and the constraint that made it interesting.

## How it works

1. Detect and crop the license plate from an image or video frame.
2. OCR the plate into a string, then match it against registered-vehicle data.
3. Record the detection, flag authorized versus unauthorized, alert, and expose historical footage
   and summary statistics.

## Notes

TODO: accuracy numbers, where the OCR failed, and what plate conditions broke it.
