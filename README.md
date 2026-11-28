# VibeGuard — Member 4 complete frontend

A polished, responsive Next.js frontend for the VibeGuard Codeverse 2.0 project, based on the Member 4 Designer-Builder role in the supplied project document.

## What's included

- Landing page with interactive, rotating procedural **3D shield** (React Three Fiber / Three.js). This is a 3D model built in code, not a Blender-authored `.glb` asset.
- GitHub scan form with URL validation, loading and error states.
- Sample scan mode, clearly labeled **DEMO**.
- Security report: trust score, severity breakdown, expandable findings, explanations, copyable fix prompts, severity filtering, JSON export, browser Print → Save as PDF.
- Scan history stored in localStorage, with trend chart.
- Pricing page and optional Razorpay **test-mode** checkout integration; not activated without test credentials and backend order endpoint.
- Responsive layout for phones, tablets, desktops.

## Run locally

Requirements: Node.js 20.9+ and npm.

```bash
npm install
cp .env.example .env.local
npm run dev -- --port 3004
```

On Windows PowerShell, use `Copy-Item .env.example .env.local` instead of `cp` if needed.

Open http://localhost:3004.

## Connect Member 3's backend

Add this to `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://YOUR-FASTAPI-SERVICE.example.com
```

The frontend calls `POST ${NEXT_PUBLIC_API_URL}/scan` with:

```json
{"url":"https://github.com/owner/repository"}
```

Expected response:

```json
{
  "score": 87,
  "findings": [
    {
      "type": "insecure_pattern",
      "severity": "high",
      "file": "src/app.py",
      "line": 15,
      "title": "Unsafe eval call",
      "evidence": "eval(user_input)",
      "explanation": "Untrusted input could be executed.",
      "fix_prompt": "Replace eval with a safe parser."
    }
  ],
  "breakdown": {"Insecure code": 15}
}
```

The frontend normalizes this response and can compute a fallback score. Member 3 must enable CORS for the frontend's domain. Repository downloads, secure file processing, and scanner accuracy belong to Members 1–3 and are **not** implemented in this frontend.

## Optional Razorpay TEST checkout

Configure these values in `.env.local`:

```env
NEXT_PUBLIC_RAZORPAY_TEST_KEY=rzp_test_...
NEXT_PUBLIC_PAYMENT_API_URL=https://YOUR-BACKEND.example.com/create-order
```

The backend must create a **test order** with Razorpay and return `{"id":"order_...","amount":49900,"currency":"INR"}`. It must enforce the amount and currency server-side and verify the Razorpay signature after checkout before granting any access. The UI currently displays a message after checkout but **does not implement server-side payment verification, user accounts, subscriptions, or live payments**. Do not use production credentials or real payments in the hackathon demo.

## Deploy to Vercel

1. Push the project to a GitHub repository.
2. Import it in Vercel (Next.js is auto-detected).
3. Add the environment variables in the Vercel project settings.
4. Deploy. Test mobile view and your FastAPI CORS configuration.

## Limitations and honest demo claims

- The supplied sample repository and findings are illustrative, not a real GitHub scan.
- Scan history is stored in the browser only, not shared across users.
- PDF export uses the browser's print dialog rather than a dedicated PDF generator.
- The 3D shield is generated in Three.js instead of Blender; it can be replaced with a Blender-exported `.glb` later.
- No production payment flow, team accounts, or backend scanner is bundled.

## Team responsibilities

Member 4: frontend pages, UI/UX, animations, responsive design, report rendering, frontend deployment. Member 3: API and scanner orchestration. Members 1 and 2: scanner logic. Member 5: LLM explanations, benchmark and pitch.

## Version 2: Google login and onboarding
Create a Google Cloud OAuth Web application. Configure consent and test users if the app is in testing mode. Add exact redirect URIs `http://localhost:3004/api/auth/callback/google` and `https://YOUR-VERCEL-DOMAIN/api/auth/callback/google`. Set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, NEXTAUTH_SECRET (generate with Python `secrets.token_urlsafe(48)`), and NEXTAUTH_URL in `.env.local` and Vercel environment settings (use the appropriate origin). Restart/redeploy. Never publish secrets. The dashboard requires a verified Google account; no bypass is included. History is separated by account in localStorage, not encrypted or synchronized; users sharing a browser should clear sensitive reports. The FastAPI and payment endpoints need independent server-side authorization; this frontend login does not secure them. Test login, logout, direct dashboard access, and two accounts before submission.

Version 3: horizontal top navigation; snippet scanning removed.

## V4 cinematic onboarding
Five tutorial slides, pointer swipe/drag, keyboard arrows, progress dots, skip to Google sign-in, replay, and browser-local tutorial completion. The existing procedural Three.js shield is reused with reduced-motion and error fallback. Dashboard manual uses the same carousel. V3 navigation and authentication are unchanged. Copy your own `.env.local` from V3; never commit it. Register the exact localhost port and deployed callback with Google. Production build and browser testing are required.

## V5 onboarding
Mouse wheel down/up advances/reverses the horizontal scroll track. Touch and keyboard remain supported. No Next/Back buttons.

## V6 onboarding
Full-width individual slides with cyan procedural 3D artwork. Mouse wheel, trackpad, touch and arrow navigation. Google OAuth configuration remains required; register the exact callback URL.

## V7 additions
Use `npm run dev -- --port 3004` or the included Python launcher. Register `http://localhost:3004` and `http://localhost:3004/api/auth/callback/google` in Google Cloud. ZIP optimization is local in the browser; the original is untouched. The 100 MiB input and 250 MiB declared expansion limits are preliminary client checks, not a security boundary. Gitignore filtering is best-effort (nested rules supported, not a complete Git index implementation); dependency manifests are retained unless their containing cache directory is excluded. Review excluded files. Member 3 must implement `POST /scan/zip` with multipart field `file`, returning the same JSON schema as `/scan`. Server must independently enforce streaming expansion limits, path safety, symlink rejection, authorization, rate limits, CORS, cleanup and no execution. Never trust browser checks. Public GitHub access must be enforced by the backend. No real scanner or payment backend is included.
