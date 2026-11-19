# ADR-0001: Fokus Law Greenfield stack and environment boundaries

- Status: Accepted
- Decision owner: Jorge, developer
- Decision date: 2026-11-18
- Recorded in this repository: 2026-11-19
- Scope: Synthetic MVP for Fokus Cloud Law — 1ª Vara Crime de Ilhéus
- Source decisions: [Linear REI-195](https://linear.app/reis-developer/issue/REI-195/vara-definir-arquitetura-greenfield-e-fronteiras-dos-ambientes) and the approved [PRD](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a) (sections 1, 7, 8, 9 and 10.1)

## Context

The product is a Greenfield application for the synthetic MVP. The approved scope has one developer, a server-rendered operational workflow, and no automatic migration of code or data from legacy systems. The authorized KVM1 is shared with existing production services, so synthetic co-hosting requires logical separation and evidence before activation. Institutional data, production use, PJe integration, and institutional homologation are outside this decision.

The architecture must support the Pessoa → Processo → Expedição workflow while keeping identity, authorization, audit, storage, and backup boundaries explicit. The runtime and capacity of the actual host, the application isolation controls, and end-to-end recovery are separate verification gates.

## Options considered

### 1. Modular Laravel monolith with server-rendered Blade — selected

- Pros: one application and runtime to build and operate; fits the PHP/Laravel hosting already selected; avoids a separate frontend/API boundary for the MVP.
- Cons: module boundaries and server-side authorization must be enforced within one application; a shared host still shares operating-system, resource, availability, and recovery failure domains.

### 2. Django 5.2 LTS with PostgreSQL

- Pros: mature framework with built-in authentication, groups, and permissions.
- Cons: introduces a second framework ecosystem for this product and still requires a separate MFA integration and hosting compatibility work.

### 3. Separate SPA and API

- Pros: separates frontend deployment from API implementation and permits independent clients.
- Cons: adds an API contract, deployment surface, and authentication boundary without a required MVP client or workflow that benefits from the split.

The alternatives and tradeoffs above reflect the options recorded in the approved REI-195 decision; no additional product or infrastructure option is implied.

## Decision

Use a modular monolith in Laravel 13 and PHP 8.5, with MySQL 8.4 LTS using InnoDB and Blade-rendered pages. Keep modules within the application; do not create separate frontend/API services for this MVP. The project is Greenfield and does not automatically migrate legacy code or data.

For synthetic development, use individual accounts with MFA and server-side authorization that denies ungranted modules and actions by default. Self-registration remains pending and grants no functional access. Only Jorge approves test accounts and explicitly grants modules, action sets, units, and secrecy levels. Login, invitation, and TOTP setup alone do not grant access. Support autonomy does not grant account-approval or access-provisioning powers.

The synthetic environment may share the KVM1 with existing production only after the developer approves activation and the controls in PRD section 10.1 are evidenced. This is logical separation, not infrastructure isolation. The application must use dedicated site directories and PHP-FPM pool, MySQL database and user, credentials, keys, sessions, and storage; contain no production data, secrets, or integrations; and pass negative cross-product access tests. No remote deployment or activation is authorized by this ADR.

For the synthetic MVP, backups are application-specific, encrypted before transfer, and sent to the separate local workstation over a protected outbound-initiated path. The approved monthly process, retention, key separation, capacity checks, and restore acceptance remain governed by PRD section 8.3. This backup decision does not apply to real or production data.

## Consequences

- The first release can be built and tested as one Laravel application with a relational schema and server-rendered UI.
- Functional module, unit, secrecy, and record-level authorization must be enforced in server-side code and verified with positive and negative tests.
- Shared KVM1 resources and failure domains remain a material risk; the approved synthetic environment cannot be activated until logical isolation, network exposure, capacity, and recovery gates pass.
- The current bootstrap and CI establish only a local development baseline. They do not demonstrate the workflow, complete authorization, KVM1 isolation, production readiness, or backup/restore.
- Later requirements for institutional identity, real data, production policy, retention, RPO/RTO, or external integration require separate authorization and a superseding decision where they change this architecture.

## Verification record

- Decision authority and selected stack: recorded in REI-195 and approved PRD, retrieved on 2026-11-19.
- Alternatives, tradeoffs, selected decision, and consequences: present in this ADR.
- Synthetic/production boundary and activation gates: cross-checked against PRD section 10.1 on 2026-11-19; all infrastructure gates remain open.
- No PJe integration, import, institutional data, or homologation is added by this ADR.
- This record documents an existing approved decision; it does not constitute runtime, security, deployment, or institutional acceptance evidence.
