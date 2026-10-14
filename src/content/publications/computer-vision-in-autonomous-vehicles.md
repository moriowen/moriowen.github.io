---
title: "Computer Vision Techniques in Autonomous Vehicles: A Survey"
subtitle: Siddhi Lahange, Prashansa Nalawade, Deep Nayak, Atharva Mohite, Pramod J. Bide
meta: ICCIP 2022
order: 3
summary: >-
  A survey of the perception stack in autonomous driving. The argument is that cameras alone are
  not enough, and that deploying autonomy on Indian roads is a materially different problem from
  deploying it anywhere else.
external:
  - { label: "Paper (PDF)", href: "/papers/computer-vision-in-autonomous-vehicles.pdf" }
  - { label: "SSRN", href: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4296815" }
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Type</dt>
<dd>Narrative survey, 11 pages. No new model, dataset, or experiment.</dd>
<dt>Venue</dt>
<dd>4th International Conference on Communication and Information Processing (ICCIP 2022). Available on SSRN, abstract 4296815.</dd>
<dt>Covers</dt>
<dd>How an autonomous vehicle senses its surroundings, seven representative studies compared side by side, the common vision methods, safety and accident detection, and the obstacles to deployment.</dd>
<dt>Central claim</dt>
<dd>Computer vision matters but is not enough by itself. Reliable autonomy needs vision fused with LiDAR, radar, ultrasonic sensing, localization, mapping, planning, and control.</dd>
<dt>Distinctive part</dt>
<dd>A focus on Indian road conditions, where infrastructure, mixed traffic, and road damage break assumptions built into models trained elsewhere.</dd>
</dl>
</div>

## How an autonomous vehicle perceives

<figure>
<img src="/papers/figures/cv-system-architecture.jpg" alt="System architecture diagram in three stages: input (sensor interface with LiDAR, camera, localization sensor; communication vehicle-to-vehicle, -infrastructure, -user), processing (data fusion of vehicle state, positioning, vision, object detection; planning of global path, local path, mission), and output (control and actuators for path tracking, speed, gear, brake), with perception linking input and processing and new communication data fed back." width="1227" height="679" loading="lazy" />
<figcaption>Fig. 1 from the paper: input, processing, and output stages of an autonomous vehicle, with perception connecting sensing to fusion and planning.</figcaption>
</figure>

The survey describes the vehicle as three stages:

- **Input.** Sensors (LiDAR, cameras, localization) plus communication with other vehicles,
  infrastructure, and the user.
- **Processing.** Data fusion (vehicle state, positioning, vision, object detection) and planning
  (global path, local path, mission).
- **Output.** Control and actuators: path tracking, speed, gear, brakes.

### The sensors, and what each is for

| Sensor | What it gives the vehicle | Where it is weak or strong |
|---|---|---|
| **Cameras** | Visual coverage on all four sides; wide-angle and panoramic lenses for parking | Rich detail, but the input most affected by lighting, weather, and tampering |
| **LiDAR** | Exact distances and a 2D or 3D map, from a rotating roof-mounted laser | Precise geometry; dynamic objects are removed so the map holds only fixed structure |
| **Radar** (incl. FMCW) | Millimeter-wave ranging at short and medium range | Keeps working when visibility drops; FMCW adds resolution and fast pulses |
| **Ultrasonic** | Short-range distance from reflected pulses | Parking and obstacles directly behind the vehicle |
| **Localization** | The vehicle's position matched against the map | Needed for route planning and to give detections a location |

Vision then has three main jobs: classify static versus dynamic objects for collision avoidance,
build 3D maps of the surroundings, and collect the large amounts of driving data that later
models are trained on.

## Seven studies, side by side

Table I of the paper compares seven representative studies. Summarized:

<ol class="studies">
<li><span class="study-head">2021 · Traffic-sign and lane detection</span>CNNs with spatial transformer networks, on a German traffic-sign set of 50,000 images in 43 classes. LeNet-5 reached about 97% accuracy against 94% for a feed-forward network.<span class="study-gap">Gap: weak on some signs because those classes had too few examples.</span></li>
<li><span class="study-head">2020 · Accident detection from dashboard cameras</span>Mask R-CNN, evaluated on MS COCO and a custom set of 30 fps accident videos collected online. Recognized 79.05% of accidents, with a 34.44% false-alarm rate.<span class="study-gap">Gap: limited training data; bounded by Mask R-CNN's own accuracy.</span></li>
<li><span class="study-head">2020 · Small-scale self-driving platform</span>A computer, an RGB-D camera, and an RC car, using OpenCV for path detection, YOLOv3 for objects, and an indoor positioning system. Built as a low-cost platform for learning and research.<span class="study-gap">Gap: image-based visual servoing needs more compute; no LiDAR.</span></li>
<li><span class="study-head">2020 · Edge-based detection</span>Canny edge detection on Sobel gradients, with Gaussian filtering for camera noise and local contrast enhancement. The combined decision rule held up well and kept detection accuracy high.<span class="study-gap">Gap: does not assess whether the driver is fit to drive or drunk.</span></li>
<li><span class="study-head">2019 · Semantic scene segmentation</span>K-means and expectation maximization for per-pixel classification on unlabeled data. Improved bounding-box localization and segmentation.<span class="study-gap">Note: applicable to predicting driver position in semi-autonomous vehicles and ADAS.</span></li>
<li><span class="study-head">2018 · Vision-based safety platform</span>Deep learning with a binocular camera and GPU for lane detection, traffic-sign classification, and vehicle detection; 39,209 training and 12,630 test images. Tested on campus with a four-wheeled electric car.<span class="study-gap">Gap: without higher-end sensors it is a research model, not deployable.</span></li>
<li><span class="study-head">2018 · SSD7 in simulation</span>A small SSD network detecting vehicles and pedestrians in a Unity environment with roads, vegetation, and people. Ran at 30 frames per second.<span class="study-gap">Gap: suggests training a larger network end to end in a richer environment.</span></li>
</ol>

<div class="note">

**A caution about this comparison.** The paper's comparative analysis names LeNet-5 the strongest
method, citing its accuracy and short training time. The seven studies use different tasks
(sign classification, accident detection, segmentation, detection in simulation), datasets,
labels, metrics, and conditions, so their headline numbers cannot be compared directly. I would
not repeat that ranking as a finding. The table is useful as a map of approaches, not a
leaderboard.

</div>

## Methods the survey covers

| Method | What it does in a vehicle |
|---|---|
| **Message Passing Neural Networks + hidden Markov models** | Classify driving behavior from graph-structured data |
| **One-stage detection (YOLO)** | Find and classify objects in a single pass, fast enough for real time |
| **Mean shift clustering** | Non-parametric clustering that does not need the number of clusters in advance; used for tracking |
| **Spatio-Temporal Video Volumes** | Score unusual events for accident detection by comparing local activity with learned patterns |
| **CNNs, semantic and instance segmentation** | Label every pixel by class, or separate individual objects |
| **Simulation and 3D maps** | Model the driving space to plan safe routes and reroute around predicted collisions |
| **Driver-state estimation** | Detect drowsiness from repeated yawning against a learned threshold |
| **Mask R-CNN on dash-cam video** | Track vehicles and detect accidents from the tracks |
| **Monocular detection + regression depth** | Detect cars with one camera, estimate their distance, and keep the car in its lane |

## Safety and accident detection

- **Low-speed autonomy.** One line of work pairs a binocular camera with an NVIDIA Jetson TX2,
  ENet, and OpenCV for traffic-signal recognition, and uses model predictive control to choose
  driving commands. Road segmentation runs grayscale conversion, Gaussian blur, Canny edges, and a
  Hough transform; CNN segmentation helps but loses edge detail when it downsamples.
- **Depth.** Stereo vision recovers depth by triangulation, from the known distance between two
  lenses and where an object appears in each image.
- **Accident detection.** The survey describes the self-driving stack as five connected parts:
  computer vision, sensor fusion, localization, path optimization, and control. A Gaussian mixture
  model with mean-shift tracking can locate vehicles, but with so few parameters it fails in harsh
  weather and heavy traffic.

## Indian roads

This is the section that justifies the paper. The conditions that break models trained elsewhere:

- Weak or inconsistent infrastructure and limited road-network planning
- Barriers, road blockers, potholes, and roads damaged by rain
- Pedestrians, motor vehicles, animals, and non-motorized vehicles sharing the same space
- Situations that change fast enough to demand immediate braking, acceleration, and steering

## Broader challenges

- **Capabilities a vehicle needs**: forward-collision warning, lane departure and lane keeping,
  pedestrian and object detection, traffic-sign recognition, headlight control, mapping,
  blind-spot monitoring, and vehicle-to-vehicle communication.
- **Weather**: whether current sensors can cope with heavy rain, dust storms, and whiteouts.
- **Supervision**: the paper cites Tesla's system as the closest to a complete solution, yet it
  only assists the driver in town, and its volunteer beta was making roughly one significant error
  per hour at the time.
- **Adversarial attacks**: small stickers on a stop sign can stop a vision model from
  recognizing it.
- **Data**: collecting enough driving data, labeling it accurately, and testing in realistic
  conditions.

The survey proposes three responses: more real-world training and testing, combining vision with
complementary sensors and AI, and designated roads or zones where autonomous vehicles operate.

## Conclusions

Autonomous vehicles still need human supervision and much more testing across environments before
they are dependable. The survey expects progress in vehicle-to-vehicle communication, connected
services, electric autonomous vehicles, coordinated traffic, and better perception and
collision-avoidance algorithms.

Some forward-looking claims in the paper, such as driving licenses becoming unnecessary or traffic
problems disappearing, are speculation rather than findings, and I would not repeat them as
conclusions.

## Limitations

- **Not systematic.** No search strategy, inclusion rule, database list, date range, or quality
  assessment. It is a narrative survey.
- **Compressed table entries.** Some rows in Table I are summarized so tightly that the original
  method is hard to identify.
- **Bibliography quality.** The reference list includes entries unrelated to the subject.
- **Evidence and speculation are mixed.** Current evidence, general explanation, and future
  predictions are not always distinguished.
- **No new contribution beyond synthesis.** No new dataset, model, or experiment.
