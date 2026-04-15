from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0F172A")
INDIGO     = colors.HexColor("#4F46E5")
CYAN       = colors.HexColor("#06B6D4")
VIOLET     = colors.HexColor("#7C3AED")
RED        = colors.HexColor("#DC2626")
GREEN      = colors.HexColor("#16A34A")
AMBER      = colors.HexColor("#F59E0B")
SLATE      = colors.HexColor("#334155")
MUTED      = colors.HexColor("#64748B")
LIGHT      = colors.HexColor("#F1F5F9")
WHITE      = colors.white
BLACK      = colors.HexColor("#0F172A")

W, H = A4   # 595 x 842 pts

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s["cover_title"] = ParagraphStyle("cover_title",
        fontName="Helvetica-Bold", fontSize=32, leading=40,
        textColor=WHITE, alignment=TA_CENTER)

    s["cover_sub"] = ParagraphStyle("cover_sub",
        fontName="Helvetica", fontSize=13, leading=20,
        textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER)

    s["cover_badge"] = ParagraphStyle("cover_badge",
        fontName="Helvetica-Bold", fontSize=11, leading=16,
        textColor=WHITE, alignment=TA_CENTER)

    s["section_heading"] = ParagraphStyle("section_heading",
        fontName="Helvetica-Bold", fontSize=18, leading=24,
        textColor=NAVY, spaceBefore=6, spaceAfter=4)

    s["track_title"] = ParagraphStyle("track_title",
        fontName="Helvetica-Bold", fontSize=15, leading=20,
        textColor=WHITE)

    s["track_sub"] = ParagraphStyle("track_sub",
        fontName="Helvetica", fontSize=10, leading=14,
        textColor=colors.HexColor("#CBD5E1"))

    s["module_title"] = ParagraphStyle("module_title",
        fontName="Helvetica-Bold", fontSize=11, leading=15,
        textColor=NAVY, spaceBefore=4)

    s["body"] = ParagraphStyle("body",
        fontName="Helvetica", fontSize=10, leading=15,
        textColor=colors.HexColor("#374151"), spaceAfter=4)

    s["bullet"] = ParagraphStyle("bullet",
        fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=colors.HexColor("#374151"),
        leftIndent=12, spaceAfter=2)

    s["caption"] = ParagraphStyle("caption",
        fontName="Helvetica", fontSize=8.5, leading=12,
        textColor=MUTED)

    s["label"] = ParagraphStyle("label",
        fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=MUTED)

    s["project_title"] = ParagraphStyle("project_title",
        fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=INDIGO)

    s["footer"] = ParagraphStyle("footer",
        fontName="Helvetica", fontSize=8, leading=11,
        textColor=MUTED, alignment=TA_CENTER)

    return s

S = make_styles()

# ── Helper flowables ──────────────────────────────────────────────────────────
def hline(color=SLATE, thickness=0.5, spaceB=6, spaceA=6):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=spaceA, spaceBefore=spaceB)

def spacer(h=6):
    return Spacer(1, h)

def bullet_item(text, color=INDIGO):
    return Paragraph(f'<font color="#{color.hexval()[2:]}">&#9679;</font>  {text}', S["bullet"])

def check_item(text):
    return Paragraph(f'<font color="#16A34A">&#10003;</font>  {text}', S["bullet"])

# ── Coloured banner for track headers ─────────────────────────────────────────
def track_banner(title, subtitle, audience, duration, accent):
    data = [[
        Paragraph(f'<b>{title}</b>', S["track_title"]),
        Paragraph(subtitle, S["track_sub"]),
    ]]
    info = [[
        Paragraph(f'<b>Who:</b> {audience}', S["track_sub"]),
        Paragraph(f'<b>Duration:</b> {duration}', S["track_sub"]),
    ]]
    banner_table = Table([[
        Table(data, colWidths=[180, 200]),
        Table(info, colWidths=[130, 110]),
    ]], colWidths=[390, 150])
    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), accent),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [8,8,8,8]),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return banner_table

