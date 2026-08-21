<!doctype html>
<meta charset="utf-8">
<!-- Alle Maße sind viewport-relativ (vh/vw), damit das Layout unabhängig von
     der Render-Skalierung exakt das 4:5-Bild füllt. Referenz: 1080x1350. -->
<style>
  :root { --accent: #7CC7EC; }
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:100%; height:100%; overflow:hidden; background:#0b0c0e; }
  .slide { position:fixed; inset:0;
           font-family:"Liberation Sans","Helvetica Neue",Helvetica,Arial,sans-serif;
           -webkit-font-smoothing:antialiased; }
  .photo { position:absolute; inset:0; width:100%; height:100%;
           object-fit:cover; object-position:__FOCUS__; }
  .veil  { position:absolute; inset:0;
           background:linear-gradient(to bottom,
             rgba(0,0,0,.45) 0%, rgba(0,0,0,.10) 28%,
             rgba(0,0,0,.35) 58%, rgba(0,0,0,.82) 100%); }
  .counter { position:absolute; top:4.6vh; left:6.3vw; font-weight:700;
             font-size:__CSIZE__; letter-spacing:__CTRACK__;
             color:__CCOLOR__; text-shadow:0 .15vh 1vh rgba(0,0,0,.5); }
  .block { position:absolute; left:6.3vw; right:6.3vw; bottom:7.1vh; }
  h1 { color:#fff; font-weight:700; font-size:__HSIZE__; line-height:1.06;
       letter-spacing:-.015em; text-shadow:0 .15vh 1.8vh rgba(0,0,0,.55); }
  h1 em { color:var(--accent); font-style:italic; }
  .rule { width:7.2vw; height:.3vh; background:var(--accent);
          margin:2.2vh 0 1.6vh; border-radius:.15vh; }
  p { color:rgba(255,255,255,.94); font-size:__BSIZE__; line-height:1.42;
      max-width:__BWIDTH__; text-shadow:0 .15vh 1.2vh rgba(0,0,0,.6); }
</style>
<div class="slide">
  __PHOTO__
  <div class="veil"></div>
  <div class="counter">__COUNTER__</div>
  <div class="block">
    <h1>__HEADLINE__</h1>
    <div class="rule"></div>
    __BODY__
  </div>
</div>
