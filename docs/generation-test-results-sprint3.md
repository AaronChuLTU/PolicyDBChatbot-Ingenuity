# Generation Test Results - Sprint 3 (PCOIS2-51)

**Date run:** 2026-09-01  
**Model:** Ollama / qwen3  
**Retrieval:** hybrid (BM25 + vector + cross-encoder rerank), threshold 0.5  
**Questions:** 16  |  **Reached the model:** 10  |  **Flagged for review:** 5

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
- Clean: **11/16**

## Results

| # | Question | Score | Status | Reached model | Flags | Verdict |
|---|---|---|---|---|---|---|
| 1 | What academic dress do graduands wear at a graduation ceremony? | 0.999 | success | yes | RULE 4 (no citations in answer): "Part E" |  |
| 2 | Who is entitled to wear a doctoral gown? | 0.902 | success | yes | - |  |
| 3 | Can I keep my academic gown after the ceremony? | 0.797 | low_confidence | no | - |  |
| 4 | What happens if a student fails the same subject more than once? | 0.985 | success | yes | UNSUPPORTED TERMS: involves |  |
| 5 | Can I appeal an academic progression decision? | 0.882 | success | yes | - |  |
| 6 | What are the stages of academic progression review? | 0.999 | success | yes | - |  |
| 7 | How do I apply for promotion to Associate Professor? | 0.977 | success | yes | - |  |
| 8 | Who sits on the academic promotions committee? | 0.998 | success | yes | UNSUPPORTED TERMS: includes, serves |  |
| 9 | What is the basis for academic promotion? | 0.991 | success | yes | - |  |
| 10 | What qualifications must academic staff hold to teach a subject? | 0.999 | success | yes | UNSUPPORTED TERMS: achieve |  |
| 11 | Does a lecturer need a qualification higher than the course they teach? | 0.111 | out_of_scope | no | - |  |
| 12 | What are the English language requirements for admission? | 0.582 | low_confidence | no | - |  |
| 13 | Can I get credit for prior study when I apply? | 0.028 | out_of_scope | no | - |  |
| 14 | How are applications for admission assessed? | 0.795 | success | yes | ROUTING: expected low_confidence, got success |  |
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
- **Response time:** 8.8s

**Answer:**

> Graduands wear academic dress appropriate to their qualification, as specified in Part E. This includes a gown, hood, stole, and/or trencher, with colours reflecting the discipline content of the award. Graduands of Aboriginal and/or Torres Strait Islander descent may also wear an additional stole in specified colours.

**Citations:**

- Academic Dress Policy - Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=208)

**Flags:**

- RULE 4 (no citations in answer): "Part E"

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

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.902  
- **Response time:** 5.1s

**Answer:**

> Persons who are entitled to wear a doctoral gown are those who have completed a University award, as academic dress is worn by persons who are entitled to wear them by virtue of their completion of a University award. Specifically, graduates of a Doctor of Philosophy or other doctoral degrees, as well as recipients of honorary doctoral degrees, are entitled to wear the academic dress associated with their award.

**Citations:**

