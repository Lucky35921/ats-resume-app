import os
import re
from collections import OrderedDict
from io import BytesIO
from urllib.parse import quote_plus

import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import docx
except Exception:
    docx = None


st.set_page_config(
    page_title="Universal Skill Gap Matcher + AI Resume Generator",
    page_icon="📄",
    layout="centered"
)

MODEL_NAME = "gpt-4.1-mini"
MAX_AI_CALLS = 5

# ----------------------------
# SKILL LIBRARY
# ----------------------------
SKILL_LIBRARY = OrderedDict({
    "python": "Python",
    "sql": "SQL",
    "excel": "Excel",
    "advanced excel": "Advanced Excel",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "salesforce": "Salesforce",
    "streamlit": "Streamlit",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "scikit-learn": "Scikit-learn",
    "xgboost": "XGBoost",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "statistics": "Statistics",
    "hypothesis testing": "Hypothesis Testing",
    "a/b testing": "A/B Testing",
    "ab testing": "A/B Testing",
    "data analysis": "Data Analysis",
    "exploratory data analysis": "Exploratory Data Analysis",
    "eda": "EDA",
    "data cleaning": "Data Cleaning",
    "data wrangling": "Data Wrangling",
    "data validation": "Data Validation",
    "data accuracy": "Data Accuracy",
    "data integrity": "Data Integrity",
    "dashboard": "Dashboard Development",
    "dashboards": "Dashboard Development",
    "reporting": "Reporting",
    "reports": "Reporting",
    "presentation": "Presentations",
    "presentations": "Presentations",
    "research": "Research",
    "database": "Database Management",
    "databases": "Database Management",
    "database management": "Database Management",
    "data entry": "Data Entry",
    "etl": "ETL",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "git": "Git",
    "github": "GitHub",
    "java": "Java",
    "c++": "C++",
    "c": "C",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "node.js": "Node.js",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "bigquery": "BigQuery",
    "spark": "Spark",
    "hadoop": "Hadoop",
    "linux": "Linux",
    "api": "APIs",
    "rest api": "REST APIs",
    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",
    "analytical": "Analytical Skills",
    "analysis": "Analytical Skills",
    "communication": "Communication",
    "organizational": "Organizational Skills",
    "leadership": "Leadership",
    "teamwork": "Teamwork",
    "stakeholder management": "Stakeholder Management",
    "project management": "Project Management",
    "agile": "Agile",
    "scrum": "Scrum",
    "testing": "Testing",
    "debugging": "Debugging",
    "confidentiality": "Confidentiality",
    "kpi": "KPI Tracking",
    "kpis": "KPI Tracking",
})

