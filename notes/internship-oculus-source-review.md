# Internship and Oculus source review

Reviewed against Notion on October 14, 2026. Source pages are named, not linked; they are private
reference material and not included in the published entry bodies.

## JPMC internship, 2022

Source: Intern Report - JP Morgan Chase 2022.
Cross-check: Atharva Mohite Resume.

The report supports resource discovery through AWS Config, Splunk, Terraform APIs, and the
Resource Groups Tagging API; Qlik Sense dashboards; AWS X-Ray integration and documentation;
Amazon Connect/Lex connectivity and UI work; and coordination of four summer interns.

The report's 10k+ figure refers to AWS accounts across the firm, not the number of resources
discovered by this implementation. The existing site's 10k+ resources claim is retained from
its resume summary, but these Notion sources do not independently establish it. Do not use the
account count as evidence for that resource count.

The report describes identifying unused resources as a potential saving. It gives no measured
savings figure or specific completed cleanup. The exact reconciliation rules are also missing.
The Amazon Connect production rollout was planned for July, not confirmed as completed.

The older Notion resume ends the internship in June; the site ends it in July. Dates were left
unchanged pending confirmation.

## JPMC internship, 2023

Sources checked: JPMC book of work,
Experience Workbook, and the Notion resume.

These describe reusable UI components, search and grid templates, shared connectors, starter
projects, documentation, and later SOLAR work. They do not clearly isolate February-May 2023
internship contributions from subsequent full-time work. The 2023 entry is unchanged.

Still needed: which components and services were delivered during the internship, the basis
for the 30-40% estimate, and the specific roles of Kafka and GraphQL in those services.

## Oculus S.P.I.T.

Primary source: Oculus 2022.
Cross-check: Bide LOR.

The project page records 1,000+ distinct users, 500+ registrations across 11 events, and
Rs 65,000+ processed through Cashfree. Use distinct users rather than registered users to
keep those counts separate. The recommendation preparation notes support the Tech Head role,
Three.js campus model, and 23 event teams using Firebase Firestore sync.

The project page supports monitoring and editing registrations through OC-Admin and keeping
its live link private to protect participant details. It does not establish tech team size,
division of implementation work, or specific event-day incidents. Those TODOs remain.
