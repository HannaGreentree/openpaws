# OpenPaws — The most Transparent Animal Rescue Support Platform

## Live Project

Deployed site:  
https://openpaws.onrender.com  

GitHub repository:  
https://github.com/HannaGreentree/openpaws

---

OpenPaws is a **full-stack Django web application** designed to provide a fast way for animal shelters and independent volunteers in Ukraine to raise funds for the animals they care about.

The platform allows shelters to request financial support for specific needs such as food, medical treatment, or parasite treatments.

To request help, shelters must first be **registered on the platform and authorised by the admin**. Visitors can support authorised shelters and volunteers by donating through the platform.

Every "closed" case gives a shelter 1 positive trust point.

There are **two ways to support animal shelters**:

- by donating to the platform and being able to see evidence of how the money is spent  
- by sending money directly to shelters using the **“Thank You”** donation option  

The more positive points a shelter has, the more credible it appears to users.

A key principle of the platform is **transparency**.

Every funded case must include proof showing how the donated money was used.  
This may include receipts, images, invoices, and links to social media publications demonstrating that the funds helped animals.

By requiring this evidence before a case can be closed, the platform ensures that donations remain accountable and traceable.

OpenPaws - Bank of Animals

---

## Platform Concept

OpenPaws is a transparency-based animal aid platform.

It brings together animal shelters and private rescuers who are willing to clearly show:

- how much support they received  
- what the money was spent on  
- what result was achieved  

The goal of the platform is to help donors feel safer, more confident, and more willing to support real animal rescue work.

---

# Project Purpose

The goal of this project is to demonstrate a **Full Stack MVC Django application** that:

- stores and manipulates relational data  
- allows user interaction through forms  
- processes payments using Stripe  
- demonstrates authentication, permissions and validation  
- implements a clear workflow system for case funding  
- provides transparency for donors  

---

# Vision

The vision of OpenPaws is to create a system where helping animals is based on trust.

- donors gain confidence  
- shelters gain credibility  
- animals receive the support they urgently need  

---

# Target Users

The application serves three types of users.

---

### Public Users

Public visitors can:

- browse shelters  
- browse rescue cases  
- donate to the platform  
- send “Thank You” donations directly to shelters  
- see case progress and transparency information  
- see receipts and platform balance  

Public users do not need to log in.

---

### Shelter / Volunteer Users

Approved shelters or volunteers can:

- create rescue cases  
- request funding  
- submit proof showing how funds were used  

---

### Admin Users

Administrators can:

- approve or reject case funding  
- review proof submissions  
- close or reject cases  
- manage shelters and donations  
- control case workflow  

---

# Case Workflow

OPEN → PROCESSING → AWAITING_REVIEW → CLOSED

### OPEN  
The shelter creates a case requesting funding.

### PROCESSING  
Admin approves the case and funding begins.

### AWAITING REVIEW  
The shelter uploads proof of how the money was used.

### CLOSED  
Admin reviews the proof and closes the case.

---

# UX Design

The design of OpenPaws focuses on clarity, trust, and ease of use.

The platform was designed to ensure that users can quickly understand:

- what the platform does  
- how to browse shelters and cases  
- how to support animals through donations  
- how transparency information is presented  

Key UX decisions include:

- simple and consistent navigation across all pages  
- clear call-to-action buttons for donations  
- structured layouts for case and shelter information  
- consistent styling and spacing across components  
- responsive design for mobile, tablet, and desktop devices  

The goal of the design is to build user trust and reduce confusion.

---

# Technologies Used

### Main Technologies

- HTML  
- CSS  
- JavaScript  
- Python  
- Django  

### Backend

- Django 4.2  

### Frontend

- Django Templates  
- HTML5  
- CSS3  
- JavaScript  

### Database

- SQLite (development database)  

### Payments

- Stripe Checkout (test mode)  

---

# Installation

To run this project locally:

1. Clone the repository:

```bash
git clone https://github.com/HannaGreentree/openpaws.git

2. Navigate into the project:

```bash
cd openpaws

3. Create a virtual environment:

```bash
python -m venv venv

4. Activate the environment:
Mac/Linux:

```bash
source venv/bin/activate

Windows:

```bash
venv\Scripts\activate

5. Install dependencies: 

```bash
pip install -r requirements.txt

6. Run migrations:

```bash
python manage.py migrate

7. Start the server:

```bash
python manage.py runserver

# Database Design

## Shelter Model
- name  
- country  
- city  
- animals_count  
- trust_points  