- Academic Dress Policy - Section 7 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Part E -  Specific Academic Dress Requirements (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Dress Policy / Section 7 - Definitions (score 0.902)

> (13) For the purposes of this Policy: academic dress: the gown, hood or stole and cap, or combination thereof, worn by persons who are entitled to wear them by virtue of their completion of a University award. Academic dress is normally worn only on ceremonial occasions, such as graduations, at which the wearing of academic dress is required or permitted. specialised award: a higher education program that prepares a graduate for a specific career that is generally identified in the name of the award (e.g. Bachelor of Laws, Master of Physiotherapy Practice). It normally requires the graduate to meet the requirements of an external accreditation or registration body as well as the University’s own requirements. trencher: mortarboard; a kind of cap with a stiff, flat, cloth-covered square piece.

**Excerpt 2** - Academic Dress Policy / Part E -  Specific Academic Dress Requirements (score 0.795)

> Award: Sub-degrees Academic Dress: A La Trobe University Bachelor’s gown, together with a stole ten centimetres wide lined with silk in the colour of the discipline. The stole is worn around the neck and drapes down the front of the gown. No trencher is worn. Award: Bachelor Degree Academic Dress: A gown in Oxford blue cloth, with bell-shaped sleeves to the wrist, together with a Burgon style Oxford hood of Oxford blue cloth with a 10-centimetre-wide silk facing in the colour of the discipline, and a black cloth trencher. The hood is worn with the hood’s silk exposed on the right shoulder. Award: Bachelor Degrees with Honours Academic Dress: The components are identical to the components of the academic dress worn by graduates of a Bachelor pass degree. However, Honours graduates will wear the hood with the hood’s silk exposed on the left shoulder instead of on the right Award: Graduate  ...

**Excerpt 3** - Academic Dress Policy / Section 5 - Policy Statement (score 0.614)

> (3) The University will prescribe from time to time the academic dress to be worn on ceremonial occasions, including graduations and presentation ceremonies and such other occasions as the Council may specify, by: officers of the University, members of Council and other members of the University; and/or graduands or graduates of degrees and other awards of the University. (4) The colours used for gown facings, hoods or stoles for particular awards generally will reflect the discipline content of the award, rather than the specific award program or the academic unit that teaches the course. (5) Staff or students of Aboriginal and/or Torres Strait Islander descent who are entitled to wear academic dress may opt to wear also a stole in Aboriginal and/or Torres Strait Islander colours.

**Excerpt 4** - Academic Dress Policy / Section 2 - Purpose (score 0.092)

> (1) This Policy prescribes: the core principles for the use of academic dress; the academic dress to be worn on ceremonial occasions of the University by various categories of staff, University Council (Council) members, and graduands/graduates and other recipients of University awards.

**Excerpt 5** - Academic Dress Policy / Preamble (score 0.054)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Dress Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Dress and Colour Protocols Part B - Requests for Changes or Additions to Academic Dress Part C - Recording of Academic Dress Requirements Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent Part E - Specific Academic Dress Requirements Staff, Council Members and Visitors Graduands/Graduates and Other Award Recipients Section 7 - Definitions Section 8 - Authority and Associated Information This is the current version of this document. To view historic versions, click the link in the document's navigation bar. Section 1 - Key Information Policy Type and Approval Body Administrative -  ...

</details>

---

### 3. Can I keep my academic gown after the ceremony?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.797  
- **Response time:** 3.6s

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
- **Response time:** 4.8s

**Answer:**

> If a student fails the same subject in a course for the second time, they will trigger Academic Progression Stage Two (AP2) – Support and Sanction. This stage involves an enrolment load restriction of a maximum of 45 credit points in the next Progression Period, unless they are enrolled in a thesis subject or a workplace-based subject. Students are also required to attend an academic recovery workshop.

**Citations:**

- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)

**Flags:**

- UNSUPPORTED TERMS: involves

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
- **Response time:** 4.5s

**Answer:**

> Students may seek a review of a decision made to exclude them from their course through the University Appeals Committee (UAC) under the provisions of the Academic Progress Statute 2010. Students must apply for such a review within twenty (20) business days of notification of the decision. The decision of the UAC is the final decision of the University.

**Citations:**

- Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=220)

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
- **Response time:** 5.1s

**Answer:**

> The stages of academic progression review are Academic Progression Stage One (AP1) – Recovery, Academic Progression Stage Two (AP2) – Support and Sanction, and Academic Progression Stage Three (AP3) – Show Cause and Course Exclusion. These stages are triggered based on the thresholds of subject failure and are associated with specific support and interventions.

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

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.977  
- **Response time:** 7.1s

**Answer:**

