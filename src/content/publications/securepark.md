---
title: "SecurePark: Vehicle Intrusion Detection System"
subtitle: Deep U. Nayak, Atharva P. Mohite, Pranav P. Nair, Pramod J. Bide
meta: IEEE, 2021
order: 4
summary: >-
  A YOLOv5s license-plate detector wired to OCR, authorization
  logic, alerts, and a monitoring dashboard. My first paper, and the one where the interesting
  problem turned out to be integration rather than the model.
external:
  - { label: "Paper (PDF)", href: "/papers/securepark.pdf" }
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Problem</dt>
<dd>Housing societies, business complexes, tolls, and parking lots in India rarely have affordable automated vehicle monitoring, so unauthorized entry and illegal parking go unchecked.</dd>
<dt>Approach</dt>
<dd>A web application that detects license plates with YOLOv5s running locally, reads them with OCR, checks them against registered vehicles, and alerts residents about unknown plates.</dd>
<dt>Data</dt>
<dd>200 labeled training images and 36 validation images, partly hand-labeled and augmented.</dd>
<dt>Headline</dt>
<dd>Moving from YOLOv4 to YOLOv5s cut training from 4 to 5 hours to about 40 minutes, and the paper reports detector accuracy of 0.97. A working end-to-end prototype, live camera feed included.</dd>
<dt>Takeaway</dt>
<dd>The detector was the easy part. OCR and the plumbing around it decided whether the system worked.</dd>
</dl>
</div>

## The problem

Unauthorized vehicles entering private premises are a security problem, and illegal parking is a
daily nuisance. Commercial automatic number-plate recognition (ANPR) systems exist, but they
usually need expensive GPUs or a cloud service, which means streaming a society's CCTV footage to a
third party around the clock. During COVID-19 there was also a push to reduce how much security
staff have to handle in person.

The design goals were:

- **Affordable.** Run on an ordinary laptop or desktop.
- **Local.** Detection happens on the premises, so footage never has to leave. That is a privacy
  argument as much as a cost one.
- **Usable by anyone.** A web interface for people who know nothing about the model.
- **Complete.** Detection, recognition, authorization, alerts, and records in one system.

## The pipeline

<ol class="flow">
<li><b>Input.</b> A user uploads an image or video, opens the laptop webcam, or connects a remote camera such as a phone.</li>
<li><b>Detect.</b> YOLOv5s processes each frame and returns a bounding box around the plate.</li>
<li><b>Crop</b> the plate out of the frame using the box coordinates.</li>
<li><b>Read.</b> The crop goes to Microsoft Vision for OCR.</li>
<li><b>Clean and validate</b> the returned string (see the OCR section).</li>
<li><b>Authorize.</b> Look the plate up in the society's registered vehicles.</li>
<li><b>Alert and log.</b> An unregistered plate creates a detection record and can trigger a text or WhatsApp message to residents who opted in.</li>
<li><b>Review.</b> The dashboard shows detections, timestamps, saved recordings, and statistics.</li>
</ol>

## Getting to YOLOv5

The first prototype used **YOLOv4 with Tesseract OCR**. On Google Colab GPUs it took 4 to 5 hours
to train on 200 images. Detections were wrong in most scenarios, and a 2 to 3 second clip took
about 30 minutes to process on a local machine. That rules it out for anything live.

We moved to **YOLOv5**, a lighter PyTorch implementation. YOLOv5 comes in four sizes, all
pretrained on COCO. We tried each one and chose **YOLOv5s**, which had the shortest training time
at acceptable accuracy.

| | YOLOv4 prototype | YOLOv5s (final) |
|---|---|---|
| Training time | 4 to 5 hours (Colab GPU) | ~40 minutes |
| Configuration | n/a | batch size 8, 100 epochs |
| Detection quality | Inaccurate in most scenarios | Reported 0.97 |
| Speed | ~30 min to process a 2 to 3 s clip locally | Used for live camera detection in the prototype (no latency figure reported) |

The paper gives no side-by-side metric table for the two versions; the comparison above is from
the narrative.

## Data

- **Source.** Labeled plate images from an online resource, plus our own images added to cover
  outliers.
- **Labeling.** We drew plate boxes in LabelImg, which saves the coordinates for each image in a
  text file.
- **Augmentation.** We rotated, tilted, blurred, and changed the contrast of some images
  ourselves, recomputing the box coordinates each time. During training YOLOv5 adds its own mosaic
  augmentation.
- **Size.** 200 labeled training images, plus a 36-image validation set that YOLOv5 uses to track
  accuracy between iterations.

## The detection result

<figure>
<img src="/papers/figures/securepark-training-curves.jpg" alt="Ten small training plots over 100 epochs: box and objectness losses falling for training and validation; precision, recall, and mAP at 0.5 rising to near 1.0; mAP at 0.5 to 0.95 rising to about 0.5." width="1100" height="544" loading="lazy" />
<figcaption>Fig. 2 from the paper: YOLOv5s training over 100 epochs. Precision, recall, and mAP@0.5 approach 1.0 on the validation set; the stricter mAP@0.5:0.95 levels off around 0.5. (The classification panels are empty because there is only one class.)</figcaption>
</figure>

The paper reports that the model trained to "0.97 accuracies". We then tested it on images with
two plates, poorly visible plates, rotated plates, and contrast changes, and those tests supported
the number.

