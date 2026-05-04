# TESTING.md — OpenPaws (Manual Testing)

Manual tests completed for the **OpenPaws Django project**.  
Testing verifies that the main user journeys work correctly, including public browsing, shelter case workflow, admin moderation, and Stripe payment integration.

The purpose of testing was to confirm that the application meets the expected project requirements such as CRUD functionality, user permissions, validation rules, and relational database behaviour.

---

# 1. Test Environment

- **Local URL:** http://127.0.0.1:8000/
- **Framework:** Django 4.2.x
- **Database:** SQLite (db.sqlite3)
- **Browser:** Safari (macOS)
- **Stripe:** Test Mode (Stripe Checkout)

---

# 2. Test Accounts / Roles Used

### Public User

- Not logged in
- Can browse public pages

### Shelter Owner

- Authenticated user linked to a Shelter record
- Can submit proof for their own cases

### Admin

- Django superuser
- Access to `/admin`
- Can approve cases and manage system data

---

# 3. Evidence Screenshots

All screenshots are stored in:

# TESTING.md — OpenPaws (Manual Testing)

Manual tests completed for the **OpenPaws Django project**.  
Testing verifies that the main user journeys work correctly, including public browsing, shelter case workflow, admin moderation, and Stripe payment integration.

The purpose of testing was to confirm that the application meets the expected project requirements such as CRUD functionality, user permissions, validation rules, and relational database behaviour.

---

# 1. Test Environment

- **Local URL:** http://127.0.0.1:8000/
- **Framework:** Django 4.2.x
- **Database:** SQLite (db.sqlite3)
- **Browser:** Safari (macOS)
- **Stripe:** Test Mode (Stripe Checkout)

---

# 2. Test Accounts / Roles Used

### Public User

- Not logged in
- Can browse public pages

### Shelter Owner

- Authenticated user linked to a Shelter record
- Can submit proof for their own cases

### Admin

- Django superuser
- Access to `/admin`
- Can approve cases and manage system data

---

# 3. Evidence Screenshots

All screenshots are stored in:
images/screenshots/

---

# 4. Manual Test Cases

Legend:

- **PASS** = works as expected
- **FAIL** = issue detected
- **N/A** = not applicable

---

# A) Navigation, Pages, Static Files

| ID  | Test                    | Steps                                           | Expected                       | Actual        | Result | Evidence                                 |
| --- | ----------------------- | ----------------------------------------------- | ------------------------------ | ------------- | ------ | ---------------------------------------- |
| T01 | Home page loads         | Open `/`                                        | Home page loads without errors | Home loads    | PASS   | images/screenshots/t01-home-loads.png    |
| T02 | Shelters list loads     | Open `/shelters/`                               | Shelter list displays          | List displays | PASS   | images/screenshots/t02-shelters-list.png |
| T03 | Cases list loads        | Open `/cases/`                                  | Case list displays             | List displays | PASS   | images/screenshots/t03-cases-list.png    |
| T04 | Navigation links work   | Click Home / Shelters / Cases / Balance / Admin | Correct pages load             | Pages load    | PASS   | images/screenshots/t04-nav-links.png     |
| T05 | Static CSS loads        | Refresh page                                    | Styling appears correctly      | CSS applied   | PASS   | images/screenshots/t05-css-loaded.png    |
| T06 | No 404 for static files | Check DevTools network tab                      | No `/static/...` errors        | No 404 errors | PASS   | images/screenshots/t06-no-static-404.png |

---

# B) Cases Workflow — Status Flow + Proof

Workflow:

OPEN → PROCESSING → AWAITING_REVIEW → CLOSED

| ID  | Test                                     | Steps                                         | Expected                                       | Actual             | Result | Evidence                                                                                                                                                                  |
| --- | ---------------------------------------- | --------------------------------------------- | ---------------------------------------------- | ------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T07 | Create Case (OPEN default)               | Create case in admin or shelter flow          | Status defaults to OPEN                        | OPEN               | PASS   | images/screenshots/t07-open-case.png, images/screenshots/t07-open-case-form.png                                                                                           |
| T08 | Approve Case sets PROCESSING             | Admin sets approved_amount >0                 | Status becomes PROCESSING                      | Updated correctly  | PASS   | images/screenshots/t08-processing.png                                                                                                                                     |
| T09 | 14-day deadline created                  | Case enters PROCESSING                        | `processing_started_at` and `proof_due_at` set | Fields created     | PASS   | images/screenshots/t09-proof-deadline.png                                                                                                                                 |
| T10 | Proof form visible to shelter owner      | Open case detail as shelter owner             | Proof form visible only for owner              | Correct visibility | PASS   | images/screenshots/t10-proof-form-visibility.png, images/screenshots/t10-proof-form-visibility-2.png                                                                      |
| T11 | Submit proof changes to AWAITING_REVIEW  | Shelter submits proof link                    | Status updates + timestamp saved               | Updated correctly  | PASS   | images/screenshots/t11-before-proof-submission.png, images/screenshots/t11-proof-submission-new-status.png, images/screenshots/t11-from-processing-to-awaiting-review.png |
| T12 | Cannot submit proof in wrong status      | Attempt proof submission when OPEN/CLOSED     | Validation blocks action                       | Blocked            | PASS   | images/screenshots/t12-before-proof-blocked-wrong-status.png                                                                                                              |
| T13 | Cannot set PROCESSING without approval   | Admin sets PROCESSING without approved_amount | Validation prevents save                       | Prevented          | PASS   | images/screenshots/t13-processing-without-approval-blocked.png                                                                                                            |
| T14 | Cannot set AWAITING_REVIEW without proof | Admin sets AWAITING_REVIEW without proof_link | Validation prevents save                       | Prevented          | PASS   | images/screenshots/t14-awaiting-review-without-proof-blocked.png                                                                                                          |
| T15 | Cannot close case without proof          | Admin attempts CLOSED without proof           | Validation blocks closing                      | Prevented          | PASS   | images/screenshots/t15-close-without-proof-blocked.png                                                                                                                    |
| T16 | Case closes successfully                 | Admin closes case with proof                  | `closed_at` timestamp set                      | Closed             | PASS   | images/screenshots/t16-closed-success.png                                                                                                                                 |

