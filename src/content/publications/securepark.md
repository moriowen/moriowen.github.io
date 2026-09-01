---
title: "SecurePark: Vehicle Intrusion Detection System"
subtitle: Deep U. Nayak, Atharva P. Mohite, Pranav P. Nair, Pramod J. Bide
meta: IEEE, 2021
order: 4
summary: >-
  A YOLOv5s license-plate detector trained on 200 labeled images, wired to OCR, authorization
  logic, alerts, and a monitoring dashboard. My first paper, and the one where the interesting
  problem turned out to be integration rather than the model.
---

## The problem

Unauthorized vehicle entry and illegal parking in residential societies, business complexes, toll
areas, and parking lots. The design goals were affordability, local processing, ease of use, and a
workflow that runs end to end on hardware people already own.

Local processing was the point. Continuous CCTV footage never needs to be streamed to a third-party
cloud for detection, which is a privacy argument as much as a cost one.

## The pipeline

1. A user uploads an image or video, or points a live camera at the system.
2. YOLOv5 detects the plate and returns a bounding box.
3. The application crops it.
4. Microsoft Vision performs OCR on the crop.
5. The text is cleaned and validated.
6. The plate is checked against stored registrations.
7. An unrecognized plate creates a detection record and can fire a text or WhatsApp alert.
8. The dashboard exposes detections, timestamps, recordings, summaries, charts, tags, and filters.

## Getting to YOLOv5

The first prototype used YOLOv4 and Tesseract. Training on Colab took 4 to 5 hours for 200 images,
detections were unreliable, and processing a 2 to 3 second video locally took about 30 minutes.
That is unusable.

Switching to YOLOv5, a lighter PyTorch implementation, changed the economics. We evaluated all four
model sizes and picked YOLOv5s for the lowest training time at reasonable accuracy: batch size 8,
100 epochs, about 40 minutes to train.

The dataset was 200 labeled training images and 36 validation images, labeled in LabelIMG, with
manual augmentation through rotation, tilt, blur, and contrast changes on top of YOLOv5's mosaic
augmentation.

## The OCR problem

Tesseract was attractive because it runs offline and offers multiple page-segmentation modes. It
read plates poorly regardless of mode, even with the character set restricted to alphanumerics. We
moved to Microsoft Vision.

That created the compromise worth naming: detection stays local, OCR does not. The system is only
partly offline, which weakens the privacy claim we started with.

OCR output needs post-processing. Punctuation appears, and the same plate yields different strings
across frames of the same video. The application converts to ASCII, checks string length, and
checks the proportion of numeric characters, accepting a result when that proportion lands within
10% of the expected value.

## What it actually contributed

Integration. A custom detector, an OCR service, authorization logic, alerts, a searchable event
log, camera ingestion including a phone as a CCTV proxy, and a dashboard, all working together as a
prototype rather than a notebook.

## Limitations

- The dataset is small, and its sourcing, split, and plate diversity are not documented well enough
  to reconstruct.
- The paper reports "0.97 accuracies" without defining whether that is precision, recall, mAP, or
  something else, and without a held-out test set. I would not quote that number without the
  caveat.
- No direct YOLOv4 versus YOLOv5 metric table.
- OCR quality is described qualitatively, never measured against labeled examples.
- No end-to-end measurement of false alerts, missed plates, or authorization errors.
- Robustness claims for weather and lighting are broader than the evidence supports.
