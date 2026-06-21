import { ArrowRight, BrainCircuit, BriefcaseBusiness, GraduationCap, SearchCheck, Wrench } from "lucide-react";

const steps = [
  { title: "Enroll", icon: GraduationCap, text: "Choose role, degree target, track, and baseline model." },
  { title: "Run HUD Tasks", icon: ArrowRight, text: "Hosted environments produce traces, rewards, and scorecards." },
  { title: "QA Teacher", icon: SearchCheck, text: "Trace Explorer reviews failure modes, false positives, and reward hacking." },
  { title: "Improve", icon: Wrench, text: "Improvement Teacher creates a bounded patch and a new version." },
  { title: "Graduate", icon: BrainCircuit, text: "Promotion Gate accepts only target lift plus held-out no-regression." },
  { title: "Workplace Sim", icon: BriefcaseBusiness, text: "Alumni agents enter autonomous-business sims; failures trigger retraining." }
];

export function TrainingLoopPage() {
  return (
    <section className="pageWrap">
      <div className="sectionHeader">
        <p className="eyebrow dark">Two-teacher architecture</p>
        <h2>The university is a deterministic hill-climb loop.</h2>
        <p>YAIL separates the evaluator teacher from the teacher that mutates the student or environment.</p>
      </div>
      <div className="loopRail">
        {steps.map((step) => {
          const Icon = step.icon;
          return (
            <article className="loopStep" key={step.title}>
              <Icon size={23} />
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </article>
          );
        })}
      </div>
      <div className="loopEvidence">
        <div>
          <strong>QA Evaluator Teacher</strong>
          <p>Faithful HUD trace-explorer v6 fork. It audits traces and task quality.</p>
        </div>
        <div>
          <strong>Improvement Teacher</strong>
          <p>Creates versioned patches to prompts, tools, tasks, environments, or models.</p>
        </div>
        <div>
          <strong>Promotion Gate</strong>
          <p>Accepts only if target metrics improve and held-out checks do not regress.</p>
        </div>
      </div>
    </section>
  );
}
