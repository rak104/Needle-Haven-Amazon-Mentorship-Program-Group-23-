window.addEventListener('scroll', function() {
    const headerRight = document.querySelector('.header-right');
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

    // Calculate the percentage of the page that has been scrolled
    const scrollPercentage = scrollY / maxScroll;

    // Calculate the new width based on the scroll percentage
    const minWidth = 205; // Initial width in pixels
    const maxWidth = window.innerWidth; // Full width
    const newWidth = minWidth + (maxWidth - minWidth) * scrollPercentage;

    // Set the new width of the header-right
    headerRight.style.width = `${newWidth}px`;
});

function getGreetingMessage() {
    const currentHour = new Date().getHours();
    let greeting;

    if (currentHour < 12) {
        greeting = 'Good Morning!';
    } else if (currentHour < 18) {
        greeting = 'Good Afternoon!';
    } else {
        greeting = 'Good Evening!';
    }

    return greeting;
}

document.addEventListener('DOMContentLoaded', () => {
    const greetingElement = document.getElementById('greeting');
    greetingElement.textContent = getGreetingMessage();
});

document.addEventListener('DOMContentLoaded', () => {
    const bubbleContainer = document.querySelector('.bubble-container');
    const totalBubbles = 20;
    const tripleBubbles = totalBubbles / 4;

    for (let i = 0; i < totalBubbles; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.classList.add(i < tripleBubbles ? 'green' : i < 2*tripleBubbles ? 'pink':i< 3*tripleBubbles?'blue':'yellow');
        const size = Math.random() * 60 + 20;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${Math.random() * 100}%`;
        bubble.style.animationDuration = `${Math.random() * 5 + 3}s`;
        bubbleContainer.appendChild(bubble);
    }
});