# ── Module table ──────────────────────────────────────────────────────────────
def module_table(modules, accent):
    rows = []
    for m in modules:
        rows.append([
            Paragraph(f'<b>{m["name"]}</b>', S["module_title"]),
            Paragraph(m["days"], S["caption"]),
        ])
        for topic in m["topics"]:
            rows.append([
                Paragraph(f'&#8226;  {topic}', S["bullet"]),
                "",
            ])
        rows.append(["", ""])   # spacer row

    col_w = [370, 80]
    t = Table(rows, colWidths=col_w)
    style = [
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING",   (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, WHITE]),
    ]
    # colour module-name rows
    row_idx = 0
    for m in modules:
        style.append(("BACKGROUND", (0,row_idx),(1,row_idx), LIGHT))
        style.append(("TEXTCOLOR",  (1,row_idx),(1,row_idx), accent))
        row_idx += len(m["topics"]) + 2   # name row + topics + spacer

    t.setStyle(TableStyle(style))
    return t

# ── Stats bar ─────────────────────────────────────────────────────────────────
def stats_bar(stats, accent):
    cells = [[Paragraph(f'<b>{v}</b>', ParagraphStyle("sv",
                fontName="Helvetica-Bold", fontSize=16, textColor=accent,
                alignment=TA_CENTER)),
              Paragraph(k, ParagraphStyle("sk",
                fontName="Helvetica", fontSize=8, textColor=MUTED,
                alignment=TA_CENTER))]
             for k, v in stats.items()]

    rows = [[c[0] for c in cells], [c[1] for c in cells]]
    col_w = [int((W - 80) / len(stats))] * len(stats)
    t = Table(rows, colWidths=col_w)
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("BACKGROUND",    (0,0),(-1,-1), LIGHT),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),[6,6,6,6]),
        ("LINEBELOW",     (0,0),(-1,0),  0.5, accent),
    ]))
    return t

# ── Capstone project box ───────────────────────────────────────────────────────
def capstone_box(title, description, deliverables, stack, accent):
    content = [
        [Paragraph(f'&#127963;  CAPSTONE PROJECT', ParagraphStyle("cp_label",
            fontName="Helvetica-Bold", fontSize=8, textColor=accent,
            spaceAfter=2))],
        [Paragraph(f'<b>{title}</b>', S["project_title"])],
        [Paragraph(description, S["body"])],
        [Paragraph('<b>What you build:</b>', S["label"])],
    ]
    for d in deliverables:
        content.append([check_item(d)])
    content.append([Paragraph(f'<b>Stack:</b> {stack}', S["label"])])

    inner = Table(content, colWidths=[440])
    inner.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
    ]))

    outer = Table([[inner]], colWidths=[460])
    outer.setStyle(TableStyle([
        ("BOX",           (0,0),(-1,-1), 1.5, accent),
        ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#F5F3FF")),
        ("TOPPADDING",    (0,0),(-1,-1), 12),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),[6,6,6,6]),
    ]))
    return outer

# ── Page templates (header/footer) ────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # top stripe
    canvas.setFillColor(NAVY)
    canvas.rect(0, H-22, W, 22, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(20, H-14, "NExGen School of Computers")
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W-20, H-14, "AI Course Catalogue  2025")

    # bottom stripe
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 18, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(20, 6, "Srikakulam, Andhra Pradesh  ·  nexgencomputers.in")
    canvas.drawRightString(W-20, 6, f"Page {doc.page}")
    canvas.restoreState()

