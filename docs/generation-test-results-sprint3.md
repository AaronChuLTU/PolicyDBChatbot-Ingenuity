# Generation Test Results - Sprint 3 (PCOIS2-51)

**Date run:** 2026-09-12  
**Model:** Ollama / qwen3  
**Retrieval:** hybrid (BM25 + vector + cross-encoder rerank), threshold 0.5  
**Questions:** 16  |  **Reached the model:** 12  |  **Flagged for review:** 10

Live end-to-end run: real Postgres, real retrieval, real model.
`test_generation.py` covers routing logic with stubs and never calls
the model, so this is the first check of whether the model actually
obeys the prompt rules.

A flag is a place to look, not a verdict. Automation narrows the
search; the Verdict column below is filled in by a human comparing
each answer against the excerpts it was given.

## Summary

- Routing failures: **2**
- Responses with unsupported numbers or terms: **8**
- Clean: **6/16**

## Results

| # | Question | Score | Status | Reached model | Flags | Verdict |
|---|---|---|---|---|---|---|
| 1 | What academic dress do graduands wear at a graduation ceremony? | 0.999 | success | yes | UNSUPPORTED TERMS: heritage, representing, standard |  |
| 2 | Who is entitled to wear a doctoral gown? | 0.902 | success | yes | UNSUPPORTED TERMS: individuals, outlined |  |
| 3 | Can I keep my academic gown after the ceremony? | 0.797 | low_confidence | no | - |  |
| 4 | What happens if a student fails the same subject more than once? | 0.985 | success | yes | UNSUPPORTED TERMS: involves |  |
| 5 | Can I appeal an academic progression decision? | 0.882 | success | yes | UNSUPPORTED TERMS: excerpts, mention |  |
| 6 | What are the stages of academic progression review? | 0.999 | success | yes | UNSUPPORTED TERMS: involve |  |
| 7 | How do I apply for promotion to Associate Professor? | 0.977 | success | yes | - |  |
| 8 | Who sits on the academic promotions committee? | 0.998 | success | yes | UNSUPPORTED TERMS: includes, serves |  |
| 9 | What is the basis for academic promotion? | 0.991 | success | yes | UNSUPPORTED TERMS: factors |  |
| 10 | What qualifications must academic staff hold to teach a subject? | 0.999 | success | yes | UNSUPPORTED TERMS: details |  |
| 11 | Does a lecturer need a qualification higher than the course they teach? | 0.107 | out_of_scope | no | - |  |
| 12 | What are the English language requirements for admission? | 0.995 | success | yes | - |  |
| 13 | Can I get credit for prior study when I apply? | 0.834 | success | yes | - |  |
| 14 | How are applications for admission assessed? | 0.971 | success | yes | ROUTING: expected low_confidence, got success |  |
| 15 | How do I book a car parking permit on campus? | 0.876 | low_confidence | no | ROUTING: expected out_of_scope, got low_confidence |  |
| 16 | What food is available at the campus cafe today? | 0.001 | out_of_scope | no | - |  |

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
- **Response time:** 42.9s

**Answer:**

> Graduands wear academic dress as prescribed by the University for ceremonial occasions, including graduations. Graduands of Aboriginal and/or Torres Strait Islander descent may also opt to wear a stole in specific colours representing their heritage in addition to the standard academic dress.

**Citations:**

- Academic Dress Policy - Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 7 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=208)

**Flags:**

- UNSUPPORTED TERMS: heritage, representing, standard

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Dress Policy / Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent (score 0.999)

> (11) Graduands/graduates of Aboriginal and/or Torres Strait Islander descent may opt to wear, in addition to the appropriate academic dress described in Part E, a stole ten centimetres wide of the following colours: Aboriginal: equal bands of Jet Black, Saffron and Post Office red silks Torres Strait Islander: larkspur silk edged on each side with Juniper silk, each colour separated by a narrow band of black piping. (12) Graduands requiring one or both of these stoles should indicate this when registering to attend their ceremony.

**Excerpt 2** - Academic Dress Policy / Section 5 - Policy Statement (score 0.998)

> (3) The University will prescribe from time to time the academic dress to be worn on ceremonial occasions, including graduations and presentation ceremonies and such other occasions as the Council may specify, by: officers of the University, members of Council and other members of the University; and/or graduands or graduates of degrees and other awards of the University. (4) The colours used for gown facings, hoods or stoles for particular awards generally will reflect the discipline content of the award, rather than the specific award program or the academic unit that teaches the course. (5) Staff or students of Aboriginal and/or Torres Strait Islander descent who are entitled to wear academic dress may opt to wear also a stole in Aboriginal and/or Torres Strait Islander colours.

**Excerpt 3** - Academic Dress Policy / Section 3 - Scope (score 0.994)

> (2) This Policy applies to: all graduands/graduates and other recipients of La Trobe awards recognised in the Australian Qualifications Framework; all staff participating in graduation and presentation ceremonies of the University or in other events at which the wearing of academic dress is required or permitted.

**Excerpt 4** - Academic Dress Policy / Section 2 - Purpose (score 0.992)

> (1) This Policy prescribes: the core principles for the use of academic dress; the academic dress to be worn on ceremonial occasions of the University by various categories of staff, University Council (Council) members, and graduands/graduates and other recipients of University awards.

**Excerpt 5** - Academic Dress Policy / Section 7 - Definitions (score 0.991)

> (13) For the purposes of this Policy: academic dress: the gown, hood or stole and cap, or combination thereof, worn by persons who are entitled to wear them by virtue of their completion of a University award. Academic dress is normally worn only on ceremonial occasions, such as graduations, at which the wearing of academic dress is required or permitted. specialised award: a higher education program that prepares a graduate for a specific career that is generally identified in the name of the award (e.g. Bachelor of Laws, Master of Physiotherapy Practice). It normally requires the graduate to meet the requirements of an external accreditation or registration body as well as the University’s own requirements. trencher: mortarboard; a kind of cap with a stiff, flat, cloth-covered square piece.

</details>

---

### 2. Who is entitled to wear a doctoral gown?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.902  
- **Response time:** 3.9s

**Answer:**

> Persons who are entitled to wear a doctoral gown are those who have completed a University award, specifically a Doctor of Philosophy or other doctoral degrees as outlined in the policy. The policy specifies that the academic dress, including the gown, hood, and headwear, is prescribed for these individuals on ceremonial occasions.

**Citations:**

- Academic Dress Policy - Section 7 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Part E -  Specific Academic Dress Requirements (https://policies.latrobe.edu.au/document/view.php?id=208)
- Academic Dress Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=208)

