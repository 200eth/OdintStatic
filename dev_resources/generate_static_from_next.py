import os
import re

NEXT_APP_DIR = r"D:\Working\Working Directory\Ai Project\Odint V1\Odint\odint-site\src\app"
OUT_DIR = r"D:\Working\Working Directory\Ai Project\Odint V2"

HEADER = """<header class="header" role="banner">
  <div class="header-container">
    <div class="header-content">
      <a href="/index.html" class="logo" aria-label="Lucent by Odint Technologies - Home">
        <img src="/images/lucent-logo-v3.png" alt="Lucent logo" class="logo-icon" />
        Lucent
      </a>
      <nav class="nav" role="navigation" aria-label="Main navigation">
        <ul class="nav-list">
          <li><a href="/platform.html" class="nav-link">Platform</a></li>
          <li><a href="/modules.html" class="nav-link">Modules</a></li>
          <li class="dropdown">
            <button class="dropdown-trigger" aria-expanded="false" aria-haspopup="true">
              Features
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div class="dropdown-menu" role="menu">
              <ul class="dropdown-list">
                <li class="dropdown-item"><a href="/features/digital-risk-protection.html" class="dropdown-link"><strong>Digital Risk Protection</strong><small>Monitor and protect against digital threats</small></a></li>
                <li class="dropdown-item"><a href="/features/technology-and-ai.html" class="dropdown-link"><strong>AI Technology</strong><small>Advanced threat detection and analysis</small></a></li>
                <li class="dropdown-item"><a href="/features/soc-workflows.html" class="dropdown-link"><strong>SOC Workflows</strong><small>Streamlined security operations</small></a></li>
              </ul>
            </div>
          </li>
          <li class="dropdown">
            <button class="dropdown-trigger" aria-expanded="false" aria-haspopup="true">
              Solutions
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div class="dropdown-menu" role="menu">
              <ul class="dropdown-list">
                <li class="dropdown-item"><a href="/solutions/business-continuity-resilience.html" class="dropdown-link"><strong>Business Continuity</strong><small>Ensure operational resilience</small></a></li>
                <li class="dropdown-item"><a href="/solutions/enterprise-regulatory-compliance.html" class="dropdown-link"><strong>Regulatory Compliance</strong><small>Meet industry standards</small></a></li>
                <li class="dropdown-item"><a href="/solutions/ransomware-preparedness.html" class="dropdown-link"><strong>Ransomware Defense</strong><small>Protect against ransomware</small></a></li>
              </ul>
            </div>
          </li>
          <li class="dropdown">
            <button class="dropdown-trigger" aria-expanded="false" aria-haspopup="true">
              Industries
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div class="dropdown-menu" role="menu">
              <ul class="dropdown-list">
                <li class="dropdown-item"><a href="/industries/financial-services.html" class="dropdown-link"><strong>Financial Services</strong><small>Banking and finance security</small></a></li>
                <li class="dropdown-item"><a href="/industries/government-public-sector.html" class="dropdown-link"><strong>Government</strong><small>Public sector cybersecurity</small></a></li>
                <li class="dropdown-item"><a href="/industries/healthcare.html" class="dropdown-link"><strong>Healthcare</strong><small>Medical data protection</small></a></li>
              </ul>
            </div>
          </li>
          <li><a href="/company/about-us.html" class="nav-link">Company</a></li>
        </ul>
      </nav>
      <button class="mobile-menu-toggle" aria-label="Toggle mobile menu" aria-expanded="false">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
</header>"""

HTML_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/main.css">
  <link rel="stylesheet" href="/styles/navigation.css">
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <div class="overlay" aria-hidden="true"></div>
  {header}
  <main id="main-content" role="main">
    {content}
  </main>
  <script src="https://unpkg.com/lucide@latest/dist/lucide.min.js"></script>
  <script>try{{lucide.createIcons();}}catch(e){{}}</script>
  <script src="/js/navigation.js"></script>
