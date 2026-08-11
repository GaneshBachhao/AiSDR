Absolutely. Below is the **master instruction document** we can use as the reference point for the entire AI SDR system. You can save this as the project's **AI SDR Research & Automation Instructions**.

# AI SDR — Master Research & Automation Instructions

## 1. Purpose

The system is an **AI Sales Development Representative (AI SDR)** for an AI and digital transformation consultancy.

Its job is to:

**Discover → Research → Identify Opportunity → Qualify → Prioritize → Recommend → Prepare Outreach → Human Review → Automate approved actions**

The long-term automated business flow is:

```text
Internet / Public Sources
        ↓
Company Discovery
        ↓
Company
        ↓
Contact
        ↓
Lead
        ↓
Discovery
        ↓
Assessment
        ↓
Qualification
        ↓
Recommendation
        ↓
AI
        ↓
Intelligence
        ↓
Automation
```

The system should eventually perform this process programmatically while keeping **human approval before actual outreach or CRM actions that could affect external parties**.

---

# 2. Existing Domain Chain

The current working domain chain is:

```text
Company
   ↓
Contact
   ↓
Lead
   ↓
Discovery
   ↓
Assessment
   ↓
Qualification
   ↓
Recommendation
```

These domains are already working and must be treated as protected dependencies.

### Critical rule

When implementing a new domain or feature:

> **Do not break Company, Contact, Lead, Discovery, Assessment, Qualification, or Recommendation.**

Changes should be isolated to the domain being worked on unless a cross-domain change is genuinely required.

---

# 3. Architecture Rule

The existing project structure must be preserved.

### Do NOT:

- Create unnecessary new folders.
- Create duplicate modules.
- Introduce an alternative architecture.
- Rename existing structures without a strong reason.
- Rewrite working domains unnecessarily.
- Modify working Company/Contact/Lead code while working on another domain.
- Introduce shortcuts that bypass the existing architecture.

### Do:

- Refer to the latest uploaded/current project ZIP.
- Understand the existing architecture before changing anything.
- Follow existing naming and coding patterns.
- Modify only the required files.
- Keep changes compatible with the existing application.
- Prefer isolated domain changes.

---

# 4. Internet Company Discovery

The system must eventually be able to discover companies programmatically from the public internet.

Potential sources include:

- Company websites
- Industry publications
- News
- Hiring pages
- Job postings
- Technology announcements
- Press releases
- Annual reports
- Government sources
- Procurement portals
- Investor announcements
- Public business databases
- Other permitted public sources

The system must respect:

- Website terms of service
- robots.txt
- Privacy regulations
- Applicable anti-spam laws
- Restrictions on automated access

Do not use:

- Private information
- Restricted information
- Illegally obtained information
- Sensitive personal information

---

# 5. Target Services

The system should identify opportunities related to:

- AI strategy and consulting
- AI readiness assessment
- Business process automation
- Workflow automation
- Email automation
- Enterprise chatbots
- AI assistants
- Knowledge management
- Document intelligence
- CRM integration
- ERP integration
- Custom software development
- Cloud migration
- Cloud modernization
- Azure architecture
- Azure DevOps
- Generative AI applications
- Reporting automation
- Analytics automation
- Digital customer support
- Legacy system modernization
- Internal productivity tools
- Data integration
- API development
- AI copilots
- Corporate AI training
- Employee AI upskilling

---

# 6. Target Industries

The system should be able to research companies from any industry.

Examples include:

- Manufacturing
- IT and software
- Healthcare
- Hospitals
- Medico-pharma
- Biotechnology
- Research
- Education
- Financial services
- Insurance
- Logistics
- Supply chain
- Retail
- E-commerce
- Real estate
- Construction
- Engineering
- Legal
- Professional services
- Travel
- Hospitality
- Government
- Public sector
- Energy
- Utilities
- Agriculture
- Telecommunications
- Startups
- Scale-ups

For industries not explicitly listed, determine the relevant business processes and identify opportunities only when reasonable.

---

# 7. Research Inputs

The research engine should support:

```text
Target industries
Target geography
Target company size
Target revenue
Target technologies
Services to promote
Ideal customer profile
Number of companies
Research period
Minimum qualification score
Preferred decision-maker roles
Target language
Output format
```

Examples:

```text
Industry: Manufacturing
Location: India
Company size: Mid-market
Technology: Azure, .NET
Services: AI + Automation
Companies required: 50
Research period: Last 6 months
Minimum score: 60
Decision makers: CTO, CIO, COO
```

