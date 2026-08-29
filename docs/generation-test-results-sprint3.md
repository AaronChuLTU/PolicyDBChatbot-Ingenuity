# Generation Test Results - Sprint 3 (PCOIS2-51)

**Date run:** 2026-08-30  
**Model:** Ollama / qwen3  
**Retrieval:** hybrid (BM25 + vector + cross-encoder rerank), threshold 0.5  
**Questions:** 16  |  **Reached the model:** 7  |  **Flagged for review:** 4

Live end-to-end run: real Postgres, real retrieval, real model.
`test_generation.py` covers routing logic with stubs and never calls
the model, so this is the first check of whether the model actually
obeys the prompt rules.

A flag is a place to look, not a verdict. Automation narrows the
search; the Verdict column below is filled in by a human comparing
each answer against the excerpts it was given.

## Summary

- Routing failures: **1**
- Responses with unsupported numbers or terms: **3**
- Clean: **12/16**

## Results

| # | Question | Score | Status | Reached model | Flags | Verdict |
|---|---|---|---|---|---|---|
| 1 | What academic dress do graduands wear at a graduation ceremony? | 0.999 | success | yes | UNSUPPORTED TERMS: depending, gowns |  |
| 2 | Who is entitled to wear a doctoral gown? | 0.902 | low_confidence | no | - |  |
| 3 | Can I keep my academic gown after the ceremony? | 0.797 | low_confidence | no | - |  |
| 4 | What happens if a student fails the same subject more than once? | 0.985 | success | yes | - |  |
| 5 | Can I appeal an academic progression decision? | 0.882 | success | yes | RULE 4 (no citations in answer): "Academic Progression Policy" |  |
| 6 | What are the stages of academic progression review? | 0.999 | success | yes | - |  |
| 7 | How do I apply for promotion to Associate Professor? | 0.977 | low_confidence | no | - |  |
| 8 | Who sits on the academic promotions committee? | 0.998 | success | yes | UNSUPPORTED TERMS: includes |  |
| 9 | What is the basis for academic promotion? | 0.991 | low_confidence | no | - |  |
| 10 | What qualifications must academic staff hold to teach a subject? | 0.999 | success | yes | - |  |
| 11 | Does a lecturer need a qualification higher than the course they teach? | 0.111 | out_of_scope | no | - |  |
| 12 | What are the English language requirements for admission? | 0.582 | low_confidence | no | - |  |
| 13 | Can I get credit for prior study when I apply? | 0.028 | out_of_scope | no | - |  |
| 14 | How are applications for admission assessed? | 0.795 | success | yes | ROUTING: expected low_confidence, got success; UNSUPPORTED TERMS: sure |  |
| 15 | How do I book a car parking permit on campus? | 0.000 | out_of_scope | no | - |  |
| 16 | What food is available at the campus cafe today? | 0.000 | out_of_scope | no | - |  |

## Answers and their excerpts

Each answer below is followed by the excerpts the model was given.
Read one against the other and record a verdict in the table above:
**grounded** (every claim traceable to an excerpt), **hallucinated**
(a claim that is not), or **wrong refusal** (the excerpts did answer
the question but the model declined).

### 1. What academic dress do graduands wear at a graduation ceremony?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 3.8s

**Answer:**

> Graduands wear the appropriate academic dress described in Part E, which includes specific gowns, hoods, stoles, and trenchers depending on their award. Graduands of Aboriginal and/or Torres Strait Islander descent may also opt to wear an additional stole in specified colours.

**Citations:**

- Academic Dress Policy - Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=208)

**Flags:**

- UNSUPPORTED TERMS: depending, gowns

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Dress Policy / Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent (score 0.999)

> (11) Graduands/graduates of Aboriginal and/or Torres Strait Islander descent may opt to wear, in addition to the appropriate academic dress described in Part E, a stole ten centimetres wide of the following colours: Aboriginal: equal bands of Jet Black, Saffron and Post Office red silks Torres Strait Islander: larkspur silk edged on each side with Juniper silk, each colour separated by a narrow band of black piping. (12) Graduands requiring one or both of these stoles should indicate this when registering to attend their ceremony.

