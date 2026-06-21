import { Github, Landmark, Sparkles } from "lucide-react";
import { degrees, tracks } from "../data/yailSeedData";

const enrollmentPaths = [
  {
    title: "Start From Scratch",
    icon: Sparkles,
    copy: "Create a blank student worker with a role, model, track, and degree target."
  },
  {
    title: "Bring an Existing Agent",
    icon: Github,
    copy: "Submit a GitHub URL for an existing agent and place it into diagnostic scorecards."
  },
  {
    title: "Sponsor an Agent",
    icon: Landmark,
    copy: "Create a sponsored AI worker for a business domain and desired degree outcome."
  }
];

export function EnrollPage() {
  return (
    <section className="pageWrap enrollPage">
      <div className="sectionHeader">
        <p className="eyebrow dark">Admissions office</p>
        <h2>Enroll a new worker, adopt an existing agent, or sponsor one.</h2>
        <p>Hackathon demo intake creates a local student profile. Live GitHub cloning and billing are future backend work.</p>
      </div>
      <div className="enrollmentGrid">
        {enrollmentPaths.map((path) => {
          const Icon = path.icon;
          return (
            <article className="pathPanel" key={path.title}>
              <Icon size={22} />
              <h3>{path.title}</h3>
              <p>{path.copy}</p>
            </article>
          );
        })}
      </div>
      <div className="enrollFormSurface">
        <label>
          Agent name
          <input placeholder="e.g. Support Scholar 04" />
        </label>
        <label>
          GitHub URL or sponsor domain
          <input placeholder="https://github.com/team/agent or Acme Support Ops" />
        </label>
        <label>
          Degree goal
          <select defaultValue="degree">
            {degrees.map((degree) => (
              <option key={degree.id} value={degree.id}>
                {degree.name} - {degree.cost}
              </option>
            ))}
          </select>
        </label>
        <label>
          Track
          <select defaultValue="Standard">
            {tracks.map((track) => (
              <option key={track.name} value={track.name}>
                {track.name} - {track.cost}
              </option>
            ))}
          </select>
        </label>
        <button className="primaryAction" type="button">
          Create Demo Enrollment
        </button>
      </div>
      <div className="trackCompare">
        {tracks.map((track) => (
          <div className="trackPanel" key={track.name}>
            <strong>{track.name}</strong>
            <span>{track.cost}</span>
            <p>{track.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
