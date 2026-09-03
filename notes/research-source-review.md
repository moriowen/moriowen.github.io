# Undergraduate research documentation

This file documents the four research papers and the Bachelor of Technology project report in this folder. It is based only on the five local PDFs. No external sources were used to correct, extend, or verify their claims.

The page references below use the physical PDF page number shown by a PDF viewer. Numbers, timings, accuracies, and conclusions are reported as the documents state them. Where two documents disagree or a claim is not supported by enough detail to reproduce it, that is called out explicitly.

## Document set

1. [SecurePark: Vehicle Intrusion Detection System](./SecurePark.pdf), 6 pages. An end-to-end automatic number plate recognition and vehicle authorization system built around YOLOv5, Microsoft Vision OCR, and a web application.
2. [Computer Vision Techniques in Autonomous Vehicles: A Survey](<./Computer Vision Techniques in Autonomous Vehicles.pdf>), 11 pages. A survey of perception methods, sensors, safety applications, accident detection, and deployment challenges for autonomous vehicles.
3. [Keyframe Extraction assisted Crime Detection](./BE___Keyframe_Extraction_assisted_Crime_Detection.pdf), 6 pages. An experimental comparison of three action-recognition models and three keyframe-extraction algorithms on selected UCF-Crime classes.
4. [Leveraging LLMs for Video Querying](./BE___Leveraging_LLMs_for_Video_Querying.pdf), 6 pages. A video-to-text-to-query pipeline that combines dense video captioning models with GPT-3.5, GPT-4, and LLaMA to retrieve event timestamps.
5. [Leveraging LLMs for Video Querying: B.Tech project report](./BE_Blackbook_Group_4.pdf), 38 pages. The long-form project record underlying the six-page LLM paper, including institutional front matter, expanded architecture and training descriptions, figures, the paper manuscript, and originality-report summaries.

## Research program at a glance

The documents show a progression from object detection, through broader computer-vision study, to long-form video understanding:

1. SecurePark detects a small spatial target, a vehicle license plate, recognizes its text, and connects the result to an operational web system.
2. The autonomous-vehicle survey broadens the scope to perception stacks that combine cameras, LiDAR, radar, ultrasonic sensing, localization, mapping, and control.
3. The keyframe paper tackles the computational cost of long surveillance video by selecting a small subset of frames before action recognition.
4. The LLM video-querying paper converts long videos into timestamped captions and lets a user find events with natural-language queries.
5. The B.Tech report expands the final system and preserves the formal project record.

Across the corpus, the recurring engineering pattern is to place a learned visual model inside a usable pipeline. The work does not stop at model selection: SecurePark includes OCR, authorization logic, alerts, logs, and a dashboard; the keyframe paper measures speed as well as classification accuracy; the LLM project manages context-window limits and returns timestamps rather than free-form text alone.

## 1. SecurePark: Vehicle Intrusion Detection System

### Bibliographic record

- Title: "SecurePark: Vehicle Intrusion Detection System"
- Authors: Deep U. Nayak, Atharva P. Mohite, Pranav P. Nair, and Pramod J. Bide
- Affiliation: Sardar Patel Institute of Technology, Mumbai, India
- Format: IEEE-style conference paper, 6 pages
- Copyright line in the paper: 2021 IEEE
- Topics: automatic number plate recognition, object detection, OCR, deep learning, web applications, vehicle authorization, and parking security

### Problem and motivation

The paper targets unauthorized vehicle entry and illegal parking in residential societies, business complexes, toll areas, and parking facilities. Its stated design goals are affordability, local processing, ease of use, and an end-to-end workflow that can run on an ordinary computer. The paper also frames local processing as a privacy advantage because continuous CCTV footage does not need to be streamed to a third-party cloud service for object detection.

The system has two core recognition tasks:

1. Detect and crop a vehicle's license plate from an image or video frame.
2. Convert the plate image into a machine-readable string, then compare it with the application's registered-vehicle data.

The broader application records detections, distinguishes authorized and unauthorized vehicles, alerts users, and exposes historical footage and summary statistics.

### System pipeline

The implemented flow is:

1. A user uploads an image or video, or supplies a live camera stream.
2. YOLOv5 detects the license plate and returns a bounding box.
3. The application crops the detected plate.
4. Microsoft Vision API performs OCR on the crop.
5. The application cleans and validates the returned text.
6. The recognized plate is checked against stored vehicle registrations.
7. An unauthorized plate creates a detection record and can trigger a text or WhatsApp alert.
8. The dashboard exposes detections, timestamps, recordings, daily or weekly or monthly summaries, charts, tags, and filters.

Figure 5 on PDF page 4 shows the application lifecycle. Figures 6 through 10 on PDF pages 4 and 5 show the dashboard, webcam detection, uploaded-video detection, recording browser, and live mobile-camera detection.

### Model selection and data preparation

The first prototype used YOLOv4 and Tesseract OCR. The paper reports that YOLOv4 training on Google Colab took 4 to 5 hours for 200 images, detections were often inaccurate, and processing a 2 to 3 second video on a local computer took about 30 minutes. This led the team to switch to YOLOv5, described as a lighter PyTorch implementation.

The final detection dataset contained:

- 200 labeled training images
- 36 validation images
- Online images plus additional outlier examples
- Labels created with LabelIMG
- Manual augmentation through rotation, tilt, blur, and contrast changes
- Additional mosaic augmentation supplied by the YOLOv5 training pipeline

The paper says the team evaluated the four YOLOv5 model sizes and selected YOLOv5s because it offered the lowest training time while preserving reasonable accuracy. The final training configuration was a batch size of 8 for 100 epochs. Training reportedly took 40 minutes.

### Reported detection result

The training statistics are described as producing "0.97 accuracies." The authors then tested scenarios containing two plates, low plate visibility, rotated objects, and contrast variation, and state that those tests supported the training result.

This should be read as the paper's reported result, not as a fully specified benchmark. The document does not define whether 0.97 is precision, recall, mean average precision, overall accuracy, or another quantity. It also does not provide a held-out test-set size, confidence intervals, per-condition results, or a confusion analysis.

### OCR design

Tesseract was attractive because it could run offline and offered multiple page-segmentation modes. The paper reports poor plate recognition even after trying different modes and restricting the character set to alphanumeric characters. The final system therefore uses Microsoft Vision API.

The OCR output is post-processed because punctuation and other unwanted characters may appear. During video processing, the same plate can also produce different strings across frames. The application converts characters to ASCII representations, checks string length, and checks the percentage of numeric characters. A result is accepted when the numeric proportion falls within 10 percent of a desired value.

