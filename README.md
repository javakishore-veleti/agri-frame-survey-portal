# agri-frame-survey-portal

Agri-Frame Survey Portal is a monorepo for agricultural survey management using a shared-nothing, domain-driven design.  
“Frame” refers both to the agricultural survey frame (sample units such as farms, tracts, or plots) and to the system as a framework that supports planning, execution, validation, and analytics.

## Business Perspective

The goal of this project is to provide an end-to-end digital platform for managing agricultural surveys.  
It covers the full lifecycle from survey planning and field data collection to validation, curation, and analytics.

This enables agricultural agencies and enterprises to:
- Plan and manage surveys consistently
- Capture observations at the field or tract level
- Validate and curate collected data
- Integrate real-time events with downstream analytics
- Provide timely and high-quality insights to decision-makers

## Enterprise Architecture Perspective

The portal is designed using a shared-nothing, microservices-based, domain-driven architecture.  
Each domain has its own service, database, and event publishing mechanism.  
Services communicate through APIs and events, not through direct database access.

### Core Domain Services (Drupal Back-Office Applications)

- **Survey Planning Service**  
  Manages survey design, assignments, and workloads. Defines what gets measured, where, and when.

- **Data Capture Service**  
  Supports field data collection for tracts, plots, and observations. Handles both online and offline scenarios.

- **Validation and Curation Service**  
  Applies rules, detects anomalies, and manages corrections to ensure high-quality data.

- **Reference Data Service**  
  Provides shared vocabularies and classifications, such as crop codes, land-use codes, and geographic definitions.

- **Identity and Access Service**  
  Manages authentication, authorization, and role-based access for users across different domains.

### Orchestration and Front-End

- **Angular Portal**  
  The unified user interface for survey planners, enumerators, validators, and analysts.  
  Accesses data only through the Backend-for-Frontend.

- **Node.js Backend-for-Frontend (BFF)**  
  Orchestrates across all domain services.  
  Provides simplified, UI-shaped APIs that aggregate responses from multiple domains.

### Analytics Applications

- **Analytics Databricks**  
  Batch analytics pipelines, Delta Live Tables, notebooks, and curated SQL views.  
  Supports end-of-day and long-term analytics.

- **Analytics Streaming**  
  Real-time stream processors (Spark, Flink, or Kafka Streams) that consume domain events.  
  Enables near real-time operational monitoring.

- **Analytics Dashboards**  
  Business intelligence dashboards built on Power BI, Looker, or Databricks SQL.  
  Provide insights for operations and executive decision-making.

### DevOps and Cloud-Native Foundations

- **Local Development**  
  Modular Docker Compose setup including Postgres, Redpanda, Kafka UI, MinIO, and pgAdmin.  
  Allows developers to run the full platform locally without Kubernetes.

- **Deployments**  
  Kubernetes manifests and Helm charts for deploying each service.

- **Cloud Overlays**  
  Configurations for cloud-native deployments:  
  - Azure (Event Hubs, Azure Database for PostgreSQL, Blob Storage, Databricks)  
  - AWS (MSK, RDS, S3, Databricks on AWS)  
  - GCP (Confluent Cloud, Cloud SQL, GCS, Databricks on GCP)

## Outcomes

- Alignment with business processes for agricultural survey management  
- Domain-driven services with independent data ownership and event-driven integration  
- Cloud-native scalability with support for multiple cloud providers  
- Real-time monitoring and historical analytics for better operational and strategic decision-making  
- Transparent architecture that can be deployed locally for development or scaled in production environments
