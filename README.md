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

### Core Domain Services (Django Back-Office Applications)

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

## Solution Architecture Overview

### 1. Frontend Layer
- **Angular Portal (UI)**  
  Users interact through the **Angular UI** to manage surveys, assignments, and data.  
  This UI communicates with the **Backend-for-Frontend (BFF)**.

### 2. Backend Layer
- **Node.js BFF (Backend-for-Frontend)**  
  Acts as a middle layer between the UI and backend services, aggregating data and serving the UI.  
  - Aggregates responses from multiple **Django domain services**.

- **Django Domain Services**  
  Each of the following services is an **independent Django app**, running in its own container and owning its own **Postgres DB**.  
  These services are independent and communicate via events and APIs:
  - **Survey Planning Service**  
  - **Data Capture Service**  
  - **Validation & Curation Service**  
  - **Reference Data Service**  
  - **Identity & Access Service**

### 3. Event Layer
- **Kafka/Redpanda Event Streaming**  
  - Used to communicate changes and events across the system, ensuring decoupling between services.  
  - Each service produces **domain events** (e.g., `survey.assignment.created`, `data.capture.updated`) that are published to **Redpanda/Kafka**.

### 4. Analytics Layer
- **Real-time Analytics (Streaming)**  
  - **Apache Spark/Flink** processes events from **Redpanda** for real-time insights (e.g., monitoring field progress, data issues).

- **Batch Analytics**  
  - **Databricks** runs **batch processing** jobs and **Delta Live Tables (DLT)** to aggregate and analyze historical data.

- **Analytics Dashboards**  
  - Business Intelligence (BI) dashboards (e.g., **Power BI**, **Looker**, **Databricks SQL**).  
  - These provide **insights and visualizations** to decision-makers based on historical or real-time data.

### 5. Data Layer
- **Postgres Databases**  
  Each domain service (e.g., Survey Planning, Data Capture) has its own **Postgres database** (multi-schema or independent per service).

### 6. Cloud Layer (Deployment and Integration)
- **Cloud Services** (Azure, AWS, GCP)  
  - The system can be deployed on multiple cloud platforms, with services like **Azure Event Hubs**, **AWS MSK**, and **GCP Pub/Sub** for event streaming, and **PostgreSQL** for database services.
  - **Databricks** for big data analytics and batch processing.

## Outcomes

- Alignment with business processes for agricultural survey management  
- Domain-driven services with independent data ownership and event-driven integration  
- Cloud-native scalability with support for multiple cloud providers  
- Real-time monitoring and historical analytics for better operational and strategic decision-making  
- Transparent architecture that can be deployed locally for development or scaled in production environments

## Enterprise Architecture (EA) and. Solution Architecture (SA) for Agri-Frame Survey Portal