# ── Cover page ────────────────────────────────────────────────────────────────
def cover_page():
    elems = []

    # dark background block via a table
    cover_data = [[
        Paragraph("NExGen School of Computers", ParagraphStyle("clogo",
            fontName="Helvetica-Bold", fontSize=11, textColor=CYAN,
            alignment=TA_CENTER)),
    ],[
        spacer(20),
    ],[
        Paragraph("AI Course Catalogue", ParagraphStyle("ctag",
            fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#94A3B8"),
            alignment=TA_CENTER)),
    ],[
        Paragraph("2025 Edition", ParagraphStyle("cyear",
            fontName="Helvetica-Bold", fontSize=36, textColor=WHITE,
            alignment=TA_CENTER, leading=44)),
    ],[
        spacer(6),
    ],[
        Paragraph(
            "Three structured tracks — from first Python program to<br/>"
            "production-ready AI agents — designed for students in<br/>"
            "Srikakulam, Andhra Pradesh.",
            ParagraphStyle("cdesc", fontName="Helvetica", fontSize=12,
                textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER,
                leading=19)),
    ],[
        spacer(30),
    ],[
        # three badges
        Table([[
            Paragraph("Track 1<br/><b>Python &amp; AI Basics</b><br/>10th Class",
                S["cover_badge"]),
            Paragraph("Track 2<br/><b>ML &amp; AI Tools</b><br/>Intermediate / 12th",
                S["cover_badge"]),
            Paragraph("Track 3<br/><b>Engineering AI</b><br/>B.Tech / Engineering",
                S["cover_badge"]),
        ]], colWidths=[140,140,140],
        style=TableStyle([
            ("BACKGROUND",(0,0),(0,0), INDIGO),
            ("BACKGROUND",(1,0),(1,0), VIOLET),
            ("BACKGROUND",(2,0),(2,0), RED),
            ("ROUNDEDCORNERS",(0,0),(-1,-1),[6,6,6,6]),
            ("TOPPADDING",(0,0),(-1,-1),10),
            ("BOTTOMPADDING",(0,0),(-1,-1),10),
            ("LEFTPADDING",(0,0),(-1,-1),8),
            ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ])),
    ],[
        spacer(30),
    ],[
        hline(color=SLATE, thickness=0.5),
    ],[
        Table([[
            Paragraph("45 Days<br/><font size='8' color='#64748B'>per track</font>",
                ParagraphStyle("cs", fontName="Helvetica-Bold", fontSize=14,
                    textColor=CYAN, alignment=TA_CENTER)),
            Paragraph("3 Tracks<br/><font size='8' color='#64748B'>all levels</font>",
                ParagraphStyle("cs", fontName="Helvetica-Bold", fontSize=14,
                    textColor=CYAN, alignment=TA_CENTER)),
            Paragraph("30+ Projects<br/><font size='8' color='#64748B'>hands-on</font>",
                ParagraphStyle("cs", fontName="Helvetica-Bold", fontSize=14,
                    textColor=CYAN, alignment=TA_CENTER)),
            Paragraph("Certificate<br/><font size='8' color='#64748B'>on completion</font>",
                ParagraphStyle("cs", fontName="Helvetica-Bold", fontSize=14,
                    textColor=CYAN, alignment=TA_CENTER)),
        ]], colWidths=[110,110,110,110],
        style=TableStyle([
            ("TOPPADDING",(0,0),(-1,-1),8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ])),
    ]]

    cover_table = Table(cover_data, colWidths=[460])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), NAVY),
        ("TOPPADDING",(0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",(0,0),(-1,-1), 20),
        ("RIGHTPADDING",(0,0),(-1,-1), 20),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),[10,10,10,10]),
    ]))

    elems.append(spacer(30))
    elems.append(cover_table)
    elems.append(PageBreak())
    return elems