</body>
</html>"""

def route_to_out_path(route_parts):
  if not route_parts:
    return None
  if route_parts == ["page.tsx"]:
    return os.path.join(OUT_DIR, "index.html")
  parts = [p for p in route_parts[:-1] if p != "(.)" and p != "(..)" and p]
  if parts[-1] == "":
    parts = parts[:-1]
  if len(parts) == 1:
    # Place index.html inside directory for section roots like solutions, features, industries
    section = parts[0]
    if section in ["solutions", "features", "industries", "company"]:
      return os.path.join(OUT_DIR, section, "index.html")
    return os.path.join(OUT_DIR, f"{section}.html")
  return os.path.join(OUT_DIR, os.path.join(*parts) + ".html")

def extract_texts(tsx):
  texts = []
  for m in re.findall(r">([^<>{}][^<]+)<", tsx):
    t = m.strip()
    if t:
      texts.append(t)
  for m in re.findall(r"title:\s*['\"]([^'\"]+)['\"]", tsx):
    texts.append(m.strip())
  for m in re.findall(r"subtitle\s*=\s*['\"]([^'\"]+)['\"]", tsx):
    texts.append(m.strip())
  return texts

def build_generic_html(texts):
  inner = []
  if texts:
    inner.append(f'<section class="py-16 bg-white"><div class="container"><h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-6">{texts[0]}</h1>')
    for t in texts[1:]:
      inner.append(f'<p class="text-gray-700 mb-4">{t}</p>')
    inner.append('</div></section>')
  return "\n".join(inner)

def build_home_html():
  hero = '''
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 z-0">
        <img src="/globe.svg" alt="" class="object-cover w-full h-full" />
        <div class="absolute inset-0 hero-overlay"></div>
      </div>
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">Proactive. AI-Driven. Comprehensive.</h1>
        <p class="text-lg md:text-2xl text-gray-200 mb-8 max-w-4xl mx-auto leading-relaxed">
          LUCENT is a GenAI-powered external threat intelligence platform that gives Malaysian enterprises and public agencies real-time visibility into threats across the Surface, Deep, and Dark Web. We help you see attacks before they strike, and understand what happened after—down to the who, where, when, and how. Consolidate CTI, DRP, and EASM into one system that prioritizes what matters and guides swift mitigation. Know more, prioritize better, act faster.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/contact-us.html" class="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold">Request Live Demo</a>
          <a href="/about-us.html" class="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold">Baseline Assessment</a>
        </div>
      </div>
    </section>
  '''
  why = '''
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900">Why LUCENT</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="shield" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Context-driven, Malaysia-ready intelligence</h3>
            <p class="text-sm text-gray-600">Aligned to your assets, industry, and risk profile. Multi-layer coverage, GenAI scoring, and MITRE ATT&amp;CK mapping reduce noise and spotlight real risk.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="network" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Seamless integrations and workflows</h3>
            <p class="text-sm text-gray-600">Alerting and mitigation workflows accelerate decisions and response. Fits SOCs at scale and teams just starting—day-one operating model fit.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="radar" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Prioritize what matters</h3>
            <p class="text-sm text-gray-600">GenAI scoring and context cut through noise so analysts act on real risk first.</p>
          </div>
        </div>
      </div>
    </section>
  '''
  what = '''
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900">What You Get</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="shield" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Unified visibility</h3>
            <p class="text-sm text-gray-600">Exposed assets, credential leaks, phishing infrastructure, and vulnerabilities—correlated with active threat actor activity.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="network" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Data and feeds</h3>
            <p class="text-sm text-gray-600">Raw data, enriched IOCs, and AI-generated feeds with STIX/TAXII for downstream tools.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="zap" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Recommendations and tracking</h3>
            <p class="text-sm text-gray-600">Automated recommendations and process management to track closure across teams.</p>
          </div>
        </div>
      </div>
    </section>
  '''
  sectors = '''
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900">Built for Malaysia’s Critical Sectors</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="shield" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Government, security, and law enforcement</h3>
            <p class="text-sm text-gray-600">Early warnings, clear risk prioritization, and audit-friendly reporting.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="network" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Financial institutions and telecommunications</h3>
            <p class="text-sm text-gray-600">Tailored monitoring plans aligned to Malaysian footprint and priorities.</p>
          </div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="building" class="w-6 h-6 text-blue-600"></i></div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Critical infrastructure and enterprises</h3>
            <p class="text-sm text-gray-600">Scales from single team deployments to MSSP multi-tenant delivery.</p>
          </div>
        </div>
      </div>
    </section>
  '''
  outcomes = '''
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900">Outcomes That Matter</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Identify threats 3× faster and streamline mitigation to as few as four clicks.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Reduce fraud by detecting compromised cards and credentials before abuse.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Strengthen operational resilience with early warnings and actionable next steps.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Build trust with transparent intelligence, audit trails, and consistent reporting.</p></div>
        </div>
      </div>
    </section>
  '''
  cta = '''
    <section class="py-20 bg-blue-600">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">See how LUCENT protects Malaysian organizations</h2>
        <p class="text-lg md:text-xl text-blue-100 mb-8 max-w-3xl mx-auto">Request a live demo and baseline assessment.</p>
        <a href="/contact-us.html" class="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold">Request Demo</a>
      </div>
    </section>
  '''
  legal = '''
    <section class="py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="sr-only">Legal and Notes</h2>
        <p class="text-xs text-gray-600">Important Notice Features and specifications are subject to change as the platform evolves. Certain functions may be subject to organizational policies or jurisdictional considerations. Contact our team for the most current capabilities and availability. © 2025 Odint Technologies Sdn Bhd.</p>
      </div>
    </section>
  '''
  summary = '''
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-8"><h2 class="text-2xl md:text-3xl font-bold text-gray-900">Summary</h2></div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">LUCENT unifies CTI, DRP, and EASM with GenAI for proactive, external threat intelligence.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Modules cover exposed assets, credentials, phishing, vulnerabilities, fraud, actors, IOCs, and ad-hoc investigations.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Dashboards, alerts, recommendations, and integrations turn intelligence into action with audit-ready workflows.</p></div>
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col"><p class="text-sm text-gray-700">Built to protect Malaysian public sector and enterprises with rapid deployment and measurable outcomes.</p></div>
        </div>
      </div>
    </section>
  '''
  return hero + why + what + sectors + outcomes + cta + legal + summary
def build_modules_html(tsx):
  hero = '''
    <div class="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold mb-6">Lucent Modules</h1>
          <p class="text-xl md:text-2xl text-blue-100 max-w-4xl mx-auto">External intelligence that turns visibility into action. Discover risk, prioritize with GenAI context, and drive mitigation across your stack.</p>
        </div>
      </div>
    </div>
  '''
  titles = re.findall(r"title:\s*'([^']+)'", tsx)
  descs = re.findall(r"description:\s*'([^']+)'", tsx)
  icons = re.findall(r"icon:\s*([A-Za-z]+)", tsx)
  variants = re.findall(r"variant:\s*'([^']+)'", tsx)
  def icon_attr(name):
    return name.replace('KeyRound','key-round').replace('BadgeAlert','badge-alert').replace('CreditCard','credit-card').replace('UserSearch','user-search').replace('ListChecks','list-checks').replace('Globe','globe').replace('Bug','bug').replace('Search','search').lower()
  grid_items = []
  for i, t in enumerate(titles):
    d = descs[i] if i < len(descs) else ""
    ic = icon_attr(icons[i]) if i < len(icons) else ""
    var = variants[0] if (i == 0 and variants) else ""
    span = ' md:col-span-2' if var == 'large' else ''
    icon_block = f'<div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4"><i data-lucide="{ic}" class="w-6 h-6 text-blue-600"></i></div>' if ic else ''
    item_html = f'''
      <div class="h-full">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow h-full flex flex-col{span}">
          {icon_block}
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{t}</h3>
          <p class="text-sm text-gray-600">{d}</p>
        </div>
      </div>
    '''
    grid_items.append(item_html)
  grid = f'''
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">
        {''.join(grid_items)}
      </div>
    </div>
  '''
  cta = '''
    <div class="bg-blue-900 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold mb-4">Ready to Enhance Your Security Posture?</h2>
        <p class="text-xl text-blue-100 mb-8">Explore how Lucent's modules can protect your organization</p>
        <div class="flex flex-col sm:flex-row items-center gap-4 justify-center">
          <a href="/contact-us.html" class="inline-flex items-center justify-center h-50 px-8 py-0 bg-white text-blue-900 rounded-lg font-semibold hover:bg-blue-50 transition-colors">Schedule Demo</a>
          <a href="/modules.html" class="inline-flex items-center justify-center h-50 px-8 py-0 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-900 transition-colors">Learn More</a>
        </div>
      </div>
    </div>
  '''
  return hero + grid + cta
def build_page_with_hero(tsx, texts):
  title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  subtitle_match = re.search(r"subtitle\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  from_match = re.search(r"from\s*=\s*['\"](from-[^'\"]+)['\"]", tsx)
  to_match = re.search(r"to\s*=\s*['\"](to-[^'\"]+)['\"]", tsx)
  title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
  subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
  from_cls = from_match.group(1).strip() if from_match else "from-blue-900"
  to_cls = to_match.group(1).strip() if to_match else "to-blue-700"
  hero = f'''
    <div class="bg-gradient-to-r {from_cls} {to_cls} text-white py-20">
      <div class="container">
        <h1 class="text-4xl font-bold mb-4">{title}</h1>
        <p class="text-xl text-blue-100 max-w-4xl">{subtitle}</p>
      </div>
    </div>
  '''
  body = build_generic_html([t for t in texts if t != title and t != subtitle])
  return hero + body
def build_solution_html(tsx, texts):
  title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  subtitle_match = re.search(r"subtitle\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
  subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
  issue_idx = None
  sol_idx = None
  for i, t in enumerate(texts):
    if t == "Example of the challenge":
      issue_idx = i
    if t == "What LUCENT can do for you":
      sol_idx = i
  issue_p = texts[issue_idx + 1] if issue_idx is not None and issue_idx + 1 < len(texts) else ""
  solution_p = texts[sol_idx + 1] if sol_idx is not None and sol_idx + 1 < len(texts) else ""
  cta_title = ""
  cta_desc = ""
  cta_btn1 = "Talk to an expert"
  cta_btn2 = "Get started"
  m = re.search(r"bg-gradient-to-r[\s\S]*?<h3[^>]*>(.*?)</h3>[\s\S]*?<p[^>]*>(.*?)</p>[\s\S]*?<a[^>]*>(.*?)</a>[\s\S]*?<a[^>]*>(.*?)</a>", tsx, re.DOTALL)
  if m:
    cta_title = m.group(1).strip()
    cta_desc = m.group(2).strip()
    cta_btn1 = m.group(3).strip()
    cta_btn2 = m.group(4).strip()
  hero = f'''
    <div class="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-20">
      <div class="container">
        <h1 class="text-4xl font-bold mb-4">{title}</h1>
        <p class="text-xl text-blue-100 max-w-4xl">{subtitle}</p>
      </div>
    </div>
  '''
  breadcrumbs = f'''
    <div class="container py-8"><nav class="text-sm text-gray-600"><a href="/index.html">Home</a> / <a href="/solutions/">Solutions</a> / <span class="text-gray-900">{title}</span></nav></div>
  '''
  grid = f'''
    <section class="container py-12">
      <h2 class="sr-only">Problem and Solution</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="rounded-2xl border border-blue-100 shadow-sm bg-white">
          <div class="p-6">
            <div class="flex items-center gap-3 mb-4">
              <i class="text-blue-700" data-lucide="alert-triangle"></i>
              <span class="text-sm font-semibold text-blue-700 uppercase tracking-wide">Issue</span>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Example of the challenge</h3>
            <p class="text-gray-700">{issue_p}</p>
          </div>
        </div>
        <div class="rounded-2xl border border-blue-100 shadow-sm bg-gradient-to-br from-blue-50 to-blue-100">
          <div class="p-6">
            <div class="flex items-center gap-3 mb-4">
              <i class="text-blue-800" data-lucide="check-circle"></i>
              <span class="text-sm font-semibold text-blue-800 uppercase tracking-wide">Solution</span>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">What LUCENT can do for you</h3>
            <p class="text-gray-800">{solution_p}</p>
          </div>
        </div>
      </div>
    </section>
  '''
  cta = f'''
    <div class="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-12">
      <div class="container text-center">
        <h3 class="text-2xl font-bold mb-3">{cta_title or "Build resilient operations"}</h3>
        <p class="text-blue-100 mb-6">{cta_desc or "Design continuity plans with Lucent."}</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/company/contact-us.html" class="btn btn-white">{cta_btn1}</a>
          <a href="/getting-started.html" class="btn btn-primary">{cta_btn2}</a>
        </div>
      </div>
    </div>
  '''
  return hero + breadcrumbs + grid + cta

def build_features_html(tsx, texts):
  title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  subtitle_match = re.search(r"subtitle\s*=\s*['\"]([^'\"]+)['\"]", tsx)
  title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
  subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
  # section titles and contents
  sec_titles = re.findall(r'title:\s*[\'"]([^\'"]+)[\'"]', tsx)
  sec_contents = re.findall(r'content:\s*[\'"]([^\'"]+)[\'"]', tsx)
  sec_images = re.findall(r'imageSrc:\s*[\'"]([^\'"]+)[\'"]', tsx)
  sec_reverse = re.findall(r'reverse:\s*(true|false)', tsx)
  hero = f'''
    <div class="bg-gradient-to-r from-purple-900 to-purple-700 text-white py-20">
      <div class="container">
        <h1 class="text-4xl font-bold mb-4">{title}</h1>
        <p class="text-xl text-purple-100 max-w-4xl">{subtitle}</p>
      </div>
    </div>
  '''
  breadcrumbs = f'''
    <div class="container py-8"><nav class="text-sm text-gray-600"><a href="/index.html">Home</a> / <a href="/features/">Features</a> / <span class="text-gray-900">{title}</span></nav></div>
  '''
  sections = []
  for i in range(min(len(sec_titles), len(sec_contents), len(sec_images))):
    rev = (i < len(sec_reverse) and sec_reverse[i] == 'true')
    img_block = f'''
      <div class="{ 'md:order-last' if rev else ''}">
        <div class="overflow-hidden rounded-xl border border-gray-200 bg-gray-50">
          <img src="{sec_images[i]}" alt="{sec_titles[i]}" class="w-full md:w-3/5 h-auto object-cover mx-auto" />
        </div>
      </div>
    '''
    text_block = f'''
      <div>
        <h3 class="text-2xl font-bold text-gray-900 mb-3">{sec_titles[i]}</h3>
        <p class="text-gray-700 text-lg leading-relaxed">{sec_contents[i]}</p>
      </div>
    '''
    row = f'''
      <div class="mb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          {img_block}
          {text_block}
        </div>
      </div>
    '''
    sections.append(row)
  grid = f'<section class="container py-12">{"".join(sections)}</section>'
  # CTA
  m = re.search(r"bg-gradient-to-r[\s\S]*?<h3[^>]*>(.*?)</h3>[\s\S]*?<p[^>]*>(.*?)</p>[\s\S]*?<a[^>]*>(.*?)</a>[\s\S]*?<a[^>]*>(.*?)</a>", tsx, re.DOTALL)
  cta_title = m.group(1).strip() if m else "Ready to reduce external risk?"
  cta_desc = m.group(2).strip() if m else "See how Lucent protects brands and identities beyond your perimeter."
  cta_btn1 = m.group(3).strip() if m else "Talk to our team"
  cta_btn2 = m.group(4).strip() if m else "Get started"
  cta = f'''
    <div class="bg-gradient-to-r from-purple-900 to-purple-700 text-white py-12">
      <div class="container text-center">
        <h3 class="text-2xl font-bold mb-3">{cta_title}</h3>
        <p class="text-purple-100 mb-6">{cta_desc}</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/company/contact-us.html" class="btn btn-white">{cta_btn1}</a>
          <a href="/getting-started.html" class="btn btn-primary">{cta_btn2}</a>
        </div>
      </div>
    </div>
  '''
  return hero + breadcrumbs + grid + cta

def build_industries_html(tsx, texts):
  # Hero with overlay image
  img_match = re.search(r'SafeImage[\\s\\S]*?src="([^"]+)"', tsx)
  hero_img = img_match.group(1).strip() if img_match else ""
  title_match = re.search(r'h1[^>]*>([^<]+)</h1>', tsx)
  # Fallback: find first h1-like title from text list
  title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Industry")
  subtitle_match = re.search(r'className="text-xl[^"]*"[^>]*>([^<]+)</p>', tsx)
  subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
  hero = f'''
    <section class="relative hero-62vh bg-gradient-to-r from-blue-900 to-blue-700 flex items-center justify-center">
      <img src="{hero_img}" alt="{title}" class="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-20" />
      <div class="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
        <h1 class="text-5xl md:text-6xl font-bold mb-6">{title}</h1>
        <p class="text-xl md:text-2xl mb-8">{subtitle}</p>
      </div>
    </section>
  '''
  # Key Vulnerabilities block: capture four headings and descriptions after "Key Vulnerabilities"
  kv_idx = texts.index("Key Vulnerabilities") if "Key Vulnerabilities" in texts else -1
  kv_titles = []
  kv_descs = []
  if kv_idx != -1:
    # expect 4 pairs after the header
    # heuristic: next 8 strings alternating title/desc
    pairs = texts[kv_idx+1:kv_idx+9]
    for i in range(0, len(pairs), 2):
      if i+1 < len(pairs):
        kv_titles.append(pairs[i])
        kv_descs.append(pairs[i+1])
  kv_cards = []
  # Try to pick lucide icons used in the TSX for Key Vulnerabilities
  kv_icon_candidates = re.findall(r'<(CreditCard|ShieldAlert|Server|FileCheck)[^>]*>', tsx)
  for i in range(len(kv_titles)):
    icon_name = kv_icon_candidates[i] if i < len(kv_icon_candidates) else "ShieldAlert"
    icon_attr = icon_name.replace('ShieldAlert','shield-alert').replace('FileCheck','file-check').replace('CreditCard','credit-card').lower()
    kv_cards.append(f'''
      <div class="text-center bg-blue-50 rounded-lg p-6">
        <div class="mx-auto mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-700"><i data-lucide="{icon_attr}" class="w-6 h-6"></i></div>
        <h3 class="text-lg font-semibold mb-2">{kv_titles[i]}</h3>
        <p class="text-gray-600">{kv_descs[i]}</p>
      </div>
    ''')
  kv_grid = f'''
    <section class="py-16 px-4">
      <div class="container">
        <div class="mb-16">
          <h2 class="text-4xl font-bold text-center text-gray-900 mb-12">Key Vulnerabilities</h2>
          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {''.join(kv_cards)}
          </div>
        </div>
  '''
  # "What LUCENT can do for you" list: gather next bullet points
  wl_idx = texts.index("What LUCENT can do for you") if "What LUCENT can do for you" in texts else -1
  bullets = []
  bullet_icons = []
  if wl_idx != -1:
    bullets = texts[wl_idx+1:wl_idx+6]
    # detect icons used in bullets (up to 5)
    bullet_icons = re.findall(r'<span[^>]*>\\s*<([A-Za-z]+)\\b', tsx)
  def icon_to_attr(name):
    return name.replace('ShieldCheck','shield-check').replace('BrainCircuit','brain-circuit').replace('CreditCard','credit-card').replace('Search','search').replace('Network','network').lower()
  wl_list = ''.join([
    f'<li class="flex items-start gap-3"><span class="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-blue-50 text-blue-700"><i data-lucide="{icon_to_attr(bullet_icons[i]) if i < len(bullet_icons) else "circle"}" class="w-5 h-5"></i></span><span>{b}</span></li>'
    for i, b in enumerate(bullets)
  ])
  wl_block = f'''
        <div class="grid md:grid-cols-2 gap-12 items-center mb-16">
          <div class="md:col-span-2 max-w-3xl mx-auto">
            <h2 class="text-4xl font-bold text-gray-900 mb-6 text-center">What LUCENT can do for you</h2>
            <ul class="space-y-4 text-gray-700">
              {wl_list}
            </ul>
          </div>
        </div>
      </div>
    </section>
  '''
  # CTA
  cta_match = re.search(r'bg-gradient-to-r[^>]*>\\s*[\\s\\S]*?<h2[^>]*>([^<]+)</h2>[\\s\\S]*?<p[^>]*>([^<]+)</p>[\\s\\S]*?<button[^>]*>([^<]+)</button>', tsx, re.DOTALL)
  cta_title = cta_match.group(1).strip() if cta_match else "Secure Your Operations"
  cta_desc = cta_match.group(2).strip() if cta_match else "Protect with industry-leading cybersecurity solutions."
  cta_btn = cta_match.group(3).strip() if cta_match else "Get Started"
  cta = f'''
    <div class="container">
      <div class="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-8 text-center text-white">
        <h2 class="text-3xl font-bold mb-4">{cta_title}</h2>
        <p class="text-xl mb-6">{cta_desc}</p>
        <a class="btn btn-white" href="/company/contact-us.html">{cta_btn}</a>
      </div>
    </div>
  '''
  return hero + kv_grid + wl_block + cta
def main():
  generated = []
  for root, _, files in os.walk(NEXT_APP_DIR):
    for f in files:
      if f == "page.tsx":
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, NEXT_APP_DIR).replace("\\", "/").split("/")
        out_path = route_to_out_path(rel)
        if not out_path:
          continue
        with open(fp, "r", encoding="utf-8") as fh:
          tsx = fh.read()
        texts = extract_texts(tsx)
        if rel == ["page.tsx"]:
          title = "Lucent - Enterprise Cybersecurity Solutions | Odint Technologies"
          content_html = build_home_html()
        elif "solutions" in rel:
          content_html = build_solution_html(tsx, texts)
          title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
          title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
        elif "features" in rel:
          content_html = build_features_html(tsx, texts)
          title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
          title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
        elif "industries" in rel:
          content_html = build_industries_html(tsx, texts)
          title = texts[0] if texts else "Industry"
        elif "modules" in rel:
          content_html = build_modules_html(tsx)
          title = "Lucent Modules"
        else:
          title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", tsx)
          title = title_match.group(1).strip() if title_match else (texts[0] if texts else "Lucent")
          content_html = build_page_with_hero(tsx, texts)
        html = HTML_TPL.format(title=title, header=HEADER, content=content_html)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as oh:
          oh.write(html)
        generated.append(out_path)
  print("Generated files:")
  for g in generated:
    print(g)

if __name__ == "__main__":
  main()
