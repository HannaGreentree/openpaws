# OpenPaws — The most Transparent Animal Rescue Support Platform

OpenPaws is a **full-stack Django web application** designed to provide a fast way for animal shelters and independent volunteers in Ukraine to raise funds for the animals they care about.

The platform allows shelters to request financial support for specific needs such as food, medical treatment, or parasite treatments.

To request help, shelters must first be **registered on the platform and authorised by the admin**. Visitors can support authorised shelters and volunteers by donating through the platform.

Every "closed" case brings shelter 1 positive point.

Once a shelter makes a help request, the platform can provide funds for that case.

There are **two ways to support animal shelters**:

- by donating to the platform and being able to see evidence of how the money is spent
- by sending money directly to shelters using the **“Thank You”** donation option

- As more positive points user see next to each shelter as more credible it is

A key principle of the platform is **transparency**.

Transparency is the core idea behind OpenPaws.

Every funded case must include proof showing how the donated money was used.  
This may include receipts, images of the products, invoices, and the most important it should include the link to social media publications demonstrating that the funds helped animals.

By requiring this evidence before a case can be closed, the platform helps ensure that donations remain accountable and traceable.

OpenPaws - Bank of Animals

---

## Platform Concept

OpenPaws is a transparency-based animal aid platform.

It brings together animal shelters and private rescuers who are willing to clearly show:

- how much support they received
- what the money was spent on
- what result was achieved

The goal of the platform is to help donors feel safer, more confident, and more willing to support real animal rescue work.

By connecting donors with shelters through a transparent system, OpenPaws aims to rebuild trust between people who want to help animals and organisations providing that help.

---

# Project Purpose

The goal of this project is to demonstrate a **Full Stack MVC Django application** that:

- stores and manipulates relational data
- allows user interaction through forms
- processes payments using Stripe
- demonstrates authentication, permissions and validation
- implements a clear workflow system for case funding
- provides transparency for donors

The project domain is **animal rescue support and donation transparency**.

---

# Vision

The vision of OpenPaws is to create a system where helping animals is based not only on kindness but also on trust.

By promoting transparency in rescue work, the platform aims to encourage more people to donate with confidence and help more shelters continue their lifesaving work.

A transparent system benefits everyone:

- donors gain confidence that their contributions are used responsibly
- shelters gain credibility through verified rescue work
- animals receive the support they urgently need

---

# Target Users

The application serves three types of users.

---

# Platform Philosophy

OpenPaws follows a simple principle:

Helping animals should be transparent.

Donors often hesitate because they are unsure whether organisations will use their money responsibly.

OpenPaws attempts to reduce this uncertainty by introducing a transparent case workflow where shelters must provide proof showing how funds were used.

This approach aims to create a system where:

- shelters demonstrate accountability
- donors can make informed decisions
- trust between supporters and rescue organisations can grow

---

### Public Users

Public visitors can:

- browse shelters
- browse rescue cases
- support animal shelters by donate money to the platform (admin approval needed)
- send “Thank You” donations that goes directly to shelters (no admin approval needed)
- see case progress and transparency information
- see all the reciepts
- see the platform balance and bank statements

Public users do not need to log in.

---

### Shelter / Volunteer Users

Approved shelters or volunteers can:

- create rescue cases
- request funding
- submit proof showing how funds were used

They cannot approve their own funding requests.

---

### Admin Users

Administrators can:

- approve case funding
- reject case funding (if shelter recieved 2 negative points recently)
- review proof submissions
- close or reject cases
- manage shelters
- manage donations
- control case workflow
- make "Thank you" payments from donors to shelters

---

# Core Project Idea

The main idea of the project is to make donations **transparent and traceable**.

Example scenario:

A shelter needs money for animals.

Example requests:

A) £300 — food for rescued cats  
B) £250 — surgery for a specific dog  
C) £100 — flea treatment

The shelter creates a case requesting funding.