# ── Track 1 ───────────────────────────────────────────────────────────────────
def track1_page():
    elems = []
    elems.append(spacer(10))
    elems.append(track_banner(
        "Track 1 — Python & AI Basics",
        "From zero programming knowledge to building your first AI project",
        "10th Class students (any stream)",
        "45 Days · 2 hrs/day",
        INDIGO
    ))
    elems.append(spacer(10))
    elems.append(stats_bar({
        "Days": "45", "Modules": "4", "Mini Projects": "15+",
        "Capstone": "1", "Prerequisite": "None"
    }, INDIGO))
    elems.append(spacer(12))
    elems.append(Paragraph("What You Will Learn", S["section_heading"]))
    elems.append(hline(INDIGO, 1, 0, 8))

    modules = [
        {
            "name": "Module 1 — Python Fundamentals",
            "days": "Days 1–10",
            "topics": [
                "Day 1: Hello World — your first Python program in Google Colab",
                "Day 2: Variables & Data Types — int, float, str, bool",
                "Day 3: Input & Output — reading user input, printing results",
                "Day 4: Operators & Expressions — arithmetic, comparison, logic",
                "Day 5: If / Else conditions — making decisions in code",
                "Day 6: Loops (for) — repeating actions automatically",
                "Day 7: Loops (while) + break/continue",
                "Day 8: Functions — writing reusable blocks of code",
                "Day 9: Lists & Tuples — storing multiple values",
                "Day 10: Dictionaries — key-value storage (like a contact book)",
            ]
        },
        {
            "name": "Module 2 — Intermediate Python for AI",
            "days": "Days 11–20",
            "topics": [
                "Day 11: File handling — reading and writing text files",
                "Day 12: Error handling — try/except so programs don't crash",
                "Day 13: NumPy basics — fast number arrays for AI calculations",
                "Day 14: Pandas basics — working with data tables (like Excel in Python)",
                "Day 15: Pandas — filtering, sorting, grouping data",
                "Day 16: Data Visualisation with Matplotlib — bar charts, line graphs",
                "Day 17: Mini project — analyse a real dataset (cricket scores or prices)",
                "Day 18: String methods & Regular Expressions",
                "Day 19: Modules & pip — using Python's library ecosystem",
                "Day 20: Revision + Quiz",
            ]
        },
        {
            "name": "Module 3 — AI Introduction",
            "days": "Days 21–32",
            "topics": [
                "Day 21: What is AI? — history, types, real applications around you",
                "Day 22: Machine Learning in plain language — how computers learn from data",
                "Day 23: Your first ML model — Linear Regression to predict exam scores",
                "Day 24: Classification — spam detection with Logistic Regression",
                "Day 25: Decision Trees — ML that explains its own decisions",
                "Day 26: Model Evaluation — accuracy, confusion matrix, train/test split",
                "Day 27: Introduction to Neural Networks — visual intuition (TF Playground)",
                "Day 28: ChatGPT & Gemini — how to use AI tools effectively",
                "Day 29: Prompt Engineering basics — asking AI the right way",
                "Day 30: AI in everyday life — Swiggy, YouTube, IRCTC, PhonePe",
                "Day 31: Ethics of AI — bias, privacy, responsible use",
                "Day 32: Revision + Mock Test",
            ]
        },
        {
            "name": "Module 4 — Capstone Project",
            "days": "Days 33–45",
            "topics": [
                "Days 33–34: Project planning + environment setup",
                "Days 35–37: Build a Mark Sheet Analyser (reads CSV, calculates ranks)",
                "Days 38–40: Add ChatGPT study tip generator using OpenAI API",
                "Days 41–43: Build a simple Streamlit web UI for the app",
                "Day 44: Testing + bug fixing",
                "Day 45: Final demo — present your app to the class",
            ]
        },
    ]

    elems.append(module_table(modules, INDIGO))
    elems.append(spacer(10))
    elems.append(capstone_box(
        "Mark Sheet Analyser + AI Study Helper",
        "A web app that reads a student mark sheet, calculates class ranks, and uses "
        "ChatGPT to generate personalised study tips for weak subjects. Runs in the browser — "
        "you can show it to your parents on their phone.",
        [
            "Upload a CSV of marks and get ranked results instantly",
            "One-click AI study tips for any weak subject",
            "Simple Streamlit UI — no HTML or CSS needed",
            "Shareable link via Streamlit Cloud (free hosting)",
        ],
        "Python · pandas · scikit-learn · OpenAI API · Streamlit",
        INDIGO
    ))
    elems.append(PageBreak())
    return elems

