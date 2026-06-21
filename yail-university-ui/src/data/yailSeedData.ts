import type { Course, Degree, Student } from "../types";

const studentV0Code = `model: claude-haiku-4-5
agent_type: claude
system_prompt: null

Runs GDPval course tasks and autonomous-business capstone tasks with no YAIL-specific workflow scaffold.`;

const studentV1Code = `You are a YAIL University student worker.

Your role is to produce reliable professional work products, not just a written explanation.

General operating policy:
1. Read the task carefully and identify the exact deliverable path and file type.
2. Inspect the available reference files directly.
3. Convert the brief into a short checklist of visible requirements.
4. Build the requested native artifact at the exact requested path.
5. Preserve traceability: identifiers, names, dates, source columns, and row relationships.
6. Verify the artifact before finishing.
7. Do not claim completion until the requested file exists and has been checked.`;

const drAtlasV1Code = `You are Dr. Atlas, a YAIL University PhD candidate worker.

Your job is to produce correct professional artifacts and leave a trace that can teach future trainable agents.

Core policy:
1. Identify the requested deliverable, output path, file type, and visible success criteria.
2. Inspect the real workspace files before deciding.
3. Make a compact requirement checklist from the prompt.
4. Build the required native artifact or business action.
5. Preserve traceability: IDs, row relationships, source columns, timestamps, and labels.
6. Verify your own output by reopening or re-querying the artifact/state.
7. Avoid hidden-rubric guessing and reward-target vocabulary.
8. Leave short observable checkpoints for QA and future SFT/RL data selection.`;

const drAtlasV2Code = `model: yail-dr-atlas-qwen30b-smoke-20260621181803
base_model: Qwen/Qwen3-30B-A3B
training: HUD Training PPO
checkpoint: step-000001
learning_rate: 1e-6
training_batch: acct-audit-easy group=4
mean_reward: 0.322723

Status: checkpoint created, but post-training held-out rerun has not passed yet.`;

export const degrees: Degree[] = [
  {
    id: "certificate",
    name: "Certificate",
    purpose: "Basic role readiness through placement tasks and deterministic course checks.",
    cost: "100 YAIL Credits",
    lanes: "1x compute lane",
    status: "available",
    requirements: ["Intro assignments", "Course score threshold", "No severe QA findings"]
  },
  {
    id: "diploma",
    name: "Diploma",
    purpose: "Prompt, tool, and workflow hardening for a role-specific worker.",
    cost: "350 YAIL Credits",
    lanes: "2x compute lanes",
    status: "available",
    requirements: ["Multiple courses", "QA trace review", "One approved version change"]
  },
  {
    id: "degree",
    name: "Degree",
    purpose: "Versioned specialization with measurable improvement over a baseline worker.",
    cost: "900 YAIL Credits",
    lanes: "4x compute lanes",
    status: "candidate",
    requirements: ["Full role curriculum", "Version timeline", "Held-out course checks"]
  },
  {
    id: "residency",
    name: "Residency",
    purpose: "Real business-environment validation inside autonomous-business capstones.",
    cost: "1,800 YAIL Credits",
    lanes: "6x compute lanes",
    status: "candidate",
    requirements: ["Integrated workflow tasks", "Customer/business outcome checks", "Capstone regression"]
  },
  {
    id: "phd",
    name: "PhD",
    purpose: "Custom model optimization through SFT/RL after enough validated reward signal exists.",
    cost: "5,000+ YAIL Credits",
    lanes: "8-16x compute lanes",
    status: "experimental",
    requirements: ["Validated trace dataset", "Reward spread", "Trainable model fork", "Held-out board exam"]
  }
];

