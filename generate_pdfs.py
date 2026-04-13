"""
NexGen School of Computers — Course PDF Generator
Generates 3 professional course documents using ReportLab Platypus.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.colors import HexColor

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
BG_DARK      = HexColor("#0F172A")
TEXT_DARK    = HexColor("#1E293B")
LIGHT_BG     = HexColor("#F8FAFC")
WHITE        = colors.white
GREY_RULE    = HexColor("#CBD5E1")
GREY_LIGHT   = HexColor("#E2E8F0")
GREY_MID     = HexColor("#94A3B8")

ACCENT = {
    1: HexColor("#4F46E5"),   # indigo
    2: HexColor("#7C3AED"),   # purple
    3: HexColor("#DC2626"),   # red
}

# ---------------------------------------------------------------------------
# Track metadata
# ---------------------------------------------------------------------------
TRACKS = [
    {
        "number": 1,
        "name": "Python & AI Basics",
        "audience": "10th Grade Students (Age 15–16)",
        "prerequisites": [
            "Basic computer literacy (file management, web browsing)",
            "No prior programming experience required",
            "Curiosity and willingness to experiment",
        ],
        "capstone": "A supervised machine-learning classifier trained on a real Kaggle dataset, complete with data-cleaning pipeline, model comparison, CLI interface, saved model artifact, and README documentation.",
        "output_file": "Track1-Python-AI-Basics.pdf",
        "modules": [
            {
                "number": 1,
                "title": "Python Fundamentals",
                "days_range": "Days 1–10",
                "days": [
                    {
                        "day": 1, "title": "Welcome to Python",
                        "objectives": [
                            "Set up Google Colab and run your first Python cell",
                            "Understand what a program is and how Python executes code",
                            "Use the print() function to display output",
                        ],
                        "key_terms": "interpreter, cell, output, syntax, print()",
                        "exercise": "Write a Colab notebook that prints your name, your school, and today's date using three separate print() calls.",
                    },
                    {
                        "day": 2, "title": "Variables and Data Types",
                        "objectives": [
                            "Declare variables and assign values of different types",
                            "Distinguish between int, float, str, and bool",
                            "Use type() to inspect a variable's data type",
                        ],
                        "key_terms": "variable, int, float, str, bool, type(), assignment",
                        "exercise": "Create variables for your age (int), height in metres (float), first name (str), and whether you like coding (bool). Print each with a label.",
                    },
                    {
                        "day": 3, "title": "Taking Input and Doing Math",
                        "objectives": [
                            "Read user input at runtime using input()",
                            "Perform arithmetic operations: +, -, *, /, //, %, **",
                            "Convert string input to numeric types for calculation",
                        ],
                        "key_terms": "input(), int(), float(), arithmetic, modulo, floor division",
                        "exercise": "Build a simple tip calculator: ask for the bill amount and tip percentage, then print the tip value and total bill.",
                    },
                    {
                        "day": 4, "title": "If-Else Decisions",
                        "objectives": [
                            "Write if, elif, and else branches to control program flow",
                            "Use comparison and logical operators correctly",
                            "Build a grade calculator that maps marks to letter grades",
                        ],
                        "key_terms": "if, elif, else, comparison operators, logical operators, boolean expression",
                        "exercise": "Grade calculator: prompt for a numeric score (0–100) and print the corresponding grade (A, B, C, D, F) with a motivational message.",
                    },
                    {
                        "day": 5, "title": "Loops",
                        "objectives": [
                            "Iterate over a range using a for loop",
                            "Repeat code while a condition holds with while",
                            "Control loop execution with break and continue",
                        ],
                        "key_terms": "for, while, range(), break, continue, iteration",
                        "exercise": "Print the multiplication table for a user-supplied number, then use a while loop to keep asking until the user types 'quit'.",
                    },
                    {
                        "day": 6, "title": "Lists",
                        "objectives": [
                            "Create and access list elements by index",
                            "Modify lists with append(), remove(), and sort()",
                            "Slice lists to extract sub-sequences",
                        ],
                        "key_terms": "list, index, slice, append(), remove(), sort(), len()",
                        "exercise": "Maintain a shopping list: allow the user to add items, remove items, and display the sorted list — all in a loop.",
                    },
                    {
                        "day": 7, "title": "Dictionaries",
                        "objectives": [
                            "Understand key-value storage and when to use dicts over lists",
                            "Create, read, update, and delete dictionary entries",
                            "Iterate over keys and values with .items()",
                        ],
                        "key_terms": "dictionary, key, value, .items(), .get(), .keys(), .values()",
                        "exercise": "Build a contacts book: store names as keys and phone numbers as values; support add, lookup, and delete operations.",
                    },
                    {
                        "day": 8, "title": "Functions",
                        "objectives": [
                            "Define reusable functions with def and call them",
                            "Pass arguments and return values",
                            "Understand scope: local vs. global variables",
                        ],
                        "key_terms": "def, parameters, arguments, return, scope, local, global",
                        "exercise": "Write a function is_prime(n) that returns True if n is prime. Use it to print all prime numbers between 1 and 100.",
                    },
                    {
                        "day": 9, "title": "String Operations",
                        "objectives": [
                            "Format strings cleanly using f-strings",
                            "Apply common string methods: .upper(), .strip(), .split(), .replace()",
                            "Index and slice strings like sequences",
                        ],
                        "key_terms": "f-string, .upper(), .lower(), .strip(), .split(), .replace(), string slice",
                        "exercise": "Write a 'word analyser': take a sentence as input, count words, find the longest word, and print it title-cased.",
                    },
                    {
                        "day": 10, "title": "Files and Error Handling",
                        "objectives": [
                            "Open, read, and write text files with open() and with blocks",
                            "Catch runtime errors gracefully using try-except",
                            "Distinguish between common exceptions: FileNotFoundError, ValueError",
                        ],
                        "key_terms": "open(), with, read(), write(), try, except, FileNotFoundError, ValueError",
                        "exercise": "Write a student grade logger: read names and scores from a CSV file, catch missing-file errors, and write a summary report file.",
                    },
                ],
            },
            {
                "number": 2,
                "title": "Intermediate Python for AI",
                "days_range": "Days 11–20",
                "days": [
                    {
                        "day": 11, "title": "NumPy — Arrays and Vectorisation",
                        "objectives": [
                            "Create NumPy arrays and understand their advantages over lists",
                            "Perform element-wise and matrix operations without loops",
                            "Use slicing and boolean masking to filter data",
                        ],
                        "key_terms": "numpy, ndarray, vectorisation, broadcasting, axis, dtype",
                        "exercise": "Generate a 5×5 matrix of random integers; compute row means, column sums, and replace all values above 50 with zero.",
                    },
                    {
                        "day": 12, "title": "Pandas — DataFrames and CSV",
                        "objectives": [
                            "Load a CSV file into a Pandas DataFrame",
                            "Select columns, filter rows, and inspect data with head() and info()",
                            "Compute summary statistics with describe()",
                        ],
                        "key_terms": "DataFrame, Series, read_csv(), iloc, loc, describe(), head()",
                        "exercise": "Load a student marks CSV; display the top 5 scorers, the average per subject, and the number of students who passed every subject.",
                    },
                    {
                        "day": 13, "title": "Matplotlib — Charts and Plots",
                        "objectives": [
                            "Create line, bar, and scatter plots using matplotlib.pyplot",
                            "Label axes, add titles, and save figures to PNG",
                            "Choose the right chart type for the data being shown",
                        ],
                        "key_terms": "matplotlib, pyplot, plt.show(), plt.savefig(), xlabel, ylabel, legend",
                        "exercise": "Plot monthly sales data as a bar chart and overlay a line for the 3-month rolling average. Save the figure.",
                    },
                    {
                        "day": 14, "title": "List Comprehensions and Lambda",
                        "objectives": [
                            "Write concise list comprehensions instead of explicit loops",
                            "Apply filtering conditions inside comprehensions",
                            "Create short anonymous functions with lambda",
                        ],
                        "key_terms": "list comprehension, lambda, map(), filter(), sorted(), key function",
                        "exercise": "Use a comprehension to extract all even squares from 1–100, then sort a list of dictionaries by a nested value using a lambda key.",
                    },
                    {
                        "day": 15, "title": "Object-Oriented Programming",
                        "objectives": [
                            "Define classes with __init__ and instance methods",
                            "Create objects and access their attributes",
                            "Understand inheritance and method overriding with a simple example",
                        ],
                        "key_terms": "class, object, __init__, self, instance, inheritance, method",
                        "exercise": "Model a BankAccount class with deposit(), withdraw(), and get_balance() methods. Create two accounts and transfer funds between them.",
                    },
                    {
                        "day": 16, "title": "Working with APIs",
                        "objectives": [
                            "Make HTTP GET requests with the requests library",
                            "Parse JSON responses into Python dictionaries",
                            "Handle errors: status codes, timeouts, missing keys",
                        ],
                        "key_terms": "requests, JSON, GET, status code, .json(), response, API endpoint",
                        "exercise": "Fetch current weather data for your city from a free API; display temperature, humidity, and a short description in a formatted print.",
                    },
                    {
                        "day": 17, "title": "Regular Expressions",
                        "objectives": [
                            "Match, search, and extract patterns from strings using re",
                            "Use character classes, quantifiers, and groups",
                            "Apply regex for data validation (email, phone number)",
                        ],
                        "key_terms": "re, pattern, match(), search(), findall(), group(), character class",
                        "exercise": "Write a validator that reads a file of contact records and flags entries with invalid email addresses or malformed phone numbers.",
                    },
                    {
                        "day": 18, "title": "Data Cleaning with Pandas",
                        "objectives": [
                            "Identify and handle missing values with fillna() and dropna()",
                            "Detect and remove duplicate rows",
                            "Standardise column types and fix inconsistent categories",
                        ],
                        "key_terms": "isnull(), fillna(), dropna(), duplicated(), astype(), value_counts()",
                        "exercise": "Take a deliberately messy dataset (provided), apply a cleaning pipeline, and compare before/after statistics using describe().",
                    },
                    {
                        "day": 19, "title": "Modules, Packages, and pip",
                        "objectives": [
                            "Import from the Python standard library and third-party packages",
                            "Install packages with pip and manage requirements",
                            "Create your own reusable module and import it",
                        ],
                        "key_terms": "import, from, pip, requirements.txt, module, package, __name__",
                        "exercise": "Build a utility module utils.py with helper functions used across two other scripts; install an external package and add it to requirements.txt.",
                    },
                    {
                        "day": 20, "title": "Mini Project — Student Data Analyser",
                        "objectives": [
                            "Apply Modules 1–2 skills to a complete end-to-end mini project",
                            "Load, clean, analyse, and visualise a real student dataset",
                            "Present findings in a readable printed report",
                        ],
                        "key_terms": "EDA, pipeline, report, visualisation, summary statistics",
                        "exercise": "Deliver a Colab notebook that loads a dataset, cleans it, computes statistics per subject and per student, plots top performers, and writes a summary to a text file.",
                    },
                ],
            },
            {
                "number": 3,
                "title": "AI Introduction",
                "days_range": "Days 21–32",
                "days": [
                    {
                        "day": 21, "title": "What is Artificial Intelligence?",
                        "objectives": [
                            "Explain the AI → ML → Deep Learning hierarchy",
                            "Name three real-world AI applications and their underlying technique",
                            "Distinguish supervised, unsupervised, and reinforcement learning",
                        ],
                        "key_terms": "AI, ML, Deep Learning, supervised, unsupervised, reinforcement learning, model",
                        "exercise": "Research one AI application (e.g., spam filter, recommendation engine) and write a half-page explanation of what data it uses and how it learns.",
                    },
                    {
                        "day": 22, "title": "Your First ML Model",
                        "objectives": [
                            "Load the Iris dataset using scikit-learn",
                            "Split data into training and test sets with train_test_split",
                            "Train a KNeighborsClassifier and evaluate its accuracy",
                        ],
                        "key_terms": "scikit-learn, fit(), predict(), train_test_split, accuracy_score, Iris dataset",
                        "exercise": "Train a KNN classifier on Iris with k=3 and k=7. Report accuracy for both and explain in a comment which you prefer and why.",
                    },
                    {
                        "day": 23, "title": "How Machine Learning Learns",
                        "objectives": [
                            "Explain the concept of a loss function and why we minimise it",
                            "Describe gradient descent in plain language",
                            "Relate the training loop to adjusting parameters iteratively",
                        ],
                        "key_terms": "loss function, gradient descent, learning rate, epoch, parameter, optimisation",
                        "exercise": "Plot a simple quadratic loss curve and animate how gradient descent steps move toward the minimum (use matplotlib).",
                    },
                    {
                        "day": 24, "title": "Linear and Logistic Regression",
                        "objectives": [
                            "Fit a Linear Regression model to predict a continuous target",
                            "Use Logistic Regression for binary classification",
                            "Interpret the model coefficients and decision boundary",
                        ],
                        "key_terms": "LinearRegression, LogisticRegression, coefficient, intercept, sigmoid, decision boundary",
                        "exercise": "Predict house prices with Linear Regression on a small dataset; then classify pass/fail using Logistic Regression on student scores.",
                    },
                    {
                        "day": 25, "title": "Decision Trees and Random Forests",
                        "objectives": [
                            "Understand how a Decision Tree splits data using information gain",
                            "Train a Random Forest and explain why ensembles outperform single trees",
                            "Visualise feature importance scores",
                        ],
                        "key_terms": "DecisionTree, RandomForest, entropy, information gain, feature importance, ensemble",
                        "exercise": "Train both a single Decision Tree and a Random Forest on the Titanic dataset. Compare accuracy and plot feature importances as a bar chart.",
                    },
                    {
                        "day": 26, "title": "Evaluating ML Models",
                        "objectives": [
                            "Compute and interpret precision, recall, and F1-score",
                            "Build and read a confusion matrix",
                            "Explain why accuracy alone can be misleading on imbalanced data",
                        ],
                        "key_terms": "precision, recall, F1-score, confusion matrix, true positive, false positive, imbalanced",
                        "exercise": "Evaluate the Day 25 Random Forest with a full classification report and confusion matrix heatmap; write a two-sentence interpretation.",
                    },
                    {
                        "day": 27, "title": "Natural Language Processing Basics",
                        "objectives": [
                            "Tokenise text and remove stopwords",
                            "Represent text as numbers using CountVectorizer",
                            "Build a simple sentiment classifier on a movie review dataset",
                        ],
                        "key_terms": "NLP, tokenisation, stopwords, CountVectorizer, sentiment, corpus, vocabulary",
                        "exercise": "Train a Naive Bayes sentiment classifier on IMDB mini-dataset; test it on three sentences you write yourself.",
                    },
                    {
                        "day": 28, "title": "Image Recognition with ML",
                        "objectives": [
                            "Load and visualise the MNIST handwritten digits dataset",
                            "Flatten images and train a classifier on pixel features",
                            "Measure accuracy and display misclassified examples",
                        ],
                        "key_terms": "MNIST, pixel, flatten, reshape, image array, classification, confusion matrix",
                        "exercise": "Train an SVM on MNIST (subset of 5 000 samples); display a 4×4 grid of test images with their predicted vs. actual labels.",
                    },
                    {
                        "day": 29, "title": "Introduction to Neural Networks",
                        "objectives": [
                            "Describe layers, neurons, weights, and activation functions",
                            "Train a Multi-Layer Perceptron using scikit-learn's MLPClassifier",
                            "Compare MLP performance to the models from earlier days",
                        ],
                        "key_terms": "neural network, layer, neuron, activation, ReLU, MLPClassifier, hidden layer",
                        "exercise": "Train an MLP on MNIST with two hidden layers of 128 neurons each. Compare accuracy with the Day 28 SVM.",
                    },
                    {
                        "day": 30, "title": "Using ChatGPT and Gemini APIs",
                        "objectives": [
                            "Call the OpenAI Chat Completions API from Python",
                            "Call the Google Gemini GenerateContent API from Python",
                            "Compare responses for the same prompt from both models",
                        ],
                        "key_terms": "API key, OpenAI, Gemini, prompt, completion, tokens, chat message",
                        "exercise": "Send the same three-question quiz to both ChatGPT (gpt-4o-mini) and Gemini (gemini-1.5-flash); print results side by side.",
                    },
                    {
                        "day": 31, "title": "Responsible AI and Ethics",
                        "objectives": [
                            "Identify sources of bias in training data and model outputs",
                            "Explain fairness, accountability, and transparency in AI systems",
                            "Describe one real-world harm caused by a biased AI system",
                        ],
                        "key_terms": "bias, fairness, accountability, transparency, explainability, harmful output",
                        "exercise": "Find a published case study of an AI bias incident; write a one-page analysis covering what went wrong, who was affected, and how it could be fixed.",
                    },
                    {
                        "day": 32, "title": "Module 3 Review — AI Fundamentals Quiz",
                        "objectives": [
                            "Consolidate knowledge from Days 21–31",
                            "Identify gaps and revisit any weak areas with targeted practice",
                            "Complete a graded quiz covering ML concepts, APIs, and ethics",
                        ],
                        "key_terms": "review, quiz, supervised learning, evaluation metrics, NLP, neural network, ethics",
                        "exercise": "20-question graded quiz (MCQ + short answer) covering all Module 3 topics, followed by a peer discussion of the ethics case studies.",
                    },
                ],
            },
            {
                "number": 4,
                "title": "Capstone Project",
                "days_range": "Days 33–45",
                "days": [
                    {
                        "day": 33, "title": "Capstone Planning",
                        "objectives": [
                            "Choose a meaningful problem domain for your ML capstone",
                            "Draft a one-page project design document with goals and success criteria",
                            "Identify 2–3 candidate datasets on Kaggle or UCI",
                        ],
                        "key_terms": "project brief, problem statement, success criteria, scope, dataset",
                        "exercise": "Submit a project plan: title, problem statement, target variable, dataset source, and proposed models to compare.",
                    },
                    {
                        "day": 34, "title": "Data Collection and Initial EDA",
                        "objectives": [
                            "Download and load the chosen dataset into a Colab notebook",
                            "Inspect shape, dtypes, missing values, and class distribution",
                            "Produce an initial set of descriptive statistics",
                        ],
                        "key_terms": "EDA, shape, dtypes, isnull(), value_counts(), describe(), class imbalance",
                        "exercise": "Complete EDA checklist: shape, null counts, duplicates, class distribution bar chart, and three observations noted as comments.",
                    },
                    {
                        "day": 35, "title": "Data Cleaning and Deep EDA",
                        "objectives": [
                            "Execute a full cleaning pipeline: nulls, duplicates, outliers, types",
                            "Create correlation heatmaps and pairplots",
                            "Identify the three most predictive features based on visualisations",
                        ],
                        "key_terms": "correlation, heatmap, pairplot, outlier, IQR, cleaning pipeline",
                        "exercise": "Produce a cleaned DataFrame and save it to CSV; document every cleaning decision with inline comments.",
                    },
                    {
                        "day": 36, "title": "Feature Engineering",
                        "objectives": [
                            "Encode categorical variables with LabelEncoder and OneHotEncoder",
                            "Scale numerical features with StandardScaler or MinMaxScaler",
                            "Create at least one derived feature that improves predictive power",
                        ],
                        "key_terms": "feature engineering, encoding, scaling, LabelEncoder, OneHotEncoder, StandardScaler",
                        "exercise": "Apply the full feature-engineering pipeline to the cleaned dataset; verify shapes and data types before and after.",
                    },
                    {
                        "day": 37, "title": "Model Training — Compare Three Models",
                        "objectives": [
                            "Train Logistic Regression, Random Forest, and a third model of choice",
                            "Evaluate all three on the test set using accuracy, F1, and confusion matrix",
                            "Select the best model and justify the choice in writing",
                        ],
                        "key_terms": "model comparison, baseline, evaluation, cross-validation, test set, leakage",
                        "exercise": "Create a comparison table (model vs. metric) and write a short justification paragraph for your chosen model.",
                    },
                    {
                        "day": 38, "title": "Improving the Model",
                        "objectives": [
                            "Tune hyperparameters with GridSearchCV",
                            "Address class imbalance using SMOTE or class_weight",
                            "Measure improvement before and after tuning",
                        ],
                        "key_terms": "GridSearchCV, hyperparameter, SMOTE, class_weight, overfitting, cross-validation",
                        "exercise": "Run GridSearchCV on your chosen model with at least 3 hyperparameters; report best params and improvement in F1-score.",
                    },
                    {
                        "day": 39, "title": "Building the User Interface — CLI",
                        "objectives": [
                            "Wrap the trained model in a command-line interface using argparse",
                            "Accept input features as CLI arguments and print a prediction",
                            "Validate input and show a helpful error message for bad data",
                        ],
                        "key_terms": "argparse, CLI, interface, prediction, input validation",
                        "exercise": "Build predict.py that loads your saved model, accepts feature values as flags, and prints the prediction with a confidence percentage.",
                    },
                    {
                        "day": 40, "title": "Testing Your Project",
                        "objectives": [
                            "Write at least five unit tests for utility functions using pytest",
                            "Test edge cases: empty input, out-of-range values, wrong types",
                            "Run the full test suite and achieve 0 failures",
                        ],
                        "key_terms": "pytest, unit test, edge case, assert, test suite, fixture",
                        "exercise": "Write a test_utils.py file with tests for all helper functions; run pytest and screenshot the passing output.",
                    },
                    {
                        "day": 41, "title": "Writing Documentation",
                        "objectives": [
                            "Write a professional README with setup, usage, and examples",
                            "Document every function with a docstring",
                            "Create an architecture diagram showing data flow",
                        ],
                        "key_terms": "README, docstring, documentation, architecture diagram, setup instructions",
                        "exercise": "Peer-review a classmate's README and give three specific improvement suggestions; incorporate their feedback on yours.",
                    },
                    {
                        "day": 42, "title": "Saving and Loading Your Model",
                        "objectives": [
                            "Serialize a trained model to disk using joblib",
                            "Load the model in a new script and make predictions",
                            "Version model artifacts with a naming convention",
                        ],
                        "key_terms": "joblib, pickle, serialization, model artifact, versioning",
                        "exercise": "Save your final tuned model as model_v1.pkl; write a standalone load_and_predict.py that loads it and predicts on three new samples.",
                    },
                    {
                        "day": 43, "title": "Polish and Improvements",
                        "objectives": [
                            "Improve CLI output formatting and user experience",
                            "Refactor repeated code into functions and modules",
                            "Ensure the project runs end-to-end without manual intervention",
                        ],
                        "key_terms": "refactoring, UX, automation, DRY principle, end-to-end",
                        "exercise": "Run the project from scratch on a clean Colab session; fix any errors that appear and commit the cleaned version.",
                    },
                    {
                        "day": 44, "title": "Rehearsal and Peer Review",
                        "objectives": [
                            "Deliver a 5-minute dry-run presentation of the capstone",
                            "Give structured feedback to two peers using the provided rubric",
                            "Incorporate feedback to improve the final presentation",
                        ],
                        "key_terms": "presentation, rubric, peer review, demo, feedback",
                        "exercise": "Time yourself presenting for exactly 5 minutes. Note the three biggest feedback points and create a task list to address them before Demo Day.",
                    },
                    {
                        "day": 45, "title": "Demo Day",
                        "objectives": [
                            "Present the completed capstone project to the full class and guests",
                            "Walk through the problem, data, model, results, and key learnings",
                            "Answer questions confidently from the audience",
                        ],
                        "key_terms": "demo, presentation, capstone, results, Q&A",
                        "exercise": "Final presentation — 5 minutes + 2-minute Q&A. Submit the completed notebook, code, model artifact, README, and a one-paragraph reflection.",
                    },
                ],
            },
        ],
    },
    # -----------------------------------------------------------------------
    # TRACK 2
    # -----------------------------------------------------------------------
    {
        "number": 2,
        "name": "Python for Data Science & ML",
        "audience": "Inter / 12th Grade Students (Age 17–18)",
        "prerequisites": [
            "Comfortable with Python basics (variables, loops, functions)",
            "Basic knowledge of school-level statistics and algebra",
            "Laptop with Python 3.10+ and Jupyter Notebook installed",
        ],
        "capstone": "An end-to-end ML product: full EDA on a real dataset, trained and deployed prediction API (Flask/FastAPI), AI-powered insight narrative from an LLM, and an interactive Streamlit dashboard.",
        "output_file": "Track2-Data-Science-ML.pdf",
        "modules": [
            {
                "number": 1,
                "title": "Python for Data Science",
                "days_range": "Days 1–12",
                "days": [
                    {
                        "day": 1, "title": "Python Environment Setup",
                        "objectives": [
                            "Create and activate a Python virtual environment",
                            "Set up Jupyter Notebook and understand the kernel model",
                            "Install the core data science stack: numpy, pandas, matplotlib, scikit-learn",
                        ],
                        "key_terms": "venv, Jupyter, kernel, pip, requirements.txt, Conda, environment isolation",
                        "exercise": "Set up a new venv, install the data science stack, launch Jupyter, and produce a notebook that prints all library versions.",
                    },
                    {
                        "day": 2, "title": "NumPy Deep Dive",
                        "objectives": [
                            "Explain broadcasting rules and when they apply",
                            "Use advanced indexing: boolean masks and fancy indexing",
                            "Perform linear algebra operations: dot product, matrix inverse",
                        ],
                        "key_terms": "broadcasting, fancy indexing, boolean mask, dot product, np.linalg, stacking",
                        "exercise": "Solve a system of linear equations using np.linalg.solve; verify by substituting back. Benchmark a loop vs. vectorised approach on 1M elements.",
                    },
                    {
                        "day": 3, "title": "Pandas Advanced — Merge, Pivot, GroupBy",
                        "objectives": [
                            "Merge two DataFrames with different join types: inner, left, right, outer",
                            "Reshape data using pivot_table and melt",
                            "Aggregate grouped data with groupby and multiple aggregation functions",
                        ],
                        "key_terms": "merge, join, pivot_table, melt, groupby, agg, multi-index",
                        "exercise": "Given two sales CSVs (transactions and products), merge them, pivot by month and category, and compute top-5 revenue products per region.",
                    },
                    {
                        "day": 4, "title": "Data Visualisation with Seaborn",
                        "objectives": [
                            "Create distribution plots: histplot, kdeplot, boxplot",
                            "Visualise relationships: scatterplot, pairplot, heatmap",
                            "Customise themes, colour palettes, and figure layout",
                        ],
                        "key_terms": "seaborn, heatmap, boxplot, kdeplot, pairplot, FacetGrid, palette",
                        "exercise": "Produce a 6-panel figure exploring a provided dataset: distributions, outliers, correlations, and a grouped comparison. Export as PNG.",
                    },
                    {
                        "day": 5, "title": "Statistical Foundations",
                        "objectives": [
                            "Compute mean, median, mode, variance, and standard deviation",
                            "Explain normal, skewed, and bimodal distributions",
                            "Interpret z-scores and percentiles in context",
                        ],
                        "key_terms": "mean, median, mode, variance, std, normal distribution, z-score, skewness, kurtosis",
                        "exercise": "Analyse a real salary dataset: compute summary stats, identify the distribution shape, find outliers using z-scores, and plot.",
                    },
                    {
                        "day": 6, "title": "Probability and Bayes Theorem",
                        "objectives": [
                            "Define probability, conditional probability, and independence",
                            "Apply Bayes Theorem to update beliefs with new evidence",
                            "Simulate probability experiments with numpy.random",
                        ],
                        "key_terms": "probability, conditional probability, Bayes Theorem, prior, posterior, likelihood, simulation",
                        "exercise": "Simulate 10 000 coin flips and coin-loaded experiments; compute empirical probabilities and compare to theoretical. Solve a medical test Bayes problem.",
                    },
                    {
                        "day": 7, "title": "Hypothesis Testing",
                        "objectives": [
                            "Formulate null and alternative hypotheses",
                            "Run a t-test and interpret the p-value correctly",
                            "Apply a chi-squared test for categorical independence",
                        ],
                        "key_terms": "null hypothesis, p-value, significance level, t-test, chi-squared, Type I error, Type II error",
                        "exercise": "Compare average scores of two class groups using an independent t-test; then test if exam pass-rate is independent of gender with chi-squared.",
                    },
                    {
                        "day": 8, "title": "Data Cleaning Pipeline",
                        "objectives": [
                            "Build a systematic pipeline to handle nulls, duplicates, and outliers",
                            "Choose between imputation strategies: mean, median, mode, KNN",
                            "Document every transformation decision in code comments",
                        ],
                        "key_terms": "imputation, KNNImputer, IQR, outlier, pipeline, fillna, dropna, duplicated",
                        "exercise": "Given a messy retail dataset with 30% nulls and known outliers, apply and document a complete cleaning pipeline. Compare pre/post statistics.",
                    },
                    {
                        "day": 9, "title": "Feature Engineering",
                        "objectives": [
                            "Encode ordinal and nominal variables appropriately",
                            "Apply StandardScaler and MinMaxScaler; know when to use each",
                            "Create polynomial features and interaction terms",
                        ],
                        "key_terms": "OrdinalEncoder, OneHotEncoder, StandardScaler, MinMaxScaler, PolynomialFeatures, interaction term",
                        "exercise": "Engineer features on the cleaned Day 8 dataset: encode categoricals, scale numerics, add an interaction term, and verify no data leakage.",
                    },
                    {
                        "day": 10, "title": "Exploratory Data Analysis — Full Workflow",
                        "objectives": [
                            "Execute a structured EDA: understand, clean, visualise, summarise",
                            "Generate hypotheses from visual and statistical patterns",
                            "Produce a concise EDA report notebook with executive summary",
                        ],
                        "key_terms": "EDA workflow, hypothesis, narrative, insight, executive summary",
                        "exercise": "Complete a full EDA on the provided e-commerce dataset; produce a notebook that tells a story from raw data to 5 actionable insights.",
                    },
                    {
                        "day": 11, "title": "Working with Time Series Data",
                        "objectives": [
                            "Parse dates with pd.to_datetime and set a DatetimeIndex",
                            "Resample time series data to different frequencies",
                            "Identify trend, seasonality, and noise with decomposition",
                        ],
                        "key_terms": "DatetimeIndex, resample, rolling, shift, seasonal_decompose, trend, seasonality",
                        "exercise": "Load a stock price CSV; resample to monthly OHLC, compute 20-day and 50-day moving averages, and plot with buy/sell signal markers.",
                    },
                    {
                        "day": 12, "title": "Module Project — Full EDA on Real Dataset",
                        "objectives": [
                            "Apply all Module 1 skills to an unseen real-world dataset",
                            "Deliver a polished, well-commented Jupyter Notebook",
                            "Present key findings in a 3-minute class lightning talk",
                        ],
                        "key_terms": "deliverable, presentation, EDA, insights, notebook, peer feedback",
                        "exercise": "Submit the completed EDA notebook and present 3 key findings. Peer reviewers score on clarity, depth, and visualisation quality.",
                    },
                ],
            },
            {
                "number": 2,
                "title": "Machine Learning",
                "days_range": "Days 13–28",
                "days": [
                    {
                        "day": 13, "title": "ML Workflow — Train, Validate, Test",
                        "objectives": [
                            "Explain the correct split strategy: train / validation / test",
                            "Identify and prevent data leakage in a pipeline",
                            "Implement stratified splitting for imbalanced datasets",
                        ],
                        "key_terms": "train/validation/test split, data leakage, stratified, holdout, cross-validation, baseline",
                        "exercise": "Set up a leakage-free train/val/test split on a housing dataset; compute baseline accuracy using a dummy classifier.",
                    },
                    {
                        "day": 14, "title": "Linear Regression — Housing Prices",
                        "objectives": [
                            "Fit OLS Linear Regression and interpret coefficients",
                            "Evaluate with MSE, RMSE, and R²",
                            "Plot actual vs. predicted and residual distributions",
                        ],
                        "key_terms": "OLS, coefficient, intercept, MSE, RMSE, R², residual, multicollinearity",
                        "exercise": "Predict housing prices on the Boston dataset; identify the three most influential features and explain their coefficient signs.",
                    },
                    {
                        "day": 15, "title": "Logistic Regression — Binary Classification",
                        "objectives": [
                            "Train Logistic Regression for a binary classification problem",
                            "Tune the decision threshold and observe precision/recall trade-off",
                            "Plot the ROC curve and compute AUC",
                        ],
                        "key_terms": "LogisticRegression, sigmoid, threshold, ROC curve, AUC, precision-recall trade-off",
                        "exercise": "Classify loan defaults; tune threshold to achieve recall ≥ 0.85 while keeping precision as high as possible. Plot ROC and P-R curves.",
                    },
                    {
                        "day": 16, "title": "Decision Trees and Random Forests",
                        "objectives": [
                            "Explain information gain and Gini impurity as splitting criteria",
                            "Train and visualise a Decision Tree; explain overfitting risk",
                            "Use a Random Forest and compare OOB score to validation accuracy",
                        ],
                        "key_terms": "information gain, Gini, max_depth, n_estimators, OOB score, feature importance, bagging",
                        "exercise": "Train a tree with no depth limit and observe overfit; then prune with max_depth. Compare to a Random Forest. Plot feature importances.",
                    },
                    {
                        "day": 17, "title": "Support Vector Machines",
                        "objectives": [
                            "Explain the maximum margin classifier and support vectors",
                            "Use the kernel trick (RBF, polynomial) for non-linear data",
                            "Tune C and gamma with GridSearch",
                        ],
                        "key_terms": "SVM, support vector, margin, kernel trick, RBF, C parameter, gamma, hyperplane",
                        "exercise": "Classify two overlapping clusters using SVM with RBF kernel; visualise the decision boundary and support vectors.",
                    },
                    {
                        "day": 18, "title": "K-Means Clustering",
                        "objectives": [
                            "Apply K-Means to segment unlabelled data",
                            "Use the elbow method and silhouette score to choose k",
                            "Interpret and label discovered clusters using domain knowledge",
                        ],
                        "key_terms": "K-Means, centroid, elbow method, silhouette score, inertia, cluster label",
                        "exercise": "Cluster customers by RFM (Recency, Frequency, Monetary) score; label segments and build a descriptive profile for each.",
                    },
                    {
                        "day": 19, "title": "Dimensionality Reduction — PCA",
                        "objectives": [
                            "Explain variance, components, and explained variance ratio in PCA",
                            "Reduce a high-dimensional dataset to 2D for visualisation",
                            "Understand when PCA helps and when it hurts model performance",
                        ],
                        "key_terms": "PCA, principal component, explained variance, scree plot, eigenvector, dimensionality",
                        "exercise": "Apply PCA to the MNIST images; project to 2D and colour by digit class. Plot explained variance vs. number of components.",
                    },
                    {
                        "day": 20, "title": "Model Evaluation — Cross-Validation and ROC",
                        "objectives": [
                            "Implement k-fold and stratified k-fold cross-validation",
                            "Interpret the mean and standard deviation of CV scores",
                            "Compare multiple models' ROC curves on the same axes",
                        ],
                        "key_terms": "k-fold, StratifiedKFold, cross_val_score, mean, std, ROC, AUC, multi-model comparison",
                        "exercise": "Run 5-fold CV on four different classifiers; produce a bar chart of mean ± std accuracy and overlay their ROC curves.",
                    },
                    {
                        "day": 21, "title": "Hyperparameter Tuning",
                        "objectives": [
                            "Distinguish manual tuning from GridSearch and RandomSearch",
                            "Run RandomizedSearchCV to efficiently explore large spaces",
                            "Understand and prevent overfitting to the validation set",
                        ],
                        "key_terms": "GridSearchCV, RandomizedSearchCV, hyperparameter, search space, best_params_, validation leakage",
                        "exercise": "Tune a Random Forest on a Kaggle dataset with RandomizedSearchCV (n_iter=50); report the best config and F1 improvement over default.",
                    },
                    {
                        "day": 22, "title": "Gradient Boosting — XGBoost and LightGBM",
                        "objectives": [
                            "Explain boosting vs. bagging intuitively",
                            "Train an XGBoost classifier with early stopping",
                            "Compare XGBoost and LightGBM speed and accuracy on the same task",
                        ],
                        "key_terms": "boosting, XGBoost, LightGBM, early stopping, learning rate, n_estimators, leaf-wise growth",
                        "exercise": "Train XGBoost and LightGBM on a credit-risk dataset with early stopping. Compare training time, final AUC, and feature importances.",
                    },
                    {
                        "day": 23, "title": "Natural Language Processing — TF-IDF and Classification",
                        "objectives": [
                            "Transform text to TF-IDF vectors and explain the weighting scheme",
                            "Train a text classifier (news category or spam detection)",
                            "Evaluate with F1-score and display the most predictive tokens",
                        ],
                        "key_terms": "TF-IDF, term frequency, inverse document frequency, Naive Bayes, text classification, vocabulary",
                        "exercise": "Train a news headline classifier on the AG News dataset; display the top 10 tokens for each category and report macro F1.",
                    },
                    {
                        "day": 24, "title": "Recommendation Systems",
                        "objectives": [
                            "Explain collaborative filtering vs. content-based filtering",
                            "Build a user-item matrix and compute cosine similarity",
                            "Generate top-N recommendations for a given user",
                        ],
                        "key_terms": "collaborative filtering, content-based, cosine similarity, user-item matrix, cold start, sparse matrix",
                        "exercise": "Build a movie recommender using the MovieLens 100K dataset; for user 42, return top-10 recommendations and explain the rationale.",
                    },
                    {
                        "day": 25, "title": "Time Series Forecasting — ARIMA and Prophet",
                        "objectives": [
                            "Test for stationarity with ADF and apply differencing",
                            "Fit an ARIMA model and interpret p, d, q parameters",
                            "Use Facebook Prophet for trend + seasonality decomposition",
                        ],
                        "key_terms": "ARIMA, stationarity, ADF test, differencing, ACF, PACF, Prophet, trend, seasonality, forecast",
                        "exercise": "Forecast monthly retail sales 6 months ahead with both ARIMA and Prophet; plot forecasts with confidence intervals and compare MAPE.",
                    },
                    {
                        "day": 26, "title": "Model Deployment — Flask and FastAPI",
                        "objectives": [
                            "Serve a trained model as a REST API endpoint with FastAPI",
                            "Validate request payloads using Pydantic schemas",
                            "Test the API with curl and a Python client",
                        ],
                        "key_terms": "FastAPI, endpoint, Pydantic, serialisation, REST, POST, JSON payload, uvicorn",
                        "exercise": "Wrap the Day 22 XGBoost model in a FastAPI app with a /predict endpoint; write a Python client that sends 5 test records and prints results.",
                    },
                    {
                        "day": 27, "title": "ML Pipelines with scikit-learn",
                        "objectives": [
                            "Chain preprocessing and model steps in a Pipeline object",
                            "Use ColumnTransformer for mixed numeric/categorical data",
                            "Ensure the pipeline eliminates all forms of data leakage",
                        ],
                        "key_terms": "Pipeline, ColumnTransformer, make_pipeline, fit_transform, leakage-free, step",
                        "exercise": "Rebuild the Day 14 housing price model as a full Pipeline with imputation, scaling, and regression; run CV inside the pipeline.",
                    },
                    {
                        "day": 28, "title": "Module Project — End-to-End ML Pipeline",
                        "objectives": [
                            "Deliver a complete ML pipeline: ingest → clean → engineer → train → evaluate → deploy",
                            "Document every decision in a structured notebook",
                            "Present results and demo the API to the class",
                        ],
                        "key_terms": "end-to-end, pipeline, deliverable, API demo, notebook, presentation",
                        "exercise": "Submit notebook + FastAPI service + a 4-minute demo. Peers score on pipeline correctness, code quality, and clarity of explanation.",
                    },
                ],
            },
            {
                "number": 3,
                "title": "AI Tools: ChatGPT & Gemini",
                "days_range": "Days 29–36",
                "days": [
                    {
                        "day": 29, "title": "Introduction to Large Language Models",
                        "objectives": [
                            "Explain transformer architecture at a conceptual level",
                            "Distinguish pre-training, fine-tuning, and RLHF",
                            "Compare GPT-4o, Gemini, Claude, and Llama by capability and cost",
                        ],
                        "key_terms": "LLM, transformer, attention, pre-training, fine-tuning, RLHF, token, context window",
                        "exercise": "Send the same complex reasoning prompt to GPT-4o-mini, Gemini Flash, and Claude Haiku; tabulate quality, speed, and token cost.",
                    },
                    {
                        "day": 30, "title": "Prompt Engineering Basics",
                        "objectives": [
                            "Apply zero-shot, one-shot, and few-shot prompting strategies",
                            "Use chain-of-thought prompting to improve reasoning tasks",
                            "Identify when a prompt produces unreliable or hallucinated output",
                        ],
                        "key_terms": "zero-shot, few-shot, chain-of-thought, hallucination, instruction following, temperature",
                        "exercise": "Write three versions of a classification prompt (zero-shot, few-shot, CoT); compare accuracy on 20 labelled test examples.",
                    },
                    {
                        "day": 31, "title": "OpenAI API — Chat Completions",
                        "objectives": [
                            "Authenticate and call the OpenAI Chat Completions endpoint",
                            "Stream responses for real-time UX with stream=True",
                            "Implement retry logic with exponential backoff for rate limits",
                        ],
                        "key_terms": "openai, chat.completions.create, stream, messages, role, system prompt, retry, rate limit",
                        "exercise": "Build a streaming CLI chatbot backed by gpt-4o-mini with a custom system prompt; implement retry with tenacity.",
                    },
                    {
                        "day": 32, "title": "Google Gemini API",
                        "objectives": [
                            "Call the Gemini GenerateContent API with text and image inputs",
                            "Use the multimodal capability to describe and analyse images",
                            "Compare Gemini Flash vs. Gemini Pro for cost and quality",
                        ],
                        "key_terms": "google-generativeai, GenerateContent, multimodal, vision, image input, Gemini Flash, Gemini Pro",
                        "exercise": "Send 5 images (charts, photos) to Gemini and ask it to describe what it sees; evaluate accuracy and note any errors.",
                    },
                    {
                        "day": 33, "title": "Building a Chatbot with Memory",
                        "objectives": [
                            "Maintain conversation history in a messages list for multi-turn chat",
                            "Implement a sliding window to stay within the context limit",
                            "Add a system prompt that defines the bot's persona",
                        ],
                        "key_terms": "conversation history, multi-turn, context window, sliding window, system prompt, persona",
                        "exercise": "Build a multi-turn data science tutor chatbot; demonstrate it correctly referencing a prior question after 8+ turns.",
                    },
                    {
                        "day": 34, "title": "Text Summarisation and Extraction",
                        "objectives": [
                            "Use LLMs to summarise long documents at different lengths",
                            "Extract structured data (JSON) from unstructured text via prompt",
                            "Compare map-reduce summarisation to whole-document summarisation",
                        ],
                        "key_terms": "summarisation, extraction, structured output, JSON, map-reduce, abstractive, extractive",
                        "exercise": "Feed a 5-page research paper PDF to the API; produce a 3-sentence abstract, a bullet-point key findings, and a JSON of authors/year/conclusions.",
                    },
                    {
                        "day": 35, "title": "AI-Powered Data Analysis",
                        "objectives": [
                            "Pass DataFrame summaries and statistics to an LLM for interpretation",
                            "Generate Python code suggestions from a natural language description",
                            "Validate LLM-generated code before execution",
                        ],
                        "key_terms": "code generation, data interpretation, prompt injection, validation, sandboxing",
                        "exercise": "Feed describe() output and a correlation matrix to the LLM; ask it to identify anomalies and suggest visualisations. Execute its suggestions.",
                    },
                    {
                        "day": 36, "title": "Module Project — AI-Assisted Data Report",
                        "objectives": [
                            "Combine EDA, ML results, and LLM narrative into a single report",
                            "Automate the report generation pipeline end-to-end",
                            "Deliver a report that a non-technical stakeholder can read",
                        ],
                        "key_terms": "automated report, narrative, stakeholder, PDF generation, pipeline, non-technical",
                        "exercise": "Build a script that runs EDA, trains a model, and calls an LLM to write a business narrative. Output a PDF report. Present to class.",
                    },
                ],
            },
            {
                "number": 4,
                "title": "Capstone Project",
                "days_range": "Days 37–45",
                "days": [
                    {
                        "day": 37, "title": "Capstone Planning and Data Selection",
                        "objectives": [
                            "Define the problem, target audience, and success metrics",
                            "Select and justify a dataset with at least 1 000 rows",
                            "Draft a project timeline with daily milestones",
                        ],
                        "key_terms": "project brief, success metric, dataset justification, timeline, milestone",
                        "exercise": "Submit: problem statement, dataset link, 3 success metrics, and a day-by-day milestone plan for Days 38–45.",
                    },
                    {
                        "day": 38, "title": "End-to-End EDA",
                        "objectives": [
                            "Execute a full EDA with visualisations for all key features",
                            "Generate and document at least 5 data-driven hypotheses",
                            "Identify feature engineering opportunities",
                        ],
                        "key_terms": "EDA, hypothesis, feature opportunity, distribution, correlation, outlier",
                        "exercise": "Produce the EDA notebook with 5 hypotheses clearly annotated; share with instructor for feedback before Day 39.",
                    },
                    {
                        "day": 39, "title": "Feature Engineering and Model Selection",
                        "objectives": [
                            "Apply a leakage-free feature engineering pipeline",
                            "Benchmark at least three candidate models with cross-validation",
                            "Select the final model and justify with evidence",
                        ],
                        "key_terms": "feature engineering, model selection, benchmark, cross-validation, leakage-free pipeline",
                        "exercise": "Produce a model comparison table (name, CV F1, CV std); write a model selection rationale paragraph.",
                    },
                    {
                        "day": 40, "title": "Model Training and Evaluation",
                        "objectives": [
                            "Train the final model with tuned hyperparameters",
                            "Produce a comprehensive evaluation report with all key metrics",
                            "Interpret results in plain language for a non-technical reader",
                        ],
                        "key_terms": "final model, evaluation report, classification report, confusion matrix, business interpretation",
                        "exercise": "Generate and save the evaluation report; write a 150-word plain-language summary of model performance.",
                    },
                    {
                        "day": 41, "title": "Building a Prediction API",
                        "objectives": [
                            "Wrap the final model in a FastAPI service with /predict and /health endpoints",
                            "Validate inputs with Pydantic and return structured JSON",
                            "Write integration tests for the API",
                        ],
                        "key_terms": "FastAPI, /predict, /health, Pydantic, integration test, JSON response",
                        "exercise": "Deploy the API locally; write a test script that hits /predict with 10 samples and asserts correct response schema.",
                    },
                    {
                        "day": 42, "title": "Adding AI Insights with LLM",
                        "objectives": [
                            "Send model predictions to an LLM to generate a business insight narrative",
                            "Format the narrative for inclusion in the dashboard",
                            "Implement caching so the LLM is not called on every request",
                        ],
                        "key_terms": "LLM integration, narrative, caching, token cost, business insight",
                        "exercise": "Extend the FastAPI service with a /insights endpoint that returns an LLM-generated narrative; demonstrate caching with a timer.",
                    },
                    {
                        "day": 43, "title": "Frontend Dashboard — Streamlit",
                        "objectives": [
                            "Build a multi-section Streamlit app: data overview, predictions, insights",
                            "Connect the dashboard to the FastAPI backend",
                            "Add interactivity: input sliders, file upload, and prediction button",
                        ],
                        "key_terms": "Streamlit, st.dataframe, st.slider, st.button, API call, session state",
                        "exercise": "Launch the Streamlit dashboard; demo a full user journey — upload data, view EDA summary, get prediction, read AI insight.",
                    },
                    {
                        "day": 44, "title": "Testing and Documentation",
                        "objectives": [
                            "Write unit and integration tests for all critical components",
                            "Complete the README with setup, usage, architecture, and examples",
                            "Document the API with auto-generated FastAPI /docs",
                        ],
                        "key_terms": "pytest, unit test, integration test, README, FastAPI docs, docstring",
                        "exercise": "Run the full test suite with zero failures; share the README with a peer who sets up the project from scratch using only the README.",
                    },
                    {
                        "day": 45, "title": "Demo Day — Present to Audience",
                        "objectives": [
                            "Deliver a 7-minute live demo covering problem, data, model, API, and dashboard",
                            "Handle audience questions about methodology and trade-offs",
                            "Submit the complete project repository",
                        ],
                        "key_terms": "demo, presentation, trade-offs, methodology, repository, capstone",
                        "exercise": "Final Demo Day. Submit GitHub repo with: notebook, API code, Streamlit app, tests, README, and a 200-word reflection on lessons learned.",
                    },
                ],
            },
        ],
    },
    # -----------------------------------------------------------------------
    # TRACK 3
    # -----------------------------------------------------------------------
    {
        "number": 3,
        "name": "Engineering AI",
        "audience": "Engineering Students (Age 18–22)",
        "prerequisites": [
            "Solid Python proficiency: OOP, decorators, generators, async",
            "Completed Track 2 or equivalent ML knowledge",
            "Comfortable with Linux CLI, git, and virtual environments",
            "Basic understanding of REST APIs and HTTP",
        ],
        "capstone": "A production-grade AI agent system: a RAG-backed intelligent agent with persistent memory, tool use, FastAPI backend, Streamlit UI, comprehensive test suite, security hardening, and a portfolio-ready deployment.",
        "output_file": "Track3-Engineering-AI.pdf",
        "modules": [
            {
                "number": 1,
                "title": "Advanced ML & Deep Learning",
                "days_range": "Days 1–15",
                "days": [
                    {
                        "day": 1, "title": "Neural Networks from Scratch",
                        "objectives": [
                            "Implement forward pass and backpropagation using only NumPy",
                            "Understand how chain rule drives gradient computation",
                            "Train a 2-layer network on XOR and a simple classification task",
                        ],
                        "key_terms": "backpropagation, chain rule, forward pass, gradient, weight update, NumPy, activation function",
                        "exercise": "Build a 2-layer neural network in pure NumPy. Train on XOR. Plot the loss curve and confirm convergence below 0.01.",
                    },
                    {
                        "day": 2, "title": "PyTorch Fundamentals",
                        "objectives": [
                            "Create and manipulate tensors on CPU and GPU",
                            "Use autograd for automatic gradient computation",
                            "Build and train a simple MLP with torch.nn.Module",
                        ],
                        "key_terms": "tensor, autograd, requires_grad, .backward(), optimizer, DataLoader, Module",
                        "exercise": "Replicate Day 1's network in PyTorch. Compare training speed CPU vs. GPU (if available). Profile with torch.profiler.",
                    },
                    {
                        "day": 3, "title": "CNNs for Image Recognition",
                        "objectives": [
                            "Explain convolution, pooling, and receptive field intuitively",
                            "Build and train a CNN on CIFAR-10 from scratch",
                            "Visualise learned filters and activation maps",
                        ],
                        "key_terms": "Conv2d, MaxPool2d, receptive field, feature map, stride, padding, batch norm",
                        "exercise": "Train a 5-layer CNN on CIFAR-10; achieve >70% test accuracy. Visualise 8 learned filters from the first conv layer.",
                    },
                    {
                        "day": 4, "title": "Transfer Learning with ResNet",
                        "objectives": [
                            "Load a pre-trained ResNet50 and fine-tune on a custom dataset",
                            "Freeze early layers and unfreeze strategically",
                            "Compare from-scratch vs. transfer learning accuracy and training time",
                        ],
                        "key_terms": "transfer learning, fine-tuning, feature extraction, frozen layers, ResNet, torchvision, pretrained weights",
                        "exercise": "Fine-tune ResNet50 on a 5-class flower dataset (500 images); achieve >90% accuracy. Plot training curves for both strategies.",
                    },
                    {
                        "day": 5, "title": "RNNs and LSTMs for Sequences",
                        "objectives": [
                            "Explain the vanishing gradient problem and why LSTMs solve it",
                            "Build an LSTM for next-character prediction",
                            "Apply sequence padding and masking for variable-length inputs",
                        ],
                        "key_terms": "RNN, LSTM, vanishing gradient, cell state, hidden state, sequence padding, PackedSequence",
                        "exercise": "Train a character-level LSTM on Shakespeare text; generate 200 characters starting from a seed phrase and evaluate coherence.",
                    },
                    {
                        "day": 6, "title": "Transformers — Attention Mechanism",
                        "objectives": [
                            "Implement scaled dot-product attention from scratch in PyTorch",
                            "Explain multi-head attention and positional encoding",
                            "Describe how BERT and GPT differ architecturally",
                        ],
                        "key_terms": "attention, query, key, value, softmax, multi-head, positional encoding, encoder, decoder",
                        "exercise": "Implement a single-head attention layer; visualise attention weights on a synthetic sentence pair and verify scores sum to 1.",
                    },
                    {
                        "day": 7, "title": "Training a GPT-2-Style Language Model",
                        "objectives": [
                            "Build a simplified GPT architecture with causal self-attention",
                            "Train on a small text corpus with teacher forcing",
                            "Implement top-k sampling for text generation",
                        ],
                        "key_terms": "causal attention, autoregressive, teacher forcing, top-k sampling, temperature, cross-entropy loss",
                        "exercise": "Train a 4-layer GPT on a Wikipedia subset; generate 5 paragraphs with temperature 0.7 and 1.2. Discuss the difference.",
                    },
                    {
                        "day": 8, "title": "Hyperparameter Tuning with Optuna",
                        "objectives": [
                            "Define an Optuna study and objective function",
                            "Use TPE sampler and pruning for efficient search",
                            "Visualise the parameter importance and optimisation history",
                        ],
                        "key_terms": "Optuna, study, trial, TPE sampler, pruner, param_importance, optimization_history",
                        "exercise": "Tune a PyTorch MLP on MNIST using Optuna (50 trials); plot optimisation history and report best validation accuracy.",
                    },
                    {
                        "day": 9, "title": "Model Interpretability — SHAP and LIME",
                        "objectives": [
                            "Compute SHAP values for a tree-based model and interpret them",
                            "Generate LIME explanations for individual predictions",
                            "Compare global (SHAP) and local (LIME) explainability approaches",
                        ],
                        "key_terms": "SHAP, LIME, Shapley value, feature importance, local explanation, global explanation, waterfall plot",
                        "exercise": "Apply SHAP to the Day 22 (Track 2) XGBoost model; produce a summary plot and explain the top 3 features for a specific prediction.",
                    },
                    {
                        "day": 10, "title": "MLflow — Experiment Tracking",
                        "objectives": [
                            "Instrument a training script with MLflow logging",
                            "Track params, metrics, and model artifacts per run",
                            "Compare runs in the MLflow UI and register the best model",
                        ],
                        "key_terms": "MLflow, experiment, run, log_metric, log_param, log_artifact, model registry, URI",
                        "exercise": "Run 10 experiments with different hyperparameters; register the best model in MLflow and load it programmatically for inference.",
                    },
                    {
                        "day": 11, "title": "Serving ML Models with FastAPI",
                        "objectives": [
                            "Design a production-grade ML serving API with versioned endpoints",
                            "Implement health, readiness, and liveness checks",
                            "Add request/response logging and latency metrics",
                        ],
                        "key_terms": "FastAPI, versioned endpoint, /health, /ready, middleware, latency, structured logging",
                        "exercise": "Serve the MLflow-registered model via FastAPI with /v1/predict; instrument with a timing middleware and log every request as JSON.",
                    },
                    {
                        "day": 12, "title": "Containerising ML Services with Docker",
                        "objectives": [
                            "Write a multi-stage Dockerfile for a FastAPI ML service",
                            "Optimise image size using .dockerignore and layer caching",
                            "Run the container and test the API with curl",
                        ],
                        "key_terms": "Docker, multi-stage build, COPY, RUN, CMD, .dockerignore, layer cache, image size",
                        "exercise": "Containerise the Day 11 FastAPI service; achieve an image size <500 MB. Run and test with curl. Show docker images output.",
                    },
                    {
                        "day": 13, "title": "Model Monitoring in Production",
                        "objectives": [
                            "Detect data drift using EvidentlyAI report generation",
                            "Monitor prediction distribution shift over time",
                            "Set up an alert threshold and describe the on-call response",
                        ],
                        "key_terms": "EvidentlyAI, data drift, prediction drift, report, alert threshold, monitoring, baseline dataset",
                        "exercise": "Introduce artificial drift into a reference dataset; generate an EvidentlyAI report showing drift detected. Propose a retraining trigger.",
                    },
                    {
                        "day": 14, "title": "Distributed Training with PyTorch DDP",
                        "objectives": [
                            "Explain data parallelism vs. model parallelism",
                            "Wrap a PyTorch model with DistributedDataParallel",
                            "Measure the speedup from multi-GPU training on a benchmark",
                        ],
                        "key_terms": "DDP, data parallelism, DistributedDataParallel, world_size, rank, NCCL, gradient synchronisation",
                        "exercise": "Convert the Day 3 CNN to DDP training; benchmark single-GPU vs. 2-GPU throughput (images/sec) and explain the scaling result.",
                    },
                    {
                        "day": 15, "title": "Reinforcement Learning with Stable Baselines3",
                        "objectives": [
                            "Frame an RL problem: state, action, reward, episode",
                            "Train a PPO agent on a Gymnasium environment",
                            "Evaluate with mean episode reward and plot learning curve",
                        ],
                        "key_terms": "RL, state, action, reward, policy, PPO, Gymnasium, episode, learning curve, Stable Baselines3",
                        "exercise": "Train PPO on CartPole-v1 until 490+ mean reward; plot the learning curve. Then swap to LunarLander-v2 and run 100 episodes.",
                    },
                ],
            },
            {
                "number": 2,
                "title": "LLM Engineering & APIs",
                "days_range": "Days 16–25",
                "days": [
                    {
                        "day": 16, "title": "OpenAI API Deep Dive",
                        "objectives": [
                            "Stream chat completions token-by-token for responsive UX",
                            "Implement exponential backoff retry for RateLimitError",
                            "Track token usage per request and estimate monthly cost",
                        ],
                        "key_terms": "stream=True, chunk, RateLimitError, tenacity, tiktoken, token counting, cost estimation",
                        "exercise": "Build a streaming CLI that shows tokens as they arrive, retries on rate limit, and prints total tokens + estimated cost after each message.",
                    },
                    {
                        "day": 17, "title": "Google Gemini API — Multimodal",
                        "objectives": [
                            "Call Gemini with image + text inputs for visual reasoning",
                            "Use Gemini's native JSON output mode for structured extraction",
                            "Compare Gemini Flash vs. Pro on a latency/quality benchmark",
                        ],
                        "key_terms": "google-generativeai, multimodal, vision, JSON mode, response_mime_type, Flash, Pro",
                        "exercise": "Feed 10 product images to Gemini; extract structured JSON (name, category, estimated price) from each. Validate with Pydantic.",
                    },
                    {
                        "day": 18, "title": "Function Calling and Tool Use",
                        "objectives": [
                            "Define tools as JSON schemas and pass them to the OpenAI API",
                            "Handle tool_call responses and route to Python functions",
                            "Build a multi-step tool-use flow with iterative refinement",
                        ],
                        "key_terms": "function calling, tool_call, JSON schema, tool routing, parallel tools, multi-step",
                        "exercise": "Build a weather + calculator agent: define two tools, wire them to real functions, and let the LLM chain them to answer a compound query.",
                    },
                    {
                        "day": 19, "title": "Embeddings and Vector Search with FAISS",
                        "objectives": [
                            "Generate text embeddings using OpenAI's embedding model",
                            "Index embeddings in FAISS and perform nearest-neighbour search",
                            "Understand cosine similarity vs. L2 distance for retrieval",
                        ],
                        "key_terms": "embedding, FAISS, IndexFlatIP, cosine similarity, nearest neighbour, vector index, retrieval",
                        "exercise": "Embed 500 FAQ entries; query with 10 user questions and return the top-3 most similar FAQs. Measure retrieval latency.",
                    },
                    {
                        "day": 20, "title": "Retrieval-Augmented Generation (RAG)",
                        "objectives": [
                            "Implement a full RAG pipeline: chunk → embed → retrieve → generate",
                            "Choose and justify chunk size and overlap for a given corpus",
                            "Evaluate retrieval quality with hit rate and MRR",
                        ],
                        "key_terms": "RAG, chunking, overlap, retrieval, context window, hit rate, MRR, hallucination reduction",
                        "exercise": "Build RAG over a 50-page PDF; answer 20 questions and compute hit@3. Compare answer quality with vs. without retrieval context.",
                    },
                    {
                        "day": 21, "title": "LangChain Framework — LCEL",
                        "objectives": [
                            "Compose LangChain Expression Language (LCEL) chains declaratively",
                            "Use RunnableParallel for concurrent chain branches",
                            "Integrate LangChain with FAISS retriever and chat models",
                        ],
                        "key_terms": "LCEL, RunnableSequence, RunnableParallel, pipe operator, retriever, chat model, chain",
                        "exercise": "Build an LCEL chain that retrieves context, formats it, and generates a structured answer; add a parallel branch for a confidence score.",
                    },
                    {
                        "day": 22, "title": "Claude API and Anthropic SDK",
                        "objectives": [
                            "Call the Anthropic Messages API with system and user turns",
                            "Use Claude's extended thinking for complex reasoning tasks",
                            "Compare Claude, GPT-4o, and Gemini on a structured benchmark",
                        ],
                        "key_terms": "anthropic, Messages API, system prompt, extended thinking, streaming, model comparison",
                        "exercise": "Run a 10-question reasoning benchmark across Claude Sonnet, GPT-4o-mini, and Gemini Flash; tabulate accuracy, latency, and cost.",
                    },
                    {
                        "day": 23, "title": "LLM Cost Optimisation",
                        "objectives": [
                            "Implement prompt caching to reduce repeated-context costs",
                            "Route queries to cheaper models based on complexity classification",
                            "Use semantic caching to avoid redundant API calls",
                        ],
                        "key_terms": "prompt caching, semantic caching, model routing, complexity classifier, cost per token, Redis",
                        "exercise": "Build a routing layer that sends simple queries to Gemini Flash and complex ones to GPT-4o; measure cost reduction on a 100-query benchmark.",
                    },
                    {
                        "day": 24, "title": "Fine-tuning LLMs with LoRA",
                        "objectives": [
                            "Explain LoRA: rank decomposition and why it reduces parameters",
                            "Fine-tune a Llama-3 8B model with LoRA using PEFT and Unsloth",
                            "Evaluate the fine-tuned model vs. base on a task-specific benchmark",
                        ],
                        "key_terms": "LoRA, PEFT, rank, adapter, Unsloth, SFTTrainer, instruction fine-tuning, VRAM",
                        "exercise": "Fine-tune Llama-3-8B on a customer support dataset (1 000 examples); compare F1 on the held-out test set vs. the untuned base model.",
                    },
                    {
                        "day": 25, "title": "Building an LLM Evaluation Framework",
                        "objectives": [
                            "Define evaluation criteria: faithfulness, relevance, coherence",
                            "Use an LLM-as-judge approach to score model outputs at scale",
                            "Build a repeatable eval harness that tracks regressions over time",
                        ],
                        "key_terms": "LLM-as-judge, faithfulness, relevance, coherence, eval harness, regression, score distribution",
                        "exercise": "Evaluate 50 RAG answers with an LLM judge on faithfulness and relevance; compute mean scores and flag answers below threshold.",
                    },
                ],
            },
            {
                "number": 3,
                "title": "Prompt Engineering Mastery",
                "days_range": "Days 26–30",
                "days": [
                    {
                        "day": 26, "title": "Structured Prompt Design",
                        "objectives": [
                            "Apply the CRISPE framework: Context, Role, Instructions, Steps, Parameters, Example",
                            "Use chain-of-thought to decompose multi-step reasoning",
                            "Format system prompts for consistent structured output",
                        ],
                        "key_terms": "CRISPE, chain-of-thought, system prompt, structured output, role, context",
                        "exercise": "Redesign three poor prompts using CRISPE; measure improvement in output quality by scoring 20 responses before and after.",
                    },
                    {
                        "day": 27, "title": "Advanced Prompting Techniques",
                        "objectives": [
                            "Implement ReAct (Reason + Act) prompting for tool-using agents",
                            "Apply self-consistency by sampling multiple outputs and voting",
                            "Use tree-of-thought for complex decision problems",
                        ],
                        "key_terms": "ReAct, self-consistency, tree-of-thought, majority voting, sampling, reasoning trace",
                        "exercise": "Solve 10 multi-step word problems using self-consistency (sample 5 answers, take majority vote); compare to single-sample accuracy.",
                    },
                    {
                        "day": 28, "title": "Prompt Security and Red Teaming",
                        "objectives": [
                            "Identify and demonstrate prompt injection and jailbreak techniques",
                            "Implement input sanitisation and output validation defences",
                            "Design a red-team test suite for a production system prompt",
                        ],
                        "key_terms": "prompt injection, jailbreak, red teaming, sanitisation, output validation, guardrail, adversarial input",
                        "exercise": "Red-team your own Day 26 system prompts with 10 adversarial inputs; document which attacks succeeded and add defences.",
                    },
                    {
                        "day": 29, "title": "Prompt Versioning and A/B Testing",
                        "objectives": [
                            "Version prompts in code with semantic version tags",
                            "Design a statistically valid A/B test for two prompt variants",
                            "Analyse results and make a data-driven promotion decision",
                        ],
                        "key_terms": "prompt versioning, A/B test, statistical significance, p-value, variant, traffic split, champion/challenger",
                        "exercise": "A/B test two system prompts on 200 queries; compute statistical significance with a chi-squared test and write a one-page decision memo.",
                    },
                    {
                        "day": 30, "title": "System Prompt Design for Production",
                        "objectives": [
                            "Write a production system prompt with persona, constraints, output format, and fallbacks",
                            "Handle edge cases: off-topic queries, ambiguous inputs, sensitive topics",
                            "Document the system prompt in version control with a change log",
                        ],
                        "key_terms": "system prompt, persona, constraint, fallback, off-topic handling, change log, version control",
                        "exercise": "Write the production system prompt for a customer-facing AI assistant; test with 20 diverse inputs including 5 edge cases. Document decisions.",
                    },
                ],
            },
            {
                "number": 4,
                "title": "Building AI Agents",
                "days_range": "Days 31–40",
                "days": [
                    {
                        "day": 31, "title": "Agent Architecture Fundamentals",
                        "objectives": [
                            "Define the perceive → plan → act loop for AI agents",
                            "Distinguish reactive agents from deliberative (planning) agents",
                            "Sketch a component diagram for a tool-using agent system",
                        ],
                        "key_terms": "perceive-plan-act, reactive agent, deliberative agent, tool use, action space, environment",
                        "exercise": "Design on paper a customer support agent: list its tools, memory types, constraints, and escalation path. Present to class for critique.",
                    },
                    {
                        "day": 32, "title": "Memory Systems for Agents",
                        "objectives": [
                            "Implement short-term (in-context), long-term (vector DB), and episodic memory",
                            "Retrieve relevant memories based on semantic similarity",
                            "Design a memory eviction policy for a long-running agent",
                        ],
                        "key_terms": "short-term memory, long-term memory, episodic memory, retrieval, eviction, vector DB, semantic similarity",
                        "exercise": "Build an agent that stores user preferences in a vector DB and retrieves relevant ones on each turn; demonstrate correct retrieval after 20 turns.",
                    },
                    {
                        "day": 33, "title": "Multi-Agent Systems with AutoGen",
                        "objectives": [
                            "Configure a two-agent chat (AssistantAgent + UserProxyAgent)",
                            "Build a group chat with a planner, coder, and critic agent",
                            "Handle agent failures and implement a retry/escalation policy",
                        ],
                        "key_terms": "AutoGen, AssistantAgent, UserProxyAgent, GroupChat, group_chat_manager, escalation",
                        "exercise": "Build a coding team: planner decomposes task, coder writes code, critic reviews it. Run on 3 tasks and evaluate output quality.",
                    },
                    {
                        "day": 34, "title": "LangGraph — Stateful Agent Workflows",
                        "objectives": [
                            "Model agent workflows as directed graphs with LangGraph",
                            "Implement conditional edges for dynamic routing decisions",
                            "Persist agent state across invocations with checkpointing",
                        ],
                        "key_terms": "LangGraph, StateGraph, node, edge, conditional edge, checkpointer, state schema",
                        "exercise": "Build a LangGraph workflow for a research agent: search → read → summarise → decide (enough info? → answer : search again).",
                    },
                    {
                        "day": 35, "title": "Guardrails and Safety for Agents",
                        "objectives": [
                            "Implement input and output guardrails using the Guardrails AI library",
                            "Define a policy that blocks harmful outputs before they reach the user",
                            "Test guardrails against a red-team set of adversarial inputs",
                        ],
                        "key_terms": "guardrails, policy, input validation, output validation, Guardrails AI, harm prevention, red team",
                        "exercise": "Add guardrails to the Day 30 system; run the 20 Day-28 adversarial inputs — all must be blocked or safely redirected. Document pass rate.",
                    },
                    {
                        "day": 36, "title": "Agent Observability with LangSmith",
                        "objectives": [
                            "Instrument an agent with LangSmith tracing",
                            "Inspect full trace trees including tool calls and retrieval steps",
                            "Set up a LangSmith dataset and run automated evaluations",
                        ],
                        "key_terms": "LangSmith, trace, span, evaluation dataset, feedback, run, project",
                        "exercise": "Trace 20 agent runs in LangSmith; identify the two highest-latency steps and propose optimisations. Run an automated evaluation on the dataset.",
                    },
                    {
                        "day": 37, "title": "Deploying Agents to Production",
                        "objectives": [
                            "Wrap an agent in a FastAPI async endpoint",
                            "Use Celery + Redis for long-running agent tasks",
                            "Implement rate limiting and request queuing for production safety",
                        ],
                        "key_terms": "async FastAPI, Celery, Redis, task queue, rate limiting, webhook, job polling",
                        "exercise": "Deploy the Day 34 LangGraph agent as a FastAPI async job; test with 20 concurrent requests and measure queue depth and latency under load.",
                    },
                    {
                        "day": 38, "title": "Coding Agent with Code Execution",
                        "objectives": [
                            "Build an agent that generates, executes, and iterates on Python code",
                            "Sandbox code execution to prevent escape and resource abuse",
                            "Handle execution errors gracefully with self-correction",
                        ],
                        "key_terms": "code execution, sandbox, subprocess, resource limit, self-correction, code generation, iteration",
                        "exercise": "Build a data analysis agent that accepts a CSV and a question in English; generates and runs analysis code until it produces a correct answer.",
                    },
                    {
                        "day": 39, "title": "Browser Agent with Playwright",
                        "objectives": [
                            "Control a headless browser with Playwright from Python",
                            "Build an agent that navigates, clicks, and extracts structured data",
                            "Handle dynamic pages, login flows, and anti-bot measures ethically",
                        ],
                        "key_terms": "Playwright, headless browser, page.goto, locator, extract, dynamic content, ethical scraping",
                        "exercise": "Build a browser agent that searches for a product on an e-commerce site, extracts name/price/rating for the top 5 results, and returns JSON.",
                    },
                    {
                        "day": 40, "title": "Building a Production RAG Agent",
                        "objectives": [
                            "Combine RAG, tool use, memory, and guardrails into one agent",
                            "Instrument with LangSmith and measure end-to-end latency",
                            "Optimise retrieval with reranking using a cross-encoder",
                        ],
                        "key_terms": "production RAG, cross-encoder, reranking, end-to-end, latency, guardrail, tracing",
                        "exercise": "Build the full production RAG agent; run a 50-question eval and report faithfulness, relevance, and latency p50/p95. Fix any regressions.",
                    },
                ],
            },
            {
                "number": 5,
                "title": "Capstone Project",
                "days_range": "Days 41–45",
                "days": [
                    {
                        "day": 41, "title": "Capstone Kickoff — System Design",
                        "objectives": [
                            "Produce a full system design document: components, data flow, APIs, storage",
                            "Define non-functional requirements: latency, throughput, reliability",
                            "Present the design for peer and instructor review",
                        ],
                        "key_terms": "system design, NFR, latency, throughput, reliability, component diagram, data flow",
                        "exercise": "Submit a 2-page system design document with a component diagram. Gate: instructor must approve before implementation begins.",
                    },
                    {
                        "day": 42, "title": "Core Intelligence Layer",
                        "objectives": [
                            "Implement the agent loop with RAG, tool use, and memory",
                            "Instrument with LangSmith from day one",
                            "Achieve passing scores on a pre-defined 20-question eval set",
                        ],
                        "key_terms": "agent loop, RAG, tool use, memory, eval, LangSmith, tracing, quality gate",
                        "exercise": "Pass the 20-question eval set with faithfulness ≥ 0.8 and relevance ≥ 0.75 before proceeding to Day 43.",
                    },
                    {
                        "day": 43, "title": "Frontend and API Integration",
                        "objectives": [
                            "Build a Streamlit UI with chat interface, document upload, and trace viewer",
                            "Connect to the FastAPI backend with proper error handling",
                            "Implement loading states and graceful degradation",
                        ],
                        "key_terms": "Streamlit, chat interface, document upload, session state, error handling, graceful degradation",
                        "exercise": "Demo the full UI → API → agent → response flow with a classmate as the user. Fix any UX issues identified in the session.",
                    },
                    {
                        "day": 44, "title": "Testing, Security, and Hardening",
                        "objectives": [
                            "Achieve ≥80% test coverage with unit and integration tests",
                            "Run a load test with Locust to verify performance under concurrent users",
                            "Harden the system: input sanitisation, rate limiting, secrets management",
                        ],
                        "key_terms": "test coverage, Locust, load test, input sanitisation, rate limiting, Vault, secrets management",
                        "exercise": "Run Locust with 50 concurrent users for 5 minutes; achieve p95 latency <5s. Fix any failures or bottlenecks before Demo Day.",
                    },
                    {
                        "day": 45, "title": "Demo Day — Portfolio Presentation",
                        "objectives": [
                            "Deliver a 10-minute live system demo to an audience including guests",
                            "Walk through: problem, system design, agent behaviour, eval results, learnings",
                            "Present the project as a portfolio piece for interviews and GitHub",
                        ],
                        "key_terms": "demo, portfolio, system design walkthrough, eval results, GitHub, Q&A",
                        "exercise": "Final Demo Day. Submit GitHub repo with: full codebase, Docker setup, README, architecture diagram, eval results, and 300-word reflection.",
                    },
                ],
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def make_styles(accent_color):
    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=WHITE,
        leading=36,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    styles["cover_tagline"] = ParagraphStyle(
        "cover_tagline",
        fontName="Helvetica",
        fontSize=13,
        textColor=HexColor("#CBD5E1"),
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["cover_meta"] = ParagraphStyle(
        "cover_meta",
        fontName="Helvetica",
        fontSize=11,
        textColor=WHITE,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles["cover_track"] = ParagraphStyle(
        "cover_track",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=WHITE,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=accent_color,
        leading=20,
        spaceBefore=16,
        spaceAfter=6,
    )
    styles["module_title"] = ParagraphStyle(
        "module_title",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=accent_color,
        leading=28,
        spaceBefore=0,
        spaceAfter=4,
    )
    styles["module_subtitle"] = ParagraphStyle(
        "module_subtitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=TEXT_DARK,
        leading=18,
        spaceAfter=10,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=4,
    )
    styles["body_bold"] = ParagraphStyle(
        "body_bold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=2,
    )
    styles["day_heading"] = ParagraphStyle(
        "day_heading",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=accent_color,
        leading=16,
        spaceBefore=10,
        spaceAfter=1,
    )
    styles["lesson_title"] = ParagraphStyle(
        "lesson_title",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=TEXT_DARK,
        leading=15,
        spaceAfter=4,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=10,
        textColor=TEXT_DARK,
        leading=14,
        leftIndent=16,
        spaceAfter=2,
        bulletIndent=6,
    )
    styles["key_terms"] = ParagraphStyle(
        "key_terms",
        fontName="Helvetica",
        fontSize=9,
        textColor=HexColor("#475569"),
        leading=13,
        spaceAfter=2,
    )
    styles["exercise"] = ParagraphStyle(
        "exercise",
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=HexColor("#334155"),
        leading=14,
        leftIndent=12,
        spaceAfter=8,
        borderPad=4,
    )
    styles["table_header"] = ParagraphStyle(
        "table_header",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=WHITE,
        leading=13,
        alignment=TA_CENTER,
    )
    styles["table_cell"] = ParagraphStyle(
        "table_cell",
        fontName="Helvetica",
        fontSize=9,
        textColor=TEXT_DARK,
        leading=13,
    )
    styles["table_cell_center"] = ParagraphStyle(
        "table_cell_center",
        fontName="Helvetica",
        fontSize=9,
        textColor=TEXT_DARK,
        leading=13,
        alignment=TA_CENTER,
    )
    styles["overview_label"] = ParagraphStyle(
        "overview_label",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=accent_color,
        leading=14,
        spaceBefore=8,
        spaceAfter=2,
    )
    styles["small_grey"] = ParagraphStyle(
        "small_grey",
        fontName="Helvetica",
        fontSize=8,
        textColor=GREY_MID,
        leading=11,
        alignment=TA_CENTER,
    )
    return styles


# ---------------------------------------------------------------------------
# Page templates (header + footer on every non-cover page)
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
HEADER_H = 18 * mm
FOOTER_H = 14 * mm


def make_header_footer(track_number, track_name, accent_color):
    """Returns onPage callable for page decorations."""

    def draw(canvas, doc):
        page_num = doc.page
        # Skip decoration on the cover (page 1)
        if page_num == 1:
            return

        canvas.saveState()

        # --- Header ---
        header_text = f"NExGen School of Computers  |  Track {track_number} \u2014 {track_name}"
        canvas.setFillColor(accent_color)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(MARGIN, PAGE_H - 14 * mm, header_text)
        # thin rule
        canvas.setStrokeColor(accent_color)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - 16 * mm, PAGE_W - MARGIN, PAGE_H - 16 * mm)

        # --- Footer ---
        canvas.setStrokeColor(GREY_RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, FOOTER_H + 2 * mm, PAGE_W - MARGIN, FOOTER_H + 2 * mm)
        canvas.setFillColor(GREY_MID)
        canvas.setFont("Helvetica", 8)
        footer_text = "www.nex-gen.in  |  ISO 9001:2015 Certified"
        canvas.drawCentredString(PAGE_W / 2, FOOTER_H - 2 * mm, footer_text)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(TEXT_DARK)
        canvas.drawCentredString(PAGE_W / 2, FOOTER_H + 4 * mm, str(page_num))

        canvas.restoreState()

    return draw


# ---------------------------------------------------------------------------
# Cover page builder
# ---------------------------------------------------------------------------
def build_cover(track, styles, accent_color):
    story = []
    # Top colored block via a table
    cover_data = [[
        Paragraph("NEx-gEN School of Computers", styles["cover_title"]),
    ]]
    cover_table = Table(
        [
            [Paragraph("NEx-gEN School of Computers", styles["cover_title"])],
            [Paragraph("Empowering Futures Through Quality Education", styles["cover_tagline"])],
            [Paragraph("ISO 9001:2015 Certified", styles["cover_meta"])],
            [Spacer(1, 8 * mm)],
            [Paragraph(f"Track {track['number']}", styles["cover_meta"])],
            [Paragraph(track["name"], styles["cover_track"])],
            [Spacer(1, 6 * mm)],
            [Paragraph("Duration: 45 Days", styles["cover_meta"])],
            [Paragraph("Location: Srikakulam, Andhra Pradesh", styles["cover_meta"])],
            [Paragraph("www.nex-gen.in", styles["cover_meta"])],
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_DARK),
        ("TOPPADDING", (0, 0), (-1, 0), 30),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 30),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))

    # Accent band at top of cover block
    accent_band = Table(
        [[Paragraph("", styles["body"])]],
        colWidths=[PAGE_W - 2 * MARGIN],
        rowHeights=[8],
    )
    accent_band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent_color),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    story.append(Spacer(1, 30 * mm))
    story.append(accent_band)
    story.append(cover_table)

    # Audience badge
    story.append(Spacer(1, 10 * mm))
    badge_data = [[
        Paragraph(f"Designed for: {track['audience']}", ParagraphStyle(
            "badge", fontName="Helvetica-Bold", fontSize=11,
            textColor=accent_color, alignment=TA_CENTER, leading=15,
        ))
    ]]
    badge = Table(badge_data, colWidths=[PAGE_W - 2 * MARGIN])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#EEF2FF")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 1, accent_color),
    ]))
    story.append(badge)
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Course overview page
# ---------------------------------------------------------------------------
def build_overview(track, styles, accent_color):
    story = []
    story.append(Paragraph("Course Overview", styles["section_heading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_color, spaceAfter=8))

    story.append(Paragraph("Who Is This For?", styles["overview_label"]))
    story.append(Paragraph(track["audience"], styles["body"]))

    story.append(Paragraph("Prerequisites", styles["overview_label"]))
    for p in track["prerequisites"]:
        story.append(Paragraph(f"\u2022  {p}", styles["bullet"]))

    story.append(Paragraph("Capstone Project", styles["overview_label"]))
    story.append(Paragraph(track["capstone"], styles["body"]))

    story.append(Spacer(1, 6 * mm))
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Module overview table
# ---------------------------------------------------------------------------
def build_module_table(track, styles, accent_color):
    story = []
    story.append(Paragraph("Module Overview", styles["section_heading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_color, spaceAfter=8))

    header = [
        Paragraph("Module", styles["table_header"]),
        Paragraph("Title", styles["table_header"]),
        Paragraph("Days", styles["table_header"]),
        Paragraph("Key Focus Areas", styles["table_header"]),
    ]
    rows = [header]

    for mod in track["modules"]:
        # derive key topics from first and last day titles
        day_titles = [d["title"] for d in mod["days"]]
        sample = day_titles[:3]
        topics_text = ", ".join(sample)
        if len(day_titles) > 3:
            topics_text += ", ..."
        rows.append([
            Paragraph(str(mod["number"]), styles["table_cell_center"]),
            Paragraph(mod["title"], styles["table_cell"]),
            Paragraph(mod["days_range"], styles["table_cell_center"]),
            Paragraph(topics_text, styles["table_cell"]),
        ])

    col_widths = [18 * mm, 55 * mm, 28 * mm, 69 * mm]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), accent_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY_RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Module divider page
# ---------------------------------------------------------------------------
def build_module_divider(mod, styles, accent_color):
    story = []

    # Left accent bar via a table
    bar_data = [[
        Table([[""]], colWidths=[6], rowHeights=[60]),
        Table([
            [Paragraph(f"Module {mod['number']}", styles["module_subtitle"])],
            [Paragraph(mod["title"], styles["module_title"])],
            [Paragraph(mod["days_range"], styles["module_subtitle"])],
        ], colWidths=[PAGE_W - 2 * MARGIN - 20])
    ]]
    bar_table = Table(bar_data, colWidths=[12, PAGE_W - 2 * MARGIN - 12])
    bar_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), accent_color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(Spacer(1, 8 * mm))
    story.append(bar_table)
    story.append(Spacer(1, 4 * mm))
    return story


# ---------------------------------------------------------------------------
# Individual lesson block
# ---------------------------------------------------------------------------
def build_lesson(day_data, styles, accent_color):
    story = []
    items = []

    items.append(Paragraph(f"Day {day_data['day']}", styles["day_heading"]))
    items.append(Paragraph(day_data["title"], styles["lesson_title"]))

    for obj in day_data["objectives"]:
        items.append(Paragraph(f"\u2022  {obj}", styles["bullet"]))

    items.append(Paragraph(
        f"<b>Key Terms:</b> {day_data['key_terms']}",
        styles["key_terms"]
    ))
    items.append(Paragraph(
        f"<b>Exercise:</b> {day_data['exercise']}",
        styles["exercise"]
    ))
    items.append(HRFlowable(width="100%", thickness=0.3, color=GREY_RULE, spaceAfter=2))

    story.append(KeepTogether(items))
    return story


# ---------------------------------------------------------------------------
# Main build function per track
# ---------------------------------------------------------------------------
def build_track_pdf(track):
    accent_color = ACCENT[track["number"]]
    styles = make_styles(accent_color)
    out_path = f"/Applications/Projects/nexgen-ai-courses/docs/{track['output_file']}"

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=24 * mm,
        bottomMargin=20 * mm,
        title=f"Track {track['number']} — {track['name']}",
        author="NExGen School of Computers",
        subject="Course Curriculum",
    )

    on_page = make_header_footer(track["number"], track["name"], accent_color)

    story = []
    story += build_cover(track, styles, accent_color)
    story += build_overview(track, styles, accent_color)
    story += build_module_table(track, styles, accent_color)

    for mod in track["modules"]:
        story += build_module_divider(mod, styles, accent_color)
        for day_data in mod["days"]:
            story += build_lesson(day_data, styles, accent_color)
        story.append(PageBreak())

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs("/Applications/Projects/nexgen-ai-courses/docs", exist_ok=True)
    for track in TRACKS:
        print(f"Building Track {track['number']} — {track['name']} ...", end=" ", flush=True)
        path = build_track_pdf(track)
        size_kb = os.path.getsize(path) / 1024
        print(f"Done  →  {path}  ({size_kb:.1f} KB)")
    print("\nAll 3 PDFs generated successfully.")