The paper does not fully specify the expected plate format, the exact desired numeric proportion, how multiple frame-level readings are consolidated, or OCR accuracy on a labeled test set. Microsoft Vision also introduces a cloud dependency, so the final pipeline is only partly offline: plate detection is local, but OCR is remote.

### Web application behavior

Users log in under their housing society or organization and register contact details, vehicle model, and license plate number. Registered vehicles are excluded from the illegal-vehicle list. Users can opt into alerts. When the system sees an unregistered plate, it can send the plate number through messaging services.

The application also provides:

- A live camera mode tested with the IP Webcam mobile application as a CCTV proxy
- Detection overlays on images and videos
- Saved recordings with detection timestamps
- Daily, weekly, and monthly detection summaries
- Time-of-day statistics
- Search by tags and filters
- Asynchronous calls and multithreading to keep the system responsive while local inference runs

### Literature surveyed

The literature section places SecurePark in the traditional four-stage automatic number plate recognition pipeline: image capture, plate detection, character segmentation, and character recognition. It reviews work using edge detection, connected components, ant colony optimization, support vector machines, feature-based localization, image scissoring, image preprocessing, YOLO, SSD, and temporal redundancy.

The paper records several comparison results from prior work, including:

- An ACO, segmentation, and SVM pipeline with 80 percent localization accuracy, 79.84 percent character-recognition success, and 97.3 percent real-time system success.
- An Indian plate system with 82 percent overall recognition after excluding non-English and badly distorted plates, plus 87 percent localization, 95 percent segmentation, and 85 percent character recognition.
- A proposed ANPR pipeline reporting 97.5 percent plate extraction, 97.5 percent segmentation, and 96.67 percent character recognition, compared with 90.83, 88.33, and 86.67 percent for the referenced existing system.
- A YOLO-based ALPR study with weaker performance on motorcycles and substantial benefits from temporal redundancy during character recognition.
- An SSD illegal-parking detector reporting 99 percent accuracy at 25 frames per second, with the paper noting that its definition of illegal parking may not transfer cleanly to Indian use cases.

These are literature-review figures, not SecurePark's own experimental results.

### Main contribution

SecurePark's clearest contribution is system integration. It combines a custom license-plate detector, an OCR service, authorization logic, alerts, a searchable event log, camera ingestion, and a dashboard into a functioning prototype. The screenshots provide concrete evidence that the interface and several input modes were implemented.

### Limitations and reproducibility gaps

- The dataset is small and its source, split procedure, plate diversity, and licensing are not documented in enough detail to reconstruct it.
- The meaning of the reported 0.97 result is undefined.
- No direct YOLOv4 versus YOLOv5 metric table is provided.
- OCR quality is described qualitatively rather than measured on labeled examples.
- The Microsoft Vision dependency weakens the claim that the complete system is offline.
- The paper does not document the web stack, database schema, authorization matching rule, alert provider, hardware, latency, throughput, or deployment procedure.
- Robustness claims for weather and lighting are broader than the evidence reported.
- There is no end-to-end measurement for false entry alerts, missed plates, or authorization errors.

### Best concise description

SecurePark is a locally run vehicle-monitoring prototype that detects license plates with a custom YOLOv5s model, reads them with Microsoft Vision OCR, checks them against registered vehicles, and surfaces unauthorized detections through a web dashboard and alerts.

## 2. Computer Vision Techniques in Autonomous Vehicles: A Survey

### Bibliographic record

- Title: "Computer Vision Techniques in Autonomous Vehicles: A Survey"
- Authors: Siddhi Lahange, Prashansa Nalawade, Deep Nayak, Atharva Mohite, and Pramod J. Bide
- Affiliation: Sardar Patel Institute of Technology, Mumbai, India
- Venue shown in the PDF: 4th International Conference on Communication and Information Processing, ICCIP 2022
- Availability shown in the PDF: SSRN, abstract 4296815
- Format: survey paper, 11 pages
- Topics: autonomous driving, computer vision, sensor systems, perception algorithms, accident detection, safety, deployment challenges, and future systems

### Purpose and scope

This paper is a broad survey rather than a new experimental system. It explains how autonomous vehicles perceive their environment, reviews seven example studies, summarizes common computer-vision methods, discusses safety and accident detection, and lists deployment challenges with special attention to Indian roads.

The central view is that cameras and computer vision are important but insufficient by themselves. Reliable autonomy depends on combining perception with LiDAR, radar, ultrasonic sensing, localization, mapping, planning, and vehicle control.

### Autonomous-vehicle sensing stack

The paper describes the following sensing and perception components:

- Cameras provide visual coverage around the vehicle, including wide-angle and panoramic views.
- LiDAR estimates object distance and supports 2D or 3D environmental maps.
- Radar uses radio waves, including frequency-modulated continuous-wave radar, and remains useful when visibility is poor.
- Ultrasonic sensors estimate short-range distance from reflected pulses and are common in parking systems.
- Localization aligns the vehicle with a map.
- Static and dynamic object classification supports collision avoidance and path decisions.
- Sensor data supplies training examples for traffic signs, potholes, road condition, lanes, pedestrians, and other road users.

Figure 1 on PDF page 3 summarizes a system architecture. Its nomenclature includes LiDAR, Message Passing Neural Network, Spatio-Temporal Video Volumes, and Convolutional Neural Network.

### Seven studies summarized in the comparison table

The survey's Table I spans PDF pages 4 and 5. It records the following studies and outcomes:

1. A 2021 traffic-sign and lane-detection study uses CNNs and spatial transformer networks on a German traffic-sign dataset of 50,000 images across 43 classes. LeNet-5 is reported at about 97 percent accuracy, compared with 94 percent for a feed-forward neural network. The listed gap is weak performance on particular signs because some classes had too few examples.
2. A 2020 dashboard-camera accident-detection system uses Mask R-CNN, MS COCO, and a custom collection of 30-fps accident videos. It reports 79.05 percent successful accident recognition and a 34.44 percent false-alert rate. The survey notes limited training data and dependence on Mask R-CNN's prediction quality.
3. A 2020 small-scale autonomous-car platform uses a computer, RGB-D camera, RC car, OpenCV, YOLOv3, and an indoor positioning system. It is framed as a learning and research platform. The listed limitations are computational requirements and the absence of LiDAR.
4. A 2020 driver-state method uses Canny edge detection, a Sobel gradient operator, Gaussian filtering, and local contrast enhancement. The survey says the combined decision procedures improve detection robustness, while also noting that driver fitness and drunk driving require further consideration.
5. A 2019 semantic-scene segmentation study uses K-means and expectation maximization with an unlabeled dataset. The paper reports improvements in bounding-box localization and semantic segmentation, with possible use in semi-autonomous vehicles and advanced driver-assistance systems.
6. A 2018 safety platform uses deep learning, a binocular camera, GPU processing, lane detection, traffic-sign classification, and vehicle detection. Its dataset contains 39,209 training and 12,630 test images. A four-wheeled electric car was used for campus testing. The survey describes the result as useful for assisted-driving research but not sufficient for deployment because higher-end sensors were absent.
7. A 2018 simulated SSD7 system detects vehicles and pedestrians in a Unity environment containing roads, vegetation, atmosphere, vehicles, and people. It reportedly reaches 30 frames per second. The survey suggests training a more capable network end to end in a richer environment.

The comparative-analysis section names LeNet-5 as the strongest method in the table because of its reported accuracy and training-time advantage. That comparison should be interpreted cautiously: the seven studies use different tasks, datasets, labels, metrics, and experimental conditions, so their headline numbers are not directly comparable.

### Algorithms and methods covered

The methodology review discusses:

- Message Passing Neural Networks and hidden Markov models for behavior classification on graph-structured data.
- One-stage object detection, especially YOLO, as an alternative to region-proposal plus classification pipelines.
- Mean shift as a non-parametric clustering and mode-seeking algorithm for image analysis.
- Spatio-Temporal Video Volumes for learning normal activity and assigning anomaly scores to unknown events.
- CNNs for visual classification and feature extraction.
- Semantic segmentation, which assigns a class to each pixel.
- Instance segmentation, which separates individual object instances.
- Simulation and 3D map creation for safer route planning.
- Driver-state estimation from yawning behavior.
- Mask R-CNN accident detection from dash-cam video.
- Monocular vehicle detection, regression-based depth estimation, lane assignment, and vehicle tracking.

### Safety and accident-detection applications

For low-speed autonomous operation, the survey describes binocular cameras, NVIDIA Jetson TX2 hardware, ENet, OpenCV, traffic-signal recognition, model predictive control, grayscale conversion, Gaussian blur, Canny edge detection, and Hough transforms. It also explains stereo depth through camera geometry and triangulation.

For accident detection, it presents the vehicle stack as five connected parts: computer vision, sensor fusion, localization, path optimization, and control. It cites a Gaussian mixture model with mean-shift tracking, then notes that a small parameter set can fail under difficult weather and traffic conditions.

### Challenges emphasized

The paper gives particular attention to Indian road conditions:

- Weak or inconsistent infrastructure
- Limited road-network planning
- Barriers and road blockers
- Potholes and rain-damaged roads
- Pedestrians, motor vehicles, animals, and non-motorized vehicles sharing the same road space
- Rapidly changing situations that demand immediate braking, acceleration, and steering decisions

It also lists broader autonomy challenges:

- Forward-collision warning
- Lane departure and lane keeping
- Pedestrian and object detection
- Traffic-sign recognition
- Headlight control
- Mapping
- Blind-spot monitoring
- Vehicle-to-vehicle communication
- Sensor reliability in heavy rain, dust storms, and whiteout conditions
- Adversarial attacks on visual perception, including altered stop signs
- Large-scale data collection, accurate labeling, and realistic testing

The proposed responses are more real-world training and testing, complementary sensing and AI, and designated roads or environments for autonomous operation.

### Conclusions and future view

The survey concludes that present systems still need human supervision and more testing across environmental conditions. It anticipates better vehicle-to-vehicle communication, connected services, electric autonomous vehicles, smarter traffic coordination, and improved perception and collision-avoidance algorithms.

Some future claims, such as the disappearance of driving licenses or traffic problems, are speculative. They should not be treated as research findings.

### Main contribution

The paper provides an accessible map of the perception technologies used in autonomous vehicles and connects them to deployment constraints. Its most useful parts are the sensor overview, the seven-study comparison, the catalog of perception methods, and the discussion of difficult mixed road conditions.

### Limitations and source-quality concerns

- The survey does not state a search strategy, paper-selection rule, database list, date range, or quality-assessment method.
- The seven studies address different tasks, so ranking them by headline accuracy is not methodologically sound.
- Several table descriptions are ambiguous or compressed enough to make the original method difficult to identify.
- The bibliography includes references that appear unrelated to autonomous-vehicle computer vision, including historical physics citations and work on cloud storage and meditation analysis.
- Some factual and product claims are time-sensitive but are not tied to dated, primary evidence in the discussion.
- The paper sometimes mixes present evidence, general explanation, and future speculation without labeling the distinction.
- No new dataset, model, or experiment is introduced.

### Best concise description

This is a 2022 survey of computer-vision and sensor techniques for autonomous vehicles, covering perception algorithms, safety and accident detection, seven representative studies, and the practical difficulty of deploying autonomy in complex road and weather conditions.

## 3. Keyframe Extraction assisted Crime Detection

### Bibliographic record

- Title: "Keyframe Extraction assisted Crime Detection"
- Authors: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, and Anant V. Nimkar
- Affiliation: Department of Computer Engineering, Sardar Patel Institute of Technology, Mumbai, India
- Format: IEEE-style conference paper, 6 pages
- Copyright line in the paper: 2023 IEEE
- Topics: action recognition, surveillance video, UCF-Crime, keyframe extraction, SlowFast, UniFormerV2, TIN, VSUMM, SIFT, histogram comparison, and computational efficiency

### Research question

Long surveillance videos contain substantial redundancy. Processing every frame increases training and inference cost, but selecting too few or the wrong frames may remove the action evidence needed for correct classification. The paper asks how three keyframe-extraction algorithms affect the speed and accuracy of three action-recognition models.

The three recognition models are:

- SlowFast, a two-pathway model that separately captures slow semantic structure and fast motion.
- UniFormerV2, which combines convolution and attention to learn short-range and long-range video relationships.
- Temporal Interlacing Network, or TIN, which interlaces temporal information to represent fast-changing actions.

The three frame-selection algorithms are:

- VSUMM, which clusters similar frames and selects representatives.
- SIFT, which finds scale and rotation invariant local features and favors frames with distinctive visual structure.
- Image histogram comparison, which selects frames around changes in color or texture distributions.

