// 상태 관리
let todos = JSON.parse(localStorage.getItem('todos') || '[]');
let currentFilter = 'all';

// DOM 요소
const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');
const countEl = document.getElementById('count');
const clearBtn = document.getElementById('clear-completed');
const filterBtns = document.querySelectorAll('.filter-btn');

// 저장
function save() {
  localStorage.setItem('todos', JSON.stringify(todos));
}

// 렌더링
function render() {
  const filtered = todos.filter(t => {
    if (currentFilter === 'active') return !t.done;
    if (currentFilter === 'completed') return t.done;
    return true;
  });

  list.innerHTML = '';

  if (filtered.length === 0) {
    list.innerHTML = '<p class="empty-msg">할일이 없습니다 🎉</p>';
  } else {
    filtered.forEach(todo => {
      const li = document.createElement('li');
      if (todo.done) li.classList.add('completed');

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = todo.done;
      checkbox.addEventListener('change', () => toggle(todo.id));

      const span = document.createElement('span');
      span.className = 'todo-text';
      span.textContent = todo.text;

      const delBtn = document.createElement('button');
      delBtn.className = 'delete-btn';
      delBtn.textContent = '✕';
      delBtn.title = '삭제';
      delBtn.addEventListener('click', () => remove(todo.id));

      li.appendChild(checkbox);
      li.appendChild(span);
      li.appendChild(delBtn);
      list.appendChild(li);
    });
  }

  // 카운트 업데이트
  const remaining = todos.filter(t => !t.done).length;
  countEl.textContent = `미완료 ${remaining}개`;
}

// 추가
function addTodo(text) {
  todos.push({ id: Date.now(), text: text.trim(), done: false });
  save();
  render();
}

// 완료 토글
function toggle(id) {
  todos = todos.map(t => t.id === id ? { ...t, done: !t.done } : t);
  save();
  render();
}

// 삭제
function remove(id) {
  todos = todos.filter(t => t.id !== id);
  save();
  render();
}

// 이벤트 핸들러
form.addEventListener('submit', e => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addTodo(text);
  input.value = '';
  input.focus();
});

clearBtn.addEventListener('click', () => {
  todos = todos.filter(t => !t.done);
  save();
  render();
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    currentFilter = btn.dataset.filter;
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  });
});

// 초기 렌더링
render();