## Case Model
- shelter  
- title  
- description  
- amount_requested  
- amount_funded  
- status  
- proof_link  

## Donation Model
- donation_type  
- amount  
- stripe_session_id  
- paid  

---

# CRUD Functionality

## Create
- shelters  
- cases  
- donations  

## Read
- browse shelters  
- browse cases  
- view details  

## Update
- update case status  
- submit proof  

## Delete
- admin only  

---

# Stripe Payment Integration

Two donation types:

- Platform donations  
- Thank You donations  

Stripe test mode is used.

---

# User Authentication

- admin users  
- shelter users  

---

# Features and Screenshots

## Case Workflow

## Payments

## Admin Panel

## Case Detail

---

# Testing

Manual testing covered:

- navigation  
- workflow  
- validation  
- payments  
- permissions  

Full testing documentation:  
TESTING.md  

Screenshots:  
images/screenshots/  

---

## CSS Validation and Testing

CSS was tested using:  
https://jigsaw.w3.org/css-validator/

---

## Accessibility Testing

Accessibility was tested using:  
https://www.accessibilitychecker.org  

---

## Accessibility Statement

OpenPaws was developed with accessibility in mind and aims to follow the **Web Content Accessibility Guidelines (WCAG) 2.1 / 2.2 Level AA**.

The design aims to meet WCAG 2.1 Level AA standards where possible.

The following accessibility measures were implemented:

- clear navigation structure  
- readable font sizes  
- sufficient colour contrast  
- keyboard-accessible elements  
- visible focus states  
- responsive design  

---

# Known Bugs

- Case-specific donations not implemented  
- Thank You payments require manual transfer  
- Trust points explanation not visible  

---

# Fixed Bugs During Development

- migration issues resolved  
- template errors fixed  
- Stripe configuration corrected  

---

# Future Improvements

- automated Stripe webhooks  
- direct case donations  
- shelter dashboards  
- improved transparency visualisation  

---

# Deployment

- GitHub for version control  
- Render for hosting  

The application was deployed using environment variables for sensitive data and configured to run in production mode.

---

# Code Quality

- clean structure  
- readable logic  
- separation of concerns  

---

# Credits

## Resources used during development

- Django Documentation  
- Stripe Documentation  
- Python Documentation  

---

## AI Assistance

This project made use of AI tools such as ChatGPT to support the development process.

AI was used for:

- debugging errors  
- improving code structure  
- explaining technical concepts  
- refining documentation  

All code was reviewed, tested, and adapted to fit the project requirements.

The final implementation and project logic were fully understood and verified by the author.

AI tools were used as a support tool only and not as a replacement for learning or development.

---

# Author

Hanna Greentree

---

# User Stories

## Public Visitor

- As a visitor, I want to browse shelters and cases so that I can understand where help is needed.  
![Home Page](images/user-stories/user-home.png)

- As a visitor, I want to view shelters so I can learn about organisations caring for animals.  
![Shelters Page](images/screenshots/user-stories-user-shelters.png)

- As a visitor, I want to view details about a shelter so I can understand their work.  
![Shelter Profile](images/screenshots/user-stories-shelter-profile.png)

- As a visitor, I want to browse rescue cases so I can see what support animals need.  
![Cases Page](images/screenshots/user-stories-user-cases.png)

- As a visitor, I want to see details of a rescue case so I can understand what funds will be used for.  
![Case Detail](images/screenshots/user-stories-case-detail.png)

---

## Donor

- As a donor, I want to donate to the platform so that rescue cases can receive funding.  
![Platform Donation](images/screenshots/user-stories-platform-donate.png)

- As a donor, I want to send a “Thank You” donation directly to shelters.  
![Thank You Donation](images/screenshots/user-stories-thankyou-donate.png)

- As a donor, I want to see platform balances.  
![Balance Page](images/screenshots/user-stories-balance.png)

---

## Shelter / Volunteer

- As a shelter volunteer, I want to create a support case.  
![Create Case](images/screenshots/user-stories-shelter-support.png)

- As a shelter volunteer, I want to submit proof.  
![Submit Proof](images/screenshots/user-stories-shelter-proof.png)

---

## Admin

- As an admin, I want to approve funding requests.  
![Admin Case Approval](images/screenshots/user-stories-admin-case-approval.png)

- As an admin, I want to close cases after reviewing evidence.  
![Admin Close Case](images/screenshots/user-stories-admin-close-case.png)