**Flags:**

- UNSUPPORTED TERMS: individuals, outlined

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Dress Policy / Section 7 - Definitions (score 0.902)

> (13) For the purposes of this Policy: academic dress: the gown, hood or stole and cap, or combination thereof, worn by persons who are entitled to wear them by virtue of their completion of a University award. Academic dress is normally worn only on ceremonial occasions, such as graduations, at which the wearing of academic dress is required or permitted. specialised award: a higher education program that prepares a graduate for a specific career that is generally identified in the name of the award (e.g. Bachelor of Laws, Master of Physiotherapy Practice). It normally requires the graduate to meet the requirements of an external accreditation or registration body as well as the University’s own requirements. trencher: mortarboard; a kind of cap with a stiff, flat, cloth-covered square piece.

**Excerpt 2** - Academic Dress Policy / Part E -  Specific Academic Dress Requirements (score 0.795)

> Award: Sub-degrees Academic Dress: A La Trobe University Bachelor’s gown, together with a stole ten centimetres wide lined with silk in the colour of the discipline. The stole is worn around the neck and drapes down the front of the gown. No trencher is worn. Award: Bachelor Degree Academic Dress: A gown in Oxford blue cloth, with bell-shaped sleeves to the wrist, together with a Burgon style Oxford hood of Oxford blue cloth with a 10-centimetre-wide silk facing in the colour of the discipline, and a black cloth trencher. The hood is worn with the hood’s silk exposed on the right shoulder. Award: Bachelor Degrees with Honours Academic Dress: The components are identical to the components of the academic dress worn by graduates of a Bachelor pass degree. However, Honours graduates will wear the hood with the hood’s silk exposed on the left shoulder instead of on the right Award: Graduate  ...

**Excerpt 3** - Academic Dress Policy / Section 5 - Policy Statement (score 0.614)

> (3) The University will prescribe from time to time the academic dress to be worn on ceremonial occasions, including graduations and presentation ceremonies and such other occasions as the Council may specify, by: officers of the University, members of Council and other members of the University; and/or graduands or graduates of degrees and other awards of the University. (4) The colours used for gown facings, hoods or stoles for particular awards generally will reflect the discipline content of the award, rather than the specific award program or the academic unit that teaches the course. (5) Staff or students of Aboriginal and/or Torres Strait Islander descent who are entitled to wear academic dress may opt to wear also a stole in Aboriginal and/or Torres Strait Islander colours.

**Excerpt 4** - Academic Dress Policy / Section 2 - Purpose (score 0.092)

> (1) This Policy prescribes: the core principles for the use of academic dress; the academic dress to be worn on ceremonial occasions of the University by various categories of staff, University Council (Council) members, and graduands/graduates and other recipients of University awards.

**Excerpt 5** - Academic Dress Policy / Part E -  Specific Academic Dress Requirements (score 0.046)

> Role: Chancellor Academic Dress: A gown of Ruby and Cardinal silk damask with gold braid trim, red silk lining and a black velvet Tudor bonnet and gold tassel Role: Deputy Chancellor Academic Dress: A gown of Ruby and Cardinal silk damask with silver braid trim, red silk lining and a black velvet Tudor bonnet and silver tassel Role: Vice-Chancellor and President Academic Dress: A gown of Oxford blue silk damask with silver braid trim, blue silk lining and black velvet Tudor bonnet with silver tassel Role: Deputy Vice-Chancellors and Vice-Presidents Academic Dress: A gown of Smalt cloth with a 10-centimetre wide silver braid trim, with blue silk lining and inserts of black velvet on the shoulders and a black Tudor bonnet with silver tassel Role: Provost Academic Dress: A gown of Smalt cloth with a 10-centimetre wide silver braid trim, with blue silk lining and inserts of black velvet on t ...

</details>

---

### 3. Can I keep my academic gown after the ceremony?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.797  
- **Response time:** 3.3s

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
- **Response time:** 3.8s

**Answer:**

> If a student fails the same subject in a course for a second time, they will trigger Academic Progression Stage Two (AP2) - Support and Sanction. This involves attending an academic recovery workshop and may result in an enrolment restriction of a maximum of 45 credit points.

**Citations:**

- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)
- Student Support Policy - Section 6 - Definitions (https://policies.latrobe.edu.au/document/view.php?id=409)

**Flags:**

- UNSUPPORTED TERMS: involves

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.985)

> Stage: Green Thresholds: Student has passed the subjects in which they are enrolled Communication or Intervention: No intervention or communication Stage: Recovery(AP1)- Yellow Thresholds: Triggered when a student fails one subject for the ﬁrst time other than a workplace-based subject Communication or Intervention: - AP1 support communication- Academic Recovery Module- Support from Library and Learning Services Teams Stage: Support and Sanction(AP2)- Amber Thresholds: Triggered when a student:- fails for the ﬁrst time any workplace-based subject, or- fails 50% or more of their enrolled credit points for the first time, or- fails the same subject in a course for a second time, or- triggers AP1 more than three times. Communication or Intervention: - AP2 support communication requiring attendance at academic recovery workshop (all students)- Attendance at workshop required to lift any rest ...

**Excerpt 2** - Student Support Policy / Section 6 - Definitions (score 0.952)

> (15) For the purposes of this Policy: reports significant life circumstances that are impacting their capacity to study belongs to a cohort identified as benefitting from additional support fails to engage with academic learning, as evidenced by failure to engage with the Learning Management System or assessment fails an early assessment item in their subject fails one subject for the ﬁrst time other than a workplace-based subject fails for the ﬁrst time any workplace-based subject fails 50% or more of their enrolled credit points for the first time fails the same subject in a course for a second time, or looks likely that they will not complete their course within the maximum period of study withdraws from all subjects for any one progression review period after the Census Date.

**Excerpt 3** - Timetabling Management Policy / Part E - Class Allocation and Load Management (score 0.318)

> (31) The University attempts to accommodate students’ choice of subjects, but the timetable might not allow every student to attend their preferred combination of subjects. Students should choose alternative electives if they are unable to resolve a clash. If students choose to accept a timetable clash (that is not on the approved clash list ) they accept any conflicting requirements (including assessment) that may result between clashing subjects. This will not be considered grounds for Special Consideration. (32) The University will directly allocate students to classes in certain circumstances, including but not limited to where: there is a scheduled single iteration of an activity there are physical access or other requirements students have failed to register for a class (33) In order to ensure adequate room capacity and continuity for any given subject, students are only permitted  ...

