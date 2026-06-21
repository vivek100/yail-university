import { ArrowRight, CircleDot, FastForward, ShieldCheck } from "lucide-react";
import { students } from "../data/yailSeedData";

interface DashboardPageProps {
  selectedStudentId: string;
  onSelectStudent: (id: string) => void;
}

export function DashboardPage({ selectedStudentId, onSelectStudent }: DashboardPageProps) {
  return (
    <section className="pageWrap dashboardPage">
      <div className="sectionHeader dashboardHeader">
        <div>
          <p className="eyebrow dark">Registrar dashboard</p>
          <h2>Enrolled agents across placement, courses, QA, and research.</h2>
        </div>
        <div className="dashboardStats">
          <span>
            <CircleDot size={16} />
            6 students
          </span>
          <span>
            <FastForward size={16} />
            2 fast-track
          </span>
          <span>
            <ShieldCheck size={16} />
            1 promotion candidate
          </span>
        </div>
      </div>
      <div className="studentTable" data-tour-id="student-dashboard">
        <div className="studentRow tableHead">
          <span>Student</span>
          <span>Current level</span>
          <span>Target level</span>
          <span>Courses</span>
          <span>Version</span>
          <span>Latest result</span>
          <span>Needs next</span>
          <span />
        </div>
        {students.map((student) => (
          <button
            className={selectedStudentId === student.id ? "studentRow selected" : "studentRow"}
            key={student.id}
            onClick={() => onSelectStudent(student.id)}
            type="button"
          >
            <span>
              <strong>{student.name}</strong>
              <small>{student.track}</small>
            </span>
            <span>
              <strong>{student.level}</strong>
            </span>
            <span>{student.degreeTarget}</span>
            <span className="courseChipCell">
              {(student.enrolledCourses ?? [student.course]).map((course) => (
                <small className="courseChip" key={`${student.id}-${course}`}>{course}</small>
              ))}
            </span>
            <span>{student.currentVersion}</span>
            <span>{student.latestScore}</span>
            <span>{student.promotionStatus}</span>
            <ArrowRight size={16} />
          </button>
        ))}
      </div>
    </section>
  );
}