export const courses: Course[] = [
  {
    id: "classification",
    title: "Ticket Classification",
    objective: "Map customer tickets to the correct labels under a policy taxonomy.",
    environment: "YAIL support-ops taskset",
    dataSource: "Planned YAIL support-ops synthetic ticket set derived from autonomous-business case shapes.",
    taskData: ["policy taxonomy labels", "customer ticket text", "hidden validation tickets"],
    trainedAgents: ["Nova-0"],
    model: "claude-haiku-4-5",
    grader: "Exact label accuracy with optional partial credit",
    qaChecks: ["False positive analysis", "Prompt alignment", "Coverage check"],
    criteria: "Graduate when held-out classification accuracy clears the role target.",
    evidence: [
      {
        agent: "Nova-0",
        version: "student-v0",
        task: "placement",
        score: null,
        note: "Placement run not started; this course is the intake baseline."
      }
    ]
  },
  {
    id: "workflow-design",
    title: "Workflow Design",
    objective: "Create JSON routing workflows that satisfy customer requirements and hidden tickets.",
    environment: "autonomous-business template",
    dataSource: "hud-evals/autonomous-businesses-template workflow-routing scenarios.",
    taskData: ["workflow JSON schema", "business requirements", "hidden routing checks"],
    trainedAgents: ["Swift-Track"],
    model: "claude-haiku-4-5",
    grader: "Schema validity and hidden ticket routing accuracy",
    qaChecks: ["Reward hacking analysis", "Missing-label audit", "Schema misuse check"],
    criteria: "Graduate when hidden tickets route correctly without invalid schema shortcuts.",
    evidence: [
      {
        agent: "Swift-Track",
        version: "student-v1-fast",
        task: "parallel workplace sims",
        score: null,
        note: "Fast-track batch is scheduled; no scorecard accepted yet."
      }
    ]
  },
  {
    id: "workflow-debugging",
    title: "Workflow Debugging",
    objective: "Diagnose and fix broken workflow configs from complaints and logs.",
    environment: "autonomous-business template",
    dataSource: "autonomous-business broken workflow cases plus YAIL QA teacher hold examples.",
    taskData: ["broken workflow config", "complaint transcript", "routing logs", "hidden regression tickets"],
    trainedAgents: ["Casey-QA"],
    model: "claude-haiku-4-5",
    grader: "Fixed config improves hidden ticket accuracy",
    qaChecks: ["Failure analysis", "No-op fix detection", "Regression check"],
    criteria: "Graduate when the fix improves the business state and does not break existing routes.",
    evidence: [
      {
        agent: "Casey-QA",
        version: "student-v0",
        task: "workflow-debugging",
        score: null,
        note: "Blocked by QA teacher; not admitted to workplace sim yet."
      }
    ]
  },
  {
    id: "communication",
    title: "Customer Communication",
    objective: "Write honest customer replies after diagnosis and workflow fixes.",
    environment: "autonomous-business template",
    dataSource: "autonomous-business customer-facing cases and policy-grounded response rubrics.",
    taskData: ["customer issue", "resolved workflow state", "policy constraints", "reply quality rubric"],
    trainedAgents: ["Swift-Track", "Casey-QA"],
    model: "claude-haiku-4-5",
    grader: "Policy-grounded tone and factuality judge",
    qaChecks: ["Unsupported promise check", "Policy alignment", "Tone review"],
    criteria: "Graduate when the reply explains the real cause and avoids impossible guarantees.",
    evidence: [
      {
        agent: "Swift-Track",
        version: "student-v1-fast",
        task: "parallel course batch",
        score: null,
        note: "Communication course is part of the pending fast-track batch."
      }
    ]
  },
  {
    id: "knowledge-work",
    title: "GDPval Knowledge Work",
    objective: "Produce native office deliverables like spreadsheets and audit workbooks.",
    environment: "yail-gdpval:v7",
    dataSource: "HUD GDPval environment adapted as yail-gdpval:v7 with deterministic grader diagnostics.",
    taskData: ["acct-afc-audit-sampling workbook", "medsec-pathology-forms dataset", "native spreadsheet/document deliverables"],
    trainedAgents: ["Ledger-1", "Ledger-2"],
    model: "claude-haiku-4-5",
    grader: "Deterministic checks plus HUD-native LLM judge when configured",
    qaChecks: ["Trace failure analysis", "Deliverable verification", "Prompt-grader alignment"],
    criteria: "Graduate when target tasks improve and held-out tasks do not regress.",
    evidence: [
      {
        agent: "Ledger-1",
        version: "student-v0",
        task: "acct-afc-audit-sampling",
        score: 0.369,
        traceId: "4f400d71-22e2-43d9-b8af-39703654e3aa",
        jobId: "e8d134facdec4721b7d1b5aeb662b6ec",
        note: "Baseline selected too much of the population."
      },
      {
        agent: "Ledger-2",
        version: "student-v1",
        task: "acct-afc-audit-sampling",
        score: 0.4275,
        traceId: "fecfac1d-c3a2-4561-a02c-643ba65bc386",
        jobId: "b525dffdfafb4bf99c0d854bca867b78",
        note: "Workflow prompt update improved acct by +0.0585."
      },
      {
        agent: "Ledger-2",
        version: "student-v1",
        task: "medsec-pathology-forms",
        score: 0.5225,
        traceId: "176ff833-d173-4fed-88af-7b9305e7651c",
        jobId: "73409774b9ab44868c15e6e7e72da9f1",
        note: "Tied baseline; kept as no-regression evidence."
      }
    ]
  },
  {
    id: "capstone",
    title: "Business Capstone",
    objective: "Operate inside integrated business environments and produce real outcome improvements.",
    environment: "autonomous-business smoke taskset",
    dataSource: "hud-evals/autonomous-businesses-template capstone scenarios.",
    taskData: ["one_deal_ai_workflow_business", "save_the_account_routing_bug", "business-state verifier"],
    trainedAgents: ["Ledger-2", "Swift-Track", "Dr. Atlas"],
    model: "claude-haiku-4-5 for students; PhD trainable model planned",
    grader: "Hidden business-state verifier",
    qaChecks: ["False positive review", "Reward hacking review", "Customer truthfulness"],
    criteria: "Graduate when business outcome checks pass under hosted HUD runs.",
    evidence: [
      {
        agent: "Ledger-2",
        version: "student-v1",
        task: "one_deal_ai_workflow_business",
        score: 1,
        traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
        jobId: "51b79002efeb4d52b7c242ba1d2136a7",
        note: "Hosted autonomous-business workplace regression passed."
      },
      {
        agent: "Ledger-2",
        version: "student-v1",
        task: "save_the_account_routing_bug",
        score: null,
        note: "Rerun pending because prior hosted attempts hit session-detach invalid runs."
      }
    ]
  }
];

