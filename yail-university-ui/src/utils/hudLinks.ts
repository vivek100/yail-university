const environmentIds: Record<string, string> = {
  "yail-gdpval:v7": "e3aa769a-9ff2-4cec-9a5d-cdbddd940d91",
  "yail-gdpval": "e3aa769a-9ff2-4cec-9a5d-cdbddd940d91",
  "autonomous-business": "b2364931-c6be-426d-b2f3-b13050b68755",
  "autonomous-business template": "b2364931-c6be-426d-b2f3-b13050b68755",
  "autonomous-business smoke taskset": "b2364931-c6be-426d-b2f3-b13050b68755",
  "autonomous-business + GDPval curriculum traces": "b2364931-c6be-426d-b2f3-b13050b68755",
  "yail-trace-explorer-v6": "5115be5a-b308-4f4f-9120-f38acb584806"
};

export function getEnvironmentUrl(environment: string) {
  const id = environmentIds[environment];
  return id ? `https://www.hud.ai/environments/${id}/scenarios` : null;
}

export function getTraceUrl(traceId?: string) {
  return traceId ? `https://www.hud.ai/trace/${traceId}` : null;
}

export function getJobUrl(jobId?: string) {
  return jobId ? `https://hud.ai/jobs/${jobId}` : null;
}

export function formatShortId(id?: string) {
  if (!id) return null;
  return id.length > 14 ? `${id.slice(0, 8)}...${id.slice(-6)}` : id;
}