**Excerpt 2** - Academic Dress Policy / Section 5 - Policy Statement (score 0.998)

> (3) The University will prescribe from time to time the academic dress to be worn on ceremonial occasions, including graduations and presentation ceremonies and such other occasions as the Council may specify, by: officers of the University, members of Council and other members of the University; and/or graduands or graduates of degrees and other awards of the University. (4) The colours used for gown facings, hoods or stoles for particular awards generally will reflect the discipline content of the award, rather than the specific award program or the academic unit that teaches the course. (5) Staff or students of Aboriginal and/or Torres Strait Islander descent who are entitled to wear academic dress may opt to wear also a stole in Aboriginal and/or Torres Strait Islander colours.

**Excerpt 3** - Academic Dress Policy / Section 3 - Scope (score 0.994)

> (2) This Policy applies to: all graduands/graduates and other recipients of La Trobe awards recognised in the Australian Qualifications Framework; all staff participating in graduation and presentation ceremonies of the University or in other events at which the wearing of academic dress is required or permitted.

**Excerpt 4** - Academic Dress Policy / Section 2 - Purpose (score 0.992)

> (1) This Policy prescribes: the core principles for the use of academic dress; the academic dress to be worn on ceremonial occasions of the University by various categories of staff, University Council (Council) members, and graduands/graduates and other recipients of University awards.

**Excerpt 5** - Academic Dress Policy / Preamble (score 0.992)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Dress Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Dress and Colour Protocols Part B - Requests for Changes or Additions to Academic Dress Part C - Recording of Academic Dress Requirements Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent Part E - Specific Academic Dress Requirements Staff, Council Members and Visitors Graduands/Graduates and Other Award Recipients Section 7 - Definitions Section 8 - Authority and Associated Information This is the current version of this document. To view historic versions, click the link in the document's navigation bar. Section 1 - Key Information Policy Type and Approval Body Administrative -  ...

</details>

---

### 2. Who is entitled to wear a doctoral gown?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.902  
- **Response time:** 3.0s

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Academic Dress Policy - Section 7 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Part E -  Specific Academic Dress Requirements (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)

---

### 3. Can I keep my academic gown after the ceremony?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.797  
- **Response time:** 3.0s

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 7 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=208)

---

### 4. What happens if a student fails the same subject more than once?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.985  
- **Response time:** 4.3s

**Answer:**

> If a student fails the same subject in a course for the second time, they will trigger Academic Progression Stage Two (AP2) - Support and Sanction. The student will be required to attend an academic recovery workshop in the next Progression Period, and their enrolment load will be restricted to a maximum of 45 credit points, unless they are enrolled in a thesis subject or a workplace-based subject.

**Citations:**

- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.985)

> Stage: Green Thresholds: Student has passed the subjects in which they are enrolled Communication or Intervention: No intervention or communication Stage: Recovery(AP1)- Yellow Thresholds: Triggered when a student fails one subject for the ﬁrst time other than a workplace-based subject Communication or Intervention: - AP1 support communication- Academic Recovery Module- Support from Library and Learning Services Teams Stage: Support and Sanction(AP2)- Amber Thresholds: Triggered when a student:- fails for the ﬁrst time any workplace-based subject, or- fails 50% or more of their enrolled credit points for the first time, or- fails the same subject in a course for a second time, or- triggers AP1 more than three times. Communication or Intervention: - AP2 support communication requiring attendance at academic recovery workshop (all students)- Attendance at workshop required to lift any rest ...

**Excerpt 2** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.188)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 3** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.078)

> the consequences of continued academic failure; their options for appealing the decision to place conditions on their enrolment (see Part C) and the availability of independent advocacy support. (17) During the academic recovery workshop students are required to engage in self-assessment and action plan generation. They may seek additional advice where required from ASK La Trobe, a Student Advisor or their Course Coordinator. (18) Students who trigger AP3 receive a communication: advising that they have reached the final stage of academic progression monitoring and why; inviting them to make a written submission within 10 business days to show cause as to why they should not be excluded from their course, and providing guidance about how this is done; if they are an international student, stating the potential impact on their CoE and visa; outlining their options for appealing the propos ...

