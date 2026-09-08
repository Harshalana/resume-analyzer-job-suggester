"""
CareerCraft AI - Skill Taxonomy, Action Verbs, and Market Roles Database
"""

from typing import Dict, List, Any

# Extensive Skill Taxonomy Categorized
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "golang", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "c", "shell", "bash",
        "powershell", "perl", "haskell", "elixir", "clojure", "matlab", "lua", "julia"
    ],
    "Web & Frontend Frameworks": [
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "svelte", "sveltekit",
        "html5", "html", "css3", "css", "tailwind css", "tailwind", "bootstrap", "sass", "scss",
        "redux", "zustand", "mobx", "webgl", "three.js", "vite", "webpack", "babel",
        "jquery", "material-ui", "shadcn", "framer motion", "storybook"
    ],
    "Backend & APIs": [
        "node.js", "express.js", "express", "fastapi", "django", "flask", "spring boot",
        "spring", "asp.net", ".net core", ".net", "ruby on rails", "rails", "nestjs",
        "graphql", "rest api", "restful api", "rest", "grpc", "microservices", "websockets",
        "gin", "fiber", "actix", "rocket", "celery", "kafka", "rabbitmq"
    ],
    "AI, ML & Data Science": [
        "machine learning", "deep learning", "artificial intelligence", "nlp",
        "natural language processing", "computer vision", "llm", "large language models",
        "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "hugging face",
        "transformers", "langchain", "llamaindex", "rag", "retrieval augmented generation",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "opencv", "mlops", "data analysis",
        "data engineering", "feature engineering", "predictive modeling", "spark", "pyspark",
        "vector database", "fine-tuning", "prompt engineering", "genai", "generative ai"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "docker", "kubernetes", "k8s", "terraform", "ansible", "helm", "ci/cd", "ci cd",
        "github actions", "gitlab ci", "jenkins", "circleci", "linux", "ubuntu", "nginx",
        "serverless", "aws lambda", "cloudformation", "prometheus", "grafana", "datadog",
        "sre", "site reliability engineering", "iac", "infrastructure as code"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
        "dynamodb", "cassandra", "snowflake", "bigquery", "redshift", "neo4j", "supabase",
        "firebase", "firestore", "couchdb", "mariadb", "pinecone", "chromadb", "weaviate",
        "qdrant", "milvus", "prisma", "sqlalchemy", "hibernate"
    ],
    "Methodologies & Tools": [
        "git", "github", "gitlab", "jira", "confluence", "agile", "scrum", "kanban",
        "tdd", "test driven development", "unit testing", "integration testing", "pytest",
        "jest", "cypress", "playwright", "selenium", "system design", "distributed systems",
        "design patterns", "clean code", "clean architecture", "code review", "postman"
    ],
    "Soft Skills & Leadership": [
        "leadership", "team management", "communication", "problem solving", "critical thinking",
        "project management", "cross-functional collaboration", "mentorship", "stakeholder management",
        "time management", "adaptability", "conflict resolution", "agile leadership", "client relations",
        "decision making", "presentation skills", "strategic planning"
    ]
}

# Flat list of all recognized skill synonyms and canonical names
CANONICAL_SKILL_MAP: Dict[str, str] = {
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular",
    "nodejs": "node.js",
    "node": "node.js",
    "nextjs": "next.js",
    "next": "next.js",
    "expressjs": "express.js",
    "express": "express.js",
    "golang": "go",
    "postgres": "postgresql",
    "k8s": "kubernetes",
    "sklearn": "scikit-learn",
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "microsoft azure": "azure",
    "ci/cd": "ci/cd",
    "ci-cd": "ci/cd",
    "restful apis": "rest api",
    "restful api": "rest api",
    "rest api": "rest api",
    "llms": "llm",
    "large language models": "llm",
    "generative ai": "genai",
    "gen ai": "genai",
    "artificial intelligence": "ai",
    "machine learning": "machine learning",
    "deep learning": "deep learning",
    "natural language processing": "nlp",
    "test-driven development": "tdd",
    "test driven development": "tdd",
}

# Strong Action Verbs for ATS and Resume Impact Evaluation
ACTION_VERBS = {
    "leadership": [
        "spearheaded", "orchestrated", "championed", "directed", "led", "governed",
        "pioneered", "guided", "mentored", "empowered", "supervised", "mobilized"
    ],
    "development": [
        "engineered", "architected", "developed", "built", "implemented", "constructed",
        "programmed", "designed", "created", "authored", "deployed", "refactored"
    ],
    "optimization": [
        "optimized", "accelerated", "streamlined", "overhauled", "enhanced", "boosted",
        "amplified", "modernized", "automated", "consolidated", "upgraded", "maximized"
    ],
    "impact_results": [
        "reduced", "increased", "generated", "saved", "achieved", "delivered",
        "scaled", "expanded", "outperformed", "yielded", "decreased", "secured"
    ],
    "research_analysis": [
        "evaluated", "benchmarked", "diagnosed", "uncovered", "modeled", "formulated",
        "discovered", "quantified", "audited", "surveyed", "synthesized", "validated"
    ]
}

