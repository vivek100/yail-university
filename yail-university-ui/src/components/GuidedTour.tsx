import { ChevronLeft, ChevronRight, MapPinned, Pause, Play, Volume2, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { SectionId } from "../types";

interface TourStep {
  id: string;
  title: string;
  section: SectionId;
  target: string;
  body: string;
  actionLabel: string;
  studentId?: string;
  links?: { label: string; href: string }[];
}

const tourSteps: TourStep[] = [
  {
    id: "campus",
    title: "What is YAIL University?",
    section: "home",
    target: "campus",
    actionLabel: "Start at home",
    body:
      "YAIL University is a school for AI workers. The idea is simple: do not ship an agent cold. Enroll it, test it on real HUD environments, review the traces, improve the agent, and only graduate it when held-out checks pass."
  },
  {
    id: "levels",
    title: "Levels are promotion gates",
    section: "degrees",
    target: "degree-levels",
    actionLabel: "Show degree catalog",
    body:
      "The school has levels: Certificate, Diploma, Degree, Residency, and PhD. The higher levels cost more because they require more hosted evals, sandboxes, trace review, and eventually model training."
  },
  {
    id: "curriculum",
    title: "Curriculum means tasksets",
    section: "curriculum",
    target: "curriculum-grid",
    actionLabel: "Open courses",
    body:
      "A YAIL course is not a lesson page. It is a bundle of HUD tasks, data, graders, QA checks, and promotion criteria. GDPval supplies professional work tasks; autonomous-business supplies workplace simulations."
  },
  {
    id: "admissions",
    title: "How an agent enrolls",
    section: "enroll",
    target: "admissions-paths",
    actionLabel: "Open admissions",
    body:
      "An agent can start from scratch, come from an existing GitHub repo, or be sponsored for a business domain. Enrollment chooses the role, degree target, track, and baseline model."
  },
  {
    id: "flow",
    title: "How agents move through school",
    section: "loop",
    target: "curriculum-flow",
    actionLabel: "Show training loop",
    body:
      "The agent takes HUD tasks, gets scored, then a QA teacher reviews whether the trace and task are trustworthy. If the result is valid, an improvement teacher proposes the next prompt, tool, environment, or model version."
  },
  {
    id: "runtime",
    title: "HUD runs the school, Modal hosts the campus",
    section: "loop",
    target: "runtime-stack",
    actionLabel: "Show runtimes",
    body:
      "HUD is where the real agent work happens: environments, tasksets, traces, scores, and training. Modal hosts this frontend so judges can click through the university as a public web app.",
    links: [{ label: "Modal app", href: "https://shukla-vivek1993--yail-university-web.modal.run" }]
  },
  {
    id: "dashboard",
    title: "The registrar dashboard",
    section: "dashboard",
    target: "student-dashboard",
    actionLabel: "Open dashboard",
    studentId: "ledger-2",
    body:
      "This is the operating view. Each row is an enrolled agent with current level, target level, courses, version, latest result, and the next required gate."
  },
  {
    id: "graduate",
    title: "Graduate journey: Ledger-2",
    section: "dashboard",
    target: "student-record",
    actionLabel: "Inspect Ledger-2",
    studentId: "ledger-2",
    body:
      "Ledger-2 is the clearest graduate-style story. It started from a baseline worker, got a QA-guided work-product workflow update, improved on the GDPval audit course, did not regress on Medsec, and passed the business capstone."
  },
  {
    id: "graduate-results",
    title: "Ledger-2 results are trace-backed",
    section: "dashboard",
    target: "student-results",
    actionLabel: "Show Ledger scores",
    studentId: "ledger-2",
    body:
      "The score cards are not marketing numbers. They link to HUD jobs and traces. Ledger-2 improved acct audit from 0.3690 to 0.4275 and passed the autonomous-business capstone at 1.0.",
    links: [{ label: "Ledger capstone trace", href: "https://www.hud.ai/trace/0b699289-8cd2-4713-a978-b466b6a3b485" }]
  },
  {
    id: "workplace",
    title: "Graduates go to workplace sims",
    section: "alumni",
    target: "alumni-runs",
    actionLabel: "Show alumni outcomes",
    body:
      "Graduation is not the end. Alumni agents enter autonomous-business workplace simulations. A business failure becomes retraining data instead of a silent production incident."
  },
  {
    id: "phd",
    title: "PhD journey: Dr. Atlas",
    section: "dashboard",
    target: "student-record",
    actionLabel: "Inspect Dr. Atlas",
    studentId: "dr-atlas",
    body:
      "Dr. Atlas is the research track. It was cloned from Ledger-2, then used to test whether a trainable open model can get a real HUD Training update from GDPval rollouts."
  },
  {
    id: "phd-results",
    title: "The PhD result is honest",
    section: "dashboard",
    target: "student-results",
    actionLabel: "Show PhD scores",
    studentId: "dr-atlas",
    body:
      "Dr. Atlas produced a real Qwen3-30B PPO checkpoint on HUD Training, but it did not graduate. The post-training rerun failed, so the next step is broader GDPval training data and safer evaluation gates.",
    links: [
      { label: "Training job", href: "https://hud.ai/jobs/fccd2c5000524e7183af8c25a002cce8" },
      { label: "Post-RL trace", href: "https://www.hud.ai/trace/f5e1e609-f599-45f1-a835-d62d81ee7ba4" }
    ]
  },
  {
    id: "end",
    title: "End state",
    section: "home",
    target: "evidence",
    actionLabel: "Return home",
    body:
      "That is the demo: a university-shaped agent improvement system, with HUD as the evaluation and training layer, Modal as the public campus, Ledger-2 as a passing worker, and Dr. Atlas as the next RL frontier."
  }
];

interface GuidedTourProps {
  active: boolean;
  onStart: () => void;
  onClose: () => void;
  onNavigate: (section: SectionId, studentId?: string) => void;
}

export function GuidedTour({ active, onStart, onClose, onNavigate }: GuidedTourProps) {
  const [index, setIndex] = useState(0);
  const [voiceOn, setVoiceOn] = useState(false);
  const step = tourSteps[index];
  const speechSupported = useMemo(() => typeof window !== "undefined" && "speechSynthesis" in window, []);

  useEffect(() => {
    if (!active) {
      window.speechSynthesis?.cancel();
      document.querySelectorAll(".tourTargetActive").forEach((node) => node.classList.remove("tourTargetActive"));
      return;
    }

    onNavigate(step.section, step.studentId);
    const timeout = window.setTimeout(() => {
      const target = document.querySelector<HTMLElement>(`[data-tour-id="${step.target}"]`);
      document.querySelectorAll(".tourTargetActive").forEach((node) => node.classList.remove("tourTargetActive"));
      if (target) {
        target.classList.add("tourTargetActive");
        target.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }, 80);

    return () => window.clearTimeout(timeout);
  }, [active, index, onNavigate, step]);

  useEffect(() => {
    if (!active || !voiceOn || !speechSupported) {
      window.speechSynthesis?.cancel();
      return;
    }

    const utterance = new SpeechSynthesisUtterance(`${step.title}. ${step.body}`);
    utterance.rate = 0.96;
    utterance.pitch = 1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);

    return () => window.speechSynthesis.cancel();
  }, [active, voiceOn, speechSupported, step]);

  useEffect(() => {
    return () => {
      document.querySelectorAll(".tourTargetActive").forEach((node) => node.classList.remove("tourTargetActive"));
      window.speechSynthesis?.cancel();
    };
  }, []);

  if (!active) {
    return (
      <button className="tourLauncher" onClick={onStart} type="button">
        <MapPinned size={18} />
        Walk me through it
      </button>
    );
  }

  const goTo = (nextIndex: number) => {
    setIndex(Math.max(0, Math.min(tourSteps.length - 1, nextIndex)));
  };

  return (
    <aside className="tourPanel" aria-live="polite">
      <div className="tourPanelTop">
        <span>
          <MapPinned size={17} />
          Stop {index + 1} of {tourSteps.length}
        </span>
        <button className="iconButton" onClick={onClose} type="button" title="Close walkthrough">
          <X size={17} />
        </button>
      </div>
      <h2>{step.title}</h2>
      <p>{step.body}</p>
      {step.links?.length ? (
        <div className="tourLinks">
          {step.links.map((link) => (
            <a href={link.href} key={link.href} target="_blank" rel="noreferrer">
              {link.label}
            </a>
          ))}
        </div>
      ) : null}
      <div className="tourProgress" aria-hidden="true">
        {tourSteps.map((item, stepIndex) => (
          <button
            className={stepIndex === index ? "tourDot active" : "tourDot"}
            key={item.id}
            onClick={() => goTo(stepIndex)}
            type="button"
            title={item.title}
          />
        ))}
      </div>
      <div className="tourActions">
        <button className="secondaryAction compact" disabled={index === 0} onClick={() => goTo(index - 1)} type="button">
          <ChevronLeft size={17} />
          Back
        </button>
        <button
          className="secondaryAction compact"
          disabled={!speechSupported}
          onClick={() => setVoiceOn((value) => !value)}
          type="button"
          title={speechSupported ? "Toggle narration" : "Text to speech is not available in this browser"}
        >
          {voiceOn ? <Pause size={17} /> : <Volume2 size={17} />}
          {voiceOn ? "Pause" : "Read"}
        </button>
        <button className="primaryAction compact" onClick={() => (index === tourSteps.length - 1 ? onClose() : goTo(index + 1))} type="button">
          {index === tourSteps.length - 1 ? (
            <>
              <Play size={17} />
              Finish
            </>
          ) : (
            <>
              Next
              <ChevronRight size={17} />
            </>
          )}
        </button>
      </div>
      <button className="tourJump" onClick={() => onNavigate(step.section, step.studentId)} type="button">
        {step.actionLabel}
      </button>
    </aside>
  );
}