const ledgerScores = {
  acctV0: {
    label: "Acct audit baseline",
    course: "GDPval Knowledge Work",
    task: "acct-afc-audit-sampling",
    score: 0.369,
    evalType: "Simple hosted eval",
    improvement: "Baseline",
    traceId: "4f400d71-22e2-43d9-b8af-39703654e3aa",
    jobId: "e8d134facdec4721b7d1b5aeb662b6ec",
    status: "failed" as const,
    note: "Selected 841 of 1516 rows and failed the sample-not-population check."
  },
  acctV1: {
    label: "Acct audit improved",
    course: "GDPval Knowledge Work",
    task: "acct-afc-audit-sampling",
    score: 0.4275,
    evalType: "Eval after QA/prompt fix",
    improvement: "+0.0585 vs v0",
    traceId: "fecfac1d-c3a2-4561-a02c-643ba65bc386",
    jobId: "b525dffdfafb4bf99c0d854bca867b78",
    status: "candidate" as const,
    note: "Selected 474 rows, passed the sample-not-population check, deterministic score rose to 0.95."
  },
  medsecV0: {
    label: "Medsec baseline",
    course: "GDPval Knowledge Work",
    task: "medsec-pathology-forms",
    score: 0.5225,
    evalType: "Simple hosted eval",
    improvement: "Baseline",
    traceId: "56a02063-376b-435d-bcac-6c3c915c96e5",
    jobId: "9aacd526702741008744b5f355ed1cad",
    status: "candidate" as const,
    note: "Fixed GDPval v7 measurement gave deterministic-only score."
  },
  medsecV1: {
    label: "Medsec v1",
    course: "GDPval Knowledge Work",
    task: "medsec-pathology-forms",
    score: 0.5225,
    evalType: "Eval after QA/prompt fix",
    improvement: "No lift vs v0",
    traceId: "176ff833-d173-4fed-88af-7b9305e7651c",
    jobId: "73409774b9ab44868c15e6e7e72da9f1",
    status: "candidate" as const,
    note: "Tied v0; deterministic routing was strong, QA review still pending."
  },
  oneDealV1: {
    label: "Capstone regression",
    course: "Business Capstone",
    task: "one_deal_ai_workflow_business",
    score: 1,
    evalType: "Held-out business eval",
    improvement: "No regression",
    traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
    jobId: "51b79002efeb4d52b7c242ba1d2136a7",
    status: "passed" as const,
    note: "Held-out autonomous-business regression passed."
  }
};