Each case on OpenPaws represents a real need.

Cases may include requests for:

- emergency veterinary treatment
- food supplies for rescued animals
- parasite treatment
- transportation for rescued animals
- temporary shelter support

By presenting clear case descriptions and funding progress, donors can better understand how their support contributes to helping animals.

The case goes through the following workflow.

---

# Case Workflow

Cases follow a controlled process.
OPEN → PROCESSING → AWAITING_REVIEW → CLOSED

### OPEN

The shelter creates a case requesting funding.

### PROCESSING

Admin approves the case and funding begins.

### AWAITING REVIEW

The shelter uploads proof of how the money was used.

### CLOSED

Admin reviews the proof and closes the case.

This workflow ensures **transparency and accountability**.

---

# Technologies Used

### Main Technologies

The project uses the required technologies:

- HTML
- CSS
- JavaScript
- Python
- Django

### Backend

- Django 4.2
- Python

### Frontend

- Django Templates
- HTML5
- CSS3
- JavaScript

### Database

- SQLite (development database)

The system is designed so that PostgreSQL or MySQL could also be used.

### Payments

- Stripe Checkout (test mode)

### Development Tools

- Git
- GitHub
- VS Code
- Safari browser

---

# Django Apps

The project uses multiple Django apps to keep the system modular.

### core

Handles shared layout and main site pages.

### shelters

Handles shelter profiles and shelter pages.

### cases

Handles rescue cases and case workflow.

### payments

Handles Stripe payments and donation records.

### accounts

Handles authentication and user accounts.

This structure follows Django best practices and meets the **multiple apps requirement**.

---

# Database Design

The project uses a relational database with connected models.

### Shelter Model

Stores shelter information.

Fields include:

- name
- country
- city
- animals_count
- trust_points
- social_link

---

### Case Model

Stores rescue case requests.

Fields include:

- shelter
- title
- description
- amount_requested
- amount_funded
- approved_amount
- status
- proof_link
- proof_due_at
- proof_submitted_at
- created_at

Each case belongs to one shelter.

---

### Donation Model

Stores payment records.

Fields include:

- donation_type
- amount
- stripe_session_id
- paid
- user
- case
- shelter

Donation types:

- PLATFORM donation
- THANK YOU donation

---

# Relational Database Relationships

The database includes the following relationships:

- One Shelter → Many Cases
- One Case → Many Donations (this option currently not available)
- One Shelter → Many Thank You Donations

This demonstrates relational data modelling.

---

# CRUD Functionality

The project implements full CRUD functionality.

### Create

- create shelter records
- create cases
- create donation records

### Read

- browse shelters
- browse cases
- view case details
- view balances

### Update

- update case status
- update approved amounts
- submit proof links

### Delete

Admin can remove records through Django admin.

---

# Forms and Validation

Forms are implemented to allow users to create and update data.

Examples include:

- case creation
- proof submission
- donation forms

Validation ensures that:

- cases cannot enter PROCESSING without approval
- cases cannot enter AWAITING_REVIEW without proof
- cases cannot close without evidence

---

# Stripe Payment Integration

The project integrates Stripe Checkout.

Two donation types are implemented.

Third donation type which was mentioned previosly is currently disabled

### Platform Donations

Support the overall platform balance.

### Thank You Donations

Allow donors to support shelters directly; the platform is then obligated to transfer those specific funds to the shelter without further authorisation.

Stripe test mode is used as required by the project specification.

Donation records store Stripe session IDs and payment details.

---

# User Authentication

Authentication is implemented using Django’s built-in system.

User types include:

- admin users
- shelter users

Authentication ensures that:

- only authorised users can create cases
- only admin users can approve funding
- protected pages require login

---

# JavaScript Features

JavaScript is used to improve the user experience.

Examples include:

- mobile navigation menu toggle
- page animations
- interactive UI elements

---

# Security

The project follows security best practices.

Security measures include:

- secret keys stored in environment variables
- sensitive files excluded from Git
- DEBUG mode disabled in production
- passwords not stored in the repository

---

# Navigation and UX Design

The website includes a clear navigation structure.

Main pages include:

- Home
- Shelters
- Cases
- Balance
- Admin

The design ensures that users can easily understand:

- what the platform does
- how to browse shelters
- how to support cases

---

# Wireframes

Wireframes were created during the planning stage to visualise the structure and layout of the platform before development began.

The purpose of the wireframes was to design a clear and simple interface that allows users to easily understand:

- how to browse shelters
- how to view rescue cases
- how to support animals through donations
- how transparency information is presented

The wireframes helped guide the layout of the pages and the navigation structure of the platform.

---

## Home Page

The home page introduces the purpose of the platform and explains how OpenPaws provides transparent support for animal rescue organisations.

Main elements include:

- hero section explaining the platform
- explanation of transparency
- how the platform works
- navigation to shelters and cases

![Home Wireframe](images/screenshots/wireframe-home.png)

---

## Shelters Page

The shelters page displays organisations participating in the platform.

Users can:

- browse shelters
- see basic shelter information
- open shelter profiles
- view rescue cases created by shelters

![Shelters Wireframe](images/screenshots/wireframe-shelters.png)

---

## Shelter Profile Page

The shelter profile page shows detailed information about each organisation.

Information displayed includes:

- shelter location
- number of animals cared for
- trust points
- rescue cases created by the shelter
- option to send a "Thank You" donation

![Shelter Profile Wireframe](images/screenshots/wireframe-shelter-profile.png)

---

## Cases Page

The cases page lists rescue cases that request support.

Users can see:

- case title
- funding request
- funding progress
- case status

![Cases Wireframe](images/screenshots/wireframe-cases.png)

---

## Case Detail Page

The case detail page provides full information about a specific rescue request.

This includes:

- case description
- funding requested
- funding progress
- case workflow status
- proof of spending when the case is completed

![Case Detail Wireframe](images/screenshots/wireframe-case-detail.png)

---

## Donation Pages

Two donation flows are available in the platform.

### Platform Donation

Users can donate to the platform to support rescue cases.

![Platform Donation Wireframe](images/screenshots/wireframe-platform-donation.png)

---

### Thank You Donation

Users can send a direct donation to shelters as appreciation for their rescue work.

![Thank You Donation Wireframe](images/screenshots/wireframe-thankyou-donation.png)

---

## Balance Page

The balance page shows transparency information about platform funds.

Users can see:

- total platform donations
- allocated funds
- available balance
- total Thank You donations

![Balance Wireframe](images/screenshots/wireframe-balance.png)

---

The wireframes helped guide the visual layout and ensured that the platform remained focused on its core principle: **transparent support for animal rescue organisations**.

---

# Testing

Manual testing was performed to verify functionality.

Testing covered:

- page loading
- navigation
- case workflow
- validation rules
- payment checkout
- database records
- permissions

Full testing documentation is included in:
TESTING.md

Screenshots are stored in:
images/screenshots/

---

Great idea, Anna 👍
A **Known Bugs section** is something tutors expect because it shows **honest evaluation and testing awareness**. It also helps meet requirements around **testing and project reflection**.

Below is a **professional version you can paste into your README.md**.

Place this section **after “Testing” and before “Deployment”**.

---

# Known Bugs

During development and testing, several issues were identified. Most were resolved during development, but a few limitations remain.

---

## 1. Case Donations Per Case (Currently Disabled)

The system design allows for **multiple donations to be linked to a specific case**, but this feature is currently disabled.

At the moment:

- donations are made to the **platform balance**
- admin then allocates funds to approved cases

This approach was chosen to simplify the workflow and maintain platform control over funding approvals.

Future versions may allow **direct donations to specific cases**.

---

## 2. Thank You Donations Manual Transfer

“Thank You” donations are intended to go directly to shelters.

