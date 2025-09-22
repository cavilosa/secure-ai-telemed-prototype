# 🛡️ Secure AI Telemedicine Prototype

## 📖 Table of Contents

- [Project Vision](#project-vision)
- [Core Features](#core-features)
- [Security Focus](#security-focus)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Roadmap](#project-roadmap)
- [Advanced Ideas & Future Scope](#advanced-ideas--future-scope)
- [Key Concepts & Resources](#key-concepts--resources)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Vision

In an era of rapidly advancing AI, handling sensitive data—especially Protected Health Information (PHI)—requires more than just functional code. This project serves as a practical, hands-on exploration of building a secure and resilient system from the ground up.

The goal is not just to build a telemedicine app, but to answer the question: **"How can we leverage AI features while systematically managing the unique risks they introduce?"**

This repository documents the entire lifecycle of securing a modern web application, from initial design and defensive AI implementation to adversarial stress-testing, automated MLOps pipelines, and finally, a full compliance-focused security audit. It is built with a cross-border compliance mindset, considering the principles of both the **US Health Insurance Portability and Accountability Act (HIPAA)** and **Canada's Personal Information Protection and Electronic Documents Act (PIPEDA)**.

## ✨ Core Features

* **Secure Messaging Module:** A chat system for patients and healthcare navigators.

* **AI-Powered PII/PHI Redaction:** An NLP-based filter that uses **Named Entity Recognition (NER)** to automatically detect and tokenize sensitive information in real-time before it's stored.

* **Reversible Masking (Tokenization):** Sensitive data is vaulted and replaced with non-sensitive tokens. The original data is only ever reconstructed in-memory for authorized, authenticated users.

* **JWT-Based Authentication:** Secure, stateless user authentication managed via Auth0.

* **Secure CI/CD Pipeline:** An automated pipeline using GitHub Actions to test code, scan for vulnerabilities, and run adversarial attacks on the AI model before deployment.

* **Structured Logging & Monitoring:** Detailed, structured (JSON) logs for security events, especially for authentication attempts and access to sensitive data.

## 🔐 Security Focus

This project is built around a four-phase security implementation plan:

1. **Phase 1: Defensive AI & Secure Foundations:** Building the initial application with security controls and a defensive AI-powered PII filter at its core.

2. **Phase 2: Adversarial Mindset & Red Teaming:** Developing a custom **Prompt Injection Fuzzer** to actively attack and identify weaknesses in the AI filter.

3. **Phase 3: Secure MLOps & Automation:** Creating a CI/CD pipeline that automates security testing, ensuring vulnerabilities are caught before they reach production.

4. **Phase 4: Full-Stack Audit & Compliance:** Conducting a comprehensive security audit of the entire application and producing a professional report mapping controls to HIPAA and PIPEDA principles.

## 🏗️ System Architecture

The system is designed with a core principle of data separation. The main application database stores only tokenized, non-sensitive information, while a separate, highly-secured "vault" stores the actual PII/PHI. Access to this vault is strictly controlled and heavily audited.

## 🛠️ Technology Stack

* **Backend:** Python 3.11+, Flask

* **AI/ML:** spaCy (for Named Entity Recognition), Scikit-learn

* **Database:** Neon (Serverless PostgreSQL), SQLite (development)

* **Authentication:** Auth0, PyJWT

* **Containerization:** Docker, Docker Compose

* **CI/CD:** GitHub Actions

* **Cloud Platform:** Heroku (Application Hosting), AWS S3 (File Storage)

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running for development and testing purposes.

### Prerequisites

* Python 3.10+

* Pip & Virtualenv

* Git

### Installation

1. **Clone the repository:**

   ```
   git clone [https://github.com/cavilosa/secure-ai-telemed-prototype.git](https://github.com/cavilosa/secure-ai-telemed-prototype.git)
   cd secure-ai-telemed-prototype
   
   ```

2. **Create and activate a virtual environment:**

   ```
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

4. **Download the NLP model:**

   ```
   python -m spacy download en_core_web_sm
   
   ```

5. **Run the application:**

   ```
   flask run
   
   ```

   The application will be available at `http://127.0.0.1:5000`.
   

## 🧪 Testing

This project uses `pytest` for unit and integration testing. All tests are located in the `tests/` directory.

The initial test suite in `tests/test_reduction.py` covers the PII/PHI redaction logic, ensuring that emails and phone numbers are correctly identified and redacted while invalid formats are ignored.

### Running Tests

1.  Make sure you have installed all project dependencies, including `pytest`.
2.  From the project's root directory, run the following command:

    ```bash
    pytest
    ```
    or
    ```
    python -m pytest
    ```

This will automatically discover and run all test files within the `tests/` directory.

## 🗺️ Project Roadmap

* \[x\] **Phase 1: Foundations & Secure AI Prototype (Sept – Nov 2025)**

  * \[x\] Scaffold Flask application with Blueprints

  * \[ \] Implement AI-powered PII/PHI Redaction Filter (Regex + NER)

  * \[ \] Integrate JWT-based authentication

  * \[ \] Dockerize the application

  * \[ \] Pass ISC² Certified in Cybersecurity (CC) exam

* \[ \] **Phase 2: Adversarial Mindset & Public Debut (Dec 2025 – Feb 2026)**

  * \[ \] Develop a Python-based Prompt Injection Fuzzer

  * \[ \] Conduct Red Team exercise against the PII filter

  * \[ \] Publish a blog post detailing the fuzzer and its findings

  * \[ \] Begin studying for CompTIA Security+

* \[ \] **Phase 3: Automation & Cross-Border Compliance (Mar – May 2026)**

  * \[ \] Build a Secure CI/CD Pipeline with GitHub Actions

  * \[ \] Automate adversarial testing within the pipeline

  * \[ \] Deep dive into HIPAA (Technical Safeguards) & PIPEDA (10 Principles)

  * \[ \] Write an article on automating security for AI features

* \[ \] **Phase 4: Full-Stack Audit & Professional Polish (June – Aug 2026)**

  * \[ \] Write a comprehensive AI Security Audit Report

  * \[ \] Map all technical controls to HIPAA/PIPEDA requirements

  * \[ \] Pass the CompTIA Security+ exam

  * \[ \] Polish portfolio and prepare for job search

## 🧠 Advanced Ideas & Future Scope

This project serves as a foundation. Here are some advanced concepts that could be explored in the future:

* **Fine-Tuning the NER Model:** Fine-tune a transformer model (like BERT) on custom, domain-specific medical data to create a PII filter with much higher accuracy and the ability to detect custom entity types (e.g., `MEDICAL_CONDITION`, `DRUG_NAME`).

* **Differential Privacy:** Implement techniques that allow for statistical analysis of the chat data without exposing individual user information.

* **Zero Trust Architecture (ZTA):** Evolve the infrastructure so that no user or service is trusted by default, requiring strict verification for every request.

* **Homomorphic Encryption:** Explore the possibility of performing computations directly on encrypted data without ever decrypting it.

* **Automated Compliance Checks:** Build scripts into the CI/CD pipeline that automatically check infrastructure and code against a subset of HIPAA/PIPEDA technical requirements.

## 📚 Key Concepts & Resources

This project is built upon established industry frameworks and best practices.

| Concept / Technology | Resource Link | 
 | ----- | ----- | 
| **Flask Framework** | [Flask Documentation](https://flask.palletsprojects.com/) | 
| **spaCy NLP Library** | [spaCy Website](https://spacy.io/) | 
| **OWASP Top 10** | [OWASP Top 10 Project](https://owasp.org/www-project-top-ten/) | 
| **MITRE ATLAS™** | [Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/) | 
| **NIST AI RMF** | [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | 
| **HIPAA Security Rule** | [HHS.gov Summary](https://www.hhs.gov/hipaa/for-professionals/security/index.html) | 
| **PIPEDA Principles** | [OPC Canada Website](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/pipeda_brief/) | 

## 🙌 Contributing

This is a personal portfolio project, but feedback and suggestions are always welcome. Please feel free to open an issue to discuss any ideas or potential improvements.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.