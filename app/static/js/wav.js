// In-browser 16 kHz Mono 16-bit PCM WAV conversion. OWNER: R4.
// No server-side ffmpeg needed: browser AudioContext does all the work.

/**
 * Convert an arbitrary audio blob (webm, ogg, etc.) to a 16 kHz mono 16-bit PCM WAV blob.
 * @param {Blob} blob - Raw audio blob from MediaRecorder.
 * @returns {Promise<Blob>} WAV blob ready for upload.
 */
async function convertTo16kHzMonoWav(blob) {
  var arrayBuffer = await blob.arrayBuffer();
  var AudioCtx = window.AudioContext || window.webkitAudioContext;
  var ctx = new AudioCtx();

  var decoded = await ctx.decodeAudioData(arrayBuffer);
  var targetSR = 16000;
  var offline = new OfflineAudioContext(
    1,
    Math.ceil(decoded.duration * targetSR),
    targetSR
  );

  var src = offline.createBufferSource();
  src.buffer = decoded;
  src.connect(offline.destination);
  src.start(0);

  var rendered = await offline.startRendering();
  await ctx.close();

  var ch = rendered.getChannelData(0);
  var n = ch.length;
  var buf = new ArrayBuffer(44 + n * 2);
  var v = new DataView(buf);

  function w(off, str) { for (var i = 0; i < str.length; i++) v.setUint8(off + i, str.charCodeAt(i)); }

  w(0, "RIFF");
  v.setUint32(4, 36 + n * 2, true);
  w(8, "WAVE");
  w(12, "fmt ");
  v.setUint32(16, 16, true);
  v.setUint16(20, 1, true);   // PCM
  v.setUint16(22, 1, true);   // mono
  v.setUint32(24, targetSR, true);
  v.setUint32(28, targetSR * 2, true);
  v.setUint16(32, 2, true);
  v.setUint16(34, 16, true);
  w(36, "data");
  v.setUint32(40, n * 2, true);

  var off = 44;
  for (var i = 0; i < n; i++) {
    var s = Math.max(-1, Math.min(1, ch[i]));
    v.setInt16(off, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    off += 2;
  }

  return new Blob([v], { type: "audio/wav" });
}