# ── Track 2 ───────────────────────────────────────────────────────────────────
def track2_page():
    elems = []
    elems.append(spacer(10))
    elems.append(track_banner(
        "Track 2 — ML & AI Tools Mastery",
        "Machine Learning, Prompt Engineering, and AI tools for the real world",
        "Intermediate / 12th Completed students",
        "45 Days · 2 hrs/day",
        VIOLET
    ))
    elems.append(spacer(10))
    elems.append(stats_bar({
        "Days": "45", "Modules": "4", "Mini Projects": "26+",
        "Capstone": "1", "Prerequisite": "Basic Python (or Track 1)"
    }, VIOLET))
    elems.append(spacer(12))
    elems.append(Paragraph("What You Will Learn", S["section_heading"]))
    elems.append(hline(VIOLET, 1, 0, 8))

    modules = [
        {
            "name": "Module 1 — Python for Data Science",
            "days": "Days 1–10",
            "topics": [
                "Days 1–2: Python revision — fast-track for those with basics",
                "Day 3: NumPy — array operations at speed",
                "Day 4: Pandas — load, clean, and filter datasets",
                "Day 5: Pandas — groupby, merge, pivot tables",
                "Day 6: Matplotlib + Seaborn — charts that tell a story",
                "Day 7: Real dataset mini project — Flipkart product analysis",
                "Day 8: Data cleaning — handling missing values and outliers",
                "Day 9: Feature engineering — creating useful inputs for ML",
                "Day 10: Mini Project 5 — Vizag weather data EDA",
            ]
        },
        {
            "name": "Module 2 — Machine Learning",
            "days": "Days 11–24",
            "topics": [
                "Day 11: What is ML? — plain language + Real India examples (Swiggy ETA, Zomato ratings)",
                "Day 12: Linear Regression — predict salary from experience",
                "Day 13: Logistic Regression — predict loan approval (yes/no)",
                "Day 14: Decision Trees — credit card fraud detection",
                "Day 15: Random Forest — why many trees beat one tree",
                "Day 16: Model evaluation — accuracy, precision, recall, F1",
                "Day 17: Train/Test split + Cross Validation",
                "Day 18: Overfitting and how to fix it",
                "Day 19: Support Vector Machines (SVM) — image classification intro",
                "Day 20: K-Nearest Neighbours (KNN) — recommendation systems",
                "Day 21: Clustering with K-Means — customer segmentation",
                "Day 22: Pipeline with scikit-learn — clean professional code",
                "Day 23: Mini Project — Exam Score Predictor (Linear Regression)",
                "Day 24: Mini Project — Loan Approval Classifier (Random Forest)",
            ]
        },
        {
            "name": "Module 3 — Prompt Engineering & AI Tools",
            "days": "Days 25–33",
            "topics": [
                "Day 25: What is Prompt Engineering? — the 4-part formula (Role, Task, Context, Format)",
                "Day 26: Zero-shot, Few-shot, Chain-of-Thought techniques",
                "Day 27: Prompting for study & work — 5 patterns you will use every day",
                "Day 28: Gemini, Copilot & AI Tools landscape — which tool for which job",
                "Day 29: Build your personal Prompt Library (Google Docs / Notion)",
                "Day 30: ChatGPT API — make AI respond inside your Python code",
                "Day 31: Gemini API — Google's AI in your app",
                "Day 32: Advanced prompts — JSON mode, system prompts, temperature",
                "Day 33: Mini Project — AI-powered WhatsApp message reply generator",
            ]
        },
        {
            "name": "Module 4 — Capstone Project",
            "days": "Days 34–45",
            "topics": [
                "Day 34: Project setup — Smart Student Helper architecture + OpenAI connection",
                "Day 35: Build the AI study summary generator (OpenAI API)",
                "Day 36: Build the Exam Score Predictor (Linear Regression model)",
                "Day 37: Connect both components",
                "Day 38: Build Streamlit UI — input form + results display",
                "Day 39: Weekly study plan dashboard",
                "Day 40: Testing with real subjects (Physics, Chemistry, Maths)",
                "Day 41: Bug fixes + UI polish",
                "Day 42: Deploy on Streamlit Cloud (free, shareable link)",
                "Day 43: Prepare your project presentation",
                "Day 44: Demo day — present to class",
                "Day 45: Certificate + GitHub portfolio setup",
            ]
        },
    ]

    elems.append(module_table(modules, VIOLET))
    elems.append(spacer(10))
    elems.append(capstone_box(
        "Smart Student Helper",
        "A Streamlit web app with two superpowers: (1) generates a personalised AI study "
        "summary for any subject and topic using the ChatGPT API, and (2) predicts your "
        "likely exam score from your study hours using a Machine Learning model. Students "
        "leave with a live, deployed app they built themselves — shareable on WhatsApp.",
        [
            "AI study summary for any topic in any subject",
            "Exam score predictor trained on class data",
            "Weekly study plan dashboard",
            "Deployed live on Streamlit Cloud — share the link with friends",
        ],
        "Python · pandas · scikit-learn · OpenAI API · Streamlit · Streamlit Cloud",
        VIOLET
    ))
    elems.append(PageBreak())
    return elems