**Excerpt 4** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.020)

> (13) Students enrolled in thesis subjects worth 30, 45 or 60 credit points will not have an enrolment restriction or cancellation applied to these subjects. (14) Students who trigger AP1 receive a communication that includes: an explanation of why they have triggered this progression stage; a request to engage with supports as identified through completion of the Support Survey in the academic recovery module; an explanation of the potential consequences of continued academic failure, including enrolment sanctions and course exclusion. (15) Student engagement with academic support at AP1 is tracked for consideration in future academic progression stages as appropriate. (16) Students who trigger AP2 receive a communication advising: why they have triggered this progression stage; that their enrolment load in the next Progression Period will be restricted to a maximum of 45 credit points,  ...

**Excerpt 5** - Academic Progression Review Policy / Section 5 - Policy Statement (score 0.003)

> (4) The University is committed to supporting all students, irrespective of their educational background, entry pathway, mode or place of study to achieve their goals in higher education. In terms of this Policy this means that: students’ academic performance is reviewed in a consistent, phased and equitable way; students who are experiencing difficulties are identified as early as possible through formal progression monitoring and additional measures such as early assessment in all subjects, as outlined in the Assessment Policy ; interventions at each stage of academic progression monitoring provide students with multiple avenues for academic and non-academic support and clear information about the consequences of failing to follow agreed action plans. (5) Trends in rates of retention, progression and completion of specific student cohorts are monitored to fulfil legislated reporting re ...

</details>

---

### 5. Can I appeal an academic progression decision?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.882  
- **Response time:** 4.0s

**Answer:**

> Yes, students may appeal a decision to exclude them from their course under the Academic Progression Policy through the University Appeals Committee (UAC). Students must apply for such a review within twenty (20) business days of notification of the decision. The decision of the UAC is the final decision of the University.

**Citations:**

- Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=220)

**Flags:**

- RULE 4 (no citations in answer): "Academic Progression Policy"

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.882)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 2** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.853)

> the consequences of continued academic failure; their options for appealing the decision to place conditions on their enrolment (see Part C) and the availability of independent advocacy support. (17) During the academic recovery workshop students are required to engage in self-assessment and action plan generation. They may seek additional advice where required from ASK La Trobe, a Student Advisor or their Course Coordinator. (18) Students who trigger AP3 receive a communication: advising that they have reached the final stage of academic progression monitoring and why; inviting them to make a written submission within 10 business days to show cause as to why they should not be excluded from their course, and providing guidance about how this is done; if they are an international student, stating the potential impact on their CoE and visa; outlining their options for appealing the propos ...

**Excerpt 3** - Academic Progression Review Policy / Section 4 - Key Decisions (score 0.572)

> Key Decisions: Decision to restrict a student’s enrolment load in a course or exclude a student from a course after failure to satisfactorily show cause Role: Academic Progression Officer: nominated senior academic (Level C or higher)

**Excerpt 4** - Academic Progression Review Policy / Part C - Review (score 0.344)

> (26) Students may seek a review of a decision made to exclude them from their course under this Policy through the University Appeals Committee (UAC) under the provisions of the Academic Progress Statute 2010 . Students must apply for such a review within twenty (20) business days of notification of the decision (note this timeframe differs from that outlined in the Statute to fulfil requirements under ESOS legislation). (27) The decision of the UAC is the final decision of the University. The University Ombudsman is not able to review decisions made by the UAC, however, students who have concerns about any aspect of the process or the way in which this Policy has been applied (as opposed to the decision or outcome) may lodge a complaint with the University Ombudsman. (28) Students who remain dissatisfied after all University processes have been exhausted may choose to lodge a complaint  ...

**Excerpt 5** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.172)

