import { ExternalLink, RotateCcw, Trophy } from "lucide-react";
import { alumniOutcomes } from "../data/yailSeedData";
import { formatShortId, getEnvironmentUrl, getTraceUrl } from "../utils/hudLinks";

function formatScore(score: number | null) {
  return score === null ? "pending" : score.toFixed(score === 1 ? 1 : 4);
}

export function AlumniPage() {
  return (
    <section className="pageWrap alumniPage">
      <div className="sectionHeader">
        <p className="eyebrow dark">Alumni workplace outcomes</p>
        <h2>Graduation is not the end. Alumni enter business simulation.</h2>
        <p>
          The autonomous-business environment is the workplace layer: passed or candidate agents are tested on
          realistic business workflows, and failures feed the next curriculum loop.
        </p>
      </div>

      <div className="workplaceSummary">
        <article>
          <Trophy size={22} />
          <strong>School result</strong>
          <p>student-v1 improved acct, tied medsec, and passed one_deal regression.</p>
        </article>
        <article>
          <RotateCcw size={22} />
          <strong>Workplace loop</strong>
          <p>Business sim failures become retraining data, not silent production incidents.</p>
        </article>
      </div>

      <div className="alumniTable">
        <div className="alumniRow alumniHead">
          <span>Agent</span>
          <span>Workplace sim</span>
          <span>Score</span>
          <span>Business result</span>
          <span>Next action</span>
          <span>Run</span>
        </div>
        {alumniOutcomes.map((outcome) => (
          <div className="alumniRow" key={`${outcome.studentId}-${outcome.task}`}>
            <span>
              <strong>{outcome.studentName}</strong>
              <small>{outcome.currentVersion} - {outcome.level}</small>
            </span>
            <span>
              <strong>{outcome.task}</strong>
              <small>
                {getEnvironmentUrl(outcome.environment) ? (
                  <a className="envLink" href={getEnvironmentUrl(outcome.environment) ?? undefined} target="_blank" rel="noreferrer">
                    {outcome.environment}
                    <ExternalLink size={14} />
                  </a>
                ) : (
                  outcome.environment
                )}
              </small>
            </span>
            <span className={`scoreBadge ${outcome.status}`}>{formatScore(outcome.score)}</span>
            <span>{outcome.businessResult}</span>
            <span>{outcome.nextAction}</span>
            <span className="runCell">
              {outcome.jobId ? <small>job {formatShortId(outcome.jobId)}</small> : null}
              {outcome.traceId && getTraceUrl(outcome.traceId) ? (
                <small>
                  <a href={getTraceUrl(outcome.traceId) ?? undefined} target="_blank" rel="noreferrer">
                    trace {formatShortId(outcome.traceId)}
                  </a>
                </small>
              ) : null}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
