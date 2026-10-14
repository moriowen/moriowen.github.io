---
title: JP Morgan Chase
subtitle: Bengaluru, India
meta: Jan 2022 - Jul 2022
order: 4
summary: >-
  First internship at the firm. Built a cloud resource discovery framework that pulled AWS Config,
  Splunk, Terraform, and tagging APIs into one inventory of 10k+ resources, so the DevOps team
  could see who owned what before cleaning it up.
roles:
  - title: Software Engineer Intern
    kind: Internship
    when: Jan 2022 - Jul 2022
    where: Bengaluru
    bullets:
      - Developed a cloud resource discovery framework that helped discover 10k+ resources, consolidating AWS Config, Splunk, Terraform, and tagging APIs into a unified inventory using Qlik Sense dashboards for tracking resource ownership, enabling data-driven cleanup decisions and improving infrastructure visibility for the DevOps team.
---

## Cloud resource discovery

I worked in the cloud enablement team, helping application teams move from on-premises
infrastructure to AWS. Resources could be provisioned through several routes, including
Terraform, service catalog, and deployment pipelines. Their details were spread across tools,
which made it difficult to trace a resource back to its account, workspace, and creator.

I collected resource details from AWS Config and Splunk, explored Terraform APIs, and used the
AWS Resource Groups Tagging API to trace ownership. The aim was to consolidate those sources
into one inventory so teams could see how resources had been provisioned and identify unused
or orphaned infrastructure.

I also built Qlik Sense dashboards and worked on infrastructure for tracking the inventory over
time. Application teams could use the inventory to track resources and estimate development
environment costs; SRE teams used it for monitoring, and it provided a consolidated view for
management. Identifying unused resources was a cost-saving opportunity, but I do not have a
measured savings figure from this work.

TODO: document the exact rules for reconciling conflicting records and a specific cleanup
decision made from the dashboards.

## Distributed tracing

One application team encountered unexplained latency while moving to the cloud. I evaluated
distributed tracing tools, including Jaeger, OpenTelemetry, and Zipkin, and built an AWS X-Ray
integration that worked within the firm's security constraints.

I wrote a primer covering integration in Java, Python, and Node.js so other teams could use the
same approach. The solution was adopted by the original application team and later by an
InstaMed team working on a C# application.

## Amazon Connect and Lex

Another team wanted to integrate Amazon Connect and a Lex chatbot into its application. The
recommended authentication approach was not approved in the firm's environment, so I built a
custom connectivity and authentication library using the existing on-premises identity system.

The work included a chatbot UI, reusable React components, and dynamic bot selection. I worked
with the application team and AWS support to test different approaches, then deployed a proof
of concept on the firm's Kubernetes platform. The internship report recorded a planned July
production rollout; it does not confirm that the rollout happened.

## Working across teams

The inventory project also became the parent project for four summer interns whose work I
helped define and coordinate. Alongside implementation, I wrote primers and design documents,
presented the work to senior leadership, and worked with teams in the US and UK.