> (21) Following the final outcome decision a communication is sent to the student advising: that they may remain enrolled in the course but may be subject to a credit-point restriction (equal to 45 credit points or less), or; that they are to be excluded from the course for a period of nine months, calculated from the date of the notification letter; if they are an international student, that they should seek advice regarding the impact on their CoE and visa; their options for appealing the outcome and the availability of independent advocacy support. (22) Any enrolment restrictions imposed at AP3 will take into account the circumstances of students who: have reached the maximum duration of study for their course, or the Expected Duration (international students) (see Enrolment Procedure – Variations ); are enrolled in an accredited course. (23) Records of all academic progression communi ...

</details>

---

### 6. What are the stages of academic progression review?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 4.6s

**Answer:**

> If a student is enrolled in a workplace-based subject and triggers Academic Progression Stage Two (AP2), their enrolment will be reviewed by their Course Coordinator to determine if an enrolment load restriction should be applied. If they are an international student, the potential impact on their CoE and visa will be communicated. They are required to attend an academic recovery workshop facilitated by Student Advisors in the next Progression Period. The enrolment sanction can be lifted following attendance/engagement with the academic recovery workshop.

**Citations:**

- Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Academic Progression Review Policy (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.999)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 2** - Academic Progression Review Policy / Academic Progression Review Policy (score 0.998)

> Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Monitoring and Determining Academic Progression Part B - Details of Academic Progression Stages Academic Progression Stage One – Recovery Academic Stage Two – Support and Sanction Academic Progression Stage Three – Show Cause and Course Exclusion Course Transfers and New Courses Part C - Review Part D - Monitoring Section 7 - Definitions Section 8 - Authority and Associated Information

**Excerpt 3** - Academic Progression Review Policy / Preamble (score 0.996)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Progression Review Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Monitoring and Determining Academic Progression Part B - Details of Academic Progression Stages Academic Progression Stage One – Recovery Academic Stage Two – Support and Sanction Academic Progression Stage Three – Show Cause and Course Exclusion Course Transfers and New Courses Part C - Review Part D - Monitoring Section 7 - Definitions Section 8 - Authority and Associated Information This is the current version of this document. To view historic versions, click the link in the document's navigation bar. Section 1 - Key Information Policy Type and Approval Body Academic - Academic Board Accountabl ...

**Excerpt 4** - Academic Progression Review Policy / Section 5 - Policy Statement (score 0.946)

> (4) The University is committed to supporting all students, irrespective of their educational background, entry pathway, mode or place of study to achieve their goals in higher education. In terms of this Policy this means that: students’ academic performance is reviewed in a consistent, phased and equitable way; students who are experiencing difficulties are identified as early as possible through formal progression monitoring and additional measures such as early assessment in all subjects, as outlined in the Assessment Policy ; interventions at each stage of academic progression monitoring provide students with multiple avenues for academic and non-academic support and clear information about the consequences of failing to follow agreed action plans. (5) Trends in rates of retention, progression and completion of specific student cohorts are monitored to fulfil legislated reporting re ...

**Excerpt 5** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.711)

> (13) Students enrolled in thesis subjects worth 30, 45 or 60 credit points will not have an enrolment restriction or cancellation applied to these subjects. (14) Students who trigger AP1 receive a communication that includes: an explanation of why they have triggered this progression stage; a request to engage with supports as identified through completion of the Support Survey in the academic recovery module; an explanation of the potential consequences of continued academic failure, including enrolment sanctions and course exclusion. (15) Student engagement with academic support at AP1 is tracked for consideration in future academic progression stages as appropriate. (16) Students who trigger AP2 receive a communication advising: why they have triggered this progression stage; that their enrolment load in the next Progression Period will be restricted to a maximum of 45 credit points,  ...

</details>

---

### 7. How do I apply for promotion to Associate Professor?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.977  
- **Response time:** 3.5s

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Academic Promotions Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

---

### 8. Who sits on the academic promotions committee?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.998  
- **Response time:** 5.0s

**Answer:**

