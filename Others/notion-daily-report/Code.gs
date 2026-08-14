// ============================================================
// Notion Daily Task Report — Google Apps Script
// ============================================================
// Đọc Notion Database → filter tasks → gửi email báo cáo mỗi ngày
// Setup: xem README.md cùng thư mục
// ============================================================

// --- CONFIG ---
const CONFIG = {
  NOTION_API_KEY: PropertiesService.getScriptProperties().getProperty('NOTION_API_KEY'),
  NOTION_DATABASE_ID: PropertiesService.getScriptProperties().getProperty('NOTION_DATABASE_ID'),
  EMAIL_TO: PropertiesService.getScriptProperties().getProperty('EMAIL_TO'), // email nhận báo cáo
  NOTION_API_VERSION: '2022-06-28',

  // Tên property trong Notion DB (chỉnh lại cho khớp DB của bạn)
  PROP_STATUS: 'Status',       // Select hoặc Status type
  PROP_TITLE: 'Name',         // Title type
  PROP_DUE_DATE: 'Due Date',  // Date type
  PROP_PRIORITY: 'Priority',  // Select type (optional)
  PROP_TAGS: 'Tags',          // Multi-select type (optional)

  // Giá trị status (chỉnh cho khớp options trong DB)
  STATUS_DONE: 'Done',
  STATUS_IN_PROGRESS: 'In Progress',
  STATUS_NOT_STARTED: 'Not Started',
};

