---
title: Private Notes
layout: default
permalink: /privatenotes.html
---

<div id="secret-wrapper" style="display:none;" markdown="1">

# Private Notes

This is private-ish content.

- Secret note 1
- Secret note 2

</div>

<div id="locked" style="text-align:center;">
  <h2>Access required</h2>
  <p>To view these notes, enter the access key.</p>
  <p>To be honest, the notes here are not very private and discovering the password is relatively easy. </p>
  <p>If you can do it, you deserve to access my notes.</p>
  <input id="pw" type="password" placeholder="Access key" autocomplete="off" />
  <button id="ok">Enter</button>
  <p id="err" style="display:none;color:#b91c1c">Wrong key — try again.</p>
</div>

<script>
async function sha256hex(str) {
  const enc = new TextEncoder();
  const data = enc.encode(str);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2,'0')).join('');
}

// SHA-256 of your password "melikeyiçokseviyorum"
const STORED_HASH = "1abbb79ae5895f05c617304b7e64b0a36f367d15ada33a5483bd6270ffb3d1e4";

document.getElementById('ok').addEventListener('click', async () => {
  const v = document.getElementById('pw').value || "";
  const hv = await sha256hex(v);
  if (hv === STORED_HASH) {
    document.getElementById('secret-wrapper').style.display = 'block';
    document.getElementById('locked').style.display = 'none';
  } else {
    document.getElementById('err').style.display = 'block';
    document.getElementById('pw').value = '';
    document.getElementById('pw').focus();
  }
});
</script>