ALL_ACTION_VERBS = set(verb for sublist in ACTION_VERBS.values() for verb in sublist)

# Curated High-Demand Market Job Roles Database
MARKET_JOB_ROLES: List[Dict[str, Any]] = [
    {
        "id": "senior-fullstack-engineer",
        "title": "Senior Full-Stack Software Engineer",
        "category": "Software Engineering",
        "level": "Senior",
        "experience_years": "4-7 years",
        "salary_range": "$135,000 - $185,000",
        "demand": "Very High",
        "description": "Lead end-to-end architecture and implementation of scalable web applications, integrating modern frontend frameworks with resilient cloud-native backends.",
        "required_skills": ["react", "typescript", "node.js", "postgresql", "docker", "aws", "rest api", "git", "system design"],
        "bonus_skills": ["next.js", "graphql", "kubernetes", "redis", "ci/cd", "microservices", "tailwind css"],
        "learning_roadmap": [
            {"topic": "Distributed System Design", "resource": "Designing Data-Intensive Applications by Martin Kleppmann"},
            {"topic": "Advanced Cloud Architecture", "resource": "AWS Certified Solutions Architect Associate"},
            {"topic": "Micro-Frontends & SSR", "resource": "Next.js 14 App Router & Server Components Masterclass"}
        ]
    },
    {
        "id": "ai-ml-engineer",
        "title": "AI & Machine Learning Engineer",
        "category": "Data & AI",
        "level": "Mid-Senior",
        "experience_years": "3-6 years",
        "salary_range": "$145,000 - $205,000",
        "demand": "Extremely High",
        "description": "Design, fine-tune, and deploy state-of-the-art machine learning, deep learning, and generative AI models (LLMs/RAG) into production cloud environments.",
        "required_skills": ["python", "pytorch", "machine learning", "deep learning", "nlp", "scikit-learn", "docker", "pandas", "llm"],
        "bonus_skills": ["langchain", "llamaindex", "rag", "vector database", "hugging face", "fastapi", "mlops", "aws", "genai"],
        "learning_roadmap": [
            {"topic": "LLM Application Engineering & RAG", "resource": "DeepLearning.AI: Building Systems with the ChatGPT API & LangChain"},
            {"topic": "Production MLOps", "resource": "Coursera: Machine Learning Engineering for Production (MLOps)"},
            {"topic": "Vector Search & Retrieval", "resource": "Pinecone / Qdrant vector database architecture guides"}
        ]
    },
    {
        "id": "devops-cloud-architect",
        "title": "DevOps & Cloud Infrastructure Engineer",
        "category": "Cloud & DevOps",
        "level": "Mid-Senior",
        "experience_years": "3-6 years",
        "salary_range": "$130,000 - $175,000",
        "demand": "Very High",
        "description": "Build automated CI/CD pipelines, container orchestration, and Infrastructure-as-Code platforms ensuring high availability, security, and scalability.",
        "required_skills": ["aws", "docker", "kubernetes", "terraform", "ci/cd", "linux", "github actions", "bash", "python"],
        "bonus_skills": ["helm", "ansible", "prometheus", "grafana", "gcp", "azure", "security", "sre"],
        "learning_roadmap": [
            {"topic": "Kubernetes Administration", "resource": "CKA (Certified Kubernetes Administrator) Curriculum"},
            {"topic": "Infrastructure as Code", "resource": "HashiCorp Certified Terraform Associate"},
            {"topic": "Observability & Site Reliability", "resource": "Google SRE Handbook & Prometheus/Grafana stack"}
        ]
    },
    {
        "id": "frontend-engineer",
        "title": "Frontend React / Next.js Developer",
        "category": "Software Engineering",
        "level": "Mid-Level",
        "experience_years": "2-5 years",
        "salary_range": "$105,000 - $145,000",
        "demand": "High",
        "description": "Craft highly responsive, accessible, and performant user interfaces using React, Next.js, and TypeScript with pixel-perfect UI standards.",
        "required_skills": ["javascript", "typescript", "react", "html5", "css3", "tailwind css", "git", "rest api"],
        "bonus_skills": ["next.js", "redux", "zustand", "jest", "cypress", "figma", "webgl", "graphql"],
        "learning_roadmap": [
            {"topic": "Advanced React Patterns", "resource": "EpicReact.dev & React 19 Concurrent Features"},
            {"topic": "Core Web Vitals & Web Performance", "resource": "web.dev performance tuning and accessibility best practices"},
            {"topic": "End-to-End Testing", "resource": "Playwright / Cypress automated UI testing suite"}
        ]
    },
    {
        "id": "backend-python-engineer",
        "title": "Backend Python / FastAPI Engineer",
        "category": "Software Engineering",
        "level": "Mid-Senior",
        "experience_years": "3-6 years",
        "salary_range": "$125,000 - $170,000",
        "demand": "High",
        "description": "Architect robust RESTful & GraphQL backend APIs, data pipelines, caching layers, and microservices with Python, FastAPI/Django, and SQL databases.",
        "required_skills": ["python", "fastapi", "postgresql", "docker", "rest api", "git", "unit testing", "redis"],
        "bonus_skills": ["django", "celery", "kafka", "aws", "microservices", "graphql", "sqlalchemy", "ci/cd"],
        "learning_roadmap": [
            {"topic": "Asynchronous Python & Concurrency", "resource": "AsyncIO in Python: Create Fast Event-Driven Applications"},
            {"topic": "High-Throughput Caching & Queues", "resource": "Redis & Apache Kafka for Real-Time Event Streams"},
            {"topic": "Database Indexing & Query Optimization", "resource": "Use The Index, Luke! - Guide to Database Performance"}
        ]
    },
    {
        "id": "data-engineer",
        "title": "Data Engineer / ETL Pipeline Specialist",
        "category": "Data & AI",
        "level": "Mid-Senior",
        "experience_years": "3-6 years",
        "salary_range": "$130,000 - $175,000",
        "demand": "Very High",
        "description": "Construct large-scale data lakes, ingestion pipelines, ETL transformations, and warehouse infrastructure for business analytics and ML applications.",
        "required_skills": ["python", "sql", "spark", "postgresql", "data engineering", "aws", "docker", "git"],
        "bonus_skills": ["snowflake", "bigquery", "kafka", "airflow", "dbt", "pyspark", "data modeling", "gcp"],
        "learning_roadmap": [
            {"topic": "Modern Data Stack & Transformations", "resource": "dbt Fundamentals & Snowflake Data Warehousing"},
            {"topic": "Distributed Data Processing", "resource": "Apache Spark & PySpark Masterclass"},
            {"topic": "Workflow Orchestration", "resource": "Apache Airflow / Prefect Workflow Automation"}
        ]
    },
    {
        "id": "technical-product-manager",
        "title": "Technical Product Manager",
        "category": "Product & Management",
        "level": "Mid-Senior",
        "experience_years": "3-7 years",
        "salary_range": "$130,000 - $180,000",
        "demand": "High",
        "description": "Bridge engineering, user experience, and business strategy to define product roadmaps, user stories, feature specifications, and go-to-market execution.",
        "required_skills": ["product management", "agile", "scrum", "jira", "data analysis", "cross-functional collaboration", "stakeholder management", "communication"],
        "bonus_skills": ["sql", "system design", "python", "user research", "a/b testing", "strategic planning", "presentation skills"],
        "learning_roadmap": [
            {"topic": "Product Metrics & Growth", "resource": "Reforge Product Strategy & Metrics Certification"},
            {"topic": "SQL for Product Analytics", "resource": "Mode Analytics SQL for Data Analysis"},
            {"topic": "Scrum Product Owner", "resource": "PSPO (Professional Scrum Product Owner) certification"}
        ]
    },
    {
        "id": "cybersecurity-analyst",
        "title": "Cybersecurity & Information Security Analyst",
        "category": "Security",
        "level": "Mid-Level",
        "experience_years": "2-5 years",
        "salary_range": "$110,000 - $155,000",
        "demand": "Very High",
        "description": "Monitor, analyze, and protect enterprise infrastructure from vulnerabilities, cyber threats, and security breaches while ensuring compliance standards.",
        "required_skills": ["linux", "python", "bash", "security", "threat analysis", "vulnerability assessment", "git"],
        "bonus_skills": ["aws", "docker", "penetration testing", "siem", "wireshark", "cryptography", "cissp", "owasp"],
        "learning_roadmap": [
            {"topic": "Security Fundamentals & Compliance", "resource": "CompTIA Security+ & CEH (Certified Ethical Hacker)"},
            {"topic": "Cloud Security Architecture", "resource": "AWS Certified Security - Specialty"},
            {"topic": "Web Application Security", "resource": "OWASP Top 10 Security Risks & PortSwigger Web Security Academy"}
        ]
    },
    {
        "id": "junior-software-developer",
        "title": "Junior Software Engineer / Associate Developer",
        "category": "Software Engineering",
        "level": "Entry-Level",
        "experience_years": "0-2 years",
        "salary_range": "$75,000 - $105,000",
        "demand": "High",
        "description": "Collaborate with senior engineers to write clean, maintainable code, test features, fix bugs, and learn modern software engineering practices.",
        "required_skills": ["python", "javascript", "git", "html", "css", "sql", "problem solving"],
        "bonus_skills": ["react", "node.js", "docker", "unit testing", "rest api", "fastapi", "typescript"],
        "learning_roadmap": [
            {"topic": "Data Structures & Algorithms", "resource": "NeetCode 150 & LeetCode medium problems"},
            {"topic": "Git & Collaborative Development", "resource": "Pro Git Book & GitHub Open Source contributions"},
            {"topic": "Full-Stack Project Portfolio", "resource": "Build 2 full-stack end-to-end applications deployed live on Vercel/Render"}
        ]
    }
]