> The academic promotions committee for promotion to Levels B and C includes the Deputy Vice-Chancellor (Research and Innovation) as Chair (ex officio), Deputy Vice-Chancellor (Academic) or nominee (ex officio), Pro Vice-Chancellor (Research) or nominee (ex officio), Deputy Provost (ex officio), Chair of Academic Board or nominee from the Academic Board membership (ex officio), up to five academic members at Academic Level D or E nominated by the Vice-Chancellor, Chief People Officer or nominee as a non-voting observer, and one invited Level E academic who is external to La Trobe University. For promotion to Levels D and E, the committee includes the Provost as Chair (ex officio).

**Citations:**

- Academic Promotions Policy - Part D - Academic Promotions Committees (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

**Flags:**

- UNSUPPORTED TERMS: includes

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Part D - Academic Promotions Committees (score 0.998)

> Deputy Vice-Chancellor (Academic) (ex officio) Pro Vice-Chancellor (Research) (ex officio) Deputy Provost (ex officio) Chair of Academic Board (ex officio) up to five academic members at Academic Level E nominated by the Vice-Chancellor, in consultation with the Provost and Deans, selected to ensure expertise in teaching, academic service, and research; and a balance of broad disciplines, campuses and genders (appointed members) Chief People Officer or nominee as a non-voting observer to provide advice at the request of the Committee (in attendance) One invited Level E academic who is external to La Trobe University (appointed member) (58) The Academic Promotions Committees are deliberative committees that will base their decisions on the application provided, the case made by the applicant and the evidence provided to support the case. They will not take into account information that is ...

**Excerpt 2** - Academic Promotions Policy / Part D - Academic Promotions Committees (score 0.996)

> (51) The Vice-Chancellor will appoint the Academic Promotions Committees. (52) The Committees shall meet once per year. (53) The term of membership of appointed members shall be three years and retiring members shall not be eligible for direct re- appointment. Retiring members may be eligible for a one year extension to their appointment. (54) The Office of the Provost will provide administrative support to the Committees. (55) There will be two Academic Promotions Committees. Committee membership will depend on the academic level for which promotion is being sought. (56) For promotion to academic Levels B and C, the Academic Promotions Committee will comprise: Deputy Vice-Chancellor (Research and Innovation) as Chair (ex officio) Deputy Vice-Chancellor (Academic) or nominee (ex officio) Pro Vice-Chancellor (Research) or nominee (ex officio) Deputy Provost (ex officio) Chair of Academic  ...

**Excerpt 3** - Academic Promotions Policy / Part D - Academic Promotions Committees (score 0.993)

> (59) Disciplinary differences will be taken into account and, where possible, the Committees will refer to appropriate disciplinary norms when assessing applications. If there are matters that require clarification, additional information may be sought by the Committees from the Dean or other appropriate senior person with a knowledge of a particular discipline or specialist area. (60) The Academic Promotions Committees will provide recommendations to the Vice-Chancellor arising from each of their meetings. (61) The Vice-Chancellor is responsible for approving, or not approving, the recommendations of the Academic Promotions Committees. (62) The Vice-Chancellor will report promotions to the Academic Board and the wider University community through All Staff communications.

**Excerpt 4** - Academic Promotions Policy / Section 4 - Key Decisions (score 0.990)

> Key Decisions: Reviewing applications for promotion to Level B and Level C and providing recommendations. Role: Level B/C Academic Promotions Committee Key Decisions: Reviewing applications for promotion to Level D and Level E and providing recommendations. Role: Level D/E Academic Promotions Committee Key Decisions: Approving or not approving the recommendations of the Academic Promotions Committees. Role: Vice-Chancellor

**Excerpt 5** - Academic Promotions Policy / Part F - Special Cases (score 0.989)

> (89) The Executive Officer will ensure the application is considered by the Academic Promotions Committee as soon as practicable. (90) After reviewing the case, the Committee may recommend the payment of a retention allowance as an alternative to promotion. (91) For applications presented out of cycle and/or in exceptional circumstances, the Vice-Chancellor is responsible for approving any variations to the academic promotions process and the outcome of the application.

</details>

---

### 9. What is the basis for academic promotion?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.991  
- **Response time:** 3.4s

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Academic Promotions Policy (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

---

### 10. What qualifications must academic staff hold to teach a subject?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 3.9s

**Answer:**

> The policy requires that academic staff must be appropriately qualified for the level of their teaching responsibilities, and a robust framework for the assessment of Professional Equivalence is applied for teaching staff who do not possess the requisite qualification for a given level of teaching according to the Standards.

**Citations:**

- Academic Staff Qualifications Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 6 - Procedures (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=420)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Staff Qualifications Policy / Section 5 - Policy Statement (score 0.999)

> (6) The University ensures that its academic staff are appropriately qualified for the level of their teaching responsibilities. This means that: staff who are responsible for the recruitment of subject teaching staff are appropriately experienced and qualified themselves, and familiar with the relevant requirements under the Standards; staff with academic coordination duties are qualified at an appropriately high level and their recruitment is overseen by a senior member of the School; a robust framework for the assessment of Professional Equivalence is applied for teaching staff who do not possess the requisite qualification for a given level of teaching according to the Standards ; for staff who do not yet meet Professional Equivalence: the range of teaching duties allocated is appropriately limited until equivalence is reached; professional development plans and appropriate supervisi ...

**Excerpt 2** - Academic Staff Qualifications Policy / Section 5 - Policy Statement (score 0.999)

> robust records of all staff qualifications, assessments of professional equivalence, and professional development plans as appropriate, are maintained in University record-keeping systems. (7) Academic staff are expected to engage in scholarly activities that enhance course and subject design, the quality of their teaching and the fulfilment of their professional goals. This means that: staff must be actively engaged in scholarship activities that: maintain and advance disciplinary knowledge, including professional practice where relevant; inform and enhance pedagogical training and practice through continuous professional development in teaching and learning practice; maintain and advance disciplinary knowledge, including professional practice where relevant; inform and enhance pedagogical training and practice through continuous professional development in teaching and learning practic ...

**Excerpt 3** - Academic Staff Qualifications Policy / Section 6 - Procedures (score 0.971)

> (9) Refer to: Academic Staff Qualifications Procedure - Teaching ; Academic Staff Qualifications Procedure - Scholarship .

**Excerpt 4** - Academic Staff Qualifications Policy / Preamble (score 0.965)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Staff Qualifications Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Section 7 - Definitions Section 8 - Authority and Associated Information This is the current version of this document. You can provide feedback on this policy to the document author - refer to the Status and Details on the document's navigation bar. Section 1 - Key Information Policy Type and Approval Body Academic – Academic Board Accountable Executive – Policy Deputy Vice-Chancellor (Academic) Responsible Manager – Policy Pro Vice-Chancellor (Learning and Teaching) Review Date 29 April 2028 Section 2 - Purpose (1) This Policy outlines the ways in which La Trobe University ensures that its teaching staff ...

**Excerpt 5** - Academic Staff Qualifications Policy / Section 3 - Scope (score 0.645)

> (2) This Policy applies to all staff who teach students enrolled in La Trobe award courses, including students enrolled in La Trobe courses taught under an educational partnership agreement. (3) Graduate research supervision requirements for Doctoral and Master’s by research candidates are further outlined in the Graduate Research Supervision Policy . (4) This Procedure does not apply to the academic teaching staff of institutions in which students are undertaking study as part of a program of outbound student mobility or partner supervisors of students undertaking placements, internships or other forms of work integrated learning. The University assures itself that such individuals are appropriately qualified to teach and/or supervise La Trobe students through the provisions of the Educational Partnerships Policy and associated procedures. (5) Any exceptions or variations to specific re ...

</details>

---

### 11. Does a lecturer need a qualification higher than the course they teach?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.111  
- **Response time:** 0.7s
- **Note:** Scored 0.111 in PCOIS2-47 - expected to be filtered before generation

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

### 12. What are the English language requirements for admission?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.582  
- **Response time:** 3.6s

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Admissions Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=169)

---

### 13. Can I get credit for prior study when I apply?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.028  
- **Response time:** 0.7s
- **Note:** Corpus gap: credit rules live in the Credit Standard, not ingested. Scored 0.028, so should not reach the model

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

### 14. How are applications for admission assessed?

- **Status:** success  
- **Confidence:** medium  
- **Top rerank score:** 0.795  
- **Response time:** 4.5s
- **Note:** ACCEPTANCE TEST for PCOIS2-49. Retrieval hands this Academic Promotions text at 0.795, well above threshold. A fluent answer about promotion committees is a hallucination and a fail

**Answer:**

> Applications for admission are assessed based on entry requirements, which are approved by the Academic Board. The University ensures transparency and equity in selection processes, making sure entry requirements are equivalent for domestic and international applicants. Applicants who meet all entry requirements are eligible for consideration but are not guaranteed an offer. Admission is based on competitive selection, and entry into courses may have limited places available.

**Citations:**

- Academic Promotions Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=76)

