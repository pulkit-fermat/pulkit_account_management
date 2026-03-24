// ============================================
// FERMÀT Account Management Portal - App Logic
// ============================================

let currentBrand = null;
// Use embedded BRAND_DATA (from data.js) - no async fetch needed
let brandData = (typeof BRAND_DATA !== 'undefined') ? BRAND_DATA : {};

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  setupSearch();
  renderBrandList();

  // Select first brand immediately - data is already loaded
  const sorted = getBrandsSorted();
  if (sorted.length > 0) {
    selectBrand(sorted[0].id);
  }
});

// ============================================
// BRAND LIST
// ============================================

function renderBrandList(filter = '') {
  const list = document.getElementById('brandList');
  const sorted = getBrandsSorted();
  const filtered = filter
    ? sorted.filter(b => b.name.toLowerCase().includes(filter.toLowerCase()))
    : sorted;

  list.innerHTML = filtered.map((brand, i) => {
    const avatarClass = `avatar-${(i % 8) + 1}`;
    const initials = getInitials(brand.name);
    const statusClass = getStatusDotClass(brand);
    const isActive = currentBrand && currentBrand.id === brand.id;
    const logoUrl = BRAND_LOGOS[brand.id];

    return `
      <div class="brand-item ${isActive ? 'active' : ''}" onclick="selectBrand('${brand.id}')" data-brand-id="${brand.id}">
        ${logoUrl
          ? `<img src="${logoUrl}" alt="${brand.name}" class="brand-list-logo" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
          : ''}
        <div class="brand-list-logo-fallback ${avatarClass}" ${logoUrl ? 'style="display:none"' : ''}>${initials}</div>
        <div class="brand-item-info">
          <div class="brand-item-name">${brand.name}</div>
          <div class="brand-item-meta">${brand.vertical} &middot; $${(brand.arr / 1000).toFixed(0)}K ARR</div>
        </div>
        <div class="brand-status-dot ${statusClass}"></div>
      </div>
    `;
  }).join('');
}

function getInitials(name) {
  return name.replace(/[^a-zA-Z0-9 ]/g, '').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
}

function getStatusDotClass(brand) {
  if (brand.churn) return 'red';
  if (brand.comments && brand.comments.toLowerCase().includes('churn')) return 'yellow';
  const data = brandData[brand.id];
  if (data && data.health && data.health.score !== undefined) {
    if (data.health.score >= 70) return 'green';
    if (data.health.score >= 40) return 'yellow';
    return 'red';
  }
  return 'gray';
}

function setupSearch() {
  const searchInput = document.getElementById('brandSearch');
  searchInput.addEventListener('input', (e) => {
    renderBrandList(e.target.value);
  });
}

// ============================================
// BRAND SELECTION
// ============================================

function selectBrand(brandId) {
  currentBrand = getBrandById(brandId);
  if (!currentBrand) return;

  renderBrandList(document.getElementById('brandSearch').value);
  updateTopBar();
  renderAllTabs();
}

function renderAllTabs() {
  if (!currentBrand) return;
  const data = brandData[currentBrand.id] || {};
  renderHealthTab(data);
  renderPerformanceTab(data);
  renderCallsTab(data);
  renderCalendarTab(data);
  renderSlackTab(data);
  renderEmailTab(data);
}

function updateTopBar() {
  if (!currentBrand) return;

  const brand = currentBrand;
  const avatarIdx = getBrandsSorted().findIndex(b => b.id === brand.id) % 8 + 1;

  // Brand logo in top bar
  const logoUrl = BRAND_LOGOS[brand.id];
  const logoImg = document.getElementById('brandLogoImg');
  const logoFallback = document.getElementById('brandAvatarFallback');
  if (logoUrl) {
    logoImg.src = logoUrl;
    logoImg.alt = brand.name;
    logoImg.style.display = 'block';
    logoFallback.style.display = 'none';
  } else {
    logoImg.style.display = 'none';
    logoFallback.style.display = 'flex';
    logoFallback.className = `brand-title-avatar-fallback avatar-${avatarIdx}`;
    logoFallback.textContent = getInitials(brand.name);
  }
  document.getElementById('brandName').textContent = brand.name;
  document.getElementById('brandVertical').innerHTML = `${brand.vertical} &middot; ${brand.type.toUpperCase()}`;

  // Badges
  const badges = [];
  if (brand.churn) {
    badges.push(`<span class="badge badge-churn">Churned</span>`);
  } else if (brand.comments && brand.comments.toLowerCase().includes('churn')) {
    badges.push(`<span class="badge badge-warning">At Risk</span>`);
  } else {
    badges.push(`<span class="badge badge-active">Active</span>`);
  }
  badges.push(`<span class="badge badge-arr">$${brand.arr.toLocaleString()} ARR</span>`);
  document.getElementById('brandBadges').innerHTML = badges.join('');

  // Info
  document.getElementById('renewalDate').textContent = brand.renewalDate || 'Not set';

  // Slack channel - show real name and make clickable
  const slackChannelName = getSlackChannelName(brand);
  const slackUrl = brand.slackId ? `https://app.slack.com/client/T/` + brand.slackId : '#';
  document.getElementById('slackChannel').innerHTML = brand.slackId
    ? `<a href="${slackUrl}" target="_blank" style="color: var(--f-forest); text-decoration: none; border-bottom: 1px solid rgba(7,44,27,0.2);">#${slackChannelName}</a>`
    : '--';
}

function getSlackChannelName(brand) {
  // Use real channel name from SLACK_CHANNELS lookup
  if (brand.slackId && SLACK_CHANNELS[brand.slackId]) {
    return SLACK_CHANNELS[brand.slackId];
  }
  // Fallback: generate from brand name
  return 'fermat-x-' + brand.name.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}

// ============================================
// TAB MANAGEMENT
// ============================================

function setupTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const tabId = btn.dataset.tab;
      document.getElementById(`tab-${tabId}`).classList.add('active');

      // Always re-render the clicked tab with fresh data
      if (currentBrand && brandData[currentBrand.id]) {
        const data = brandData[currentBrand.id];
        switch (tabId) {
          case 'health': renderHealthTab(data); break;
          case 'performance': renderPerformanceTab(data); break;
          case 'calls': renderCallsTab(data); break;
          case 'calendar': renderCalendarTab(data); break;
          case 'slack': renderSlackTab(data); break;
          case 'email': renderEmailTab(data); break;
        }
      }
    });
  });
}

