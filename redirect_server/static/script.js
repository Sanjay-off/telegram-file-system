/* ============================================================
   Countdown Script for Verification Redirect System
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const token = window.VERIFY_TOKEN || null;

    // Only run countdown logic if countdown element exists
    const countdownSpan = document.getElementById("countdown-seconds");

    if (!countdownSpan || !token) {
        return;
    }

    let seconds = parseInt(countdownSpan.innerText) || 10;

    const tick = () => {
        seconds -= 1;

        if (seconds <= 0) {
            // Timer complete → redirect to /return
            window.location.href = `/return?result=verified&token=${token}`;
            return;
        }

        countdownSpan.innerText = seconds;
        setTimeout(tick, 1000);
    };

    // Begin ticking
    setTimeout(tick, 1000);
});
