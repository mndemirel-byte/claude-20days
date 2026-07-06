# -*- coding: utf-8 -*-
"""
HTML kabuğu — CSS tokens.css'ten okunur ve standalone HTML'e gömülür.

Tek stil kaynağı: generators/tokens.css
  • Bu modül, tokens.css'i import anında okur → CSS değişkeni her build'de güncel olur.
  • React app için: tokens.css → frontend/src/tokens.css kopyalanır ve import edilir.
"""
import os as _os

_HERE = _os.path.dirname(_os.path.abspath(__file__))

def _load_tokens():
    path = _os.path.join(_HERE, "tokens.css")
    with open(path, encoding="utf-8") as f:
        return f.read()

# Build anında tokens.css okunur; HTML'e satır içi gömülür → tam standalone dosya.
CSS = _load_tokens()

JS = r"""
(function(){
  var day = window.__CCEDU_DAY__ || 1;
  var ns = "ccedu:v1:day" + day + ":";
  var boxes = Array.prototype.slice.call(document.querySelectorAll('input[type=checkbox][data-k]'));
  boxes.forEach(function(b){
    try{ if(localStorage.getItem(ns + b.dataset.k) === "1") b.checked = true; }catch(e){}
    b.addEventListener('change', function(){
      try{ localStorage.setItem(ns + b.dataset.k, b.checked ? "1":"0"); }catch(e){}
      update();
    });
  });
  var finals = boxes.filter(function(b){ return b.dataset.final === "1"; });
  var bar = document.querySelector('.topbar .prog>span');
  var lab = document.querySelector('.topbar .proglabel');
  function update(){
    var done = finals.filter(function(b){return b.checked;}).length;
    var pct = finals.length ? Math.round(done*100/finals.length) : 0;
    if(bar) bar.style.width = pct + "%";
    if(lab) lab.textContent = "Gün " + day + " · %" + pct;
    try{ localStorage.setItem("ccedu:v1:dayDone:"+day, (finals.length && done===finals.length)?"1":"0"); }catch(e){}
  }
  update();
  document.querySelectorAll('.copybtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var pre = btn.parentElement.querySelector('pre');
      if(!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(function(){
        var t = btn.textContent; btn.textContent = "kopyalandı ✓";
        setTimeout(function(){ btn.textContent = t; }, 1400);
      });
    });
  });
  var mb = document.querySelector('.menu-btn'), scrim = document.querySelector('.scrim');
  if(mb) mb.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
  if(scrim) scrim.addEventListener('click', function(){ document.body.classList.remove('nav-open'); });
})();
"""

PAGE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<style>%%CSS%%</style>
</head>
<body>
<header class="topbar">
  <button class="menu-btn" aria-label="Menü">☰</button>
  <a class="brand" href="index.html">Claude Code <b>Master</b></a>
  <div class="prog"><span></span></div>
  <span class="proglabel"></span>
</header>
<div class="scrim"></div>
<div class="layout">
  <aside class="sidebar">%%SIDEBAR%%</aside>
  <div class="main"><article class="content">%%CONTENT%%</article></div>
</div>
<script>window.__CCEDU_DAY__=%%DAY%%;</script>
<script>%%JS%%</script>
</body>
</html>
"""