Each recognition model is evaluated without keyframe extraction and with all three extraction methods.

### Claimed contributions

The introduction presents two contributions:

1. Benchmark state-of-the-art action-recognition models combined with keyframe-extraction methods on UCF-Crime.
2. Propose parameter-efficient fine-tuning that uses 90 percent less training data and yields a 1 to 2 percent performance gain.

The body provides the comparative keyframe experiment in detail. It does not provide enough implementation detail, ablation results, trainable-parameter counts, or a separate result table to substantiate the parameter-efficient fine-tuning claim.

### Dataset

The paper describes UCF-Crime as 128 hours of 1,900 untrimmed real-world surveillance videos covering 13 anomalies: Abuse, Arrest, Arson, Assault, Road Accident, Burglary, Explosion, Fighting, Robbery, Shooting, Stealing, Shoplifting, and Vandalism.

For faster experimentation, the authors state that they focus on five classes: Explosion, Assault, Shooting, Fighting, and Road Accident. The results also include a Normal class, so the experiment tables contain six class-specific sections despite the text saying five selected classes.

### Processing architecture

Figure 1 on PDF page 4 shows the comparison pipeline:

1. Read a video from UCF-Crime.
2. Apply one selected keyframe algorithm.
3. Pass the extracted frames to an action-recognition model.
4. Produce confidence scores for action classes.
5. Select the five highest-confidence classes for the output.

The system is modular so the recognition model and extraction method can be changed independently. The paper says experimentation showed that about 10 percent of a video's frames can retain a substantial portion of its important content.

### Experimental setup

- Hardware: one Tesla K80 GPU with 12 GB of memory
- Training limit: 25 epochs for each model and keyframe pairing
- SlowFast memory footprint as stated: 150 MB when loaded
- SlowFast batch size: 10
- SlowFast training time as stated in the prose: about 1 to 1.5 hours per epoch
- UniFormerV2 batch size: 20
- UniFormerV2 learning rate: 5e-5
- UniFormerV2 training time as stated in the prose: about 1.5 to 1.75 hours per epoch

The paper does not provide the train, validation, and test split; number of videos per class; random seed; preprocessing dimensions; pretrained checkpoints; optimizer for every model; augmentation policy; software versions; or criterion used to label a prediction correct.

### Reported time results

Table I on PDF page 4 labels its quantities as time per epoch with and without keyframe extraction:

- SlowFast plus histogram: about 1.0 hour versus 2.88 hours, a 65.28 percent decrease.
- SlowFast plus VSUMM: about 0.9 hour versus 2.88 hours, a 67.12 percent decrease.
- SlowFast plus SIFT: about 1.3 hours versus 2.88 hours, a 54.86 percent decrease.
- UniFormerV2 plus histogram: about 1.4 hours versus 3.84 hours, a 63.54 percent decrease.
- UniFormerV2 plus VSUMM: about 1.2 hours versus 3.84 hours, a 68.75 percent decrease.
- UniFormerV2 plus SIFT: about 1.3 hours versus 3.84 hours, a 66.15 percent decrease.
- TIN plus histogram: about 3.0 hours versus 3.15 hours, a 4.76 percent decrease.
- TIN plus VSUMM: about 2.9 hours versus 3.15 hours, a 7.94 percent decrease.
- TIN plus SIFT: about 2.6 hours versus 3.15 hours, a 17.46 percent decrease.

The largest percentage reduction is UniFormerV2 with VSUMM at 68.75 percent. TIN benefits much less from frame selection than SlowFast or UniFormerV2 in these measurements.

The surrounding text sometimes calls these figures inference time, while the table calls them time per epoch and the numbers are measured in hours. The document therefore does not cleanly distinguish training time from inference time.

### Average classification accuracy

Table II on PDF page 5 reports average accuracy across all included classes:

- SlowFast without keyframes: 79.20 percent
- SlowFast with histogram: 84.53 percent
- SlowFast with VSUMM: 83.05 percent
- SlowFast with SIFT: 82.10 percent
- UniFormerV2 without keyframes: 79.46 percent
- UniFormerV2 with histogram: 80.14 percent
- UniFormerV2 with VSUMM: 81.73 percent
- UniFormerV2 with SIFT: 79.09 percent
- TIN without keyframes: 78.76 percent
- TIN with histogram: 82.21 percent
- TIN with VSUMM: 80.92 percent
- TIN with SIFT: 83.60 percent

Relative to each model's no-keyframe baseline, the changes are:

- SlowFast: histogram +5.33 points, VSUMM +3.85, SIFT +2.90.
- UniFormerV2: histogram +0.68 points, VSUMM +2.27, SIFT -0.37.
- TIN: histogram +3.45 points, VSUMM +2.16, SIFT +4.84.

The best average result is SlowFast with histogram extraction at 84.53 percent. The only reported average decline is UniFormerV2 with SIFT, which is 0.37 points below its baseline.

### Per-class results

Explosion:

- SlowFast: 78.95 baseline, 81.65 histogram, 85.43 VSUMM, 80.32 SIFT.
- UniFormerV2: 79.54 baseline, 82.47 histogram, 84.62 VSUMM, 79.57 SIFT.
- TIN: 80.19 baseline, 82.57 histogram, 83.90 VSUMM, 80.26 SIFT.
- Best: SlowFast with VSUMM at 85.43 percent.

Shooting:

- SlowFast: 79.22 baseline, 80.25 histogram, 85.21 VSUMM, 80.27 SIFT.
- UniFormerV2: 81.90 baseline, 79.92 histogram, 84.71 VSUMM, 80.32 SIFT.
- TIN: 79.42 baseline, 81.34 histogram, 84.63 VSUMM, 78.96 SIFT.
- Best: SlowFast with VSUMM at 85.21 percent.

Fighting:

- SlowFast: 77.89 baseline, 82.92 histogram, 81.36 VSUMM, 83.72 SIFT.
- UniFormerV2: 76.98 baseline, 79.13 histogram, 80.74 VSUMM, 81.53 SIFT.
- TIN: 77.25 baseline, 83.94 histogram, 81.81 VSUMM, 84.00 SIFT.
- Best: TIN with SIFT at 84.00 percent.

Assault:

- SlowFast: 78.12 baseline, 81.39 histogram, 80.51 VSUMM, 83.36 SIFT.
- UniFormerV2: 77.59 baseline, 80.47 histogram, 81.14 VSUMM, 84.83 SIFT.
- TIN: 79.73 baseline, 83.14 histogram, 82.57 VSUMM, 84.69 SIFT.
- Best: UniFormerV2 with SIFT at 84.83 percent.