Currently:

- the payment is processed through Stripe
- the admin must manually transfer the amount to the shelter

This limitation exists because automatic Stripe webhooks and payout automation were not implemented in this version.

Future improvements may include **automated payout systems**.

---

## 3. Trust Points Display

Trust points increase when cases are successfully completed.

Currently:

- the trust score increases when a case is closed
- there is no separate visual explanation for users about how trust points are calculated

Future improvements may include a **clear trust score explanation section** on shelter profiles.

---

## 4. Case Status Updates

The case workflow follows the required process:

OPEN → PROCESSING → AWAITING_REVIEW → CLOSED

During early development, cases could occasionally skip workflow steps if values were modified manually in the admin panel.

Additional validation was added to prevent this during normal platform usage.

---

# Fixed Bugs During Development

Several issues were identified and fixed during development.

---

### Migration File Accidentally Deleted

At one point a migration file was accidentally removed during development.

This was resolved by:

- restoring the migration folder
- running migrations again
- verifying database structure

---

### Template Naming Issue

Initially some templates were named incorrectly, causing Django errors such as:

```
TemplateDoesNotExist
```

This issue was resolved by ensuring that:

- templates matched view references
- template folders followed Django conventions

---

### Stripe Payment Testing

During early Stripe testing:

- incorrect session configuration caused payment errors

This was resolved by:

- verifying Stripe test keys
- confirming correct redirect URLs

---

# Future Improvements

Some improvements planned for future versions include:

- automated Stripe webhook handling
- direct case funding
- shelter dashboards
- improved transparency visualisation
- automated donation allocation

---

# Known Bugs

During development and testing, several issues were identified. Most were resolved during development, but a few limitations remain.

## 1. Case Donations Per Case (Currently Disabled)

The system design allows for multiple donations to be linked to a specific case, but this feature is currently disabled.
At the moment:

- donations are made to the platform balance
- admin then allocates funds to approved cases

This approach was chosen to simplify the workflow and maintain platform control over funding approvals.
Future versions may allow direct donations to specific cases.

## 2. Thank You Donations Manual Transfer

“Thank You” donations are intended to go directly to shelters.
Currently:

- the payment is processed through Stripe
- the admin must manually transfer the amount to the shelter

This limitation exists because automatic Stripe webhooks and payout automation were not implemented in this version.
Future improvements may include automated payout systems.

## 3. Trust Points Display

Trust points increase when cases are successfully completed.

Currently:

- the trust score increases when a case is closed
- there is no separate visual explanation for users about how trust points are calculated

Future improvements may include a clear trust score explanation section on shelter profiles.

## 4. Case Status Updates

The case workflow follows the required process:

OPEN → PROCESSING → AWAITING_REVIEW → CLOSED

During early development, cases could occasionally skip workflow steps if values were modified manually in the admin panel.

Additional validation was added to prevent this during normal platform usage.

# Fixed Bugs During Development

Several issues were identified and fixed during development.

## Migration File Accidentally Deleted

At one point a migration file was accidentally removed during development.

This was resolved by:

- restoring the migration folder
- running migrations again
- verifying database structure

## Template Naming Issue

Initially some templates were named incorrectly, causing Django errors such as:

TemplateDoesNotExist
This issue was resolved by ensuring that:

- templates matched view references
- template folders followed Django conventions

## Stripe Payment Testing

During early Stripe testing:

- incorrect session configuration caused payment errors
  This was resolved by:
- verifying Stripe test keys
- confirming correct redirect URLs

## Future Improvements

Some improvements planned for future versions include:

- automated Stripe webhook handling
- direct case funding
- shelter dashboards
- improved transparency visualisation
- automated donation allocation

# Deployment

The project was deployed to a cloud hosting platform.

Deployment process included:

- pushing the repository to GitHub
- configuring environment variables
- installing dependencies
- running migrations
- configuring static files

The deployed version was tested to ensure it matches the development version.