function getCurrentTabId() {
  const activeBtn = document.querySelector('.tab-btn.active');
  return activeBtn ? activeBtn.dataset.tab : 'health';
}

function renderCurrentTab() {
  if (!currentBrand) return;
  const tabId = getCurrentTabId();
  const data = brandData[currentBrand.id] || {};

  switch (tabId) {
    case 'health': renderHealthTab(data); break;
    case 'performance': renderPerformanceTab(data); break;
    case 'calls': renderCallsTab(data); break;
    case 'calendar': renderCalendarTab(data); break;
    case 'slack': renderSlackTab(data); break;
    case 'email': renderEmailTab(data); break;
  }
}

// ============================================
// DATA (embedded from data.js - no async fetch)
// ============================================

// Update last refresh timestamp from first brand with data
(function updateRefreshTime() {
  for (const id in brandData) {
    if (brandData[id] && brandData[id].last_updated) {
      const el = document.getElementById('lastRefresh');
      if (el) el.textContent = 'Last refresh: ' + new Date(brandData[id].last_updated).toLocaleString();
      break;
    }
  }
})();

// ============================================
// HEALTH SCORE TAB
// ============================================

function renderHealthTab(data) {
  const container = document.getElementById('healthContent');
  const brand = currentBrand;
  const health = data.health || null;

  let html = '';

  // Brand Info Cards
  html += `<div class="info-grid">
    <div class="info-card">
      <div class="info-card-label">ARR</div>
      <div class="info-card-value">$${brand.arr.toLocaleString()}</div>
      <div class="info-card-sub">${brand.type.toUpperCase()}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Vertical</div>
      <div class="info-card-value">${brand.vertical}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Renewal Date</div>
      <div class="info-card-value">${brand.renewalDate || 'Not set'}</div>
      ${brand.optOutDate ? `<div class="info-card-sub">Opt-out: ${brand.optOutDate}</div>` : ''}
    </div>
    <div class="info-card">
      <div class="info-card-label">Growth Manager</div>
      <div class="info-card-value">${brand.gm}</div>
      ${brand.olderGm ? `<div class="info-card-sub">Prev: ${brand.olderGm}</div>` : ''}
    </div>
    <div class="info-card">
      <div class="info-card-label">Active Users (L7D)</div>
      <div class="info-card-value">${brand.users.filter(u => u.activeL7D).length} / ${brand.users.length}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Active Users (L30D)</div>
      <div class="info-card-value">${brand.users.filter(u => u.activeL30D).length} / ${brand.users.length}</div>
    </div>
  </div>`;

  // Comments/Warnings
  if (brand.comments) {
    html += `<div class="warning-card">
      <div class="warning-title">&#9888; Account Note</div>
      <p>${brand.comments}</p>
    </div>`;
  }

  if (brand.churn) {
    html += `<div class="warning-card">
      <div class="warning-title">&#10060; Churned</div>
      <p>Churn Date: ${brand.churnDate || 'Unknown'}</p>
      ${brand.churnReason ? `<p style="margin-top:4px">Reason: ${brand.churnReason}</p>` : ''}
    </div>`;
  }

  // Health Score Section
  if (health && health.score !== undefined) {
    const scoreColor = health.score >= 70 ? '#1a8a3e' : health.score >= 40 ? '#92700c' : 'var(--f-red)';
    const scoreStatus = health.score >= 70 ? 'Healthy' : health.score >= 40 ? 'Needs Attention' : 'Critical';
    const statusBg = health.score >= 70 ? 'rgba(62,214,96,0.1)' : health.score >= 40 ? 'rgba(184,146,64,0.08)' : 'rgba(200,70,50,0.08)';
    const circumference = 2 * Math.PI * 75;
    const offset = circumference - (health.score / 100) * circumference;

    html += `<div class="health-overview">
      <div class="card health-score-circle">
        <div class="score-ring">
          <svg width="180" height="180" viewBox="0 0 180 180">
            <circle class="score-ring-bg" cx="90" cy="90" r="75"/>
            <circle class="score-ring-fill" cx="90" cy="90" r="75"
              stroke="${scoreColor}"
              stroke-dasharray="${circumference}"
              stroke-dashoffset="${offset}"/>
          </svg>
          <div class="score-value">
            <div class="score-number" style="color: ${scoreColor}">${health.score}</div>
            <div class="score-label">Health Score</div>
          </div>
        </div>
        <div class="score-status" style="background: ${statusBg}; color: ${scoreColor}">${scoreStatus}</div>
      </div>

      <div class="health-breakdown">
        ${renderHealthFactor('Platform Activity', health.breakdown?.platform_activity, '&#128187;', 'rgba(7,44,27,0.06)', 'var(--f-forest)', health.breakdown?.platform_detail)}
        ${renderHealthFactor('Communication', health.breakdown?.communication, '&#128172;', 'rgba(62,214,96,0.08)', '#1a8a3e', health.breakdown?.communication_detail)}
        ${renderHealthFactor('Performance Metrics', health.breakdown?.performance, '&#128200;', 'rgba(37,99,235,0.08)', 'var(--f-blue)', health.breakdown?.performance_detail)}
        ${renderHealthFactor('Engagement Trend', health.breakdown?.engagement, '&#128640;', 'rgba(184,146,64,0.08)', 'var(--f-gold)', health.breakdown?.engagement_detail)}
        ${renderHealthFactor('Call Frequency', health.breakdown?.call_frequency, '&#9742;', 'rgba(200,168,154,0.12)', 'var(--f-blush)', health.breakdown?.call_detail)}
      </div>
    </div>`;

    // Health Signals
    if (health.signals && health.signals.length > 0) {
      html += `<div class="sh" style="margin-top:32px"><h2>Health Signals</h2></div>`;
      html += `<div class="health-signals">`;
      health.signals.forEach(signal => {
        const icon = signal.type === 'positive' ? '&#10003;' : signal.type === 'negative' ? '&#10007;' : '&#9888;';
        html += `
          <div class="signal-card ${signal.type}">
            <div class="signal-icon">${icon}</div>
            <div>
              <div class="signal-text">${signal.text}</div>
              ${signal.time ? `<div class="signal-time">${signal.time}</div>` : ''}
            </div>
          </div>`;
      });
      html += `</div>`;
    }
  } else {
    html += `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#9829;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">No Health Data Available</div>
      <p>Run the <code>/account-dashboard</code> skill in Claude Code to populate health scores from all data sources.</p>
      <div class="hint">The skill aggregates data from FERMÀT metrics, Glyphic calls, Granola meetings, Slack, Gmail, and PostHog.</div>
    </div>`;
  }

  // Users Table
  if (brand.users.length > 0) {
    html += `<div class="section-divider"></div>`;
    html += `<div class="sh"><h2>Platform Users</h2></div>`;
    html += `<div class="card" style="padding: 0; overflow: hidden;">
      <table class="user-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Timezone</th>
            <th>L7D</th>
            <th>L30D</th>
            <th>Last Active</th>
          </tr>
        </thead>
        <tbody>
          ${brand.users.map(u => `
            <tr>
              <td style="color: var(--f-black); font-weight: 500;">${u.email}</td>
              <td style="color: #3a3a3a; font-size: 12px;">${u.timezone || '--'}</td>
              <td><span class="activity-badge ${u.activeL7D ? 'active' : 'inactive'}">${u.activeL7D ? 'Active' : 'No'}</span></td>
              <td><span class="activity-badge ${u.activeL30D ? 'active' : 'inactive'}">${u.activeL30D ? 'Active' : 'No'}</span></td>
              <td style="color: #3a3a3a; font-size: 12px;">${u.lastActive || '--'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>`;
  }

  container.innerHTML = html;
}

function renderHealthFactor(name, score, icon, iconBg, iconColor, detail) {
  if (score === undefined || score === null) return '';
  const barColor = score >= 70 ? '#1a8a3e' : score >= 40 ? '#92700c' : 'var(--f-red)';
  const scoreColor = score >= 70 ? '#1a8a3e' : score >= 40 ? '#92700c' : 'var(--f-red)';

  return `
    <div class="health-factor">
      <div class="health-factor-icon" style="background: ${iconBg}; color: ${iconColor}">${icon}</div>
      <div class="health-factor-info">
        <div class="health-factor-name">${name}</div>
        <div class="health-factor-detail">${detail || ''}</div>
      </div>
      <div class="health-factor-score" style="color: ${scoreColor}">${score}</div>
      <div class="health-factor-bar">
        <div class="health-factor-bar-fill" style="width: ${score}%; background: ${barColor}"></div>
      </div>
    </div>`;
}

// ============================================
// PERFORMANCE TAB
// ============================================

let currentPeriod = '7d';

function renderPerformanceTab(data) {
  const container = document.getElementById('performanceContent');
  if (!data || !data.performance) {
    // No data at all - show empty state
    container.innerHTML = `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#9651;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">Loading performance data...</div>
      <p>If this persists, run <code>/account-dashboard</code> to refresh.</p>
    </div>`;
    return;
  }

  const perf = data.performance;
  let html = '';

  // Period Selector - always show
  html += `<div class="period-selector">
    ${['yesterday', '3d', '7d', '15d', '30d', '45d'].map(p => `
      <button class="period-btn ${p === currentPeriod ? 'active' : ''}" onclick="switchPeriod('${p}')">${p === 'yesterday' ? 'Yesterday' : p}</button>
    `).join('')}
  </div>`;

  // Get current period data - default to empty object if not found
  const pd = perf[currentPeriod] || {};
  const prevPeriod = getPreviousPeriodKey(currentPeriod);
  const prev = perf[prevPeriod] || {};

  html += `<div class="metrics-grid">
      ${renderMetricCard('Ad Spend', pd.ad_spend, prev.ad_spend, 'spend', '$')}
      ${renderMetricCard('Revenue', pd.revenue, prev.revenue, 'revenue', '$')}
      ${renderMetricCard('CVR', pd.cvr, prev.cvr, 'cvr', '', '%')}
      ${renderMetricCard('Sessions', pd.sessions, prev.sessions, 'sessions')}
      ${renderMetricCard('ROAS', pd.roas, prev.roas, 'roas', '', 'x')}
      ${renderMetricCard('CPA', pd.cpa, prev.cpa, 'cpa', '$')}
    </div>`;

    // Funnel breakdown if available
    if (pd.funnels && pd.funnels.length > 0) {
      html += `<div class="sh" style="margin-top:32px"><h2>Funnel Breakdown</h2></div>`;
      html += `<div class="funnel-grid">`;
      pd.funnels.forEach(f => {
        html += `
          <div class="funnel-card">
            <div class="funnel-name">${f.name}</div>
            <div class="funnel-type">${f.type || 'Funnel'}</div>
            <div class="funnel-stats">
              <div>
                <div class="funnel-stat-label">Spend</div>
                <div class="funnel-stat-value">${formatCurrency(f.spend)}</div>
              </div>
              <div>
                <div class="funnel-stat-label">Revenue</div>
                <div class="funnel-stat-value">${formatCurrency(f.revenue)}</div>
              </div>
              <div>
                <div class="funnel-stat-label">CVR</div>
                <div class="funnel-stat-value">${f.cvr ? f.cvr.toFixed(2) + '%' : '--'}</div>
              </div>
            </div>
          </div>`;
      });
      html += `</div>`;
    }

    // Period comparison table
    html += `<div class="section-divider"></div>`;
    html += `<div class="sh"><h2>All Periods Comparison</h2></div>`;
    html += `<div class="card" style="padding: 0; overflow: hidden;">
      <div class="perf-table-wrap">
        <table class="perf-table">
          <thead>
            <tr>
              <th>Period</th>
              <th>Ad Spend</th>
              <th>Revenue</th>
              <th>CVR</th>
              <th>Sessions</th>
              <th>ROAS</th>
              <th>CPA</th>
            </tr>
          </thead>
          <tbody>
            ${['yesterday', '3d', '7d', '15d', '30d', '45d'].map(p => {
              const d = perf[p] || {};
              const isActive = p === currentPeriod;
              return `<tr style="${isActive ? 'background: rgba(7,44,27,0.04);' : ''}">
                <td style="font-weight: 600;">${p === 'yesterday' ? 'Yesterday' : p}</td>
                <td class="number">${formatCurrency(d.ad_spend)}</td>
                <td class="number">${formatCurrency(d.revenue)}</td>
                <td class="number">${d.cvr !== undefined ? d.cvr.toFixed(2) + '%' : '--'}</td>
                <td class="number">${d.sessions !== undefined ? d.sessions.toLocaleString() : '--'}</td>
                <td class="number">${d.roas !== undefined ? d.roas.toFixed(2) + 'x' : '--'}</td>
                <td class="number">${formatCurrency(d.cpa)}</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>`;

  container.innerHTML = html;
}

function switchPeriod(period) {
  currentPeriod = period;
  if (currentBrand) {
    const data = brandData[currentBrand.id] || {};
    renderPerformanceTab(data);
  }
}

function renderMetricCard(label, value, prevValue, type, prefix = '', suffix = '') {
  const formatted = value !== undefined && value !== null
    ? `${prefix}${typeof value === 'number' ? (prefix === '$' ? value.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}) : suffix === '%' ? value.toFixed(2) : suffix === 'x' ? value.toFixed(2) : value.toLocaleString()) : value}${suffix}`
    : '--';

  let changeHtml = '';
  if (value !== undefined && prevValue !== undefined && prevValue !== null && prevValue !== 0) {
    const pctChange = ((value - prevValue) / Math.abs(prevValue)) * 100;
    const changeClass = type === 'cpa' ? (pctChange < 0 ? 'up' : pctChange > 0 ? 'down' : 'neutral') : (pctChange > 0 ? 'up' : pctChange < 0 ? 'down' : 'neutral');
    const arrow = pctChange > 0 ? '&#9650;' : pctChange < 0 ? '&#9660;' : '&#8212;';
    changeHtml = `<div class="metric-change ${changeClass}">${arrow} ${Math.abs(pctChange).toFixed(1)}%</div>`;
  }

  return `
    <div class="metric-card ${type}">
      <div class="metric-label">${label}</div>
      <div class="metric-value">${formatted}</div>
      ${changeHtml}
    </div>`;
}

function getPreviousPeriodKey(period) {
  const map = { 'yesterday': 'yesterday', '3d': 'yesterday', '7d': '3d', '15d': '7d', '30d': '15d', '45d': '30d' };
  return map[period] || 'yesterday';
}

// ============================================
// CALLS TAB
// ============================================

function renderCallsTab(data) {
  const container = document.getElementById('callsContent');
  const calls = data.calls || null;

  let html = '';

  if (calls && calls.analysis) {
    html += `<div class="analysis-box">
      <div class="analysis-title">&#128161; Call Analysis</div>
      <div class="analysis-text">${calls.analysis}</div>
    </div>`;
  }

  if (calls && calls.recent && calls.recent.length > 0) {
    html += `<div class="sh"><h2>Recent Calls</h2></div>`;
    html += `<div class="call-list">`;

    calls.recent.forEach(call => {
      const date = new Date(call.date);
      const day = date.getDate();
      const month = date.toLocaleString('en', { month: 'short' });

      html += `
        <div class="call-card">
          <div class="call-date-badge">
            <div class="call-date-day">${day}</div>
            <div class="call-date-month">${month}</div>
          </div>
          <div class="call-info">
            <div class="call-title">${call.title || 'Brand Call'}</div>
            <div class="call-meta">
              <span class="call-meta-item">&#128337; ${call.duration || '--'}</span>
              <span class="call-meta-item">&#128101; ${call.participants || '--'}</span>
              ${call.source ? `<span class="call-meta-item" style="color: var(--f-forest);">${call.source}</span>` : ''}
            </div>
            ${call.summary ? `<div class="call-summary">${call.summary}</div>` : ''}
            <div class="call-actions">
              ${call.recording_url ? `<a href="${call.recording_url}" target="_blank" class="call-action-btn">&#9654; Recording</a>` : ''}
              ${call.snippets && call.snippets.length > 0 ? `<button class="call-action-btn" onclick="toggleSnippets(this)">&#128196; Snippets (${call.snippets.length})</button>` : ''}
            </div>
            ${call.snippets && call.snippets.length > 0 ? `
              <div class="call-snippets" style="display: none; margin-top: 12px;">
                ${call.snippets.map(s => `
                  <div style="padding: 10px; background: var(--f-white); border-radius: 6px; margin-bottom: 6px; font-size: 12px; color: #3a3a3a; line-height: 1.5;">
                    ${s.text || s}
                  </div>
                `).join('')}
              </div>
            ` : ''}
            ${call.action_items && call.action_items.length > 0 ? `
              <div style="margin-top: 10px;">
                <div style="font-size: 12px; font-weight: 600; color: var(--f-forest); margin-bottom: 6px;">Action Items:</div>
                ${call.action_items.map(a => `
                  <div style="font-size: 12px; color: #3a3a3a; padding: 4px 0; display: flex; gap: 6px;">
                    <span style="color: var(--f-forest);">&#8226;</span> ${a}
                  </div>
                `).join('')}
              </div>
            ` : ''}
          </div>
        </div>`;
    });

    html += `</div>`;
  } else {
    html += `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#9742;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">No Call Data Available</div>
      <p>Run <code>/account-dashboard</code> to pull call data from Glyphic and Granola.</p>
      <div class="hint">Includes call recordings, transcripts, action items, and AI analysis.</div>
    </div>`;
  }

  container.innerHTML = html;
}

function toggleSnippets(btn) {
  const snippets = btn.closest('.call-info').querySelector('.call-snippets');
  if (snippets) {
    snippets.style.display = snippets.style.display === 'none' ? 'block' : 'none';
  }
}

// ============================================
// CALENDAR TAB
// ============================================

function renderCalendarTab(data) {
  const container = document.getElementById('calendarContent');
  const calendar = data.calendar || null;

  let html = '';

  if (calendar) {
    // Upcoming Events
    if (calendar.upcoming && calendar.upcoming.length > 0) {
      html += `<div class="calendar-section">
        <div class="calendar-section-title">&#128994; Upcoming Calls</div>
        ${calendar.upcoming.map(evt => `
          <div class="calendar-event upcoming">
            <div class="calendar-event-time">${formatEventDate(evt.start)}<br>${formatEventTime(evt.start)} - ${formatEventTime(evt.end)}</div>
            <div class="calendar-event-title">${evt.title}</div>
            <div class="calendar-event-attendees">${evt.attendees ? evt.attendees.join(', ') : ''}</div>
          </div>
        `).join('')}
      </div>`;
    } else {
      html += `<div class="calendar-section">
        <div class="calendar-section-title">&#128994; Upcoming Calls</div>
        <div style="padding: 20px; color: var(--f-mid); font-size: 13px; background: var(--f-bg); border-radius: 8px;">No upcoming calls scheduled</div>
      </div>`;
    }

    // Past Events
    if (calendar.past && calendar.past.length > 0) {
      html += `<div class="calendar-section">
        <div class="calendar-section-title">&#9899; Recent Past Calls</div>
        ${calendar.past.map(evt => `
          <div class="calendar-event past">
            <div class="calendar-event-time">${formatEventDate(evt.start)}<br>${formatEventTime(evt.start)} - ${formatEventTime(evt.end)}</div>
            <div class="calendar-event-title">${evt.title}</div>
            <div class="calendar-event-attendees">${evt.attendees ? evt.attendees.join(', ') : ''}</div>
          </div>
        `).join('')}
      </div>`;
    }
  } else {
    html += `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#128197;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">No Calendar Data Available</div>
      <p>Run <code>/account-dashboard</code> to pull calendar events from Google Calendar.</p>
      <div class="hint">Shows previous 3 calls and next 4-5 upcoming calls for this brand.</div>
    </div>`;
  }

  container.innerHTML = html;
}

// ============================================
// SLACK TAB
// ============================================

function renderSlackTab(data) {
  const container = document.getElementById('slackContent');
  const slack = data.slack || null;

  let html = '';

  if (slack && slack.analysis) {
    html += `<div class="analysis-box">
      <div class="analysis-title">&#128172; Communication Analysis</div>
      <div class="analysis-text">${slack.analysis}</div>
    </div>`;
  }

  if (slack && slack.messages && slack.messages.length > 0) {
    html += `<div class="sh"><h2>Recent Slack Messages</h2></div>`;
    html += `<div class="message-list">`;

    slack.messages.forEach((msg, i) => {
      const avatarClass = `avatar-${(i % 8) + 1}`;
      const initials = msg.user ? msg.user.substring(0, 2).toUpperCase() : '??';

      html += `
        <div class="message-card">
          <div class="message-avatar ${avatarClass}">${initials}</div>
          <div class="message-content">
            <div class="message-header">
              <span class="message-sender">${msg.user || 'Unknown'}</span>
              <span class="message-channel">${msg.channel || ''}</span>
              <span class="message-time">${msg.timestamp ? formatDateTime(msg.timestamp) : ''}</span>
            </div>
            <div class="message-text">${msg.text || ''}</div>
          </div>
        </div>`;
    });

    html += `</div>`;
  } else {
    html += `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#128172;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">No Slack Data Available</div>
      <p>Run <code>/account-dashboard</code> to pull recent Slack messages from the brand channel.</p>
      <div class="hint">Slack channel: #${getSlackChannelName(currentBrand)} (${currentBrand.slackId || 'Not configured'})</div>
    </div>`;
  }

  container.innerHTML = html;
}

// ============================================
// EMAIL TAB
// ============================================

function renderEmailTab(data) {
  const container = document.getElementById('emailContent');
  const email = data.email || null;

  let html = '';

  if (email && email.analysis) {
    html += `<div class="analysis-box">
      <div class="analysis-title">&#9993; Email Communication Analysis</div>
      <div class="analysis-text">${email.analysis}</div>
    </div>`;
  }

  if (email && email.messages && email.messages.length > 0) {
    html += `<div class="sh"><h2>Recent Emails</h2></div>`;
    html += `<div class="message-list">`;

    email.messages.forEach((msg, i) => {
      const avatarClass = `avatar-${(i % 8) + 1}`;
      const initials = msg.from ? msg.from.substring(0, 2).toUpperCase() : '??';

      html += `
        <div class="message-card">
          <div class="message-avatar ${avatarClass}">${initials}</div>
          <div class="message-content">
            <div class="message-header">
              <span class="message-sender">${msg.from || 'Unknown'}</span>
              <span class="message-time">${msg.date ? formatDateTime(msg.date) : ''}</span>
            </div>
            ${msg.subject ? `<div class="message-subject">${msg.subject}</div>` : ''}
            <div class="message-text">${msg.snippet || msg.body || ''}</div>
          </div>
        </div>`;
    });

    html += `</div>`;
  } else {
    html += `<div class="no-data-msg">
      <div style="font-size: 36px; opacity: 0.3; margin-bottom: 12px;">&#9993;</div>
      <div style="font-size: 15px; font-weight: 600; color: #3a3a3a;">No Email Data Available</div>
      <p>Run <code>/account-dashboard</code> to pull recent emails from Gmail.</p>
      <div class="hint">Searches for emails to/from brand contacts listed in the users table.</div>
    </div>`;
  }

  container.innerHTML = html;
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatCurrency(value) {
  if (value === undefined || value === null) return '--';
  return '$' + value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

function formatDateTime(dateStr) {
  if (!dateStr) return '--';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) +
      ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  } catch {
    return dateStr;
  }
}

function formatEventDate(dateStr) {
  if (!dateStr) return '--';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  } catch {
    return dateStr;
  }
}

function formatEventTime(dateStr) {
  if (!dateStr) return '--';
  try {
    const d = new Date(dateStr);
    return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  } catch {
    return dateStr;
  }
}

function openDashboardInTerminal() {
  alert('Run this in Claude Code terminal:\\n\\n/account-dashboard\\n\\nThis will pull fresh data from all MCPs and update the dashboard.');
}