Road Accident:

- SlowFast: 77.23 baseline, 84.31 histogram, 80.72 VSUMM, 81.89 SIFT.
- UniFormerV2: 76.61 baseline, 80.43 histogram, 81.62 VSUMM, 82.98 SIFT.
- TIN: 77.01 baseline, 85.07 histogram, 82.08 VSUMM, 83.45 SIFT.
- Best: TIN with histogram at 85.07 percent.

Normal:

- SlowFast: 77.47 baseline, 82.31 histogram, 79.89 VSUMM, 83.58 SIFT.
- UniFormerV2: 77.60 baseline, 83.81 histogram, 80.12 VSUMM, 82.77 SIFT.
- TIN: 77.34 baseline, 84.25 histogram, 81.21 VSUMM, 83.14 SIFT.
- Best: TIN with histogram at 84.25 percent.

### Interpretation offered by the authors

The paper associates VSUMM with events that benefit from broad scene coverage, especially explosions and shootings. It associates SIFT with actions where distinctive people, clothing, objects, or weapons matter, especially fighting and assault. It associates histogram changes with road accidents, where damaged vehicles, injuries, and traffic changes may alter color and texture distributions.

These explanations are plausible post-hoc interpretations, but the paper does not include feature-level analysis, qualitative error cases, or a statistical test showing that the proposed causal explanations account for the observed class differences.

### Main conclusion

The authors select SlowFast with histogram extraction as the best overall balance of accuracy and efficiency. That choice is supported by the highest reported average accuracy, 84.53 percent. It is not the fastest configuration in Table I, so "best balance" is more accurate than "fastest."

### Limitations and reproducibility gaps

- Dataset splits, video counts, class balance, and evaluation protocol are absent.
- The text says five selected classes, but the tables include six when Normal is counted.
- Training time, time per epoch, and inference time are used inconsistently.
- No variability, repeated-run average, confidence interval, or significance test is reported.
- The parameter-efficient fine-tuning claim is not documented in enough detail to reproduce or validate.
- The paper claims 10 percent of frames preserve important content but does not define the selection threshold experiment.
- The top-five output is unusual for a six-class evaluation and is not tied to the accuracy calculation.
- No confusion matrix or error analysis is provided.
- Several class-level explanations are interpretive rather than experimentally isolated.

### Best concise description

This paper compares SlowFast, UniFormerV2, and TIN with VSUMM, SIFT, and histogram-based frame selection on UCF-Crime. Its best reported average accuracy is 84.53 percent for SlowFast plus histogram extraction, while keyframe selection cuts the reported per-epoch time by as much as 68.75 percent for UniFormerV2 plus VSUMM.

## 4. Leveraging LLMs for Video Querying

### Bibliographic record

- Title: "Leveraging LLMs for Video Querying"
- Authors: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, and Anant V. Nimkar
- Affiliation: Department of Computer Engineering, Sardar Patel Institute of Technology, Mumbai, India
- Format: IEEE-style conference paper, 6 pages
- Copyright line in the paper: 2023 IEEE
- Topics: dense video captioning, natural-language video retrieval, BMT, Vid2Seq, GPT-3.5, GPT-4, LLaMA, UCF-Crime, prompt design, timestamp localization, and long-context processing

### Problem and research questions

Searching a long video by manually reviewing it or relying on coarse metadata does not provide precise event localization. The proposed system turns a video into timestamped textual captions, then gives an LLM both the captions and a user's natural-language query. The LLM returns the interval or intervals where the requested event likely occurred.

The paper asks:

1. Can LLMs be combined with video-captioning transformers to perform a more complex multimodal task without retraining the LLM for the domain?
2. How does a chain of modal conversions, from video and audio to captions to an LLM response, affect performance?
3. Why do different LLMs perform differently when querying long crime videos?
4. How do captioning-model choice, domain fine-tuning, and prompt specificity affect timestamp retrieval?

### End-to-end architecture

The common pipeline is:

1. A captioning model divides the video into temporal regions.
2. It generates a caption for each region and preserves its start and end time.
3. A caption accumulator builds a timestamped textual representation of the video.
4. A user submits a natural-language query.
5. An LLM reads the timestamped captions and query.
6. The LLM returns one or more predicted time intervals.

The output is described as a list of records containing `ST`, `ET`, and `SEN`, meaning start time, end time, and the sentence generated for the interval.

### BMT captioning path

The Bi-modal Transformer path uses:

- I3D features for visual embeddings
- VGGish features for audio embeddings
- A bi-modal encoder with self-attention to fuse audio and visual information
- A proposal generator that chooses relevant temporal regions and attaches timestamps
- A bi-modal decoder fine-tuned to produce crime-related captions
- A caption accumulator
- A recursive LLM strategy for long caption sequences

Figure 1 on PDF page 3 diagrams this architecture. The proposal generator is important because it limits captioning to selected regions and maintains temporal alignment between the visual evidence and generated text.

### Recursive handling of long videos

The complete caption sequence for a long surveillance video may exceed an LLM's context window. The recursive strategy splits the caption summary into chunks, adds the query to each chunk, processes them independently, stores intermediate answers, and repeats the process on the surviving results until the remaining information fits in one context window.

The paper also describes this as breaking a generic prompt's output into hashes and pruning the number of hashes by half on successive passes. This is conceptually similar to hierarchical retrieval and reduction. Exact chunk sizes, overlap rules, prompt templates, stopping conditions, storage representation, and duplicate-merging logic are not provided.

### Vid2Seq captioning path

Vid2Seq processes two inputs separately:

- Visual embeddings extracted from video frames
- Audio transcription produced through Google Cloud API

Separate encoder blocks process the temporal video and transcript. Their representations are concatenated and passed to a text decoder that generates captions for video regions. Figure 2 on PDF page 4 shows the architecture.

The paper concludes that BMT generated more relevant captions for long-form video than Vid2Seq in this project, but it does not provide a caption-quality table or metric that directly compares the two models.

### Handcrafted dataset and annotation

The project hand-annotated 50 UCF-Crime videos. Three annotators described randomly selected frames in one sentence. If their descriptions differed substantially, a fourth annotator helped reach consensus. The instructions emphasized brief, relevant descriptions of visible objects, actions, and context.

This design tries to reduce individual annotator bias and create domain-specific frame-caption pairs. The paper does not state:

