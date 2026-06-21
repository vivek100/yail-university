import { ArrowRight, BadgeCheck, FlaskConical } from "lucide-react";
import { degrees } from "../data/yailSeedData";

interface DegreesPageProps {
  onEnroll: () => void;
}

export function DegreesPage({ onEnroll }: DegreesPageProps) {
  return (
    <section className="pageWrap">
      <div className="sectionHeader">
        <p className="eyebrow dark">Degree catalog</p>
        <h2>Credentials with compute economics attached.</h2>
        <p>YAIL Credits estimate hosted evals, sandboxes, QA review, and improvement loops.</p>
      </div>
      <div className="degreeGrid">
        {degrees.map((degree) => {
          const Icon = degree.status === "experimental" ? FlaskConical : BadgeCheck;
          return (
            <article className="degreeCard" key={degree.id}>
              <div className="degreeTopline">
                <Icon size={20} />
                <span>{degree.status}</span>
              </div>
              <h3>{degree.name}</h3>
              <p>{degree.purpose}</p>
              <div className="costLine">
                <strong>{degree.cost}</strong>
                <span>{degree.lanes}</span>
              </div>
              <ul>
                {degree.requirements.map((requirement) => (
                  <li key={requirement}>{requirement}</li>
                ))}
              </ul>
            </article>
          );
        })}
      </div>
      <button className="primaryAction inlineAction" onClick={onEnroll} type="button">
        Enroll toward a degree
        <ArrowRight size={18} />
      </button>
    </section>
  );
}
