// ===== Basic Dashboard Animation =====
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, i) => {
    card.style.opacity = "0";
    setTimeout(() => {
      card.style.transition = "all 0.5s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, i * 150);
  });
});

// Generic confirmDelete that infers route from current path
function confirmDelete(id) {
  if (!id && id !== 0) return;
  let base = '/users/delete/';
  const path = window.location.pathname.toLowerCase();
  if (path.indexOf('/courses') !== -1) base = '/courses/delete/';
  else if (path.indexOf('/enrollments') !== -1) base = '/enrollments/delete/';
  else if (path.indexOf('/instructors') !== -1) base = '/instructors/delete/';

  if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
    window.location.href = base + id;
  }
}

// show/hide add/view forms (safe: checks for existence)
function showAddMode() {
  const add = document.getElementById('addForm');
  const view = document.getElementById('viewForm');
  if (add) add.style.display = 'block';
  if (view) view.style.display = 'none';
  const focusable = add ? add.querySelector('input, textarea, select') : null;
  if (focusable) focusable.focus();
}

function showViewMode() {
  const add = document.getElementById('addForm');
  const view = document.getElementById('viewForm');
  if (view) view.style.display = 'block';
  if (add) add.style.display = 'none';
}

// Auto-hide alerts after 4s
document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease-out';
    }, 4000);
  });
});
