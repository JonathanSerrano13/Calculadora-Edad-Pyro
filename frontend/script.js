function parseDate(s) {
  s = s.trim();
  const formats = [
    /^\d{2}\/\d{2}\/\d{4}$/, 
    /^\d{2}-\d{2}-\d{4}$/, 
    /^\d{4}-\d{2}-\d{2}$/
  ];
  if (formats[0].test(s) || formats[1].test(s)) {
    const sep = s.includes('/') ? '/' : '-';
    const [d, m, y] = s.split(sep).map(Number);
    return new Date(y, m - 1, d);
  }
  if (formats[2].test(s)) {
    const [y, m, d] = s.split('-').map(Number);
    return new Date(y, m - 1, d);
  }
  throw new Error('Formato de fecha no reconocido. Usa (Dia/Mes/Año) o (Año-Mes-Dia).');
}

function calculateAge(birthdate, today = new Date()) {
  let years = today.getFullYear() - birthdate.getFullYear();
  const beforeBirthday = (today.getMonth() < birthdate.getMonth()) ||
    (today.getMonth() === birthdate.getMonth() && today.getDate() < birthdate.getDate());
  if (beforeBirthday) years -= 1;
  return years;
}

function daysUntilNextBirthday(birthdate, today = new Date()) {
  const year = today.getFullYear();
  let next = new Date(year, birthdate.getMonth(), birthdate.getDate());
  // Manejo simple 29 de febrero
  if (isNaN(next.getTime())) {
    if (birthdate.getMonth() === 1 && birthdate.getDate() === 29) {
      next = new Date(year, 2, 1);
    } else {
      throw new Error('Fecha inválida');
    }
  }
  if (next < today) {
    next = new Date(year + 1, birthdate.getMonth(), birthdate.getDate());
    if (isNaN(next.getTime()) && birthdate.getMonth() === 1 && birthdate.getDate() === 29) {
      next = new Date(year + 1, 2, 1);
    }
  }
  // Normalizar horas para evitar problemas con timezone
  next.setHours(0,0,0,0);
  const t = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  return Math.round((next - t) / (1000 * 60 * 60 * 24));
}

function zodiacSign(birthdate) {
  const month = birthdate.getMonth() + 1;
  const day = birthdate.getDate();

  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) return 'Aries';
  if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) return 'Tauro';
  if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) return 'Géminis';
  if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) return 'Cáncer';
  if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) return 'Leo';
  if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) return 'Virgo';
  if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) return 'Libra';
  if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) return 'Escorpio';
  if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) return 'Sagitario';
  if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) return 'Capricornio';
  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) return 'Acuario';
  return 'Piscis';
}

const API_URL = '/api/calculate';

const signsEl = document.getElementById('signs');
const signResultEl = document.getElementById('signResult');
const out = document.getElementById('result');

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function showSignGrid(){
  if(signsEl) signsEl.style.display = '';
  if(signResultEl){ signResultEl.style.display = 'none'; signResultEl.innerHTML = ''; }
}

function showSingleSign(sign, element){
  if(signsEl) signsEl.style.display = 'none';
  if(signResultEl){
    signResultEl.style.display = 'flex';
    signResultEl.innerHTML = `<div class="sign-card large" data-sign="${sign}" data-element="${element}"><span class="symbol"></span><span class="name">${sign}</span></div>`;
  }
}

function renderResult(data) {
  if (!out) return;

  out.innerHTML = `
    <p>Tienes <strong>${escapeHtml(data.age)}</strong> años y naciste en <strong>${escapeHtml(data.weekday)}</strong>.</p>
    <p>Tu signo zodiacal es: <strong>${escapeHtml(data.sign)}</strong></p>
    <p>Tu próximo cumpleaños será dentro de: <strong>${escapeHtml(data.days_until_next_birthday)}</strong> días.</p>
    <p><strong>Llevas de vida:</strong></p>
    <div class="life-details">
      <p>En meses: <strong>${escapeHtml(data.months_lived)} meses.</strong></p>
      <p>En semanas: <strong>${escapeHtml(data.weeks_lived)} semanas.</strong></p>
      <p>En días: <strong>${escapeHtml(data.days_lived)} días.</strong></p>
    </div>
  `;
}

async function calculateWithPyro() {
  const input = document.getElementById('dob').value;
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ birthdate: input })
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'No se pudo obtener el resultado remoto.');
    }
    renderResult(data);
    showSingleSign(data.sign, data.element);
  } catch (e) {
    out.textContent = e.message;
    showSignGrid();
  }
}

document.getElementById('calc').addEventListener('click', calculateWithPyro);

document.getElementById('clear').addEventListener('click', () => {
  document.getElementById('dob').value = '';
  out.innerHTML = '';
  showSignGrid();
});

document.getElementById('dob').addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    calculateWithPyro();
  }
});

// Inicializar
showSignGrid();