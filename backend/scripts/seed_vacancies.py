"""Seed the database with 25 diverse vacancies across different roles and stacks."""

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
                       "You will work on transaction processing, fraud detection APIs, and microservice orchestration.",
        "requirements": "Python, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, CI/CD, REST APIs, asyncio",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "salary_min": 75000, "salary_max": 95000,
    },
    {
        "title": "Go Backend Engineer",
        "company": "CloudScale Inc.",
        "description": "Build scalable distributed systems for our cloud infrastructure platform. "
                       "Focus on real-time data pipelines and low-latency services.",
        "requirements": "Go, gRPC, Kafka, PostgreSQL, Docker, Kubernetes, Prometheus, Grafana",
        "location": "Remote (EU)",
        "employment_type": "full-time",
        "salary_min": 80000, "salary_max": 110000,
    },
    {
        "title": "Java Spring Boot Developer",
        "company": "Enterprise Corp",
        "description": "Develop enterprise microservices for insurance claims processing. "
                       "Maintain and extend the existing Spring Boot ecosystem with clean architecture.",
        "requirements": "Java, Spring Boot, Hibernate, Oracle DB, Maven, JUnit, RabbitMQ, Jenkins",
        "location": "Munich, Germany",
        "employment_type": "full-time",
        "salary_min": 65000, "salary_max": 85000,
    },
    {
        "title": "Node.js Backend Developer",
        "company": "SocialApp Ltd.",
        "description": "Build real-time messaging and notification services for our social platform. "
                       "Work with WebSockets, event-driven architecture, and high-throughput APIs.",
        "requirements": "Node.js, TypeScript, Express, MongoDB, Redis, Socket.io, AWS Lambda, GraphQL",
        "location": "London, UK",
        "employment_type": "full-time",
        "salary_min": 60000, "salary_max": 85000,
    },
    {
        "title": "Rust Systems Engineer",
        "company": "CryptoSecure AG",
        "description": "Develop low-level cryptographic libraries and blockchain node software. "
                       "Performance-critical code with a focus on memory safety and zero-copy networking.",
        "requirements": "Rust, C, tokio, libp2p, cryptography, Linux, WebAssembly, Networking",
        "location": "Zurich, Switzerland",
        "employment_type": "full-time",
        "salary_min": 100000, "salary_max": 140000,
    },

    # ── Frontend ─────────────────────────────────────────────────
    {
        "title": "Senior React Frontend Developer",
        "company": "DesignHub",
        "description": "Create beautiful, accessible UI components for our collaborative design tool. "
                       "Pixel-perfect implementation from Figma mockups with smooth animations.",
        "requirements": "React, TypeScript, Next.js, TailwindCSS, Framer Motion, Storybook, Jest, Cypress",
        "location": "Amsterdam, Netherlands",
        "employment_type": "full-time",
        "salary_min": 65000, "salary_max": 90000,
    },
    {
        "title": "Vue.js Frontend Engineer",
        "company": "EduTech Platform",
        "description": "Build interactive learning experiences for our online education platform. "
                       "Focus on real-time collaboration features and rich-text editing.",
        "requirements": "Vue 3, Vuex/Pinia, TypeScript, Vite, SCSS, WebRTC, ProseMirror, Vitest",
        "location": "Paris, France",
        "employment_type": "full-time",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "Angular Frontend Developer",
        "company": "HealthTech Solutions",
        "description": "Develop HIPAA-compliant patient portal and telemedicine dashboard. "
                       "Strong focus on forms, data visualization, and accessibility.",
        "requirements": "Angular, TypeScript, RxJS, NgRx, D3.js, Material UI, Jasmine, Karma",
        "location": "Vienna, Austria",
        "employment_type": "full-time",
        "salary_min": 55000, "salary_max": 70000,
    },

    # ── Fullstack ────────────────────────────────────────────────
    {
        "title": "Fullstack Developer (Python + React)",
        "company": "DataViz Startup",
        "description": "Build end-to-end data visualization platform from API to UI. "
                       "Work across the entire stack including data ingestion pipelines.",
        "requirements": "Python, FastAPI, React, TypeScript, PostgreSQL, D3.js, Docker, Pandas",
        "location": "Hamburg, Germany",
        "employment_type": "full-time",
        "salary_min": 60000, "salary_max": 80000,
    },
    {
        "title": "Fullstack Engineer (Ruby on Rails)",
        "company": "Shopify Partner Agency",
        "description": "Build custom e-commerce solutions and Shopify integrations. "
                       "End-to-end feature development from database schema to polished UI.",
        "requirements": "Ruby, Rails, PostgreSQL, Redis, Hotwire, Stimulus, TailwindCSS, Sidekiq, RSpec",
        "location": "Remote",
        "employment_type": "full-time",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "Fullstack .NET Developer",
        "company": "LogisticsPlus",
        "description": "Develop warehouse management and fleet tracking applications. "
                       "Build RESTful APIs and responsive web frontends for logistics operations.",
        "requirements": "C#, .NET 8, ASP.NET Core, Blazor, SQL Server, Entity Framework, Azure, SignalR",
        "location": "Frankfurt, Germany",
        "employment_type": "full-time",
        "salary_min": 65000, "salary_max": 85000,
    },

    # ── Data & ML ────────────────────────────────────────────────
    {
        "title": "Machine Learning Engineer",
        "company": "AI Research Lab",
        "description": "Design and deploy production ML pipelines for NLP tasks. "
                       "Fine-tune LLMs, build RAG systems, and optimize inference performance.",
        "requirements": "Python, PyTorch, Transformers, LangChain, FastAPI, Docker, MLflow, CUDA, Pandas",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "salary_min": 80000, "salary_max": 110000,
    },
    {
        "title": "Data Engineer",
        "company": "BigData Analytics",
        "description": "Build and maintain scalable ETL pipelines processing terabytes of daily data. "
                       "Design data warehouse schemas and ensure data quality.",
        "requirements": "Python, Apache Spark, Airflow, dbt, Snowflake, SQL, Kafka, AWS S3, Terraform",
        "location": "Dublin, Ireland",
        "employment_type": "full-time",
        "salary_min": 70000, "salary_max": 95000,
    },
    {
        "title": "Data Scientist",
        "company": "RetailAnalytics Co.",
        "description": "Apply statistical modeling and machine learning to optimize pricing strategies "
                       "and demand forecasting for retail clients.",
        "requirements": "Python, scikit-learn, Pandas, NumPy, SQL, Jupyter, Tableau, A/B testing, Statistics",
        "location": "Stockholm, Sweden",
        "employment_type": "full-time",
        "salary_min": 60000, "salary_max": 80000,
    },

    # ── DevOps / SRE ─────────────────────────────────────────────
    {
        "title": "Senior DevOps Engineer",
        "company": "MediaStream GmbH",
        "description": "Manage cloud infrastructure for video streaming platform serving millions of users. "
                       "Automate deployments, monitoring, and incident response.",
        "requirements": "AWS, Terraform, Kubernetes, Docker, GitHub Actions, Prometheus, Grafana, Python, Bash, Linux",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "salary_min": 75000, "salary_max": 100000,
    },
    {
        "title": "Site Reliability Engineer",
        "company": "PaymentGateway Inc.",
        "description": "Ensure 99.99% uptime for critical payment processing infrastructure. "
                       "Design resilient systems, manage incident response, and drive SLO improvements.",
        "requirements": "Linux, Kubernetes, Go, Python, Terraform, Datadog, PagerDuty, PostgreSQL, gRPC",
        "location": "Remote (Global)",
        "employment_type": "full-time",
        "salary_min": 85000, "salary_max": 120000,
    },

    # ── Mobile ───────────────────────────────────────────────────
    {
        "title": "iOS Developer (Swift)",
        "company": "FitnessApp GmbH",
        "description": "Build the next generation of fitness tracking and workout planning features. "
                       "Focus on HealthKit integration, real-time GPS tracking, and smooth animations.",
        "requirements": "Swift, SwiftUI, UIKit, Core Data, HealthKit, MapKit, Combine, XCTest",
        "location": "Munich, Germany",
        "employment_type": "full-time",
        "salary_min": 65000, "salary_max": 85000,
    },
    {
        "title": "Android Developer (Kotlin)",
        "company": "TravelBuddy",
        "description": "Develop offline-first travel companion app with maps, itinerary planning, "
                       "and real-time translation features.",
        "requirements": "Kotlin, Jetpack Compose, Room, Retrofit, Coroutines, Google Maps SDK, Firebase, Hilt",
        "location": "Barcelona, Spain",
        "employment_type": "full-time",
        "salary_min": 55000, "salary_max": 75000,
    },
    {
        "title": "React Native Mobile Developer",
        "company": "FoodDelivery Express",
        "description": "Build cross-platform mobile app for food ordering and delivery tracking. "
                       "Real-time order status, push notifications, and payment integration.",
        "requirements": "React Native, TypeScript, Redux, Firebase, Stripe, Google Maps, Jest, Detox",
        "location": "Warsaw, Poland",
        "employment_type": "full-time",
        "salary_min": 50000, "salary_max": 70000,
    },

    # ── Security / Niche ─────────────────────────────────────────
    {
        "title": "Security Engineer",
        "company": "CyberShield",
        "description": "Perform penetration testing, vulnerability assessments, and security audits. "
                       "Build automated security scanning tools and CI/CD security gates.",
        "requirements": "Python, Burp Suite, OWASP, Docker, Kubernetes, Terraform, AWS IAM, Nmap, Wireshark",
        "location": "Remote (EU)",
        "employment_type": "full-time",
        "salary_min": 70000, "salary_max": 100000,
    },
    {
        "title": "Embedded C/C++ Developer",
        "company": "AutoDrive Systems",
        "description": "Develop firmware for autonomous driving sensor fusion modules. "
                       "Real-time systems programming with strict safety requirements (ISO 26262).",
        "requirements": "C, C++, RTOS, CAN bus, SPI, I2C, ARM Cortex, AUTOSAR, MISRA C, Git",
        "location": "Stuttgart, Germany",
        "employment_type": "full-time",
        "salary_min": 70000, "salary_max": 95000,
    },

    # ── Junior / Internship ──────────────────────────────────────
    {
        "title": "Junior Frontend Developer",
        "company": "Creative Agency Berlin",
        "description": "Join our team to build beautiful marketing websites and landing pages. "
                       "Great opportunity to learn modern web development in a creative environment.",
        "requirements": "HTML, CSS, JavaScript, React, Git, Figma, responsive design",
        "location": "Berlin, Germany",
        "employment_type": "full-time",
        "salary_min": 38000, "salary_max": 45000,
    },
    {
        "title": "Working Student — Backend Development",
        "company": "TU Munich Spin-off",
        "description": "Support our engineering team in building research data management platform. "
                       "Part-time position, flexible hours, perfect for CS students.",
        "requirements": "Python, Flask or FastAPI, SQL, Git, Linux basics",
        "location": "Munich, Germany",
        "employment_type": "part-time",
        "salary_min": 15000, "salary_max": 20000,
    },
    {
        "title": "QA Automation Engineer",
        "company": "GameDev Studios",
        "description": "Build and maintain automated test suites for our multiplayer gaming platform. "
                       "End-to-end, integration, and performance testing.",
        "requirements": "Python, Playwright, Selenium, pytest, Jenkins, Docker, SQL, Jira, REST APIs",
        "location": "Helsinki, Finland",
        "employment_type": "full-time",
        "salary_min": 50000, "salary_max": 70000,
    },
    {
        "title": "Platform Engineer (Kubernetes)",
        "company": "SaaS Factory",
        "description": "Build internal developer platform and self-service infrastructure for 50+ engineering teams. "
                       "Design Helm charts, Operators, and GitOps workflows.",
        "requirements": "Kubernetes, Helm, ArgoCD, Terraform, Go, Python, AWS/GCP, Istio, Vault, Linux",
        "location": "Amsterdam, Netherlands",
        "employment_type": "full-time",
        "salary_min": 80000, "salary_max": 110000,
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
        print(f"Seeded {len(VACANCIES)} vacancies.")


if __name__ == "__main__":
    asyncio.run(seed())
