// Get DOM elements
const feedbackBtn = document.getElementById('feedbackBtn');
const feedbackPanel = document.getElementById('feedbackPanel');
const confirmationPanel = document.getElementById('confirmationPanel');
const errorPanel = document.getElementById('errorPanel');
const overlay = document.getElementById('overlay');
const cancelBtn = document.getElementById('cancelBtn');
const closeBtn = document.getElementById('closeBtn');
const confirmationCloseBtn = document.getElementById('confirmationCloseBtn');

// Function to open the feedback panel
function openFeedbackPanel() {
  feedbackPanel.classList.add('open');
  overlay.style.display = 'block';

  // Small delay to ensure the display change happens before the opacity transition
  setTimeout(() => {
    overlay.classList.add('visible');
  }, 10);

  document.body.style.overflow = 'hidden'; // Disable scrolling
}

// Function to close the feedback panel
function closeFeedbackPanel() {
  feedbackPanel.classList.remove('open');

  // Only close overlay if other panels are not open
  if ((!confirmationPanel || !confirmationPanel.classList.contains('open')) && 
      (!errorPanel || !errorPanel.classList.contains('open'))) {
    overlay.classList.remove('visible');

    // Wait for the transition to complete before hiding the overlay
    setTimeout(() => {
      overlay.style.display = 'none';
    }, 300);

    document.body.style.overflow = 'auto'; // Re-enable scrolling
  }
}

// Function to open the confirmation panel
function openConfirmationPanel() {
  console.log("Opening confirmation panel");
  
  // First close the feedback panel if it's open
  if (feedbackPanel && feedbackPanel.classList.contains('open')) {
    feedbackPanel.classList.remove('open');
  }

  // Show overlay if not already visible
  if (overlay && overlay.style.display !== 'block') {
    overlay.style.display = 'block';
    setTimeout(() => {
      overlay.classList.add('visible');
    }, 10);
    document.body.style.overflow = 'hidden';
  }

  // Open confirmation panel
  if (confirmationPanel) {
    setTimeout(() => {
      confirmationPanel.classList.add('open');
    }, 300);
  }
}

// Function to close the confirmation panel
function closeConfirmationPanel() {
  if (!confirmationPanel) return;
  
  confirmationPanel.classList.remove('open');
  
  // Only close overlay if other panels are not open
  if ((!feedbackPanel || !feedbackPanel.classList.contains('open')) && 
      (!errorPanel || !errorPanel.classList.contains('open'))) {
    if (overlay) {
      overlay.classList.remove('visible');
      
      // Wait for the transition to complete before hiding the overlay
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 300);
    }
    
    document.body.style.overflow = 'auto'; // Re-enable scrolling
  }
}

// Function to open the error panel
function openErrorPanel() {
  console.log("Opening error panel");
  
  // First close the feedback panel if it's open
  if (feedbackPanel && feedbackPanel.classList.contains('open')) {
    feedbackPanel.classList.remove('open');
  }

  // Show overlay if not already visible
  if (overlay && overlay.style.display !== 'block') {
    overlay.style.display = 'block';
    setTimeout(() => {
      overlay.classList.add('visible');
    }, 10);
    document.body.style.overflow = 'hidden';
  }

  // Open error panel
  if (errorPanel) {
    setTimeout(() => {
      errorPanel.classList.add('open');
    }, 300);
  }
}

// Function to close the error panel
function closeErrorPanel() {
  if (!errorPanel) return;
  
  errorPanel.classList.remove('open');
  
  // Only close overlay if other panels are not open
  if ((!feedbackPanel || !feedbackPanel.classList.contains('open')) && 
      (!confirmationPanel || !confirmationPanel.classList.contains('open'))) {
    if (overlay) {
      overlay.classList.remove('visible');
      
      // Wait for the transition to complete before hiding the overlay
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 300);
    }
    
    document.body.style.overflow = 'auto'; // Re-enable scrolling
  }
}

// Event listeners
if (feedbackBtn) {
  feedbackBtn.addEventListener('click', openFeedbackPanel);
}

if (cancelBtn) {
  cancelBtn.addEventListener('click', closeFeedbackPanel);
}

if (confirmationCloseBtn) {
  confirmationCloseBtn.addEventListener('click', closeConfirmationPanel);
}

if (closeBtn) {
  closeBtn.addEventListener('click', closeErrorPanel);
}

// Close panels with overlay click
if (overlay) {
  overlay.addEventListener('click', function() {
    if (feedbackPanel && feedbackPanel.classList.contains('open')) {
      closeFeedbackPanel();
    } else if (confirmationPanel && confirmationPanel.classList.contains('open')) {
      closeConfirmationPanel();
    } else if (errorPanel && errorPanel.classList.contains('open')) {
      closeErrorPanel();
    }
  });
}

// Close panels with Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    if (feedbackPanel && feedbackPanel.classList.contains('open')) {
      closeFeedbackPanel();
    } else if (confirmationPanel && confirmationPanel.classList.contains('open')) {
      closeConfirmationPanel();
    } else if (errorPanel && errorPanel.classList.contains('open')) {
      closeErrorPanel();
    }
  }
});

// Check if we need to show confirmation or error panel on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM loaded, checking for panels to show");
  
  // If Django set is_sent to true, show confirmation panel
  if (confirmationPanel && confirmationPanel.dataset.show === 'true') {
    console.log("Should show confirmation panel based on data attribute");
    openConfirmationPanel();
  }
  
  // If Django set is_error to true, show error panel
  if (errorPanel && errorPanel.dataset.show === 'true') {
    console.log("Should show error panel based on data attribute");
    openErrorPanel();
  }
});