| **Aspect**                         | Enterprise Architecture (EA)                                         | Solution Architecture (SA)                                             |
|------------------------------------|------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **Scope**                          | Focuses on **the entire Agri-Frame Survey Portal** ecosystem, its alignment with **business goals**, and how it fits within the larger agricultural survey ecosystem. | Focuses on the **Agri-Frame Survey Portal system** itself: how the **UI, BFF, domain services, and analytics** integrate and work together to solve specific business needs. |
| **Focus**                          | **Strategic alignment** with agricultural survey management business goals, overall technology stack, cloud adoption, and data integration across multiple services. | **Detailed design and technical implementation** of the Agri-Frame Survey Portal: the specific components, their interactions, technologies used, and how it will be implemented. |
| **Key Objective**                  | Ensure that the entire **Agri-Frame Survey Portal platform** supports the long-term **business objectives** of streamlining agricultural survey management and decision-making. | Implement **Agri-Frame Survey Portal** as a working system, ensuring the **UI, BFF**, and **domain services** are integrated efficiently to meet the business objectives. |
| **Components**                     | - **Business Process Integration**: Survey Planning, Data Capture, Validation, and Analytics. <br> - **Cloud and Infrastructure Integration**: Event Hubs (Azure), MSK (AWS), Postgres, Databricks. <br> - **Event-Driven Architecture**: Kafka/Redpanda for event streaming. | - **Angular UI** (Frontend) <br> - **Node.js BFF** (Backend-for-Frontend) <br> - **Domain Services** (Survey Planning, Data Capture, Validation) <br> - **Event Streaming** (Kafka/Redpanda) <br> - **Analytics** (Databricks, Dashboards) |
| **Level of Detail**                | **High-level, abstract view** of the system architecture: focusing on how **different business domains** and **technologies** integrate. | **Detailed view**: How each component (UI, BFF, domain services, event streaming, analytics) **communicates**, how data flows between them, and the **technical implementation** of each service. |
| **Technologies Covered**           | High-level strategic decisions on cloud platforms (e.g., Azure, AWS, GCP), data infrastructure, and integration points (Kafka, Databricks, Postgres). | Specific technologies used in the **Agri-Frame Survey Portal** system such as **Node.js**, **Angular**, **Django** (Postgres-backed), **Kafka/Redpanda**, **Databricks**, and cloud services (Azure, AWS, GCP). |
| **Architecture Type**              | **Holistic view** of **Agri-Frame Survey Portal’s** place within the broader enterprise ecosystem of agricultural survey management, data integration, and decision-making. | **Specific system design** of the **Agri-Frame Survey Portal** application and services, focusing on how each service integrates, communicates, and functions within the platform. |
| **Stakeholders Involved**          | - **Business Leaders**: To ensure the system aligns with agricultural survey management goals. <br> - **Enterprise Architects**: For defining overall architecture principles and tech strategy. <br> - **Cloud Engineers**: For deploying on platforms like Azure, AWS, GCP. | - **Solution Architects**: For designing the system architecture of the portal. <br> - **Developers**: For implementing the UI, BFF, and backend services. <br> - **DevOps Engineers**: For continuous deployment and scalability of services. |
| **Long-Term vs. Short-Term**       | Focuses on **long-term IT strategy**, scaling the system, and ensuring it supports the agricultural survey industry’s needs at an enterprise level. | Focuses on the **short-term implementation** of the **Agri-Frame Survey Portal** solution, ensuring it is **built, deployed, and operational**. |
| **Example for Agri-Frame**         | **Agri-Frame Survey Portal** as part of an enterprise solution for agricultural survey management. Integration with multiple **cloud providers** and **data platforms** (Azure Event Hubs, AWS MSK, GCP Databricks). | The **Agri-Frame Survey Portal**: A system with **Angular UI**, **Node.js BFF**, **Django Services**, **Kafka/Redpanda Event Streaming**, **Postgres databases**, and **Databricks analytics**. |
| **Data Flow**                      | High-level data flows: How **survey data** flows across **multiple services**, from **data collection to analytics**, and integrates with **cloud data platforms** for long-term reporting. | Detailed data flows within the portal: How **Survey Planning**, **Data Capture**, **Validation**, and **Analytics** components communicate, share data, and respond to events published to the **Kafka/Redpanda** bus. |
| **Governance & Standards**         | Defines **enterprise-wide IT governance**, **data security**, **cloud standards**, and **compliance** policies. | Focuses on **solution-specific standards**, such as **API design**, **data validation rules**, **event-driven architecture**, and **security** for the Agri-Frame Portal system. |
| **Example Diagram**                | A **high-level systems view** showing integration between the **Survey Planning**, **Data Capture**, **Validation**, and **Analytics** domains, along with **cloud integration** (Azure Event Hubs, AWS MSK). | A **solution-specific diagram** detailing the interactions between **Angular UI**, **Node.js BFF**, **Django domain services**, **Kafka/Redpanda Event Streaming**, and **Databricks analytics**. |

---

## Creating Django Projects

```shell
cd apps
python -m pip install Django
pip install --upgrade pip
 
mkdir -p django-identity-access

django-admin startproject identity_access django-identity-access
cd django-identity-access
python manage.py runserver
```