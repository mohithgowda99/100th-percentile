let currentSession=[];
let currentIndex=0;
let selectedIndex=null;
let startedAt=0;
let timerId=null;

const $=(id)=>document.getElementById(id);

function showView(id){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.view===id));
  $(id).classList.add('active');
}

document.querySelectorAll('.tab').forEach(btn=>btn.addEventListener('click',()=>showView(btn.dataset.view)));

async function loadDashboard(){
  const data=await fetch('/api/dashboard').then(r=>r.json());
  $('days').textContent=data.days_remaining;
  $('attempts').textContent=data.summary.attempts;
  $('accuracy').textContent=Math.round(data.summary.accuracy*100)+'%';
  $('avgTime').textContent=Math.round(data.summary.avg_seconds)+'s';
  $('mockScore').textContent=data.latest_mock?.total_score ?? '—';
  if(data.top_recommendation){
    $('focusTarget').textContent=data.top_recommendation.target_id.replaceAll('_',' ');
    $('focusWhy').textContent='Why now: '+data.top_recommendation.reason_codes.join(' · ').replaceAll('_',' ').toLowerCase();
  }
}

async function loadAtlas(){
  const data=await fetch('/api/atlas').then(r=>r.json());
  $('atlasGrid').innerHTML=data.map(a=>`
    <article class="atlas-card">
      <p class="eyebrow">${a.id}</p>
      <h3>${a.name}</h3>
      <p class="muted">${a.question_count} current seed question${a.question_count===1?'':'s'}</p>
      <div class="chips">${a.skills.map(s=>`<span class="chip">${s.replaceAll('_',' ')}</span>`).join('')}</div>
    </article>
  `).join('');
}

async function startSession(mode='foundation'){
  const data=await fetch('/api/session?mode='+mode+'&limit=8').then(r=>r.json());
  currentSession=data.questions;
  currentIndex=0;
  $('trainStart').classList.add('hidden');
  $('trainer').classList.remove('hidden');
  showView('train');
  renderQuestion();
}

function renderQuestion(){
  const q=currentSession[currentIndex];
  selectedIndex=null;
  $('feedback').classList.add('hidden');
  $('submitAnswer').disabled=true;
  $('questionCounter').textContent=`${currentIndex+1} / ${currentSession.length}`;
  $('difficulty').textContent='Difficulty '+q.difficulty;
  $('prompt').textContent=q.prompt;
  $('options').innerHTML=q.options.map((o,i)=>`<button class="option" data-index="${i}">${String.fromCharCode(65+i)}. ${o}</button>`).join('');
  document.querySelectorAll('.option').forEach(btn=>btn.addEventListener('click',()=>{
    selectedIndex=Number(btn.dataset.index);
    document.querySelectorAll('.option').forEach(x=>x.classList.remove('selected'));
    btn.classList.add('selected');
    $('submitAnswer').disabled=false;
  }));
  startedAt=Date.now();
  clearInterval(timerId);
  timerId=setInterval(()=>{
    const sec=Math.floor((Date.now()-startedAt)/1000);
    $('timer').textContent=`${Math.floor(sec/60)}:${String(sec%60).padStart(2,'0')}`;
  },250);
}

$('confidence').addEventListener('input',e=>$('confidenceValue').textContent=e.target.value+'%');

$('submitAnswer').addEventListener('click',async()=>{
  if(selectedIndex===null)return;
  clearInterval(timerId);
  const q=currentSession[currentIndex];
  const seconds=(Date.now()-startedAt)/1000;
  const payload={
    question_id:q.id,
    selected_index:selectedIndex,
    response_seconds:seconds,
    confidence:Number($('confidence').value)/100
  };
  const res=await fetch('/api/attempt',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data=await res.json();
  document.querySelectorAll('.option').forEach(x=>x.disabled=true);
  $('feedback').classList.remove('hidden');
  $('verdict').textContent=data.correct?'Correct':'Missed';
  $('verdict').className='verdict '+(data.correct?'good':'bad');
  $('archetype').textContent=data.archetype_name;
  $('skeleton').textContent=data.skeleton;
  $('trap').textContent=data.trap;
  $('explanation').textContent=data.explanation;
  $('submitAnswer').disabled=true;
  loadDashboard();
});

$('nextQuestion').addEventListener('click',()=>{
  currentIndex++;
  if(currentIndex>=currentSession.length){
    $('trainer').classList.add('hidden');
    $('trainStart').classList.remove('hidden');
    loadDashboard();
    return;
  }
  renderQuestion();
});

document.querySelectorAll('.mode-card').forEach(btn=>btn.addEventListener('click',()=>startSession(btn.dataset.mode)));
$('startToday').addEventListener('click',()=>startSession('foundation'));

$('mockForm').addEventListener('submit',async(e)=>{
  e.preventDefault();
  const fd=new FormData(e.target);
  const obj={};
  for(const [k,v] of fd.entries()){
    obj[k]=v===''?null:v;
  }
  for(const key of ['total_score','quant_score','verbal_score','di_score']){
    if(obj[key]!==null)obj[key]=Number(obj[key]);
  }
  const res=await fetch('/api/mock',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(obj)});
  $('mockStatus').textContent=res.ok?'Saved. This is now part of your calibration history.':'Could not save mock.';
  if(res.ok){e.target.reset();loadDashboard();}
});

loadDashboard();
loadAtlas();