> To apply for promotion to Associate Professor, applicants must meet the qualifications and/or experience requirements, assess their eligibility against the Minimum Standards for Academic Levels and the Academic Performance Framework, and submit a completed Academic Promotions Application Form, CV, and supporting documents electronically via the Academic Promotions link on the Internal Jobs intranet page. Applicants are encouraged to seek guidance from their Career Success Manager, Academic Reviewer, Head of Department, Dean, or academic mentor before submitting their application. The Academic Promotions Committee will convene once per year to consider applications, and applications must be submitted by the cut-off date for inclusion in those meetings.

**Citations:**

- Academic Promotions Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Section 3 - Scope (score 0.977)

> (2) This Policy applies to all academic staff employed at La Trobe University whether full time or part time, fixed-term or continuing, academic practitioners, and those with joint appointments who seek promotion to: Level B (Lecturer; Research Fellow) Level C (Senior Lecturer; Senior Research Fellow) Level D (Associate Professor; or Principal Research Fellow and Associate Professor) Level E (Professor) (3) This Policy does not apply to casual or sessional academic staff, clinical practitioners, or recent professional practice employees. (4) Staff must have successfully completed probation prior to lodging an application for promotion. In exceptional circumstances, applicants may apply to the Provost to have requirement waived. (5) Fixed-term staff are eligible to apply for promotion but if a promotion is granted it will not extend a fixed-term appointment.

**Excerpt 2** - Academic Promotions Policy / Preamble (score 0.942)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Promotions Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Principles Section 6 - Procedures Part A - Domains of Academic Work Part B - Basis for Promotion Qualifications and/or Relevant Experience Preparing and Lodging the Application Part C - Referee and External Assessor Reports Referee Reports Independent External Assessors for Applications to Level D and E Only Part D - Academic Promotions Committees Membership of Academic Promotions Committees Assessment of Application Approval Process Part E - Outcomes Effective Date of Promotion and Salary Point Unsuccessful Applicants Reconsideration Part F - Special Cases Upgrading a Reversionary Substantive Position Promotion of Joint Appointments Out ...

**Excerpt 3** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.936)

> (21) The Committee will, in the context of the level for which promotion is applied, consider the appropriateness of levels and types of formal qualifications and/or substantial progress towards such qualifications or, where relevant consider and determine the equivalence of alternative qualifications and/or experience held by applicants. (22) Applicants will assess whether they are eligible for promotion and merit promotion with reference to the Minimum Standards for Academic Levels and the Academic Performance Framework . (23) Applicants are strongly encouraged to seek guidance and discuss their application with the following before making an application for promotion: Career Success Manager/Academic Reviewer/Head of Department Dean/Director of Centre/Institute An academic mentor (24) The Academic Promotions Committee will convene once per year to consider applications. The dates of Ac ...

**Excerpt 4** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.790)

> (26) Applicants must follow the “Instructions for Applicants” and submit applications electronically via the Academic Promotions link that will be available on the Internal Jobs intranet page. The submission must include: completed Academic Promotions Application Form CV in the standardised format, available on the Academic Promotions Intranet all supporting documents as required by the “Instructions for Applicants”. (27) Applicants will receive an automatic acknowledgment once their application has been lodged.

**Excerpt 5** - Academic Promotions Policy / Part F - Special Cases (score 0.761)

> (78) A staff member who holds a continuing substantive position and is appointed as a result of an externally competitive process to a fixed-term academic position at a higher level at La Trobe, may apply for promotion to upgrade their reversionary substantive position. (79) Provided that the fixed-term appointment and the substantive position are both research-only positions, the staff member may submit their appointment application in place of the narrative section of their promotion application. All other promotion documentation and reports are required as for a standard application. (80) A current Level C member of staff who has been awarded an ARC Future Fellowship or an NHMRC Investigator Grant at equivalent to Level D may apply for promotion on the basis of excellence in research to upgrade their substantive position. Provided the applicant applies within 18 months of being awarde ...

