# Research section recommendation

## Recommendation

For the main one-page resume, combine the two UCF-Crime papers into one research entry. They form a clear technical story: first reduce redundant video frames for action recognition, then make long videos searchable through timestamped captions and natural-language queries.

Do not list the B.Tech report separately because it documents the same work as the LLM paper. Leave the autonomous-vehicle survey off the main resume because it did not introduce a new model, dataset, or experiment. Add SecurePark only for computer-vision-focused applications or a two-page academic resume.

## Where it should go

Rename `PROJECTS` to `SELECTED RESEARCH & PROJECTS` and place the research entry first, immediately after Skills. Keep it within three bullets. On the one-page version, use the space already occupied by the current `Crime Detection and Video Querying` entry instead of adding a new section below it.

For AI and ML roles, keep MaanSick after the research entry and shorten or remove OC-Three. For general software engineering roles, keep OC-Three and shorten or remove MaanSick.

## Recommended one-page entry

### Video Understanding Research | 2 Papers | UCF-Crime, PyTorch, GPT-4, BMT, Vid2Seq

- Evaluated 12 combinations of SlowFast, UniFormerV2, TIN, and three keyframe-extraction methods on selected UCF-Crime classes; the best configuration reached 84.53% average accuracy, 5.33 percentage points above its baseline.
- Reduced reported per-epoch processing time by up to 68.75% through keyframe selection while comparing the speed and accuracy tradeoffs of histogram, VSUMM, and SIFT extraction.
- Built a video-query pipeline that generated timestamped captions with BMT and Vid2Seq and retrieved events with GPT-3.5, GPT-4, and LLaMA; GPT-4 reached 56% exact timestamp matching and 85% within a two-minute tolerance.

If the links fit on the title line, use separate links for the keyframe paper and LLM paper. Link the longer project documentation through `Docs`, but do not count the report as an additional publication.

## Alternative version emphasizing implementation

### Video Understanding Research | 2 Papers | UCF-Crime, PyTorch, GPT-4, BMT, Vid2Seq

- Built a long-video search pipeline that converted surveillance footage into timestamped captions with BMT and Vid2Seq, then used GPT-3.5, GPT-4, and LLaMA to retrieve events from natural-language queries.
- Hand-annotated 50 UCF-Crime videos using three annotators and a consensus process, fine-tuned the captioning models, and added recursive caption chunking to handle videos that exceeded the LLM context window.
- Benchmarked 12 action-recognition and keyframe-extraction combinations; the best result reached 84.53% average accuracy, while keyframe selection reduced reported per-epoch time by up to 68.75%.

Use this version for AI engineering roles because it shows the data, model, context-management, and evaluation work more clearly. Use the first version for ML research roles because it gives more space to the experiment and its results.

## Optional SecurePark entry for computer vision roles

### SecurePark | Paper | YOLOv5, Microsoft Vision OCR, Web Application

- Trained a YOLOv5s license-plate detector on 200 labeled training images and integrated OCR, vehicle authorization, alerts, saved recordings, and usage analytics into a working monitoring dashboard.

SecurePark is the best third paper to include because it demonstrates an end-to-end application. Do not include its reported `0.97` result because the paper does not define the metric.

## Claims to remove or correct in the current resume

The existing research entry contains three claims that should be changed:

- Replace "reducing inference time by 68.75%" with "reducing reported per-epoch time by up to 68.75%." The paper's table says time per epoch, while its prose uses inconsistent terminology.
- Replace "improving accuracy by 5%" with "improving average accuracy by 5.33 percentage points," or give the complete comparison from 79.20% to 84.53%.
- Remove the claim that parameter-efficient fine-tuning used 90% less training data and produced a 2% gain. The paper states the claim but does not provide enough experimental detail or a separate result table to support it.

The current line "achieving 85% accuracy in event detection with GPT-4" also needs context. The defensible result is 56% exact timestamp matching and 85% within a two-minute tolerance. The current phrase makes the 85% result sound like exact event-classification accuracy.

The claim about fine-tuning on "handcrafted datasets" should be singular and concrete. The documents support a 50-video, multi-annotator UCF-Crime caption dataset, but they do not quantify a direct gain in caption quality.

## Changes elsewhere on the resume

- The page is already dense. Add research by replacing the current research project, not by inserting more content.
- The Skills section takes about six lines and contains several broad concepts. Removing generic entries such as Design Patterns, Cloud Architecture, RESTful API design, and Testing would recover space without weakening the resume.
- The Achievement stating "Published 4 research papers" becomes repetitive once the papers are visible above. Replace it with a compact publication count on the research heading or remove it.
- The Software Engineer II section currently has three bullets. If a fourth strong ownership story is added later, it should displace a weaker project bullet rather than shrink the font.
- Change "scaling throughput to 5M+ trades per day" to "designed for 5M+ trades per day" unless 5M+ is a verified production result. The existing resume review notes describe this as planned capacity.
- Keep the LLM-agent regression bullet only if the generation, orchestration, diagnosis, and validation capabilities are implemented and explainable in an interview.

## Suggested one-page order

1. Education
2. Experience
3. Skills
4. Selected Research & Projects
5. Achievements

Within Selected Research & Projects:

1. Video Understanding Research
2. MaanSick for AI and ML applications, or OC-Three for software engineering applications
3. One remaining project only if the page stays readable at the current font size

The strongest default resume should contain the two UCF-Crime papers, not all four papers. Add SecurePark for computer vision openings. Reserve the survey paper and full project report for Google Scholar, the website, or a separate academic CV.
