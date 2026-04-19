"""
Controlled skills dictionary — the canonical list of skills the matching engine knows.

This is a simple keyword bank used by the v1 extractor.
Each canonical skill maps to a list of surface-form aliases that may appear in
resume or vacancy text.  The aliases are lowercased and matched as whole words.

EXTENSION POINTS:
  - Add / remove skills here as the domain grows.
  - Later this file can be replaced by a skills ontology (ESCO, O*NET).
  - For v2 (TF-IDF / embeddings) the extractor can fall back to these
    skills for explainability even when the model changes.
"""

# ── Skill → aliases mapping ─────────────────────────────────────────
# The canonical name (key) is used in matched_skills / missing_skills output.
# Aliases are lower-case variants and common abbreviations.
SKILLS_DB: dict[str, list[str]] = {
    # ── Programming languages ────────────────────────────────────────
    "Python": ["python", "py"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "Java": ["java", "j2ee"],
    "C++": ["c++", "cpp", "c plus plus"],
    "C#": ["c#", "csharp", "dotnet"],
    "Go": ["go", "golang"],
    "Rust": ["rust", "rs"],
    "Ruby": ["ruby", "rb"],
    "PHP": ["php"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin", "kt"],
    "Scala": ["scala"],
    "R": ["r programming", "r language"],
    "SQL": ["sql"],
    "Shell": ["shell", "bash", "zsh", "sh"],
    "C": ["c programming", "c language", "ansi c"],

    # ── Web frameworks & libraries ───────────────────────────────────
    "React": ["react", "reactjs", "react.js"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Angular": ["angular", "angularjs", "ng"],
    "Next.js": ["next", "nextjs", "next.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi", "fast api"],
    "Express": ["express", "expressjs", "express.js"],
    "Spring Boot": ["spring boot", "springboot", "spring"],
    "Rails": ["rails", "ruby on rails", "ror"],
    "Laravel": ["laravel"],
    "Node.js": ["node", "nodejs", "node.js"],
    "Svelte": ["svelte"],
    "ASP.NET": ["asp.net", "asp.net core", "aspnet"],
    "Blazor": ["blazor"],
    "Hibernate": ["hibernate"],
    "RabbitMQ": ["rabbitmq", "rabbit mq"],
    "Kafka": ["kafka", "apache kafka"],
    "gRPC": ["grpc", "g rpc"],
    "WebSocket": ["websocket", "websockets", "socket.io"],
    "Sidekiq": ["sidekiq"],
    "Hotwire": ["hotwire", "stimulus"],
    "SignalR": ["signalr"],

    # ── Data & ML ────────────────────────────────────────────────────
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "NLP": ["nlp", "natural language processing"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "np"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Visualization": ["data visualization", "dataviz"],
    "Matplotlib": ["matplotlib"],
    "Jupyter": ["jupyter", "jupyter notebook"],
    "Spark": ["spark", "apache spark", "pyspark"],
    "Airflow": ["airflow", "apache airflow"],
    "dbt": ["dbt"],
    "Snowflake": ["snowflake"],
    "Tableau": ["tableau"],
    "LangChain": ["langchain"],
    "MLflow": ["mlflow"],
    "Transformers": ["transformers", "huggingface", "hugging face"],

    # ── Databases ────────────────────────────────────────────────────
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "Elasticsearch": ["elasticsearch", "elastic"],
    "SQLite": ["sqlite"],
    "Oracle": ["oracle db", "oracle database"],
    "Cassandra": ["cassandra"],
    "DynamoDB": ["dynamodb", "dynamo db"],
    "SQL Server": ["sql server", "mssql"],
    "Entity Framework": ["entity framework", "ef core"],

    # ── Cloud & DevOps ───────────────────────────────────────────────
    "AWS": ["aws", "amazon web services"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure", "microsoft azure"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s", "kuber"],
    "Terraform": ["terraform", "tf"],
    "CI/CD": ["ci/cd", "ci cd", "continuous integration", "continuous deployment"],
    "Jenkins": ["jenkins"],
    "GitHub Actions": ["github actions", "gha"],
    "GitLab CI": ["gitlab ci", "gitlab"],
    "Ansible": ["ansible"],
    "Linux": ["linux"],
    "Nginx": ["nginx"],
    "Prometheus": ["prometheus"],
    "Grafana": ["grafana"],
    "Datadog": ["datadog"],
    "Helm": ["helm"],
    "ArgoCD": ["argocd", "argo cd"],
    "Istio": ["istio"],
    "Vault": ["vault", "hashicorp vault"],

    # ── Tools & practices ────────────────────────────────────────────
    "Git": ["git", "version control"],
    "REST API": ["rest", "rest api", "restful api"],
    "GraphQL": ["graphql", "gql"],
    "Agile": ["agile", "scrum", "kanban", "sprint"],
    "TDD": ["tdd", "test driven development", "test-driven development"],
    "Microservices": ["microservices", "micro services", "microservice"],
    "System Design": ["system design", "architecture design"],
    "API Design": ["api design", "api development"],
    "OAuth": ["oauth", "oauth2", "jwt", "json web token"],
    "Testing": ["testing", "unit testing", "integration testing"],
    "pytest": ["pytest", "py.test"],
    "Jest": ["jest"],
    "Selenium": ["selenium"],
    "Playwright": ["playwright"],
    "Cypress": ["cypress"],
    "JUnit": ["junit", "junit5"],
    "RSpec": ["rspec"],
    "Storybook": ["storybook"],
    "Figma": ["figma"],
    "D3.js": ["d3", "d3.js"],

    # ── Mobile ──────────────────────────────────────────────────────────
    "React Native": ["react native"],
    "Flutter": ["flutter"],
    "SwiftUI": ["swiftui"],
    "Jetpack Compose": ["jetpack compose"],
    "Firebase": ["firebase"],
    "Redux": ["redux"],
    "Stripe": ["stripe"],

    # ── General soft skills & domain knowledge ──────────────────────
    "Communication": ["communication", "verbal communication"],
    "Teamwork": ["teamwork", "team player", "collaboration"],
    "Problem Solving": ["problem solving", "analytical thinking"],
    "Project Management": ["project management", "pm"],
    "Leadership": ["leadership", "leading"],
}


def get_all_skill_aliases() -> dict[str, str]:
    """
    Return a flat mapping: alias → canonical_skill_name.
    Used for fast lookup during text scanning.
    """
    alias_map: dict[str, str] = {}
    for canonical, aliases in SKILLS_DB.items():
        for alias in aliases:
            alias_map[alias] = canonical
    return alias_map


# ── Weighted Skill Priority ─────────────────────────────────────────

CORE_SKILLS = {
    # Programming languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", 
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "Shell", "C",
    # Web frameworks & libraries
    "React", "Vue.js", "Angular", "Next.js", "Django", "Flask", "FastAPI", 
    "Express", "Spring Boot", "Rails", "Laravel", "Node.js", "Svelte", "ASP.NET", 
    "Blazor", "Hibernate", "RabbitMQ", "Kafka", "gRPC", "WebSocket", "Sidekiq", 
    "Hotwire", "SignalR",
    # Data & ML
    "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch", 
    "scikit-learn", "Pandas", "NumPy", "Data Analysis", "Data Visualization", 
    "Matplotlib", "Jupyter", "Spark", "Airflow", "dbt", "Snowflake", "Tableau", 
    "LangChain", "MLflow", "Transformers",
    # Mobile
    "React Native", "Flutter", "SwiftUI", "Jetpack Compose", "Firebase", 
    "Redux", "Stripe"
}

SOFT_SKILLS = {
    # General soft skills & domain knowledge
    "Communication", "Teamwork", "Problem Solving", "Project Management", "Leadership"
}

def get_skill_weight(canonical_skill: str) -> float:
    """
    Returns the weight of a skill based on its category.
    Core Tech (Languages, Frameworks, ML): 2.0
    Secondary Tech (DBs, Cloud, Tools): 1.0 (default)
    Soft Skills: 0.5
    """
    if canonical_skill in CORE_SKILLS:
        return 2.0
    elif canonical_skill in SOFT_SKILLS:
        return 0.5
    return 1.0
