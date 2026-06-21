import { ArrowUpRight, Code2, ExternalLink, GitBranch, ShieldCheck, Wrench } from "lucide-react";
import type { Student } from "../types";
import { formatShortId, getEnvironmentUrl, getJobUrl, getTraceUrl } from "../utils/hudLinks";

interface StudentDetailProps {
  student: Student;
}

export function StudentDetail({ student }: StudentDetailProps) {
  return (
    <section className="studentDetail" data-tour-id="student-record" id="student-record">
      <div className="studentHero">
        <div>
          <p className="eyebrow dark">Student record</p>
          <h2>{student.name}</h2>
          <p>{student.summary}</p>
          <div className="enrolledCourseStrip">
            {(student.enrolledCourses ?? [student.course]).map((course) => (
              <span key={`${student.id}-detail-${course}`}>{course}</span>
            ))}
          </div>
        </div>
        <div className="studentMeta">
          <span>{student.track}</span>
          <strong>Current: {student.level}</strong>
          <small>Target: {student.degreeTarget}</small>
        </div>
      </div>
      <div className="detailGrid">
        <article className="detailPanel">
          <h3>
            <ShieldCheck size={19} />
            Course Record
          </h3>
          <div className="scoreList" data-tour-id="student-results">
            {student.scores.map((score) => (
              <div className="scoreRow" key={`${score.label}-${score.task}`}>
                <div>
                  <strong>{score.label}</strong>
                  {score.course ? <small>{score.course}</small> : null}
                  <small>{score.task}</small>
                  <p>{score.note}</p>
                  <div className="scoreMethodLine">
                    {score.evalType ? <span>{score.evalType}</span> : null}
                    {score.improvement ? <span>{score.improvement}</span> : null}
                  </div>
                  {(score.jobId || score.traceId) && (
                    <small className="runMeta">
                      {score.jobId ? `job ${formatShortId(score.jobId)}` : ""}
                      {score.jobId && score.traceId ? " / " : ""}
                      {score.traceId && getTraceUrl(score.traceId) ? (
                        <a href={getTraceUrl(score.traceId) ?? undefined} target="_blank" rel="noreferrer">
                          trace {formatShortId(score.traceId)}
                        </a>
                      ) : null}
                    </small>
                  )}
                </div>
                <div className={`scoreBadge ${score.status}`}>
                  {score.score === null ? score.status : score.score.toFixed(score.score === 1 ? 1 : 4)}
                </div>
                <div className="scoreActions">
                  {score.traceId && getTraceUrl(score.traceId) ? (
                    <a href={getTraceUrl(score.traceId) ?? undefined} target="_blank" rel="noreferrer">
                      HUD Trace
                      <ExternalLink size={14} />
                    </a>
                  ) : null}
                  {score.jobId && getJobUrl(score.jobId) ? (
                    <a href={getJobUrl(score.jobId) ?? undefined} target="_blank" rel="noreferrer">
                      HUD Job
                      <ExternalLink size={14} />
                    </a>
                  ) : null}
                </div>
              </div>
            ))}
          </div>
        </article>
        <article className="detailPanel">
          <h3>
            <GitBranch size={19} />
            Agent Versions
          </h3>
          <div className="timeline">
            {student.versions.map((version) => (
              <div className="timelineItem" key={version.id}>
                <span />
                <div>
                  <strong>{version.id}</strong>
                  <small>{version.title} - {version.status}</small>
                  <p>{version.note}</p>
                </div>
              </div>
            ))}
          </div>
        </article>
      </div>
      {student.versions.some((version) => version.codeSnippet) ? (
        <article className="detailPanel versionCodePanel">
          <h3>
            <Code2 size={19} />
            Agent Version Code
          </h3>
          <div className="versionCodeGrid">
            {student.versions
              .filter((version) => version.codeSnippet)
              .map((version) => (
                <div className="versionCodeCard" key={`${student.id}-${version.id}-code`}>
                  <div>
                    <strong>{version.id}</strong>
                    <small>{version.sourcePath}</small>
                  </div>
                  <pre>{version.codeSnippet}</pre>
                </div>
              ))}
          </div>
        </article>
      ) : null}
      {student.transcript?.length ? (
        <article className="detailPanel transcriptPanel" data-tour-id="run-evidence">
          <h3>
            <ArrowUpRight size={19} />
            Evaluation Runs
          </h3>
          <div className="transcriptTable">
            <div className="transcriptRow transcriptHead">
              <span>Version</span>
              <span>Environment</span>
              <span>Task</span>
              <span>Score</span>
              <span>Delta</span>
              <span>Decision</span>
              <span>Run</span>
            </div>
            {student.transcript.map((entry) => (
              <div className="transcriptRow" key={`${entry.version}-${entry.task}-${entry.traceId ?? entry.decision}`}>
                <span>
                  <strong>{entry.version}</strong>
                </span>
                <span>
                  {getEnvironmentUrl(entry.environment) ? (
                    <a className="envLink" href={getEnvironmentUrl(entry.environment) ?? undefined} target="_blank" rel="noreferrer">
                      {entry.environment}
                      <ExternalLink size={14} />
                    </a>
                  ) : (
                    entry.environment
                  )}
                </span>
                <span>
                  <strong>{entry.task}</strong>
                  <small>{entry.note}</small>
                </span>
                <span>{entry.score === null ? "pending" : entry.score.toFixed(entry.score === 1 ? 1 : 4)}</span>
                <span className={entry.delta && entry.delta > 0 ? "positiveDelta" : ""}>
                  {entry.delta === undefined || entry.delta === null
                    ? "-"
                    : entry.delta === 0
                      ? "0.0000"
                      : `+${entry.delta.toFixed(4)}`}
                </span>
                <span>{entry.decision}</span>
                <span className="runCell">
                  {entry.jobId ? <small>job {formatShortId(entry.jobId)}</small> : null}
                  {entry.traceId && getTraceUrl(entry.traceId) ? (
                    <small>
                      <a href={getTraceUrl(entry.traceId) ?? undefined} target="_blank" rel="noreferrer">
                        trace {formatShortId(entry.traceId)}
                      </a>
                    </small>
                  ) : null}
                </span>
              </div>
            ))}
          </div>
        </article>
      ) : null}
      {student.improvements?.length ? (
        <article className="detailPanel improvementPanel">
          <h3>
            <Wrench size={19} />
            Version Changes
          </h3>
          {student.improvements.map((improvement) => (
            <div className="improvementCard" key={`${improvement.fromVersion}-${improvement.toVersion}`}>
              <div>
                <strong>
                  {improvement.fromVersion} {"->"} {improvement.toVersion}
                </strong>
                <p>{improvement.patch}</p>
              </div>
              <div>
                <span>Why it changed</span>
                <p>{improvement.evidence}</p>
              </div>
              <div>
                <span>Measured result</span>
                <p>{improvement.result}</p>
              </div>
            </div>
          ))}
        </article>
      ) : null}
      <div className="gateStrip">
        <span>QA status: {student.qaStatus}</span>
        <span>Promotion: {student.promotionStatus}</span>
        <span>Cost: {student.costUsed} used / {student.costRemaining} remaining</span>
      </div>
    </section>
  );
}