</details>

---

### 8. Who sits on the academic promotions committee?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.998  
- **Response time:** 11.4s

**Answer:**

> The academic promotions committee includes the Deputy Vice-Chancellor (Academic) (ex officio), Pro Vice-Chancellor (Research) (ex officio), Deputy Provost (ex officio), Chair of Academic Board (ex officio), up to five academic members at Academic Level E nominated by the Vice-Chancellor, Chief People Officer or nominee as a non-voting observer, and one invited Level E academic who is external to La Trobe University. For promotion to Levels B and C, the committee also includes the Deputy Vice-Chancellor (Research and Innovation) as Chair, and for promotion to Levels D and E, the Provost serves as Chair.

**Citations:**

- Academic Promotions Policy - Part D - Academic Promotions Committees (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

**Flags:**

- UNSUPPORTED TERMS: includes, serves

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

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.991  
- **Response time:** 12.7s

**Answer:**

> Promotion is based on the applicant’s qualifications and/or experience, evidence of achievement in the domains of academic activity: teaching, research/SOLT and service, as appropriate with respect to the type of employment and agreed work plan, and confirmation from the applicant’s Career Success Manager/Academic Reviewer that the applicant has demonstrated a level of achievement and performance that is appropriate to their existing academic level. In addition, consideration is given to the appropriate balance of performance and outcomes in disciplines and professions where there is a greater reliance on current professional practice, joint appointments with partner institutions or industry, performance relative to opportunity, and recognition of interrupted careers and fractional appointments due to family commitments, ill health or medical condition, disability or major life disruptions. Applicants must provide supporting evidence for any claims made in their application.

**Citations:**

- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Academic Promotions Policy (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.991)

> (17) Promotion is based on: the applicant’s qualifications and/or experience; evidence (see Definitions) of achievement in the domains of academic activity: teaching, research/SOLT and service, as appropriate with respect to the type of employment and agreed work plan; confirmation from the applicant’s Career Success Manager/Academic Reviewer that the applicant has demonstrated a level of achievement and performance that is appropriate to their existing academic level. (18) In addition to the above, consideration is also given to the following: the appropriate balance of performance and outcomes in disciplines and professions where there is a greater reliance on current professional practice; joint appointments with partner institutions or industry; performance relative to opportunity and recognition of interrupted careers and fractional appointments due to family commitments (e.g. paren ...

**Excerpt 2** - Academic Promotions Policy / Academic Promotions Policy (score 0.986)

> Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Principles Section 6 - Procedures Part A - Domains of Academic Work Part B - Basis for Promotion Qualifications and/or Relevant Experience Preparing and Lodging the Application Part C - Referee and External Assessor Reports Referee Reports Independent External Assessors for Applications to Level D and E Only Part D - Academic Promotions Committees Membership of Academic Promotions Committees Assessment of Application Approval Process Part E - Outcomes Effective Date of Promotion and Salary Point Unsuccessful Applicants Reconsideration Part F - Special Cases Upgrading a Reversionary Substantive Position Promotion of Joint Appointments Out of Cycle Expedited Promotion – Exceptional Circumstances Section 7 - Definitions Section 8 - Authority and Associated Information

**Excerpt 3** - Academic Promotions Policy / Preamble (score 0.983)

> Current Version Status and Details Associated Information Historic Versions Future Versions Print Feedback Academic Promotions Policy Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Principles Section 6 - Procedures Part A - Domains of Academic Work Part B - Basis for Promotion Qualifications and/or Relevant Experience Preparing and Lodging the Application Part C - Referee and External Assessor Reports Referee Reports Independent External Assessors for Applications to Level D and E Only Part D - Academic Promotions Committees Membership of Academic Promotions Committees Assessment of Application Approval Process Part E - Outcomes Effective Date of Promotion and Salary Point Unsuccessful Applicants Reconsideration Part F - Special Cases Upgrading a Reversionary Substantive Position Promotion of Joint Appointments Out ...

**Excerpt 4** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.972)

> (21) The Committee will, in the context of the level for which promotion is applied, consider the appropriateness of levels and types of formal qualifications and/or substantial progress towards such qualifications or, where relevant consider and determine the equivalence of alternative qualifications and/or experience held by applicants. (22) Applicants will assess whether they are eligible for promotion and merit promotion with reference to the Minimum Standards for Academic Levels and the Academic Performance Framework . (23) Applicants are strongly encouraged to seek guidance and discuss their application with the following before making an application for promotion: Career Success Manager/Academic Reviewer/Head of Department Dean/Director of Centre/Institute An academic mentor (24) The Academic Promotions Committee will convene once per year to consider applications. The dates of Ac ...

**Excerpt 5** - Academic Promotions Policy / Part F - Special Cases (score 0.959)

> a statement by the Provost detailing the exceptional circumstances which would warrant out-of-cycle, expedited assessment (including evidence of an offer to the staff member from another University if this is the basis for the case); the date by which the applicant must respond to an offer from another University (if applicable); the significance of the staff member’s contributions in terms of meeting strategic or operational objectives of the area/University; an assessment of the staff member’s profile and contributions against the criteria for promotion to that level; a statement from the Dean supporting the promotion; details of two assessors nominated by the Provost in consultation with the professor of discipline or other appropriate senior person with a knowledge of a particular discipline or specialist area may be required upon request of the Vice-Chancellor and/or the Chair of th ...

</details>

---

### 10. What qualifications must academic staff hold to teach a subject?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 5.1s

**Answer:**

> La Trobe University ensures that academic staff are appropriately qualified for the level of their teaching responsibilities. Staff who do not meet the requisite qualification for a given level of teaching must achieve Professional Equivalence through a robust assessment framework. The University maintains records of all staff qualifications, assessments of professional equivalence, and professional development plans.

**Citations:**

- Academic Staff Qualifications Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 6 - Procedures (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Preamble (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=420)

**Flags:**

- UNSUPPORTED TERMS: achieve

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
- **Response time:** 4.0s

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
- **Response time:** 6.8s
- **Note:** ACCEPTANCE TEST for PCOIS2-49. Retrieval hands this Academic Promotions text at 0.795, well above threshold. A fluent answer about promotion committees is a hallucination and a fail

**Answer:**

> Applications for admission are assessed based on entry requirements, which are approved by the Academic Board, and are transparent, equitable, and clearly communicated. The University ensures that entry requirements are equivalent for domestic and international applicants and that information regarding these requirements is easily accessible. Applicants who meet all applicable entry requirements are eligible to be considered for entry but are not guaranteed a place, as entry is based on competitive selection.

**Citations:**

- Academic Promotions Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=76)

**Flags:**

- ROUTING: expected low_confidence, got success

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
- **Response time:** 0.7s
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

**1. The acceptance test passed.**
Question 14 hands the model Academic Promotions text at 0.795, well above the
0.5 threshold, so nothing upstream filters it. The model ignored it and
answered from the Admissions Policy excerpts scoring 0.191 and 0.099. Every
claim traces to those chunks; nothing about promotion committees appears.
Rule 1 works. This is the failure mode the prompt exists to prevent, and it
held across all three runs including after the rules were loosened.

**2. No hallucinated figures in any run.**
Zero unsupported numbers across all 16 questions in every run. Since policy
answers turn on day counts, credit points and percentages - "twenty (20)
business days", "45 credit points" - and an invented figure is both the most
damaging error and the easiest to detect, this is the strongest available
evidence that grounding is holding.

**3. Over-refusal was the main defect, and the prompt rewrite substantially
fixed it.**
The first live run refused 5 of 12 in-scope questions, several with rerank
scores above 0.97. After the rewrite, 10 of 16 questions reached a generated
answer, up from 7, and over-refusals dropped from 5 to 2. Question 9 is the
clearest case: previously refused despite a 0.991 score on a section titled
"Part B - Basis for Promotion", it now returns the operative clause verbatim.
Question 7 now returns the actual application procedure including electronic
submission via the Internal Jobs intranet page.

**4. Question 6 was answering the wrong question, and now does not.**
Asked for the stages of academic progression review, the earlier runs
described AP2 mechanics - Course Coordinator review, CoE and visa
implications - despite excerpt 1 listing the three stages explicitly. It now
returns AP1 Recovery, AP2 Support and Sanction, and AP3 Show Cause and Course
Exclusion. No automated check caught the original error, because the words
used did appear somewhere in the excerpts. This is a limitation of
term-matching: it detects invented content, not irrelevant content.

**5. Three prompt changes were made together and cannot be attributed
individually.**
Answering was moved ahead of refusing and given a worked example; the user
prompt was changed so it no longer ends on the refusal instruction; and
excerpts now carry their section heading. The section-heading change is the
most likely driver - a chunk headed "Part B - Basis for Promotion" is strong
evidence it answers "what is the basis for promotion", and withholding it
discarded that signal. Setting INCLUDE_SECTION_TITLES = False and re-running
would isolate it. Policy titles remain withheld, so the citation-invention
risk the original design guarded against is unchanged.

**6. An earlier hypothesis was tested and rejected.**
Before this rewrite, a narrower change loosened one Rule 2 bullet about
definitions and scope statements. It produced no improvement on the four
target questions and one regression: question 2 stopped refusing but answered
about British colour standards rather than doctoral gowns. That change was
reverted. Recording it matters because it shows the improvement above came
from the second hypothesis, not the first.

**7. The two remaining refusals appear correct.**
Question 3 (keeping the gown after the ceremony) - the Academic Dress Policy
does not address ownership. Question 12 (English language requirements) - the
Admissions Policy refers to a separate English Language Entry Requirements
Policy which is not in the corpus. Both are corpus gaps rather than model
errors, matching the pattern already identified for question 13 and credit
transfer. Expanding ingestion beyond the five pilot policies should resolve
all three.

**8. Citation integrity is the outstanding defect.**
Question 14's answer is drawn from Admissions Policy excerpts but its only
citation reads "Academic Promotions Policy - Section 5". This is because
build_citations() in respond.py filters to chunks scoring at or above 0.50,
and only the promotions chunk cleared it. For a system whose stated purpose
is source-referenced answers, a correct answer with a wrong citation is worse
than a refusal: it is confidently unverifiable, and a user following the link
lands on an unrelated policy. Raised for PCOIS2-50.

**9. One minor rule violation.**
Question 1's answer writes "as specified in Part E", breaching the rule
against writing section references. Cosmetic rather than a grounding failure,
and the detection regex was widened during this sprint to catch letter-suffixed
parts as well as numbered sections.

**10. Chunking defects reach the model.**
Preamble and table-of-contents chunks appear in the excerpt sets for questions
1, 6, 7, 9 and 10, scoring as high as 0.996. They occupy context slots that
could hold substantive clauses. An explicit refusal trigger for
table-of-contents content was added to the prompt as mitigation, but the
underlying fix is the clean_and_chunk.py duplication defect.

**11. Response times are acceptable.**
3-13 seconds per generated answer, and under 1 second for questions filtered
before generation. Suitable for an interactive chatbot, though the longer
responses would benefit from streaming output in the frontend.

**Overall.** Grounding holds: no invented figures, no fabricated policy
content, and the confidently-wrong-policy scenario the prompt was written to
prevent did not occur. The prompt rewrite converted three incorrect refusals
into correct answers without weakening that defence. Remaining work is
citation integrity in respond.py, the chunking defect in clean_and_chunk.py,
and corpus expansion to close the three content gaps - none of which are
prompt problems.
