const SPREADSHEET_ID = 'PUT_YOUR_SPREADSHEET_ID_HERE';
const SHEET_NAME = 'course_feedback';
const HEADERS = [
  'submitted_at',
  'course_slug',
  'course_name',
  'content_rating',
  'instructor_rating',
  'strengths',
  'improvements',
  'source_page',
  'user_agent'
];

function doGet() {
  return jsonOutput_({
    ok: true,
    service: 'dz-academy-course-feedback',
    status: 'ready'
  });
}

function doPost(e) {
  try {
    const payload = parsePayload_(e);
    validatePayload_(payload);

    const sheet = getSheet_();
    ensureHeaders_(sheet);

    sheet.appendRow([
      new Date(),
      payload.course_slug,
      payload.course_name,
      Number(payload.content_rating),
      Number(payload.instructor_rating),
      payload.strengths,
      payload.improvements,
      payload.source_page || '',
      payload.user_agent || ''
    ]);

    return jsonOutput_({
      ok: true,
      message: 'Feedback saved.'
    });
  } catch (error) {
    return jsonOutput_({
      ok: false,
      error: error.message
    });
  }
}

function parsePayload_(e) {
  const raw = e && e.postData && e.postData.contents ? e.postData.contents : '';
  if (raw) {
    return normalizePayload_(JSON.parse(raw));
  }

  return normalizePayload_(e.parameter || {});
}

function normalizePayload_(payload) {
  return {
    course_slug: stringValue_(payload.course_slug),
    course_name: stringValue_(payload.course_name),
    content_rating: stringValue_(payload.content_rating),
    instructor_rating: stringValue_(payload.instructor_rating),
    strengths: stringValue_(payload.strengths),
    improvements: stringValue_(payload.improvements),
    source_page: stringValue_(payload.source_page),
    user_agent: stringValue_(payload.user_agent)
  };
}

function validatePayload_(payload) {
  if (!payload.course_slug) {
    throw new Error('Missing course_slug.');
  }

  if (!isValidRating_(payload.content_rating)) {
    throw new Error('Invalid content_rating.');
  }

  if (!isValidRating_(payload.instructor_rating)) {
    throw new Error('Invalid instructor_rating.');
  }

  if (!payload.strengths) {
    throw new Error('Missing strengths.');
  }

  if (!payload.improvements) {
    throw new Error('Missing improvements.');
  }

  if (payload.strengths.length > 2000 || payload.improvements.length > 2000) {
    throw new Error('Feedback text is too long.');
  }
}

function isValidRating_(value) {
  return ['1', '2', '3', '4', '5'].indexOf(String(value)) >= 0;
}

function getSheet_() {
  if (!SPREADSHEET_ID || SPREADSHEET_ID === 'PUT_YOUR_SPREADSHEET_ID_HERE') {
    throw new Error('Please set SPREADSHEET_ID in Code.gs before deploying.');
  }

  const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = spreadsheet.getSheetByName(SHEET_NAME) || spreadsheet.insertSheet(SHEET_NAME);
  return sheet;
}

function ensureHeaders_(sheet) {
  if (sheet.getLastRow() !== 0) return;
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  sheet.setFrozenRows(1);
}

function stringValue_(value) {
  return value == null ? '' : String(value).trim();
}

function jsonOutput_(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
