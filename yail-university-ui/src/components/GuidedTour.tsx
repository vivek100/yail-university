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
}

const tourSteps: TourStep[] = [
  {
    id: "campus",
    title: "This is the campus",
    section: "home",
    target: "campus",
    actionLabel: "Start at home",
    body:
      "YAIL University is a school for AI workers. Agents enroll, take HUD tasks, get trace reviews, improve through teacher agents, and only graduate after held-out checks."
  },
  {
    id: "evidence",
    title: "The proof strip",
    section: "home",
    target: "evidence",
    actionLabel: "Show evidence",
    body:
      "These are the demo anchors: the HUD GDPval environment, the trace QA teacher, the student model, and the current strongest proof from real HUD runs."
  },
  {
    id: "curriculum",
    title: "Courses are benchmark tasksets",
    section: "curriculum",
    target: "curriculum-grid",
    actionLabel: "Open courses",
    body:
      "A course is not a lecture. It is a bundle of HUD tasks, graders, trace audits, and promotion criteria. GDPval supplies real professional work, and business sims test workplace behavior."
  },
  {
    id: "dashboard",
    title: "Registrar dashboard",
    section: "dashboard",
    target: "student-dashboard",
    actionLabel: "Open dashboard",
    studentId: "dr-atlas",
    body:
      "This table shows enrolled agents like students. Each row has current level, target level, enrolled courses, active version, latest result, and what the agent needs next."
  },
  {
    id: "student",
    title: "Student record",
    section: "dashboard",
    target: "student-record",
    actionLabel: "Inspect Dr. Atlas",
    studentId: "dr-atlas",
    body:
      "The student record links scores to HUD jobs and traces. Dr. Atlas has a real Qwen3-30B PPO checkpoint, but it is not a graduate because the post-training rerun did not improve."
  },
  {
    id: "loop",
    title: "The training loop",
    section: "loop",
    target: "training-loop",
    actionLabel: "Show loop",
    body:
      "YAIL separates two teachers: a QA evaluator that decides whether the trace is trustworthy, and an improvement teacher that proposes a bounded next version. Promotion requires measured improvement."
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