**Flags:**

- ROUTING: expected low_confidence, got success
- UNSUPPORTED TERMS: sure

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Section 5 - Policy Statement (score 0.795)

> Academic staff will be provided with appropriate advice and support in the preparation of applications and will receive clear and timely feedback on the outcomes; Applications will be assessed on the evidence provided about the quality, outcomes and impact of contributions holistically across domains; Application and assessment will be based on demonstrated performance, relative to opportunity. Applications from under-represented groups will be actively encouraged; Evidence will be assessed over an academic staff member’s entire career, however more significance will be placed on achievements, outputs and impact in the period since last promotion or appointment to the current academic level; Applications will be judged on their merit, there are no quotas on the number of staff promoted annually. In the case of a successful promotion outcome, it is the responsibility of the relevant acade ...

**Excerpt 2** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.240)

> (21) The Committee will, in the context of the level for which promotion is applied, consider the appropriateness of levels and types of formal qualifications and/or substantial progress towards such qualifications or, where relevant consider and determine the equivalence of alternative qualifications and/or experience held by applicants. (22) Applicants will assess whether they are eligible for promotion and merit promotion with reference to the Minimum Standards for Academic Levels and the Academic Performance Framework . (23) Applicants are strongly encouraged to seek guidance and discuss their application with the following before making an application for promotion: Career Success Manager/Academic Reviewer/Head of Department Dean/Director of Centre/Institute An academic mentor (24) The Academic Promotions Committee will convene once per year to consider applications. The dates of Ac ...