---

# Version Control

**I forgot about this to be honest and it was too late when I realised it.**

Git and GitHub were used throughout development.

Version control provides:

- commit history
- development documentation
- backup of project progress

Regular commits were made during development.

---

# Code Quality

The project follows clean code principles.

Examples include:

- clear file structure
- readable Python functions
- separation of logic between models, views and templates
- consistent URL structure

---

# Transparency Principles

The OpenPaws platform is built around several transparency principles:

- rescue cases must clearly explain what funding is requested for
- funding approvals are controlled by administrators
- shelters must provide proof showing how funds were used
- completed cases contribute to shelter trust points

Trust points help visitors identify shelters that have successfully completed transparent rescue cases.

---

# Future Improvements

Possible improvements include:

- shelter self-registration with admin approval
- improved shelter dashboards
- automatic Stripe webhooks
- improved case progress visualisation
- notification system for case updates

---

# Contact

If you are a shelter, volunteer rescuer, donor, or supporter who would like to learn more about the OpenPaws platform, you are welcome to get in touch.

Questions, suggestions, and feedback are always appreciated.

The platform aims to build a community of people who care about animals and support transparent rescue work.

---

## Deployment

The project code is stored on GitHub, and the live application is deployed on Render.

- GitHub was used for version control and project documentation.
- Render was used to deploy the live Django application for public access and testing.

---

# Credits

Resources used during development:

- Django Documentation
- Stripe Documentation
- Python Documentation

---

# Author

Hanna Greentree

Full Stack Web Development Project












## User Stories

The OpenPaws platform was designed around several user roles and their needs.

---

### Public Visitor

A public visitor is someone who wants to help animals but may not know which organisation to trust.

**User Story**

> As a visitor, I want to browse shelters and cases so that I can understand where help is needed.

![Home Page](images/user-stories/user-home.png)

---

**User Story**

> As a visitor, I want to view shelters so I can learn about organisations caring for animals.

![Shelters Page](images/user-stories/user-shelters.png)

---

**User Story**

> As a visitor, I want to view details about a shelter so I can understand their work and see their rescue cases.

![Shelter Profile](images/user-stories/user-shelter-profile.png)

---

**User Story**

> As a visitor, I want to browse rescue cases so I can see what support animals need.

![Cases Page](images/user-stories/user-cases.png)

---

**User Story**

> As a visitor, I want to see details of a rescue case so I can understand what the requested funds will be used for.

![Case Detail](images/user-stories/user-case-detail.png)

---

### Donor

A donor wants to support rescue organisations in a transparent way.

**User Story**

> As a donor, I want to donate to the platform so that rescue cases can receive funding.

![Platform Donation](images/user-stories/user-platform-donate.png)

---

**User Story**

> As a donor, I want to send a “Thank You” donation directly to shelters so I can support their rescue work.

![Thank You Donation](images/user-stories/user-thankyou-donate.png)

---

**User Story**

> As a donor, I want to see platform balances so that I can understand how donations are used.

![Balance Page](images/user-stories/user-balance.png)

---

### Shelter / Volunteer

Shelters and volunteers can create cases and provide evidence of how funds are used.

**User Story**

> As a shelter volunteer, I want to create a rescue case so that I can request funding for animals in need.

![Create Case](images/user-stories/shelter-create-case.png)

---

**User Story**

> As a shelter volunteer, I want to submit proof showing how the funds were spent so that donors can see the results.

![Submit Proof](images/user-stories/shelter-submit-proof.png)

---

### Admin

Admins review cases to ensure transparency and responsible use of donations.

**User Story**

> As an admin, I want to approve funding requests so that legitimate rescue cases can receive support.

![Admin Case Approval](images/user-stories/admin-case-approval.png)

---

**User Story**

> As an admin, I want to close cases after reviewing evidence so that donors can see that funds were used correctly.

![Admin Close Case](images/user-stories/admin-close-case.png)