- How many frames or captions were produced
- The sampling frequency or temporal-region definition
- Which UCF-Crime categories were included
- How train, validation, and test sets were separated
- Whether videos, rather than frames, were kept disjoint across splits
- How disagreement was measured
- Whether inter-annotator agreement was calculated
- Whether the evaluation timestamps were created independently of training captions

### Training configuration reported in the paper

For BMT and Vid2Seq, the paper reports:

- Initialization from pretrained image-captioning weights
- Fine-tuning on the handcrafted crime-video caption dataset
- Batch size: 32
- Optimizer: Adam
- Learning rate: 0.001
- Augmentations: random crop, flip, and rotation
- Training length: 100 epochs
- Hardware: four NVIDIA V100 GPUs
- Approximate epoch time: 1.5 hours
- Stated total training duration: 30 hours
- Google Cloud API transcription supplied to Vid2Seq

The reported 100 epochs at 1.5 hours each would imply about 150 hours, not 30 hours. The project report says 20 epochs, which is consistent with the stated 30-hour total. This discrepancy is documented in the report section below.

### Query design

Queries can be specific, such as asking for the exact moment a car accident occurs, or generic, such as asking when a crowd gathers. The authors argue that generic wording may retrieve more occurrences, while precise wording may improve contextual targeting. The recommended prompt balances specificity, context, and generality.

The paper says GPT-3.5, GPT-4, and LLaMA interpret the query and return timestamps. It does not provide the actual prompts, generation parameters, model versions, date of API use, sampling settings, number of attempts, or rule for parsing free-form answers into intervals.

### Evaluation metric

For each ground-truth segment, the start and end times are compared with the model's predicted start and end. The paper reports three accuracy levels:

- Exact overlap: both predicted boundaries must match the expected boundaries.
- One-minute temporal deviation: the sum of absolute start and end boundary errors must be at most 2 minutes.
- Two-minute temporal deviation: the sum of absolute start and end boundary errors must be at most 4 minutes.

The prose illustrates the rule with an expected clip from 2:00 to 4:00 and a prediction from 2:00 to 5:00. The prediction fails exact matching but passes the one-minute-deviation rule.

This metric is boundary-error tolerance, not conventional temporal intersection over union. The paper does not explain how it matches multiple predicted segments to multiple ground-truth segments, handles missing or extra predictions, or aggregates videos with different numbers of events.

### Reported LLM results

Table I on PDF page 5 reports the percentage of segments accepted at each tolerance:

- GPT-3.5: 53 percent exact, 72 percent within one minute, and 80 percent within two minutes.
- GPT-4: 56 percent exact, 77 percent within one minute, and 85 percent within two minutes.
- LLaMA: 52 percent exact, 73 percent within one minute, and 78 percent within two minutes.

GPT-4 is best at all three tolerance levels. Its margins over GPT-3.5 are 3, 5, and 5 percentage points. Its margins over LLaMA are 4, 4, and 7 points.

The paper attributes GPT-4's result to scale, training diversity, contextual understanding, and domain adaptability. It describes LLaMA as specialized for video captioning, but the cited LLaMA reference is a general foundation-language-model paper. No LLaMA fine-tuning procedure for this task is documented, so the specialization claim is unclear.

### Main conclusion

The system demonstrates a practical decomposition of video search into dense captioning and language-based retrieval. The authors conclude that GPT-4 can query video content when given sufficient timestamped text, that domain fine-tuning improves the captioning models, and that BMT is more suitable than Vid2Seq for their long-form crime videos. They also state that a commercial system based on the architecture is feasible.

Only the LLM timestamp table is quantified. The claims about captioning-model improvement, BMT superiority, prompt effects, and commercial feasibility are not accompanied by direct comparison metrics, latency, cost, reliability, or deployment measurements.

### Limitations and reproducibility gaps

- The 50-video annotation set is not fully specified or released in the document.
- The paper gives inconsistent training duration figures.
- No BMT versus Vid2Seq caption metric is reported.
- No baseline compares the LLM pipeline with embedding search, keyword search, or a direct temporal-grounding model.
- Prompt templates and model configurations are absent.
- The evaluation sample size is not reported.
- Segment matching, false positives, false negatives, and multiple-occurrence handling are underspecified.
- The one-minute and two-minute tolerances are generous for short events and may inflate apparent usefulness.
- Model accuracy is not separated by event type, video length, captioning model, or prompt style.
- No end-to-end speed, token usage, API cost, or context-length result is reported.
- The paper relies on proprietary services for GPT models and Google transcription, while the exact service versions are not recorded.

### Best concise description

This paper converts surveillance video into timestamped captions with BMT or Vid2Seq, then uses an LLM to answer natural-language event queries with predicted time intervals. GPT-4 produces the best reported timestamp accuracy: 56 percent exact, 77 percent within one minute, and 85 percent within two minutes.

## 5. B.Tech project report: Leveraging LLMs for Video Querying

### Formal record

- Title: "Leveraging LLMs for Video Querying"
- Students: Deep Nayak, Atharva Mohite, and Ameya Jangam
- Guide: Dr. Anant V. Nimkar
- Degree: Bachelor of Technology in Computer Engineering
- Institution: Department of Computer Engineering, Sardar Patel Institute of Technology, Bharatiya Vidya Bhavan, autonomous institute affiliated with the University of Mumbai
- Submission date shown: May 2023
- Length: 38 PDF pages

The front matter contains the title page, completion certificate, approval certificate, declaration, contents, list of figures, and abstract. The student declaration states that the report is original work submitted for the degree and not previously submitted elsewhere.

### Report organization

The main report contains:

1. Introduction, motivation, problem statement, objectives, and scope
2. Literature survey on video captioning, LLMs, and UCF-Crime
3. Research contribution and detailed BMT and Vid2Seq architectures
4. Experimental setup, dataset construction, model training, and LLM query behavior
5. Results and discussion
6. Conclusion
7. Bibliography

The appendices contain a reproduced copy of the six-page research paper and two originality-report summary pages.

### Motivation, problem statement, objectives, and scope

The motivation is the growth of online video and the difficulty of finding a precise moment with metadata tags or manual annotation. The formal problem statement is to improve video search through LLM-assisted captioning, with attention to prompt design, model choice, and system evaluation.

The stated objectives are:

- Build a video-search system that uses LLMs over generated captions.
- Compare GPT-3.5, GPT-4, and LLaMA.
- Study how prompt design affects accuracy and efficiency.
- Use UCF-Crime and domain-specific caption data to improve querying.

