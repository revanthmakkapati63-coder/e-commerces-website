// app/static/js/main.js
document.addEventListener('DOMContentLoaded',()=>{

  /* ---- Update cart badge via AJAX (optional, works when user adds/removes) ---- */
  const badge = document.getElementById('cart-badge');
  if(badge){
    fetch('{{ url_for("cart.view_cart") }}')
      .then(r=>r.text())
      .then(html=>{
        const cnt = (html.match(/cart-badge["']>\s*(\d+)/) || [])[1];
        if(cnt) badge.textContent = cnt;
      })
      .catch(()=>{});
  }

  /* ---- Deal countdown timer ---- */
  const cd = document.getElementById('dealCountdown');
  if(cd){
    const end = parseFloat(cd.dataset.end)*1000;   // ms since epoch
    const tick = ()=>{
      const diff = Math.max(0, end - Date.now());
      const h = String(Math.floor(diff/3.6e6)).padStart(2,'0');
      const m = String(Math.floor((diff%3.6e6)/6e4)).padStart(2,'0');
      const s = String(Math.floor((diff%6e4)/1000)).padStart(2,'0');
      cd.textContent = `Ends in ${h}:${m}:${s}`;
      if(diff) setTimeout(tick,1000);
    };
    tick();
  }
});