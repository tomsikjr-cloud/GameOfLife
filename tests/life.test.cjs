const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const script = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
function app() {
  const elements = new Map(), timers = new Map(); let serial = 0;
  const context = vm.createContext({ Uint8Array, document: { getElementById(id) {
    if (!elements.has(id)) elements.set(id, { width: 960, height: 640, value: '', disabled: false,
      addEventListener() {}, getContext: () => new Proxy({}, { get: () => () => {} }) });
    return elements.get(id);
  } }, setTimeout(fn) { const id = ++serial; timers.set(id, fn); return id; }, clearTimeout(id) { timers.delete(id); } });
  vm.runInContext(script, context);
  return { run: code => vm.runInContext(code, context), elements, timers };
}
function board(cells) { const grid = new Uint8Array(2400); for (const [x,y] of cells) grid[y*60+x] = 1; return grid; }
function step(grid) { const a = app(); a.run('globalThis.step = nextGeneration'); return a.run('step')(grid); }
test('block remains stable; isolated cell dies; input is unchanged', () => {
  const block = board([[5,5],[6,5],[5,6],[6,6]]);
  assert.deepEqual(step(block), block);
  const single = board([[5,5]]); assert.equal(step(single).some(Boolean), false); assert.equal(single[305], 1);
});
test('blinker has period two, including across wrapping edges', () => {
  for (const y of [0,20,39]) {
    const horizontal = board([[59,y],[0,y],[1,y]]);
    const vertical = board([[0,(y+39)%40],[0,y],[0,(y+1)%40]]);
    assert.deepEqual(step(horizontal), vertical); assert.deepEqual(step(vertical), horizontal);
  }
});
test('glider moves diagonally after four generations', () => {
  const cells = [[1,0],[2,1],[0,2],[1,2],[2,2]]; let grid = board(cells);
  for(let i=0;i<4;i++) grid = step(grid);
  assert.deepEqual(grid, board(cells.map(([x,y]) => [x+1,y+1])));
});
test('pulsar repeats after three generations', () => {
  const a = app(); a.run("$('pattern').onchange({target:{value:'pulsar'}}); globalThis.initial = grid.slice(); advance(); advance(); advance();");
  assert.equal(a.run('grid.every((v,i) => v === initial[i])'), true);
});
test('Forward, single Back, edits, and reset maintain consistent history', () => {
  const a=app(); a.run("$('pattern').onchange({target:{value:'blinker'}}); $('forward').onclick();");
  assert.equal(a.run('generation'),1); assert.equal(a.elements.get('back').disabled,false);
  a.run("$('back').onclick(); $('back').onclick();"); assert.equal(a.run('generation'),0);
  a.run("$('forward').onclick(); edit(0,1);"); assert.equal(a.run('previous'),null);
  a.run("$('clear').onclick();"); assert.equal(a.run('generation'),0); assert.equal(a.run('grid.some(Boolean)'),false);
});
test('rapid stop/start and speed changes never duplicate the playback timer', () => {
  const a=app(); a.run("$('pattern').onchange({target:{value:'blinker'}}); $('start').onclick();");
  assert.equal(a.timers.size,1); assert.equal(a.elements.get('forward').disabled,true);
  a.run("$('start').onclick(); changeSpeed(25);"); assert.equal(a.timers.size,1);
  a.run("$('stop').onclick();"); assert.equal(a.timers.size,0);
  a.run("$('start').onclick(); $('stop').onclick(); $('start').onclick();"); assert.equal(a.timers.size,1);
  a.run('changeSpeed(99)'); assert.equal(a.run('speed'),25);
  a.run('changeSpeed(-1)'); assert.equal(a.run('speed'),1);
});
test('extinction stops playback without scheduling a new timer', () => {
  const a=app(); a.run("edit(0,1); $('start').onclick();");
  assert.equal(a.run('running'),false); assert.equal(a.timers.size,0);
  assert.equal(a.elements.get('status').textContent,'No living cells');
});