The scope is limited to LLM-assisted video captioning and search, comparison of the three LLMs, and exploration of prompt specificity.

### Expanded technical architecture

The report provides a longer explanation of the same two paths documented in the paper.

For BMT:

1. I3D extracts visual features.
2. VGGish extracts audio features.
3. A bi-modal encoder fuses the modalities with self-attention.
4. A proposal generator selects relevant regions and associates timestamps.
5. A crime-domain decoder generates a caption for each proposed region.
6. The caption accumulator assembles timestamped text.
7. The recursive LLM strategy processes chunks that exceed the language model's context window.
8. Intermediate results are repeatedly reduced until the result fits the context window.
9. The system retains multiple occurrences of the queried event across the video.

For Vid2Seq:

1. Google Cloud API transcribes the audio.
2. A temporal encoder processes visual frames.
3. A text encoder processes the transcript.
4. Their representations are concatenated.
5. A text decoder produces temporally localized captions.
6. The same caption accumulator, recursive LLM strategy, and query stage retrieve timestamps.

Figures 3.1 and 3.2 on PDF pages 18 and 19 show the architectures. Figure 3.1 labels the BMT encoder, captioning frame, proposal generator, decoder, caption accumulator, recursive strategy, LLM, user query, and returned region of interest. Figure 3.2 shows the separate temporal and text encoders in Vid2Seq.

### Dataset and annotation details

The report repeats the 50-video UCF-Crime annotation procedure but explains its intent more fully. Three annotators independently write one-sentence descriptions of randomly selected frames. A fourth annotator is used when the first three disagree. Guidelines emphasize brevity, relevant objects, actions, and context. The resulting annotations serve both as training pairs and as reference points for evaluation.

The design contains a potential leakage risk that the report does not resolve: it does not say whether frames or videos used to fine-tune the captioners are disjoint from those used to evaluate timestamp retrieval. A reproducible version should split by source video before sampling frames.

### Training details and the paper-report discrepancy

The report states:

- Batch size 32
- Adam optimizer
- Learning rate 0.001
- Random crop, flip, and rotation augmentation
- Four NVIDIA V100 GPUs
- About 1.5 hours per epoch
- 20 epochs
- 30 hours total

These values are internally consistent because 20 epochs multiplied by 1.5 hours is 30 hours. The six-page paper instead states 100 epochs while retaining the same 1.5-hour epoch time and 30-hour total. The report's 20-epoch value is therefore the coherent account, but the source set does not prove which number reflects the actual run.

Figures 4.1 and 4.2 on PDF page 21 show loss-versus-epoch curves for BMT and Vid2Seq. Both trend downward with fluctuations. The axes are small, and the report does not provide the numeric loss values, validation curves, stopping rule, or checkpoint-selection criterion.

### Query processing

The report expands the explanation of specificity and generality. A precise query communicates a narrow event and context. A general query increases recall by allowing the LLM to find related instances without exact location or wording. The model returns timestamps and a generated sentence for each interval.

For long inputs, generic-query results are broken into chunks, processed, and repeatedly reduced. The report describes the final response as a set of timestamps that indicate where the requested event probably occurred.

### Results

The report uses the same temporal-deviation measure and the same result table as the paper:

- GPT-3.5: 53 percent exact, 72 percent within one minute, 80 percent within two minutes.
- GPT-4: 56 percent exact, 77 percent within one minute, 85 percent within two minutes.
- LLaMA: 52 percent exact, 73 percent within one minute, 78 percent within two minutes.

GPT-4 is the reported winner. The report attributes this to model size, training breadth, contextual understanding, and adaptability. As in the paper, the evaluation set size and matching procedure are not fully documented.

### Conclusion and claims

The report concludes that:

- LLMs can query video when given adequate textual context.
- GPT-4 performs best among the three evaluated language models.
- BMT produces more relevant long-form captions than Vid2Seq in this project.
- Fine-tuning on a crime-specific caption dataset improves both captioning paths.
- A commercial implementation is feasible.

The first two claims have direct support from the architecture and timestamp table. The BMT versus Vid2Seq and fine-tuning claims need a dedicated caption-quality or retrieval-ablation table. Commercial feasibility would require additional evidence about latency, cost, data privacy, scaling, uptime, and failure handling.

### Relationship to the six-page paper

The report and paper describe the same project, architecture, dataset, models, metric, and numerical results. The report adds institutional documentation, motivation and scope, longer prose, standalone architecture and loss figures, a bibliography, a copy of the paper, and originality summaries.

For technical citation, the paper is the concise publication-style source. For project provenance, architecture explanation, and the internally consistent 20-epoch training account, the report is the better source.

### Originality-report appendices

PDF page 37 is labeled "Research paper plag" and reports:

- Similarity index: 8 percent
- Internet sources: 5 percent
- Publications: 6 percent
- Student papers: 2 percent

PDF page 38 is labeled "bb plag" and reports:

- Similarity index: 5 percent
- Internet sources: 3 percent
- Publications: 3 percent
- Student papers: 2 percent

These are summary pages from an originality checker. They are not measures of research quality, correctness, or reproducibility.

### Limitations of the report

The report inherits the paper's missing dataset, split, prompt, configuration, and evaluation details. It also contains lengthy general explanations that do not add implementation evidence. The most important unresolved items are the exact dataset artifact, code and dependency versions, split discipline, model checkpoints, prompt templates, evaluation sample size, interval-matching algorithm, and the discrepancy between 20 and 100 epochs.

### Best concise description

The B.Tech report is the formal long-form record of the LLM video-querying project. It documents the BMT and Vid2Seq captioning paths, a recursive strategy for querying captions longer than an LLM context window, a 50-video UCF-Crime annotation effort, and GPT-4's best reported timestamp result of 56 percent exact and 85 percent within two minutes.

## Cross-paper technical synthesis

### Shared architectural pattern

Three of the four papers use a staged system in which each model has a narrow responsibility:

- SecurePark: image or frame to plate box, plate crop to text, text to authorization decision, decision to alert and log.
- Keyframe crime detection: video to representative frames, frames to action class, class confidence to ranked output.
- LLM video querying: video and audio to timestamped captions, captions plus query to predicted intervals.

This modularity is useful because components can be replaced independently. It also creates compound error: a missed plate cannot be recovered by OCR, a poor keyframe can hide an action from the recognizer, and an incorrect caption can mislead the LLM even if the language model reasons correctly.