**Excerpt 3** - Admissions Policy / Section 5 - Policy Statement (score 0.191)

> (6) The University ensures that its admission policies and procedures are robust, and that admitted students have appropriate preparation for study. This is achieved by: Academic Board approval of entry requirements, including General Admission Requirements; the granting of credit in accordance with the principles and conditions outlined in the Credit Standard; monitoring the success of student cohorts according to the basis of their admission, including the amount of credit granted, whether by the University or third parties; the maintenance of accurate, reliable, and secure admissions records and assurance of these processes through regular review. (7) Admission and selection processes are transparent, equitable and clearly communicated. This is achieved by ensuring that: entry requirements for individual courses are equivalent for domestic and international applicants, and for all off ...

**Excerpt 4** - Admissions Policy / Section 5 - Policy Statement (score 0.099)

> where quotas or limits on admission numbers are established for specific courses, indicative thresholds for entry for specific intakes are published on the University’s website. (8) The University encourages and supports participation from persons who have experienced disadvantage or are from a group underrepresented in higher education. This is achieved by the provision of: special entry access schemes and alternative entry programs, including pathways between Australian Qualifications Framework (AQF) levels; additional targeted programs for Aboriginal and Torres Strait Islander peoples, such as sub-quotas for designated courses and culturally appropriate pathway programs; opportunities for applicants to discuss any need they may have for Reasonable Adjustments to their course to accommodate a disability (as defined in this Policy), or ongoing health condition, before applying and/or pr ...

**Excerpt 5** - Admissions Policy / Preamble (score 0.095)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Admissions Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Section 7 - Definitions Section 8 - Authority and Associated Information This is the current version of this document. To view historic versions, click the link in the document's navigation bar. Section 1 - Key Information Policy Type and Approval Body Academic – Academic Board Accountable Executive – Policy Deputy Vice-Chancellor (Future Growth) Responsible Manager – Policy Director, Admissions and Scholarships Review Date 19 April 2027 Section 2 - Purpose (1) This Policy outlines the principles governing the eligibility and selection of applicants to coursework courses, including the use of entry requirements, the applica ...