export const students: Student[] = [
  {
    id: "nova-0",
    name: "Nova-0",
    role: "Customer Support Operations Worker",
    level: "Certificate",
    track: "Standard",
    degreeTarget: "Certificate",
    model: "claude-haiku-4-5",
    currentVersion: "student-v0",
    course: "Placement Exams",
    enrolledCourses: ["Ticket Classification", "GDPval Knowledge Work"],
    latestScore: "No score yet",
    qaStatus: "Not started",
    promotionStatus: "Needs first placement run",
    costUsed: "8 credits",
    costRemaining: "92 credits",
    summary: "A newly enrolled blank student waiting for first HUD placement scorecard.",
    scores: [{ label: "Placement", course: "Ticket Classification", task: "baseline", score: null, evalType: "Placement eval", improvement: "Not started", status: "pending", note: "Placement scorecard pending." }],
    versions: [
      {
        id: "student-v0",
        title: "Initial student",
        status: "created",
        note: "No course attempts yet.",
        sourcePath: "yail-university/versions/student-v0/agent.md",
        codeSnippet: studentV0Code
      }
    ],
    transcript: [
      {
        version: "student-v0",
        environment: "pending",
        task: "placement",
        score: null,
        decision: "Placement pending",
        note: "No HUD run yet."
      }
    ]
  },
  {
    id: "ledger-1",
    name: "Ledger-1",
    role: "Customer Support Operations Worker",
    level: "Diploma",
    track: "Standard",
    degreeTarget: "Degree",
    model: "claude-haiku-4-5",
    currentVersion: "student-v0",
    course: "GDPval Knowledge Work",
    enrolledCourses: ["GDPval Knowledge Work", "Business Capstone"],
    latestScore: "Acct audit 0.369",
    qaStatus: "Needs review",
    promotionStatus: "Baseline recorded",
    costUsed: "142 credits",
    costRemaining: "758 credits",
    summary: "Baseline worker on GDPval course tasks. Useful as the comparison point for YAIL improvement loops.",
    scores: [ledgerScores.acctV0, ledgerScores.medsecV0],
    versions: [
      {
        id: "student-v0",
        title: "Baseline prompt",
        status: "baseline",
        note: "No workflow hardening patch.",
        sourcePath: "yail-university/versions/student-v0/agent.md",
        codeSnippet: studentV0Code
      }
    ],
    transcript: [
      {
        version: "student-v0",
        environment: "yail-gdpval:v7",
        task: "acct-afc-audit-sampling",
        score: 0.369,
        traceId: "4f400d71-22e2-43d9-b8af-39703654e3aa",
        jobId: "e8d134facdec4721b7d1b5aeb662b6ec",
        decision: "Baseline failure",
        note: "Deterministic score 0.82; selected too much of the population."
      },
      {
        version: "student-v0",
        environment: "yail-gdpval:v7",
        task: "medsec-pathology-forms",
        score: 0.5225,
        traceId: "56a02063-376b-435d-bcac-6c3c915c96e5",
        jobId: "9aacd526702741008744b5f355ed1cad",
        decision: "Baseline comparison point",
        note: "Deterministic-only grading after environment v7 measurement fixes."
      }
    ]
  },
  {
    id: "ledger-2",
    name: "Ledger-2",
    role: "Customer Support Operations Worker",
    level: "Degree",
    track: "Standard",
    degreeTarget: "Degree",
    model: "claude-haiku-4-5",
    currentVersion: "student-v1",
    course: "GDPval Knowledge Work",
    enrolledCourses: ["GDPval Knowledge Work", "Business Capstone", "QA Review"],
    latestScore: "Acct audit 0.4275",
    qaStatus: "QA pending",
    promotionStatus: "Needs QA review",
    costUsed: "218 credits",
    costRemaining: "682 credits",
    summary: "The first improved student. Acct improved over v0, medsec tied, and one_deal did not regress.",
    scores: [ledgerScores.acctV1, ledgerScores.medsecV1, ledgerScores.oneDealV1],
    versions: [
      {
        id: "student-v0",
        title: "Parent baseline",
        status: "parent",
        note: "Acct 0.369, medsec 0.5225.",
        sourcePath: "yail-university/versions/student-v0/agent.md",
        codeSnippet: studentV0Code
      },
      {
        id: "student-v1",
        title: "Workflow prompt patch",
        status: "active candidate",
        note: "QA-guided prompt update added a professional work-product workflow.",
        sourcePath: "yail-university/versions/student-v1/agent.md",
        codeSnippet: studentV1Code
      }
    ],
    transcript: [
      {
        version: "student-v0",
        environment: "yail-gdpval:v7",
        task: "acct-afc-audit-sampling",
        score: 0.369,
        traceId: "4f400d71-22e2-43d9-b8af-39703654e3aa",
        jobId: "e8d134facdec4721b7d1b5aeb662b6ec",
        decision: "Parent baseline",
        note: "Selected 841 rows and failed the sample-not-population check."
      },
      {
        version: "student-v1",
        environment: "yail-gdpval:v7",
        task: "acct-afc-audit-sampling",
        score: 0.4275,
        delta: 0.0585,
        traceId: "fecfac1d-c3a2-4561-a02c-643ba65bc386",
        jobId: "b525dffdfafb4bf99c0d854bca867b78",
        decision: "Improved",
        note: "Selected 474 rows, passed sample-not-population, deterministic score rose to 0.95."
      },
      {
        version: "student-v0",
        environment: "yail-gdpval:v7",
        task: "medsec-pathology-forms",
        score: 0.5225,
        traceId: "56a02063-376b-435d-bcac-6c3c915c96e5",
        jobId: "9aacd526702741008744b5f355ed1cad",
        decision: "Parent baseline",
        note: "Deterministic-only score after grader observability fix."
      },
      {
        version: "student-v1",
        environment: "yail-gdpval:v7",
        task: "medsec-pathology-forms",
        score: 0.5225,
        delta: 0,
        traceId: "176ff833-d173-4fed-88af-7b9305e7651c",
        jobId: "73409774b9ab44868c15e6e7e72da9f1",
        decision: "Tied",
        note: "No lift over v0; still useful as no-regression evidence."
      },
      {
        version: "student-v1",
        environment: "autonomous-business",
        task: "one_deal_ai_workflow_business",
        score: 1,
        traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
        jobId: "51b79002efeb4d52b7c242ba1d2136a7",
        decision: "Held-out capstone passed",
        note: "Business simulation regression passed at 1.0."
      }
    ],
    improvements: [
      {
        fromVersion: "student-v0",
        toVersion: "student-v1",
        patch: "Added professional work-product workflow prompt: inspect files, build native artifacts, preserve IDs, verify before final answer.",
        evidence: "Baseline GDPval failures showed weak deliverable workflow and insufficient verification.",
        result: "Acct improved +0.0585, medsec tied, one_deal capstone passed."
      }
    ],
    workplaceOutcomes: [
      {
        environment: "autonomous-business",
        task: "one_deal_ai_workflow_business",
        score: 1,
        traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
        jobId: "51b79002efeb4d52b7c242ba1d2136a7",
        businessResult: "Completed the workflow business task in the hosted autonomous-business sim.",
        status: "passed",
        nextAction: "Run QA false-positive review before marking as full alumni."
      },
      {
        environment: "autonomous-business",
        task: "save_the_account_routing_bug",
        score: null,
        businessResult: "Rerun pending because earlier hosted attempts hit session-detach invalid runs.",
        status: "pending",
        nextAction: "Retry after hosted session stability or classify as invalid-run evidence."
      }
    ]
  },
  {
    id: "swift-track",
    name: "Swift-Track",
    role: "Customer Support Operations Worker",
    level: "Diploma",
    track: "Fast Track",
    degreeTarget: "Residency",
    model: "claude-haiku-4-5",
    currentVersion: "student-v1-fast",
    course: "Parallel Course Batch",
    enrolledCourses: ["Workflow Design", "Customer Communication", "Business Capstone"],
    latestScore: "Batch scheduled",
    qaStatus: "Parallel QA scheduled",
    promotionStatus: "Needs course runs",
    costUsed: "410 credits",
    costRemaining: "1,390 credits",
    summary: "Demo fast-track student using extra parallel HUD runs and sandboxes to compress iteration time.",
    scores: [{ label: "Fast-track batch", course: "Workflow Design", task: "mixed curriculum", score: null, evalType: "Parallel eval batch", improvement: "Scheduled", status: "pending", note: "Fast-track batches run more tasks in parallel at higher cost." }],
    versions: [{ id: "student-v1-fast", title: "Accelerated lane", status: "scheduled", note: "Same student policy, more parallel HUD evals and QA review." }],
    workplaceOutcomes: [
      {
        environment: "autonomous-business",
        task: "parallel workplace sims",
        score: null,
        businessResult: "Fast-track workplace simulations scheduled across extra sandboxes.",
        status: "pending",
        nextAction: "Wait for parallel scorecards."
      }
    ]
  },
  {
    id: "casey-qa",
    name: "Casey-QA",
    role: "Customer Support Operations Worker",
    level: "Diploma",
    track: "Standard",
    degreeTarget: "Diploma",
    model: "claude-haiku-4-5",
    currentVersion: "student-v0",
    course: "Workflow Debugging",
    enrolledCourses: ["Workflow Debugging", "Customer Communication", "QA Review"],
    latestScore: "Blocked by QA",
    qaStatus: "Teacher hold",
    promotionStatus: "Needs safer fix",
    costUsed: "203 credits",
    costRemaining: "147 credits",
    summary: "A student held back by QA review after traces looked passable but the teacher flagged a likely reward-hacking path.",
    scores: [{ label: "Workflow debugging hold", course: "Workflow Debugging", task: "workflow-debugging", score: null, evalType: "QA trace review", improvement: "Blocked", status: "blocked", note: "Teacher requires a revised task or patch before promotion." }],
    versions: [{ id: "student-v0", title: "Held version", status: "blocked by QA", note: "Needs an approved version change before another workplace sim." }],
    workplaceOutcomes: [
      {
        environment: "autonomous-business",
        task: "workflow-debugging workplace sim",
        score: null,
        businessResult: "Not admitted to workplace sim because QA flagged the school trace.",
        status: "blocked",
        nextAction: "Create a safer improvement patch."
      }
    ]
  },
  {
    id: "dr-atlas",
    name: "Dr. Atlas",
    role: "Customer Support Operations Worker",
    level: "PhD",
    track: "Fast Track",
    degreeTarget: "PhD",
    model: "Qwen/Qwen3-30B-A3B trainable fork",
    currentVersion: "dr-atlas-v2-rl-smoke",
    course: "GDPval Knowledge Work",
    enrolledCourses: ["GDPval Knowledge Work", "Business Capstone", "PhD RL Lab"],
    latestScore: "RL checkpoint created",
    qaStatus: "Needs post-RL QA",
    promotionStatus: "Needs held-out improvement",
    costUsed: "1,180 credits",
    costRemaining: "5,000+ credits",
    summary: "PhD candidate cloned from Ledger-2 student-v1. It produced a real HUD Training PPO checkpoint on a Qwen3-30B fork, but the first post-training audit rerun failed, so it has not graduated.",
    scores: [
      {
        label: "Business capstone seed",
        course: "Business Capstone",
        task: "one_deal_ai_workflow_business",
        score: 1,
        evalType: "Held-out business eval",
        improvement: "Inherited from Ledger-2",
        traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
        jobId: "51b79002efeb4d52b7c242ba1d2136a7",
        status: "passed",
        note: "Seed policy inherits Ledger-2 one_deal pass and GDPval acct lift; this is not an RL checkpoint."
      },
      {
        label: "Compact audit sampling",
        course: "GDPval Knowledge Work",
        task: "acct-audit-easy group=4",
        score: 0.691275,
        evalType: "Pre-training spread test",
        improvement: "Ready for first RL run; no weights trained",
        jobId: "1981f4d9b0aa4138a48d036f75883531",
        traceId: "ecfe8b13-74e3-4d62-bec1-9dbb35b73fd7",
        status: "candidate",
        note: "Qwen3-30B group=4 rewards were [0.0, 0.0, 0.663523, 0.691275]. This proves there is a learning signal, but it is not a training run."
      },
      {
        label: "RL smoke checkpoint",
        course: "PhD RL Lab",
        task: "acct-audit-easy group=4",
        score: 0.322723,
        evalType: "HUD Training PPO step",
        improvement: "Checkpoint step-000001",
        jobId: "fccd2c5000524e7183af8c25a002cce8",
        traceId: "db83b280-4db0-469b-be5a-a5ba58975892",
        status: "experimental",
        note: "Forked Qwen3-30B to yail-dr-atlas-qwen30b-smoke-20260621181803 and trained one PPO step at lr=1e-6. Batch rewards were [0.0, 0.0, 0.628836, 0.662056]."
      },
      {
        label: "Post-RL audit rerun",
        course: "PhD RL Lab",
        task: "acct-audit-easy group=2",
        score: 0,
        evalType: "Post-training eval",
        improvement: "Failed graduation gate",
        jobId: "797c91448a66444e845968100d007f3b",
        traceId: "f5e1e609-f599-45f1-a835-d62d81ee7ba4",
        status: "failed",
        note: "First post-training rerun on the active checkpoint produced all-zero rewards. The RL loop works, but this candidate needs broader GDPval training before graduation."
      }
    ],
    versions: [
      {
        id: "dr-atlas-v0-ledger2-clone",
        title: "Ledger-2 clone",
        status: "baseline seed",
        note: "Exact clone of Ledger-2 student-v1 prompt for a frozen PhD baseline.",
        sourcePath: "yail-university/versions/dr-atlas-v0-ledger2-clone/agent.md",
        codeSnippet: studentV1Code
      },
      {
        id: "dr-atlas-v1-rl-candidate",
        title: "Trace-hygiene prompt",
        status: "active candidate",
        note: "Prompt-only improvement to collect cleaner QA/SFT/RL trajectories.",
        sourcePath: "yail-university/versions/dr-atlas-v1-rl-candidate/agent.md",
        codeSnippet: drAtlasV1Code
      },
      {
        id: "dr-atlas-v2-rl-smoke",
        title: "Qwen3-30B PPO checkpoint",
        status: "checkpoint created",
        note: "Real HUD Training step completed; not a graduate because post-training eval failed.",
        sourcePath: "results/yail-rl-smoke-dr-atlas-qwen30b-lr1e6-20260621.json",
        codeSnippet: drAtlasV2Code
      }
    ],
    transcript: [
      {
        version: "dr-atlas-v0-ledger2-clone",
        environment: "autonomous-business",
        task: "one_deal_ai_workflow_business",
        score: 1,
        traceId: "0b699289-8cd2-4713-a978-b466b6a3b485",
        jobId: "51b79002efeb4d52b7c242ba1d2136a7",
        decision: "Seed accepted",
        note: "Inherited Ledger-2 student-v1 held-out capstone pass."
      },
      {
        version: "dr-atlas-v1-rl-candidate",
        environment: "yail-gdpval:v10",
        task: "acct-audit-easy Qwen3-30B spread gate",
        score: 0.691275,
        traceId: "ecfe8b13-74e3-4d62-bec1-9dbb35b73fd7",
        jobId: "1981f4d9b0aa4138a48d036f75883531",
        decision: "Ready for RL run",
        note: "Pre-training spread test completed with rewards [0.0, 0.0, 0.663523, 0.691275] and no invalid runs."
      },
      {
        version: "dr-atlas-v2-rl-smoke",
        environment: "yail-gdpval:v10",
        task: "acct-audit-easy PPO training batch",
        score: 0.322723,
        traceId: "db83b280-4db0-469b-be5a-a5ba58975892",
        jobId: "fccd2c5000524e7183af8c25a002cce8",
        decision: "Checkpoint created",
        note: "HUD Training created checkpoint step-000001 on trainable fork yail-dr-atlas-qwen30b-smoke-20260621181803."
      },
      {
        version: "dr-atlas-v2-rl-smoke",
        environment: "yail-gdpval:v10",
        task: "acct-audit-easy post-training rerun",
        score: 0,
        delta: -0.3227,
        traceId: "f5e1e609-f599-45f1-a835-d62d81ee7ba4",
        jobId: "797c91448a66444e845968100d007f3b",
        decision: "Not graduated",
        note: "Post-training group=2 eval returned [0.0, 0.0], so the candidate needs more tasks or safer training settings."
      }
    ],
    improvements: [
      {
        fromVersion: "dr-atlas-v0-ledger2-clone",
        toVersion: "dr-atlas-v1-rl-candidate",
        patch: "Added trace-hygiene guidance: observable checkpoints, verification evidence, no hidden-rubric guessing, no reward-target vocabulary.",
        evidence: "Ledger-2 is a good seed, but RL needs trajectories that are useful for QA labeling and trainable-model updates.",
        result: "Prompt-only candidate created. Spread test passed and then seeded a real HUD Training smoke."
      },
      {
        fromVersion: "dr-atlas-v1-rl-candidate",
        toVersion: "dr-atlas-v2-rl-smoke",
        patch: "Forked Qwen3-30B through HUD Training and ran one PPO update on grouped acct-audit-easy trajectories.",
        evidence: "Grouped rewards had spread, so the batch could produce a policy-gradient update.",
        result: "Checkpoint step-000001 was created, but post-training eval failed all-zero. The loop is proven; the candidate is not a graduate."
      }
    ],
    workplaceOutcomes: [
      {
        environment: "autonomous-business + GDPval curriculum traces",
        task: "PhD thesis loop",
        score: 0,
        traceId: "f5e1e609-f599-45f1-a835-d62d81ee7ba4",
        jobId: "797c91448a66444e845968100d007f3b",
        businessResult: "A real HUD Training checkpoint exists, but the first post-training GDPval rerun failed. Do not graduate yet.",
        status: "blocked",
        nextAction: "Train on a broader GDPval taskset with reward spread, then rerun held-out GDPval and autonomous-business gates."
      }
    ]
  }
];

export const alumniOutcomes = students
  .filter((student) => student.workplaceOutcomes?.length)
  .flatMap((student) =>
    (student.workplaceOutcomes ?? []).map((outcome) => ({
      studentId: student.id,
      studentName: student.name,
      level: student.level,
      currentVersion: student.currentVersion,
      degreeTarget: student.degreeTarget,
      ...outcome
    }))
  );

export const tracks = [
  {
    name: "Standard",
    cost: "1x base cost",
    pace: "Sequential reviews",
    description: "Lower cost path for agents that can learn over slower promotion cycles."
  },
  {
    name: "Fast Track",
    cost: "2.5-4x base cost",
    pace: "Parallel HUD runs and QA",
    description: "Higher cost path using more sandboxes and parallel scorecards to graduate faster."
  }
];

export const evidence = [
  { label: "GDPval environment", value: "yail-gdpval:v10 for PhD tools" },
  { label: "QA teacher", value: "yail-trace-explorer-v6" },
  { label: "Student model", value: "claude-haiku-4-5" },
  { label: "Best current proof", value: "student-v1 acct lift + Dr. Atlas spread gate" }
];