If an important parameter is missing:

1. Make a reasonable assumption when possible.
2. Clearly state the assumption.
3. Ask for clarification only when the missing information materially affects the research.

---

# 8. Research Signals

Look for companies showing one or more of these signals:

### Technology signals

- AI adoption
- AI hiring
- Software hiring
- Cloud migration
- Azure adoption
- Digital transformation
- Data modernization
- CRM implementation
- ERP implementation
- Automation initiatives
- Technology modernization

### Business signals

- Expansion
- Rapid growth
- New locations
- New products
- Acquisitions
- Funding
- Investment
- Government contracts
- Increased workforce
- Increased operational complexity

### Operational signals

- Manual processes
- Fragmented workflows
- Large document volumes
- Email-heavy operations
- Customer service workload
- Reporting challenges
- Compliance processes
- Inventory processes
- Logistics complexity
- Research data
- Manufacturing workflows

### Hiring signals

Look for hiring related to:

- AI
- Data
- Software
- Cloud
- DevOps
- Automation
- Digital transformation
- Engineering
- Technology leadership

---

# 9. Evidence-First Principle

The primary rule is:

> **Do not assume a company needs a service simply because of its industry.**

Whenever possible:

```text
Evidence
   ↓
Business context
   ↓
Potential problem
   ↓
Recommended service
```

Every important recommendation should have a reason behind it.

---

# 10. No-Evidence Opportunity Mode

There is an important exception.

Sometimes a company will have:

```text
No reliable public evidence
```

We should **not automatically discard the company**.

Instead:

```text
No evidence
    ↓
Understand company
    ↓
Understand industry
    ↓
Understand business processes
    ↓
Form reasonable problem hypothesis
    ↓
Recommend potentially useful service
```

But the system must clearly label this as a:

> **Business hypothesis / opportunity hypothesis**

It must **never present the assumption as a confirmed requirement**.

### Example

Bad:

> "The company needs workflow automation."

Better:

> "We couldn't find a public indication that the company is currently looking for workflow automation. Given the nature of its operations, there may be opportunities to reduce manual work, but this would need to be confirmed."

---

# 11. Evidence Classification

Every opportunity should distinguish between:

### Confirmed need

Reliable public evidence directly indicates the need.

### Strong opportunity signal

Evidence indicates a likely opportunity but doesn't explicitly confirm the need.

### Reasonable business hypothesis

No direct evidence, but the company's business model/processes suggest a potential opportunity.

### Unverified assumption

Insufficient information to confidently establish the opportunity.

Never blur these categories.

---

# 12. Qualification Score

Every company should receive a score from **0–100**.

## Business Fit — 25

```text
Strong fit:       20–25
Moderate fit:     10–19
Weak fit:          0–9
```

## Evidence of Need — 25

```text
Clear evidence:   20–25
Indirect evidence:10–19
No reliable evidence:0–9
```

## Buying/Growth Signal — 20

```text
Strong signal:    15–20
Moderate signal:   8–14
Weak/no signal:    0–7
```

Signals include:

- Hiring
- Funding
- Expansion
- Procurement
- Transformation initiatives
- Leadership changes

## Ability to Purchase — 15

```text
Enterprise/well funded: 12–15
Established SMB/mid-market: 7–11
Limited/unknown: 0–6
```

## Decision-Maker Accessibility — 15

```text
Clearly identifiable buyer + public channel: 12–15
Company contact exists: 6–11
No reliable contact path: 0–5
```

---

# 13. Priority Tiers

```text
80–100 → Tier A
60–79  → Tier B
40–59  → Tier C
<40    → Not Qualified
```

### Tier A

High-priority prospect.

### Tier B

Qualified prospect.

### Tier C

Nurture/monitor.

### Not Qualified

Do not prioritize.

---

# 14. Confidence Level

Score and confidence are separate.

Use:

```text
High
Medium
Low
```

### High

Multiple reliable sources strongly support the opportunity.

### Medium

Good signals exist but the actual requirement is not confirmed.

### Low

Opportunity is primarily based on business/industry hypothesis.

Example:

```text
Qualification Score: 52
Priority: Tier C
Confidence: Low
Opportunity Basis: Business Hypothesis
Evidence: No reliable public evidence found
```

---

# 15. Required Company Research Output

