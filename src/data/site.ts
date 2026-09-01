// Single source of truth for the whole site. Edit here, nothing else.

export const site = {
  name: 'Atharva Mohite',
  title: 'Atharva Mohite',
  tagline:
    'Software engineer. MS CS at Georgia Tech, starting Aug 2026. Distributed systems, and machine learning for video.',
  description:
    'Atharva Mohite - software engineer working on distributed systems and machine learning. MS CS student at Georgia Tech.',
  location: 'Atlanta, GA',
};

// TODO: fill in the Scholar id and the resume PDF, then uncomment those links.
export const links = [
  { label: 'Email', href: 'mailto:amohite8@gatech.edu' },
  { label: 'GitHub', href: 'https://github.com/moriowen' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/atharva-mohite/' },
  // { label: 'Scholar', href: 'https://scholar.google.com/citations?user=REPLACE_ME' },
  // { label: 'Resume', href: '/resume.pdf' },
];

export const about = [
  `I build backend systems that move a lot of money and a lot of messages. For the last three years
   that has meant trade settlement infrastructure at JP Morgan Chase, where I worked on pulling
   services out of a monolith, orchestrating end-of-day processing, and making 750k records
   searchable in under 150ms.`,
  `Before that I did computer vision research on long surveillance video, asking how much of a video
   you can throw away before a model stops recognizing what happened in it, and whether a language
   model can find the moment you are looking for. Four papers came out of it.`,
  `In August 2026 I start an MS in Computer Science at Georgia Tech, specializing in machine learning.`,
];

export const education = [
  {
    school: 'Georgia Institute of Technology',
    degree: 'MS in Computer Science, Machine Learning',
    where: 'Atlanta, GA',
    when: 'Aug 2026 - May 2028 (expected)',
  },
  {
    school: 'Sardar Patel Institute of Technology',
    degree: 'BTech in Computer Science, CGPA 3.9/4.0',
    where: 'Mumbai, India',
    when: 'Aug 2019 - May 2023',
  },
];

export const experience = [
  {
    org: 'JP Morgan Chase',
    role: 'Software Engineer II',
    when: 'Jan 2026 - Aug 2026',
    points: [
      'Owned cross-service design and production readiness for a new business line across 7 microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.',
      'Designed a Spring Boot aggregation engine that folds high-volume trade streams into consolidated settlement instructions across configurable dimensions, cutting instruction volume by 70%.',
      'Built an LLM-agent regression framework that generates and diagnoses multi-service test workflows, automating 300+ scenarios and cutting manual test effort 90%. Adopted by 30+ engineers across 5 teams.',
    ],
  },
  {
    org: 'JP Morgan Chase',
    role: 'Software Engineer I',
    when: 'Feb 2023 - Dec 2025',
    points: [
      'Led extraction of a high-throughput microservice from a legacy trade settlement monolith, processing 1M+ messages per day on an event-driven, non-blocking stack with Kafka and Spring WebFlux.',
      "Designed distributed end-of-day orchestration coordinating 3 services to close and settle the day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and concurrent state transitions with idempotent replay on failure.",
      'Architected a materialized datastore in Elasticsearch, aggregating and rehydrating data from multiple source systems for sub-150ms complex search over 750k records, enabling the decommission of 4 legacy systems.',
      'Migrated 15 legacy applications to an in-house Kubernetes platform, saving $450k annually in infrastructure costs and cutting deployment time by 50%.',
    ],
  },
];

export const publications = [
  {
    title: 'Leveraging LLMs for Video Querying',
    authors: 'Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar',
    venue: 'IEEE, 2023',
    note: `Turns long video into timestamped captions with BMT and Vid2Seq, then lets an LLM answer
           natural-language queries about it. GPT-4 hit 56% exact timestamp matching and 85% within a
           two-minute tolerance on UCF-Crime.`,
    href: '',
  },
  {
    title: 'Keyframe Extraction assisted Crime Detection',
    authors: 'Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar',
    venue: 'IEEE, 2023',
    note: `Evaluated 12 combinations of SlowFast, UniFormerV2, and TIN against histogram, VSUMM, and
           SIFT keyframe extraction. Best configuration reached 84.53% average accuracy, 5.33 points
           over baseline, while cutting per-epoch processing time by up to 68.75%.`,
    href: '',
  },
  {
    title: 'Computer Vision Techniques in Autonomous Vehicles: A Survey',
    authors: 'Siddhi Lahange, Prashansa Nalawade, Deep Nayak, Atharva Mohite, Pramod J. Bide',
    venue: 'ICCIP 2022',
    note: `Survey of the perception stack in autonomous driving, arguing that cameras alone are not
           enough and that deployment on Indian roads is its own problem.`,
    href: '',
  },
  {
    title: 'SecurePark: Vehicle Intrusion Detection System',
    authors: 'Deep U. Nayak, Atharva P. Mohite, Pranav P. Nair, Pramod J. Bide',
    venue: 'IEEE, 2021',
    note: `End-to-end license plate recognition and vehicle authorization that runs locally on an
           ordinary machine, so CCTV footage never leaves the premises.`,
    href: '',
  },
];

export const projects = [
  {
    name: 'OC-Three',
    stack: 'React, Firebase, Django, Three.js',
    note: `Event management portal for a college fest. 1,000+ registered users and Rs 65K+ in
           transactions through Cashfree, a Three.js campus model for navigation, and an admin
           dashboard that let 23 non-technical event teams push real-time updates.`,
    href: '',
  },
  {
    name: 'MaanSick',
    stack: 'Python, DIPY, scikit-learn, Flask, React',
    note: `Classifies depression vulnerability from DTI metrics in 3D neuroimaging data. Preprocessing
           pipeline computes eigenvalues from diffusion tensors for voxel-level features; the SVM
           reaches 90%+ accuracy, served through Flask for real-time inference.`,
    href: '',
  },
];

export const awards = [
  'Winner of 2 national hackathons: Smart India Hackathon 2022 and Code for Good 2021.',
  'Top finishes in internal company hackathons with 100+ participants: 1 win, 2 runner-up.',
  '4 papers published in international conferences in machine learning and computer vision.',
];

export const skills = [
  { group: 'Languages', items: 'Java, Python, TypeScript, SQL' },
  {
    group: 'Technologies',
    items:
      'Spring Boot, Kafka, Elasticsearch, React, Next.js, Node.js, Django, Flask, Oracle, AWS, Terraform, Kubernetes, Docker, Jenkins',
  },
  {
    group: 'Other',
    items:
      'Distributed systems design, event-driven architecture, REST and GraphQL API design, CI/CD, testing, observability (Splunk, Grafana)',
  },
];

export const elsewhere =
  'Away from a keyboard: boxing, lifting, running, dancing, cooking, and writing. Collecting places to go and poems worth rereading.';