The metric is not named. The training plots suggest it is mAP@0.5 or precision on the 36
validation images, and they also show that under the stricter COCO-style mAP@0.5:0.95 the
detector scores around 0.5. In other words, it finds plates reliably but its boxes are not tight.
I would quote "0.97" only with that context.

## The OCR problem

**Tesseract** was the first choice: it runs offline and has several page-segmentation modes. It
read plates poorly no matter which mode we used, even with the character set restricted to letters
and digits. We moved to the **Microsoft Vision API**, which needs an API key and an upload for each
crop.

That created the compromise worth naming: **detection stays local, OCR does not.** The system is
only partly offline, which weakens the privacy argument we started with.

OCR output also needs post-processing. Plates pick up stray punctuation, and in a video the same
plate comes back as a different string from frame to frame:

<figure>
<img src="/papers/figures/securepark-ocr-variants.jpg" alt="Screenshot of the SecurePark video page: a car with a detected plate box on the left, and a log on the right listing three slightly different readings of the same plate (UP32HE5691, UP32HF5691, UP321IF5691)." width="1400" height="631" loading="lazy" />
<figcaption>Fig. 8 from the paper: one plate, three OCR readings across frames of a single video. This is why the validation step exists.</figcaption>
</figure>

The cleanup rule:

<ol class="flow">
<li><b>Normalize</b> every character to its ASCII equivalent and strip punctuation.</li>
<li><b>Check the length</b> of the string against an expected plate length.</li>
<li><b>Check the share of digits.</b> Accept the string if its proportion of numeric characters is within 10% of the expected value.</li>
</ol>

This removes obvious garbage. As the screenshot shows, it does not merge near-duplicate readings
of the same plate into one, and the paper does not specify how that would be done.

## The web application

<figure>
<img src="/papers/figures/securepark-dashboard.jpg" alt="SecurePark dashboard: counters for total, legal, and illegal cars detected, a weekly chart of legal and illegal detections, and a recent-logs list of plates marked with green checks or red crosses and timestamps." width="1400" height="631" loading="lazy" />
<figcaption>Fig. 6 from the paper: the dashboard, with detection counts, a weekly chart, and recent logs marked authorized or not.</figcaption>
</figure>

- **Accounts by society.** Users log in and are grouped under their housing society or
  organization. They register a contact number, car model, and plate number. Registered plates
  are never flagged.
- **Alerts.** Residents can opt in to text or WhatsApp messages with the plate number whenever an
  unregistered vehicle is detected, and can check the alert against the record themselves.
- **Input modes.** Image upload, video upload, the laptop webcam, and a live remote feed. For
  testing, the IP Webcam app turned a phone into a stand-in for a CCTV camera.
- **Recordings.** Processed videos are saved, with detection timestamps listed alongside so you
  can jump straight to each one.
- **Statistics.** Daily, weekly, and monthly detection counts and the time of day with the most
  detections, shown as charts.
- **Search.** Logs can be searched by tag and filtered.
- **Responsiveness.** Asynchronous calls and multithreading keep the interface responsive while
  inference runs locally.

## Related work we built on

The literature review places SecurePark in the classic four-stage ANPR pipeline: capture the
image, detect the plate, segment the characters, recognize them. Figures reported by prior work
(theirs, not ours):

| Approach | Reported result | Noted limitation |
|---|---|---|
| Ant colony optimization for localization + SVM character recognition | 80% localization, 79.84% character recognition, 97.3% real-time system success | Noisy, blurred, and night images |
| Feature-based localization + image scissoring, for Indian plates | 82% overall; 87% localization, 95% segmentation, 85% recognition | Excludes non-English and badly distorted plates |
| Four-phase ANPR with preprocessing | 97.5% extraction, 97.5% segmentation, 96.67% recognition (against 90.83 / 88.33 / 86.67 for the existing system) | Weak on low-contrast, blurred, and noisy images |
| YOLO-based ALPR with temporal redundancy | Character recognition 81.8% → 93.53% (SSIG) and 64.89% → 78.33% (UFPR) with redundancy | Most errors on motorcycles |
| SSD for illegal-parking detection | 99% accuracy at 25 FPS | "Illegal" defined as waiting over 15 s, which does not fit Indian conditions |

Two lessons from that review shaped the design: modern single-stage detectors had made plate
localization close to solved, and using several frames of the same vehicle (temporal redundancy)
makes character recognition noticeably better.

## What it actually contributed

Integration. A custom detector, an OCR service, authorization logic, alerts, a searchable event
log, several camera inputs including a phone standing in for CCTV, and a dashboard, all working
together as a prototype rather than a notebook. The screenshots in the paper are the evidence that
it ran end to end.

## Limitations

- **Small, under-documented dataset.** 200 training images, with source, split procedure, plate
  diversity, and licensing not recorded well enough to reconstruct.
- **Undefined headline metric.** "0.97 accuracies" is never defined, and there is no held-out test
  set beyond the 36 validation images.
- **No YOLOv4 versus YOLOv5 metric table.**
- **OCR quality is described, never measured** against labeled plates.
- **Partly cloud-dependent.** Microsoft Vision undercuts the claim of a fully offline system.
- **No end-to-end evaluation.** False alerts, missed plates, and authorization errors are not
  measured.
- **Undocumented engineering.** The web stack, database schema, plate-matching rule, alert
  provider, hardware, latency, and throughput are not described.
- **Robustness claims outrun the evidence.** The paper says the model works across seasons and
  lighting, but reports no per-condition results.