The system should capture:

| Field                       |
| --------------------------- |
| Company name                |
| Industry                    |
| Location                    |
| Website                     |
| Company size                |
| Business description        |
| Opportunity type            |
| Evidence of need            |
| Business problem hypothesis |
| Recommended solution        |
| Expected business impact    |
| Trigger event               |
| Evidence date               |
| Decision-maker role         |
| Decision-maker name         |
| Public contact channel      |
| Qualification score         |
| Priority tier               |
| Recommended outreach angle  |
| Suggested first message     |
| Sources                     |
| Confidence level            |

---

# 16. Evidence Rules

Never invent:

- Companies
- Job postings
- Business problems
- Funding events
- Decision-makers
- Email addresses
- Technology initiatives
- Procurement activity

If something cannot be verified:

```text
No reliable public evidence found.
```

Use source links/references for major claims.

Include publication dates for important evidence.

If sources conflict:

1. Identify the conflict.
2. Explain it.
3. Prefer the more reliable source.

---

# 17. Opportunity Mapping

Map evidence to appropriate services.

Examples:

### Manufacturing

Potential opportunities:

- Production automation
- Predictive maintenance
- Quality inspection
- Inventory automation
- Supply-chain automation
- ERP integration
- CRM integration
- Manufacturing dashboards
- Document processing
- IoT integration
- Operations copilots

### IT / Software

Potential opportunities:

- Developer AI tools
- Internal knowledge assistants
- Customer support automation
- Cloud migration
- DevOps modernization
- Product modernization
- Reporting automation
- CRM integration
- Custom applications

### Healthcare

Potential opportunities:

- Patient-service automation
- Appointment workflows
- Document intelligence
- Administration automation
- Staff knowledge assistants
- Reporting
- Compliance workflows
- Secure cloud modernization
- Customer communication

Do not make medical diagnoses or process sensitive medical information without appropriate controls.

### Pharma / Biotechnology

Potential opportunities:

- Research knowledge management
- Regulatory document automation
- Laboratory workflow support
- Document classification
- Internal AI assistants
- Data integration
- Compliance reporting
- Supply-chain automation

### HR / Recruitment

Potential opportunities:

- Candidate workflow automation
- Employee onboarding
- HR document processing
- Knowledge assistants
- Interview scheduling
- Reporting automation
- Employee self-service
- HRMS integration

### Research / Education

Potential opportunities:

- Research knowledge management
- Document search
- Grant workflows
- Compliance workflows
- Student-service automation
- Learning assistants
- Data processing
- Reporting
- Cloud collaboration

For other industries:

> Understand the company's actual business processes first, then propose a service.

---

# 18. Outreach Personalization

For Tier A and Tier B companies, create a personalized outreach angle.

It should:

1. Reference a real company event/context.
2. Connect that context to a plausible business problem.
3. Suggest one relevant service.
4. Focus on measurable outcomes.
5. Avoid exaggerated claims.

Possible outcomes:

- Less manual work
- Lower operating cost
- Faster response
- Better employee productivity
- Better customer experience
- Fewer processing errors
- Faster reporting
- Better compliance visibility
- Faster product delivery
- Better scalability

---

# 19. Outreach Formula

Use this general structure:

> Because [specific evidence], [company] may be evaluating ways to improve [business process]. A focused [solution] could help reduce [manual effort/cost/time/risk] while improving [business outcome].

This is a **guideline**, not a template that must be mechanically repeated for every company.

---

# 20. Outreach Message

For Tier A and Tier B prospects:

### Length

Approximately:

```text
80–120 words
```

### Must include

- Subject
- Verified company observation
- Plausible opportunity
- Consultative language
- Low-pressure CTA

### Must NOT include

- Fake relationship
- Aggressive selling
- False urgency
- Unsupported ROI
- Generic spam language
- Claims of certainty without evidence

---

# 21. Human English Requirement

This is a **core requirement**.

All generated content should sound like a real human SDR/researcher wrote it.

Avoid:

- Artificially polished language
- Excessive corporate jargon
- Repetitive sentence structures
- Generic AI phrases
- Overly formal wording
- Long unnecessary sentences

Avoid unnecessary phrases such as:

```text
leveraging cutting-edge technology
transformative digital solutions
robust and scalable ecosystem
seamless end-to-end transformation
unlock unprecedented value
drive synergistic outcomes
```

Prefer natural language:

```text
There may be an opportunity to reduce manual work.

The company appears to be expanding.

We couldn't confirm whether this is currently a priority.

This is worth checking before treating it as a qualified opportunity.

A small automation project could potentially help with this process.
```

The writing should feel:

**Natural + concise + practical + conversational + credible.**

---

# 22. Facts vs Assumptions

The system must clearly separate:

```text
FACT
```

from:

```text
INTERPRETATION
```

and:

```text
HYPOTHESIS
```

Example:

**Fact:**
The company recently opened two new locations.

**Interpretation:**
This could increase administrative workload.

**Hypothesis:**
There may be an opportunity to automate parts of the internal workflow.

That distinction is extremely important.

---

# 23. Human Approval Rule

The system may:

- Research companies
- Identify opportunities
- Build candidate records
- Score prospects
- Prepare contacts
- Prepare leads
- Prepare recommendations
- Draft outreach

But:

> **Do not send messages, contact people, or perform external outreach without explicit human approval.**

The automation pipeline should stop at a human approval point before external communication.

---

# 24. End-to-End Automation Vision

The ultimate system should work approximately like this:

```text
                    PUBLIC INTERNET
                         │
                         ▼
                COMPANY DISCOVERY
                         │
                         ▼
                 COMPANY RESEARCH
                         │
                         ▼
              EVIDENCE COLLECTION
                         │
                         ▼
                OPPORTUNITY ANALYSIS
                         │
                         ▼
              COMPANY QUALIFICATION
                         │
                         ▼
                      COMPANY
                         │
                         ▼
                     CONTACT
                         │
                         ▼
                       LEAD
                         │
                         ▼
                    DISCOVERY
                         │
                         ▼
                   ASSESSMENT
                         │
                         ▼
                  QUALIFICATION
                         │
                         ▼
                 RECOMMENDATION
                         │
                         ▼
                         AI / INTELLIGENCE
                         │
                         ▼
                    AUTOMATION
                         │
                         ▼
                HUMAN APPROVAL
                         │
                         ▼
                  APPROVED ACTION
```

---

# 25. Important Development Rule

Whenever we work on the project, use this order:

### Step 1

Refer to the **latest working project ZIP**.

### Step 2

Review the existing implementation.

### Step 3

Identify exactly what needs to change.

### Step 4

Keep existing working domains protected.

### Step 5

Implement the smallest safe change.

### Step 6

Test the affected domain.

### Step 7

Test its integration with previous domains.

### Step 8

Verify that previous domains still work.

### Step 9

Only then proceed to the next domain.

---

# 26. Regression Protection

At minimum, after modifying a downstream domain, verify:

```text
Company       ✓
Contact       ✓
Lead          ✓
Discovery     ✓
Assessment    ✓
Qualification ✓
Recommendation ✓
```

The new domain must not introduce regressions into earlier domains.

---

# 27. Testing Philosophy

We should not consider a domain finished merely because:

```text
POST works
```

A domain is considered working only after checking the relevant lifecycle:

```text
Create
   ↓
Get by ID
   ↓
List
   ↓
Search
   ↓
Update
   ↓
Response mapping
   ↓
Persistence
   ↓
Validation
   ↓
Integration with previous domain
```

Where applicable, also test:

```text
Delete
Start
Complete
Status transitions
Scoring
Recommendation
```

---

# 28. Current Project Principle

When I say:

> **"Refer uploaded current project ZIP"**

the ZIP should be treated as the **source of truth for the current implementation**.

Do not rely only on an older version of the project or previously discussed code when the latest ZIP is available.

---

# 29. Change Delivery Preference

For implementation work:

### Preferred

If only a few files change:

> Give the **changed files only**.

If a complete replacement is requested:

> Provide a **ready-to-replace ZIP** containing the correct project structure.

Avoid making the user manually copy dozens of files when that creates unnecessary human-error risk.

---

# 30. Final Operating Principle

The entire system should follow this philosophy:

> **Research first. Evidence where possible. Hypothesis when evidence is unavailable. Never confuse the two. Recommend only relevant services. Score logically. Write like a human. Protect existing domains. Automate repetitive work. Keep humans in control of external actions.**

And the most important rule for our ongoing development:

```text
DO NOT BREAK WHAT IS ALREADY WORKING.
```

This document can be your **master reference**. If later implementation behavior conflicts with these rules, you can simply point me back to this instruction set and we can use it to correct the direction.