---

# C) Trust Points

Trust points reflect successful case completion.

| ID  | Test                                 | Steps        | Expected                      | Actual  | Result | Evidence                                |
| --- | ------------------------------------ | ------------ | ----------------------------- | ------- | ------ | --------------------------------------- |
| T17 | Trust points update when case closes | Close a case | Shelter trust_points increase | Updated | PASS   | images/screenshots/t17-trust-points.png |

---

# D) Payments — Stripe Checkout

Donation types:

- PLATFORM → platform balance
- THANK_YOU → directed to shelter

| ID  | Test                                 | Steps                            | Expected                       | Actual           | Result | Evidence                                                                                                                        |
| --- | ------------------------------------ | -------------------------------- | ------------------------------ | ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| T18 | Balance page loads                   | Open `/payments/balance/`        | Balance values displayed       | Loads correctly  | PASS   | images/screenshots/t18-balance-page-1.png, images/screenshots/t18-balance-page-2.png, images/screenshots/t18-balance-page-3.png |
| T19 | Platform donate page loads           | Open `/payments/donate/`         | Donation form visible          | Form shown       | PASS   | images/screenshots/t19-donate-platform-page.png                                                                                 |
| T20 | Thank You page loads                 | Open `/payments/thank-you/<id>/` | Thank-you form displayed       | Form shown       | PASS   | images/screenshots/t20-thank-you-page.png                                                                                       |
| T21 | Stripe checkout opens (Platform)     | Submit donation                  | Redirect to Stripe Checkout    | Checkout opens   | PASS   | images/screenshots/t21-stripe-checkout-platform.png                                                                             |
| T22 | Stripe checkout opens (Thank You)    | Submit thank-you donation        | Redirect to Stripe Checkout    | Checkout opens   | PASS   | images/screenshots/t22-stripe-checkout-thankyou-1.png, images/screenshots/t22-stripe-checkout-thankyou-2.png                    |
| T23 | Donation record saved                | View admin donations             | Record saved with correct data | Correct record   | PASS   | images/screenshots/t23-donation-record-admin.png                                                                                |
| T24 | Thank You donation linked to shelter | View THANK_YOU donation          | Shelter field populated        | Linked correctly | PASS   | images/screenshots/t24-thankyou-linked-shelter.png                                                                              |

Note:  
Stripe webhooks can automatically confirm payment events in production.  
In this project Stripe Checkout sessions are successfully created and donation records are stored in the database using **Stripe test mode**.

---

# E) Permissions & Security

| ID  | Test                                | Steps                          | Expected               | Actual          | Result | Evidence                                                                                                                           |
| --- | ----------------------------------- | ------------------------------ | ---------------------- | --------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| T25 | Public can browse pages             | Open site not logged in        | Pages accessible       | Accessible      | PASS   | images/screenshots/t25-public-browse-1.png, images/screenshots/t25-public-browse-2.png, images/screenshots/t25-public-browse-3.png |
| T26 | Only shelter owner can submit proof | Submit proof as different user | Action blocked         | Blocked         | PASS   | images/screenshots/t26-proof-owner-only.png                                                                                        |
| T27 | Admin panel requires login          | Open `/admin` logged out       | Redirect to login page | Redirect occurs | PASS   | images/screenshots/t27-admin-login-required.png                                                                                    |

---

# 5. Bugs Found & Fixes

| Bug                                   | Location             | Cause                                                 | Fix                                            |
| ------------------------------------- | -------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| NoReverseMatch for `payments:balance` | Navigation           | URL not defined                                       | Added payments URL route                       |
| NoReverseMatch for donate page        | Case detail template | Missing URL                                           | Added donation views and routes                |
| Stripe AuthenticationError            | Payment checkout     | Missing Stripe key                                    | Added `STRIPE_SECRET_KEY` environment variable |
| Incorrect proof status name           | Case workflow        | Used `AWAITING_APPROVAL` instead of `AWAITING_REVIEW` | Updated form logic                             |

---

# 6. Final Confirmation Checklist

- [x] All main pages load correctly
- [x] Status workflow works (OPEN → PROCESSING → AWAITING_REVIEW → CLOSED)
- [x] Proof submission restricted to shelter owner
- [x] Admin cannot close case without proof
- [x] Deadline fields populate correctly
- [x] Stripe checkout opens successfully
- [x] Donation records save correctly
- [x] Balance page calculations display correctly
- [x] Screenshots stored in `images/screenshots/`

---

# 7. Sign-off

Manual testing completed by: **Hanna Greentree**  
Date: **10 March 2026**  
Environment: Local development (Django 4.2, SQLite, Safari)

---

# 8. Additional Testing

## CSS Validation

CSS was validated using:
https://jigsaw.w3.org/css-validator/

No critical errors were found after corrections.

---

## Accessibility Testing

Accessibility was tested using:
https://www.accessibilitychecker.org

The site meets basic accessibility expectations including:

- readable font sizes
- colour contrast
- keyboard navigation support
- responsive design

---

## Cross-Browser Testing

The application was tested in:

- Safari (primary browser)
- Chrome (basic verification)

No major issues were detected.