// --- MAIN FUNCTION (gắn trigger vào hàm này) ---
function sendDailyReport() {
  const today = new Date();
  const todayStr = Utilities.formatDate(today, Session.getScriptTimeZone(), 'yyyy-MM-dd');

  // Lấy tất cả tasks chưa Done
  const incompleteTasks = queryNotionDatabase({
    filter: {
      property: CONFIG.PROP_STATUS,
      status: { does_not_equal: CONFIG.STATUS_DONE }
    },
    sorts: [
      { property: CONFIG.PROP_DUE_DATE, direction: 'ascending' }
    ]
  });

  // Lấy tasks hoàn thành hôm qua (optional — nếu DB có last_edited_time)
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = Utilities.formatDate(yesterday, Session.getScriptTimeZone(), 'yyyy-MM-dd');

  const completedYesterday = queryNotionDatabase({
    filter: {
      and: [
        { property: CONFIG.PROP_STATUS, status: { equals: CONFIG.STATUS_DONE } },
        { timestamp: 'last_edited_time', last_edited_time: { on_or_after: yesterdayStr } }
      ]
    }
  });

  // Phân loại tasks
  const overdue = [];
  const dueToday = [];
  const upcoming = [];
  const noDueDate = [];

  incompleteTasks.forEach(task => {
    const parsed = parseTask(task);
    if (!parsed.dueDate) {
      noDueDate.push(parsed);
    } else if (parsed.dueDate < todayStr) {
      overdue.push(parsed);
    } else if (parsed.dueDate === todayStr) {
      dueToday.push(parsed);
    } else {
      upcoming.push(parsed);
    }
  });

  const completedParsed = completedYesterday.map(parseTask);

  // Sort by priority: Urgent > High > Medium > Low > null
  const priorityOrder = { 'Urgent': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
  const sortByPriority = (a, b) => (priorityOrder[a.priority] ?? 4) - (priorityOrder[b.priority] ?? 4);
  overdue.sort(sortByPriority);
  dueToday.sort(sortByPriority);
  upcoming.sort(sortByPriority);

  // Build email
  const subject = `Daily Task Report - ${todayStr}`;
  const htmlBody = buildEmailHtml({
    date: todayStr,
    overdue,
    dueToday,
    upcoming: upcoming.slice(0, 10), // top 10 sắp tới
    noDueDate,
    completed: completedParsed,
    stats: {
      total: incompleteTasks.length,
      overdue: overdue.length,
      dueToday: dueToday.length,
      completedYesterday: completedParsed.length,
    }
  });

  GmailApp.sendEmail(CONFIG.EMAIL_TO, subject, '', { htmlBody });
  Logger.log(`Report sent to ${CONFIG.EMAIL_TO} at ${new Date().toISOString()}`);
}

// --- NOTION API ---
function queryNotionDatabase(body) {
  const allResults = [];
  let hasMore = true;
  let startCursor = undefined;

  while (hasMore) {
    const payload = { ...body, page_size: 100 };
    if (startCursor) payload.start_cursor = startCursor;

    const response = UrlFetchApp.fetch(
      `https://api.notion.com/v1/databases/${CONFIG.NOTION_DATABASE_ID}/query`,
      {
        method: 'post',
        headers: {
          'Authorization': `Bearer ${CONFIG.NOTION_API_KEY}`,
          'Notion-Version': CONFIG.NOTION_API_VERSION,
          'Content-Type': 'application/json',
        },
        payload: JSON.stringify(payload),
        muteHttpExceptions: true,
      }
    );

    const data = JSON.parse(response.getContentText());

    if (response.getResponseCode() !== 200) {
      Logger.log(`Notion API error: ${JSON.stringify(data)}`);
      throw new Error(`Notion API error: ${data.message || response.getResponseCode()}`);
    }

    allResults.push(...data.results);
    hasMore = data.has_more;
    startCursor = data.next_cursor;
  }

  return allResults;
}

// --- PARSE NOTION PAGE → simple object ---
function parseTask(page) {
  const props = page.properties;

  const titleProp = props[CONFIG.PROP_TITLE];
  const title = titleProp?.title?.[0]?.plain_text || '(Untitled)';

  const statusProp = props[CONFIG.PROP_STATUS];
  const status = statusProp?.status?.name || statusProp?.select?.name || 'Unknown';

  const dateProp = props[CONFIG.PROP_DUE_DATE];
  const dueDate = dateProp?.date?.start || null;

  const priorityProp = props[CONFIG.PROP_PRIORITY];
  const priority = priorityProp?.select?.name || null;

  const tagsProp = props[CONFIG.PROP_TAGS];
  const tags = tagsProp?.multi_select?.map(t => t.name) || [];

  return {
    title,
    status,
    dueDate,
    priority,
    tags,
    url: page.url,
  };
}

// --- BUILD HTML EMAIL ---
function buildEmailHtml({ date, overdue, dueToday, upcoming, noDueDate, completed, stats }) {
  const priorityEmoji = (p) => {
    if (!p) return '';
    const map = {
      'Urgent': '<span style="color:#dc2626;font-weight:bold;">!!</span>',
      'High': '<span style="color:#ea580c;font-weight:bold;">!</span>',
      'Medium': '<span style="color:#ca8a04;">-</span>',
      'Low': '<span style="color:#16a34a;">~</span>'
    };
    return map[p] || `[${p}]`;
  };

  const taskRow = (task) => `
    <tr>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;">
        <a href="${task.url}" style="color:#2563eb;text-decoration:none;">${task.title}</a>
      </td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;">${priorityEmoji(task.priority)} ${task.priority || '-'}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;">${task.dueDate || '-'}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #eee;">${task.tags.join(', ') || '-'}</td>
    </tr>`;

  const taskTable = (tasks, emptyMsg) => {
    if (tasks.length === 0) return `<p style="color:#888;margin:8px 0;">${emptyMsg}</p>`;
    return `
    <table style="width:100%;border-collapse:collapse;font-size:14px;margin:8px 0;">
      <thead>
        <tr style="background:#f8f9fa;">
          <th style="text-align:left;padding:8px 10px;">Task</th>
          <th style="text-align:left;padding:8px 10px;">Priority</th>
          <th style="text-align:left;padding:8px 10px;">Due</th>
          <th style="text-align:left;padding:8px 10px;">Tags</th>
        </tr>
      </thead>
      <tbody>${tasks.map(taskRow).join('')}</tbody>
    </table>`;
  };

  return `
  <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:700px;margin:0 auto;padding:20px;">

    <!-- Stats Summary -->
    <div style="display:flex;gap:12px;margin:0 0 32px 0;flex-wrap:wrap;">
      <div style="background:#fee2e2;padding:12px 16px;border-radius:8px;flex:1;min-width:120px;">
        <div style="font-size:24px;font-weight:bold;color:#dc2626;">${stats.overdue}</div>
        <div style="font-size:12px;color:#991b1b;">Overdue</div>
      </div>
      <div style="background:#fef3c7;padding:12px 16px;border-radius:8px;flex:1;min-width:120px;">
        <div style="font-size:24px;font-weight:bold;color:#d97706;">${stats.dueToday}</div>
        <div style="font-size:12px;color:#92400e;">Due Today</div>
      </div>
      <div style="background:#dbeafe;padding:12px 16px;border-radius:8px;flex:1;min-width:120px;">
        <div style="font-size:24px;font-weight:bold;color:#2563eb;">${stats.total}</div>
        <div style="font-size:12px;color:#1e40af;">Total Open</div>
      </div>
      <div style="background:#d1fae5;padding:12px 16px;border-radius:8px;flex:1;min-width:120px;">
        <div style="font-size:24px;font-weight:bold;color:#059669;">${stats.completedYesterday}</div>
        <div style="font-size:12px;color:#065f46;">Done</div>
      </div>
    </div>

    <!-- Overdue -->
    ${overdue.length > 0 ? `
    <div style="margin-bottom:32px;">
      <h2 style="font-size:16px;color:#dc2626;margin:0 0 12px 0;">OVERDUE (${overdue.length})</h2>
      ${taskTable(overdue.slice(0, 5), '')}
      ${overdue.length > 5 ? `<p style="color:#dc2626;font-size:13px;margin-top:8px;">+ ${overdue.length - 5} more overdue tasks in Notion</p>` : ''}
    </div>
    ` : ''}

    <!-- Due Today -->
    ${dueToday.length > 0 ? `
    <div style="margin-bottom:32px;">
      <h2 style="font-size:16px;color:#d97706;margin:0 0 12px 0;">TODAY (${dueToday.length})</h2>
      ${taskTable(dueToday.slice(0, 5), '')}
      ${dueToday.length > 5 ? `<p style="color:#d97706;font-size:13px;margin-top:8px;">+ ${dueToday.length - 5} more due today in Notion</p>` : ''}
    </div>
    ` : ''}

    <!-- Focus: what to do right now -->
    ${(overdue.length > 0 || dueToday.length > 0) ? '' : `
    <p style="color:#16a34a;font-size:14px;margin:0 0 32px 0;padding:12px;background:#f0fdf4;border-radius:6px;">All clear — no overdue or due-today tasks.</p>
    `}

    <!-- Upcoming -->
    <div style="margin-bottom:32px;">
      <h2 style="font-size:16px;color:#2563eb;margin:0 0 12px 0;">UPCOMING (${upcoming.length})</h2>
      ${taskTable(upcoming.slice(0, 5), 'No upcoming tasks.')}
      ${upcoming.length > 5 ? `<p style="color:#2563eb;font-size:13px;margin-top:8px;">+ ${upcoming.length - 5} more in Notion</p>` : ''}
    </div>

    <!-- No Due Date -->
    ${noDueDate.length > 0 ? `
    <div style="margin-bottom:32px;">
      <h2 style="font-size:16px;color:#6b7280;margin:0 0 12px 0;">NO DEADLINE (${noDueDate.length})</h2>
      ${taskTable(noDueDate.slice(0, 3), '')}
      ${noDueDate.length > 3 ? `<p style="color:#6b7280;font-size:13px;margin-top:8px;">+ ${noDueDate.length - 3} more without deadline</p>` : ''}
    </div>
    ` : ''}

    <!-- Completed -->
    ${completed.length > 0 ? `
    <div style="margin-bottom:32px;">
      <h2 style="font-size:16px;color:#059669;margin:0 0 12px 0;">DONE (${completed.length})</h2>
      ${taskTable(completed.slice(0, 3), '')}
      ${completed.length > 3 ? `<p style="color:#059669;font-size:13px;margin-top:8px;">+ ${completed.length - 3} more completed</p>` : ''}
    </div>
    ` : ''}

    <hr style="margin-top:16px;border:none;border-top:1px solid #eee;">
    <p style="font-size:12px;color:#999;margin-top:12px;">
      Auto-generated by Google Apps Script • Source: Notion Database
    </p>
  </div>`;
}

// --- TEST FUNCTION (chạy thủ công để debug) ---
function testReport() {
  sendDailyReport();
}