# ── Track 3 ───────────────────────────────────────────────────────────────────
def track3_page():
    elems = []
    elems.append(spacer(10))
    elems.append(track_banner(
        "Track 3 — Engineering AI",
        "Deep Learning, LLM APIs, Agentic AI, and production-ready AI systems",
        "B.Tech / Engineering students (any branch)",
        "45 Days · 2 hrs/day",
        RED
    ))
    elems.append(spacer(10))
    elems.append(stats_bar({
        "Days": "45", "Modules": "5", "Mini Projects": "30+",
        "Capstone": "1", "Prerequisite": "Python + basic ML (or Track 2)"
    }, RED))
    elems.append(spacer(12))
    elems.append(Paragraph("What You Will Learn", S["section_heading"]))
    elems.append(hline(RED, 1, 0, 8))

    modules = [
        {
            "name": "Module 1 — ML Review & Deep Learning Intuition",
            "days": "Days 1–5",
            "topics": [
                "Day 1: Visual neural networks — TensorFlow Playground (no code, pure intuition)",
                "Day 2: ML algorithms in plain language — which to use when + Real India examples",
                "Day 3: First complete ML pipeline — train/test, evaluation, sklearn",
                "Day 4: Deep learning vs classical ML — why deep learning wins on images/text",
                "Day 5: PyTorch setup — tensors, GPU vs CPU, Google Colab GPU runtime",
            ]
        },
        {
            "name": "Module 2 — Advanced ML & Deep Learning",
            "days": "Days 6–18",
            "topics": [
                "Day 6: Neural networks from scratch — one neuron, then a full network in NumPy",
                "Day 7: Activation functions — ReLU, Sigmoid, Softmax (what they do, not just math)",
                "Day 8: Backpropagation — how the network learns from its mistakes",
                "Day 9: PyTorch nn.Module — build a proper neural net in 20 lines",
                "Day 10: Convolutional Neural Networks (CNNs) — how computers see images",
                "Day 11: CNN mini project — MNIST digit classifier (99% accuracy)",
                "Day 12: Transfer Learning — use a pretrained model, train in minutes",
                "Day 13: Object detection basics — YOLO intuition",
                "Day 14: Recurrent Neural Networks (RNNs) — sequence data, time series",
                "Day 15: Natural Language Processing (NLP) — tokenisation, embeddings",
                "Day 16: Transformers — the architecture behind ChatGPT",
                "Day 17: Hugging Face — use state-of-the-art models in 5 lines of code",
                "Day 18: Mini Project — Sentiment analyser on Flipkart product reviews",
            ]
        },
        {
            "name": "Module 3 — LLM Engineering & APIs",
            "days": "Days 19–27",
            "topics": [
                "Day 19: What is an LLM? — tokens, context window, cost awareness (in rupees)",
                "Day 20: OpenAI API — chat completions, system prompts, parameters",
                "Day 21: Streaming responses — real-time output like ChatGPT",
                "Day 22: Function calling — make GPT trigger your Python functions",
                "Day 23: RAG (Retrieval-Augmented Generation) — open-book exam analogy",
                "Day 24: LangChain basics — simplest 5-line LCEL chain first",
                "Day 25: Claude API (Anthropic) — compare models, choose the right one",
                "Day 26: LLM cost management — smart routing, caching, rate limits",
                "Day 27: Mini Project — Document Q&A bot for your college notes",
            ]
        },
        {
            "name": "Module 4 — Prompt Engineering & Agentic AI",
            "days": "Days 28–37",
            "topics": [
                "Day 28: Advanced prompt patterns — JSON mode, system prompts, few-shot",
                "Day 29: Prompt security — injection attacks, jailbreaks, guardrails",
                "Day 30: What is an AI Agent? — the agent loop (Perceive → Think → Act)",
                "Day 31: Tool use — give your LLM the ability to call Python functions",
                "Day 32: Memory in agents — short-term (conversation) vs long-term (vector DB)",
                "Day 33: LangChain Agents — build a research agent with web search tool",
                "Day 34: Multi-agent systems with AutoGen — two agents collaborating",
                "Day 35: LangGraph — stateful agent workflows with branching logic",
                "Day 36: Guardrails & PII detection — responsible AI in production",
                "Day 37: Mini Project — AI research assistant that searches and summarises",
            ]
        },
        {
            "name": "Module 5 — Capstone Project",
            "days": "Days 38–45",
            "topics": [
                "Day 38: Architecture + Day 1 — JD skill extractor (OpenAI API)",
                "Day 39: Cover letter generator with prompt templates",
                "Day 40: Streamlit UI — upload resume, paste JD, get results",
                "Day 41: Add email delivery (Python smtplib)",
                "Day 42: Testing with 5 real job postings from Naukri / LinkedIn",
                "Day 43: Demo preparation + GitHub README",
                "Day 44: Final demo — present live to class",
                "Day 45: Certificate + LinkedIn portfolio guidance",
            ]
        },
    ]

    elems.append(module_table(modules, RED))
    elems.append(spacer(10))
    elems.append(capstone_box(
        "AI Job Application Agent",
        "An AI agent that takes a job description (paste from Naukri or LinkedIn), "
        "extracts required skills using GPT, compares them against the student's resume, "
        "and generates a tailored cover letter. Optionally emails it automatically. "
        "Every B.Tech student can use this the day they graduate — it is immediately useful.",
        [
            "Paste any JD → get required skills extracted in seconds",
            "Resume gap analysis — see what's missing vs what you have",
            "Tailored cover letter generated with one click",
            "Optional: auto-email the cover letter from your Gmail",
            "Deployed on Streamlit Cloud with a shareable link",
        ],
        "Python · OpenAI API · LangChain · Streamlit · smtplib · Streamlit Cloud",
        RED
    ))
    elems.append(PageBreak())
    return elems