**Excerpt 4** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.188)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 5** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.078)

> the consequences of continued academic failure; their options for appealing the decision to place conditions on their enrolment (see Part C) and the availability of independent advocacy support. (17) During the academic recovery workshop students are required to engage in self-assessment and action plan generation. They may seek additional advice where required from ASK La Trobe, a Student Advisor or their Course Coordinator. (18) Students who trigger AP3 receive a communication: advising that they have reached the final stage of academic progression monitoring and why; inviting them to make a written submission within 10 business days to show cause as to why they should not be excluded from their course, and providing guidance about how this is done; if they are an international student, stating the potential impact on their CoE and visa; outlining their options for appealing the propos ...

</details>

---

### 5. Can I appeal an academic progression decision?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.882  
- **Response time:** 3.2s

**Answer:**

> Students may appeal a determination of academic misconduct, including any penalty, within twenty (20) business days of receiving the notice of decision. However, the excerpts do not specifically mention appealing an academic progression decision.

**Citations:**

- Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression (https://policies.latrobe.edu.au/document/view.php?id=220)
- Student Academic Misconduct Policy - Part F - Appeals (https://policies.latrobe.edu.au/document/view.php?id=221)
- Graduate Research and RTP Scholarships Policy - Part G - Right of Review (https://policies.latrobe.edu.au/document/view.php?id=317)
- Academic Progression Review Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=220)

**Flags:**

- UNSUPPORTED TERMS: excerpts, mention

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.882)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 2** - Student Academic Misconduct Policy / Part F - Appeals (score 0.865)

> (57) Students may appeal a determination of minor or serious academic misconduct made under this Policy, including any penalty, within twenty (20) business days of receiving the notice of decision. Appeals must be lodged in writing with the University Appeals Committee (UAC), accompanied by appropriate evidence, and can only be made where the student can demonstrate that: this Policy and Procedure were not appropriately followed in the reaching of the determination or penalty; or there was bias towards the student on the part of any individual involved with the findings; or more evidence has become available that was not available to decision-makers at the time. (58) Where a penalty is suspension or exclusion, no action may be taken to implement the penalty associated with an allegation before: the conclusion of the 20-day appeal period, even if the student has not yet lodged an appeal;  ...

**Excerpt 3** - Graduate Research and RTP Scholarships Policy / Part G - Right of Review (score 0.626)

> (61) Appeals will be considered only in relation to the application of this Policy, Procedure and associated schedules. (62) Candidates wishing to appeal a decision in relation to a scholarship must do so in writing to the Board of Graduate Research within 20 business days of the date of the written notice of the decision. (63) Members of the Board who were not involved in the original decision will consider the appeal. (64) Scholarship applicants or holders not satisfied with the outcome of any review may seek a review from the University Ombudsman. (65) If a scholarship is awarded as a result of a successful appeal that determines the original decision was made in error due to the academic school’s assessment, the school will be responsible for funding the stipend until the start of the following academic year.

**Excerpt 4** - Academic Progression Review Policy / Section 4 - Key Decisions (score 0.572)

> Key Decisions: Decision to restrict a student’s enrolment load in a course or exclude a student from a course after failure to satisfactorily show cause Role: Academic Progression Officer: nominated senior academic (Level C or higher)

**Excerpt 5** - Graduate Research Admissions Policy / Part G - Right of Review (score 0.416)

> (42) Applicants wishing to appeal a decision in relation to an application for graduate research candidature must do so in writing to the Board of Graduate Research within 20 business days of the date of the written notice of the decision. (43) The appeal will be considered by members of the Board who were not involved in the original decision. (44) Applicants not satisfied with the outcome of any review may seek a review from the University Ombudsman.

</details>

---

### 6. What are the stages of academic progression review?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 4.0s

**Answer:**

> The stages of academic progression review are Academic Progression Stage One (AP1) – Recovery, Academic Progression Stage Two (AP2) – Support and Sanction, and Academic Progression Stage Three (AP3) – Show Cause and Course Exclusion. These stages are triggered by subject failure and involve specific support, interventions, and potential consequences as outlined in the policy.

**Citations:**

- Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Academic Progression Review Policy (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=220)
- Academic Progression Review Policy - Part B - Details of Academic Progression Stages (https://policies.latrobe.edu.au/document/view.php?id=220)

**Flags:**

- UNSUPPORTED TERMS: involve

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Progression Review Policy / Part A - Monitoring and Determining Academic Progression (score 0.999)

> (7) Academic progression in a coursework course is assessed at designated points in time, known as Progression Periods. (8) Where students pass all the subjects in which they are enrolled no interventions are made. (9) Students who experience subject failure will trigger one of three stages of academic progression: Academic Progression Stage One (AP1) – Recovery Academic Progression Stage Two (AP2) – Support and Sanction Academic Progression Stage Three (AP3)– Show Cause and Course Exclusion (10) The thresholds at which students are assessed as having triggered a progression stage are outlined in Table One with the associated support and interventions. (11) Progression outcomes may be reviewed in circumstances where a change is made to a student’s results for any reason, including a successful appeal against a Remission of Debt outcome for Special Circumstances (see Student Fees Procedur ...

**Excerpt 2** - Academic Progression Review Policy / Academic Progression Review Policy (score 0.998)

> Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Monitoring and Determining Academic Progression Part B - Details of Academic Progression Stages Academic Progression Stage One – Recovery Academic Stage Two – Support and Sanction Academic Progression Stage Three – Show Cause and Course Exclusion Course Transfers and New Courses Part C - Review Part D - Monitoring Section 7 - Definitions Section 8 - Authority and Associated Information

**Excerpt 3** - Academic Progression Review Policy / Section 5 - Policy Statement (score 0.946)

> (4) The University is committed to supporting all students, irrespective of their educational background, entry pathway, mode or place of study to achieve their goals in higher education. In terms of this Policy this means that: students’ academic performance is reviewed in a consistent, phased and equitable way; students who are experiencing difficulties are identified as early as possible through formal progression monitoring and additional measures such as early assessment in all subjects, as outlined in the Assessment Policy ; interventions at each stage of academic progression monitoring provide students with multiple avenues for academic and non-academic support and clear information about the consequences of failing to follow agreed action plans. (5) Trends in rates of retention, progression and completion of specific student cohorts are monitored to fulfil legislated reporting re ...

**Excerpt 4** - Academic Progression Review Policy / Part B - Details of Academic Progression Stages (score 0.711)

> (13) Students enrolled in thesis subjects worth 30, 45 or 60 credit points will not have an enrolment restriction or cancellation applied to these subjects. (14) Students who trigger AP1 receive a communication that includes: an explanation of why they have triggered this progression stage; a request to engage with supports as identified through completion of the Support Survey in the academic recovery module; an explanation of the potential consequences of continued academic failure, including enrolment sanctions and course exclusion. (15) Student engagement with academic support at AP1 is tracked for consideration in future academic progression stages as appropriate. (16) Students who trigger AP2 receive a communication advising: why they have triggered this progression stage; that their enrolment load in the next Progression Period will be restricted to a maximum of 45 credit points,  ...

**Excerpt 5** - Student Support Policy / Section 5 - Policy Statement (score 0.445)

> Support Type: Processes for assessing a student’s suitability to continue to undertake a subject, or to identify students at risk of not completing Instrument(s): Academic Progression Review PolicyAdmissions PolicyAssessment StandardsGraduate Research Progress Policy Support Type: Processes for supporting students that are identified as ‘academically at risk’ of unsuccessful completion Instrument(s): Academic Progression Review PolicyStudent Transition PolicyGraduate Research Progress PolicyGraduate Research Show Cause Procedure Support Type: Processes to ensure:students have access to support services including before Census Datestudents are pro-actively offered access to support services prior to the Census Date where they:- are assessed at risk of not completing- have previously failed to successfully complete a subject- demonstrate a low level of engagement Instrument(s): Academic Pr ...

</details>

---

### 7. How do I apply for promotion to Associate Professor?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.977  
- **Response time:** 3.5s

**Answer:**

> To apply for promotion to Associate Professor, applicants must follow the “Instructions for Applicants” and submit applications electronically via the Academic Promotions link on the Internal Jobs intranet page. The submission must include a completed Academic Promotions Application Form, a CV in the standardised format, and all supporting documents as required.

**Citations:**

- Academic Promotions Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Section 3 - Scope (score 0.977)

> (2) This Policy applies to all academic staff employed at La Trobe University whether full time or part time, fixed-term or continuing, academic practitioners, and those with joint appointments who seek promotion to: Level B (Lecturer; Research Fellow) Level C (Senior Lecturer; Senior Research Fellow) Level D (Associate Professor; or Principal Research Fellow and Associate Professor) Level E (Professor) (3) This Policy does not apply to casual or sessional academic staff, clinical practitioners, or recent professional practice employees. (4) Staff must have successfully completed probation prior to lodging an application for promotion. In exceptional circumstances, applicants may apply to the Provost to have requirement waived. (5) Fixed-term staff are eligible to apply for promotion but if a promotion is granted it will not extend a fixed-term appointment.

**Excerpt 2** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.936)

> (21) The Committee will, in the context of the level for which promotion is applied, consider the appropriateness of levels and types of formal qualifications and/or substantial progress towards such qualifications or, where relevant consider and determine the equivalence of alternative qualifications and/or experience held by applicants. (22) Applicants will assess whether they are eligible for promotion and merit promotion with reference to the Minimum Standards for Academic Levels and the Academic Performance Framework . (23) Applicants are strongly encouraged to seek guidance and discuss their application with the following before making an application for promotion: Career Success Manager/Academic Reviewer/Head of Department Dean/Director of Centre/Institute An academic mentor (24) The Academic Promotions Committee will convene once per year to consider applications. The dates of Ac ...

**Excerpt 3** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.790)

> (26) Applicants must follow the “Instructions for Applicants” and submit applications electronically via the Academic Promotions link that will be available on the Internal Jobs intranet page. The submission must include: completed Academic Promotions Application Form CV in the standardised format, available on the Academic Promotions Intranet all supporting documents as required by the “Instructions for Applicants”. (27) Applicants will receive an automatic acknowledgment once their application has been lodged.

**Excerpt 4** - Academic Promotions Policy / Part F - Special Cases (score 0.761)

> (78) A staff member who holds a continuing substantive position and is appointed as a result of an externally competitive process to a fixed-term academic position at a higher level at La Trobe, may apply for promotion to upgrade their reversionary substantive position. (79) Provided that the fixed-term appointment and the substantive position are both research-only positions, the staff member may submit their appointment application in place of the narrative section of their promotion application. All other promotion documentation and reports are required as for a standard application. (80) A current Level C member of staff who has been awarded an ARC Future Fellowship or an NHMRC Investigator Grant at equivalent to Level D may apply for promotion on the basis of excellence in research to upgrade their substantive position. Provided the applicant applies within 18 months of being awarde ...

**Excerpt 5** - Academic Promotions Policy / Part F - Special Cases (score 0.694)

> (89) The Executive Officer will ensure the application is considered by the Academic Promotions Committee as soon as practicable. (90) After reviewing the case, the Committee may recommend the payment of a retention allowance as an alternative to promotion. (91) For applications presented out of cycle and/or in exceptional circumstances, the Vice-Chancellor is responsible for approving any variations to the academic promotions process and the outcome of the application.

</details>

---

### 8. Who sits on the academic promotions committee?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.998  
- **Response time:** 4.3s

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
- **Response time:** 3.8s

**Answer:**

> Promotion is based on the applicant’s qualifications and/or experience, evidence of achievement in the domains of teaching, research/SOLT and service, confirmation from the Career Success Manager/Academic Reviewer, and consideration of factors such as balance of performance, joint appointments, and performance relative to opportunity. The policy also states that promotion will be based on evidence of the quality and impact of contributions to the University’s strategic goals in the relevant domains.

**Citations:**

- Academic Promotions Policy - Part B - Basis for Promotion (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Academic Promotions Policy (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Part F - Special Cases (https://policies.latrobe.edu.au/document/view.php?id=76)
- Academic Promotions Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=76)

**Flags:**

- UNSUPPORTED TERMS: factors

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.991)

> (17) Promotion is based on: the applicant’s qualifications and/or experience; evidence (see Definitions) of achievement in the domains of academic activity: teaching, research/SOLT and service, as appropriate with respect to the type of employment and agreed work plan; confirmation from the applicant’s Career Success Manager/Academic Reviewer that the applicant has demonstrated a level of achievement and performance that is appropriate to their existing academic level. (18) In addition to the above, consideration is also given to the following: the appropriate balance of performance and outcomes in disciplines and professions where there is a greater reliance on current professional practice; joint appointments with partner institutions or industry; performance relative to opportunity and recognition of interrupted careers and fractional appointments due to family commitments (e.g. paren ...

**Excerpt 2** - Academic Promotions Policy / Academic Promotions Policy (score 0.986)

> Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Principles Section 6 - Procedures Part A - Domains of Academic Work Part B - Basis for Promotion Qualifications and/or Relevant Experience Preparing and Lodging the Application Part C - Referee and External Assessor Reports Referee Reports Independent External Assessors for Applications to Level D and E Only Part D - Academic Promotions Committees Membership of Academic Promotions Committees Assessment of Application Approval Process Part E - Outcomes Effective Date of Promotion and Salary Point Unsuccessful Applicants Reconsideration Part F - Special Cases Upgrading a Reversionary Substantive Position Promotion of Joint Appointments Out of Cycle Expedited Promotion – Exceptional Circumstances Section 7 - Definitions Section 8 - Authority and Associated Information

**Excerpt 3** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.972)

> (21) The Committee will, in the context of the level for which promotion is applied, consider the appropriateness of levels and types of formal qualifications and/or substantial progress towards such qualifications or, where relevant consider and determine the equivalence of alternative qualifications and/or experience held by applicants. (22) Applicants will assess whether they are eligible for promotion and merit promotion with reference to the Minimum Standards for Academic Levels and the Academic Performance Framework . (23) Applicants are strongly encouraged to seek guidance and discuss their application with the following before making an application for promotion: Career Success Manager/Academic Reviewer/Head of Department Dean/Director of Centre/Institute An academic mentor (24) The Academic Promotions Committee will convene once per year to consider applications. The dates of Ac ...

**Excerpt 4** - Academic Promotions Policy / Part F - Special Cases (score 0.959)

> a statement by the Provost detailing the exceptional circumstances which would warrant out-of-cycle, expedited assessment (including evidence of an offer to the staff member from another University if this is the basis for the case); the date by which the applicant must respond to an offer from another University (if applicable); the significance of the staff member’s contributions in terms of meeting strategic or operational objectives of the area/University; an assessment of the staff member’s profile and contributions against the criteria for promotion to that level; a statement from the Dean supporting the promotion; details of two assessors nominated by the Provost in consultation with the professor of discipline or other appropriate senior person with a knowledge of a particular discipline or specialist area may be required upon request of the Vice-Chancellor and/or the Chair of th ...

**Excerpt 5** - Academic Promotions Policy / Section 5 - Policy Statement (score 0.958)

> (6) La Trobe seeks to attract, retain and develop very high quality staff to achieve the University’s strategic goals. As part of this commitment, it seeks to encourage, by way of promotion, those members of academic staff who demonstrate outstanding qualities in performing their responsibilities. (7) The University will recognise and reward sustained academic excellence through a transparent and consistent process of promotion. Promotion will be awarded based on evidence of the quality and impact of contributions to the University’s strategic goals at the academic level sought in each of the domains: teaching research and/or scholarship of learning and teaching as appropriate; and service (8) Where an academic appointment specifically precludes or constrains contribution to one of these domains (for example, research-only positions), the application will be judged against the relevant d ...

</details>

---

### 10. What qualifications must academic staff hold to teach a subject?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.999  
- **Response time:** 3.2s

**Answer:**

> The University ensures that academic staff are appropriately qualified for the level of their teaching responsibilities. Academic staff are expected to maintain and advance disciplinary knowledge, including professional practice where relevant. The policy also refers to the Academic Staff Qualifications Procedure - Teaching for further details.

**Citations:**

- Academic Staff Qualifications Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 6 - Procedures (https://policies.latrobe.edu.au/document/view.php?id=420)
- Academic Staff Qualifications Policy - Section 3 - Scope (https://policies.latrobe.edu.au/document/view.php?id=420)
- Outside Studies Program for Academic Staff Policy - Part B - Application Process (https://policies.latrobe.edu.au/document/view.php?id=82)

**Flags:**

- UNSUPPORTED TERMS: details

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Academic Staff Qualifications Policy / Section 5 - Policy Statement (score 0.999)

> (6) The University ensures that its academic staff are appropriately qualified for the level of their teaching responsibilities. This means that: staff who are responsible for the recruitment of subject teaching staff are appropriately experienced and qualified themselves, and familiar with the relevant requirements under the Standards; staff with academic coordination duties are qualified at an appropriately high level and their recruitment is overseen by a senior member of the School; a robust framework for the assessment of Professional Equivalence is applied for teaching staff who do not possess the requisite qualification for a given level of teaching according to the Standards ; the range of teaching duties allocated is appropriately limited until equivalence is reached; professional development plans and appropriate supervision arrangements are established; such arrangements are r ...

**Excerpt 2** - Academic Staff Qualifications Policy / Section 6 - Procedures (score 0.971)

> (9) Refer to: Academic Staff Qualifications Procedure - Teaching ; Academic Staff Qualifications Procedure - Scholarship .

**Excerpt 3** - Academic Staff Qualifications Policy / Section 3 - Scope (score 0.645)

> (2) This Policy applies to all staff who teach students enrolled in La Trobe award courses, including students enrolled in La Trobe courses taught under an educational partnership agreement. (3) Graduate research supervision requirements for Doctoral and Master’s by research candidates are further outlined in the Graduate Research Supervision Policy . (4) This Procedure does not apply to the academic teaching staff of institutions in which students are undertaking study as part of a program of outbound student mobility or partner supervisors of students undertaking placements, internships or other forms of work integrated learning. The University assures itself that such individuals are appropriately qualified to teach and/or supervise La Trobe students through the provisions of the Educational Partnerships Policy and associated procedures. (5) Any exceptions or variations to specific re ...

**Excerpt 4** - Outside Studies Program for Academic Staff Policy / Part B - Application Process (score 0.589)

> (54) The staff member is to assess, where practicable, the degree to which the program has assisted research, teaching or other academic interests and the extent to which it was of benefit to the individual and to the University. (55) The staff member is also free to comment on other matters, not necessarily related to their field of work, that are of value to the University.

**Excerpt 5** - Academic Promotions Policy / Part B - Basis for Promotion (score 0.473)

> (17) Promotion is based on: the applicant’s qualifications and/or experience; evidence (see Definitions) of achievement in the domains of academic activity: teaching, research/SOLT and service, as appropriate with respect to the type of employment and agreed work plan; confirmation from the applicant’s Career Success Manager/Academic Reviewer that the applicant has demonstrated a level of achievement and performance that is appropriate to their existing academic level. (18) In addition to the above, consideration is also given to the following: the appropriate balance of performance and outcomes in disciplines and professions where there is a greater reliance on current professional practice; joint appointments with partner institutions or industry; performance relative to opportunity and recognition of interrupted careers and fractional appointments due to family commitments (e.g. paren ...

</details>

---

### 11. Does a lecturer need a qualification higher than the course they teach?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.107  
- **Response time:** 0.5s
- **Note:** Scored 0.111 in PCOIS2-47 - expected to be filtered before generation

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

### 12. What are the English language requirements for admission?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.995  
- **Response time:** 3.8s

**Answer:**

> Applicants must meet University and, where applicable, course-specific English Language Proficiency (ELP) entry requirements to be eligible for admission. The University provides opportunities for students to further develop their ELP, and applicants who do not meet the required level of ELP at the time of application must satisfactorily complete an appropriate English language program before being admitted.

**Citations:**

- English Language Entry Requirements Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=72)
- English Language Entry Requirements Policy - Part F - Applications and Offers (https://policies.latrobe.edu.au/document/view.php?id=72)
- English Language Entry Requirements Policy - Section 4 - Key Decisions (https://policies.latrobe.edu.au/document/view.php?id=72)
- English Language Entry Requirements Policy - Section 2 - Purpose (https://policies.latrobe.edu.au/document/view.php?id=72)
- English Language Entry Requirements Policy - Part E - Evidence (https://policies.latrobe.edu.au/document/view.php?id=72)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - English Language Entry Requirements Policy / Section 5 - Policy Statement (score 0.995)

> (6) English is the primary language of instruction at La Trobe University. Through this Policy and its admissions policies and processes, the University seeks to ensure that admitted students have the English Language Proficiency (ELP) that: is required to participate successfully in their intended course; and complies, where relevant, with Australian government requirements for holders of Student Visas. (7) To be eligible for admission to a course, applicants must meet University and, where applicable, course-specific ELP entry requirements. All requirements are made clear in promotional material to future students. (8) The University provides opportunities for admitted students to further develop their ELP. Students are responsible for the continued development of their own ELP and any discipline-specific language requirements.

**Excerpt 2** - English Language Entry Requirements Policy / Part F - Applications and Offers (score 0.991)

> applicants who do not meet the required level of ELP at the time of application. In these circumstances applicants are required to satisfactorily complete an appropriate English language program with the required grade/mark for their course of study before being admitted to the University. (38) Where the ELP requirements for a course change, the University will honour any unconditional offers already made. (39) In accordance with the Admissions Procedure and the Graduate Research Admissions Policy the University reserves the right to withdraw or cancel an offer of enrolment where an offer is made based on incomplete or inaccurate information supplied by the applicant or certifying authority.

**Excerpt 3** - English Language Entry Requirements Policy / Section 4 - Key Decisions (score 0.984)

> Key Decisions: Approve English language entry requirements for all courses Role: Academic Board Key Decisions: Approve ELP equivalencies against minimum requirements Role: Director, Admissions and Scholarships Key Decisions: Approve ELP equivalencies for higher degree by research applicants against minimum requirements Role: Chair, Board of Graduate Research

**Excerpt 4** - English Language Entry Requirements Policy / Section 2 - Purpose (score 0.984)

> (1) This Policy establishes the framework for English language requirements for entry to La Trobe University courses and for assessing the English Language Proficiency (ELP) of applicants in accordance with: the Education Services for Overseas Students Act 2000 ; the National Code of Practice for Providers of Education and Training to Overseas Students 2018 ; the Tertiary Education Quality and Standards Agency Act 2011 ; and the Higher Education Standards Framework (Threshold Standards) 2021 . (2) This Policy should be read in conjunction with: the Admissions Policy the Graduate Research Admissions Policy

**Excerpt 5** - English Language Entry Requirements Policy / Part E - Evidence (score 0.975)

> (30) Applicants seeking to demonstrate English language proficiency based on residency and employment and/or life experience in a non-English speaking country may be considered, however, must provide a statement from the employer or equivalent confirming that work has been conducted in an English-speaking environment. (31) Graduate research applicants who wish to be considered on these grounds must submit a written case, endorsed by their prospective supervisor, to the Chair of the Board of Graduate Research in accordance with the Graduate Research Admissions Policy . (32) Coursework applicants who wish to be considered based on employment and/or unscored Year 12 who do not meet the above criteria are referred to the Special Tertiary Admissions Test (STAT). The assessment of STAT results is based on equivalence to the VCE English Study Score 3 and 4 required for the specific course – bas ...

</details>

---

### 13. Can I get credit for prior study when I apply?

- **Status:** success  
- **Confidence:** medium  
- **Top rerank score:** 0.834  
- **Response time:** 3.8s
- **Note:** Corpus gap: credit rules live in the Credit Standard, not ingested. Scored 0.028, so should not reach the model

**Answer:**

> Yes, you can get credit for prior study when you apply. The La Trobe RTO recognises all qualifications recognised by the Australian Qualifications Framework, and provides written advice about its processes for Recognition of Prior Learning (RPL) and credit for previous relevant VET study when an offer is made to students. Students are awarded credit for a unit(s) if they can provide evidence of having completed equivalent units in appropriate timeframes through another RTO.

**Citations:**

- VET Students Policy - Part C - Credit and Recognition of Prior Learning (https://policies.latrobe.edu.au/document/view.php?id=400)
- OS-HELP Loans Policy - Part C - Applying For an OS-HELP Loan (https://policies.latrobe.edu.au/document/view.php?id=204)

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - VET Students Policy / Part C - Credit and Recognition of Prior Learning (score 0.834)

> (21) The La Trobe RTO: recognises all qualifications recognised by the Australian Qualifications Framework, and Records of Results and Statements of Attainment issued by any other Registered Training Organisations; provides written advice about its processes for Recognition of Prior Learning (RPL) and credit for previous relevant VET study when an offer is made to students; maintains records of credit and RPL claims and outcomes in relevant student files. (22) Students are awarded credit for a unit(s) if they can provide evidence of having completed equivalent units in appropriate timeframes through another RTO (refer equivalent unit information at training.gov.au ). (23) Where a previous qualification does not meet VET equivalency requirements, students may either apply for RPL or must enrol in the relevant unit of competency being delivered in the course. (24) Students who request RPL  ...

**Excerpt 2** - OS-HELP Loans Policy / Part C - Applying For an OS-HELP Loan (score 0.527)

> (16) Prior to submitting an application for an OS-HELP Loan, students must obtain a number of approvals and accompanying evidence: confirmation that their proposed overseas Exchange or Short-Term Program has been approved for credit, or is a course requirement, for their course of enrolment at La Trobe; evidence that allows the La Trobe OS-HELP team to confirm that the study will be undertaken on a full-time basis (see the Study Abroad webpage for guidance); acceptance by the host university or provider into the overseas program; La Trobe Learning Abroad acceptance notification. (17) Applications for OS-HELP Loans for approved overseas study can be submitted at any time from six (6) months prior to the start date of their overseas program, but no earlier. Where students intending to participate in an Exchange program have all the necessary documentation and approvals, it is recommended t ...

**Excerpt 3** - VET Students Policy / VET Students Policy (score 0.220)

> Section 1 - Key Information Section 2 - Purpose Section 3 - Scope Section 4 - Key Decisions Section 5 - Policy Statement Section 6 - Procedures Part A - Information for Students Part B - Admission Applications Selection Offers Part C - Credit and Recognition of Prior Learning Credit Recognition of Prior Learning Part D - Enrolment Part E - Fees Fee Conditions Setting of Fees Payment of Fees Financial Hardship Failure to Pay Fees Tuition Assurance/Fee Protection Refund of Fees Part F - Student Support Part G - Student Conduct Part H - Academic Integrity Part I - Review Section 7 - Definitions Section 8 - Authority and Associated Information

**Excerpt 4** - Short Courses Policy / Part D - Registration (score 0.106)

> (26) Entry requirements for some short courses may include a requirement for professional registration, or a specified level of experience or proficiency in a relevant area. Applicants seeking registration in a short course of the University: are advised of any required prior knowledge or experience; must meet the pre-requisites of that course, where they exist. (27) Domestic and Non-Resident applicants are eligible to apply for short courses. (28) International participants are not eligible for a student visa based on their registration in a short course. International students on a student visa who seek to register in a short course: must also be enrolled in a CRICOS-registered course; are not eligible to register in a short course in addition to their award course enrolment where they intend to apply for credit towards any AQF qualification. (29) Applications for short courses are mad ...

**Excerpt 5** - International Students Release Policy / Section 5 - Policy Statement (score 0.020)

> (3) International students are free to transfer to another registered provider after completing six calendar months of study from the commencement of classes in their principal course, and in these circumstances are not required to obtain approval for a Release. (4) Students wishing to withdraw prior to the first six calendar months of study from the commencement of classes in their principal course are required to obtain approval for a Release. Please note: a Leave of Absence (a break from studies) is not counted towards the six calendar months calculation. (5) The Procedures outline the conditions under which a student may apply for a Release prior to six months and the steps for application and appeal.

</details>

---

### 14. How are applications for admission assessed?

- **Status:** success  
- **Confidence:** high  
- **Top rerank score:** 0.971  
- **Response time:** 3.6s
- **Note:** ACCEPTANCE TEST for PCOIS2-49. Retrieval hands this Academic Promotions text at 0.795, well above threshold. A fluent answer about promotion committees is a hallucination and a fail

**Answer:**

> Applications for admission are assessed based on merit, capacity, and strategic priorities, with consideration given to the applicant's reasonable expectation of success in their chosen graduate research degree and the availability of appropriate supervisory experience and resources. Applicants who meet the entry requirements are considered for selection but are not guaranteed admission, as the final decision is at the sole discretion of La Trobe University.

**Citations:**

- Recruitment Policy - Part I - Screening and Shortlisting Applicants (https://policies.latrobe.edu.au/document/view.php?id=56)
- Graduate Research Admissions Policy - Part B - Academic Entry Requirements (https://policies.latrobe.edu.au/document/view.php?id=113)
- Academic Promotions Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=76)
- Graduate Research Admissions Policy - Section 5 - Policy Statement (https://policies.latrobe.edu.au/document/view.php?id=113)

**Flags:**

- ROUTING: expected low_confidence, got success

<details><summary>Excerpts the model was given</summary>

**Excerpt 1** - Recruitment Policy / Part I - Screening and Shortlisting Applicants (score 0.971)

> (38) All applications are to be treated confidentially and assessed according to suitability and capability required to perform the position. (39) Applications submitted are assessed against the essential criteria, capability, skills and experience required for the position. These assessments are informed by and may include: Resume Video question responses Written question responses Essential criteria responses Any other relevant assessments as required

**Excerpt 2** - Graduate Research Admissions Policy / Part B - Academic Entry Requirements (score 0.894)

> (28) Applicants seeking admission on equity or alternative entry grounds must address the following special requirements with their application: provide a statement describing their circumstances and why they believe they should be considered for entry to a higher degree by research; provide a statement to show how they possess knowledge equivalent to the AQF level learning outcomes that pertain to the qualifying degree, pursuant to discipline expectations; provide a statement that demonstrates their capacity to undertake a graduate research degree in their chosen field or discipline; and provide documentation that substantiates (in writing and/or, where relevant, other forms of evidence) points b. and c. above. (29) The Graduate Research School will provide a template form and set of instructions for how to submit an application on equity or alternative entry grounds, available on the G ...

**Excerpt 3** - Academic Promotions Policy / Section 5 - Policy Statement (score 0.795)

> Academic staff will be provided with appropriate advice and support in the preparation of applications and will receive clear and timely feedback on the outcomes; Applications will be assessed on the evidence provided about the quality, outcomes and impact of contributions holistically across domains; Application and assessment will be based on demonstrated performance, relative to opportunity. Applications from under-represented groups will be actively encouraged; Evidence will be assessed over an academic staff member’s entire career, however more significance will be placed on achievements, outputs and impact in the period since last promotion or appointment to the current academic level; Applications will be judged on their merit, there are no quotas on the number of staff promoted annually. In the case of a successful promotion outcome, it is the responsibility of the relevant acade ...

**Excerpt 4** - Graduate Research Admissions Policy / Section 5 - Policy Statement (score 0.553)

> (4) La Trobe University’s graduate research application processes are transparent, equitable and clearly communicated to prospective applicants. (5) La Trobe University admits applicants based on the consideration of merit, capacity, and strategic priorities and makes offers of a place to applicants assessed as having a reasonable expectation of success in their chosen graduate research degree and only where appropriate supervisory experience and resources are available. (6) Applicants who meet the entry requirements will be considered for selection but are not guaranteed admission to graduate research degrees. The decision of whether to offer a place is at the sole discretion of La Trobe University, and may be subject to factors beyond the specific merit of an individual’s application. (7) Academic Board approves minimum entry requirements and English language requirements for La Trobe  ...

**Excerpt 5** - Academic Promotions Policy / Part C - Referee and External Assessor Reports (score 0.463)

> (50) After the outcome of the application is known the applicant (and/or their Dean) may be provided with copies of the assessor reports where assessors have agreed to make them available. Assessors may elect not to make their report to available to the applicant/Dean by indicating in their report.

</details>

---

### 15. How do I book a car parking permit on campus?

- **Status:** low_confidence  
- **Confidence:** low  
- **Top rerank score:** 0.876  
- **Response time:** 2.8s
- **Note:** Out-of-scope control - scored 0.000, must not reach the model

**Answer:**

> The available policy information does not provide enough detail to answer this question confidently.

**Citations:**

- Campus Access, Premises and Facilities Policy - Part B - Parking (https://policies.latrobe.edu.au/document/view.php?id=434)
- University Vehicle Fleet Policy - Part C - Vehicles (https://policies.latrobe.edu.au/document/view.php?id=257)
- University Vehicle Fleet Policy - Part D - Car Share (GoGet) Vehicles (https://policies.latrobe.edu.au/document/view.php?id=257)

**Flags:**

- ROUTING: expected out_of_scope, got low_confidence

---

### 16. What food is available at the campus cafe today?

- **Status:** out_of_scope  
- **Confidence:** low  
- **Top rerank score:** 0.001  
- **Response time:** 0.4s
- **Note:** Out-of-scope control - scored 0.000, must not reach the model

**Answer:**

> I could not find relevant information in the available La Trobe University policy documents.

---

## Observations

**1. Corpus expansion resolved two previously unexplained refusals.**
Questions 12 and 13 both refused in earlier runs against the five-policy
corpus. Both now answer. Question 12 draws on the English Language Entry
Requirements Policy at 0.995, and question 13 on VET Students Policy - Part C
- Credit and Recognition of Prior Learning at 0.834. Neither document existed
in the pilot corpus. The model was correct to decline in the earlier runs -
the answers genuinely were not in the excerpts it was given - which is
evidence the refusal behaviour is working as intended rather than being
over-cautious.

**2. No hallucinated figures across any run.**
Zero unsupported numbers in every run to date. Eight questions carry
UNSUPPORTED TERMS flags, all of which are ordinary connecting verbs the model
used while paraphrasing - "involves", "includes", "details", "factors",
"serves". The term check is deliberately noisy so that genuine inventions are
not missed; the number check is the reliable signal and it remains clean.

**3. Question 14 regressed, and it is the most serious finding.**
Against the pilot corpus, the model was handed Academic Promotions text and
correctly ignored it, answering from the Admissions Policy excerpts. With the
full corpus it answers from the Graduate Research Admissions Policy instead -
rules for PhD applicants, presented as though they apply to admission
generally. The answer is fluent, confident, and wrong for most people who
would ask this question.

Diagnosis by running retrieval at top-20: the Admissions Policy appears only
at rank 9, scoring 0.191, behind Recruitment Policy (0.971), Graduate
Research Admissions (0.894) and Academic Promotions (0.795). Three policies
about assessing applications now outrank the one about assessing admissions.
Increasing top-k would not fix this - the correct chunk arrives buried under
four confident wrong ones.

**4. The root cause of question 14 is corpus scope, not ranking.**
At rank 20 the diagnostic returned Admissions Policy - Section 6 -
Procedures, which reads in full: "Refer to: Admissions Procedure, Admissions
Schedule, Admissions Procedure - Credit, Admissions Standard - Credit". The
Admissions Policy does not state how applications are assessed; it delegates
that to a Procedure. Discovery filtered the Policy Library on Document Type =
Policy, so Procedures, Standards and Schedules were never ingested. No amount
of retrieval tuning can surface an answer that is not in the corpus.

This is a scoping decision for the team rather than a defect. The project
brief specifies the "Policy Database", and Procedures are documents within
that library. Questions 11, 13 and 14 all trace to the same exclusion.

**5. Citation integrity degraded as the corpus grew.**
Question 14 carries four citations spanning Recruitment, Graduate Research
Admissions and Academic Promotions - three unrelated domains for a single
answer. Question 4's answer about academic progression cites the Student
Support Policy alongside the correct one. Question 10 cites the Outside
Studies Program for Academic Staff Policy. build_citations() attaches every
chunk above the 0.50 threshold regardless of whether the answer drew on it,
and with a larger corpus more unrelated chunks clear that bar. For a system
whose purpose is source-referenced answers, citations that do not correspond
to the answer undermine the core value. Raised for PCOIS2-50.

**6. Question 5 produced a self-contradictory answer.**
The response states that students may appeal a determination of academic
misconduct, then adds "the excerpts do not specifically mention appealing an
academic progression decision" - answering a different question and then
disclaiming it. It also breaches Rule 6 by referring to the excerpts
directly. Retrieval handed it appeals provisions from three separate policies
(Academic Progression Review, Student Academic Misconduct, Graduate Research
and RTP Scholarships) and the model blended them. The same collision pattern
as question 14, with a different outcome.

**7. Question 15's routing flag reflects a stale expectation, not a fault.**
The test still expects out_of_scope because the question was written as a
control against the five-policy corpus. There is now a Campus Access,
Premises and Facilities Policy with a Part B on Parking, so the question is
in scope. The model retrieved it, judged that it does not explain how to book
a permit, and declined. That is correct behaviour. The expectation should be
updated, as was done for the retrieval test set.

**8. Genuine out-of-scope detection still works.**
The campus cafe control scores 0.001 and is filtered before generation.
Question 11 scores 0.107 and is likewise filtered. With 140 policies there is
almost always something topically adjacent, so the fact that clearly
unanswerable questions still score near zero indicates the reranker is
discriminating on answerability rather than topic overlap.

**9. Response times remain acceptable.**
3-4 seconds per generated answer after model load, under 1 second for
filtered questions. The 42.9s on question 1 is first-call model loading, not
representative.

**Overall.** Grounding held through a 28x corpus expansion: no invented
figures, no fabricated policy content. Two content gaps closed. The new
failure mode is semantic collision - student, staff and graduate-research
policies sharing vocabulary such as "applications assessed" and "appeal a
decision" - which retrieval alone cannot resolve because the distinguishing
context is not in the chunk text. Two candidate mitigations for Sprint 4:
ingest Procedures and Standards so the correct answer exists in the corpus,
and use the category field already stored on each chunk to bias retrieval
toward the relevant domain.
