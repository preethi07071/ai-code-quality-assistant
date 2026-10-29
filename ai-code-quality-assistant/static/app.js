const codeInput=document.getElementById("code"), languageInput=document.getElementById("language");
const analyzeBtn=document.getElementById("analyze-btn"), lineCount=document.getElementById("line-count");
const emptyState=document.getElementById("empty-state"), loading=document.getElementById("loading");
const report=document.getElementById("report"), errorBox=document.getElementById("error"), findingsBox=document.getElementById("findings");
function updateLineCount(){const n=codeInput.value.split("\n").length;lineCount.textContent=`${n} line${n===1?"":"s"}`;}
codeInput.addEventListener("input",updateLineCount);updateLineCount();
function showOnly(el){[emptyState,loading,report,errorBox].forEach(x=>x.classList.add("hidden"));if(el)el.classList.remove("hidden");}
function esc(v){return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function render(data){
 document.getElementById("total").textContent=data.summary.total;document.getElementById("high").textContent=data.summary.high;
 document.getElementById("medium").textContent=data.summary.medium;document.getElementById("other").textContent=data.summary.low+data.summary.info;
 document.getElementById("report-note").textContent=data.note;
 findingsBox.innerHTML=data.findings.length?data.findings.map(x=>`<article class="finding"><div class="finding-top"><span class="severity ${esc(x.severity)}">${esc(x.severity.toUpperCase())}</span><span class="line">LINE ${x.line}</span></div><h3>${esc(x.title)}</h3><p>${esc(x.explanation)}</p><div class="suggestion"><strong>Suggestion:</strong> ${esc(x.suggestion)}</div></article>`).join(""):'<div class="finding"><h3>No heuristic findings</h3><p>No issues were detected by these starter rules. This does not guarantee that the code is bug-free.</p></div>';
}
analyzeBtn.addEventListener("click",async()=>{analyzeBtn.disabled=true;showOnly(loading);try{
 const res=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code:codeInput.value,language:languageInput.value})});
 const data=await res.json();if(!res.ok)throw new Error(data.error||"Analysis failed.");render(data);showOnly(report);
 }catch(e){errorBox.textContent=e.message||"Could not connect to analyzer.";showOnly(errorBox);}finally{analyzeBtn.disabled=false;}});
document.getElementById("clear-btn").addEventListener("click",()=>{findingsBox.innerHTML="";showOnly(emptyState);});