# ── Comparison & enrolment page ───────────────────────────────────────────────
def comparison_page():
    elems = []
    elems.append(spacer(10))
    elems.append(Paragraph("Track Comparison at a Glance", S["section_heading"]))
    elems.append(hline(INDIGO, 1, 0, 10))

    comp_data = [
        [
            Paragraph("<b>Feature</b>", S["label"]),
            Paragraph("<b>Track 1</b><br/>Python &amp; AI Basics", S["label"]),
            Paragraph("<b>Track 2</b><br/>ML &amp; AI Tools", S["label"]),
            Paragraph("<b>Track 3</b><br/>Engineering AI", S["label"]),
        ],
        ["Who it is for",      "10th Class", "Intermediate / 12th", "B.Tech / Engineering"],
        ["Duration",           "45 Days",    "45 Days",             "45 Days"],
        ["Hours per day",      "2 hours",    "2 hours",             "2 hours"],
        ["Prerequisite",       "None",       "Basic Python",        "Python + ML basics"],
        ["Python",             "From zero",  "Revision + advanced", "Advanced"],
        ["Machine Learning",   "Intro only", "Core algorithms",     "Advanced + Deep Learning"],
        ["Deep Learning",      "—",          "—",                   "PyTorch + CNNs + Transformers"],
        ["AI Tools / ChatGPT", "Introduction","ChatGPT + Gemini APIs","OpenAI + Claude + Hugging Face"],
        ["Prompt Engineering", "Basics",     "Full module",         "Advanced + security"],
        ["Agentic AI",         "—",          "—",                   "LangChain + AutoGen + LangGraph"],
        ["Mini Projects",      "15+",        "26+",                 "30+"],
        ["Capstone Project",   "Mark Sheet Analyser", "Smart Student Helper", "AI Job Application Agent"],
        ["Certificate",        "Yes",        "Yes",                 "Yes"],
        ["Suitable for jobs",  "Entry-level support", "Junior AI roles", "AI/ML Engineer roles"],
    ]

    col_w = [130, 100, 100, 100]
    comp_table = Table(comp_data, colWidths=col_w)
    comp_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),  (-1,0),   NAVY),
        ("TEXTCOLOR",     (0,0),  (-1,0),   WHITE),
        ("FONTNAME",      (0,0),  (-1,0),   "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),  (-1,-1),  9),
        ("ALIGN",         (1,0),  (-1,-1),  "CENTER"),
        ("VALIGN",        (0,0),  (-1,-1),  "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1),  [WHITE, LIGHT]),
        ("GRID",          (0,0),  (-1,-1),  0.4, colors.HexColor("#E2E8F0")),
        ("TOPPADDING",    (0,0),  (-1,-1),  6),
        ("BOTTOMPADDING", (0,0),  (-1,-1),  6),
        ("LEFTPADDING",   (0,0),  (-1,-1),  8),
        ("RIGHTPADDING",  (0,0),  (-1,-1),  8),
        # colour the track name cells
        ("BACKGROUND",    (1,0),  (1,0),    INDIGO),
        ("BACKGROUND",    (2,0),  (2,0),    VIOLET),
        ("BACKGROUND",    (3,0),  (3,0),    RED),
    ]))
    elems.append(comp_table)
    elems.append(spacer(24))

    # Why NexGen
    elems.append(Paragraph("Why NexGen School of Computers?", S["section_heading"]))
    elems.append(hline(CYAN, 1, 0, 10))

    why_data = [
        [
            check_item("<b>Only AI course in Srikakulam</b> — no travel, no hostel cost"),
            check_item("<b>Small batches (8–12 students)</b> — personal attention, not a lecture hall"),
        ],
        [
            check_item("<b>Portfolio certificate</b> — you graduate with a real project on GitHub"),
            check_item("<b>Track-based entry</b> — join at your level, not everyone's level"),
        ],
        [
            check_item("<b>Indian examples throughout</b> — Swiggy, IRCTC, Naukri, cricket"),
            check_item("<b>Google Colab only</b> — no expensive laptop or setup required"),
        ],
        [
            check_item("<b>Industry-relevant stack</b> — same tools used at Google, Meta, Swiggy"),
            check_item("<b>Placement guidance</b> — resume, LinkedIn, GitHub, and interview prep"),
        ],
    ]
    why_table = Table(why_data, colWidths=[230, 230])
    why_table.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    elems.append(why_table)
    elems.append(spacer(24))

    # Enrolment
    elems.append(Paragraph("Enrolment & Contact", S["section_heading"]))
    elems.append(hline(GREEN, 1, 0, 10))

    enrol_data = [[
        Table([
            [Paragraph("How to Enrol", ParagraphStyle("eh",
                fontName="Helvetica-Bold", fontSize=11, textColor=NAVY))],
            [check_item("Step 1: WhatsApp us your name, class, and preferred track")],
            [check_item("Step 2: Attend a free demo class (30 minutes)")],
            [check_item("Step 3: Complete enrolment form + fee payment")],
            [check_item("Step 4: Receive your login to the NexGen portal")],
            [check_item("Step 5: Start learning on Day 1")],
        ], colWidths=[200]),

        Table([
            [Paragraph("Contact Us", ParagraphStyle("ch",
                fontName="Helvetica-Bold", fontSize=11, textColor=NAVY))],
            [Paragraph("&#128205; NExGen School of Computers<br/>"
                       "Srikakulam, Andhra Pradesh", S["body"])],
            [Paragraph("&#128241; WhatsApp: <b>+91 XXXXX XXXXX</b>", S["body"])],
            [Paragraph("&#127760; nexgencomputers.in", S["body"])],
            [Paragraph("&#128197; Next batch starts: <b>rolling enrolment</b>", S["body"])],
        ], colWidths=[200]),
    ]]

    enrol_table = Table(enrol_data, colWidths=[240, 220])
    enrol_table.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
    ]))
    elems.append(enrol_table)

    return elems

# ── Build PDF ─────────────────────────────────────────────────────────────────
def build():
    out = "/Applications/Projects/nexgen-ai-courses/docs/NexGen-AI-Course-Details.pdf"

    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=30*mm, rightMargin=30*mm,
        topMargin=28*mm, bottomMargin=20*mm,
        title="NexGen AI Course Catalogue 2025",
        author="NExGen School of Computers",
        subject="AI Course Details — All Three Tracks",
    )

    story = []
    story += cover_page()
    story += track1_page()
    story += track2_page()
    story += track3_page()
    story += comparison_page()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved: {out}")

if __name__ == "__main__":
    build()
