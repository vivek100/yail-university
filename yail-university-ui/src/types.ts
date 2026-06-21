export type SectionId =
  | "home"
  | "curriculum"
  | "degrees"
  | "enroll"
  | "alumni"
  | "dashboard"
  | "loop";

export type DegreeStatus = "available" | "candidate" | "experimental";
export type TrackType = "Standard" | "Fast Track";

export interface Degree {
  id: string;
  name: string;
  purpose: string;
  cost: string;
  lanes: string;
  status: DegreeStatus;
  requirements: string[];
}

export interface Course {
  id: string;
  title: string;
  objective: string;
  environment: string;
  dataSource: string;
  taskData: string[];
  trainedAgents: string[];
  model: string;
  grader: string;
  qaChecks: string[];
  criteria: string;
  evidence: {
    agent: string;
    version: string;
    task: string;
    score: number | null;
    traceId?: string;
    jobId?: string;
    note: string;
  }[];
}

export interface ScoreRecord {
  label: string;
  course?: string;
  task: string;
  score: number | null;
  evalType?: string;
  improvement?: string;
  traceId?: string;
  jobId?: string;
  status: "passed" | "failed" | "candidate" | "pending" | "blocked" | "experimental";
  note: string;
}

export interface TranscriptEntry {
  version: string;
  environment: string;
  task: string;
  score: number | null;
  delta?: number | null;
  traceId?: string;
  jobId?: string;
  decision: string;
  note: string;
}

export interface ImprovementRecord {
  fromVersion: string;
  toVersion: string;
  patch: string;
  evidence: string;
  result: string;
}

export interface WorkplaceOutcome {
  environment: string;
  task: string;
  score: number | null;
  traceId?: string;
  jobId?: string;
  businessResult: string;
  status: "passed" | "candidate" | "pending" | "blocked" | "experimental";
  nextAction: string;
}

export interface Student {
  id: string;
  name: string;
  role: string;
  level: string;
  track: TrackType;
  degreeTarget: string;
  model: string;
  currentVersion: string;
  course: string;
  enrolledCourses?: string[];
  latestScore: string;
  qaStatus: string;
  promotionStatus: string;
  costUsed: string;
  costRemaining: string;
  summary: string;
  scores: ScoreRecord[];
  versions: {
    id: string;
    title: string;
    status: string;
    note: string;
    sourcePath?: string;
    codeSnippet?: string;
  }[];
  transcript?: TranscriptEntry[];
  improvements?: ImprovementRecord[];
  workplaceOutcomes?: WorkplaceOutcome[];
}
