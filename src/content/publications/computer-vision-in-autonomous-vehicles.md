---
title: "Computer Vision Techniques in Autonomous Vehicles: A Survey"
subtitle: Siddhi Lahange, Prashansa Nalawade, Deep Nayak, Atharva Mohite, Pramod J. Bide
meta: ICCIP 2022
order: 3
summary: >-
  A survey of the perception stack in autonomous driving. The argument is that cameras alone are
  not enough, and that deploying autonomy on Indian roads is a materially different problem from
  deploying it anywhere else.
---

## Scope

No new system. The paper explains how autonomous vehicles perceive their environment, reviews seven
representative studies, catalogs the common computer-vision methods, covers safety and accident
detection, and lists deployment challenges.

Available on SSRN, abstract 4296815.

## The central claim

Cameras and computer vision matter but are not sufficient alone. Reliable autonomy needs perception
fused with LiDAR, radar, ultrasonic sensing, localization, mapping, planning, and control.

The sensing stack as the paper lays it out: cameras for visual coverage including wide-angle and
panoramic; LiDAR for distance and 2D or 3D mapping; radar, including FMCW, which keeps working when
visibility fails; ultrasonic for short range; localization to align the vehicle to a map; and static
versus dynamic object classification feeding collision avoidance.

## Methods surveyed

Message Passing Neural Networks and hidden Markov models for behavior classification on graph data,
one-stage detection with YOLO, mean shift clustering, Spatio-Temporal Video Volumes for anomaly
scoring, CNNs, semantic and instance segmentation, simulation and 3D map creation for route
planning, driver-state estimation from yawning, Mask R-CNN accident detection on dash-cam video,
and monocular detection with regression-based depth estimation.

## Indian roads

This is the section that justifies the paper. The conditions that break models trained elsewhere:

- Weak and inconsistent infrastructure, limited road-network planning
- Barriers, road blockers, potholes, rain-damaged surfaces
- Pedestrians, motor vehicles, animals, and non-motorized vehicles sharing the same space
- Situations that change fast enough to demand immediate braking, acceleration, and steering

Alongside the general challenges: sensor reliability in heavy rain, dust storms and whiteout, and
adversarial attacks on visual perception such as altered stop signs.

## A caution about the comparison table

The paper's Table I ranks seven studies and names LeNet-5 the strongest on reported accuracy. That
ranking should be read carefully. The seven studies use different tasks, datasets, labels, metrics,
and conditions, so their headline numbers are not directly comparable. Comparing them on accuracy
alone is not methodologically sound, and I would not repeat the ranking as a finding.

## Limitations

- No stated search strategy, selection rule, database list, date range, or quality assessment. It is
  a narrative survey, not a systematic one.
- Some table entries are compressed enough that the original method is hard to identify.
- The bibliography includes references unrelated to the subject.
- Present evidence, general explanation, and future speculation are not always distinguished. The
  forward-looking claims are speculation, not research findings.
- No new dataset, model, or experiment.
