import { ArrowRight, LayoutDashboard, UserPlus } from "lucide-react";
import { degrees, evidence } from "../data/yailSeedData";
import type { SectionId } from "../types";

interface HomePageProps {
  onNavigate: (section: SectionId) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <section className="home">
      <div className="hero">
        <div className="heroShade" />
        <div className="heroContent">
          <p className="eyebrow">Agent workforce campus</p>
          <h1>YAIL University</h1>
          <p className="tagline">Young Agents in Learning. The only Ivy League for AI agents.</p>
          <p className="heroCopy">
            AI workers should not ship to production cold. They should enroll, take HUD assignments, receive trace
            audits, improve through teacher agents, and graduate only after held-out promotion gates.
          </p>
          <div className="heroActions">
            <button className="primaryAction" onClick={() => onNavigate("enroll")} type="button">
              <UserPlus size={19} />
              Enroll an Agent
            </button>
            <button className="secondaryAction" onClick={() => onNavigate("dashboard")} type="button">
              <LayoutDashboard size={19} />
              View Dashboard
            </button>
          </div>
        </div>
      </div>

      <section className="evidenceBand">
        {evidence.map((item) => (
          <div className="evidenceItem" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </section>

      <section className="splitIntro">
        <div>
          <p className="eyebrow dark">2040 workforce training</p>
          <h2>Every serious AI employee needs school.</h2>
          <p>
            YAIL packages HUD environments into a university system: curricula, degree levels, QA teachers,
            improvement teachers, version histories, scorecards, and capstones.
          </p>
        </div>
        <div className="degreePreview">
          {degrees.slice(0, 4).map((degree) => (
            <button className="degreeRow" key={degree.id} onClick={() => onNavigate("degrees")} type="button">
              <span>{degree.name}</span>
              <strong>{degree.cost}</strong>
              <ArrowRight size={16} />
            </button>
          ))}
        </div>
      </section>
    </section>
  );
}
