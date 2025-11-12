// Global variable to store the action confirmed by the modal
let modalActionCallback = null;

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
    
    // Setup modal handlers immediately on load
    setupModalHandlers();
});

// Function to handle showing the modal
function showModal(message, callback) {
    const overlay = document.getElementById('custom-modal-overlay');
    const msgElement = document.getElementById('modal-message');
    
    if (!overlay || !msgElement) {
        console.error("Custom modal elements not found.");
        return;
    }

    msgElement.textContent = message;
    modalActionCallback = callback;
    overlay.style.display = 'flex'; // Show the modal
}

// Function to hide the modal
function hideModal() {
    const overlay = document.getElementById('custom-modal-overlay');
    if (overlay) {
        overlay.style.display = 'none';
        modalActionCallback = null; // Clear the stored callback
    }
}

// Setup event listeners for the modal buttons
function setupModalHandlers() {
    const confirmBtn = document.getElementById('modal-confirm-btn');
    const cancelBtn = document.getElementById('modal-cancel-btn');

    if (confirmBtn) {
        confirmBtn.onclick = () => {
            if (modalActionCallback) {
                modalActionCallback(true); // Execute the confirmation action
            }
            hideModal();
        };
    }

    if (cancelBtn) {
        cancelBtn.onclick = () => {
            hideModal(); // Simply hide the modal on cancel
        };
    }
}

// Generic confirmDelete now calls the custom modal
function confirmDelete(id) {
    if (id === null || id === undefined) return;
    
    let base = '/users/delete/';
    const path = window.location.pathname.toLowerCase();
    let dashboardType = 'Unknown';
    
    // Determine the base path based on URL segment
    if (path.includes('/courses')) {
        base = '/courses/delete/';
        dashboardType = 'Courses';
    } else if (path.includes('/enrollments')) {
        base = '/enrollments/delete/';
        dashboardType = 'Enrollments';
    } else if (path.includes('/instructors')) {
        base = '/instructors/delete/';
        dashboardType = 'Instructors';
    } else if (path.includes('/users')) {
        base = '/users/delete/';
        dashboardType = 'Users';
    } else {
        console.error("Could not determine deletion route for current path.");
        return; 
    }

    // --- DEBUGGING STEP ---
    const finalUrl = base + id;
    console.log(`[DELETE] Dashboard: ${dashboardType}, ID: ${id}, Target URL: ${finalUrl}`);
    // ----------------------

    // Show the custom confirmation modal
    showModal(
        'Are you sure you want to delete this item? This action cannot be undone.', 
        (isConfirmed) => {
            if (isConfirmed) {
                // Execute the redirect if confirmed
                window.location.href = finalUrl;
            }
        }
    );
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