</details>

---

### 15. How do I book a car parking permit on campus?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.000  
- **Response time:** 0.6s
- **Note:** Out-of-scope control - scored 0.000, must not reach the model

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

### 16. What food is available at the campus cafe today?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.000  
- **Response time:** 0.7s
- **Note:** Out-of-scope control - scored 0.000, must not reach the model

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

## Observations

## Observations

**1. The acceptance test result is more nuanced than a pass/fail.**
Question 14 was flagged as a routing failure, but reading the answer against
the excerpts shows the prompt worked as designed. The model was handed
Academic Promotions text at 0.795 and ignored it, answering instead from the
Admissions Policy excerpts that scored 0.191 and 0.099. Every claim traces to
those chunks. Rule 1 did its job.

**2. The real defect is citation integrity, and it is more serious.**
Because `build_citations()` filters to chunks scoring at or above 0.50, the
Admissions chunks the answer was actually built from were excluded, and the
only citation attached is "Academic Promotions Policy - Section 5". The
answer is correct; the citation points at an unrelated policy. For a system
whose stated purpose is source-referenced answers, a correct answer with a
wrong citation is worse than a refusal - it is confidently unverifiable, and
a user following the link finds a policy about staff promotion.

Two possible fixes, for whoever owns PCOIS2-50:
- Cite every chunk the model was shown, not only those above the threshold.
- Or have the model indicate which excerpts it used, and cite those.
The first is simpler and errs toward over-citing, which is the safer
direction.

**3. Over-refusal is the dominant failure mode: 5 of 12 in-scope questions.**
Questions 2, 3, 7, 9 and 12 returned low_confidence despite scores of 0.902,
0.797, 0.977, 0.991 and 0.582. Question 9 is the clearest case - "What is the
basis for academic promotion?" retrieved "Part B - Basis for Promotion" at
0.991, a section named after the question, and the model still declined.
Refusing is the safer direction to fail, but at this rate the chatbot
declines to answer a large share of legitimate questions, which undermines
its usefulness. Rule 2's list of refusal triggers is likely too broad,
particularly the clause about definitions and scope statements.

**4. Question 6 answered a different question, and no check caught it.**
Asked for the stages of academic progression review. Excerpt 1 lists them
explicitly (AP1 Recovery, AP2 Support and Sanction, AP3 Show Cause and Course
Exclusion), but the answer instead described AP2 mechanics, Course
Coordinator review and international student visa implications. The response
is grounded in the corpus but does not answer what was asked. No automated
flag fired, since the words used do appear somewhere in the excerpts. This is
a limitation of term-matching as a check: it detects invented content, not
irrelevant content.

**5. Two Rule 4 violations; one escaped detection.**
Question 5 wrote "under the Academic Progression Policy" into the answer body
(also a slight misnaming - the document is the Academic Progression Review
Policy). Question 1 wrote "described in Part E". The detection regex matches
"Part" followed by a digit but not by a letter, so the second was missed. The
pattern should be widened.

**6. The chunking defect is visible in generation, not just retrieval.**
Preamble chunks - containing the document's table of contents and site
navigation - appear in the excerpt set for questions 1 and 6. They consume
context slots that could hold substantive clauses, and question 6's answer
may have been influenced by the model reading a list of section headings as
content. This supports fixing the clean_and_chunk.py duplication defect
before expanding the corpus.

**7. Response times are acceptable.**
3-5 seconds per generated answer after model load, and under 1 second for
questions filtered before generation. Suitable for an interactive chatbot.

**Overall assessment.** The hallucination defences hold: no invented figures,
no fabricated policy content, and out-of-scope controls stopped before
reaching the model in every case. The two problems worth carrying into Sprint
4 are citation integrity, which is a correctness issue affecting user trust,
and over-refusal, which is a usefulness issue. Neither was visible from the
stubbed tests in test_generation.py, and both were found on the first live
run.
