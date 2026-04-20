// Vercel Serverless Function — Server-side pe chalta hai, token safe rehta hai
export default async function handler(req, res) {
  // Sirf POST allow karo
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // Token server-side environment variable se aata hai (VITE_ prefix NAHI!)
  const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
  const REPO_OWNER = "umairrana007";
  const REPO_NAME = "ak-lasbela-analysis";

  if (!GITHUB_TOKEN) {
    return res.status(500).json({ error: 'Server config error: Token missing' });
  }

  try {
    const response = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/dispatches`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ event_type: 're-sync-ai' }),
      }
    );

    if (response.ok || response.status === 204) {
      return res.status(200).json({ success: true, message: 'AI Sync triggered!' });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: 'GitHub API error', detail: errorText });
    }
  } catch (err) {
    return res.status(500).json({ error: 'Network error', detail: err.message });
  }
}