# ----------------------------
# LEARNING RESOURCES
# ----------------------------
SKILL_RESOURCES = {
    "Python": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=python+full+course"),
        ("Practice", "https://www.hackerrank.com/domains/python")
    ],
    "SQL": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=sql+full+course"),
        ("Practice", "https://www.hackerrank.com/domains/sql")
    ],
    "Excel": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=excel+full+course"),
        ("Practice", "https://www.youtube.com/results?search_query=excel+practice+for+data+analyst")
    ],
    "Advanced Excel": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=advanced+excel+for+data+analyst"),
        ("Practice", "https://www.youtube.com/results?search_query=advanced+excel+practice")
    ],
    "Power BI": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=power+bi+full+course"),
        ("Microsoft Learn", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/")
    ],
    "Tableau": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=tableau+full+course"),
        ("Tableau Learning", "https://www.tableau.com/learn/training")
    ],
    "Pandas": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=pandas+tutorial"),
        ("Documentation", "https://pandas.pydata.org/docs/")
    ],
    "NumPy": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=numpy+tutorial"),
        ("Documentation", "https://numpy.org/doc/")
    ],
    "Matplotlib": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=matplotlib+tutorial"),
        ("Documentation", "https://matplotlib.org/stable/users/index.html")
    ],
    "Scikit-learn": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=scikit+learn+tutorial"),
        ("Documentation", "https://scikit-learn.org/stable/user_guide.html")
    ],
    "XGBoost": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=xgboost+tutorial"),
        ("Documentation", "https://xgboost.readthedocs.io/")
    ],
    "Statistics": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=statistics+for+data+analysis"),
        ("Learning", "https://www.khanacademy.org/math/statistics-probability")
    ],
    "Hypothesis Testing": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=hypothesis+testing+tutorial"),
        ("Learning", "https://www.youtube.com/results?search_query=hypothesis+testing+for+data+analysis")
    ],
    "A/B Testing": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=a%2Fb+testing+tutorial"),
        ("Learning", "https://www.youtube.com/results?search_query=ab+testing+for+data+analyst")
    ],
    "AWS": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=aws+for+beginners"),
        ("Learning", "https://www.youtube.com/results?search_query=aws+data+engineering+tutorial")
    ],
    "Azure": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=azure+for+beginners"),
        ("Learning", "https://www.youtube.com/results?search_query=azure+data+factory+tutorial")
    ],
    "GCP": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=gcp+for+beginners"),
        ("Learning", "https://www.youtube.com/results?search_query=google+cloud+platform+tutorial")
    ],
    "Git": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=git+and+github+tutorial"),
        ("Documentation", "https://git-scm.com/doc")
    ],
    "GitHub": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=github+tutorial"),
        ("GitHub Skills", "https://skills.github.com/")
    ],
    "MySQL": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=mysql+tutorial"),
        ("Practice", "https://www.youtube.com/results?search_query=mysql+practice+questions")
    ],
    "PostgreSQL": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=postgresql+tutorial"),
        ("Practice", "https://www.youtube.com/results?search_query=postgresql+practice")
    ],
    "MongoDB": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=mongodb+tutorial"),
        ("Documentation", "https://www.mongodb.com/docs/")
    ],
    "BigQuery": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=bigquery+tutorial"),
        ("Learning", "https://www.youtube.com/results?search_query=bigquery+for+beginners")
    ],
    "Streamlit": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=streamlit+tutorial"),
        ("Documentation", "https://docs.streamlit.io/")
    ],
    "Machine Learning": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=machine+learning+full+course"),
        ("Learning", "https://www.youtube.com/results?search_query=machine+learning+for+beginners")
    ],
    "ETL": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=etl+tutorial"),
        ("Learning", "https://www.youtube.com/results?search_query=etl+for+data+analyst")
    ],
    "Salesforce": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=salesforce+tutorial"),
        ("Learning", "https://www.youtube.com/results?search_query=salesforce+for+beginners")
    ],
    "React": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=react+full+course"),
        ("Documentation", "https://react.dev/learn")
    ],
    "JavaScript": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=javascript+full+course"),
        ("Practice", "https://www.youtube.com/results?search_query=javascript+practice")
    ],
    "HTML": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=html+full+course"),
        ("Practice", "https://www.youtube.com/results?search_query=html+practice")
    ],
    "CSS": [
        ("YouTube Tutorial", "https://www.youtube.com/results?search_query=css+full+course"),
        ("Practice", "https://www.youtube.com/results?search_query=css+practice")
    ],
}

# ----------------------------
# BASE LATEX FOR AI MODE
# Put your FULL base resume here
# ----------------------------
BASE_RESUME_LATEX = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[margin=0.26in]{geometry}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{enumitem}
\usepackage{hyperref}
\setlist{nosep}
\titlespacing*{\section}{0pt}{6pt}{2pt}
\setlength{\parskip}{2pt}

\begin{document}
\pagenumbering{gobble}

