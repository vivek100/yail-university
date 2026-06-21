import { CheckCircle2, Database, ExternalLink, GraduationCap, UserRoundCog } from "lucide-react";
import { courses } from "../data/yailSeedData";
import { formatShortId, getEnvironmentUrl, getTraceUrl } from "../utils/hudLinks";

export function CurriculumPage() {
  return (
    <section className="pageWrap">
      <div className="sectionHeader">
        <p className="eyebrow dark">Customer Support Ops Worker</p>
        <h2>Courses that turn generic agents into role-specific operators.</h2>
        <p>Each course maps to HUD tasks, trace review, and explicit promotion criteria.</p>
      </div>
      <div className="courseGrid">
        {courses.map((course, index) => {
          const environmentUrl = getEnvironmentUrl(course.environment);

          return (
          <article className="coursePanel" key={course.id}>
            <span className="courseNumber">{String(index + 1).padStart(2, "0")}</span>
            <h3>{course.title}</h3>
            <p>{course.objective}</p>
            <dl>
              <dt>Environment</dt>
              <dd>
                {environmentUrl ? (
                  <a className="envLink" href={environmentUrl} target="_blank" rel="noreferrer">
                    {course.environment}
                    <ExternalLink size={14} />
                  </a>
                ) : (
                  course.environment
                )}
              </dd>
              <dt>Data Source</dt>
              <dd>{course.dataSource}</dd>
              <dt>Student Model</dt>
              <dd>{course.model}</dd>
              <dt>Grader</dt>
              <dd>{course.grader}</dd>
              <dt>Promotion</dt>
              <dd>{course.criteria}</dd>
            </dl>
            <div className="courseDetailBlock">
              <strong>
                <Database size={15} />
                Task data
              </strong>
              <div className="pillList">
                {course.taskData.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </div>
            <div className="courseDetailBlock">
              <strong>
                <UserRoundCog size={15} />
                Agents trained or evaluated
              </strong>
              <div className="pillList">
                {course.trainedAgents.map((agent) => (
                  <span key={agent}>{agent}</span>
                ))}
              </div>
            </div>
            <div className="courseEvidence">
              <strong>
                <GraduationCap size={15} />
                Run evidence
              </strong>
              {course.evidence.map((item) => (
                <div className="courseEvidenceRow" key={`${course.id}-${item.agent}-${item.task}-${item.version}`}>
                  <span>
                    <b>{item.agent}</b>
                    <small>{item.version}</small>
                  </span>
                  <span>
                    <b>{item.task}</b>
                    <small>{item.note}</small>
                    {(item.jobId || item.traceId) && (
                      <small className="runMeta">
                        {item.jobId ? `job ${formatShortId(item.jobId)}` : ""}
                        {item.jobId && item.traceId ? " / " : ""}
                        {item.traceId && getTraceUrl(item.traceId) ? (
                          <a href={getTraceUrl(item.traceId) ?? undefined} target="_blank" rel="noreferrer">
                            trace {formatShortId(item.traceId)}
                          </a>
                        ) : null}
                      </small>
                    )}
                  </span>
                  <span className={item.score === null ? "scoreBadge pending" : "scoreBadge candidate"}>
                    {item.score === null ? "pending" : item.score}
                  </span>
                  <span aria-hidden="true" />
                </div>
              ))}
            </div>
            <div className="qaList">
              {course.qaChecks.map((check) => (
                <span key={check}>
                  <CheckCircle2 size={14} />
                  {check}
                </span>
              ))}
            </div>
          </article>
          );
        })}
      </div>
    </section>
  );
}