### Progression in temporal reasoning

SecurePark mainly treats video as a sequence of independent frames and uses repeated observations to stabilize OCR. The keyframe paper explicitly reduces temporal redundancy before recognition. The LLM project preserves temporal regions and uses language to retrieve one or more event intervals from long video. This is the clearest technical progression across the research set.

### Datasets

- SecurePark uses 200 labeled training images and 36 validation images for license-plate detection.
- The autonomous-vehicle survey cites several external datasets but introduces none.
- The keyframe paper uses selected UCF-Crime categories and reports results for five anomalies plus Normal.
- The LLM project hand-annotates 50 UCF-Crime videos to create domain-specific caption data.

UCF-Crime is the common foundation of the two later projects. The keyframe paper uses it for action classification; the LLM project uses it for captioning and timestamp search.

### Evaluation styles

- SecurePark reports a detector value of 0.97 but does not name the metric.
- The survey compares published headline results across heterogeneous tasks.
- The keyframe paper reports time and classification accuracy for 12 model-extractor configurations.
- The LLM paper reports segment-boundary accuracy at exact, one-minute, and two-minute tolerances.

The keyframe paper has the most extensive quantitative comparison. The LLM paper has a clearly defined custom metric but an underspecified matching and aggregation protocol. SecurePark has the strongest application demonstration but the weakest metric definition.

### Engineering tradeoffs

- Local versus cloud: SecurePark keeps detection local but sends crops to Microsoft Vision. The LLM project depends on external LLM services and Google transcription for parts of the pipeline.
- Accuracy versus speed: the keyframe paper makes this tradeoff explicit. SlowFast plus histogram has the best average accuracy, while UniFormerV2 plus VSUMM has the largest reported time reduction.
- Specific versus generic queries: the LLM project treats prompt specificity as a precision-recall tradeoff, although it does not quantify that tradeoff separately.
- Rich input versus context limits: BMT and Vid2Seq create more text as videos grow longer, which motivates recursive chunking and reduction.

### Strongest evidenced contributions

1. A working SecurePark interface integrating detection, OCR, registration, alerts, saved video, and analytics.
2. A full matrix of keyframe and action-model results, including per-class accuracies and time reductions.
3. A multimodal video-query architecture that preserves timestamps, manages long context recursively, and compares three LLMs with one defined temporal metric.
4. A 50-video, multi-annotator effort to adapt captioning to crime footage, although the resulting artifact is not fully specified in the documents.

### Claims that require careful wording

When describing this research in a resume, portfolio, interview, or future paper, use the reported scope precisely:

- Say "reported 0.97 detector accuracy in the project paper" only if the undefined metric is acceptable in context. A safer description is "trained a YOLOv5s license-plate detector on 200 labeled images and integrated it with OCR and a monitoring dashboard."
- Say "reduced reported per-epoch time by up to 68.75 percent" rather than "made inference 68.75 percent faster," because the paper's terminology conflicts.
- Say "achieved 84.53 percent average accuracy in the reported UCF-Crime experiment" rather than implying performance on the full 13-class dataset.
- Say "GPT-4 reached 56 percent exact timestamp matching and 85 percent within a two-minute tolerance" rather than using a single undifferentiated accuracy number.
- Say "hand-annotated 50 UCF-Crime videos with a multi-annotator consensus process" without claiming a released or independently validated dataset.
- Treat BMT superiority, fine-tuning gains, and commercial feasibility as project conclusions, not independently quantified findings.

## Reproducibility checklist for future use

A future replication or extension should preserve the following artifacts:

### SecurePark

- Image source and license
- Exact train, validation, and test manifests
- Label format and class definitions
- YOLOv5 commit, model size, image size, optimizer, learning-rate schedule, and checkpoint
- Standard detection metrics, including precision, recall, and mean average precision
- OCR test set and exact-match or character-error rate
- Plate-normalization and multi-frame voting rules
- Hardware, latency, and frames per second
- Web stack, database schema, and alert-provider configuration

### Keyframe-assisted crime detection

- UCF-Crime video manifests grouped by class and split
- Frame sampling and each keyframe algorithm's thresholds
- Pretrained model checkpoints and all fine-tuning hyperparameters
- A strict definition of training time, per-epoch time, and inference time
- Seeds and repeated runs
- Confusion matrices and per-class support
- Statistical uncertainty
- Full details for the claimed parameter-efficient fine-tuning method

### LLM video querying

- List of the 50 annotated videos and a split by source video
- Frame or segment sampling policy
- Annotation instructions, agreement measure, and final adjudication rule
- Caption dataset schema and example records
- BMT and Vid2Seq checkpoints, code versions, and training logs
- Resolution of the 20-versus-100-epoch discrepancy
- Google transcription settings
- Exact GPT-3.5, GPT-4, and LLaMA versions
- System and user prompts, temperature, token limits, and retry policy
- Chunk size, overlap, recursion, pruning, and duplicate-merging rules
- Ground-truth interval format and prediction-to-target matching algorithm
- Evaluation video count, event count, false positives, false negatives, and per-class results
- Latency, token usage, API cost, privacy controls, and failure cases

## Source map

Use these pages when returning to the original evidence:

- SecurePark: overview and motivation on page 1; prior work on pages 1 and 2; model and dataset on page 3; OCR and application flow on page 4; interface and conclusion on page 5; remaining references on page 6.
- Autonomous-vehicle survey: overview on pages 1 and 2; sensors and architecture on pages 2 and 3; comparison table on pages 4 and 5; methods on pages 5 and 6; applications and comparative analysis on page 7; challenges on page 8; conclusions and future scope on page 9; references on pages 9 and 10; author biographies on page 11.
- Keyframe-assisted crime detection: problem and contributions on page 1; model and algorithm literature on pages 2 and 3; architecture, setup, and timing on page 4; accuracy tables on page 5; interpretation, conclusion, and references on page 6.
- LLM video querying paper: problem and contributions on page 1; related work on pages 2 and 3; architectures, annotation, and loss plots on pages 3 and 4; training, query format, metric, and results on page 5; conclusion and references on page 6.
- B.Tech report: formal front matter on pages 1 through 7; introduction and scope on pages 8 through 10; literature survey on pages 11 through 13; technical contribution on pages 14 through 19; experimental setup on pages 20 through 25; results on pages 26 and 27; conclusion on page 28; bibliography on pages 29 and 30; reproduced paper on pages 31 through 36; originality summaries on pages 37 and 38.
