(() => {
  let sparkFrame;
  const playMetalSparks = () => {
    const canvas = document.querySelector('.metal-sparks');
    if (!canvas) return;
    cancelAnimationFrame(sparkFrame);
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    const ctx = canvas.getContext('2d');
    ctx.scale(ratio, ratio);
    const particles = Array.from({length:110}, () => {
      const angle = Math.random() * Math.PI * 2;
      const speed = width * (.12 + Math.random() * .65);
      return {vx:Math.cos(angle)*speed, vy:Math.sin(angle)*speed, life:.25+Math.random()*1.1, delay:Math.random()*.08, thickness:.3+Math.random()*.7};
    });
    const start = performance.now();
    const draw = now => {
      const time = (now-start)/1000-1.5;
      ctx.clearRect(0,0,width,height);
      if (time>=0) {
        ctx.globalCompositeOperation='lighter';
        for (const p of particles) {
          const age=time-p.delay;
          if(age<0 || age>p.life) continue;
          const tail=Math.max(0,age-.025);
          const x=t=>width*.5+p.vx*(1-Math.exp(-t*1.2))/1.2;
          const y=t=>height*.445+p.vy*(1-Math.exp(-t*1.2))/1.2+width*.22*t*t;
          const fade=Math.pow(1-age/p.life,1.4);
          ctx.strokeStyle=`rgba(255,${Math.round(105+fade*135)},${Math.round(30+fade*160)},${fade})`;
          ctx.lineWidth=p.thickness;
          ctx.beginPath();ctx.moveTo(x(tail),y(tail));ctx.lineTo(x(age),y(age));ctx.stroke();
        }
        if(time<.13){
          const flash=ctx.createRadialGradient(width*.5,height*.445,0,width*.5,height*.445,width*.12);
          flash.addColorStop(0,`rgba(255,251,224,${1-time/.13})`);flash.addColorStop(.15,`rgba(255,190,80,${.55*(1-time/.13)})`);flash.addColorStop(1,'rgba(255,90,10,0)');
          ctx.fillStyle=flash;ctx.fillRect(0,0,width,height);
        }
      }
      if(time<1.5) sparkFrame=requestAnimationFrame(draw);
      else ctx.clearRect(0,0,width,height);
    };
    sparkFrame=requestAnimationFrame(draw);
  };
  const replayCrest = () => {
    const emblem = document.querySelector('.crest-sequence');
    if (emblem) emblem.replaceWith(emblem.cloneNode(true));
    playMetalSparks();
  };
  document.querySelector('.guardian-stage')?.addEventListener('click', replayCrest);
  document.querySelector('.guardian-stage')?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      replayCrest();
      document.querySelector('.crest-sequence')?.focus();
    }
  });
  playMetalSparks();
})();
