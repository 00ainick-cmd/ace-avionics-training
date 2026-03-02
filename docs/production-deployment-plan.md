# Take ACE Avionics Training Live — Implementation Plan

## Current State

The ACE Avionics Training platform is a **static HTML/JS application** with two backend strategies:

1. **Local**: `server.py` (Python `http.server` + SQLite) serving both static files and REST APIs on `localhost:8000`. No authentication, no HTTPS, wide-open CORS (`*`).
2. **Cloud**: Supabase (PostgreSQL) for enrollment auth (`ace_enrollments` table), analytics tracking, and a skeleton Stripe webhook Edge Function.

**What already exists:**
- `enrollment.html` + `ace-auth.js` — enrollment code validation via Supabase
- `admin.html` — instructor dashboard with student CRUD (talks to local `server.py`)
- `supabase/functions/stripe-webhook/index.ts` — Deno Edge Function skeleton (placeholder Stripe Price IDs)
- `supabase-client.js` — analytics tracking to Supabase

**Critical Security Problems:**
- Supabase URL and anon key hardcoded in client JS (this is actually *normal* for Supabase anon key — it's designed to be public, but RLS must be properly configured)
- No admin page authentication — anyone who knows the URL `/admin.html` can manage students
- CORS is `Access-Control-Allow-Origin: *` (fine for dev, dangerous in production)
- No rate limiting on any endpoint
- No HTTPS (Python's `http.server` is HTTP only)
- `DELETE /api/students/all` (purge) has zero authentication

---

## Deployment Architecture Decision

> [!IMPORTANT]
> **The biggest architectural decision**: Your current `server.py` (Python/SQLite) is designed for **offline/restricted environments** only. For going live on the internet, we should use **Supabase as the sole backend** and deploy the frontend to **Vercel** (or Netlify) as a static site.
>
> This means the admin dashboard will also talk to Supabase instead of `server.py`. The local Python server would remain available for offline/classroom use only.

### Why Not Wix?

Wix **cannot host raw HTML/JS static files**. It's a closed website builder — you design pages in its editor, and it generates & serves its own HTML. Your app is 40+ custom HTML files with JavaScript modules, JSON data banks, and complex routing. Wix can't serve this.

**The solution**: Keep your domain (`aceavionicstraining.com`) registered at Wix. Point its DNS (via CNAME record) to **Vercel**, which hosts your actual app. Visitors go to `aceavionicstraining.com` → Vercel serves your files. Free, automatic HTTPS, global CDN.

### Proposed Stack
| Layer | Technology | Why |
|:---|:---|:---|
| **Frontend Hosting** | **Vercel** (free tier) | Zero-config static hosting, automatic HTTPS, global CDN, GitHub auto-deploy |
| **Database + Auth** | **Supabase** (existing project) | Already set up, RLS-capable, Edge Functions for webhooks |
| **Payments** | **Stripe Checkout** | Pre-built hosted payment page, PCI-compliant, webhook integration |
| **Domain** | **Wix DNS → Vercel** | Keep domain at Wix, point CNAME to Vercel |

---

## Confirmed Parameters

| Parameter | Value |
|:---|:---|
| **Stripe** | ✅ Existing account |
| **Domain** | `aceavionicstraining.com` (owned via Wix) |
| **Plan: Yearly** | $247/yr (365 days access) |
| **Plan: Lifetime** | $397 (no expiration) |

> [!WARNING]
> **The local `server.py` cannot be used for a public-facing deployment**. Python's built-in `http.server` is explicitly not production-ready. The plan below moves admin functions to Supabase while keeping `server.py` available for offline classroom use.

---

## Proposed Changes

### Security Hardening — Supabase RLS & Admin Auth

These changes secure the platform so that only authorized users can access admin functions and student data.

---

#### [NEW] [ace-admin-auth.js](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/shared/js/ace-admin-auth.js)

New client-side admin auth module that gates `admin.html` behind a password check. Uses Supabase's built-in auth (email/password) for admin users.

- Creates `AceAdminAuth` global with `login(email, password)`, `require()`, and `signOut()` methods
- `require()` redirects non-authenticated users to a login modal
- Admin credentials stored in Supabase Auth (not hardcoded)

---

#### [MODIFY] [admin.html](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/admin.html)

- Add login gate: show a password modal before rendering admin content
- Switch all API calls from `localhost:8000` to Supabase REST endpoints
- Add enrollment management section (view/create/deactivate enrollment codes)
- Add manual "Enroll Student" button that generates a code and optionally emails it
- Remove seed/purge functions from the production UI (move to dev-only)

---

#### [NEW] [supabase-admin-schema.sql](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/docs/supabase-admin-schema.sql)

SQL to run in Supabase SQL editor:
- Create `admin_users` role check function
- Add RLS policies: admin-only read/write on `students`, `diagnostic_scores`, `ace_enrollments`
- Add read-only policy for `ace_enrollments` so students can validate their own code (existing behavior)

---

#### [NEW] [.env.example](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/.env.example)

Template for environment variables:
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`  
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_YEARLY`, `STRIPE_PRICE_LIFETIME`

---

#### [MODIFY] [ace-auth.js](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/shared/js/ace-auth.js)

- Extract Supabase URL/key into shared config module (imported by both auth and admin)
- No hardcoded keys in the file (use a config pattern since this is a static site — the anon key is meant to be public, but centralize it)

---

#### [MODIFY] [server.py](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/server.py)

- Add `X-Admin-Key` header check for destructive endpoints (`DELETE`, seed)
- Tighten CORS to configurable origin list
- Add basic rate limiting (in-memory, per-IP)
- This is for the **offline classroom** mode only; production uses Supabase

---

### Stripe Integration

These changes enable the purchase → enrollment flow.

---

#### [NEW] [checkout.html](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/checkout.html)

A pricing/checkout page that:
- Displays plan options (Yearly $247, Lifetime $397)
- Uses Stripe Checkout (redirect to Stripe-hosted payment page)
- Includes a "Buy Now" button that calls `Stripe.redirectToCheckout()` with the correct Price ID
- After successful payment, Stripe redirects to a success page

---

#### [NEW] [checkout-success.html](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/checkout-success.html)

Post-payment landing page:
- Thanks the customer
- Instructs them to check email for their access code
- Links to `enrollment.html` to activate

---

#### [MODIFY] [stripe-webhook/index.ts](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/supabase/functions/stripe-webhook/index.ts)

- Replace placeholder `PRICE_MAP` keys with `yearly` ($247, 365 days) and `lifetime` ($397, no expiry)
- Add email notification via Supabase Edge Function (send access code to buyer)
- Add idempotency check (don't create duplicate enrollments for the same Stripe session)

---

### Admin Enrollment Management

These changes give the admin page the ability to manage enrollment codes directly.

---

#### [MODIFY] [admin.html](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/admin.html)

Add a new "Enrollments" tab/section with:
- **Enrollment table**: code, email, plan, status (active/expired/deactivated), activated date
- **Generate Code button**: manually create enrollment codes (for comp/scholarship)
- **Deactivate/Reactivate toggle**: disable a code without deleting it
- **Extend Expiry**: push the expiration date forward
- Search/filter by email, code, or status

---

### Deployment Configuration

---

#### [NEW] [vercel.json](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/vercel.json)

Vercel deployment config:
- Set root directory
- Configure SPA fallback routes
- Add security headers (X-Frame-Options, CSP, HSTS, etc.)

---

#### [NEW] [deployment-guide.md](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/docs/deployment-guide.md)

Step-by-step deployment guide covering:
1. Stripe account + product setup
2. Supabase schema setup + RLS policies
3. Supabase Edge Function deployment
4. Vercel deployment from GitHub
5. DNS/domain configuration
6. Environment variable configuration
7. Go-live checklist

---

#### [MODIFY] [.gitignore](file:///c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/.gitignore)

Add:
- `*.db` (don't commit SQLite databases)
- `.env` (already present via `.env` pattern)
- `node_modules/` (if any npm packages get added)

---

## Verification Plan

### Automated Browser Tests

1. **Enrollment gate test**: Navigate to `dashboard.html` without enrollment → verify redirect to `enrollment.html`
   - Run: Use the browser tool to navigate to the live/local URL and check for redirect

2. **Admin auth gate test**: Navigate to `admin.html` without login → verify login modal appears
   - Run: Use the browser tool to navigate to `admin.html` and verify the login overlay is displayed

3. **Checkout page test**: Navigate to `checkout.html` → verify pricing cards render and Stripe buttons are functional
   - Run: Use the browser tool to navigate and check for Stripe elements

### Manual Verification (User Required)

1. **Stripe end-to-end test**:
   - Use Stripe test mode with test card `4242 4242 4242 4242`
   - Complete a checkout → verify webhook creates enrollment in Supabase
   - Use the generated access code on `enrollment.html` → verify access to dashboard
   - **You (the user) will need to**: Set up Stripe test products, run the webhook locally or deploy the edge function, and test the full flow

2. **Admin login test**:
   - Create an admin user in Supabase Auth dashboard
   - Log in at `admin.html` → verify access to student roster
   - Try accessing admin without login → verify blocked

3. **Security spot-check**:
   - Try accessing `/api/students` directly → verify it requires auth
   - Check browser DevTools Network tab for exposed credentials
   - Verify CORS headers only allow your production domain

4. **Deployment test**:
   - Push to GitHub → verify Vercel auto-deploys
   - Check HTTPS certificate is active
   - Test the live URL from an incognito browser
