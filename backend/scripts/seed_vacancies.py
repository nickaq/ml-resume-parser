"""Seed the database with highly detailed, diverse vacancies across different roles and stacks."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from app.core.database import async_session_factory, engine
from app.models.vacancy import Vacancy

VACANCIES = [
    # ── Backend ──────────────────────────────────────────────────
    {
        "title": "Senior Python Backend Developer",
        "company": "FinTech Solutions GmbH",
        "description": "Design and build high-performance backend services for our digital banking platform. "
                       "You will work on mission-critical transaction processing algorithms, fraud detection APIs, and microservice orchestration. "
                       "As a senior member of the team, you will also mentor junior developers, participate in architectural decisions, and ensure our systems can scale to millions of daily active users. "
                       "We value a strong engineering culture including rigorous automated testing, code reviews, and continuous pair programming.",
        "requirements": "Python, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, CI/CD, REST APIs, asyncio, System Design, Mentorship",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 75000, "salary_max": 95000,
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes"],
        "nice_to_have_skills": ["Redis", "CI/CD"],
        "industry_domain": "FinTech",
        "human_languages": ["English"],
        "work_format": "Hybrid"
    },
    {
        "title": "Go Backend Engineer",
        "company": "CloudScale Inc.",
        "description": "Build scalable distributed systems for our global cloud infrastructure platform. "
                       "Your primary focus will be on real-time data pipelines and low-latency internal microservices that handle petabytes of telemetry data. "
                       "You will write high-concurrency Go code daily, optimize gRPC communication, and implement sophisticated caching strategies. "
                       "A deep understanding of Linux system performance and memory management in Go is crucial.",
        "requirements": "Go, gRPC, Kafka, PostgreSQL, Docker, Kubernetes, Prometheus, Grafana, Concurrent Programming",
        "location": "Remote (EU)",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 80000, "salary_max": 110000,
        "required_skills": ["Go", "Kafka", "Linux", "gRPC"],
        "nice_to_have_skills": ["Prometheus", "Grafana"],
        "industry_domain": "Cloud Infrastructure",
        "human_languages": ["English"],
        "work_format": "Remote"
    },
    {
        "title": "Java Spring Boot Developer",
        "company": "Enterprise Corp",
        "description": "Develop and document robust enterprise microservices for our vast insurance claims processing network. "
                       "You will maintain and extend the existing Spring Boot ecosystem using clean architecture and Domain-Driven Design principles. "
                       "The role involves integrating with complex legacy systems, migrating older monolithic components to reactive microservices, and setting up asynchronous event-driven flows with RabbitMQ.",
        "requirements": "Java, Spring Boot, Hibernate, Oracle DB, Maven, JUnit, RabbitMQ, Jenkins, Microservices, DDD",
        "location": "Munich, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 65000, "salary_max": 85000,
        "required_skills": ["Java", "Spring Boot", "RabbitMQ"],
        "industry_domain": "Insurance",
        "work_format": "Office"
    },
    {
        "title": "Node.js Backend Developer",
        "company": "SocialApp Ltd.",
        "description": "Build real-time messaging and notification services for our rapidly growing social platform. "
                       "You will work extensively with WebSockets, event-driven abstractions, and high-throughput REST APIs. "
                       "Responsibilities include scaling Node.js clusters, sharding MongoDB databases for optimal query performance, and securing our user data. "
                       "We look for engineers who are passionate about user experience and backend performance.",
        "requirements": "Node.js, TypeScript, Express, MongoDB, Redis, Socket.io, AWS Lambda, GraphQL, WebSockets",
        "location": "London, UK",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 60000, "salary_max": 85000,
    },
    {
        "title": "Rust Systems Engineer",
        "company": "CryptoSecure AG",
        "description": "Develop ultra-low-level cryptographic libraries and reliable blockchain node software. "
                       "This role demands performance-critical code with an obsessive focus on memory safety and zero-copy networking. "
                       "You will implement advanced cryptographic primitives, optimize network consensus protocols, and conduct rigorous security audits of your own and teammates' code. "
                       "A strong background in C/C++ or low-level systems programming is highly preferred.",
        "requirements": "Rust, C, tokio, libp2p, cryptography, Linux, WebAssembly, Networking, Security Audits",
        "location": "Zurich, Switzerland",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 100000, "salary_max": 140000,
    },

    # ── Frontend ─────────────────────────────────────────────────
    {
        "title": "Senior React Frontend Developer",
        "company": "DesignHub",
        "description": "Create incredibly beautiful, accessible UI components for our next-generation collaborative design tool. "
                       "You will be responsible for pixel-perfect implementation directly from Figma mockups, ensuring buttery-smooth animations using Framer Motion. "
                       "You will lead architectural decisions on the frontend, establish Storybook guidelines for the team, and rigorously test components using Jest and Cypress to ensure zero-regression deployments.",
        "requirements": "React, TypeScript, Next.js, TailwindCSS, Framer Motion, Storybook, Jest, Cypress, Accessibility (a11y)",
        "location": "Amsterdam, Netherlands",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 65000, "salary_max": 90000,
    },
    {
        "title": "Vue.js Frontend Engineer",
        "company": "EduTech Platform",
        "description": "Build deeply interactive and engaging learning experiences for our modern online education platform. "
                       "Your primary focus will be engineering real-time collaboration features (whiteboards, chat) and rich-text editing using WebRTC and ProseMirror. "
                       "You'll optimize the Vue 3 application for low bandwidth connections, ensuring students worldwide get a snappy, responsive experience.",
        "requirements": "Vue 3, Vuex/Pinia, TypeScript, Vite, SCSS, WebRTC, ProseMirror, Vitest",
        "location": "Paris, France",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "Angular Frontend Developer",
        "company": "HealthTech Solutions",
        "description": "Develop a rigorously secure, HIPAA-compliant patient portal and clinical telemedicine dashboard. "
                       "There is a strong focus on complex interactive forms, dense data visualization for medical records, and strict WCAG accessibility compliance. "
                       "You will collaborate closely with healthcare professionals to iterate on UI/UX, transforming heavy clinical workflows into intuitive digital interfaces.",
        "requirements": "Angular, TypeScript, RxJS, NgRx, D3.js, Material UI, Jasmine, Karma",
        "location": "Vienna, Austria",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 55000, "salary_max": 70000,
    },

    # ── Fullstack ────────────────────────────────────────────────
    {
        "title": "Fullstack Developer (Python + React)",
        "company": "DataViz Startup",
        "description": "Build an end-to-end data visualization platform from API architecture all the way up to the polished UI. "
                       "You will work across the entire stack, including writing data ingestion pipelines in Pandas, serving them via FastAPI, and rendering complex interactive charts on the frontend using React and D3.js. "
                       "This is a fast-paced environment where you will take complete ownership of major product features from concept to deployment.",
        "requirements": "Python, FastAPI, React, TypeScript, PostgreSQL, D3.js, Docker, Pandas",
        "location": "Hamburg, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 60000, "salary_max": 80000,
    },
    {
        "title": "Fullstack Engineer (Ruby on Rails)",
        "company": "Shopify Partner Agency",
        "description": "Build bespoke e-commerce solutions and complex, custom Shopify integrations for premium global brands. "
                       "You'll drive end-to-end feature development ranging from optimizing backend database schemas in PostgreSQL to building polished, highly converted frontend interfaces with Hotwire and TailwindCSS. "
                       "A product-minded approach and a keen eye for design details are absolutely essential.",
        "requirements": "Ruby, Rails, PostgreSQL, Redis, Hotwire, Stimulus, TailwindCSS, Sidekiq, RSpec",
        "location": "Remote",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "Fullstack .NET Developer",
        "company": "LogisticsPlus",
        "description": "Develop robust warehouse management and live fleet tracking applications to optimize supply chain operations. "
                       "You will build robust RESTful APIs in C# .NET 8, and create responsive, lightning-fast web frontends using Blazor and SignalR. "
                       "You'll also interact with IoT device data streams, processing location and environmental data from our global container fleet.",
        "requirements": "C#, .NET 8, ASP.NET Core, Blazor, SQL Server, Entity Framework, Azure, SignalR, IoT concepts",
        "location": "Frankfurt, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 65000, "salary_max": 85000,
    },

    # ── Data & ML ────────────────────────────────────────────────
    {
        "title": "Machine Learning Engineer",
        "company": "AI Research Lab",
        "description": "Design, deploy, and monitor production-grade ML pipelines explicitly for cutting-edge NLP tasks. "
                       "Your daily responsibilities will include fine-tuning massive LLMs, building highly efficient RAG (Retrieval-Augmented Generation) systems, and heavily optimizing inference performance for high-throughput APIs. "
                       "You will work closely with AI Researchers to transition experimental notebook models into scalable, containerized production code.",
        "requirements": "Python, PyTorch, Transformers, LangChain, FastAPI, Docker, MLflow, CUDA, Pandas",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 80000, "salary_max": 110000,
    },
    {
        "title": "Data Engineer",
        "company": "BigData Analytics",
        "description": "Architect, build, and maintain highly scalable ETL pipelines processing tens of terabytes of daily real-time event data. "
                       "You will design efficient data warehouse schemas, enforce strict data quality rules, and work closely with Data Scientists to ensure data is clean, accessible, and structured. "
                       "A strong emphasis will be placed on optimizing cloud costs (Snowflake/AWS) and ensuring zero downtime in our pipelines.",
        "requirements": "Python, Apache Spark, Airflow, dbt, Snowflake, SQL, Kafka, AWS S3, Terraform",
        "location": "Dublin, Ireland",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 70000, "salary_max": 95000,
    },
    {
        "title": "Data Scientist",
        "company": "RetailAnalytics Co.",
        "description": "Apply rigorous statistical modeling and advanced machine learning techniques to fundamentally optimize pricing strategies and highly accurate demand forecasting for top-tier retail clients. "
                       "You'll be designing A/B tests, interpreting massive customer behavioral datasets, and presenting actionable business insights directly to executive stakeholders via dynamic tools like Tableau.",
        "requirements": "Python, scikit-learn, Pandas, NumPy, SQL, Jupyter, Tableau, A/B testing, Statistics",
        "location": "Stockholm, Sweden",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 60000, "salary_max": 80000,
    },

    # ── DevOps / SRE ─────────────────────────────────────────────
    {
        "title": "Senior DevOps Engineer",
        "company": "MediaStream GmbH",
        "description": "Manage and secure the vast cloud infrastructure for a video streaming platform currently serving millions of daily active users. "
                       "You will automate zero-downtime deployments via GitHub Actions, maintain comprehensive monitoring across all microservices, and organize incident response procedures. "
                       "You must be comfortable writing automation scripts in Python and bash, and managing large-scale Kubernetes deployments with Terraform.",
        "requirements": "AWS, Terraform, Kubernetes, Docker, GitHub Actions, Prometheus, Grafana, Python, Bash, Linux",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 75000, "salary_max": 100000,
    },
    {
        "title": "Site Reliability Engineer",
        "company": "PaymentGateway Inc.",
        "description": "Guarantee a strict 99.99% uptime for our mission-critical global payment processing infrastructure. "
                       "You will design inherently resilient systems, manage severe incident responses as a blameless post-mortem leader, and continually drive SLO/SLI improvements. "
                       "Expect to dive deep into application code (Go/Python) to fix bottlenecks, and manage complex PostgreSQL replication setups under extreme load.",
        "requirements": "Linux, Kubernetes, Go, Python, Terraform, Datadog, PagerDuty, PostgreSQL, gRPC",
        "location": "Remote (Global)",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 85000, "salary_max": 120000,
    },

    # ── Mobile ───────────────────────────────────────────────────
    {
        "title": "iOS Developer (Swift)",
        "company": "FitnessApp GmbH",
        "description": "Architect and build the very next generation of fitness tracking and intelligent workout planning features. "
                       "There is a massive focus on tight HealthKit integration, highly optimized real-time GPS tracking for runs, and implementing beautiful, fluid animations with SwiftUI. "
                       "You will work in tandem with hardware engineers to extract metrics from wearable Bluetooth devices.",
        "requirements": "Swift, SwiftUI, UIKit, Core Data, HealthKit, MapKit, Combine, XCTest",
        "location": "Munich, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 65000, "salary_max": 85000,
    },
    {
        "title": "Android Developer (Kotlin)",
        "company": "TravelBuddy",
        "description": "Develop our flagship offline-first travel companion application complete with custom interactive maps, sophisticated itinerary planning algorithms, and real-time on-device translation features. "
                       "You will use cutting-edge Jetpack Compose patterns, strictly enforce clean architecture, and ensure the app uses minimal battery while running GPS background tasks in remote areas.",
        "requirements": "Kotlin, Jetpack Compose, Room, Retrofit, Coroutines, Google Maps SDK, Firebase, Hilt",
        "location": "Barcelona, Spain",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "React Native Mobile Developer",
        "company": "FoodDelivery Express",
        "description": "Build our primary cross-platform mobile app used for instant food ordering, restaurant management, and live delivery courier tracking. "
                       "You'll implement real-time bidirectional order status updates, deep integration with Stripe for seamless payments, and heavily utilize push notifications to engage hungry users.",
        "requirements": "React Native, TypeScript, Redux, Firebase, Stripe, Google Maps, Jest, Detox",
        "location": "Warsaw, Poland",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 50000, "salary_max": 70000,
    },

    # ── Security / Niche ─────────────────────────────────────────
    {
        "title": "Security Engineer",
        "company": "CyberShield",
        "description": "Perform proactive penetration testing, comprehensive vulnerability assessments, and rigorous security audits of both our codebase and infrastructure. "
                       "You will actively build in-house automated security scanning tools and create strict CI/CD security gating. "
                       "You'll also run red-team exercises and train engineers on secure coding practices.",
        "requirements": "Python, Burp Suite, OWASP, Docker, Kubernetes, Terraform, AWS IAM, Nmap, Wireshark",
        "location": "Remote (EU)",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 70000, "salary_max": 100000,
    },
    {
        "title": "Embedded C/C++ Developer",
        "company": "AutoDrive Systems",
        "description": "Develop absolute zero-fault firmware for cutting-edge autonomous driving sensor fusion hardware modules. "
                       "This is extremely hardcore real-time systems programming governed by the strictest functional safety requirements (ISO 26262). "
                       "You will directly interface with LiDAR, radar, and camera streams over CAN bus and automotive ethernet, writing logic that saves lives.",
        "requirements": "C, C++, RTOS, CAN bus, SPI, I2C, ARM Cortex, AUTOSAR, MISRA C, Git",
        "location": "Stuttgart, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 70000, "salary_max": 95000,
    },

    # ── Junior / Internship ──────────────────────────────────────
    {
        "title": "Junior Frontend Developer",
        "company": "Creative Agency Berlin",
        "description": "Join our dynamic, fast-paced team to build stunningly beautiful marketing websites, portfolios, and conversion-optimized landing pages. "
                       "This is an incredible opportunity to learn modern responsive web development standards directly from senior designers and engineers. "
                       "You'll slice Figma files into fluid HTML/CSS and implement simple interactive elements using React.",
        "requirements": "HTML, CSS, JavaScript, React, Git, Figma, responsive design",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 38000, "salary_max": 45000,
    },
    {
        "title": "Working Student — Backend Development",
        "company": "TU Munich Spin-off",
        "description": "Support our core engineering team in fundamentally building out a massive research data management platform used by top universities. "
                       "This is a part-time position featuring highly flexible hours tailored specifically to accommodate Computer Science students. "
                       "You'll write API endpoints in Python, craft SQL migration scripts, and learn professional branching strategies with Git.",
        "requirements": "Python, Flask or FastAPI, SQL, Git, Linux basics",
        "location": "Munich, Germany",
        "employment_type": "part-time",
        "experience_level": "junior",
        "salary_min": 15000, "salary_max": 20000,
    },
    {
        "title": "QA Automation Engineer",
        "company": "GameDev Studios",
        "description": "Build, optimize, and maintain massive automated test suites for our flagship multiplayer gaming distribution platform. "
                       "You'll author comprehensive end-to-end browser tests using Playwright, stress-test our backend with intense performance testing scripts, and integrate all test results tightly into Jenkins pipelines. "
                       "Your goal is to catch bugs before our passionate player base does.",
        "requirements": "Python, Playwright, Selenium, pytest, Jenkins, Docker, SQL, Jira, REST APIs",
        "location": "Helsinki, Finland",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 50000, "salary_max": 70000,
    },
    {
        "title": "Platform Engineer (Kubernetes)",
        "company": "SaaS Factory",
        "description": "Architect an enterprise-grade internal developer platform (IDP) and completely self-service infrastructure empowering over 50 disjointed engineering teams. "
                       "You'll design and maintain complex Helm charts, craft custom Kubernetes Operators in Go, and evangelize strict GitOps deployment workflows across the entire engineering org.",
        "requirements": "Kubernetes, Helm, ArgoCD, Terraform, Go, Python, AWS/GCP, Istio, Vault, Linux",
        "location": "Amsterdam, Netherlands",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 80000, "salary_max": 110000,
    },

    # ── Additions from previous iteration ────────────────────────
    {
        "title": "Junior Java Developer",
        "company": "TechTrainee Hub",
        "description": "An excellent, highly-nurturing entry-level opportunity for a recent university graduate or bootcamp alumni. "
                       "You will work on vast enterprise Java applications strictly under the mentorship and code-review guidance of veteran senior engineers. "
                       "You will learn enterprise design patterns, write comprehensive unit tests, and slowly gain ownership of microservice features.",
        "requirements": "Java, Spring, SQL, Git, Basic understanding of REST APIs",
        "location": "Warsaw, Poland",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 35000, "salary_max": 45000,
    },
    {
        "title": "Senior Java Architect",
        "company": "BankCorp Global",
        "description": "Take global lead on the architectural design of impossibly high-throughput, latency-critical forex trading systems. "
                       "You will be strictly responsible for orchestrating large-scale migrations from legacy CORBA mainframes to modern event-driven microservices patterns. "
                       "Excellent stakeholder management, system design acumen, and deep understanding of Java garbage collection optimization are required.",
        "requirements": "Java, Spring Cloud, Kafka, Cassandra, Kubernetes, System Design, Microservices, Domain Driven Design",
        "location": "London, UK",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 110000, "salary_max": 150000,
    },
    {
        "title": "Python Data Developer",
        "company": "Metrics.io",
        "description": "Develop robust internal data wrangling tools and insightful business dashboards empowering hundreds of global data analysts. "
                       "You will work lockstep with product managers to instantly deliver actionable business insights directly into executive leadership's hands. "
                       "You'll build Django apps backed by complex PostgreSQL materialized views.",
        "requirements": "Python, Django, Pandas, PostgreSQL, Docker, Metabase, Git",
        "location": "Remote (US/EU)",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 65000, "salary_max": 85000,
    },
    {
        "title": "Junior Mobile Developer (Flutter)",
        "company": "Startup Inc",
        "description": "Join our founding team to help us build our very first cross-platform mobile application from scratch. "
                       "This is an incredible high-growth learning environment nestled in a fast-paced, highly collaborative startup culture. "
                       "You will work alongside full-stack devs to wire up Firebase logic and implement beautiful, native-feeling widgets in Dart.",
        "requirements": "Dart, Flutter, Firebase, REST APIs, Git",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 40000, "salary_max": 50000,
    },
    {
        "title": "Principal Kubernetes Engineer",
        "company": "CloudNative Core",
        "description": "Design deeply secure and immensely scalable multi-region Kubernetes clusters for Fortune 500 enterprise clients. "
                       "You'll be heavily encouraged to contribute bug fixes and feature enhancements back to massive open-source K8s native projects (like Cilium and Argo). "
                       "Expert-level knowledge of Linux networking interfaces and eBPF is highly regarded.",
        "requirements": "Kubernetes, Go, AWS EKS, GCP GKE, Istio, Cilium, Terraform, Linux kernel",
        "location": "San Francisco, CA",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 150000, "salary_max": 200000,
    },
    {
        "title": "Kotlin Backend Developer",
        "company": "Fintech Disrupt",
        "description": "Help us build absolutely massive-throughput core retail banking systems written purely in idiomatic Kotlin. "
                       "You will strictly embrace functional programming principles and implement event-sourcing with Kafka as the core backbone of truth. "
                       "We emphasize type-safe code, rigorous testing, and immutability everywhere.",
        "requirements": "Kotlin, Spring Boot, Axon Framework, PostgreSQL, Docker, Kafka",
        "location": "Tallinn, Estonia",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 70000, "salary_max": 95000,
    },
    {
        "title": "Senior Vue.js Engineer",
        "company": "E-Commerce Giants",
        "description": "Champion our massive frontend team tasked to painstakingly migrate our sprawling, legacy jQuery storefront to a cutting-edge Vue 3 application. "
                       "Your ultimate focus will be squeezing out milliseconds of web performance, dominating SEO metrics, and ensuring bulletproof accessibility across all target demographics.",
        "requirements": "Vue 3, Nuxt, TypeScript, Pinia, TailwindCSS, Webpack, Jest",
        "location": "Madrid, Spain",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 75000, "salary_max": 90000,
    },
    {
        "title": "Junior Cybersecurity Analyst",
        "company": "SecureNet",
        "description": "Proactively monitor vast internal corporate networks for any hint of potential security breaches and rapidly respond to automated SOC alerts. "
                       "This is the perfect entry point into advanced offensive and defensive enterprise cybersecurity. "
                       "You will document network anomalies, hunt for zero-days on endpoints, and write automated Python threat-intelligence scrapers.",
        "requirements": "Linux, Networking protocols, Python, Wireshark, Splunk basics",
        "location": "Remote",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 45000, "salary_max": 60000,
    },
    {
        "title": "Scala Data Engineer",
        "company": "AdTech Scale",
        "description": "Reliably process an overwhelming billions of ad bidding events per single day leveraging an immense Apache Spark cluster. "
                       "Your extreme focus will be entirely on microsecond latency optimization, managing huge data aggregations over sliding windows, and ensuring absolute data consistency for financial billing ledgers.",
        "requirements": "Scala, Apache Spark, Hadoop, Kafka, AWS EMR, ScalaTest",
        "location": "New York, NY",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 120000, "salary_max": 160000,
    },
    {
        "title": "Data Architect",
        "company": "Global Enterprises",
        "description": "Conceptually design and continually govern the entire multi-national company-wide data strategy, encompassing sprawling data lakes and highly-structured data warehouses. "
                       "You will centrally manage data lineage, enforce strict GDPR/CCPA compliance, and define overarching governance procedures. "
                       "A huge part of your role is unifying siloed business units onto a single Snowflake data mesh.",
        "requirements": "Data Architecture, Snowflake, AWS, Python, dbt, Data Governance, SQL",
        "location": "Frankfurt, Germany",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 110000, "salary_max": 140000,
    },

    # ── BRAND NEW 10 VACANCIES (Detailed & Unique) ───────────────
    {
        "title": "Lead Unity Game Developer",
        "company": "NextGen Studios",
        "description": "Take the technical helm of our highly anticipated AAA open-world RPG title built entirely in Unity. "
                       "You will be directly responsible for architecting core game systems including complex AI behavior trees, seamless level streaming, and custom rendering pipelines. "
                       "You will manage a team of 10+ programmers, coordinate intimately with art and design directors, and squash critical memory leaks prior to major console certification milestones. "
                       "A profound passion for performant C# code and modern game design is an absolute must.",
        "requirements": "Unity, C#, 3D Math, Performance Profiling, Memory Management, Shader Graph, Git, Console SDKs",
        "location": "Montreal, Canada",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 95000, "salary_max": 130000,
    },
    {
        "title": "Junior Smart Contract Engineer",
        "company": "Web3 Innovators",
        "description": "Kickstart your career in the decentralized web by auditing, writing, and deploying resilient Ethereum smart contracts. "
                       "You will closely pair-program with veteran blockchain engineers to implement complex DeFi protocols, automated market makers, and deeply integrated NFT minting logistics. "
                       "You will quickly gain expertise in gas optimization techniques and the meticulous usage of the Foundry and Hardhat testing frameworks.",
        "requirements": "Solidity, Ethereum, Hardhat/Foundry, JavaScript/TypeScript, Web3.js/ethers.js, Git",
        "location": "Remote (Global)",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 50000, "salary_max": 75000,
    },
    {
        "title": "Generative AI Prompt Engineer",
        "company": "Synthetica",
        "description": "Bridge the fascinating gap between linguistics and cutting-edge machine learning logic. "
                       "You will rigorously design, meticulously test, and heavily optimize complex multi-shot prompts for our vast suite of enterprise-grade LLM applications. "
                       "You will systematically orchestrate chaining methods, develop comprehensive evaluation datasets for accuracy tracking, and craft failsafes to completely mitigate AI hallucinations in high-stakes environments.",
        "requirements": "Prompt Engineering, Python, NLP fundamentals, OpenAI API, LangChain, Data Analysis, Critical Thinking",
        "location": "San Francisco, CA",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 85000, "salary_max": 115000,
    },
    {
        "title": "Senior UX/UI Designer",
        "company": "AppCraft Studio",
        "description": "Lead the end-to-end design lifecycle for our flagship multi-tenant B2B SaaS platform. "
                       "You will dive deep into user psychology, conducting extensive user research and A/B testing to intimately understand enterprise workflows. "
                       "From low-fidelity wireframes to absolute pixel-perfect high-fidelity prototypes in Figma, your designs must be beautiful, deeply intuitive, and universally accessible. "
                       "You will collaborate constantly with frontend engineering to ensure pristine visual implementation.",
        "requirements": "Figma, User Research, Wireframing, Prototyping, Design Systems, HTML/CSS basics, Accessibility",
        "location": "London, UK",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 70000, "salary_max": 95000,
    },
    {
        "title": "C++ Trading Systems Developer",
        "company": "AlphaQuant HFT",
        "description": "Design inherently deterministic, ultra-low-latency market data handlers and complex order execution gateways for our immense high-frequency algorithmic trading desk. "
                       "You will write fiercely optimized C++20 code, actively leveraging template metaprogramming, lock-free concurrency, and kernel-bypass networking (DPDK). "
                       "Every single microsecond absolutely counts in this intensely competitive, immensely rewarding role.",
        "requirements": "C++17/20, Linux, Low Latency, Multithreading, Multicast Networking, Algorithm Design, Python",
        "location": "Chicago, IL",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 150000, "salary_max": 250000,
    },
    {
        "title": "Mid-level Salesforce Developer",
        "company": "CRM Experts Group",
        "description": "Build, extensively customize, and maintain critical Salesforce solutions tailored for massive enterprise clients across various sectors. "
                       "You will write deeply customized Apex triggers, interactive Lightning Web Components (LWC), and orchestrate complex declarative flows. "
                       "A significant portion of this role is integrating Salesforce securely via REST APIs with sweeping external legacy ERP and billing systems.",
        "requirements": "Salesforce, Apex, LWC, SOQL, API Integration, Git, Agile Methodologies",
        "location": "Remote (US)",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 80000, "salary_max": 110000,
    },
    {
        "title": "Junior IT Support Specialist",
        "company": "Corporate Tech GmbH",
        "description": "Serve as the reliable, friendly face of IT resolving day-to-day hardware, software, and networking issues for our sprawling 500+ employee office. "
                       "You will provision secure new employee laptops (macOS and Windows), expertly manage SaaS provisioning in Google Workspace/Active Directory, and troubleshoot local network infrastructure limits. "
                       "Excellent, patient communication skills are just as vital as your technical troubleshooting prowess.",
        "requirements": "Windows OS, macOS, Active Directory, Network basics, Customer Service, Ticketing Systems",
        "location": "Munich, Germany",
        "employment_type": "full-time",
        "experience_level": "junior",
        "salary_min": 35000, "salary_max": 45000,
    },
    {
        "title": "Elixir/Phoenix Backend Developer",
        "company": "RealTime ChatOps",
        "description": "Leverage the immense power of the BEAM virtual machine to build profoundly fault-tolerant, highly concurrent real-time backend systems. "
                       "You will architect robust Phoenix LiveView applications and seamlessly manage millions of sustained concurrent WebSocket connections. "
                       "You'll employ rigorous OTP design principles heavily to ensure our distributed message brokering systems never go offline.",
        "requirements": "Elixir, Phoenix, Erlang OTP, PostgreSQL, WebSockets, Redis, Docker",
        "location": "Stockholm, Sweden",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 75000, "salary_max": 105000,
    },
    {
        "title": "Product Owner",
        "company": "Agile Innovations",
        "description": "Own the absolute strategic vision, holistic roadmap, and detailed feature backlog for our flagship predictive analytics dashboard. "
                       "You will continually interview high-value users, meticulously define razor-sharp user stories, and relentlessly prioritize development sprints alongside a dedicated squad of 8 engineers and designers. "
                       "You must deeply balance technical architectural debt against urgent, high-visibility feature launches.",
        "requirements": "Agile, Scrum, Backlog Management, User Stories, Data Analytics, Communication, Jira/Confluence",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "experience_level": "mid",
        "salary_min": 70000, "salary_max": 90000,
    },
    {
        "title": "Senior Computer Vision Engineer",
        "company": "DroneTech Autonomous",
        "description": "Design and fiercely optimize real-time object detection and dynamic tracking algorithms deployed directly to edge computing devices aboard our cutting-edge autonomous drones. "
                       "You will train sophisticated deep learning models rigorously using custom expansive datasets, quantize them for strict local GPU inference constraints, and integrate them completely with flight control telemetry loops. "
                       "Experience with TensorRT and edge-AI accelerators is absolutely paramount.",
        "requirements": "C++, Python, OpenCV, PyTorch, TensorRT, CUDA, Edge AI, Object Detection",
        "location": "Zurich, Switzerland",
        "employment_type": "full-time",
        "experience_level": "senior",
        "salary_min": 105000, "salary_max": 145000,
    },
]

async def seed():
    async with async_session_factory() as session:
        existing = (await session.execute(select(Vacancy))).scalars().all()
        if existing:
            print(f"Clearing {len(existing)} existing vacancies...")
            for e in existing:
                await session.delete(e)
            await session.flush()

        for v in VACANCIES:
            session.add(Vacancy(**v))
        await session.commit()
        print(f"Seeded {len(VACANCIES)} highly detailed vacancies.")


if __name__ == "__main__":
    asyncio.run(seed())
