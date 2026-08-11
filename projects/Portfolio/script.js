/* ==========================================================================
   Nayab Gull — Portfolio script
   Vanilla JS. No dependencies.
   ========================================================================== */

const PREFERS_REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const IS_COARSE_POINTER = window.matchMedia('(pointer: coarse)').matches;

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initTypingHero();
  initScrollReveal();
  initStatsCounters();
  initSkills();
  loadProjects();
  initNetworkCanvas();
  initCursorGlow();
  initTilt();
  initMagneticButtons();
  initHeroParallax();
});

/* ---------------------------------------------------------------------- */
/* Mobile nav toggle                                                       */
/* ---------------------------------------------------------------------- */

function initNav() {
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Hero typing animation — like a Jupyter cell executing                   */
/* ---------------------------------------------------------------------- */

function initTypingHero() {
  const nameEl = document.getElementById('typedName');
  const roleEl = document.getElementById('heroRole');
  if (!nameEl || !roleEl) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const name = 'Nayab Gull';
  const role = "AI/ML Developer · App Developer";

  if (prefersReducedMotion) {
    nameEl.textContent = name;
    roleEl.textContent = role;
    return;
  }

  let i = 0;
  function typeName() {
    if (i <= name.length) {
      nameEl.textContent = name.slice(0, i);
      i++;
      setTimeout(typeName, 65);
    } else {
      setTimeout(typeRole, 250);
    }
  }

  let j = 0;
  function typeRole() {
    if (j <= role.length) {
      roleEl.textContent = role.slice(0, j);
      j++;
      setTimeout(typeRole, 32);
    }
  }

  setTimeout(typeName, 400);
}

/* ---------------------------------------------------------------------- */
/* Scroll reveal — fade/slide-in for .reveal elements                      */
/* ---------------------------------------------------------------------- */

function initScrollReveal() {
  const items = document.querySelectorAll('.reveal:not([data-reveal-bound])');
  if (!items.length) return;

  if (PREFERS_REDUCED_MOTION) {
    items.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const grid = entry.target.parentElement;
        const siblings = grid ? Array.from(grid.children).filter(c => c.classList.contains('reveal')) : [];
        const idx = siblings.indexOf(entry.target);
        const delay = idx > 0 ? Math.min(idx * 70, 350) : 0;
        entry.target.style.transitionDelay = delay + 'ms';
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  items.forEach(el => {
    el.setAttribute('data-reveal-bound', '1');
    observer.observe(el);
  });
}

/* ---------------------------------------------------------------------- */
/* Stats counter animation (12+ Projects, 2 Internships, 1 Hackathon)      */
/* ---------------------------------------------------------------------- */

function initStatsCounters() {
  const statsRow = document.getElementById('statsRow');
  if (!statsRow) return;

  const numbers = statsRow.querySelectorAll('.stat-number');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const animate = () => {
    numbers.forEach(el => {
      const target = parseInt(el.dataset.target, 10) || 0;
      const suffix = el.dataset.suffix || '';

      if (prefersReducedMotion) {
        el.textContent = target + suffix;
        return;
      }

      const duration = 900;
      const start = performance.now();

      function step(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = Math.round(eased * target);
        el.textContent = value + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animate();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  observer.observe(statsRow);
}

/* ---------------------------------------------------------------------- */
/* Skills — grouped by category                                            */
/* ---------------------------------------------------------------------- */

function initSkills() {
  const grid = document.getElementById('skillsGrid');
  if (!grid) return;

  const skillGroups = [
    {
      title: 'ML / Data Science',
      items: ['Python', 'Pandas', 'NumPy', 'Scikit-learn', 'SHAP', 'Matplotlib', 'Seaborn', 'EDA', 'Feature Engineering', 'GridSearchCV']
    },
    {
      title: 'AI Integration',
      items: ['LLM APIs (Gemini)', 'Prompt Engineering', 'Anomaly Detection', 'AI-powered Automation']
    },
    {
      title: 'App Development',
      items: ['Flutter', 'Kotlin', 'Firebase (Auth, Firestore)', 'SQLite', 'Provider', 'Google Maps / OSM', 'GPS & Location']
    },
    {
      title: 'Web & Deployment',
      items: ['HTML/CSS/JS', 'Vercel', 'Render', 'Netlify']
    },
    {
      title: 'Tools',
      items: ['Git', 'GitHub', 'Jupyter / Kaggle', 'PyCharm', 'Streamlit', 'Tkinter', 'Google Colab']
    }
  ];

  const frag = document.createDocumentFragment();

  skillGroups.forEach(group => {
    const card = document.createElement('div');
    card.className = 'skill-card reveal';

    const title = document.createElement('p');
    title.className = 'skill-card-title';
    title.textContent = group.title;
    card.appendChild(title);

    const list = document.createElement('ul');
    list.className = 'skill-tags';
    group.items.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      list.appendChild(li);
    });
    card.appendChild(list);

    frag.appendChild(card);
  });

  grid.appendChild(frag);

  // newly-injected .reveal elements need observing
  initScrollReveal();
}

/* ---------------------------------------------------------------------- */
/* Projects — loaded dynamically from projects.json                        */
/* ---------------------------------------------------------------------- */

async function loadProjects() {
  const aiContainer = document.getElementById('aiProjects');
  const appContainer = document.getElementById('appProjects');
  if (!aiContainer || !appContainer) return;

  try {
    const res = await fetch('projects.json');
    if (!res.ok) throw new Error('Failed to load projects.json');
    const projects = await res.json();

    const aiProjects = projects.filter(p => p.category === 'ai-ml');
    const appProjects = projects.filter(p => p.category === 'app-dev');

    renderProjectCards(aiContainer, aiProjects);
    renderProjectCards(appContainer, appProjects);
  } catch (err) {
    console.error(err);
    const errorMsg = '<p style="color: var(--text-dim); font-family: var(--font-mono); font-size: 13px;">Could not load projects.json — make sure it sits alongside index.html.</p>';
    aiContainer.innerHTML = errorMsg;
    appContainer.innerHTML = '';
  }

  // re-run reveal observer for freshly injected cards
  initScrollReveal();
}

function renderProjectCards(container, projects) {
  const frag = document.createDocumentFragment();

  projects.forEach((project, index) => {
    const card = document.createElement('article');
    card.className = 'project-card reveal';

    const chrome = document.createElement('div');
    chrome.className = 'cell-chrome';
    chrome.innerHTML = `
      <div class="cell-dots"><span></span><span></span><span></span></div>
      <span class="cell-path">In [${index + 1}]:</span>
    `;
    card.appendChild(chrome);

    const body = document.createElement('div');
    body.className = 'project-card-body';

    const title = document.createElement('h4');
    title.className = 'project-title';
    title.textContent = project.title;
    body.appendChild(title);

    const desc = document.createElement('p');
    desc.className = 'project-desc';
    desc.textContent = project.description;
    body.appendChild(desc);

    if (Array.isArray(project.tags) && project.tags.length) {
      const tagList = document.createElement('ul');
      tagList.className = 'project-tags';
      project.tags.forEach(tag => {
        const li = document.createElement('li');
        li.textContent = tag;
        tagList.appendChild(li);
      });
      body.appendChild(tagList);
    }

    const links = document.createElement('div');
    links.className = 'project-links';

    if (project.demo && project.demo.trim() !== '') {
      const demoLink = document.createElement('a');
      demoLink.href = project.demo;
      demoLink.target = '_blank';
      demoLink.rel = 'noopener noreferrer';
      demoLink.className = 'project-link demo-link';
      demoLink.innerHTML = '<span>▸</span> Live Demo';
      links.appendChild(demoLink);
    }

    if (project.github && project.github.trim() !== '') {
      const githubLink = document.createElement('a');
      githubLink.href = project.github;
      githubLink.target = '_blank';
      githubLink.rel = 'noopener noreferrer';
      githubLink.className = 'project-link';
      githubLink.innerHTML = '<span>⌥</span> GitHub';
      links.appendChild(githubLink);
    }

    if (links.children.length) {
      body.appendChild(links);
    }

    card.appendChild(body);
    frag.appendChild(card);
  });

  container.appendChild(frag);
}

/* ---------------------------------------------------------------------- */
/* AI network canvas — faint connected dots/lines, low opacity             */
/* ---------------------------------------------------------------------- */

function initNetworkCanvas() {
  const canvas = document.getElementById('networkCanvas');
  if (!canvas) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const ctx = canvas.getContext('2d');
  let width, height, dpr;
  let nodes = [];
  let animId = null;

  const NODE_COUNT_DENSITY = 9000; // px^2 per node — kept sparse/subtle
  const MAX_LINK_DIST = 130;
  const TEAL = '94, 234, 212';

  function resize() {
    const section = canvas.parentElement;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = section.offsetWidth;
    height = section.offsetHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const count = Math.max(14, Math.min(46, Math.floor((width * height) / NODE_COUNT_DENSITY)));
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      r: 1 + Math.random() * 1.4
    }));
  }

  function step() {
    ctx.clearRect(0, 0, width, height);

    nodes.forEach(n => {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > width) n.vx *= -1;
      if (n.y < 0 || n.y > height) n.vy *= -1;
    });

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MAX_LINK_DIST) {
          const opacity = (1 - dist / MAX_LINK_DIST) * 0.28;
          ctx.strokeStyle = `rgba(${TEAL}, ${opacity})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    nodes.forEach(n => {
      ctx.fillStyle = `rgba(${TEAL}, 0.45)`;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();
    });

    animId = requestAnimationFrame(step);
  }

  resize();

  if (prefersReducedMotion) {
    // draw a single static frame, no animation loop
    step();
    cancelAnimationFrame(animId);
  } else {
    step();
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (animId) cancelAnimationFrame(animId);
      resize();
      if (!prefersReducedMotion) step();
    }, 200);
  });
}

/* ---------------------------------------------------------------------- */
/* Cursor-reactive glow — notebook cells, project cards, skill cards       */
/* Uses event delegation so it works on cards injected after page load.    */
/* ---------------------------------------------------------------------- */

function initCursorGlow() {
  if (PREFERS_REDUCED_MOTION || IS_COARSE_POINTER) return;

  const GLOW_SELECTOR = '.notebook-cell, .project-card, .skill-card';

  document.addEventListener('pointermove', (e) => {
    const target = e.target.closest(GLOW_SELECTOR);
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    target.style.setProperty('--mx', x + '%');
    target.style.setProperty('--my', y + '%');
  }, { passive: true });
}

/* ---------------------------------------------------------------------- */
/* 3D tilt on project cards                                                */
/* ---------------------------------------------------------------------- */

function initTilt() {
  if (PREFERS_REDUCED_MOTION || IS_COARSE_POINTER) return;

  const MAX_TILT = 6; // degrees, kept subtle for a premium (not gimmicky) feel

  document.addEventListener('pointermove', (e) => {
    const card = e.target.closest('.project-card');
    if (!card) return;
    const rect = card.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    const rotateY = px * MAX_TILT * 2;
    const rotateX = -py * MAX_TILT * 2;
    card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
  }, { passive: true });

  document.addEventListener('pointerout', (e) => {
    const card = e.target.closest('.project-card');
    if (!card) return;
    // only reset if we're actually leaving the card, not moving to a child
    if (card.contains(e.relatedTarget)) return;
    card.style.transform = '';
  }, { passive: true });
}

/* ---------------------------------------------------------------------- */
/* Magnetic buttons — CTA buttons drift slightly toward the cursor         */
/* ---------------------------------------------------------------------- */

function initMagneticButtons() {
  if (PREFERS_REDUCED_MOTION || IS_COARSE_POINTER) return;

  const STRENGTH = 0.28;
  const buttons = document.querySelectorAll('.btn, .contact-link, .project-link');

  buttons.forEach(btn => {
    btn.addEventListener('pointermove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = (e.clientX - rect.left - rect.width / 2) * STRENGTH;
      const y = (e.clientY - rect.top - rect.height / 2) * STRENGTH;
      btn.style.transform = `translate(${x}px, ${y}px)`;
    }, { passive: true });

    btn.addEventListener('pointerleave', () => {
      btn.style.transform = '';
    }, { passive: true });
  });
}

/* ---------------------------------------------------------------------- */
/* Hero cell parallax — very subtle tilt following pointer across viewport */
/* ---------------------------------------------------------------------- */

function initHeroParallax() {
  if (PREFERS_REDUCED_MOTION || IS_COARSE_POINTER) return;

  const heroCell = document.querySelector('.hero-cell');
  const hero = document.getElementById('hero');
  if (!heroCell || !hero) return;

  const MAX_TILT = 2.5;

  hero.addEventListener('pointermove', (e) => {
    const rect = hero.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    heroCell.style.transform = `perspective(1400px) rotateX(${(-py * MAX_TILT).toFixed(2)}deg) rotateY(${(px * MAX_TILT).toFixed(2)}deg)`;
  }, { passive: true });

  hero.addEventListener('pointerleave', () => {
    heroCell.style.transform = '';
  }, { passive: true });
}