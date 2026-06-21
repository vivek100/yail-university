import { useCallback, useMemo, useState } from "react";
import { ArrowRight, BookOpen, BriefcaseBusiness, GraduationCap, LayoutDashboard, ScrollText, UserPlus } from "lucide-react";
import { AlumniPage } from "./components/AlumniPage";
import { CurriculumPage } from "./components/CurriculumPage";
import { DashboardPage } from "./components/DashboardPage";
import { DegreesPage } from "./components/DegreesPage";
import { EnrollPage } from "./components/EnrollPage";
import { GuidedTour } from "./components/GuidedTour";
import { HomePage } from "./components/HomePage";
import { StudentDetail } from "./components/StudentDetail";
import { TrainingLoopPage } from "./components/TrainingLoopPage";
import { students } from "./data/yailSeedData";
import type { SectionId } from "./types";

const navItems: { id: SectionId; label: string; icon: React.ElementType }[] = [
  { id: "home", label: "Home", icon: GraduationCap },
  { id: "curriculum", label: "Curriculum", icon: BookOpen },
  { id: "degrees", label: "Degrees", icon: ScrollText },
  { id: "enroll", label: "Enroll", icon: UserPlus },
  { id: "alumni", label: "Alumni", icon: BriefcaseBusiness },
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "loop", label: "Training Loop", icon: ArrowRight }
];

export function App() {
  const [section, setSection] = useState<SectionId>("home");
  const [selectedStudentId, setSelectedStudentId] = useState("ledger-2");
  const [tourActive, setTourActive] = useState(false);
  const selectedStudent = useMemo(
    () => students.find((student) => student.id === selectedStudentId) ?? students[0],
    [selectedStudentId]
  );
  const navigate = useCallback((nextSection: SectionId, studentId?: string) => {
    setSection(nextSection);
    if (studentId) {
      setSelectedStudentId(studentId);
    }
  }, []);

  return (
    <div className="app">
      <header className="topbar">
        <button className="brand" onClick={() => navigate("home")} type="button">
          <span className="crest">Y</span>
          <span>
            <strong>YAIL University</strong>
            <small>Young Agents in Learning</small>
          </span>
        </button>
        <nav className="nav" aria-label="Primary navigation">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={section === item.id ? "navButton active" : "navButton"}
                key={item.id}
                onClick={() => navigate(item.id)}
                type="button"
                title={item.label}
              >
                <Icon size={17} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </header>

      <main>
        {section === "home" && <HomePage onNavigate={navigate} onStartTour={() => setTourActive(true)} />}
        {section === "curriculum" && <CurriculumPage />}
        {section === "degrees" && <DegreesPage onEnroll={() => setSection("enroll")} />}
        {section === "enroll" && <EnrollPage />}
        {section === "alumni" && <AlumniPage />}
        {section === "dashboard" && (
          <DashboardPage
            selectedStudentId={selectedStudentId}
            onSelectStudent={(id) => {
              navigate("dashboard", id);
              window.setTimeout(() => {
                document.getElementById("student-record")?.scrollIntoView({ behavior: "smooth", block: "start" });
              }, 0);
            }}
          />
        )}
        {section === "loop" && <TrainingLoopPage />}
        {section === "dashboard" && <StudentDetail student={selectedStudent} />}
      </main>
      <GuidedTour
        active={tourActive}
        onClose={() => setTourActive(false)}
        onNavigate={navigate}
        onStart={() => setTourActive(true)}
      />
    </div>
  );
}
