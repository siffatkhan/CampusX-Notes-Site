/* Sifat Notes — shared behavior: theme toggle, code copy, sidebar search/filter,
   math/code render init, and the end-of-topic quiz engine. */

function toggleTheme(){
  const html = document.documentElement;
  const isLight = html.getAttribute('data-theme') === 'light';
  html.setAttribute('data-theme', isLight ? 'dark' : 'light');
  syncThemeLabel();
}

function syncThemeLabel(){
  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  document.querySelectorAll('[data-theme-btn]').forEach(btn=>{
    const icon = btn.querySelector('[data-theme-icon]');
    const label = btn.querySelector('[data-theme-label]');
    if(icon) icon.textContent = isLight ? 'dark_mode' : 'light_mode';
    if(label) label.textContent = isLight ? 'Dark' : 'Light';
  });
}

function copyCode(btn){
  const code = btn.parentElement.querySelector('code').innerText;
  navigator.clipboard.writeText(code).then(()=>{
    const old = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(()=>btn.textContent = old, 1200);
  });
}

function toggleSidebar(){
  const el = document.getElementById('sidebarSlot');
  const backdrop = document.getElementById('sidebarBackdrop');
  if(el) el.classList.toggle('mobile-open');
  if(backdrop) backdrop.classList.toggle('hidden');
}

function filterNav(){
  const box = document.getElementById('searchBox');
  if(!box) return;
  const q = box.value.toLowerCase();
  const nav = document.getElementById('tocNav');
  nav.querySelectorAll('.sub-links a, a.flat').forEach(a=>{
    a.style.display = a.textContent.toLowerCase().includes(q) ? 'flex' : 'none';
  });
  nav.querySelectorAll('details').forEach(d=>{
    const anyVisible = [...d.querySelectorAll('.sub-links a')].some(a=>a.style.display !== 'none');
    d.style.display = (q === '' || anyVisible) ? 'block' : 'none';
    if(q !== '' && anyVisible) d.open = true;
  });
}

/* ---------------- Quiz engine ----------------
   Markup contract per question block:
   <div class="quiz-q" data-correct="2">
     <div class="quiz-options">
       <button class="quiz-option" data-index="0">...</button>
       ...
     </div>
     <div class="quiz-explanation hidden">...</div>
   </div>
   Container: <div class="quiz-block" data-quiz-id="...">...<button data-quiz-submit>Check Answers</button></div>
------------------------------------------------- */
function initQuiz(quizId){
  const block = document.querySelector(`[data-quiz-id="${quizId}"]`);
  if(!block) return;
  const questions = [...block.querySelectorAll('.quiz-q')];

  questions.forEach(q=>{
    q.querySelectorAll('.quiz-option').forEach(opt=>{
      opt.addEventListener('click', ()=>{
        if(block.dataset.submitted === 'true') return;
        q.querySelectorAll('.quiz-option').forEach(o=>o.classList.remove('ring-2', 'ring-[var(--primary)]'));
        opt.classList.add('ring-2', 'ring-[var(--primary)]');
        q.dataset.selected = opt.dataset.index;
      });
    });
  });

  const submitBtn = block.querySelector('[data-quiz-submit]');
  const resultEl = block.querySelector('[data-quiz-result]');
  submitBtn.addEventListener('click', ()=>{
    let score = 0;
    questions.forEach(q=>{
      const correct = q.dataset.correct;
      const selected = q.dataset.selected;
      q.querySelectorAll('.quiz-option').forEach(opt=>{
        opt.classList.remove('ring-2', 'ring-[var(--primary)]');
        opt.disabled = true;
        if(opt.dataset.index === correct) opt.classList.add('correct');
        else if(opt.dataset.index === selected) opt.classList.add('incorrect');
      });
      if(selected === correct) score++;
      const exp = q.querySelector('.quiz-explanation');
      if(exp) exp.classList.remove('hidden');
    });
    block.dataset.submitted = 'true';
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    if(resultEl){
      resultEl.classList.remove('hidden');
      resultEl.textContent = `Score: ${score} / ${questions.length}`;
    }
  });
}

document.addEventListener('DOMContentLoaded', function(){
  syncThemeLabel();
  if(!document.getElementById('sidebarSlot')){
    const menuBtn = document.getElementById('mobileMenuBtn');
    if(menuBtn) menuBtn.classList.add('hidden');
  }
  if(window.renderMathInElement){
    renderMathInElement(document.body, {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "\\(", right: "\\)", display: false}
      ]
    });
  }
  if(window.Prism) Prism.highlightAll();
  const searchBox = document.getElementById('searchBox');
  if(searchBox) searchBox.addEventListener('input', filterNav);
  document.querySelectorAll('[data-quiz-id]').forEach(b=>initQuiz(b.dataset.quizId));

  const tocNav = document.getElementById('tocNav');
  if(tocNav){
    tocNav.addEventListener('click', (e)=>{
      if(e.target.tagName === 'A' && window.innerWidth < 768) toggleSidebar();
    });
  }
});