\begin{center}
\textbf{\LARGE Lakshmana Rao Vallapuneni} \\[2pt]
Grand Rapids, MI \;|\; (616) 329-4914 \;|\; vlakshmanarao216@gmail.com \;|\;
\href{https://linkedin.com/in/lakshmanarao-vallapuneni}{linkedin.com/in/lakshmanarao-vallapuneni} \;|\;
\href{https://github.com/Lucky35921}{github.com/Lucky35921}
\end{center}

\section*{Professional Summary}
Data Analyst with 2+ years of experience specializing in KPI reporting, pricing analytics, and business intelligence. Proven ability to analyze large datasets (50K--200K+ records), automate reporting workflows, and deliver actionable insights that drive 8--40\% improvements in efficiency and performance. Skilled in SQL, Python, Excel, and Power BI with a strong focus on data-driven decision making.

\section*{Technical Skills}
\begin{itemize}[leftmargin=*]
\item \textbf{Programming Languages:}
SQL (Joins, Window Functions, CTEs, Subqueries, Aggregations), Python (Pandas, NumPy), R
\item \textbf{Data Analysis \& Business Intelligence:}
Excel (Pivot Tables, Power Query, Data Modeling, Advanced Formulas), Power BI, KPI Reporting, Dashboard Development, Data Visualization
\item \textbf{Data Engineering:}
ETL, Data Modeling, Data Warehousing, MySQL, MongoDB
\item \textbf{Machine Learning \& Statistics:}
Scikit-learn, XGBoost, Regression, Classification, Hypothesis Testing, A/B Testing
\item \textbf{Tools \& Platforms:}
AWS (S3, EC2, Redshift), Azure (Data Factory, Azure SQL), Git, Jupyter Notebook
\item \textbf{Analytics \& Reporting:}
Data Cleaning, Data Validation, Trend Analysis, Root Cause Analysis, Predictive Analytics, Descriptive Analytics, Stakeholder Communication, Process Improvement
\end{itemize}

\section*{Professional Experience}

\textbf{Data Analyst, Slash Mark IT Solutions Pvt. Ltd., Hyderabad, India}
\hfill \textit{Jul 2023 -- Jul 2024}
\begin{itemize}[leftmargin=*]
\item Automated KPI reporting pipelines using SQL, Python, and Excel across 100K+ records, reducing manual reporting effort by 40\% and accelerating decision-making timelines.
\item Examined 50K--200K records to identify pricing gaps, assortment inefficiencies, and portfolio opportunities, enabling data-driven business decisions.
\item Built interactive Power BI dashboards tracking 10+ KPIs, enhancing real-time visibility for stakeholders across Sales, Pricing, and Operations.
\item Collaborated with cross-functional teams (Sales, Pricing, Supply Chain, Marketing) to translate business requirements into actionable data insights and reporting solutions.
\item Integrated AWS and Azure data sources to streamline reporting workflows and improve data accessibility across systems.
\end{itemize}

\textbf{Data Analyst (Machine Learning Project), Slash Mark IT Solutions Pvt. Ltd.}
\hfill \textit{Dec 2022 -- May 2023}
\begin{itemize}[leftmargin=*]
\item Improved XGBoost models achieving 78.6\% accuracy, improving predictive performance and supporting data-driven decision-making.
\item Built end-to-end ML pipelines including data preprocessing, feature engineering, model training, and evaluation, enhancing model reliability and scalability.
\item Applied statistical techniques, feature engineering, and model evaluation methods to improve model performance and reliability.
\item Delivered visual insights and reports to support stakeholder understanding and data-driven decisions.
\end{itemize}

\textbf{Data Analyst, HCLTech, Hyderabad, India}
\hfill \textit{Oct 2021 -- Oct 2022}
\begin{itemize}[leftmargin=*]
\item Analyzed large datasets using SQL and Python to identify inconsistencies, improve data quality, and lower processing errors by 25\%.
\item Designed Power BI dashboards tracking 10+ KPIs, improving performance visibility and enabling faster decision-making for finance and operations teams.
\item Supported ETL workflows and data migration across multiple systems, enhanced data accuracy by 20\%, reducing reporting discrepancies and enhancing data reliability across systems.
\item Conducted ad-hoc and trend analysis on 10+ datasets, decreased reporting turnaround time by 25\%, enabling faster business decision-making through optimized data workflows.
\end{itemize}

\section*{Projects}

\textbf{Retail Pricing Optimization Analysis -- Excel, SQL, Power BI}
\begin{itemize}[leftmargin=*]
\item Assessed 100K+ retail transactions using SQL, Python, and Power BI to identify pricing inefficiencies and demand patterns, uncovering opportunities for 8--12\% margin improvement.
\item Identified underpriced and overpriced SKUs, enabling potential margin improvement of 8--12\% and supporting data-driven pricing strategy.
\end{itemize}

\textbf{Customer Churn Analysis \& Retention Strategy -- Excel, SQL, Power BI}
\begin{itemize}[leftmargin=*]
\item Investigated 50K+ customer records to identify churn drivers and behavioral patterns, enabling targeted retention strategies that could reduce churn by 15--20\%.
\item Developed retention strategies based on behavioral insights, potentially reducing churn by 15--20\% and improving customer lifetime value.
\end{itemize}

\textbf{Supply Chain \& Inventory Performance Analysis -- Excel, SQL, Power BI}
\begin{itemize}[leftmargin=*]
\item Evaluated supply chain data across 20+ SKUs to identify stockouts and demand variability, recommending strategies that reduced stockouts by 18\% and improved fulfillment efficiency.
\item Recommended inventory optimization strategies reducing stockouts by 18\% and improving order fulfillment efficiency.
\end{itemize}

\section*{Education}
\textbf{Grand Valley State University, Grand Rapids, MI}
\hfill \textit{Aug 2024 -- Expected Apr 2026}

Master of Science in Data Science and Analytics

\textbf{R.V.R \& J.C College of Engineering, Guntur, India}
\hfill \textit{Apr 2020 -- Apr 2024}

Bachelor of Technology in Information Technology

\section*{Certifications}
\begin{itemize}[leftmargin=*]
\item Microsoft Certified Power BI Data Analyst Associate
\item Google Data Analytics Professional Certificate -- Coursera
\item SQL (Advanced) -- HackerRank
\item NPTEL: Data Mining, Machine Learning, DSA using Python
\end{itemize}

\end{document}
"""

# ----------------------------
# HELPERS
# ----------------------------
def normalize_text(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", text).strip()

def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    replacements = {
        "powerbi": "power bi",
        "ms excel": "excel",
        "microsoft excel": "excel",
        "structured query language": "sql",
        "google cloud platform": "gcp",
        "amazon web services": "aws",
        "ab testing": "a/b testing",
    }
    return replacements.get(skill, skill)

def keyword_in_text(keyword: str, text: str) -> bool:
    keyword = re.escape(keyword.lower())
    pattern = rf"(?<!\w){keyword}(?!\w)"
    return bool(re.search(pattern, text.lower()))

@st.cache_data(show_spinner=False)
def extract_text_from_pdf(file_bytes: bytes) -> str:
    if pdfplumber is None:
        return ""
    text_parts = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()

@st.cache_data(show_spinner=False)
def extract_text_from_docx(file_bytes: bytes) -> str:
    if docx is None:
        return ""
    document = docx.Document(BytesIO(file_bytes))
    return "\n".join([p.text for p in document.paragraphs]).strip()

@st.cache_data(show_spinner=False)
def read_uploaded_resume(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    if filename.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="ignore")
    return ""

def extract_library_skills(text: str):
    found = []
    seen = set()
    lower_text = text.lower()

    for phrase, display_name in SKILL_LIBRARY.items():
        if keyword_in_text(phrase, lower_text) and display_name not in seen:
            found.append(display_name)
            seen.add(display_name)

    return found

def extract_skills_from_text(text: str):
    return extract_library_skills(text)

def find_missing_skills(job_description: str, resume_text: str):
    jd_skills = extract_skills_from_text(job_description)
    resume_skills = extract_skills_from_text(resume_text)

    resume_norm = {normalize_skill(skill) for skill in resume_skills}

    missing_skills = []
    for skill in jd_skills:
        if normalize_skill(skill) not in resume_norm:
            missing_skills.append(skill)

    return jd_skills, resume_skills, missing_skills

def get_resources_for_skill(skill: str):
    if skill in SKILL_RESOURCES:
        return SKILL_RESOURCES[skill]

    youtube_link = f"https://www.youtube.com/results?search_query={quote_plus(skill + ' tutorial')}"
    return [
        ("YouTube Tutorial", youtube_link),
        ("Search More", youtube_link),
    ]

def build_ai_prompt(job_description: str, missing_skills: list[str], resume_text: str) -> str:
    missing_text = ", ".join(missing_skills) if missing_skills else "None"

    return f"""
You are an expert LaTeX resume writer.

TASK:
Generate a FULL LaTeX resume code tailored to the job description.

STRICT RULES:
1. Return ONLY complete LaTeX code.
2. The output must be a full compilable LaTeX document from \\documentclass to \\end{{document}}.
3. Keep the same layout, spacing, margins, and style as the base resume.
4. Use the base resume as the starting structure.
5. Update summary, technical skills, experience bullets, and projects to better align with the JD.
6. Keep content realistic and based only on the provided resume text, base resume, and JD.
7. Do not invent fake companies, fake dates, or fake experience.
8. You may strengthen wording and merge JD-relevant skills into existing bullets.
9. Include all major sections:
   - Header
   - Professional Summary
   - Technical Skills
   - Professional Experience
   - Projects
   - Education
   - Certifications
10. Output only raw LaTeX, with no markdown fences and no explanation.

MISSING SKILLS:
{missing_text}

BASE RESUME LATEX:
{BASE_RESUME_LATEX}

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}
""".strip()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Add it locally or in Streamlit Secrets.")
    if OpenAI is None:
        raise ValueError("openai package not installed. Run: pip install openai")
    return OpenAI(api_key=api_key)

@st.cache_data(show_spinner=False)
def cached_generate_latex(job_description: str, missing_skills_key: str, resume_text: str):
    client = get_openai_client()
    missing_skills = missing_skills_key.split("|||") if missing_skills_key else []

    prompt = build_ai_prompt(
        job_description=job_description,
        missing_skills=missing_skills,
        resume_text=resume_text
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    return str(response)

# ----------------------------
# UI
# ----------------------------
st.title("📄 Universal Skill Gap Matcher")
st.caption("Upload your resume, paste a job description, find missing skills, get learning resources, and generate a full LaTeX resume.")
st.markdown(f"**AI model:** `{MODEL_NAME}`")

uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
job_description = st.text_area(
    "Paste the job description",
    height=280,
    placeholder="Paste the full job description here..."
)

use_ai = st.toggle("Enable AI Resume Generation (uses API credits)", value=False)

if not use_ai:
    st.info("AI is OFF. Skill matching and learning resources work for free.")

if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0
if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []
if "jd_skills" not in st.session_state:
    st.session_state.jd_skills = []
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []
if "latex_code" not in st.session_state:
    st.session_state.latex_code = ""

col1, col2 = st.columns(2)
with col1:
    analyze = st.button("Find Missing Skills", type="primary", use_container_width=True)
with col2:
    generate = st.button("Generate Full LaTeX Resume", use_container_width=True)

if analyze:
    if uploaded_resume is None:
        st.error("Please upload your resume first.")
    elif not job_description.strip():
        st.error("Please paste the job description.")
    else:
        with st.spinner("Extracting skills and comparing..."):
            resume_text = read_uploaded_resume(uploaded_resume)
            resume_text = normalize_text(resume_text)
            job_description_clean = normalize_text(job_description)

            jd_skills, resume_skills, missing_skills = find_missing_skills(
                job_description_clean,
                resume_text
            )

            st.session_state.jd_skills = jd_skills
            st.session_state.resume_skills = resume_skills
            st.session_state.missing_skills = missing_skills

        st.subheader("Missing Skills")
        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.success("No missing skills found.")

        with st.expander("Show extracted job description skills"):
            st.write(", ".join(jd_skills) if jd_skills else "No skills detected from job description.")

        with st.expander("Show extracted resume skills"):
            st.write(", ".join(resume_skills) if resume_skills else "No skills detected from resume.")

        st.subheader("Learning Resources for Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"### {skill}")
                for title, url in get_resources_for_skill(skill):
                    st.markdown(f"- [{title}]({url})")
        else:
            st.write("No resources needed because no missing skills were found.")

if generate:
    if uploaded_resume is None:
        st.warning("Please upload your resume first.")
    elif not job_description.strip():
        st.warning("Please paste the job description.")
    elif not use_ai:
        st.warning("Enable AI Resume Generation first.")
    else:
        if st.session_state.api_calls >= MAX_AI_CALLS:
            st.error(f"Daily AI limit reached ({MAX_AI_CALLS} calls).")
        else:
            try:
                resume_text = read_uploaded_resume(uploaded_resume)
                resume_text = normalize_text(resume_text)

                if not resume_text:
                    st.error("Could not extract resume text.")
                else:
                    # If user did not click Analyze first, compute skills now
                    if not st.session_state.jd_skills and not st.session_state.resume_skills:
                        jd_skills, resume_skills, missing_skills = find_missing_skills(
                            normalize_text(job_description),
                            resume_text
                        )
                        st.session_state.jd_skills = jd_skills
                        st.session_state.resume_skills = resume_skills
                        st.session_state.missing_skills = missing_skills

                    missing_skills_key = "|||".join(st.session_state.missing_skills)

                    with st.spinner("Generating full LaTeX resume..."):
                        latex_code = cached_generate_latex(
                            normalize_text(job_description),
                            missing_skills_key,
                            resume_text
                        )

                    st.session_state.api_calls += 1
                    st.session_state.latex_code = latex_code
                    st.success("Full LaTeX resume generated successfully.")

            except Exception as e:
                st.error(f"AI generation failed: {str(e)}")

if st.session_state.latex_code:
    st.subheader("Generated Full LaTeX Resume")
    st.text_area("LaTeX Output", st.session_state.latex_code, height=500)

    st.download_button(
        label="Download tailored_resume.tex",
        data=st.session_state.latex_code,
        file_name="tailored_resume.tex",
        mime="text/plain"
    )

st.markdown("---")
st.caption(f"AI calls used this session: {st.session_state.api_calls}/{MAX_AI_CALLS}")
